"""ORM models."""

from contextlib import suppress
from datetime import datetime
from uuid import uuid4

from peewee import DoesNotExist, Model, PrimaryKeyField, ForeignKeyField, \
    DateField, DateTimeField, CharField, TextField, IntegerField

from filedb import add, get, delete, FileProperty
from his.orm import Account
from homeinfo.crm import Customer
from peeweeplus import MySQLDatabase

from hinews.config import CONFIG

__all__ = [
    'InvalidTag',
    'InvalidElements',
    'create_tables',
    'Article',
    'ArticleImage',
    'MODELS']


DATABASE = MySQLDatabase(
    CONFIG['db']['db'], host=CONFIG['db']['host'], user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'], closing=True)


class InvalidTag(Exception):
    """Indicates that a respective tag is not registered."""

    pass


class InvalidElements(Exception):
    """Indicates that the respective elements are invalid."""

    def __init__(self, elements):
        """Sets the invalid elements."""
        super().__init__(elements)
        self.elements = elements

    def __iter__(self):
        """Yields the invalid elements."""
        yield from self.elements


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
    active_from = DateField(null=True)
    active_until = DateField(null=True)
    title = CharField(255)
    subtitle = CharField(255, null=True)
    text = TextField()
    source = TextField()

    @classmethod
    def from_dict(cls, author, dictionary):
        """Creates a new article from the provided dictionary."""
        article = cls()
        article.author = author
        article.created = datetime.now()
        article.active_from = dictionary.get('active_from')
        article.active_until = dictionary.get('active_until')
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

    @tags.setter
    def tags(self, tags):
        """Sets the respective tags."""
        for tag in self.tags:
            tag.delete_instance()

        invalid_tags = []

        for tag in tags:
            try:
                self.tags.add(tag)
            except InvalidTag:
                invalid_tags.append(tag)

        if invalid_tags:
            raise InvalidElements(invalid_tags)

    @property
    def customers(self):
        """Yields customers of this article."""
        return ArticleCustomerProxy(self)

    @customers.setter
    def customers(self, cids):
        """Sets the respective customers."""
        for customer in self.customers:
            customer.delete_instance()

        invalid_customers = []

        for cid in cids:
            try:
                customer = Customer.get(Customer.id == cid)
            except (ValueError, DoesNotExist):
                invalid_customers.append(cid)
            else:
                self.customers.add(customer)

        if invalid_customers:
            raise InvalidElements(invalid_customers)

    @property
    def active(self):
        """Determines whether the article is considered active."""
        today = datetime.now().date()

        if self.active_from is not None:
            if self.active_until is not None:
                return self.active_from <= today <= self.active_until

            return self.active_from <= today
        elif self.active_until is not None:
            return today <= self.active_until

        return True

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        return {
            'id': self.id,
            'author': self.author.to_dict(),
            'created': self.created,
            'active_from': self.active_from,
            'active_until': self.active_until,
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
        with suppress(KeyError):
            self.active_from = dictionary['active_from']

        with suppress(KeyError):
            self.active_until = dictionary['active_until']

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
            'timestamp': self.timestamp}


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
    data_ = FileProperty(file)

    @classmethod
    def add(cls, article, data, metadata, account):
        """Adds the respective image data to the article."""
        print('Integer field name: ', cls.data_.interger_field.name)
        print('Integer field match: ', cls.data_.interger_field == cls.file)
        article_image = cls()
        print('Integer field value: ', article_image.file)
        print('Integer field value2: ', article_image.data_.interger_field)
        article_image.article = article
        article_image.account = account
        article_image.data = data
        article_image.uploaded = datetime.now()
        article_image.source = metadata['source']
        return article_image

    @property
    def data(self):
        """Returns the respective data."""
        return get(self.file)

    @data.setter
    def data(self, data):
        """Sets the respective data."""
        if self.file is not None:
            delete(self.file)

        if data is not None:
            self.file = add(data)

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

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        return {
            'id': self.id,
            'tag': self.tag}


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

    def to_dict(self):
        """Returns a JSON-ish representation of the article customer."""
        return {'id': self.id, 'customer': self.customer.id}


class AccessToken(NewsModel):
    """Customers' access tokens."""

    class Meta:
        """Sets the table name."""
        db_table = 'access_token'

    customer = ForeignKeyField(
        Customer, db_column='customer', on_delete='CASCADE',
        on_update='CASCADE')
    token = CharField(36)   # UUID4

    @classmethod
    def add(cls, customer):
        """Adds an access token for the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except DoesNotExist:
            access_token = cls()
            access_token.customer = customer
            access_token.token = str(uuid4())
            return access_token


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

    def __contains__(self, customer):
        """Determines whether the respective
        customer may use the respective article.
        """
        empty = True

        for article_customer in self:
            empty = False

            if article_customer.customer == customer:
                return True

        return empty

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
    Article, ArticleEditor, ArticleImage, Tag, ArticleTag, ArticleCustomer,
    AccessToken]
