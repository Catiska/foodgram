from rest_framework.pagination import PageNumberPagination


class PageNumberLimitPagination(PageNumberPagination):
    """Отображение 6 рецептов на странице."""

    page_size = 6
    page_size_query_param = 'limit'
