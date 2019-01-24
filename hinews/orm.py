"""ORM models."""

from datetime import date, datetime
from functools import lru_cache
from uuid import uuid4

from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField
from peewee import UUIDField

from filedb import mimetype, FileProperty
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
    'MODELS']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


def create_tables(fail_silently=False):
    """Creates all tables."""

    for model in MODELS:
        model.create_table(fail_silently=fail_silently)


def article_active():
    """Yields article active query."""

    today = date.today()
    return (
        ((Article.active_from >> None) | (Article.active_from <= today))
        & ((Article.active_until >> None) | (Article.active_until >= today)))


@lru_cache()
def _cached_account_info(ident):
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
    def from_json(cls, dictionary, author, **kwargs):
        """Creates a new article from the provided dictionary."""
        article = super().from_json(dictionary, **kwargs)
        article.author = author
        return article

    @property
    def customers(self):
        """Returns a frozen set of customers that
        are whitelisted for this article.
        """
        return frozenset(whitelist.customer for whitelist in self.whitelist)

    def update_tags(self, tags):
        """Updates the respective tags."""
        if tags is None:
            return

        for tag in self.tags:
            tag.delete_instance()

        if not tags:
            return

        for tag in tags:
            yield Tag.add(self, tag)

    def update_customers(self, cids):
        """Updates the respective customers."""
        if cids is None:
            return

        for whitelist in self.whitelist:
            whitelist.delete_instance()

        if not cids:
            return

        for cid in cids:
            yield Whitelist.add(self, cid)

    def to_json(self, preview=False, fk_fields=True, **kwargs):
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

    def to_dom(self, local=False):
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

    def delete_instance(self, recursive=False, delete_nullable=False):
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
    def add(cls, article, account):
        """Adds a new author record to the respective article."""
        try:
            return cls.get((cls.article == article) & (cls.account == account))
        except cls.DoesNotExist:
            return cls(article=article, account=account)

    def to_json(self, *args, **kwargs):
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
    _file = IntegerField(column_name='file')
    uploaded = DateTimeField()
    source = TextField(null=True)
    data = FileProperty(_file)

    @classmethod
    def add(cls, article, data, metadata, account):
        """Adds the respective image data to the article."""
        article_image = cls()
        article_image.article = article
        article_image.account = account
        article_image.data = data
        article_image.uploaded = datetime.now()
        article_image.source = metadata['source']
        return article_image

    @property
    def oneliner(self):
        """Returns the source text as a one-liner."""
        return ' '.join(self.source.split('\n'))

    @property
    def watermarked(self):
        """Returns a watermarked image."""
        return watermark(self.data, 'Quelle: {}'.format(self.oneliner))

    def patch_json(self, dictionary):
        """Patches the image metadata with the respective dictionary."""
        return super().patch_json(
            dictionary, skip=('uploaded',), fk_fields=False)

    def to_json(self, preview=False, fk_fields=True, **kwargs):
        """Returns a JSON-compliant integer."""
        if preview:
            fk_fields = False

        dictionary = super().to_json(fk_fields=fk_fields, **kwargs)

        if not preview:
            dictionary['account'] = _cached_account_info(self.account_id)

        dictionary['mimetype'] = mimetype(self._file)
        return dictionary

    def to_dom(self, filename=None):
        """Converts the image into a XML DOM model."""
        image = dom.Image()
        image.uploaded = self.uploaded
        image.source = self.source
        image.mimetype = mimetype(self._file)

        if filename is None:
            image.id = self.id
        else:
            image.filename = filename

        return image

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deltes the image."""
        self.data = None    # Delete file.
        return super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class TagList(_NewsModel):
    """An tag for articles."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'tag_list'

    tag = CharField(255)

    @classmethod
    def add(cls, tag):
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
    def add(cls, article, tag, validate=True):
        """Adds a new tag to the article."""
        if validate:
            try:
                TagList.get(TagList.tag == tag)
            except TagList.DoesNotExist:
                raise InvalidTag(tag)

        try:
            return cls.get((cls.article == article) & (cls.tag == tag))
        except cls.DoesNotExist:
            article_tag = cls()
            article_tag.article = article
            article_tag.tag = tag
            return article_tag

    def to_json(self, preview=False, **kwargs):
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
    def add(cls, article, customer):
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
    def add(cls, customer):
        """Adds an access token for the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            access_token = cls()
            access_token.customer = customer
            return access_token


MODELS = [Article, Editor, Image, TagList, Tag, Whitelist, AccessToken]
