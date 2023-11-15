from django.shortcuts import get_object_or_404
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from car.serializers import (
    TractorStoreSerializer,
    TrailerStoreSerializer
)
from car.models import (
    Trailer,
    Tractor
)

from common.permissions import IsDeactivate
from . permissions import (
    IsAddTractor,
    IsAddTrailer,
    IsViewTractor,
    IsViewTrailer
)


class TractorViewSet(viewsets.ModelViewSet):
    """ tractor controller """

    def get_serializer_class(self):
        """ define serializer """
        return TractorStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddTractor]
        elif self.action == 'list':
            self.permission_classes = [IsViewTractor]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Tractor.objects.all()
        else:
            queryset = Tractor.objects.filter(is_active=True)
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
        """ add tractor """
        serializer = TractorStoreSerializer(
            data=request.data
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    tractor = Tractor.create(
                        brand=serializer.validated_data['brand'],
                        model=serializer.validated_data['model'],
                        registration=serializer.validated_data['registration'],
                        serial_number=serializer.validated_data['serial_number'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                tractor = None

            return Response(
                TractorStoreSerializer(
                    tractor
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class TrailerViewSet(viewsets.ModelViewSet):
    """ trailer controller """

    def get_serializer_class(self):
        """ define serializer """
        return TrailerStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddTrailer]
        elif self.action == 'list':
            self.permission_classes = [IsViewTrailer]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['member']['is_superuser'] is True:
            queryset = Trailer.objects.all()
        else:
            queryset = Trailer.objects.filter(is_active=True)
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
        """ add trailer """
        serializer = TrailerStoreSerializer(
            data=request.data
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    trailer = Trailer.create(
                        brand=serializer.validated_data['brand'],
                        model=serializer.validated_data['model'],
                        registration=serializer.validated_data['registration'],
                        serial_number=serializer.validated_data['serial_number'],
                        empty_volume=serializer.validated_data['empty_volume'],
                        user=request.infoUser.get('id')
                    )
            except DatabaseError:
                trailer = None

            return Response(
                TrailerStoreSerializer(
                    trailer
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
