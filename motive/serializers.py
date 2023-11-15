from rest_framework import serializers

from motive.models import Motive


class MotiveStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add motive """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Motive
        fields = [
            'id',
            'is_active',
            'suspension_name',
            'active_name',
            'special_active',
            'service'
        ]


    def validate(self, data):
        """ check logical validity of data """
        try:
            image = base64.b64decode(value)
            img = Image.open(io.BytesIO(image))
            if img.format.lower() in ACCEPT_IMAGE:
                width, height = img.size
                if width * height > MAX_IMAGE_SIZE:
                    raise serializers.ValidationError('image too large')
            else:
                raise serializers.ValidationError('not valid extension')
        except Exception:
            raise serializers.ValidationError('logo is not valid base64 image')
        return value


class FirmDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update entity """
    id = serializers.CharField(
        max_length=1000, required=False, read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Firm
        fields = "__all__"

    def validate_business_name(self, value):
        """ check validity of social_raison """
        try:
            f = Firm.objects.get(business_name=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError(
                    'business_name already exists'
                )
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_unique_identifier_number(self, value):
        """ check validity of unique_identifier_number """
        try:
            f = Firm.objects.get(unique_identifier_number=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError(
                    'unique_identifier_number already exists'
                )
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_trade_register(self, value):
        """ check validity of trade_register """
        try:
            f = Firm.objects.get(trade_register=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError(
                    'trade_register already exists'
                )
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_type_person(self, value):
        """ check validity of type_person """
        if value not in [1, 2, '1', '2']:
            raise serializers.ValidationError(
                'provide correct value for type_person'
            )
        return value

    def validate_logo(self, value):
        """ check validity of logo """
        try:
            image = base64.b64decode(value)
            img = Image.open(io.BytesIO(image))
            if img.format.lower() in ACCEPT_IMAGE:
                width, height = img.size
                if width * height > MAX_IMAGE_SIZE:
                    raise serializers.ValidationError('image too large')
            else:
                raise serializers.ValidationError('not valid extension')
        except Exception:
            raise serializers.ValidationError('logo is not valid base64 image')
        return value
