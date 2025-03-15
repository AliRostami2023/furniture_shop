from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter
from .paginations import ProductPagination, CommentProductPagination, ProductFavoritePagination
from .models import *
from .serializers import *


class CategoryProductViewSet(viewsets.ModelViewSet):
    queryset = CategoryProduct.objects.select_related('image')
    serializer_class = CategoryProductSerializer
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'image')
    serializer_class = EditProductSerializer
    permissions_classes = [permissions.IsAdminUser]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'category']
    ordering_fields = ['price', 'create_at']
    lookup_field = 'slug'

    def get_permission(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        return super().get_serializer_class()
    
    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permissions_classes = [permissions.IsAdminUser]
    pagination_class = CommentProductPagination


    def perform_create(self, serializer):
            serializer.save(user=self.request.user)

    def get_serializer_context(self):
            return {"product_slug": self.kwargs['product_slug'], "request": self.request}

    def get_serializer_class(self):
            if self.request.method == 'POST':
                    return CreateCommentSerializer
            return super().get_serializer_class()

    def get_permissions(self):
            if self.request.method in ["GET", "POST"]:
                    return [permissions.IsAuthenticated()]
            return super().get_permissions()

    def get_queryset(self):
            return CommentProduct.objects.filter(product__slug=self.kwargs['product_slug']).select_related('user', 'product', 'reply')


    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

class FavoriteProductView(generics.GenericAPIView):
    serializer_class = ProductFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        if ProductFavorite.objects.filter(product=product, user=request.user).exists():
            return Response({"detail": _("این محصول قبلاً به علاقه‌مندی‌ها اضافه شده است.")}, status=status.HTTP_400_BAD_REQUEST)

        favorite = ProductFavorite.objects.create(product=product, user=request.user)
        serializer = self.serializer_class(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        favorite = ProductFavorite.objects.filter(product=product, user=request.user)
        if favorite.exists():
            favorite.delete()
            return Response({"detail": _("محصول از علاقه‌مندی‌ها حذف شد.")}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": _("این محصول در لیست علاقه‌مندی‌های شما وجود ندارد.")}, status=status.HTTP_400_BAD_REQUEST)


class ListProductFavoriteAPIView(generics.ListAPIView):
    serializer_class = ProductFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductFavoritePagination

    def get_queryset(self):
        return ProductFavorite.objects.filter(user=self.request.user)
    
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    