from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("contact_us", views.ContactUsViewSet, basename='contact_us')
router.register("about_us", views.AboutUsViewSet, basename='about_us')
router.register("employees", views.EmployeesViewSet, basename='employees')
router.register("slider", views.SliderHomeViewSet, basename='slider')
router.register("footer_link", views.FooterLinkViewSet, basename='footer_link')
router.register("licence", views.LicenceViewSet, basename='licence')
router.register("information_shop", views.InformationShopViewSet, basename='information_shop')
router.register("services", views.ServiceViewSet, basename='services')

app_name = 'home'

urlpatterns = router.urls
