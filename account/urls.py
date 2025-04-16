from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


app_name = 'auth'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.CreateUserAPIView.as_view(), name='register'),
    path('password-reset/', views.PasswordResetAPIView.as_view(), name='password-reset'),
    path('confirm-password-reset/<str:token>/', views.ConfirmResetPasswordAPIView.as_view(), name='confirm-reset-password'),
   
    # Profile
    path('profile/', views.ProfileRetrieveAPIView.as_view(), name='profile-detail'),
    path('profile/update/', views.ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('profile_list/', views.ProfileListAPIView.as_view(), name='profile-list'),
]
