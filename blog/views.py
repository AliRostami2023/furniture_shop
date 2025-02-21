from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions
from .paginations import BlogPagination, CommentBlogPagination
from .models import *
from .serializers import *


class CategoryBlogViewSet(viewsets.ModelViewSet):
    queryset = CategoryBlog.objects.all()
    serializers_class = CategoryBlogSerializers
    permissions_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'

    def get_permission(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.select_related('category', 'image')
    serializers_class = EditBlogSerializer
    permissions_classes = [permissions.IsAdminUser]
    pagination_class = BlogPagination
    lookup_field = 'slug'

    def get_permission(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BlogSerializer
        return super().get_serializer_class()
    

    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CommentBlogViewSet(viewsets.ModelViewSet):
    serializers_class = CommentSerializer
    permissions_classes = [permissions.IsAdminUser]
    pagination_class = CommentBlogPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"blog_slug": self.kwargs['blog_slug'], "request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        return CommentBlog.objects.filter(blog__slug=self.kwargs['blog_slug']).select_related('user', 'blog', 'reply')


    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    