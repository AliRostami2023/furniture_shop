from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter
from . import views 


router = DefaultRouter()
router.register("category", views.CategoryProductViewSet, basename='category')
router.register("products", views.ProductViewSet, basename='products')

product_router = NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('comment', views.CommentViewSet, basename='comment')


app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('product_favorite/<int:product_id>', views.FavoriteProductView.as_view(), name='product_favorite'),
    path('favorits/', views.ListProductFavoriteAPIView.as_view(), name='list_favorits')
]
