from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseUUIDModel, BaseHistoryModel
from django.core import signing

import http.client
import json
import datetime

from common.constants import (
    ENDPOINT_ENTITY,
    BALANCE_OPERATION_CHOICE,
    STATUS_TRANSFER_CHOICE,
    SALE_CHOICE,
    STATUS_SALE_CHOICE
)
from article.models import Article
from car.models import (
    Tractor,
    Trailer
)

# Create your models here.


class StockageAera(BaseUUIDModel):
    village = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["name", "is_active", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.name)

    @staticmethod
    def insertHistory(stockageaera: "StockageAera", user: str, operation: int):
        hstockageaera = HStockageAera()
        hstockageaera.stockageaera = stockageaera
        hstockageaera.village = stockageaera.village
        hstockageaera.name = stockageaera.name
        hstockageaera.is_active = stockageaera.is_active
        hstockageaera.date = stockageaera.date
        hstockageaera.operation = operation
        hstockageaera.user = user

        hstockageaera.save()

    @staticmethod
    def create(
        name: str,
        village: str,
        user: str
    ):
        """ add stockage aera """
        try:
            stockageaera = StockageAera.objects.get(
                name=name.upper(),
                village=village
            )
            stockageaera.is_active = True
        except StockageAera.DoesNotExist:
            stockageaera = StockageAera()
            stockageaera.name = name.upper()
            stockageaera.village = village

        try:
            with transaction.atomic():
                stockageaera.save()
                StockageAera.insertHistory(
                    stockageaera=stockageaera, user=user, operation=1)
            return stockageaera
        except DatabaseError:
            return None

    def change(
        self,
        name: str,
        user: str
    ):
        """ change stockage aera """
        self.name = name.upper()

        try:
            with transaction.atomic():
                self.save()
                StockageAera.insertHistory(
                    stockageaera=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete stockage aera """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                StockageAera.insertHistory(
                    stockageaera=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active stockage aera previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                StockageAera.insertHistory(
                    stockageaera=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None

    @staticmethod
    def get_village(village: str, authorization: str):
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = ''
        headers = {
            "Authorization": authorization
        }
        url = "/village/" + village + "/"
        conn.request("GET", url, payload, headers)
        response = conn.getresponse()
        dat = response.read()
        data = json.loads(dat)
        return data if data.get('id', 0) != 0 else None


class StockagePartner(BaseUUIDModel):
    firm = models.CharField(max_length=1000)
    village = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["name", "is_active", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.name)

    @staticmethod
    def insertHistory(
        stockagepartner: "StockagePartner",
        user: str,
        operation: int
    ):
        hstockagepartner = HStockagePartner()
        hstockagepartner.stockagePartner = stockagepartner
        hstockagepartner.village = stockagepartner.village
        hstockagepartner.name = stockagepartner.name
        hstockagepartner.firm = stockagepartner.firm
        hstockagepartner.is_active = stockagepartner.is_active
        hstockagepartner.date = stockagepartner.date
        hstockagepartner.operation = operation
        hstockagepartner.user = user

        hstockagepartner.save()

    @staticmethod
    def create(
        name: str,
        village: str,
        firm: str,
        user: str
    ):
        """ add stockage partner """
        try:
            stockagepartner = StockagePartner.objects.get(
                name=name.upper(),
                village=village
            )
            stockagepartner.is_active = True
        except StockagePartner.DoesNotExist:
            stockagepartner = StockagePartner()
            stockagepartner.name = name.upper()
            stockagepartner.village = village
        stockagepartner.firm = firm

        try:
            with transaction.atomic():
                stockagepartner.save()
                StockagePartner.insertHistory(
                    stockagepartner=stockagepartner, user=user, operation=1)
            return stockagepartner
        except DatabaseError:
            return None

    def change(
        self,
        name: str,
        user: str
    ):
        """ change stockage aera """
        self.name = name.upper()

        try:
            with transaction.atomic():
                self.save()
                StockagePartner.insertHistory(
                    stockagepartner=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete stockage partner """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                StockagePartner.insertHistory(
                    stockagepartner=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active stockage partner previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                StockagePartner.insertHistory(
                    stockagepartner=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None

    @staticmethod
    def get_village(village: str, authorization: str):
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = ''
        headers = {
            "Authorization": authorization
        }
        url = "/village/" + village + "/"
        conn.request("GET", url, payload, headers)
        response = conn.getresponse()
        dat = response.read()
        data = json.loads(dat)
        return data if data.get('id', 0) != 0 else None

    @staticmethod
    def get_firm(firm: str, authorization: str):
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = ''
        headers = {
            "Authorization": authorization
        }
        url = "/firm/" + firm + "/"
        conn.request("GET", url, payload, headers)
        response = conn.getresponse()
        dat = response.read()
        data = json.loads(dat)
        return data if data.get('id', 0) != 0 else None


class Carriere(BaseUUIDModel):
    village = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    uin = models.CharField(max_length=13)
    localisation = models.CharField(max_length=1000, default='waiting GPS')
    proprio = models.CharField(max_length=100, default='proprio')
    is_suspend = models.BooleanField(default=False)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["-is_suspend", "name", "is_active", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.name)

    @staticmethod
    def insertHistory(carriere: "Carriere", user: str, operation: int):
        hcarriere = HCarriere()
        hcarriere.carriere = carriere
        hcarriere.village = carriere.village
        hcarriere.name = carriere.name
        hcarriere.uin = carriere.uin
        hcarriere.localisation = carriere.localisation
        hcarriere.proprio = carriere.proprio
        hcarriere.is_suspend = carriere.is_suspend
        hcarriere.is_active = carriere.is_active
        hcarriere.date = carriere.date
        hcarriere.operation = operation
        hcarriere.user = user

        hcarriere.save()

    @staticmethod
    def create(
        name: str,
        village: str,
        uin: str,
        localisation: str,
        proprio: str,
        user: str
    ):
        """ add career """
        try:
            carriere = Carriere.objects.get(
                name=name.upper(),
            )
            carriere.is_active = True
        except Carriere.DoesNotExist:
            carriere = Carriere()
            carriere.name = name.upper()
            carriere.uin = uin

        carriere.village = village
        carriere.localisation = localisation
        carriere.proprio = proprio

        try:
            with transaction.atomic():
                carriere.save()
                Carriere.insertHistory(
                    carriere=carriere, user=user, operation=1)
            return carriere
        except DatabaseError:
            return None

    def change(
        self,
        name: str,
        niu: str,
        user: str
    ):
        """ change career """
        self.name = name.upper()
        self.niu = niu

        try:
            with transaction.atomic():
                self.save()
                Carriere.insertHistory(
                    carriere=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete career """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Carriere.insertHistory(
                    carriere=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active career previously disabled """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Carriere.insertHistory(
                    carriere=self, user=user, operation=4)
            return self
        except DatabaseError:
            return None

    @staticmethod
    def get_village(village: str, authorization: str):
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = ''
        headers = {
            "Authorization": authorization
        }
        url = "/village/" + village + "/"
        conn.request("GET", url, payload, headers)
        response = conn.getresponse()
        dat = response.read()
        data = json.loads(dat)
        return data if data.get('id', 0) != 0 else None


class CareerLv(BaseUUIDModel):
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="careerlv",
        editable=False
    )
    last_demand_quantity = models.IntegerField()
    last_demand_volume = models.FloatField()
    last_approve_quantity = models.IntegerField(default=0)
    last_approve_volume = models.FloatField(default=0)
    is_waiting_approve = models.BooleanField(default=True)
    available_quantity = models.IntegerField(default=0)
    available_volume = models.FloatField(default=0)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_waiting_approve", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.career.name)

    @staticmethod
    def insertHistory(careerlv: "CareerLv", user: str, operation: int):
        hcareerlv = HCareerLv()
        hcareerlv.careerlv = careerlv
        hcareerlv.career = careerlv.career
        hcareerlv.last_demand_quantity = careerlv.last_demand_quantity
        hcareerlv.last_demand_volume = careerlv.last_demand_volume
        hcareerlv.last_approve_quantity = careerlv.last_approve_quantity
        hcareerlv.last_approve_volume = careerlv.last_approve_volume
        hcareerlv.is_waiting_approve = careerlv.is_waiting_approve
        hcareerlv.available_quantity = careerlv.available_quantity
        hcareerlv.available_volume = careerlv.available_volume
        hcareerlv.is_active = careerlv.is_active
        hcareerlv.date = careerlv.date
        hcareerlv.operation = operation
        hcareerlv.user = user

        hcareerlv.save()

    @staticmethod
    def create(
        career: Carriere,
        quantity: float,
        volume: float,
        user: str
    ):
        """ new demand of lv for career """
        try:
            careerlv = CareerLv.objects.get(
                career=career,
            )
        except CareerLv.DoesNotExist:
            careerlv = CareerLv()
            careerlv.career = career

        careerlv.last_demand_quantity = quantity
        careerlv.last_demand_volume = round(volume, 3)
        careerlv.is_waiting_approve = True

        try:
            with transaction.atomic():
                careerlv.save()
                CareerLv.insertHistory(
                    careerlv=careerlv, user=user, operation=1)
            return careerlv
        except DatabaseError:
            return None

    def change(
        self,
        quantity: float,
        volume: float,
        user: str
    ):
        """ approve demand of lv for career """
        self.last_approve_quantity = quantity
        self.last_approve_volume = volume
        self.is_waiting_approve = False
        self.available_quantity = self.available_quantity + quantity
        self.available_volume = round(self.available_volume + volume, 3)

        try:
            with transaction.atomic():
                self.save()
                CareerLv.insertHistory(
                    careerlv=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None


class StockageAeraLv(BaseUUIDModel):
    stockageaera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="stockageaeralv",
        editable=False
    )
    last_demand_quantity = models.IntegerField()
    last_demand_volume = models.FloatField()
    last_approve_quantity = models.IntegerField(default=0)
    last_approve_volume = models.FloatField(default=0)
    is_waiting_approve = models.BooleanField(default=True)
    available_quantity = models.IntegerField(default=0)
    available_volume = models.FloatField(default=0)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_waiting_approve", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.stockageaera.name)

    @staticmethod
    def insertHistory(
        stockageaeralv: "StockageAeraLv",
        user: str, operation: int
    ):
        hstockageaeralv = HStockageAeraLv()
        hstockageaeralv.stockageaeralv = stockageaeralv
        hstockageaeralv.stockageaera = stockageaeralv.stockageaera
        hstockageaeralv.last_demand_quantity = stockageaeralv.last_demand_quantity
        hstockageaeralv.last_demand_volume = stockageaeralv.last_demand_volume
        hstockageaeralv.last_approve_quantity = stockageaeralv.last_approve_quantity
        hstockageaeralv.last_approve_volume = stockageaeralv.last_approve_volume
        hstockageaeralv.is_waiting_approve = stockageaeralv.is_waiting_approve
        hstockageaeralv.available_quantity = stockageaeralv.available_quantity
        hstockageaeralv.available_volume = stockageaeralv.available_volume
        hstockageaeralv.is_active = stockageaeralv.is_active
        hstockageaeralv.date = stockageaeralv.date
        hstockageaeralv.operation = operation
        hstockageaeralv.user = user

        hstockageaeralv.save()

    @staticmethod
    def create(
        stockageaera: StockageAera,
        quantity: float,
        volume: float,
        user: str
    ):
        """ new demand of lv for stockageaera """
        try:
            stockageaeralv = StockageAeraLv.objects.get(
                stockageaera=stockageaera,
            )
        except StockageAeraLv.DoesNotExist:
            stockageaeralv = StockageAeraLv()
            stockageaeralv.stockageaera = stockageaera

        stockageaeralv.last_demand_quantity = quantity
        stockageaeralv.last_demand_volume = round(volume, 3)
        stockageaeralv.is_waiting_approve = True

        try:
            with transaction.atomic():
                stockageaeralv.save()
                StockageAeraLv.insertHistory(
                    stockageaeralv=stockageaeralv, user=user, operation=1)
            return stockageaeralv
        except DatabaseError:
            return None

    def change(
        self,
        quantity: float,
        volume: float,
        user: str
    ):
        """ approve demand of lv for stockageaera """
        self.last_approve_quantity = quantity
        self.last_approve_volume = volume
        self.is_waiting_approve = False
        self.available_quantity = self.available_quantity + quantity
        self.available_volume = round(self.available_volume + volume, 3)

        try:
            with transaction.atomic():
                self.save()
                StockageAeraLv.insertHistory(
                    stockageaeralv=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None


class CareerArticle(BaseUUIDModel):
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="careerarticles",
        editable=False
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="careerarticles",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="careerarticles",
        editable=False
    )
    price_sale = models.IntegerField()
    price_car = models.IntegerField()

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["price_sale", "price_car", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.career.name, self.article.name)

    @staticmethod
    def insertHistory(
        careerarticle: "CareerArticle",
        user: str,
        operation: int
    ):
        hcareerarticle = HCareerArticle()
        hcareerarticle.careerarticle = careerarticle
        hcareerarticle.career = careerarticle.career
        hcareerarticle.article = careerarticle.article
        hcareerarticle.stockage_aera = careerarticle.stockage_aera
        hcareerarticle.price_sale = careerarticle.price_sale
        hcareerarticle.price_car = careerarticle.price_car
        hcareerarticle.is_active = careerarticle.is_active
        hcareerarticle.date = careerarticle.date
        hcareerarticle.operation = operation
        hcareerarticle.user = user

        hcareerarticle.save()

    @staticmethod
    def create(
        career: Carriere,
        article: Article,
        stockage_aera: StockageAera,
        price_sale: int,
        price_car: int,
        user: str
    ):
        """ associate career an product """
        try:
            careerarticle = CareerArticle.objects.get(
                career=career,
                article=article
            )
        except CareerArticle.DoesNotExist:
            careerarticle = CareerArticle()
            careerarticle.career = career
            careerarticle.article = article

        careerarticle.stockage_aera = stockage_aera
        careerarticle.price_car = price_car
        careerarticle.price_sale = price_sale

        try:
            with transaction.atomic():
                careerarticle.save()
                CareerArticle.insertHistory(
                    careerarticle=careerarticle, user=user, operation=1)
            return careerarticle
        except DatabaseError:
            return None

    def change(
        self,
        stockage_aera: StockageAera,
        price_sale: int,
        price_car: int,
        user: str
    ):
        """ update an association career product """
        self.stockage_aera = stockage_aera
        self.price_car = price_car
        self.price_sale = price_sale

        try:
            with transaction.atomic():
                self.save()
                CareerArticle.insertHistory(
                    careerarticle=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete careerarticle """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                CareerArticle.insertHistory(
                    careerarticle=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None


class StockageAeraArticle(BaseUUIDModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="stockageaeraarticles",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="stockageaeraarticles",
        editable=False
    )
    available_volume = models.FloatField()

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["available_volume", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.stockage_aera.name, self.article.name)

    @staticmethod
    def insertHistory(
        stockage_aera_article: "StockageAeraArticle",
        user: str,
        operation: int
    ):
        hstockage_aera_article = HStockageAeraArticle()
        hstockage_aera_article.stockage_aera_article = stockage_aera_article
        hstockage_aera_article.article = stockage_aera_article.article
        hstockage_aera_article.stockage_aera = stockage_aera_article.stockage_aera
        hstockage_aera_article.available_volume = stockage_aera_article.available_volume
        hstockage_aera_article.is_active = stockage_aera_article.is_active
        hstockage_aera_article.date = stockage_aera_article.date
        hstockage_aera_article.operation = operation
        hstockage_aera_article.user = user

        hstockage_aera_article.save()

    @staticmethod
    def create(
        article: Article,
        stockage_aera: StockageAera,
        volume: float,
        user: str
    ):
        """ associate an aera stockage with a product """
        try:
            stockage_aera_article = StockageAeraArticle.objects.get(
                article=article,
                stockage_aera=stockage_aera
            )
            stockage_aera.is_active = True
        except StockageAeraArticle.DoesNotExist:
            stockage_aera_article = StockageAeraArticle()
            stockage_aera_article.stockage_aera = stockage_aera
            stockage_aera_article.article = article

        stockage_aera_article.available_volume += volume
        stockage_aera_article.available_volume = round(stockage_aera_article.available_volume, 3)

        try:
            with transaction.atomic():
                stockage_aera_article.save()
                StockageAeraArticle.insertHistory(
                    stockage_aera_article=stockage_aera_article,
                    user=user,
                    operation=1
                )
            return stockage_aera_article
        except DatabaseError:
            return None


class StockagePartnerArticle(BaseUUIDModel):
    stockage_partner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="stockagepartnerarticles",
        editable=False
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="stockagepartnerarticles",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="stockagepartnerarticles",
        editable=False
    )
    price_sale = models.IntegerField()
    price_car = models.IntegerField()

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["price_sale", "price_car", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.stockage_partner.name, self.article.name)

    @staticmethod
    def insertHistory(
        stockage_partner_article: "StockagePartnerArticle",
        user: str,
        operation: int
    ):
        hstockage_partner_article = HStockagePartnerArticle()
        hstockage_partner_article.stockage_partner_article = stockage_partner_article
        hstockage_partner_article.stockage_partner = stockage_partner_article.stockage_partner
        hstockage_partner_article.stockage_aera = stockage_partner_article.stockage_aera
        hstockage_partner_article.article = stockage_partner_article.article
        hstockage_partner_article.price_sale = stockage_partner_article.price_sale
        hstockage_partner_article.price_car = stockage_partner_article.price_car
        hstockage_partner_article.is_active = stockage_partner_article.is_active
        hstockage_partner_article.date = stockage_partner_article.date
        hstockage_partner_article.operation = operation
        hstockage_partner_article.user = user

        hstockage_partner_article.save()

    @staticmethod
    def create(
        stockage_partner: StockagePartner,
        article: Article,
        stockage_aera: StockageAera,
        price_sale: int,
        price_car: int,
        user: str
    ):
        """ associate stockage partner an product """
        try:
            stockage_partner_article = StockagePartnerArticle.objects.get(
                stockage_partner=stockage_partner,
                article=article,
                stockage_aera=stockage_aera
            )
            stockage_partner_article.is_active = True
        except StockagePartnerArticle.DoesNotExist:
            stockage_partner_article = StockagePartnerArticle()
            stockage_partner_article.stockage_partner = stockage_partner
            stockage_partner_article.article = article
            stockage_partner_article.stockage_aera = stockage_aera

        stockage_partner_article.price_car = price_car
        stockage_partner_article.price_sale = price_sale

        try:
            with transaction.atomic():
                stockage_partner_article.save()
                StockagePartnerArticle.insertHistory(
                    stockage_partner_article=stockage_partner_article,
                    user=user,
                    operation=1
                )
            return stockage_partner_article
        except DatabaseError:
            return None

    def change(
        self,
        stockage_aera: StockageAera,
        price_sale: int,
        price_car: int,
        user: str
    ):
        """ update an association stockage partner product """
        self.stockage_aera = stockage_aera
        self.price_car = price_car
        self.price_sale = price_sale

        try:
            with transaction.atomic():
                self.save()
                StockagePartnerArticle.insertHistory(
                    stockage_partner_article=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None


class Depot(BaseUUIDModel):
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="depots",
        editable=False
    )
    numero = models.CharField(max_length=50)
    leader = models.CharField(max_length=100, default='unknow')

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["numero"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.career.name, self.numero)

    @staticmethod
    def insertHistory(
        depot: "Depot",
        user: str,
        operation: int
    ):
        hdepot = HDepot()
        hdepot.depot = depot
        hdepot.career = depot.career
        hdepot.numero = depot.numero
        hdepot.leader = depot.leader
        hdepot.is_active = depot.is_active
        hdepot.date = depot.date
        hdepot.operation = operation
        hdepot.user = user

        hdepot.save()

    @staticmethod
    def create(
        career: Carriere,
        numero: str,
        leader: str,
        user: str
    ):
        """ associate career an depot """
        try:
            depot = Depot.objects.get(
                career=career,
                numero=numero
            )
            depot.is_active = True
        except Depot.DoesNotExist:
            depot = Depot()
            depot.career = career
            depot.numero = numero
        depot.leader = leader

        try:
            with transaction.atomic():
                depot.save()
                Depot.insertHistory(
                    depot=depot, user=user, operation=1)
            return depot
        except DatabaseError:
            return None

    def change(
        self,
        numero: str,
        leader: str,
        user: str
    ):
        """ update an association career depot """
        self.numero = numero
        self.leader = leader

        try:
            with transaction.atomic():
                self.save()
                Depot.insertHistory(
                    depot=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete depot """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()
                Depot.insertHistory(
                    depot=self, user=user, operation=3)
            return self
        except DatabaseError:
            return None


class ProductBalance(BaseUUIDModel):
    depot = models.ForeignKey(
        Depot,
        on_delete=models.RESTRICT,
        related_name="productbalances",
        editable=False,
        null=True
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="productbalances",
        editable=False,
        null=True
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="productbalances",
        editable=False,
        null=True
    )
    stockage_partner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="productbalances",
        editable=False,
        null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="productbalances",
        editable=False
    )
    balance = models.CharField(max_length=2000)
    action = models.IntegerField(choices=BALANCE_OPERATION_CHOICE)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["date", 'action']

    def __str__(self):
        """ name in the administration """
        return "(%s)" % (self.action)

    @staticmethod
    def insertHistory(
        product_balance: "ProductBalance",
        user: str,
        operation: int
    ):
        hproduct_balance = HProductBalance()
        hproduct_balance.product_balance = product_balance
        hproduct_balance.depot = product_balance.depot
        hproduct_balance.career = product_balance.career
        hproduct_balance.article = product_balance.article
        hproduct_balance.stockage_aera = product_balance.stockage_aera
        hproduct_balance.stockage_partner = product_balance.stockage_partner
        hproduct_balance.balance = product_balance.balance
        hproduct_balance.action = product_balance.action
        hproduct_balance.is_active = product_balance.is_active
        hproduct_balance.date = product_balance.date
        hproduct_balance.operation = operation
        hproduct_balance.user = user

        hproduct_balance.save()

    @staticmethod
    def create(
        career: Carriere or None,
        article: Article,
        stockage_aera: StockageAera or None,
        stockage_partner: StockagePartner or None,
        depot: Depot or None,
        action: int,
        balance: float,
        operation: int,
        user: str
    ):
        """ calcul balance available """
        action = int(action)
        try:
            if action == 1:
                product_balance = ProductBalance.objects.get(
                    depot=depot,
                    career=career,
                    action=1
                )
            elif action == 2:
                product_balance = ProductBalance.objects.get(
                    career=career,
                    stockage_aera=stockage_aera,
                    action=2
                )
            elif action == 3:
                product_balance = ProductBalance.objects.get(
                    stockage_aera=stockage_aera,
                    stockage_partner=stockage_partner,
                    action=3
                )
            elif action == 4:
                product_balance = ProductBalance.objects.get(
                    stockage_aera=stockage_aera,
                    action=4
                )
            elif action == 5:
                product_balance = ProductBalance.objects.get(
                    stockage_partner=stockage_partner,
                    action=5
                )
            try:
                product_balance.balance = signing.loads(product_balance.balance)['balance']
            except signing.BadSignature:
                product_balance.balance = 0
        except ProductBalance.DoesNotExist:
            product_balance = ProductBalance()
            product_balance.action = action
            if action == 1:
                product_balance.depot = depot
                product_balance.career = career
            elif action == 2:
                product_balance.career = career
                product_balance.stockage_aera = stockage_aera
            elif action == 3:
                product_balance.stockage_aera = stockage_aera
                product_balance.stockage_partner = stockage_partner
            elif action == 4:
                product_balance.stockage_aera = stockage_aera
            elif action == 5:
                product_balance.stockage_partner = stockage_partner

            try:
                product_balance.balance = signing.loads(product_balance.balance)['balance']
            except signing.BadSignature:
                product_balance.balance = 0
                # signal alert

        product_balance.is_active = True
        product_balance.article = article

        if operation == 1:
            volume = round(product_balance.balance + balance, 3)
        else:
            volume = round(product_balance.balance - balance, 3)

        volume = signing.dumps({'balance': volume})
        product_balance.balance = volume

        try:
            with transaction.atomic():
                product_balance.save()
                ProductBalance.insertHistory(
                    product_balance=product_balance, user=user, operation=1)
                return product_balance
        except DatabaseError:
            return None

    @staticmethod
    def readBalanceAireStockage(
        article: Article,
        stockage_aera: StockageAera,
        user: str
    ):
        """ calcul balance available """
        try:
            product_balance = ProductBalance.objects.get(
                stockage_aera=stockage_aera,
                article=article,
                action__in=[4, '4']
            )
        except ProductBalance.DoesNotExist:
            transfers = Transfer.objects.filter(
                article=article,
                stockage_aera=stockage_aera,
                status=2
            )
            volume = 0
            for transfer in transfers:
                volume += transfer.volume_receptionned
            volume = round(volume, 3)
            product_balance = ProductBalance.create(
                stockage_aera=stockage_aera,
                article=article,
                stockage_partner=None,
                career=None,
                depot=None,
                user=user,
                balance=volume,
                operation=1,
                action=4
            )
        product_balance.balance = signing.loads(
            product_balance.balance)['balance']
        return product_balance

    @staticmethod
    def readBalanceAirePartner(
        article: Article,
        stockage_partner: StockagePartner,
        user: str
    ):
        """ calcul balance available """
        try:
            product_balance = ProductBalance.objects.get(
                stockage_partner=stockage_partner,
                article=article,
                action__in=[5, '5']
            )
        except ProductBalance.DoesNotExist:
            sales = Sale.objects.filter(
                article=article,
                stockage_partner=stockage_partner,
                type_sale=1,
                status__in=[2, 3]
            )
            volume = 0
            for sale in sales:
                volume += sale.volume
            volume = round(volume, 3)
            product_balance = ProductBalance.create(
                stockage_aera=None,
                article=article,
                stockage_partner=stockage_partner,
                career=None,
                depot=None,
                user=user,
                balance=volume,
                operation=1,
                action=5
            )
        product_balance.balance = signing.loads(
            product_balance.balance)['balance']
        return product_balance


class Transfer(BaseUUIDModel):
    tractor = models.ForeignKey(
        Tractor,
        on_delete=models.RESTRICT,
        related_name="transfers",
        editable=False
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.RESTRICT,
        related_name="transfers",
        editable=False,
        null=True
    )
    waybill = models.CharField(max_length=50)
    depot = models.ForeignKey(
        Depot,
        on_delete=models.RESTRICT,
        related_name="transfers",
        editable=False,
        null=True
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="transfers",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="transfers",
        editable=False
    )
    transfer_slip = models.CharField(max_length=50)
    physical_waybill = models.CharField(max_length=50)
    driver = models.CharField(max_length=50, blank=True, default=" ")
    status = models.IntegerField(choices=STATUS_TRANSFER_CHOICE)
    following = models.CharField(default="0", max_length=1000)
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="transfers",
        editable=False
    )
    product_name = models.CharField(default="inconnue", max_length=100)
    product_price = models.IntegerField(default=0)
    transport_price = models.IntegerField(default=0)
    volume_transferred = models.FloatField(default=0)
    volume_receptionned = models.FloatField(default=0)
    date_recep = models.DateTimeField(null=True)
    date_op = models.DateTimeField()

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["status", "-date_recep", "-date_op", "date", "waybill"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.waybill, self.driver)

    @staticmethod
    def insertHistory(
        transfer: "Transfer",
        user: str,
        operation: int
    ):
        htransfer = HTransfer()
        htransfer.transfer = transfer
        htransfer.tractor = transfer.tractor
        htransfer.trailer = transfer.trailer
        htransfer.waybill = transfer.waybill
        htransfer.depot = transfer.depot
        htransfer.waybill = transfer.waybill
        htransfer.depot = transfer.depot
        htransfer.career = transfer.career
        htransfer.stockage_aera = transfer.stockage_aera
        htransfer.transfer_slip = transfer.transfer_slip
        htransfer.physical_waybill = transfer.physical_waybill
        htransfer.driver = transfer.driver
        htransfer.status = transfer.status
        htransfer.following = transfer.following
        htransfer.article = transfer.article
        htransfer.product_name = transfer.product_name
        htransfer.product_price = transfer.product_price
        htransfer.transport_price = transfer.transport_price
        htransfer.volume_transferred = transfer.volume_transferred
        htransfer.volume_receptionned = transfer.volume_receptionned
        htransfer.date_recep = transfer.date_recep
        htransfer.date_op = transfer.date_op
        htransfer.is_active = transfer.is_active
        htransfer.date = transfer.date
        htransfer.operation = operation
        htransfer.user = user

        htransfer.save()

    @staticmethod
    def create(
        tractor: Tractor,
        trailer: Trailer,
        depot: Depot or None,
        career: Carriere,
        stockage_aera: StockageAera,
        transfer_slip: str,
        physical_waybill: str,
        driver: str,
        article: Article,
        volume_transferred: float,
        date_op: str,
        user: str
    ):
        """ create a transfer """
        transfer = Transfer()
        transfer.tractor = tractor
        transfer.trailer = trailer

        fin = datetime.datetime.now().strftime("%m/%Y")
        numero = str(
            10001 + len(
                Transfer.objects.filter(
                    waybill__contains=fin
                )
            )
        ) + "/" + fin
        transfer.waybill = numero

        transfer.depot = depot
        transfer.career = career
        transfer.stockage_aera = stockage_aera
        transfer.transfer_slip = transfer_slip
        transfer.physical_waybill = physical_waybill
        transfer.driver = driver
        transfer.status = 1

        transfer.following = "-1"
        transfer.article = article
        transfer.product_name = article.name

        associate = CareerArticle.objects.get(
            career=career,
            article=article,
            is_active=True
        )
        transfer.product_price = associate.price_sale
        transfer.transport_price = associate.price_car
        transfer.volume_transferred = round(volume_transferred, 3)
        transfer.date_op = datetime.datetime.strptime(
            date_op, '%d-%m-%Y %H:%M'
        )

        try:
            with transaction.atomic():
                transfer.save()
                Transfer.insertHistory(
                    transfer=transfer, user=user, operation=1)
            return transfer
        except DatabaseError:
            return None

    def change_following(self, id: str, user: str):
        self.following = id
        try:
            with transaction.atomic():
                self.save()
                Transfer.insertHistory(
                    transfer=self, user=user, operation=7)
            return self
        except DatabaseError:
            return None

    def reception(self, volume: float, date_recep: str, user: str):
        self.status = 2
        self.volume_receptionned = round(volume, 3)
        self.date_recep = datetime.datetime.strptime(
            date_recep, '%d-%m-%Y %H:%M'
        )

        no_following = Transfer.objects.filter(
            following="-1",
            is_active=True
        )
        if len(no_following) > 1:
            i = 0
            max = len(no_following)
            for item in no_following:
                if max > i + 1:
                    Transfer.change_following(
                        self=item,
                        id=no_following[i+1].id,
                        user=user
                    )

        try:
            with transaction.atomic():
                self.save()
                Transfer.insertHistory(
                    transfer=self,
                    user=user,
                    operation=8
                )

                if self.depot is not None:
                    ProductBalance.create(
                        career=self.career,
                        depot=self.depot,
                        article=self.article,
                        stockage_aera=self.stockage_aera,
                        stockage_partner=None,
                        user=user,
                        action=1,
                        operation=1,
                        balance=volume
                    )
                ProductBalance.create(
                    career=self.career,
                    stockage_aera=self.stockage_aera,
                    article=self.article,
                    stockage_partner=None,
                    depot=self.depot,
                    user=user,
                    action=2,
                    operation=1,
                    balance=volume
                )
                ProductBalance.create(
                    stockage_aera=self.stockage_aera,
                    article=self.article,
                    stockage_partner=None,
                    career=self.career,
                    depot=self.depot,
                    user=user,
                    balance=volume,
                    operation=1,
                    action=4
                )
            return self
        except DatabaseError:
            return None

    def receptionVente(
        self,
        volume: float,
        date_recep: str,
        stockagePartner: StockagePartner or None,
        destination: str,
        sale_unit_price: int,
        user: str
    ):
        try:
            with transaction.atomic():
                self.reception(
                    volume=volume,
                    date_recep=date_recep,
                    user=user
                )
                Sale.create(
                    sale_slip=self.transfer_slip,
                    stockage_aera=self.stockage_aera,
                    stockage_partner=stockagePartner,
                    article=self.article,
                    destination=destination,
                    sale_unit_price=sale_unit_price,
                    driver=self.driver,
                    tractor=self.tractor,
                    trailer=self.trailer,
                    volume=self.volume_receptionned,
                    type_sale=1 if stockagePartner is not None else 2,
                    date_op=date_recep,
                    user=user
                )
            return self
        except DatabaseError:
            return None


class Sale(BaseUUIDModel):
    sale_slip = models.CharField(default="inconnue", max_length=50)
    waybill = models.CharField(max_length=50)
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="sales",
        null=True
    )
    stockage_partner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="sales",
        null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="sales"
    )
    destination = models.CharField(
        max_length=100,
        default=" ",
        blank=True
    )
    product_name = models.CharField(default="inconnue", max_length=100)
    product_price = models.IntegerField(default=0)
    sale_unit_price = models.IntegerField(default=0)
    driver = models.CharField(max_length=50, blank=True, default=" ")
    tractor = models.ForeignKey(
        Tractor,
        on_delete=models.RESTRICT,
        related_name="sales",
        editable=False
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.RESTRICT,
        related_name="sales",
        editable=False,
        null=True
    )
    volume = models.FloatField(default=0, verbose_name="volume vendu")
    volume_r = models.FloatField(default=0, verbose_name="volume receptionné")
    status = models.IntegerField(choices=STATUS_SALE_CHOICE)
    type_sale = models.IntegerField(choices=SALE_CHOICE)
    date_op = models.DateTimeField(null=True)
    date_recep = models.DateTimeField(null=True)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["status", "-date_op", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.waybill, self.status)

    @staticmethod
    def insertHistory(
        sale: "Sale",
        user: str,
        operation: int
    ):
        hsale = HSale()
        hsale.sale = sale
        hsale.sale_slip = sale.sale_slip
        hsale.waybill = sale.waybill
        hsale.stockage_aera = sale.stockage_aera
        hsale.stockage_partner = sale.stockage_partner
        hsale.article = sale.article
        hsale.destination = sale.destination
        hsale.product_name = sale.product_name
        hsale.product_price = sale.product_price
        hsale.sale_unit_price = sale.sale_unit_price
        hsale.driver = sale.driver
        hsale.tractor = sale.tractor
        hsale.trailer = sale.trailer
        hsale.volume = sale.volume
        hsale.volume_r = sale.volume_r
        hsale.status = sale.status
        hsale.type_sale = sale.type_sale
        hsale.date_op = sale.date_op
        hsale.date_recep = sale.date_recep
        hsale.is_active = sale.is_active
        hsale.date = sale.date
        hsale.operation = operation
        hsale.user = user

        hsale.save()

    @staticmethod
    def create(
        sale_slip: str,
        stockage_aera: StockageAera or None,
        stockage_partner: StockagePartner or None,
        article: Article,
        destination: str,
        sale_unit_price: int,
        driver: str,
        tractor: Tractor,
        trailer: Trailer,
        volume: float,
        type_sale: int,
        date_op: str,
        user: str
    ):
        """ associate career an product """
        sale = Sale()
        sale.sale_slip = sale_slip

        fin = datetime.datetime.now().strftime("%m/%Y")
        numero = str(10001 + len(Sale.objects.filter(waybill__contains=fin))) + "/" + fin
        sale.waybill = numero

        sale.stockage_aera = stockage_aera
        sale.stockage_partner = stockage_partner
        sale.article = article
        sale.destination = destination
        sale.product_name = article.name

        type_sale = int(type_sale)
        if type_sale == 1:
            stockage_article_partner = StockagePartnerArticle(
                stockage_aera=stockage_aera,
                article=article,
                stockage_partner=stockage_partner
            )
            sale.product_price = stockage_article_partner.price_sale
        else:
            sale.product_price = 0

        sale.sale_unit_price = sale_unit_price
        sale.driver = driver
        sale.tractor = tractor
        sale.trailer = trailer
        sale.volume = volume
        if type_sale == 1:
            sale.status = 1
        else:
            sale.status = 2
            sale.date_recep = datetime.datetime.strptime(
                date_op, '%d-%m-%Y %H:%M'
            )

        sale.type_sale = type_sale
        sale.date_op = datetime.datetime.strptime(date_op, '%d-%m-%Y %H:%M')

        try:
            with transaction.atomic():
                sale.save()
                Sale.insertHistory(
                    sale=sale, user=user, operation=1)
                ProductBalance.create(
                    career=None,
                    article=sale.article,
                    stockage_aera=sale.stockage_aera,
                    stockage_partner=sale.stockage_partner,
                    depot=None,
                    action=5 if sale.type_sale == 3 else 4,
                    balance=sale.volume,
                    operation=2,
                    user=user
                )
                if type_sale == 2:
                    Annuaire.create(sale=sale, user=user)
            return sale
        except DatabaseError:
            return None

    def reception(
        self,
        user: str
    ):
        """ receive a sale """
        self.status = 2

        try:
            with transaction.atomic():
                self.save()
                Sale.insertHistory(
                    sale=self, user=user, operation=2)
                Annuaire.create(sale=self)
            return self
        except DatabaseError:
            return None


class Annuaire(BaseUUIDModel):
    transfert = models.ForeignKey(
        Transfer,
        on_delete=models.RESTRICT,
        related_name="annuaires"
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.RESTRICT,
        related_name="annuaires"
    )
    volume_restant = models.FloatField()
    last = models.BooleanField(default=True)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["last", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.transfert.waybill, self.sale.waybill)

    @staticmethod
    def create(
        sale: Sale,
        user: str
    ):
        """ sale annuary used for redevance """
        annuaire = Annuaire()
        try:
            previous_annuaire = Annuaire.objects.get(
                last=True,
                sale__type_sale__in=[1, 2, "1", "2"],
                sale__status=2
            )
        except Annuaire.DoesNotExist:
            previous_annuaire = None

        if previous_annuaire is not None:
            if previous_annuaire.volume_restant != 0:
                try:
                    with transaction.atomic():
                        previous_annuaire.last = False
                        previous_annuaire.save()
                        transf = previous_annuaire.transfert
                        # décrémente le volume du dépot à la carriere
                        ProductBalance.create(
                            career=transf.career,
                            article=transf.article,
                            action=1,
                            balance=transf.volume_receptionned if sale.volume >= previous_annuaire.volume_restant else sale.volume,
                            depot=transf.depot,
                            operation=2,
                            stockage_aera=transf.stockage_aera,
                            stockage_partner=None,
                            user=user
                        )
                        # décrémente le volume de la carrière au hub minier
                        ProductBalance.create(
                            career=transf.career,
                            article=transf.article,
                            action=2,
                            balance=transf.volume_receptionned if sale.volume >= previous_annuaire.volume_restant else sale.volume,
                            depot=transf.depot,
                            operation=2,
                            stockage_aera=transf.stockage_aera,
                            stockage_partner=None,
                            user=user
                        )
                        if sale.volume > previous_annuaire.volume_restant:
                            annuaire.volume_restant = 0
                            annuaire.transfert = previous_annuaire.transfert
                            annuaire.sale = sale
                            annuaire.last = True
                            annuaire.save()
                            previous_annuaire.transfert.status = 4
                            previous_annuaire.transfert.save()
                            Annuaire.create(sale=sale)
                        elif sale.volume == previous_annuaire.volume_restant:
                            annuaire.volume_restant = 0
                            annuaire.transfert = previous_annuaire.transfert
                            annuaire.sale = sale
                            annuaire.last = True
                            annuaire.save()
                            previous_annuaire.transfert.status = 4
                            previous_annuaire.transfert.save()
                        else:
                            annuaire.volume_restant = round(
                                previous_annuaire.volume_restant - sale.volume,
                                3
                            )
                            annuaire.transfert = previous_annuaire.transfert
                            annuaire.sale = sale
                            annuaire.last = True
                            annuaire.save()
                            previous_annuaire.transfert.status = 3
                            previous_annuaire.transfert.save()
                    return annuaire
                except DatabaseError:
                    return None
            else:
                try:
                    transfer = Transfer.objects.get(
                        id=previous_annuaire.transfert.following,
                        article=sale.article
                    )
                except Transfer.DoesNotExist:
                    transfers = Transfer.objects.filter(
                        status=3,
                        article=sale.article
                    )
                    if len(transfers) > 0:
                        transfer = transfers[0]
                    else:
                        transfers = Transfer.objects.filter(
                            status=2,
                            article=sale.article
                        )
                        transfer = transfers[0]
                try:
                    with transaction.atomic():
                        # décrémente le volume du dépot à la carriere
                        ProductBalance.create(
                            career=transfer.career,
                            article=transfer.article,
                            action=1,
                            balance=transfer.volume_receptionned if sale.volume >= transfer.volume_receptionned else sale.volume,
                            depot=transfer.depot,
                            operation=2,
                            stockage_aera=transfer.stockage_aera,
                            stockage_partner=None,
                            user=user
                        )
                        # décrémente le volume de la carrière au hub minier
                        ProductBalance.create(
                            career=transfer.career,
                            article=transfer.article,
                            action=2,
                            balance=transfer.volume_receptionned if sale.volume >= transfer.volume_receptionned else sale.volume,
                            depot=transfer.depot,
                            operation=2,
                            stockage_aera=transfer.stockage_aera,
                            stockage_partner=None,
                            user=user
                        )
                        if sale.volume > transfer.volume_receptionned:
                            annuaire.volume_restant = 0
                            annuaire.transfert = transfer
                            annuaire.sale = sale
                            annuaire.last = True
                            annuaire.save()
                            transfer.status = 4
                            transfer.save()
                            Annuaire.create(sale=sale)
                        elif sale.volume == transfer.volume_receptionned:
                            annuaire.volume_restant = 0
                            annuaire.transfert = transfer
                            annuaire.sale = sale
                            annuaire.last = True
                            annuaire.save()
                            transfer.status = 4
                            transfer.save()
                        else:
                            annuaire.volume_restant = round(
                                transfer.volume_receptionned - sale.volume,
                                3
                            )
                            annuaire.transfert = transfer
                            annuaire.sale = sale
                            annuaire.last = True
                            annuaire.save()
                            transfer.status = 3
                            transfer.save()
                except DatabaseError:
                    return None
        else:
            transfers = Transfer.objects.filter(
                status=3,
                article=sale.article
            )
            if len(transfers) > 0:
                transfer = transfers[0]
            else:
                transfers = Transfer.objects.filter(
                    status=2
                )
                transfer = transfers[0]

            # décrémente le volume du dépot à la carriere
            ProductBalance.create(
                career=transfer.career,
                article=transfer.article,
                action=1,
                balance=transfer.volume_receptionned if sale.volume >= transfer.volume_receptionned else sale.volume,
                depot=transfer.depot,
                operation=2,
                stockage_aera=transfer.stockage_aera,
                stockage_partner=None,
                user=user
            )
            # décrémente le volume de la carrière au hub minier
            ProductBalance.create(
                career=transfer.career,
                article=transfer.article,
                action=2,
                balance=transfer.volume_receptionned if sale.volume >= transfer.volume_receptionned else sale.volume,
                depot=transfer.depot,
                operation=2,
                stockage_aera=transfer.stockage_aera,
                stockage_partner=None,
                user=user
            )
            if sale.volume > transfer.volume_receptionned:
                annuaire.volume_restant = 0
                annuaire.transfert = transfer
                annuaire.sale = sale
                annuaire.last = True
                annuaire.save()
                transfer.status = 4
                transfer.save()
                Annuaire.create(sale=sale)
            elif sale.volume == transfer.volume_receptionned:
                annuaire.volume_restant = 0
                annuaire.transfert = transfer
                annuaire.sale = sale
                annuaire.last = True
                annuaire.save()
                transfer.status = 4
                transfer.save()
            else:
                annuaire.volume_restant = round(
                    transfer.volume_receptionned - sale.volume,
                    3
                )
                annuaire.transfert = transfer
                annuaire.sale = sale
                annuaire.last = True
                annuaire.save()
                transfer.status = 3
                transfer.save()

# journalisation


class HStockageAera(BaseHistoryModel):
    """ stockage aera history """
    stockageaera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hstockageaera",
        editable=False
    )
    name = models.CharField(max_length=100, editable=False)
    village = models.CharField(max_length=100, editable=False)


class HStockagePartner(BaseHistoryModel):
    """ stockage partner history """
    stockagePartner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="hstockagepartners",
        editable=False
    )
    firm = models.CharField(max_length=1000,editable=False)
    name = models.CharField(max_length=100, editable=False)
    village = models.CharField(max_length=100, editable=False)


class HCarriere(BaseHistoryModel):
    carriere = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="hcarriere",
        editable=False
    )
    village = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    uin = models.CharField(max_length=13)
    localisation = models.CharField(max_length=1000, default='waiting GPS')
    proprio = models.CharField(max_length=100, default='proprio')
    is_suspend = models.BooleanField(default=False)


class HCareerLv(BaseHistoryModel):
    careerlv = models.ForeignKey(
        CareerLv,
        on_delete=models.RESTRICT,
        related_name="hcareerlvs",
        editable=False
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="hcareerlvs",
        editable=False
    )
    last_demand_quantity = models.FloatField()
    last_demand_volume = models.FloatField()
    last_approve_quantity = models.FloatField(default=0)
    last_approve_volume = models.FloatField(default=0)
    is_waiting_approve = models.BooleanField(default=True)
    available_quantity = models.FloatField(default=0)
    available_volume = models.FloatField(default=0)


class HStockageAeraLv(BaseHistoryModel):
    stockageaeralv = models.ForeignKey(
        StockageAeraLv,
        on_delete=models.RESTRICT,
        related_name="hstockageaeralv",
        editable=False
    )
    stockageaera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hstockageaeralv",
        editable=False
    )
    last_demand_quantity = models.FloatField()
    last_demand_volume = models.FloatField()
    last_approve_quantity = models.FloatField(default=0)
    last_approve_volume = models.FloatField(default=0)
    is_waiting_approve = models.BooleanField(default=True)
    available_quantity = models.FloatField(default=0)
    available_volume = models.FloatField(default=0)


class HCareerArticle(BaseHistoryModel):
    careerarticle = models.ForeignKey(
        CareerArticle,
        on_delete=models.RESTRICT,
        related_name="hcareerarticles",
        editable=False
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="hcareerarticles",
        editable=False
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="hcareerarticles",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hcareerarticles",
        editable=False
    )
    price_sale = models.IntegerField()
    price_car = models.IntegerField()


class HStockageAeraArticle(BaseHistoryModel):
    stockage_aera_article = models.ForeignKey(
        StockageAeraArticle,
        on_delete=models.RESTRICT,
        related_name="hstockageaeraarticles",
        editable=False
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="hstockageaeraarticles",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hstockageaeraarticles",
        editable=False
    )
    available_volume = models.FloatField()


class HStockagePartnerArticle(BaseHistoryModel):
    stockage_partner_article = models.ForeignKey(
        StockagePartnerArticle,
        on_delete=models.RESTRICT,
        related_name="hstockagepartnerarticles",
        editable=False
    )
    stockage_partner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="hstockagepartnerarticles",
        editable=False
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="hstockagepartnerarticles",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hstockagepartnerarticles",
        editable=False
    )
    price_sale = models.IntegerField()
    price_car = models.IntegerField()


class HDepot(BaseHistoryModel):
    depot = models.ForeignKey(
        Depot,
        on_delete=models.RESTRICT,
        related_name="hdepots",
        editable=False
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="hdepots",
        editable=False
    )
    numero = models.CharField(max_length=50)
    leader = models.CharField(max_length=100)


class HProductBalance(BaseHistoryModel):
    product_balance = models.ForeignKey(
        ProductBalance,
        on_delete=models.RESTRICT,
        related_name="hproductbalances",
        editable=False
    )
    depot = models.ForeignKey(
        Depot,
        on_delete=models.RESTRICT,
        related_name="hproductbalances",
        editable=False,
        null=True
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="hproductbalances",
        editable=False,
        null=True
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hproductbalances",
        editable=False,
        null=True
    )
    stockage_partner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="hproductbalances",
        editable=False,
        null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="hproductbalances",
        editable=False,
        null=True
    )
    balance = models.CharField(max_length=2000)
    action = models.IntegerField(choices=BALANCE_OPERATION_CHOICE)


class HTransfer(BaseHistoryModel):
    transfer = models.ForeignKey(
        Transfer,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False
    )
    tractor = models.ForeignKey(
        Tractor,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False,
        null=True
    )
    waybill = models.CharField(max_length=50)
    depot = models.ForeignKey(
        Depot,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False,
        null=True
    )
    career = models.ForeignKey(
        Carriere,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False
    )
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False
    )
    transfer_slip = models.CharField(max_length=50)
    physical_waybill = models.CharField(max_length=50)
    driver = models.CharField(max_length=50, blank=True, default=" ")
    status = models.IntegerField(choices=STATUS_TRANSFER_CHOICE)
    following = models.CharField(default="0", max_length=1000)
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="htransfers",
        editable=False
    )
    product_name = models.CharField(default="inconnue", max_length=100)
    product_price = models.IntegerField(default=0)
    transport_price = models.IntegerField(default=0)
    volume_transferred = models.FloatField(default=0)
    volume_receptionned = models.FloatField(default=0)
    date_recep = models.DateTimeField(null=True)
    date_op = models.DateTimeField()


class HAnnuaire(BaseHistoryModel):
    annuaire = models.ForeignKey(
        Annuaire,
        on_delete=models.RESTRICT,
        related_name="hannuaires"
    )
    transfert = models.ForeignKey(
        Transfer,
        on_delete=models.RESTRICT,
        related_name="hannuaires"
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.RESTRICT,
        related_name="hannuaires"
    )
    volume = models.FloatField()
    last = models.BooleanField(default=True)


class HSale(BaseHistoryModel):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.RESTRICT,
        related_name="hsales"
    )
    sale_slip = models.CharField(default="inconnue", max_length=50)
    waybill = models.CharField(max_length=50)
    stockage_aera = models.ForeignKey(
        StockageAera,
        on_delete=models.RESTRICT,
        related_name="hsales",
        null=True
    )
    stockage_partner = models.ForeignKey(
        StockagePartner,
        on_delete=models.RESTRICT,
        related_name="hsales",
        null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.RESTRICT,
        related_name="hsales"
    )
    destination = models.CharField(
        max_length=100,
        default=" ",
        blank=True
    )
    product_name = models.CharField(default="inconnue", max_length=100)
    product_price = models.IntegerField(default=0)
    sale_unit_price = models.IntegerField(default=0)
    driver = models.CharField(max_length=50, blank=True, default=" ")
    tractor = models.ForeignKey(
        Tractor,
        on_delete=models.RESTRICT,
        related_name="hsales",
        editable=False
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.RESTRICT,
        related_name="hsales",
        editable=False,
        null=True
    )
    volume = models.FloatField(default=0, verbose_name="volume vendu")
    volume_r = models.FloatField(default=0, verbose_name="volume receptionné")
    status = models.IntegerField(choices=STATUS_SALE_CHOICE)
    type_sale = models.IntegerField(choices=SALE_CHOICE)
    date_op = models.DateTimeField(null=True)
    date_recep = models.DateTimeField(null=True)
