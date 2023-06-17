from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientsAmount, Recipe, Tag
from rest_framework import serializers, validators, exceptions
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from users.models import User
#
# from .validators import (validate_cooking_time, validate_ingredients,
#                          validate_tags)


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


class UserSerializer(serializers.ModelSerializer):
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
        return user.follower.filter(author=obj).exists()


class MiniRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipe с укороченным набором полей для сериализатора
     подписок"""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(UserSerializer):
    """Сериализатор подписок на других юзеров."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = '__all__',

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.select_related('author')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = MiniRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return True


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериалиатор модели тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsAmountSerializer(serializers.ModelSerializer):
    """Сериализатор модели связи рецепта и ингредиентов."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientsAmount.objects.all(),
                fields=['ingredient', 'recipe'],
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецептов (создание, обновление, чтение рецепта)."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'tags', 'ingredients', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_ingredients(self, recipe):
        ingredients = recipe.recipes_ingredients.filter(recipe=recipe)
        return IngredientsAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=recipe).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингридиент для рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингридиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Убедитесь, что значение количества '
                                    'ингредиента больше 0')
                })
        data['ingredients'] = ingredients
        return data
        # tags = self.initial_data.get('tags')
        # ingredients = self.initial_data.get('ingredients')
        # cooking_time = self.initial_data.get('cooking_time')
        #
        # data.update({
        #     'tags': tags,
        #     'ingredients': ingredients,
        #     'cooking_time': cooking_time,
        #     'author': self.context.get('request').user})
        # return data

    # def validate_ingredients(self, ingredients):
    #     if not ingredients:
    #         raise ValidationError({
    #             'ingredients': 'Из воздуха каши не сваришь, добавьте '
    #                            'ингредиенты'})
    #     valid_ingredients = []
    #     for item in ingredients:
    #         ingredient = get_object_or_404(Ingredient, id=item['id'])
    #         if int(item['amount']) < 1:
    #             raise ValidationError({
    #                 'ingredients': 'Добавьте корректное количество '
    #                                'ингредиента, значение должно
    #                                быть больше 0'
    #             })
    #         if ingredient in valid_ingredients:
    #             raise ValidationError({
    #                 'ingredients': 'Ингредиенты не должны дублироваться'})
    #         valid_ingredients.append(ingredient)
    #
    #     return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise exceptions.ValidationError({
                'tags': 'Нужно выбрать хотя бы оин тэг'
            })
        valid_tags = []
        for tag in tags:
            if not Tag.objects.filter(id__in=tags).exists():
                raise exceptions.ValidationError({
                    'tags': 'Такой тэг пока не добавили, '
                            'обратитесь к админу :)'
                })
            if tag in valid_tags:
                raise exceptions.ValidationError({
                    'tags': 'Вы уже добавили этот тэг, проверьте :)'
                })
            valid_tags.append(tag)
        return tags

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < 1:
            raise ValidationError({
                'cooking_time': 'Введите корректное время готовки, оно должно '
                                'быть больше 1'
            })
        return cooking_time

    @staticmethod
    def create_ingredients_amount(ingredients, recipe):
        for ingredient in ingredients:
            IngredientsAmount.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        # ingredients_list = []
        # for ingredient_data in ingredients:
        #     ingredient = Ingredient.objects.get(id=ingredient_data['id'])
        #     ingredients_list.append(
        #         IngredientsAmount(ingredient=ingredient,
        #                           amount=ingredient_data.pop('amount'),
        #                           recipe=recipe))
        # recipe.recipes_ingredients.bulk_create(ingredients_list)

    def create(self, validated_data) -> Recipe:
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amount(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for key, value in validated_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
        if ingredients:
            recipe.ingredients.clear()
            self.create_ingredients_amount(ingredients, recipe)
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        recipe.save()
        return recipe
