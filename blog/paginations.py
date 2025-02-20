from rest_framework.pagination import PageNumberPagination


class BlogPagination(PageNumberPagination):
    page_size = 15


class CommentBlogPagination(PageNumberPagination):
    page_size = 30
    