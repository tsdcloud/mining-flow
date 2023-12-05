from django.shortcuts import get_object_or_404
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from career.serializers import (
    StockageAeraStoreSerializer,
    CareerStoreSerializer,
    StockageAeraLvStoreSerializer,
    StockageAeraLvApproveSerializer,
    CareerLvStoreSerializer,
    CareerArticleStoreSerializer,
    CareerLvApproveSerializer,
    DepotStoreSerializer,
    StockagePartnerStoreSerializer,
    TransferStoreSerializer,
    ReceiveTransferSerializer,
    DepotVenteArticleStoreSerializer,
    ReceiveTransferVenteSerializer,
    SaleStoreSerializer,
    ReceiveVenteSerializer
)
from career.models import (
    StockageAera,
    Carriere,
    StockageAeraLv,
    CareerLv,
    CareerArticle,
    Depot,
    StockagePartner,
    Transfer,
    Tractor,
    Trailer,
    StockagePartnerArticle,
    Sale
)
from article.models import Article

from common.permissions import IsDeactivate
from . permissions import (
    IsAddStockageAera,
    IsViewAllStockageAera,
    IsAddCareer,
    IsViewAllCareer,
    IsApproveCareerLv,
    IsAddStockageAeraLv,
    IsViewAllStockageAeraLv,
    IsApproveStockageAeraLv,
    IsAddCareerLv,
    IsViewAllCareerLv,
    IsAddCareerArticle,
    IsViewAllCareerArticle,
    IsAddDepot,
    IsViewAllDepot,
    IsAddHubPartner,
    IsViewAllHubPartner,
    IsAddTransfer,
    IsViewAllTransfer,
    IsReceiveTransfer,
    IsAddStockagePartnerArticle,
    IsViewAllStockagePartnerArticle,
    IsReceiveSaleTransfer,
    IsAddSale,
    IsViewAllSale,
    IsReceiveSale
)

import http.client
import json
from article.models import Categorie
from article.serializers import ArticleStoreSerializer


class StockageAeraViewSet(viewsets.ModelViewSet):
    """ stockage aera controller """

    def get_serializer_class(self):
        """ define serializer """
        return StockageAeraStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddStockageAera]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllStockageAera]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = StockageAera.objects.all()
        else:
            queryset = StockageAera.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add stockage aera """
        serializer = StockageAeraStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    stockageaera = StockageAera.create(
                        name=serializer.validated_data['name'],
                        village=serializer.validated_data['village_id'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                stockageaera = None

            return Response(
                StockageAeraStoreSerializer(
                    stockageaera,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CareerViewSet(viewsets.ModelViewSet):
    """ career aera controller """

    def get_serializer_class(self):
        """ define serializer """
        return CareerStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddCareer]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllCareer]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Carriere.objects.all()
        else:
            queryset = Carriere.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add career """
        serializer = CareerStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    career = Carriere.create(
                        name=serializer.validated_data['name'],
                        village=serializer.validated_data['village_id'],
                        uin=serializer.validated_data['uin'],
                        localisation=serializer.validated_data['localisation'],
                        proprio=serializer.validated_data['proprio'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                career = None

            return Response(
                CareerStoreSerializer(
                    career,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class StockageAeraLvViewSet(viewsets.ModelViewSet):
    """ stockage aera lv controller """

    def get_serializer_class(self):
        """ define serializer """
        return StockageAeraLvStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddStockageAeraLv]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllStockageAeraLv]
        elif self.action == 'approve':
            self.permission_classes = [IsApproveStockageAeraLv]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = StockageAeraLv.objects.all()
        else:
            queryset = StockageAeraLv.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add stockageaeralv """
        serializer = StockageAeraLvStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    stockageaeralv = StockageAeraLv.create(
                        quantity=serializer.validated_data[
                            'last_demand_quantity'],
                        stockageaera=StockageAera.readByToken(
                            token=serializer.validated_data['stockageaera_id']
                        ),
                        volume=serializer.validated_data['last_demand_volume'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                stockageaeralv = None

            return Response(
                StockageAeraLvStoreSerializer(
                    stockageaeralv,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        """ approve demand stockage lv """
        stockage_aera_lv = self.get_object()
        serializer = StockageAeraLvApproveSerializer(
            data=request.data,
            context={
                "request": request,
                "stockage_aera_lv": stockage_aera_lv
            }
        )
        if serializer.is_valid():
            stockage_aera_lv.change(
                quantity=serializer.validated_data['last_approve_quantity'],
                volume=serializer.validated_data["last_approve_volume"],
                user=self.request.infoUser["id"]
            )
            return Response(
                StockageAeraLvApproveSerializer(
                    stockage_aera_lv,
                    context={
                        "request": request,
                        "stockage_aera_lv": stockage_aera_lv
                    },
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CareerLvViewSet(viewsets.ModelViewSet):
    """ career lv controller """

    def get_serializer_class(self):
        """ define serializer """
        return CareerLvStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddCareerLv]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllCareerLv]
        elif self.action == 'approve':
            self.permission_classes = [IsApproveCareerLv]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = CareerLv.objects.all()
        else:
            queryset = CareerLv.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add career lv """
        serializer = CareerLvStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    careerlv = CareerLv.create(
                        quantity=serializer.validated_data[
                            'last_demand_quantity'],
                        career=Carriere.readByToken(
                            token=serializer.validated_data['career_id']
                        ),
                        volume=serializer.validated_data['last_demand_volume'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                careerlv = None

            return Response(
                CareerLvStoreSerializer(
                    careerlv,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        """ approve demand career lv """
        career_lv = self.get_object()
        serializer = CareerLvApproveSerializer(
            data=request.data,
            context={
                "request": request,
                "career_lv": career_lv
            }
        )
        if serializer.is_valid():
            career_lv.change(
                quantity=serializer.validated_data['last_approve_quantity'],
                volume=serializer.validated_data["last_approve_volume"],
                user=self.request.infoUser["id"]
            )
            return Response(
                CareerLvApproveSerializer(
                    career_lv,
                    context={
                        "request": request,
                        "career_lv": career_lv
                    },
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CareerArticleViewSet(viewsets.ModelViewSet):
    """ career article controller """

    def get_serializer_class(self):
        """ define serializer """
        return CareerArticleStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddCareerArticle]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllCareerArticle]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = CareerArticle.objects.all()
        else:
            queryset = CareerArticle.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add career article """
        serializer = CareerArticleStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    careerarticle = CareerArticle.create(
                        article=Article.readByToken(token=serializer.validated_data['article_id']),
                        career=Carriere.readByToken(token=serializer.validated_data['career_id']),
                        price_car=serializer.validated_data['price_car'],
                        price_sale=serializer.validated_data['price_sale'],
                        stockage_aera=StockageAera.readByToken(token=serializer.validated_data['stockage_id']),
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                careerarticle = None

            return Response(
                CareerArticleStoreSerializer(
                    careerarticle,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class DepotViewSet(viewsets.ModelViewSet):
    """ depot controller """

    def get_serializer_class(self):
        """ define serializer """
        return DepotStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddDepot]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllDepot]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Depot.objects.all()
        else:
            queryset = Depot.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add depot """
        serializer = DepotStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    depot = Depot.create(
                        career=Carriere.readByToken(
                            token=serializer.validated_data['career_id']),
                        leader=serializer.validated_data['leader'],
                        numero=serializer.validated_data['numero'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                depot = None

            return Response(
                DepotStoreSerializer(
                    depot,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class StockagePartnerViewSet(viewsets.ModelViewSet):
    """ stockage partner controller """

    def get_serializer_class(self):
        """ define serializer """
        return StockagePartnerStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddHubPartner]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllHubPartner]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = StockagePartner.objects.all()
        else:
            queryset = StockagePartner.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add stockage partner """
        serializer = StockagePartnerStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    stockagepartner = StockagePartner.create(
                        firm=serializer.validated_data['firm_id'],
                        village=serializer.validated_data['village_id'],
                        name=serializer.validated_data['name'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                stockagepartner = None

            return Response(
                StockagePartnerStoreSerializer(
                    stockagepartner,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class TransferViewSet(viewsets.ModelViewSet):
    """ transfer controller """

    def get_serializer_class(self):
        """ define serializer """
        return TransferStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create' or self.action == 'ptz':
            self.permission_classes = [IsAddTransfer]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllTransfer]
        elif self.action == 'reception':
            self.permission_classes = [IsReceiveTransfer]
        elif self.action == 'receptionvente':
            self.permission_classes = [IsReceiveSaleTransfer]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Transfer.objects.all()
        else:
            queryset = Transfer.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add transfer """
        serializer = TransferStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    transfer = Transfer.create(
                        article=Article.readByToken(
                            token=serializer.validated_data['article_id']
                        ),
                        career=Carriere.readByToken(
                            token=serializer.validated_data['career_id']
                        ),
                        date_op=serializer.validated_data['date_op'],
                        depot=Depot.readByToken(
                            token=serializer.validated_data['depot_id']
                        ),
                        driver=serializer.validated_data['driver'],
                        physical_waybill=serializer.validated_data[
                            'physical_waybill'
                        ],
                        stockage_aera=StockageAera.readByToken(
                            token=serializer.validated_data['stockageaera_id']
                        ),
                        tractor=Tractor.readByToken(
                            token=serializer.validated_data['tractor_id']
                        ),
                        trailer=Trailer.readByToken(
                            token=serializer.validated_data['trailer_id']
                        ),
                        transfer_slip=serializer.validated_data[
                            'transfer_slip'
                        ],
                        volume_transferred=serializer.validated_data[
                            'volume_transferred'
                        ],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                transfer = None

            return Response(
                TransferStoreSerializer(
                    transfer,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def reception(self, request, pk):
        """ to receive a transfer """
        transfer = self.get_object()
        serializer = ReceiveTransferSerializer(
            data=request.data,
            context={
                "request": request,
                "transfer": transfer
            }
        )
        if serializer.is_valid():
            transfer.reception(
                date_recep=serializer.validated_data['date_recep'],
                volume=serializer.validated_data["volume_receptionned"],
                user=self.request.infoUser["id"]
            )
            return Response(
                TransferStoreSerializer(
                    transfer,
                    context={
                        "request": request
                    },
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def receptionvente(self, request, pk):
        """ to receive a transfer plus sale """
        transfer = self.get_object()
        serializer = ReceiveTransferVenteSerializer(
            data=request.data,
            context={
                "request": request,
                "transfer": transfer
            }
        )
        if serializer.is_valid():
            if serializer.validated_data['stockage_partner_id'] != 'Autre':
                stockage_partner = StockagePartner.readByToken(
                    serializer.validated_data['stockage_partner_id']
                )
                stock_partner_art = StockagePartnerArticle.objects.get(
                    stockage_partner=stockage_partner,
                    article=transfer.article,
                    stockage_aera=transfer.stockage_aera
                )
                sale_unit_price = stock_partner_art.price_sale
                destination = stockage_partner.name
            else:
                stockage_partner = None
                sale_unit_price = serializer.validated_data['sale_unit_price']
                destination = serializer.validated_data['destination']

            transfer.receptionVente(
                date_recep=serializer.validated_data['date_recep'],
                destination=destination,
                sale_unit_price=sale_unit_price,
                stockagePartner=stockage_partner,
                volume=serializer.validated_data['volume_receptionned'],
                user=self.request.infoUser["id"]
            )
            return Response(
                TransferStoreSerializer(
                    transfer,
                    context={
                        "request": request
                    },
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"])
    def ptz(self, request, pk=None):
        """ import careers, stockage """
        conn1 = http.client.HTTPSConnection('bfc.api.zukulufeg.com')
        payload1 = ''
        headers1 = {
            "Authorization": 'd3f46689-b1bc-4ab5-947b-968367a54982:04-06-2023-14-01-16'
        }
        conn1.request("GET", "/api/transfert", payload1, headers1)
        response1 = conn1.getresponse()
        data = json.loads(response1.read())
        d = data['data']
        transfers = []
        user=self.request.infoUser["id"]
        for item in d:
            nom_article = item['nom']
            try:
                article = Article.objects.get(name=nom_article)
            except Article.DoesNotExist:
                categorie = Categorie.create(name='sable', user=user)
                article = Article.create(
                    name=nom_article,
                    categorie=categorie,
                    user=user
                )
            nom_career = item['carriere']['nom']
            try:
                career = Carriere.objects.get(name=nom_career)
            except Carriere.DoesNotExist:
                career = Carriere.create(
                    name=nom_career,
                    village="non defini",
                    uin="aaaaaaaaaaaaa",
                    localisation="non definie",
                    proprio="non defini",
                    user=user
                )
                CareerArticle.create(
                    career=career,
                    article=article,
                    
                )
            nom_stockage = item['stockage']['nom']
            transfert = Transfer.create()
            transfers.push(transfert)
        return Response(
            TransferStoreSerializer(
                transfers,
                context={"request": request},
                many=True
            ).data,
            status=status.HTTP_201_CREATED
        )


class StockagePartnerArticleViewSet(viewsets.ModelViewSet):
    """ stockage partner article controller """

    def get_serializer_class(self):
        """ define serializer """
        return DepotVenteArticleStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddStockagePartnerArticle]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllStockagePartnerArticle]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = StockagePartnerArticle.objects.all()
        else:
            queryset = StockagePartnerArticle.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add stockage partner article """
        serializer = DepotVenteArticleStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    stockagepartnerarticle = StockagePartnerArticle.create(
                        stockage_partner=StockagePartner.readByToken(
                            token=serializer.validated_data['stockage_partner_id']
                        ),
                        article=Article.readByToken(
                            token=serializer.validated_data['article_id']
                        ),
                        stockage_aera=StockageAera.readByToken(
                            token=serializer.validated_data['stockage_id']
                        ),
                        price_car=serializer.validated_data['price_car'],
                        price_sale=serializer.validated_data['price_sale'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                stockagepartnerarticle = None

            return Response(
                DepotVenteArticleStoreSerializer(
                    stockagepartnerarticle,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class SaleViewSet(viewsets.ModelViewSet):
    """ sale controller """

    def get_serializer_class(self):
        """ define serializer """
        return SaleStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddSale]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllSale]
        elif self.action == 'reception':
            self.permission_classes = [IsReceiveSale]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Sale.objects.all()
        else:
            queryset = Sale.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add sale """
        serializer = SaleStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            if serializer.validated_data['stockage_aera_id'] != 'Autre':
                stockage_aera = StockageAera.readByToken(
                    token=serializer.validated_data['stockage_aera_id']
                )
            else:
                stockage_aera = None

            if serializer.validated_data['stockage_partner_id'] != 'Autre':
                stockage_partner = StockagePartner.readByToken(
                    token=serializer.validated_data['stockage_partner_id']
                )
            else:
                stockage_partner = None

            if stockage_aera is not None and stockage_partner is not None:
                type_sale = 1
            elif stockage_aera is not None and stockage_partner is None:
                type_sale = 2
            else:
                type_sale = 3

            sale = Sale.create(
                article=Article.readByToken(
                    token=serializer.validated_data['article_id']),
                date_op=serializer.validated_data['date_op'],
                destination=serializer.validated_data['destination'],
                driver=serializer.validated_data['driver'],
                sale_slip=serializer.validated_data['sale_slip'],
                sale_unit_price=serializer.validated_data['sale_unit_price'],
                stockage_aera=stockage_aera,
                stockage_partner=stockage_partner,
                tractor=Tractor.readByToken(token=serializer.validated_data['tractor_id']),
                trailer=Trailer.readByToken(token=serializer.validated_data['trailer_id']),
                type_sale=type_sale,
                user=request.infoUser.get('id'),
                volume=serializer.validated_data['volume']
            )

            return Response(
                SaleStoreSerializer(
                    sale,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def reception(self, request, pk):
        """ to receive sale """
        sale = self.get_object()
        serializer = ReceiveVenteSerializer(
            data=request.data,
            context={
                "request": request,
                "sale": sale
            }
        )
        if serializer.is_valid():
            sale.reception(
                date_recep=serializer.validated_data['date_recep'],
                volume=serializer.validated_data["volume_receptionned"],
                user=self.request.infoUser["id"]
            )
            return Response(
                SaleStoreSerializer(
                    sale,
                    context={
                        "request": request
                    },
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
