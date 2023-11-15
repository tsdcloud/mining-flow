from django.shortcuts import get_object_or_404
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.decorators import action

from article.serializers import (
    CategorieStoreSerializer,
    ArticleStoreSerializer
)
from article.models import Categorie, Article

from common.permissions import IsDeactivate
from . permissions import (
    IsAddCategorie,
    IsViewAllCategorie,
    IsAddArticle,
    IsViewAllArticle
)


class CategorieViewSet(viewsets.ModelViewSet):
    """ categorie controller """

    def get_serializer_class(self):
        """ define serializer """
        return CategorieStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddCategorie]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllCategorie]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Categorie.objects.all()
        else:
            queryset = Categorie.objects.filter(is_active=True)
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
        """ add categorie """
        serializer = CategorieStoreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    categorie = Categorie.create(
                        name=serializer.validated_data['name'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                categorie = None

            return Response(
                CategorieStoreSerializer(categorie).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ArticleViewSet(viewsets.ModelViewSet):
    """ article controller """

    def get_serializer_class(self):
        """ define serializer """
        return ArticleStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddArticle]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllArticle]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(is_active=True)
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
        """ add article """
        serializer = ArticleStoreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    categorie = Categorie.readByToken(
                        token=serializer.validated_data['category_id']
                    )
                    article = Article.create(
                        name=serializer.validated_data['name'],
                        categorie=categorie,
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                article = None

            return Response(
                ArticleStoreSerializer(article).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )