from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 21


class CommentProductPagination(PageNumberPagination):
    page_size = 30


class ProductFavoritePagination(PageNumberPagination):
    page_size = 10
    