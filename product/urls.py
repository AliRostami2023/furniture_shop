from django.urls import path, re_path
from . import views 


app_name = 'product'

urlpatterns = [
    path('', views.ListProductAPIView.as_view(), name='product_list'),
    re_path(r'^detail/(?P<slug>[-\wآ-ی]+)/', views.RetriveProductAPIView.as_view(), name='product_detail'),
    path('create/', views.CreateProductAPIView.as_view(), name='create_product'),
    path('update/<int:pk>/', views.UpdateProductAPIView.as_view(), name='update_product'),
    path('category_list/', views.ListCategoryProductAPIView.as_view(), name='list_category_product'),
    re_path(r'^category/detail/(?P<slug>[-\wآ-ی]+)/', views.RetriveCategoryProductAPIView.as_view(), name='category_product_detail'),
    path('create_category/', views.CreateCategoryProductAPIView.as_view(), name='create_category_product'),
    path('update_category/<int:pk>/', views.UpdateCategoryProductAPIView.as_view(), name='update_category_product'),
    path('favorits/', views.ListProductFavoriteAPIView.as_view(), name='list_favorits'),
    path('favorite/<int:product_id>', views.FavoriteProductView.as_view(), name='add_product_favorite'),
    re_path(r'^(?P<product_slug>[-\wآ-ی]+)/comments/', views.CommentListAPIView.as_view(), name='comment-list'),
    re_path(r'^(?P<product_slug>[-\wآ-ی]+)/create_comment/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    re_path(r'^(?P<product_slug>[-\wآ-ی]+)/(?P<comment_id>\d+)/reply/', views.ReplyCreateAPIView.as_view(), name='comment-reply'),
    re_path(r'^(?P<product_slug>[-\wآ-ی]+)/(?P<pk>\d+)/edit/', views.CommentUpdateDeleteAPIView.as_view(), name='comment-edit'),
    re_path(r'^(?P<product_slug>[-\wآ-ی]+)/replies/(?P<pk>\d+)/edit/', views.ReplyUpdateDeleteAPIView.as_view(), name='reply-edit'),
]
