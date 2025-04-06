from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import F, ExpressionWrapper, IntegerField
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter
from .paginations import ProductPagination, CommentProductPagination, ProductFavoritePagination
from .models import *
from .serializers import *


class ListCategoryProductAPIView(generics.ListAPIView):
    queryset = CategoryProduct.objects.select_related('image')
    serializer_class = ListRetriveCategoryProductSerializer


class RetriveCategoryProductAPIView(generics.RetrieveAPIView):
    queryset = CategoryProduct.objects.select_related('image')
    serializer_class = ListRetriveCategoryProductSerializer
    lookup_field = 'slug'


class CreateCategoryProductAPIView(generics.CreateAPIView):
    queryset = CategoryProduct.objects.select_related('image')
    serializer_class = CreateCategoryProductSerializer
    permission_classes = [permissions.IsAdminUser]


class UpdateCategoryProductAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = CategoryProduct.objects.select_related('image')
    serializer_class = UpdateCategoryProductSerializer
    permission_classes = [permissions.IsAdminUser]
    


class ListProductAPIView(generics.ListAPIView):
    queryset = Product.objects.select_related(
         'category', 'image').prefetch_related(
              'comment_product', 'product_image').annotate(
                   final_price=ExpressionWrapper(
                   F('price') * (1 - F('discount') / 100),
                   output_field=IntegerField()
              ))
    serializer_class = ListRetriveProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'category']
    ordering_fields = ['price', 'create_at']


class RetriveProductAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related(
                            'category', 'image').prefetch_related('comment_product', 'product_image')
    serializer_class = ListRetriveProductSerializer
    lookup_field = 'slug'


class CreateProductAPIView(generics.CreateAPIView):
    queryset = Product.objects.select_related(
                        'category', 'image').prefetch_related('comment_product', 'product_image')
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAdminUser]
    


class UpdateProductAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Product.objects.select_related(
                            'category', 'image').prefetch_related('comment_product', 'product_image')
    serializer_class = UpdateProductSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentProductPagination

    def get_queryset(self):
        return CommentProduct.objects.filter(
            product__slug=self.kwargs['product_slug'],
            reply=None
        ).select_related('user', 'product', 'reply')


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        serializer.save(user=self.request.user, product=product)


class ReplyCreateAPIView(generics.CreateAPIView):
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        parent_comment = get_object_or_404(CommentProduct, pk=self.kwargs['comment_id'])

        if parent_comment.reply is not None:
            raise serializers.ValidationError("ریپلای روی ریپلای مجاز نیست.")

        serializer.save(user=self.request.user, product=product, reply=parent_comment)


class CommentUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return CommentProduct.objects.filter(
            product__slug=self.kwargs['product_slug'],
            reply=None
        )


class ReplyUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReplyUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return CommentProduct.objects.filter(
            product__slug=self.kwargs['product_slug']
        ).exclude(reply=None)


    

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
    
    