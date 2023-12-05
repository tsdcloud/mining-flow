from django.db import models
from common.models import BaseUUIDModel
import json
from datetime import datetime

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

        categorie._change_reason = json.dumps({
            "reason": "Add a new categorie",
            "user": user
        })
        categorie._history_date = datetime.now()
        categorie.save()
        return categorie

    def change(
        self,
        name: str,
        user: str
    ):
        """ change categorie """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update categorie",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete categorie """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete categorie",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active motive previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore categorie",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


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

        article._change_reason = json.dumps({
            "reason": "Add a new article",
            "user": user
        })
        article._history_date = datetime.now()
        article.save()
        return article

    def change(
        self,
        name: str,
        user: str
    ):
        """ change article """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update article",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete article """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete article",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active article previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore article",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
