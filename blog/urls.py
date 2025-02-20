from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from . import views


router = DefaultRouter()
router.register('blog', views.BlogViewSet, basename='blog')
router.register('category', views.CategoryBlogViewSet, basename='category_blog')

article_router = NestedDefaultRouter(router, 'blog', lookup='blog')
article_router.register('comment', views.CommentBlogViewSet, basename='comment')


app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(article_router.urls)),
]