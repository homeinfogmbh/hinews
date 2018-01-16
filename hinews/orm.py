"""ORM models."""

from peewee import Model, PrimaryKeyField, ForeignKeyField, DateTimeField, \
    CharField, TextField, IntegerField

from peeweeplus import MySQLDatabase

from hinews.config import CONFIG


DATABASE = MySQLDatabase(
    CONFIG['db']['db'], host=CONFIG['db']['host'], user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'], closing=True)


class NewsModel(Model):
    """Basic news database model."""

    class Meta:
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
            'images': [image.to_dict() for image in self.images],
            'tags': [tag.to_dict() for tag in self.tags],
            'customers': [customer.to_dict() for customer in self.customers]}

    def delete_instance(self):
        """Deletes the article."""
        for image in self.images:
            image.delete_instance()

        return super().delete_instance()


class ArticleImage(NewsModel):
    """An image of an article."""

    article = ForeignKeyField(Article, db_column='article')
    file = IntegerField()
    data = FileProperty(file)

    def __bytes__(self):
        """Returns the file's data."""
        return self.data

    @classmethod
    def add(cls, article, data):
        """Adds the respective image data to the article."""
        article_image = cls()
        article_image.article = article
        article_image.data = data
        return article_image

    def delete_instance(self):
        """Deltes the image."""
        delete(self.file)
        return super().delete_instance()


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


class ArticleTag(NewsModel):
    """Article <> Tag mappings."""

    article = ForeignKeyField(Article, db_column='article')
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

    article = ForeignKeyField(Article, db_column='article')
    customer = ForeignKeyField(Customer, db_column='customer')

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


class ArticleProxy:
    """Proxy.to transparently handle data associated with articles."""

    def __init__(self, article):
        """Sets the respective article."""
        self.article = article


class ArticleImageProxy(ArticleProxy):
    """Proxies images of articles."""

    def __iter__(self):
        """Yields images of the respective article."""
        yield from ArticleImage.select().where(
            ArticleImage.article == self.article)

    def add(self, data):
        """Adds an image to the respective article."""
        article_image = ArticleImage.add(self.article, data)
        article_image.save()
        return article_image

    def delete(self, ident):
        """Removes the respective article image."""
        try:
            article_image = ArticleImage.get(
                (ArticleImage.article == self.article)
                & (ArticleImage.id == ident))
        except DoesNotExist:
            return False

        return article_image.delete_instance()


class ArticleTagProxy(ArticleProxy):
    """Proxies tags of articles."""

    def __iter__(self):
        """Yields the respective article's tags."""
        yield from ArticleTag.select().where(
            ArticleTag.article == self.article)

    def add(self, tag):
        """Adds the respective tag."""
        article_tag = ArticleTag.add(self.article, tag)
        article_tag.save()
        return article_tag

    def delete(self, tag_or_id):
        """Deletes the respective tag."""
        try:
            ident = int(tag_or_id)
        except ValueError:
            selection = ArticleTag.tag == tag_or_id
        else:
            selection = ArticleTag.id == ident

        try:
            article_tag = ArticleTag.get(
                (ArticleTag.article == self.article) & selection)
        except DoesNotExist:
            return False

        return article_tag.delete_instance()


class ArticleCustomerProxy(ArticleProxy):
    """Proxies customers of the respective article."""

    def __iter__(self):
        """Yields customers of the respective article."""
        yield from ArticleCustomer.select().where(
            ArticleCustomer.article == self.article)

    def add(self, customer):
        """Adds a customer to the respective article."""
        article_customer = ArticleCustomer.add(self.article, customer)
        article_customer.save()
        return article_customer

    def delete(self, customer):
        """Deletes the respective customer from the article."""
        try:
            article_customer = ArticleCustomer.get(
                (ArticleCustomer.article == self.article)
                & (ArticleCustomer.customer == customer))
        except DoesNotExist:
            return False

        return article_customer.delete_instance()
