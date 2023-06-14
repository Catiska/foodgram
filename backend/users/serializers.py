from rest_framework import serializers, validators
from drf_extra_fields.fields import Base64ImageField

from .models import User, Follow
from recipes.models import Recipe


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания юзера."""
    email = serializers.EmailField(
        validators=(validators.UniqueValidator(queryset=User.objects.all()),)
    )
    username = serializers.CharField(
        validators=(validators.UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class MyUserSerializer(serializers.ModelSerializer):
    """Сериализатор юзера."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or user is None:
            return False
        # return user.follower.filter(author=obj).exists()
        return Follow.objects.filter(user=user, author=obj).exists()


class MiniRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipe с укороченным набором полей для сериализатора
     подписок"""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(MyUserSerializer):
    """Сериализатор подписок на других юзеров."""
    recipes = MiniRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(MyUserSerializer.Meta):
        model = User
        fields = MyUserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = '__all__',

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return True
