"""ORM models."""

from __future__ import annotations
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator, Set, Union
from uuid import uuid4

from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import Expression
from peewee import ForeignKeyField
from peewee import TextField
from peewee import UUIDField

from filedb import File
from his.orm import Account
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel

from hinews import dom  # pylint: disable=E0611
from hinews.config import CONFIG
from hinews.exceptions import InvalidTag
from hinews.watermark import watermark


__all__ = [
    'create_tables',
    'article_active',
    'Article',
    'Editor',
    'Image',
    'TagList',
    'Tag',
    'Whitelist',
    'AccessToken',
    'MODELS'
]


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


def create_tables(fail_silently: bool = False):
    """Creates all tables."""

    for model in MODELS:
        model.create_table(fail_silently=fail_silently)


def article_active() -> Expression:
    """Yields article active query."""

    today = date.today()
    return (
        ((Article.active_from >> None) | (Article.active_from <= today))
        & ((Article.active_until >> None) | (Article.active_until >= today)))


@lru_cache()
def _cached_account_info(ident: int) -> Account:
    """Returns the respective author by its ID."""

    return Account.get(Account.id == ident).to_json()


class _NewsModel(JSONModel):
    """Basic news database model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Article(_NewsModel):
    """A news-related text."""

    author = ForeignKeyField(Account, column_name='author')
    created = DateTimeField(default=datetime.now)
    active_from = DateField(null=True)
    active_until = DateField(null=True)
    title = CharField(255)
    subtitle = CharField(255, null=True)
    text = TextField()
    source = TextField(null=True)

    @classmethod
    def from_json(cls, json: dict, author: Account, **kwargs) -> Article:
        """Creates a new article from a JSON-ish dict."""
        article = super().from_json(json, **kwargs)
        article.author = author
        return article

    @property
    def customers(self) -> Set[Customer]:
        """Returns a frozen set of customers that
        are whitelisted for this article.
        """
        return frozenset(whitelist.customer for whitelist in self.whitelist)

    def update_tags(self, tags: Iterable[str]) -> Iterator[Tag]:
        """Updates the respective tags."""
        if tags is None:
            return

        for tag in self.tags:
            tag.delete_instance()

        if not tags:
            return

        for tag in tags:
            yield Tag.add(self, tag)

    def update_customers(self, cids: Iterable[int]) -> Iterator[Whitelist]:
        """Updates the respective customers."""
        if cids is None:
            return

        for whitelist in self.whitelist:
            whitelist.delete_instance()

        if not cids:
            return

        for cid in cids:
            yield Whitelist.add(self, cid)

    def to_json(self, preview: bool = False, fk_fields: bool = True,
                **kwargs) -> dict:
        """Returns a JSON-ish dictionary."""
        if preview:
            fk_fields = False

        dictionary = super().to_json(fk_fields=fk_fields, **kwargs)
        dictionary['images'] = [
            image.to_json(preview=preview) for image in self.images]
        dictionary['tags'] = [
            tag.to_json(preview=preview) for tag in self.tags]

        if not preview:
            dictionary['author'] = _cached_account_info(self.author_id)
            dictionary['editors'] = [
                editor.to_json() for editor in self.editors]
            dictionary['customers'] = [
                customer.to_json() for customer in self.customers]

        return dictionary

    def to_dom(self, local: bool = False) -> dom.Article:
        """Converts the article into a XML DOM model."""
        article = dom.Article()
        article.created = self.created
        article.active_from = self.active_from
        article.active_until = self.active_until
        article.title = self.title
        article.subtitle = self.subtitle
        article.text = self.text
        article.source = self.source
        article.tag = [tag.tag for tag in self.tags]

        if not local:
            article.id = self.id
            article.image = [image.to_dom() for image in self.images]

        return article

    def delete_instance(self, recursive: bool = False,
                        delete_nullable: bool = False):
        """Deletes the article."""
        # Manually delete all referencing images to ensure
        # deletion of the respective filedb entries.
        for image in self.images:
            image.delete_instance()

        return super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class Editor(_NewsModel):
    """An article's editor."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'editor'

    article = ForeignKeyField(
        Article, column_name='article', backref='editors', on_delete='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    timestamp = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, article: Article, account: Account) -> Editor:
        """Adds a new author record to the respective article."""
        try:
            return cls.get((cls.article == article) & (cls.account == account))
        except cls.DoesNotExist:
            return cls(article=article, account=account)

    def to_json(self, *args, **kwargs) -> dict:
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_json(*args, **kwargs)
        dictionary['account'] = self.account.info
        return dictionary


class Image(_NewsModel):
    """An image of an article."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'image'

    article = ForeignKeyField(
        Article, column_name='article', backref='images', on_delete='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    file = ForeignKeyField(File, column_name='file')
    uploaded = DateTimeField()
    source = TextField(null=True)

    @classmethod
    def add(cls, article: Article, account: Account, bytes_: bytes,
            metadata: dict) -> Image:
        """Adds the respective image data to the article."""
        image = cls()
        image.article = article
        image.account = account
        image.file = File.from_bytes(bytes_)
        image.uploaded = datetime.now()
        image.source = metadata['source']
        return image

    @property
    def bytes(self) -> bytes:
        """Returns the file's bytes."""
        return self.file.bytes

    @property
    def watermarked(self) -> bytes:
        """Returns a watermarked image."""
        return watermark(self.bytes, f'Quelle: {self.oneliner}')

    @property
    def oneliner(self) -> str:
        """Returns the source text as a one-liner."""
        return ' '.join(self.source.split('\n'))

    def patch_json(self, json: dict):
        """Patches the image metadata with the respective dictionary."""
        return super().patch_json(json, skip={'uploaded'}, fk_fields=False)

    def to_json(self, preview: bool = False, fk_fields: bool = True,
                **kwargs) -> dict:
        """Returns a JSON-compliant integer."""
        if preview:
            fk_fields = False

        dictionary = super().to_json(fk_fields=fk_fields, **kwargs)

        if not preview:
            dictionary['account'] = _cached_account_info(self.account_id)

        dictionary['mimetype'] = self.file.mimetype
        return dictionary

    def to_dom(self, filename: Union[Path, str] = None) -> dom.Image:
        """Converts the image into a XML DOM model."""
        image = dom.Image()
        image.uploaded = self.uploaded
        image.source = self.source
        image.mimetype = self.file.mimetype

        if filename is None:
            image.id = self.id
        else:
            image.filename = str(filename)

        return image


class TagList(_NewsModel):
    """An tag for articles."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'tag_list'

    tag = CharField(255)

    @classmethod
    def add(cls, tag: str) -> TagList:
        """Adds the respective tag."""
        try:
            return cls.get(cls.tag == tag)
        except cls.DoesNotExist:
            tag_ = cls()
            tag_.tag = tag
            return tag_


class Tag(_NewsModel):
    """Article <> Tag mappings."""

    article = ForeignKeyField(
        Article, column_name='article', backref='tags', on_delete='CASCADE')
    tag = CharField(255)

    @classmethod
    def add(cls, article: Article, tag: str, validate: bool = True) -> Tag:
        """Adds a new tag to the article."""
        if validate:
            try:
                TagList.get(TagList.tag == tag)
            except TagList.DoesNotExist:
                raise InvalidTag(tag) from None

        try:
            return cls.get((cls.article == article) & (cls.tag == tag))
        except cls.DoesNotExist:
            article_tag = cls()
            article_tag.article = article
            article_tag.tag = tag
            return article_tag

    def to_json(self, preview: bool = False, **kwargs) -> dict:
        """Returns a JSON-ish representation."""
        if preview:
            return self.tag

        return super().to_json(**kwargs)


class Whitelist(_NewsModel):
    """Article <> Customer mappings."""

    article = ForeignKeyField(
        Article, column_name='article', backref='whitelist',
        on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')

    @classmethod
    def add(cls, article: Article, customer: Customer) -> Whitelist:
        """Adds the respective customer to the article."""
        try:
            return cls.get(
                (cls.article == article) & (cls.customer == customer))
        except cls.DoesNotExist:
            article_customer = cls()
            article_customer.article = article
            article_customer.customer = customer
            return article_customer


class AccessToken(_NewsModel):
    """Customers' access tokens."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'access_token'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')
    token = UUIDField(default=uuid4)

    @classmethod
    def add(cls, customer: Customer) -> AccessToken:
        """Adds an access token for the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            access_token = cls()
            access_token.customer = customer
            return access_token


MODELS = [Article, Editor, Image, TagList, Tag, Whitelist, AccessToken]
