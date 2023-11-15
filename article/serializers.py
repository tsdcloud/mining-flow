from rest_framework import serializers

from article.models import Categorie, Article


class CategorieStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add categorie """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Categorie
        fields = [
            'id',
            'is_active',
            'name',
        ]

    def validate_name(self, value):
        """ check logical validity of name """
        try:
            Categorie.objects.get(
                name=value.upper(), is_active=True)
            raise serializers.ValidationError(
                detail="categorie already exists"
            )
        except Exception:
            pass
        return value


class ArticleStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add article """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    categorie = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = Article
        fields = [
            'id',
            'is_active',
            'name',
            'category_id',
            'categorie'
        ]

    def get_categorie(self, instance):
        return {
            "id": instance.categorie.id,
            "name": instance.categorie.name
        }

    def validate_name(self, value):
        """ check logical validity of name """
        try:
            Article.objects.get(
                name=value.upper(), is_active=True)
            raise serializers.ValidationError(
                detail="article already exists"
            )
        except Exception:
            pass
        return value

    def validate_category_id(self, value):
        """ check logical validity of category """
        try:
            Categorie.objects.get(
                id=value, is_active=True)
        except Exception:
            raise serializers.ValidationError(
                detail="article not found"
            )
        return value
