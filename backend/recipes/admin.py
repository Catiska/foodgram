from django.contrib import admin
from .models import (Recipe, Tag, Ingredient, IngredientsAmount, ShoppingCart,
                     Favorite)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-'


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time', 'text',
                    'in_favorites')
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author', 'tags', 'cooking_time')
    empty_value_display = '-'
    inlines = [IngredientInline, ]
    exclude = ('ingredient',)

    def in_favorites(self, obj):
        return obj.favorites.count()

    in_favorites.short_description = 'В избранном'


@admin.register(IngredientsAmount)
class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)
    empty_value_display = '-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    empty_value_display = '-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    empty_value_display = '-'
