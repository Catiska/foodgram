from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .pagination import PageNumberLimitPagination
from .filters import RecipeFilterSet, IngredientSearchFilter
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipeSerializer)
from users.serializers import MiniRecipeSerializer
from recipes.models import (Recipe, Tag, Ingredient, IngredientsAmount,
                            Favorite, ShoppingCart)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов, добавлять ингредиенты может только админ."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тэгов, добавлять тэги может только админ."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


# class FavoritesViewSet()

class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов. Создание, удаление и обновление рецепта.
    Возможность добавлять рецепты в избранное и в список покупок.
    Возможность скачать список покупок в формате txt."""
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PageNumberLimitPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_object(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk):
            return Response({'errors': 'Этот рецепт уже добавлен'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = MiniRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_object(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Уже удалено'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['get', 'post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        if request.method == 'DELETE':
            return self.delete_object(Favorite, request.user, pk)
        return self.add_object(Favorite, request.user, pk)

    @action(detail=True,
            methods=['get', 'post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'DELETE':
            return self.delete_object(ShoppingCart, request.user, pk)
        return self.add_object(ShoppingCart, request.user, pk)

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        if not request.user.shopping_cart.exists():
            return Response({'errors': 'Корзина пуста'},
                            status=status.HTTP_400_BAD_REQUEST)
        download_list = 'Список покупок:/n'
        ingredients = IngredientsAmount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).order_by(
            'ingredient__name'
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        current_date = datetime.today()

        for num, ingredient in enumerate(ingredients):
            download_list += (
                f'\n{num+1}. {ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}'
            )
        download_list += f'\n\n\n{current_date:%d.%m.%Y}\n' \
                         f'Создано на сайте foodgram.catiska.ru ' \
                         f'пользователем {request.user.get_full_name()}'
        filename = f'{request.user.username}_download_list.txt'
        response = HttpResponse(download_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
