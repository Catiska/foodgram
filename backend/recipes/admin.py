from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name',)
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
    search_fields = ('name',)
    inlines = [IngredientInline, ]
    exclude = ('ingredient',)

    def in_favorites(self, obj):
        return obj.favorite.count()

    in_favorites.short_description = 'В избранном'


@admin.register(IngredientsAmount)
class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)
    search_fields = ('recipe',)
    empty_value_display = '-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('recipe',)
    empty_value_display = '-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('recipe',)
    empty_value_display = '-'
