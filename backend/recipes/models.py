from django.core import validators
from django.db import models
from users.models import User

from .colors import HexColors


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField('Ингредиент', max_length=200)
    measurement_unit = models.CharField('Единица измерения',
                                        max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient-measure')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тэга."""

    name = models.CharField('Тэг', unique=True, max_length=200)
    color = models.CharField('Цвет Hex',
                             max_length=7,
                             unique=True,
                             choices=HexColors.choices,
                             default=HexColors.GRAY)
    slug = models.SlugField('Слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField('Рецепт', max_length=200)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    image = models.ImageField('Фото блюда', upload_to='recipes/')
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='IngredientsAmount',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Тэги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            validators.MinValueValidator(
                1, 'Минимальное время готовки - 1 минута'),),
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):
    """Модель связи ингредиентов и рецепта."""

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipes_ingredients')
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            validators.MinValueValidator(
                1, 'Нужно хоть какое-то количество ингредиента'),),
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique recipe-ingredients'
            )
        ]

    def __str__(self):
        return (f'{self.ingredient.name}, {self.ingredient.measurement_unit}'
                f' - {self.amount}')


class Favorite(models.Model):
    """Модель избранных рецептов."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorite')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Юзер',
                             related_name='favorite')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - избранный рецепт для юзера {self.user}'


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='shopping_cart')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Юзер',
                             related_name='shopping_cart')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique cart-user'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - в корзине юзера {self.user}'
