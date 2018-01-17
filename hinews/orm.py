"""ORM models."""

from contextlib import suppress
from datetime import datetime

from peewee import DoesNotExist, Model, PrimaryKeyField, ForeignKeyField, \
    DateTimeField, CharField, TextField, IntegerField

from filedb import delete, FileProperty
from his.orm import Account
from homeinfo.crm import Customer
from peeweeplus import MySQLDatabase
from timelib import strpdatetime, isoformat

from hinews.config import CONFIG

__all__ = ['InvalidTag', 'create_tables', 'Article', 'ArticleImage', 'MODELS']


DATABASE = MySQLDatabase(
    CONFIG['db']['db'], host=CONFIG['db']['host'], user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'], closing=True)


class InvalidTag(Exception):
    """Indicates that a respective tag is not registered."""

    pass


def create_tables(fail_silently=False):
    """Creates all tables."""

    for model in MODELS:
        model.create_table(fail_silently=fail_silently)


class NewsModel(Model):
    """Basic news database model."""

    class Meta:
        """Configures the database and schema."""
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()


class Article(NewsModel):
    """A news-related text."""

    author = ForeignKeyField(Account, db_column='author')
    created = DateTimeField()
    last_change = DateTimeField(null=True)
    active_from = DateTimeField(null=True)
    active_until = DateTimeField(null=True)
    title = CharField(255)
    subtitle = CharField(255, null=True)
    text = TextField()
    source = TextField()

    @classmethod
    def from_dict(cls, dictionary, author=None):
        """Creates a new article from the provided dictionary."""
        article = cls()
        article.author = author
        article.created = datetime.now()
        article.last_change = None
        article.active_from = strpdatetime(dictionary.get('active_from'))
        article.active_until = strpdatetime(dictionary.get('active_until'))
        article.title = dictionary['title']
        article.subtitle = dictionary.get('subtitle')
        article.text = dictionary['text']
        return article

    @property
    def editors(self):
        """Yields article editors."""
        return ArticleEditorProxy(self)

    @property
    def images(self):
        """Yields images of this article."""
        return ArticleImageProxy(self)

    @property
    def tags(self):
        """Yields tags of this article."""
        return ArticleTagProxy(self)

    @property
    def customers(self):
        """Yields customers of this article."""
        return ArticleCustomerProxy(self)

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        return {
            'author': self.author.to_dict(),
            'created': isoformat(self.created),
            'last_change': isoformat(self.last_change),
            'active_from': isoformat(self.active_from),
            'active_until': isoformat(self.active_until),
            'title': self.title,
            'subtitle': self.subtitle,
            'text': self.text,
            'source': self.source,
            'editors': [editor.to_dict() for editor in self.editors],
            'images': [image.to_dict() for image in self.images],
            'tags': [tag.to_dict() for tag in self.tags],
            'customers': [customer.to_dict() for customer in self.customers]}

    def patch(self, dictionary):
        """Patches the article with the provided JSON-ish dictionary."""
        self.last_change = datetime.now()

        with suppress(KeyError):
            self.active_from = strpdatetime(dictionary['active_from'])

        with suppress(KeyError):
            self.active_until = strpdatetime(dictionary['active_until'])

        with suppress(KeyError):
            self.title = dictionary['title']

        with suppress(KeyError):
            self.subtitle = dictionary['subtitle']

        with suppress(KeyError):
            self.text = dictionary['text']

        with suppress(KeyError):
            self.source = dictionary['source']

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deletes the article."""
        # Manually delete all referencing images to ensure
        # deletion of the respective filedb entries.
        for image in self.images:
            image.delete_instance()

        return super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class ArticleEditor(NewsModel):
    """An article's editor."""

    class Meta:
        """Sets the table name."""
        db_table = 'article_editor'

    article = ForeignKeyField(
        Article, db_column='article', on_delete='CASCADE')
    account = ForeignKeyField(
        Account, db_column='account', on_delete='CASCADE')
    timestamp = DateTimeField()

    @classmethod
    def add(cls, article, account, timestamp=None):
        """Adds a new author record to the respective article."""
        article_author = cls()
        article_author.article = article
        article_author.account = account
        article_author.timestamp = timestamp or datetime.now()
        return article_author

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        return {
            'account': self.account.to_dict(),
            'timestamp': isoformat(self.timestamp)}


class ArticleImage(NewsModel):
    """An image of an article."""

    class Meta:
        """Sets the table name."""
        db_table = 'image'

    article = ForeignKeyField(
        Article, db_column='article', on_delete='CASCADE')
    account = ForeignKeyField(
        Account, db_column='account', on_delete='CASCADE')
    file = IntegerField()
    uploaded = DateTimeField()
    source = TextField(null=True)
    data = FileProperty(file)

    @classmethod
    def add(cls, article, data, metadata, account):
        """Adds the respective image data to the article."""
        article_image = cls()
        article_image.article = article
        article_image.account = account
        article_image.source = metadata['source']
        article_image.uploaded = datetime.now()
        article_image.data = data
        return article_image

    def patch(self, dictionary):
        """Patches the image metadata with the respective dictionary."""
        with suppress(KeyError):
            self.source = dictionary['source']

    def to_dict(self):
        """Returns a JSON-compliant integer."""
        return {'id': self.id, 'source': self.source}

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deltes the image."""
        delete(self.file)
        return super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class Tag(NewsModel):
    """An tag for articles."""

    tag = CharField(255)

    @classmethod
    def add(cls, tag):
        """Adds the respective tag."""
        try:
            return cls.get(cls.tag == tag)
        except DoesNotExist:
            tag_ = cls()
            tag_.tag = tag
            return tag_

    def to_dict(self):
        """Returns a JSON-compliant string."""
        return self.tag


class ArticleTag(NewsModel):
    """Article <> Tag mappings."""

    class Meta:
        """Sets the table name."""
        db_table = 'article_tag'

    article = ForeignKeyField(
        Article, db_column='article', on_delete='CASCADE')
    tag = CharField(255)

    @classmethod
    def add(cls, article, tag, validate=True):
        """Adds a new tag to the article."""
        if validate:
            try:
                Tag.get(Tag.tag == tag)
            except DoesNotExist:
                raise InvalidTag(tag)

        try:
            return cls.get((cls.article == article) & (cls.tag == tag))
        except DoesNotExist:
            article_tag = cls()
            article_tag.article = article
            article_tag.tag = tag
            return article_tag


class ArticleCustomer(NewsModel):
    """Article <> Customer mappings."""

    class Meta:
        """Sets the table name."""
        db_table = 'article_customer'

    article = ForeignKeyField(
        Article, db_column='article', on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, db_column='customer', on_delete='CASCADE')

    @classmethod
    def add(cls, article, customer):
        """Adds the respective customer to the article."""
        try:
            return ArticleCustomer.get(
                (ArticleCustomer.article == article)
                & (ArticleCustomer.customer == customer))
        except DoesNotExist:
            article_customer = cls()
            article_customer.article = article
            article_customer.customer = customer
            return article_customer


class Proxy:
    """Proxy.to transparently handle data
    associated with the respective target.
    """

    def __init__(self, model, target):
        """Sets the model and target."""
        self.model = model
        self.target = target


class ArticleProxy(Proxy):
    """An article-related proxy."""

    def __iter__(self):
        """Yields sources of the respective article."""
        yield from self.model.select().where(self.model.article == self.target)


class ArticleEditorProxy(ArticleProxy):
    """Proxies article authors."""

    def __init__(self, target):
        """Sets model and target."""
        super().__init__(ArticleEditor, target)

    def add(self, author):
        """Adds the respective author."""
        article_author = self.model.add(self.target, author)
        article_author.save()
        return article_author


class ArticleImageProxy(ArticleProxy):
    """Proxies images of articles."""

    def __init__(self, target):
        """Sets the model and target."""
        super().__init__(ArticleImage, target)

    def add(self, data, metadata, account):
        """Adds an image to the respective article."""
        article_image = self.model.add(self.target, data, metadata, account)
        article_image.save()
        return article_image

    def delete(self, ident):
        """Removes the respective article image."""
        try:
            article_image = self.model.get(
                (self.model.article == self.target) & (self.model.id == ident))
        except DoesNotExist:
            return False

        return article_image.delete_instance()


class ArticleTagProxy(ArticleProxy):
    """Proxies tags of articles."""

    def __init__(self, target):
        """Sets the model and target."""
        super().__init__(ArticleTag, target)

    def add(self, tag):
        """Adds the respective tag."""
        article_tag = self.model.add(self.target, tag)
        article_tag.save()
        return article_tag

    def delete(self, tag_or_id):
        """Deletes the respective tag."""
        try:
            ident = int(tag_or_id)
        except ValueError:
            selection = self.model.tag == tag_or_id
        else:
            selection = self.model.id == ident

        try:
            article_tag = self.model.get(
                (self.model.article == self.target) & selection)
        except DoesNotExist:
            return False

        return article_tag.delete_instance()


class ArticleCustomerProxy(ArticleProxy):
    """Proxies customers of the respective article."""

    def __init__(self, target):
        """Sets the model and target."""
        super().__init__(ArticleCustomer, target)

    def add(self, customer):
        """Adds a customer to the respective article."""
        article_customer = self.model.add(self.target, customer)
        article_customer.save()
        return article_customer

    def delete(self, customer):
        """Deletes the respective customer from the article."""
        try:
            article_customer = self.model.get(
                (self.model.article == self.target)
                & (self.model.customer == customer))
        except DoesNotExist:
            return False

        return article_customer.delete_instance()


class ImageProxy(Proxy):
    """An image-related proxy."""

    def __iter__(self):
        """Yields records of the respective model, related tor the image."""
        yield from self.model.select().where(self.model.image == self.target)


MODELS = [
    Article, ArticleEditor, ArticleImage, Tag, ArticleTag, ArticleCustomer]
