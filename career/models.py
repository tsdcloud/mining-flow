from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseUUIDModel
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

        stockageaera._change_reason = json.dumps({
            "reason": "Add a new mining hub",
            "user": user
        })
        stockageaera._history_date = datetime.now()
        stockageaera.save()
        return stockageaera

    def change(
        self,
        name: str,
        user: str
    ):
        """ change stockage aera """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update mining hub",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete stockage aera """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete mining hub",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active stockage aera previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Delete mining hub",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

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

        stockagepartner._change_reason = json.dumps({
            "reason": "Add a new sale depot",
            "user": user
        })
        stockagepartner._history_date = datetime.now()
        stockagepartner.save()
        return stockagepartner

    def change(
        self,
        name: str,
        user: str
    ):
        """ change stockage aera """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update sale depot",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete stockage partner """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete sale depot",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active stockage partner previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore sale depot",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

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

        carriere._change_reason = json.dumps({
            "reason": "Add a new career",
            "user": user
        })
        carriere._history_date = datetime.now()
        carriere.save()
        return carriere

    def change(
        self,
        name: str,
        niu: str,
        user: str
    ):
        """ change career """
        self.name = name.upper()
        self.niu = niu

        self._change_reason = json.dumps({
            "reason": "Update career",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete career """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete career",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active career previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Add a new career",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

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

        careerlv._change_reason = json.dumps({
            "reason": "Consignment note request for career",
            "user": user
        })
        careerlv._history_date = datetime.now()
        careerlv.save()
        return careerlv

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

        self._change_reason = json.dumps({
            "reason": "Approval of consignment note request for career",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


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

        stockageaeralv._change_reason = json.dumps({
            "reason": "Consignment note request for mining hub",
            "user": user
        })
        stockageaeralv._history_date = datetime.now()
        stockageaeralv.save()
        return stockageaeralv

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

        self._change_reason = json.dumps({
            "reason": "Approval of consignment note request for mining hub",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


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

        careerarticle._change_reason = json.dumps({
            "reason": "Associate a career with an article",
            "user": user
        })
        careerarticle._history_date = datetime.now()
        careerarticle.save()
        return careerarticle

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

        self._change_reason = json.dumps({
            "reason": "Modify the association of a career and an article",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete careerarticle """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete the association of a career and an article",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


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
        stockage_aera_article.available_volume = round(
            stockage_aera_article.available_volume, 3
        )

        stockage_aera_article._change_reason = json.dumps({
            "reason": "Associate a mining hub with an article",
            "user": user
        })
        stockage_aera_article._history_date = datetime.now()
        stockage_aera_article.save()
        return stockage_aera_article


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

        stockage_partner_article._change_reason = json.dumps({
            "reason": "Associate a sale depot with an article",
            "user": user
        })
        stockage_partner_article._history_date = datetime.now()
        stockage_partner_article.save()
        return stockage_partner_article

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

        self._change_reason = json.dumps({
            "reason": "Modify the association of a sale depot and an article",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


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

        depot._change_reason = json.dumps({
            "reason": "Add depot",
            "user": user
        })
        depot._history_date = datetime.now()
        depot.save()
        return depot

    def change(
        self,
        numero: str,
        leader: str,
        user: str
    ):
        """ update an association career depot """
        self.numero = numero
        self.leader = leader

        self._change_reason = json.dumps({
            "reason": "Update depot",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete depot """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete depot",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


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
        lv = None
        try:
            if action == 1:
                product_balance = ProductBalance.objects.get(
                    depot=depot,
                    career=career,
                    action=1
                )
                lv = None
                text = "Update the deposit balance at the career"
            elif action == 2:
                product_balance = ProductBalance.objects.get(
                    career=career,
                    stockage_aera=stockage_aera,
                    action=2
                )
                lv = CareerLv.objects.get(
                    career=career
                )
                text = "Update the career balance at the mining hub"
            elif action == 3:
                product_balance = ProductBalance.objects.get(
                    stockage_aera=stockage_aera,
                    stockage_partner=stockage_partner,
                    action=3
                )
                lv = StockageAeraLv.objects.get(
                    stockageaera=stockage_aera)
                text = "Update the mining hub balance at the sale depot"
            elif action == 4:
                product_balance = ProductBalance.objects.get(
                    stockage_aera=stockage_aera,
                    action=4
                )
                lv = None
                text = "Update the career balance"
            elif action == 5:
                product_balance = ProductBalance.objects.get(
                    stockage_partner=stockage_partner,
                    action=5
                )
                lv = None
                text = "Update the sale depot balance"
            try:
                product_balance.balance = signing.loads(
                    product_balance.balance)['balance']
            except signing.BadSignature:
                product_balance.balance = 0
        except ProductBalance.DoesNotExist:
            product_balance = ProductBalance()
            product_balance.action = action
            if action == 1:
                product_balance.depot = depot
                product_balance.career = career
                text = "Update the deposit balance at the career"
            elif action == 2:
                product_balance.career = career
                product_balance.stockage_aera = stockage_aera
                lv = CareerLv.objects.get(
                    career=career
                )
                text = "Update the career balance at the mining hub"
            elif action == 3:
                product_balance.stockage_aera = stockage_aera
                product_balance.stockage_partner = stockage_partner
                lv = StockageAeraLv.objects.get(
                    stockageaera=stockage_aera)
                text = "Update the mining hub balance at the sale depot"
            elif action == 4:
                product_balance.stockage_aera = stockage_aera
                text = "Update the career balance"
            elif action == 5:
                product_balance.stockage_partner = stockage_partner
                text = "Update the sale depot balance"

            try:
                product_balance.balance = signing.loads(
                    product_balance.balance)['balance']
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
                product_balance._change_reason = json.dumps({
                    "reason": text,
                    "user": user
                })
                product_balance._history_date = datetime.now()
                product_balance.save()
                if lv is not None:
                    lv.available_quantity -= 1
                    lv.available_volume -= balance
                    lv._change_reason = json.dumps({
                        "reason": "Update available quantity",
                        "user": user
                    })
                    lv._history_date = datetime.now()
                    lv.save()
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

        fin = datetime.now().strftime("%m/%Y")
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
        transfer.date_op = datetime.strptime(
            date_op, '%d-%m-%Y %H:%M'
        )

        transfer._change_reason = json.dumps({
            "reason": "Add transfer",
            "user": user
        })
        transfer._history_date = datetime.now()
        transfer.save()
        return transfer

    def change_following(self, id: str, user: str):
        self.following = id
        self._change_reason = json.dumps({
            "reason": "Update following transfer",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def reception(self, volume: float, date_recep: str, user: str):
        self.status = 2
        self.volume_receptionned = round(volume, 3)
        self.date_recep = datetime.strptime(
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
                self._change_reason = json.dumps({
                    "reason": "To receive a transfer",
                    "user": user
                })
                self._history_date = datetime.now()
                self.save()

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

        fin = datetime.now().strftime("%m/%Y")
        numero = str(10001 + len(Sale.objects.filter(waybill__contains=fin))) + "/" + fin
        sale.waybill = numero

        sale.stockage_aera = stockage_aera
        sale.stockage_partner = stockage_partner
        sale.article = article
        sale.destination = destination
        sale.product_name = article.name

        type_sale = int(type_sale)
        if type_sale == 1:
            stockage_article_partner = StockagePartnerArticle.objects.get(
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
            sale.date_recep = datetime.strptime(
                date_op, '%d-%m-%Y %H:%M'
            )

        sale.type_sale = type_sale
        sale.date_op = datetime.strptime(date_op, '%d-%m-%Y %H:%M')

        try:
            with transaction.atomic():
                sale._change_reason = json.dumps({
                    "reason": "Add a new sale",
                    "user": user
                })
                sale._history_date = datetime.now()
                sale.save()
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
                if type_sale in [1, 2]:
                    lv = StockageAeraLv.objects.get(
                        stockageaera=sale.stockage_aera
                    )
                    lv.available_quantity -= 1
                    lv.available_volume -= sale.volume
                    lv.save()
            return sale
        except DatabaseError:
            return None

    def reception(
        self,
        volume,
        date_recep,
        user: str
    ):
        """ receive a sale """
        self.status = 2
        self.volume_r = volume
        self.date_recep = datetime.strptime(
            date_recep, '%d-%m-%Y %H:%M')

        try:
            with transaction.atomic():
                self._change_reason = json.dumps({
                    "reason": "To receive a sale",
                    "user": user
                })
                self._history_date = datetime.now()
                self.save()
                Annuaire.create(sale=self, user=user)
                ProductBalance.create(
                    career=None,
                    article=self.article,
                    stockage_aera=self.stockage_aera,
                    stockage_partner=self.stockage_partner,
                    depot=None,
                    action=5,
                    balance=volume,
                    operation=1,
                    user=user
                )
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
                sale__status=2,
                transfert__article=sale.article
            )
        except Annuaire.DoesNotExist:
            previous_annuaire = None
        except Annuaire.MultipleObjectsReturned:
            previous_annuaires = Annuaire.objects.filter(
                last=True,
                sale__type_sale__in=[1, 2, "1", "2"],
                sale__status=2,
                transfert__article=sale.article
            )
            previous_annuaire = previous_annuaires[len(previous_annuaires)-1]

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
                            Annuaire.create(sale=sale, user=user)
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
                        previous_annuaire.last = False
                        previous_annuaire.save()
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
