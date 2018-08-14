"""ORM models."""

from contextlib import suppress
from datetime import datetime
from uuid import uuid4

from peewee import AutoField, ForeignKeyField, DateField, DateTimeField, \
    CharField, TextField, IntegerField, UUIDField

from filedb import mimetype, FileProperty
from his.orm import Account
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel, JSONField

from hinews import dom
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

    now = datetime.now()
    return (
        ((Article.active_from >> None) | (Article.active_from <= now))
        & ((Article.active_until >> None) | (Article.active_until >= now)))


class _NewsModel(JSONModel):
    """Basic news database model."""

    class Meta:
        """Configures the database and schema."""
        database = DATABASE
        schema = database.database

    id = JSONField(AutoField)


class Article(_NewsModel):
    """A news-related text."""

    author = ForeignKeyField(Account, column_name='author')
    created = JSONField(DateTimeField, default=datetime.now)
    active_from = JSONField(DateField, null=True, key='activeFrom')
    active_until = JSONField(DateField, null=True, key='activeUntil')
    title = JSONField(CharField, 255)
    subtitle = JSONField(CharField, 255, null=True)
    text = JSONField(TextField)
    source = JSONField(TextField)

    @classmethod
    def from_dict(cls, author, dictionary, **kwargs):
        """Creates a new article from the provided dictionary."""
        tags = dictionary.pop('tags', None)
        customers = dictionary.pop('customers', None)
        article = super().from_dict(dictionary, **kwargs)
        article.author = author
        yield article
        yield from article.update_tags(tags)
        yield from article.update_customers(customers)

    @property
    def customers(self):
        """Returns a frozen set of customers that
        are whitelisted for this article.
        """
        return frozenset(whitelist.customer for whitelist in self.whitelist)

    def patch(self, dictionary, **kwargs):
        """Patches article from the provided dictionary."""
        tags = dictionary.pop('tags', None)
        customers = dictionary.pop('customers', None)
        yield super().patch(dictionary, **kwargs)
        yield from self.update_tags(tags)
        yield from self.update_customers(customers)

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

        for customer in self.customers:
            customer.delete_instance()

        if not cids:
            return

        for cid in cids:
            yield Whitelist.add(self, cid)

    def to_dict(self, preview=False, fk_fields=True, **kwargs):
        """Returns a JSON-ish dictionary."""
        if preview:
            fk_fields = False

        dictionary = super().to_dict(fk_fields=fk_fields, **kwargs)
        dictionary['images'] = [
            image.to_dict(preview=preview) for image in self.images]
        dictionary['tags'] = [
            tag.to_dict(preview=preview) for tag in self.tags]

        if not preview:
            dictionary['author'] = self.author.info
            dictionary['editors'] = [
                editor.to_dict() for editor in self.editors]
            dictionary['customers'] = [
                customer.to_dict() for customer in self.customers]

        return dictionary

    def to_dom(self):
        """Converts the article into a XML DOM model."""
        article = dom.Article()
        article.id = self.id
        article.created = self.created
        article.active_from = self.active_from
        article.active_until = self.active_until
        article.title = self.title
        article.subtitle = self.subtitle
        article.text = self.text
        article.source = self.source
        article.image = [image.to_dom() for image in self.images]
        article.tag = [tag.tag for tag in self.tags]
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

    class Meta:
        """Sets the table name."""
        table_name = 'editor'

    article = JSONField(
        ForeignKeyField, Article, column_name='article', backref='editors',
        on_delete='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    timestamp = JSONField(DateTimeField, default=datetime.now)

    @classmethod
    def add(cls, article, account):
        """Adds a new author record to the respective article."""
        try:
            return cls.get((cls.article == article) & (cls.account == account))
        except cls.DoesNotExist:
            return cls(article=article, account=account)

    def to_dict(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['account'] = self.account.info
        return dictionary


class Image(_NewsModel):
    """An image of an article."""

    class Meta:
        """Sets the table name."""
        table_name = 'image'

    article = JSONField(
        ForeignKeyField, Article, column_name='article', backref='images',
        on_delete='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    _file = IntegerField(column_name='file')
    uploaded = JSONField(DateTimeField)
    source = JSONField(TextField, null=True)
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

    def patch(self, dictionary):
        """Patches the image metadata with the respective dictionary."""
        with suppress(KeyError):
            self.source = dictionary['source']

    def to_dict(self, preview=False, fk_fields=True, **kwargs):
        """Returns a JSON-compliant integer."""
        if preview:
            fk_fields = False

        dictionary = super().to_dict(fk_fields=fk_fields, **kwargs)

        if not preview:
            dictionary['account'] = self.account.info

        dictionary['mimetype'] = mimetype(self._file)
        return dictionary

    def to_dom(self):
        """Converts the image into a XML DOM model."""
        image = dom.Image()
        image.id = self.id
        image.uploaded = self.uploaded
        image.source = self.source
        image.mimetype = mimetype(self._file)
        return image

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deltes the image."""
        self.data = None    # Delete file.
        return super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class TagList(_NewsModel):
    """An tag for articles."""

    class Meta:
        """Sets the table name."""
        table_name = 'tag_list'

    tag = JSONField(CharField, 255)

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

    article = JSONField(
        ForeignKeyField, Article, column_name='article', backref='tags',
        on_delete='CASCADE')
    tag = JSONField(CharField, 255)

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

    def to_dict(self, preview=False, **kwargs):
        """Returns a JSON-ish representation."""
        if preview:
            return self.tag

        return super().to_dict(**kwargs)


class Whitelist(_NewsModel):
    """Article <> Customer mappings."""

    article = ForeignKeyField(
        Article, column_name='article', backref='whitelist',
        on_delete='CASCADE')
    customer = JSONField(
        ForeignKeyField, Customer, column_name='customer', on_delete='CASCADE')

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

    class Meta:
        """Sets the table name."""
        table_name = 'access_token'

    customer = JSONField(
        ForeignKeyField, Customer, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')
    token = JSONField(UUIDField, default=uuid4)

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
