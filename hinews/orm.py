"""ORM models."""

from contextlib import suppress
from datetime import datetime

from peewee import PrimaryKeyField, ForeignKeyField, DateField, DateTimeField,\
    CharField, TextField, IntegerField

from filedb import mimetype, FileProperty
from his.orm import Account
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel, UUID4Field

from hinews import dom
from hinews.config import CONFIG
from hinews.exceptions import InvalidCustomer, InvalidElements, InvalidTag
from hinews.proxy import ArticleProxy
from hinews.watermark import watermark


__all__ = [
    'create_tables',
    'article_active',
    'Article',
    'ArticleEditor',
    'ArticleImage',
    'TagList',
    'CustomerList',
    'ArticleTag',
    'ArticleCustomer',
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


class NewsModel(JSONModel):
    """Basic news database model."""

    class Meta:
        """Configures the database and schema."""
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()


class Article(NewsModel):
    """A news-related text."""

    author = ForeignKeyField(Account, column_name='author')
    created = DateTimeField(default=datetime.now)
    active_from = DateField(null=True)
    active_until = DateField(null=True)
    title = CharField(255)
    subtitle = CharField(255, null=True)
    text = TextField()
    source = TextField()

    @classmethod
    def from_dict(cls, author, dictionary, **kwargs):
        """Creates a new article from the provided dictionary."""
        article = super().from_dict(dictionary, **kwargs)
        article.author = author
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
            except (ValueError, Customer.DoesNotExist):
                invalid_customers.append(cid)
            else:
                self.customers.add(customer)

        if invalid_customers:
            raise InvalidElements(invalid_customers)

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


class ArticleEditor(NewsModel):
    """An article's editor."""

    class Meta:
        """Sets the table name."""
        table_name = 'article_editor'

    article = ForeignKeyField(
        Article, column_name='article', on_delete='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
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
        dictionary = super().to_dict()
        dictionary['account'] = self.account.info
        return dictionary


class ArticleImage(NewsModel):
    """An image of an article."""

    class Meta:
        """Sets the table name."""
        table_name = 'image'

    article = ForeignKeyField(
        Article, column_name='article', on_delete='CASCADE')
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


class TagList(NewsModel):
    """An tag for articles."""

    class Meta:
        """Sets the table name."""
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


class CustomerList(NewsModel):
    """Csutomers enabled for gettings news."""

    class Meta:
        """Sets the table name."""
        table_name = 'customer_list'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')

    @classmethod
    def add(cls, customer):
        """Adds the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            customer_list = cls()
            customer_list.customer = customer
            customer_list.save()
            return customer_list

    def to_dict(self):
        """Returns the respective customer's dict."""
        return self.customer.to_dict(company=True)


class ArticleTag(NewsModel):
    """Article <> Tag mappings."""

    class Meta:
        """Sets the table name."""
        table_name = 'article_tag'

    article = ForeignKeyField(
        Article, column_name='article', on_delete='CASCADE')
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

    def to_dict(self, preview=False, **kwargs):
        """Returns a JSON-ish representation."""
        if preview:
            return self.tag

        return super().to_dict(**kwargs)


class ArticleCustomer(NewsModel):
    """Article <> Customer mappings."""

    class Meta:
        """Sets the table name."""
        table_name = 'article_customer'

    article = ForeignKeyField(
        Article, column_name='article', on_delete='CASCADE')
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')

    @classmethod
    def add(cls, article, customer):
        """Adds the respective customer to the article."""
        try:
            CustomerList.get(CustomerList.customer == customer)
        except CustomerList.DoesNotExist:
            raise InvalidCustomer(customer)

        try:
            return cls.get(
                (cls.article == article) & (cls.customer == customer))
        except cls.DoesNotExist:
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
        table_name = 'access_token'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')
    token = UUID4Field()

    @classmethod
    def add(cls, customer):
        """Adds an access token for the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            access_token = cls()
            access_token.customer = customer
            return access_token


class ArticleEditorProxy(ArticleProxy):
    """Proxies article authors."""

    def __init__(self, target):
        """Sets model and target."""
        super().__init__(ArticleEditor, target)


class ArticleImageProxy(ArticleProxy):
    """Proxies images of articles."""

    def __init__(self, target):
        """Sets the model and target."""
        super().__init__(ArticleImage, target)


class ArticleTagProxy(ArticleProxy):
    """Proxies tags of articles."""

    def __init__(self, target):
        """Sets the model and target."""
        super().__init__(ArticleTag, target)

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
        except self.model.DoesNotExist:
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

    def delete(self, customer):
        """Deletes the respective customer from the article."""
        try:
            article_customer = self.model.get(
                (self.model.article == self.target)
                & (self.model.customer == customer))
        except self.model.DoesNotExist:
            return False

        return article_customer.delete_instance()


MODELS = [
    Article, ArticleEditor, ArticleImage, TagList, CustomerList, ArticleTag,
    ArticleCustomer, AccessToken]
