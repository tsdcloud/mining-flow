from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseUUIDModel, BaseHistoryModel

# Create your models here.


class Categorie(BaseUUIDModel):
    """ Categorie's class purpose is to manage categories """
    name = models.CharField(max_length=100)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["name", "is_active", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.name)

    @staticmethod
    def insertHistory(categorie: "Categorie", user: str, operation: int):
        hcategorie = HCategorie()
        hcategorie.categorie = categorie
        hcategorie.name = categorie.name
        hcategorie.is_active = categorie.is_active
        hcategorie.date = categorie.date
        hcategorie.operation = operation
        hcategorie.user = user

        hcategorie.save()

    @staticmethod
    def create(
        name: str,
        user: str
    ):
        """ add categorie """
        try:
            categorie = Categorie.objects.get(name=name.upper())
            categorie.is_active = True
        except Categorie.DoesNotExist:
            categorie = Categorie()
            categorie.name = name.upper()

        try:
            with transaction.atomic():
                categorie.save()
                Categorie.insertHistory(
                    categorie=categorie, user=user, operation=1)
            return categorie
        except DatabaseError:
            return None

    def change(
        self,
        name: str,
        user: str
    ):
        """ change categorie """
        self.name = name.upper()

        try:
            with transaction.atomic():
                self.save()
                Categorie.insertHistory(categorie=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete categorie """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Categorie.insertHistory(categorie=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active motive previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Categorie.insertHistory(categorie=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None


class Article(BaseUUIDModel):
    """ Article's class purpose is to manage articles """
    name = models.CharField(max_length=100)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.RESTRICT,
        related_name="articles",
    )

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["name", "is_active", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.name)

    @staticmethod
    def insertHistory(article: "Article", user: str, operation: int):
        harticle = HArticle()
        harticle.article = article
        harticle.categorie = article.categorie
        harticle.name = article.name
        harticle.is_active = article.is_active
        harticle.date = article.date
        harticle.operation = operation
        harticle.user = user

        harticle.save()

    @staticmethod
    def create(
        name: str,
        categorie: Categorie,
        user: str
    ):
        """ add article """
        try:
            article = Article.objects.get(name=name.upper())
            article.is_active = True
        except Article.DoesNotExist:
            article = Article()
            article.name = name.upper()
        article.categorie = categorie

        try:
            with transaction.atomic():
                article.save()
                Article.insertHistory(
                    article=article, user=user, operation=1)
            return article
        except DatabaseError:
            return None

    def change(
        self,
        name: str,
        user: str
    ):
        """ change article """
        self.name = name.upper()

        try:
            with transaction.atomic():
                self.save()
                Article.insertHistory(article=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete article """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Article.insertHistory(article=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active article previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Article.insertHistory(article=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None


class HCategorie(BaseHistoryModel):
    """ categorie history """
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.RESTRICT,
        related_name="hcategories",
        editable=False
    )
    name = models.CharField(max_length=100, editable=False)


class HArticle(BaseHistoryModel):
    """ article history """
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="harticles",
        editable=False
    )
    name = models.CharField(max_length=100, editable=False)
