from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('', views.PendingCartView.as_view(), name='pending-cart'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('update-cart-item/<int:pk>/', views.UpdateCartItemQuantityView.as_view(), name='update-cart-item'),
    path('remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('remove-cart/', views.ClearCartView.as_view(), name='remove-cart'),
    path('user-orders/', views.UserOrderListView.as_view(), name='user-orders'),
    path('admin-orders/', views.AdminOrderListView.as_view(), name='admin-orders'),
]
