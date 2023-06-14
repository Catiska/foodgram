from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Follow
from .serializers import MyUserSerializer, FollowSerializer
from api.pagination import PageNumberLimitPagination


class MyUserViewSet(UserViewSet):
    """Вьюсет юзера. Возможность подписываться и отписываться от других
    юзеров, просмотреть список подписок."""
    pagination_class = PageNumberLimitPagination
    serializer_class = MyUserSerializer
    queryset = User.objects.all()

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if request.method == 'DELETE':
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)
        # Не трогать даже под дулом пистолета:
        serializer = self.get_serializer(author)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=self.request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages, many=True,)
        return self.get_paginated_response(serializer.data)
