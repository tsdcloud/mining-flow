from rest_framework import serializers
from django.core import signing

from career.models import (
    StockageAera, Carriere,
    StockageAeraLv, CareerLv,
    CareerArticle, Depot,
    StockagePartner, Transfer,
    StockagePartnerArticle, Sale,
    ProductBalance
)

from car.models import (
    Trailer, Tractor
)

from article.models import Article

import datetime

import pytz


class StockageAeraStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add stockage aera """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    village = serializers.SerializerMethodField(read_only=True)
    village_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = StockageAera
        fields = [
            'id',
            'is_active',
            'name',
            'village_id',
            'village'
        ]

    def get_village(self, instance):
        data = StockageAera.get_village(
            village=instance.village,
            authorization=self.context['request'].headers.get('Authorization')
        )
        return data

    def validate_village_id(self, value):
        """ check logical validity of village """
        data = StockageAera.get_village(
            village=value,
            authorization=self.context['request'].headers.get('Authorization')
        )
        if data is None:
            raise serializers.ValidationError(
                detail="village not found"
            )
        return value

    def validate(self, data):
        """ check logical validity of stockageAera """
        try:
            StockageAera.objects.get(
                name=data['name'],
                is_active=True,
                village=data['village']
            )
            raise serializers.ValidationError(
                detail="stockage aera already exists"
            )
        except Exception:
            pass
        return data


class StockagePartnerStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add stockage partner """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    village = serializers.SerializerMethodField(read_only=True)
    village_id = serializers.CharField(write_only=True)
    firm = serializers.SerializerMethodField(read_only=True)
    firm_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = StockagePartner
        fields = [
            'id',
            'is_active',
            'name',
            'village_id',
            'village',
            'firm_id',
            'firm'
        ]

    def get_village(self, instance):
        data = StockagePartner.get_village(
            village=instance.village,
            authorization=self.context['request'].headers.get('Authorization')
        )
        return data

    def get_firm(self, instance):
        data = StockagePartner.get_firm(
            firm=instance.firm,
            authorization=self.context['request'].headers.get('Authorization')
        )
        return data

    def validate_village_id(self, value):
        """ check logical validity of village """
        data = StockagePartner.get_village(
            village=value,
            authorization=self.context['request'].headers.get('Authorization')
        )
        if data is None:
            raise serializers.ValidationError(
                detail="village not found"
            )
        return value

    def validate_firm_id(self, value):
        """ check logical validity of firm """
        data = StockagePartner.get_firm(
            firm=value,
            authorization=self.context['request'].headers.get('Authorization')
        )
        if data is None:
            raise serializers.ValidationError(
                detail="firm not found"
            )
        return value

    def validate(self, data):
        """ check logical validity of stockagePartner """
        try:
            StockagePartner.objects.get(
                name=data['name'].upper(),
                is_active=True,
                village=data['village']
            )
            raise serializers.ValidationError(
                detail="stockage partner already exists"
            )
        except Exception:
            pass
        return data


class CareerStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add career aera """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_suspend = serializers.BooleanField(read_only=True)
    village = serializers.SerializerMethodField(read_only=True)
    village_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = Carriere
        fields = [
            'id',
            'is_active',
            'name',
            'village_id',
            'village',
            'uin',
            'localisation',
            'proprio',
            'is_suspend'
        ]

    def get_village(self, instance):
        data = Carriere.get_village(
            village=instance.village,
            authorization=self.context['request'].headers.get('Authorization')
        )
        return data

    def validate_village_id(self, value):
        """ check logical validity of village """
        data = Carriere.get_village(
            village=value,
            authorization=self.context['request'].headers.get('Authorization')
        )
        if data is None:
            raise serializers.ValidationError(
                detail="village not found"
            )
        return value

    def validate_uin(self, value):
        """ check uin """
        try:
            Carriere.objects.get(uin=value, is_active=True)
            raise serializers.ValidationError(
                detail="uin already exists"
            )
        except Carriere.DoesNotExist:
            pass
        return value

    def validate_name(self, value):
        """ check name """
        try:
            Carriere.objects.get(name=value, is_active=True)
            raise serializers.ValidationError(
                detail="name already exists"
            )
        except Carriere.DoesNotExist:
            pass
        return value


class StockageAeraLvStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add stockageaeralv """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_waiting_approve = serializers.BooleanField(read_only=True)
    stockageaera = serializers.SerializerMethodField(read_only=True)
    stockageaera_id = serializers.CharField(write_only=True)
    available_quantity = serializers.FloatField(read_only=True)
    available_volume = serializers.FloatField(read_only=True)
    last_approve_quantity = serializers.FloatField(read_only=True)
    last_approve_volume = serializers.FloatField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = StockageAeraLv
        fields = [
            'id',
            'is_active',
            'is_waiting_approve',
            'stockageaera',
            'stockageaera_id',
            'available_quantity',
            'available_volume',
            'last_approve_quantity',
            'last_approve_volume',
            'last_demand_quantity',
            'last_demand_volume'
        ]

    def get_stockageaera(self, instance):
        return {
            "id": instance.stockageaera.id,
            "name": instance.stockageaera.name
        }

    def validate_stockageaera_id(self, value):
        """ check logical validity of stockageaera """
        try:
            StockageAera.objects.get(id=value, is_active=True)
        except StockageAera.DoesNotExist:
            raise serializers.ValidationError(
                detail="stockageaera_id not found"
            )
        return value

    def validate_last_demand_quantity(self, value):
        """ check last_demand_quantity """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_demand_quantity"
            )
        return value

    def validate_last_demand_volume(self, value):
        """ check last_demand_volume """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_demand_volume"
            )
        return value


class StockageAeraLvApproveSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for approve stockageaeralv """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_waiting_approve = serializers.BooleanField(read_only=True)
    stockageaera = serializers.SerializerMethodField(read_only=True)
    available_quantity = serializers.FloatField(read_only=True)
    available_volume = serializers.FloatField(read_only=True)
    last_demand_quantity = serializers.FloatField(read_only=True)
    last_demand_volume = serializers.FloatField(read_only=True)
    last_approve_quantity = serializers.IntegerField(required=True)
    last_approve_volume = serializers.FloatField(required=True)

    class Meta:
        """ attributs serialized """
        model = StockageAeraLv
        fields = [
            'id',
            'is_active',
            'is_waiting_approve',
            'stockageaera',
            'available_quantity',
            'available_volume',
            'last_approve_quantity',
            'last_approve_volume',
            'last_demand_quantity',
            'last_demand_volume'
        ]

    def get_stockageaera(self, instance):
        return {
            "id": instance.stockageaera.id,
            "name": instance.stockageaera.name
        }

    def validate_last_approve_quantity(self, value):
        """ check last_approve_quantity """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_approve_quantity"
            )
        stockage_aera_lv = self.context['stockage_aera_lv']
        if value > stockage_aera_lv.last_demand_quantity:
            raise serializers.ValidationError(
                detail="last_approve_quantity is too long"
            )
        return value

    def validate_last_approve_volume(self, value):
        """ check last_approve_volume """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_approve_volume"
            )
        stockage_aera_lv = self.context['stockage_aera_lv']
        if value > stockage_aera_lv.last_demand_volume:
            raise serializers.ValidationError(
                detail="last_approve_volume is too long"
            )
        return value

    def validate(self, data):
        """ check stockage_aera_lvt """
        stockage_aera_lv = self.context['stockage_aera_lv']
        if stockage_aera_lv.is_waiting_approve is False:
            raise serializers.ValidationError(
                detail=" demand is already approved "
            )
        return data


class CareerLvStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add careerlv """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_waiting_approve = serializers.BooleanField(read_only=True)
    career = serializers.SerializerMethodField(read_only=True)
    career_id = serializers.CharField(write_only=True)
    available_quantity = serializers.FloatField(read_only=True)
    available_volume = serializers.FloatField(read_only=True)
    last_approve_quantity = serializers.FloatField(read_only=True)
    last_approve_volume = serializers.FloatField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = CareerLv
        fields = [
            'id',
            'is_active',
            'is_waiting_approve',
            'career',
            'career_id',
            'available_quantity',
            'available_volume',
            'last_approve_quantity',
            'last_approve_volume',
            'last_demand_quantity',
            'last_demand_volume'
        ]

    def get_career(self, instance):
        return {
            "id": instance.career.id,
            "name": instance.career.name
        }

    def validate_career_id(self, value):
        """ check logical validity of career """
        try:
            Carriere.objects.get(id=value, is_active=True)
        except CareerLv.DoesNotExist:
            raise serializers.ValidationError(
                detail="career_id not found"
            )
        return value

    def validate_last_demand_quantity(self, value):
        """ check last_demand_quantity """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_demand_quantity"
            )
        return value

    def validate_last_demand_volume(self, value):
        """ check last_demand_volume """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_demand_volume"
            )
        return value


class CareerLvApproveSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for approve stockageaeralv """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_waiting_approve = serializers.BooleanField(read_only=True)
    career = serializers.SerializerMethodField(read_only=True)
    available_quantity = serializers.FloatField(read_only=True)
    available_volume = serializers.FloatField(read_only=True)
    last_demand_quantity = serializers.FloatField(read_only=True)
    last_demand_volume = serializers.FloatField(read_only=True)
    last_approve_quantity = serializers.IntegerField(required=True)
    last_approve_volume = serializers.FloatField(required=True)

    class Meta:
        """ attributs serialized """
        model = CareerLv
        fields = [
            'id',
            'is_active',
            'is_waiting_approve',
            'career',
            'available_quantity',
            'available_volume',
            'last_approve_quantity',
            'last_approve_volume',
            'last_demand_quantity',
            'last_demand_volume'
        ]

    def get_career(self, instance):
        return {
            "id": instance.career.id,
            "name": instance.career.name
        }

    def validate_last_approve_quantity(self, value):
        """ check last_approve_quantity """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_approve_quantity"
            )
        career_lv = self.context['career_lv']
        if value > career_lv.last_demand_quantity:
            raise serializers.ValidationError(
                detail="last_approve_quantity is too long"
            )
        return value

    def validate_last_approve_volume(self, value):
        """ check last_approve_volume """
        if 1 > value:
            raise serializers.ValidationError(
                detail=" bad last_approve_volume"
            )
        career_lv = self.context['career_lv']
        if value > career_lv.last_demand_volume:
            raise serializers.ValidationError(
                detail="last_approve_volume is too long"
            )
        return value

    def validate(self, data):
        """ check stockage_aera_lvt """
        career_lv = self.context['career_lv']
        if career_lv.is_waiting_approve is False:
            raise serializers.ValidationError(
                detail=" demand is already approved "
            )
        return data


class CareerArticleStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add careerarticle """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    career = serializers.SerializerMethodField(read_only=True)
    career_id = serializers.CharField(write_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    article_id = serializers.CharField(write_only=True)
    stockage = serializers.SerializerMethodField(read_only=True)
    stockage_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = CareerArticle
        fields = [
            'id',
            'is_active',
            'career',
            'career_id',
            'article',
            'article_id',
            'stockage',
            'stockage_id',
            'price_sale',
            'price_car'
        ]

    def get_career(self, instance):
        return {
            "id": instance.career.id,
            "name": instance.career.name,
            "village": Carriere.get_village(
                village=instance.career.village,
                authorization=self.context['request'].headers.get('Authorization')
            )
        }

    def get_article(self, instance):
        return {
            "id": instance.article.id,
            "name": instance.article.name
        }

    def get_stockage(self, instance):
        return {
            "id": instance.stockage_aera.id,
            "name": instance.stockage_aera.name
        }

    def validate_career_id(self, value):
        """ check logical validity of career """
        try:
            Carriere.objects.get(id=value, is_active=True)
        except Carriere.DoesNotExist:
            raise serializers.ValidationError(
                detail="career_id not found"
            )
        return value

    def validate_article_id(self, value):
        """ check logical validity of article_id """
        try:
            Article.objects.get(id=value, is_active=True)
        except Article.DoesNotExist:
            raise serializers.ValidationError(
                detail="article_id not found"
            )
        return value

    def validate_stockage_id(self, value):
        """ check logical validity of article_id """
        try:
            StockageAera.objects.get(id=value, is_active=True)
        except StockageAera.DoesNotExist:
            raise serializers.ValidationError(
                detail="stockage_id not found"
            )
        return value

    def validate_price_sale(self, value):
        if 0 > value:
            raise serializers.ValidationError(
                detail='invalide price_sale'
            )
        return value

    def validate_price_car(self, value):
        if 0 > value:
            raise serializers.ValidationError(
                detail='invalide price_car'
            )
        return value


class DepotVenteArticleStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add depotventearticle """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    stockage_partner = serializers.SerializerMethodField(read_only=True)
    stockage_partner_id = serializers.CharField(write_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    article_id = serializers.CharField(write_only=True)
    stockage = serializers.SerializerMethodField(read_only=True)
    stockage_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = StockagePartnerArticle
        fields = [
            'id',
            'is_active',
            'stockage_partner',
            'stockage_partner_id',
            'article',
            'article_id',
            'stockage',
            'stockage_id',
            'price_sale',
            'price_car'
        ]

    def get_stockage_partner(self, instance):
        return {
            "id": instance.stockage_partner.id,
            "name": instance.stockage_partner.name,
            "village": Carriere.get_village(
                village=instance.stockage_partner.village,
                authorization=self.context['request'].headers.get('Authorization')
            )
        }

    def get_article(self, instance):
        return {
            "id": instance.article.id,
            "name": instance.article.name
        }

    def get_stockage(self, instance):
        return {
            "id": instance.stockage_aera.id,
            "name": instance.stockage_aera.name
        }

    def validate_stockage_partner_id(self, value):
        """ check logical validity of stockage_partner_id """
        try:
            StockagePartner.objects.get(id=value, is_active=True)
        except StockagePartner.DoesNotExist:
            raise serializers.ValidationError(
                detail="stockage_partner_id not found"
            )
        return value

    def validate_article_id(self, value):
        """ check logical validity of article_id """
        try:
            Article.objects.get(id=value, is_active=True)
        except Article.DoesNotExist:
            raise serializers.ValidationError(
                detail="article_id not found"
            )
        return value

    def validate_stockage_id(self, value):
        """ check logical validity of article_id """
        try:
            StockageAera.objects.get(id=value, is_active=True)
        except StockageAera.DoesNotExist:
            raise serializers.ValidationError(
                detail="stockage_id not found"
            )
        return value

    def validate_price_sale(self, value):
        if 0 > value:
            raise serializers.ValidationError(
                detail='invalide price_sale'
            )
        return value

    def validate_price_car(self, value):
        if 0 > value:
            raise serializers.ValidationError(
                detail='invalide price_car'
            )
        return value


class DepotStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add depot """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    career_id = serializers.CharField(write_only=True)
    career = serializers.SerializerMethodField(read_only=True)
    numero = serializers.CharField(required=True)
    leader = serializers.CharField(required=True)

    class Meta:
        """ attributs serialized """
        model = Depot
        fields = [
            'id',
            'is_active',
            'career_id',
            'career',
            'numero',
            'leader'
        ]

    def get_career(self, instance):
        return {
            "name": instance.career.name,
            "id": instance.career.id,
            "proprio": instance.career.proprio
        }

    def validate_career_id(self, value):
        """ check logical validity of career """
        try:
            Carriere.objects.get(
                id=value,
                is_active=True
            )
        except Carriere.DoesNotExist:
            raise serializers.ValidationError(
                detail='career not found'
            )
        return value

    def validate(self, data):
        career = Carriere.readByToken(
            token=data['career_id']
        )
        try:
            Depot.objects.get(
                is_active=True,
                numero=data['numero'],
                career=career
            )
            raise serializers.ValidationError(
                detail='numero already exists'
            )
        except Depot.DoesNotExist:
            return data


class TransferStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add transfer """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    tractor_id = serializers.CharField(write_only=True)
    tractor = serializers.SerializerMethodField(read_only=True)
    trailer_id = serializers.CharField(write_only=True, required=False)
    trailer = serializers.SerializerMethodField(read_only=True)
    depot_id = serializers.CharField(write_only=True)
    depot = serializers.SerializerMethodField(read_only=True)
    career_id = serializers.CharField(write_only=True)
    career = serializers.SerializerMethodField(read_only=True)
    stockageaera_id = serializers.CharField(write_only=True)
    stockageaera = serializers.SerializerMethodField(read_only=True)
    transfer_slip = serializers.CharField(required=True)
    physical_waybill = serializers.CharField(required=True)
    driver = serializers.CharField(required=True)
    status = serializers.CharField(read_only=True)
    article_id = serializers.CharField(write_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_price = serializers.CharField(read_only=True)
    transport_price = serializers.CharField(read_only=True)
    volume_receptionned = serializers.FloatField(read_only=True)
    volume_transferred = serializers.FloatField(required=True)
    date_recep = serializers.CharField(read_only=True)
    date_op = serializers.CharField(required=True)

    class Meta:
        """ attributs serialized """
        model = Transfer
        fields = [
            'id',
            'is_active',
            'tractor_id',
            'tractor',
            'trailer_id',
            'trailer',
            'depot_id',
            'depot',
            'career_id',
            'career',
            'stockageaera_id',
            'stockageaera',
            'transfer_slip',
            'physical_waybill',
            'driver',
            'status',
            'article_id',
            'article',
            'product_name',
            'product_price',
            'transport_price',
            'volume_receptionned',
            'volume_transferred',
            'date_recep',
            'date_op'
        ]

    def get_tractor(self, instance):
        return {
            "registration": instance.tractor.registration,
            "id": instance.tractor.id,
            "serial_number": instance.tractor.serial_number,
            "is_used": instance.tractor.is_used
        }

    def get_trailer(self, instance):
        return {
            "registration": instance.trailer.registration,
            "id": instance.trailer.id,
            "serial_number": instance.trailer.serial_number,
            "is_used": instance.trailer.is_used,
            "empty_volume": instance.trailer.empty_volume
        }

    def get_depot(self, instance):
        return {
            "numero": instance.depot.numero,
            "id": instance.depot.id,
            "leader": instance.depot.leader
        }

    def get_career(self, instance):
        return {
            "name": instance.career.name,
            "id": instance.career.id,
            "uin": instance.career.uin,
            "proprio": instance.career.proprio,
            "is_suspend": instance.career.is_suspend
        }

    def get_stockageaera(self, instance):
        return {
            "name": instance.stockage_aera.name,
            "id": instance.stockage_aera.id,
            "village": instance.stockage_aera.village
        }

    def get_article(self, instance):
        return {
            "name": instance.article.name,
            "id": instance.article.id,
            "categorie": {
                "id": instance.article.categorie.id,
                "name": instance.article.categorie.name
            }
        }

    def validate_tractor_id(self, value):
        """ check logical validity of tractor """
        try:
            tractor = Tractor.objects.get(
                id=value,
                is_active=True,
            )
            if tractor.is_used is True:
                raise serializers.ValidationError(
                    detail='tractor is not available'
                )
        except Tractor.DoesNotExist:
            raise serializers.ValidationError(
                detail='tractor not found'
            )
        return value

    def validate_trailer_id(self, value):
        """ check logical validity of trailer """
        try:
            trailer = Trailer.objects.get(
                id=value,
                is_active=True,
            )
            if trailer.is_used is True:
                raise serializers.ValidationError(
                    detail='trailer is not available'
                )
        except Tractor.DoesNotExist:
            raise serializers.ValidationError(
                detail='trailer not found'
            )
        return value

    def validate_depot_id(self, value):
        """ check logical validity of depot """
        try:
            Depot.objects.get(
                id=value,
                is_active=True,
            )
        except Depot.DoesNotExist:
            raise serializers.ValidationError(
                detail='depot not found'
            )
        return value

    def validate_career_id(self, value):
        """ check logical validity of career """
        try:
            career = Carriere.objects.get(
                id=value,
                is_active=True,
            )
            if career.is_suspend is True:
                raise serializers.ValidationError(
                    detail='the career is suspend'
                )
        except Carriere.DoesNotExist:
            raise serializers.ValidationError(
                detail='career not found'
            )
        return value

    def validate_stockageaera_id(self, value):
        """ check logical validity of stockage aera """
        try:
            StockageAera.objects.get(
                id=value,
                is_active=True,
            )
        except StockageAera.DoesNotExist:
            raise serializers.ValidationError(
                detail='stockage aera not found'
            )
        return value

    def validate_transfer_slip(self, value):
        """ check logical validity of transfer slip """
        try:
            Transfer.objects.get(
                transfer_slip=value,
            )
            raise serializers.ValidationError(
                detail='transfer slip already exists'
            )
        except Transfer.DoesNotExist:
            return value

    def validate_physical_waybill(self, value):
        """ check logical validity of physical waybill """
        try:
            Transfer.objects.get(
                physical_waybill=value,
            )
            raise serializers.ValidationError(
                detail='physical waybill already exists'
            )
        except Transfer.DoesNotExist:
            return value

    def validate_article_id(self, value):
        """ check logical validity of article """
        try:
            Article.objects.get(
                id=value,
                is_active=True,
            )
        except Article.DoesNotExist:
            raise serializers.ValidationError(
                detail='article not found'
            )
        return value

    def validate_volume_transferred(self, value):
        """ check logical validity of volume_transferred """
        if 1 > value:
            raise serializers.ValidationError(
                detail='volume transfered is small'
            )
        return value

    def validate_date_op(self, value):
        """ check logical validity of date_op """
        try:
            date_op = datetime.datetime.strptime(value, '%d-%m-%Y %H:%M')
            utc = pytz.UTC
            current_date = datetime.datetime.now()
            date_op = date_op.replace(tzinfo=utc)
            current_date = current_date.replace(tzinfo=utc)
            if date_op > current_date:
                raise serializers.ValidationError(
                    detail='check the date of operation'
                )
        except ValueError:
            raise serializers.ValidationError(
                detail="not valid date format"
            )
        return value

    def validate(self, data):
        depot = Depot.objects.get(id=data['depot_id'])
        career = Carriere.objects.get(id=data['career_id'])
        article = Article.objects.get(id=data['article_id'])
        stockage_aera = StockageAera.objects.get(id=data['stockageaera_id'])
        try:
            CareerArticle.objects.get(
                career=career,
                article=article,
                stockage_aera=stockage_aera,
                is_active=True
            )
        except CareerArticle.DoesNotExist:
            raise serializers.ValidationError(
                detail='career article stockage aera unauthorized'
            )

        try:
            lv = CareerLv.objects.get(career=career)
            if 1 > lv.available_quantity:
                raise serializers.ValidationError(
                    detail='career has not a lv'
                )
            if data['volume_transferred'] > lv.available_volume:
                raise serializers.ValidationError(
                    detail='career has not lv availlable for this volume'
                )
        except CareerLv.DoesNotExist:
            raise serializers.ValidationError(
                detail='career has not available lv'
            )

        if depot.career != career:
            raise serializers.ValidationError(
                detail='depot unauthorized'
            )
        return data


class ReceiveTransferSerializer(serializers.HyperlinkedModelSerializer):
    date_recep = serializers.CharField(required=True)
    volume_receptionned = serializers.FloatField(required=True)

    class Meta:
        """ attributs serialized """
        model = Transfer
        fields = [
            'date_recep',
            'volume_receptionned'
        ]

    def validate_volume_receptionned(self, value):
        """ check logical validity of volume_transferred """
        transfer = self.context['transfer']
        if 0 > value:
            raise serializers.ValidationError(
                detail='volume receptionned is small'
            )
        elif value > transfer.volume_transferred:
            raise serializers.ValidationError(
                detail='volume receptionned is long'
            )
        else:
            return value

    def validate_date_recep(self, value):
        """ check logical validity of date_recep """
        try:
            date_recep = datetime.datetime.strptime(value, '%d-%m-%Y %H:%M')
            utc = pytz.UTC
            current_date = datetime.datetime.now()
            date_recep = date_recep.replace(tzinfo=utc)
            current_date = current_date.replace(tzinfo=utc)
            if date_recep > current_date:
                raise serializers.ValidationError(
                    detail='check the date of operation'
                )
            transfer = self.context['transfer']
            date_op = transfer.date_op.replace(tzinfo=utc)
            if date_op > date_recep:
                raise serializers.ValidationError(
                    detail='check the reception date'
                )
        except ValueError:
            raise serializers.ValidationError(
                detail="not valid date format"
            )
        return value

    def validate(self, data):
        """ check logical validity of transfer """
        transfer = self.context['transfer']
        if transfer.status != 1:
            raise serializers.ValidationError(
                detail='transfer is not pending'
            )
        return data


class ReceiveTransferVenteSerializer(serializers.HyperlinkedModelSerializer):
    date_recep = serializers.CharField(required=True)
    volume_receptionned = serializers.FloatField(required=True)
    stockage_partner_id = serializers.CharField(write_only=True, required=True)
    stockage_partner = serializers.SerializerMethodField(read_only=True)
    destination = serializers.CharField(required=True)
    sale_unit_price = serializers.IntegerField()

    class Meta:
        """ attributs serialized """
        model = Transfer
        fields = [
            'date_recep',
            'volume_receptionned',
            'stockage_partner_id',
            'stockage_partner',
            'destination',
            'sale_unit_price'
        ]

    def get_stockage_partner(self, instance):
        sale = Sale.objects.get(
            sale_slip=instance.transfer_slip
        )
        if sale.type_sale == 1:
            return {
                "id": sale.stockage_partner.id,
                "name": sale.stockage_partner.name
            }
        else:
            return {
                "id": "",
                "name": ""
            }

    def validate_volume_receptionned(self, value):
        """ check logical validity of volume_transferred """
        transfer = self.context['transfer']
        if 0 > value:
            raise serializers.ValidationError(
                detail='volume receptionned is small'
            )
        elif value > transfer.volume_transferred:
            raise serializers.ValidationError(
                detail='volume receptionned is long'
            )
        else:
            return value

    def validate_date_recep(self, value):
        """ check logical validity of date_recep """
        try:
            date_recep = datetime.datetime.strptime(value, '%d-%m-%Y %H:%M')
            utc = pytz.UTC
            current_date = datetime.datetime.now()
            date_recep = date_recep.replace(tzinfo=utc)
            current_date = current_date.replace(tzinfo=utc)
            if date_recep > current_date:
                raise serializers.ValidationError(
                    detail='check the date of operation'
                )
            transfer = self.context['transfer']
            date_op = transfer.date_op.replace(tzinfo=utc)
            if date_op > date_recep:
                raise serializers.ValidationError(
                    detail='check the reception date'
                )
        except ValueError:
            raise serializers.ValidationError(
                detail="not valid date format"
            )
        return value

    def validate_stockage_partner_id(self, value):
        """ check validity of stockage partner """
        if value != "Autre":
            try:
                stockage_partner = StockagePartner.objects.get(
                    id=value,
                    is_active=True
                )
                transfer = self.context['transfer']
                try:
                    StockagePartnerArticle.objects.get(
                        stockage_partner=stockage_partner,
                        article=transfer.article,
                        stockage_aera=transfer.stockage_aera
                    )
                except StockagePartnerArticle.DoesNotExist:
                    raise serializers.ValidationError(
                        detail='this sales depot is not configured to sell this type of product to this mining hub'
                    )
            except StockagePartner.DoesNotExist:
                raise serializers.ValidationError(
                    detail='stockage partner id not found'
                )
        return value

    def validate_sale_unit_price(self, value):
        if value < 1:
            raise serializers.ValidationError(
                detail='sale unit price is not valid'
            )
        return value

    def validate(self, data):
        """ check logical validity of transfer """
        transfer = self.context['transfer']
        if transfer.status != 1:
            raise serializers.ValidationError(
                detail='transfer is not pending'
            )
        return data


class SaleStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add sale """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    sale_slip = serializers.CharField()
    waybill = serializers.CharField(read_only=True)
    stockage_aera = serializers.SerializerMethodField(read_only=True)
    stockage_aera_id = serializers.CharField(write_only=True)
    stockage_partner = serializers.SerializerMethodField(read_only=True)
    stockage_partner_id = serializers.CharField(write_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    article_id = serializers.CharField(write_only=True)
    destination = serializers.CharField(required=True)
    product_name = serializers.CharField(read_only=True)
    product_price = serializers.IntegerField(read_only=True)
    sale_unit_price = serializers.IntegerField(required=True)
    driver = serializers.CharField(required=True)
    tractor_id = serializers.CharField(write_only=True)
    tractor = serializers.SerializerMethodField(read_only=True)
    trailer_id = serializers.CharField(write_only=True, required=True)
    trailer = serializers.SerializerMethodField(read_only=True)
    volume = serializers.FloatField(required=True)
    volume_r = serializers.CharField(read_only=True)
    status = serializers.IntegerField(read_only=True)
    type_sale = serializers.IntegerField(read_only=True)
    date_op = serializers.CharField(required=True)
    date_recep = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Sale
        fields = [
            'id',
            'is_active',
            'sale_slip',
            'waybill',
            'stockage_aera',
            'stockage_aera_id',
            'stockage_partner',
            'stockage_partner_id',
            'article',
            'article_id',
            'destination',
            'product_name',
            'product_price',
            'sale_unit_price',
            'driver',
            'tractor_id',
            'tractor',
            'trailer_id',
            'trailer',
            'volume',
            'status',
            'type_sale',
            'date_op',
            'date_recep',
            'volume_r'
        ]

    def get_stockage_aera(self, instance):
        if instance.type_sale == 3:
            return {}
        request = self.context['request']
        product_balance = ProductBalance.readBalanceAireStockage(
            stockage_aera=instance.stockage_aera,
            article=instance.article,
            user=request.infoUser.get('id')
        )
        data = {
            "id": instance.stockage_aera.id,
            "name": instance.stockage_aera.name,
            "solde": product_balance.balance
        }
        return data

    def get_stockage_partner(self, instance):
        if instance.type_sale == 2:
            return {}
        request = self.context['request']
        product_balance = ProductBalance.readBalanceAirePartner(
            article=instance.article,
            stockage_partner=instance.stockage_partner,
            user=request.infoUser.get('id')
        )
        data = {
            "id": instance.stockage_partner.id,
            "name": instance.stockage_partner.name,
            "solde": product_balance.balance
        }
        return data

    def get_article(self, instance):
        return {
            "name": instance.article.name,
            "id": instance.article.id,
            "categorie": {
                "id": instance.article.categorie.id,
                "name": instance.article.categorie.name
            }
        }

    def get_tractor(self, instance):
        return {
            "registration": instance.tractor.registration,
            "id": instance.tractor.id,
            "serial_number": instance.tractor.serial_number,
            "is_used": instance.tractor.is_used
        }

    def get_trailer(self, instance):
        return {
            "registration": instance.trailer.registration,
            "id": instance.trailer.id,
            "serial_number": instance.trailer.serial_number,
            "is_used": instance.trailer.is_used,
            "empty_volume": instance.trailer.empty_volume
        }

    def validate_sale_slip(self, value):
        """ check logical validity of sale slip """
        try:
            Sale.objects.get(
                is_active=True,
                sale_slip=value
            )
            raise serializers.ValidationError(
                detail=('sale_slip already exists')
            )
        except Sale.DoesNotExist:
            return value

    def validate_stockage_aera_id(self, value):
        """ check stockage_aera_id """
        if value != 'Autre':
            try:
                StockageAera.objects.get(
                    id=value, is_active=True
                )
            except StockageAera.DoesNotExist:
                raise serializers.ValidationError(
                    detail="stockage aera not found"
                )
        return value

    def validate_stockage_partner_id(self, value):
        """ check stockage_partner_id """
        if value != 'Autre':
            try:
                StockagePartner.objects.get(
                    id=value, is_active=True
                )
            except StockagePartner.DoesNotExist:
                raise serializers.ValidationError(
                    detail="Sale depot not found"
                )
        return value

    def validate_article_id(self, value):
        """ check logical validity of article """
        try:
            Article.objects.get(
                id=value,
                is_active=True,
            )
        except Article.DoesNotExist:
            raise serializers.ValidationError(
                detail='article not found'
            )
        return value

    def validate_sale_unit_price(self, value):
        if value < 1:
            raise serializers.ValidationError(
                detail='sale unit price is not valid'
            )
        return value

    def validate_tractor_id(self, value):
        """ check logical validity of tractor """
        try:
            tractor = Tractor.objects.get(
                id=value,
                is_active=True,
            )
            if tractor.is_used is True:
                raise serializers.ValidationError(
                    detail='tractor is not available'
                )
        except Tractor.DoesNotExist:
            raise serializers.ValidationError(
                detail='tractor not found'
            )
        return value

    def validate_trailer_id(self, value):
        """ check logical validity of trailer """
        try:
            trailer = Trailer.objects.get(
                id=value,
                is_active=True,
            )
            if trailer.is_used is True:
                raise serializers.ValidationError(
                    detail='trailer is not available'
                )
        except Tractor.DoesNotExist:
            raise serializers.ValidationError(
                detail='trailer not found'
            )
        return value

    def validate_volume(self, value):
        """ check logical validity volume """
        if 0 > value:
            raise serializers.ValidationError(
                detail='volume is too small'
            )
        return value

    def validate_date_recep(self, value):
        """ check logical validity of date_op """
        try:
            date_op = datetime.datetime.strptime(value, '%d-%m-%Y %H:%M')
            utc = pytz.UTC
            current_date = datetime.datetime.now()
            date_op = date_op.replace(tzinfo=utc)
            current_date = current_date.replace(tzinfo=utc)
            if date_op > current_date:
                raise serializers.ValidationError(
                    detail='check the date of operation'
                )
        except ValueError:
            raise serializers.ValidationError(
                detail="not valid date format"
            )
        return value

    def validate(self, data):
        """ check logical validity of transfer """
        article = Article.readByToken(
            token=data['article_id']
        )
        request = self.context['request']
        if data['stockage_aera_id'] != 'Autre':
            stockage_aera = StockageAera.objects.get(
                id=data['stockage_aera_id']
            )
            product_balance = ProductBalance.readBalanceAireStockage(
                article=article,
                stockage_aera=stockage_aera,
                user=request.infoUser.get('id')
            )
            try:
                lv = StockageAeraLv.objects.get(
                    stockageaera=stockage_aera
                )
                if 1 > lv.available_quantity:
                    raise serializers.ValidationError(
                        detail='Hub minier has not available lv'
                    )
                if data['volume'] > lv.available_volume:
                    raise serializers.ValidationError(
                        detail='Hub minier has not this volume in available lv'
                    )
            except StockageAeraLv.DoesNotExist:
                raise serializers.ValidationError(
                    detail='lv Hub minier not found'
                )
            if data['stockage_partner_id'] != 'Autre':
                stockage_partner = StockagePartner.objects.get(
                    id=data['stockage_partner_id']
                )
                try:
                    StockagePartnerArticle.objects.get(
                        article=article,
                        stockage_partner=stockage_partner,
                        stockage_aera=stockage_aera
                    )
                except StockagePartnerArticle.DoesNotExist:
                    raise serializers.ValidationError(
                        detail='Hub minier, Sale depot and article is not configure'
                    )
        else:
            try:
                stockage_partner = StockagePartner.objects.get(
                    id=data['stockage_partner_id']
                )
            except StockagePartner.DoesNotExist:
                raise serializers.ValidationError(
                    detail='stockage_partner not found'
                )
            product_balance = ProductBalance.readBalanceAirePartner(
                article=article,
                stockage_partner=stockage_partner,
                user=request.infoUser.get('id')
            )

        volume = data['volume']

        if volume > product_balance.balance:
            raise serializers.ValidationError(
                detail='insufficient available volume ' + str(
                    product_balance.balance
                )
            )
        return data


class ReceiveVenteSerializer(serializers.HyperlinkedModelSerializer):
    date_recep = serializers.CharField(required=True)
    volume_receptionned = serializers.FloatField(required=True)

    class Meta:
        """ attributs serialized """
        model = Transfer
        fields = [
            'date_recep',
            'volume_receptionned'
        ]

    def validate_volume_receptionned(self, value):
        """ check logical validity of volume_transferred """
        sale = self.context['sale']
        if 0 > value:
            raise serializers.ValidationError(
                detail='volume receptionned is small'
            )
        elif value > sale.volume:
            raise serializers.ValidationError(
                detail='volume receptionned is long'
            )
        else:
            return value

    def validate_date_recep(self, value):
        """ check logical validity of date_recep """
        try:
            date_recep = datetime.datetime.strptime(value, '%d-%m-%Y %H:%M')
            utc = pytz.UTC
            current_date = datetime.datetime.now()
            date_recep = date_recep.replace(tzinfo=utc)
            current_date = current_date.replace(tzinfo=utc)
            if date_recep > current_date:
                raise serializers.ValidationError(
                    detail='check the date of operation'
                )
            sale = self.context['sale']
            date_op = sale.date_op.replace(tzinfo=utc)
            if date_op > date_recep:
                raise serializers.ValidationError(
                    detail='check the reception date'
                )
        except ValueError:
            raise serializers.ValidationError(
                detail="not valid date format"
            )
        return value

    def validate(self, data):
        """ check logical validity of transfer """
        sale = self.context['sale']
        if sale.status != 1:
            raise serializers.ValidationError(
                detail='sale is not pending'
            )
        return data
