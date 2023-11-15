from rest_framework import serializers

from car.models import (
    Trailer,
    Tractor
)


class TractorStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add tractor """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_used = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Tractor
        fields = [
            'id',
            'is_active',
            'registration',
            'serial_number',
            'brand',
            'model',
            'is_used'
        ]

    def validate_registration(self, value):
        """ check logical validity of registration """
        try:
            Tractor.objects.get(registration=value, is_active=True)
            raise serializers.ValidationError(
                detail='registration already exists'
            )
        except Tractor.DoesNotExist:
            if 5 > len(value):
                raise serializers.ValidationError(
                    detail='bad registration'
                )
            return value

    def validate_serial_number(self, value):
        """ check logical validity of serial_number """
        try:
            Tractor.objects.get(serial_number=value, is_active=True)
            raise serializers.ValidationError(
                detail='serial_number already exists'
            )
        except Tractor.DoesNotExist:
            if 5 > len(value):
                raise serializers.ValidationError(
                    detail='bad serial number'
                )
            return value


class TrailerStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add trailer """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_used = serializers.BooleanField(read_only=True)
    empty_volume = serializers.FloatField(required=True)

    class Meta:
        """ attributs serialized """
        model = Trailer
        fields = [
            'id',
            'is_active',
            'registration',
            'serial_number',
            'brand',
            'model',
            'empty_volume',
            'is_used'
        ]

    def validate_registration(self, value):
        """ check logical validity of registration """
        try:
            Trailer.objects.get(registration=value, is_active=True)
            raise serializers.ValidationError(
                detail='registration already exists'
            )
        except Trailer.DoesNotExist:
            if 5 > len(value):
                raise serializers.ValidationError(
                    detail='bad registration'
                )
            return value

    def validate_serial_number(self, value):
        """ check logical validity of serial_number """
        try:
            Trailer.objects.get(serial_number=value, is_active=True)
            raise serializers.ValidationError(
                detail='serial_number already exists'
            )
        except Trailer.DoesNotExist:
            if 5 > len(value):
                raise serializers.ValidationError(
                    detail='bad serial number'
                )
            return value

    def validate_empty_volume(self, value):
        """ check logical validity of empty_volume """
        if 1 > value:
            raise serializers.ValidationError(
                detail='bad empty volume'
            )
        return value
