from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics
from .paginations import BlogPagination, CommentBlogPagination
from .models import *
from .serializers import *


class ListCategoryBlogAPIView(generics.ListAPIView):
    queryset = CategoryBlog.objects.all()
    serializer_class = ListRetriveCategoryBlogSerializer


class RetriveCategoryBlogAPIView(generics.RetrieveAPIView):
    queryset = CategoryBlog.objects.all()
    serializer_class = ListRetriveCategoryBlogSerializer
    lookup_field = 'slug'


class CreateCategoryBlogAPIView(generics.CreateAPIView):
    queryset = CategoryBlog.objects.all()
    serializer_class = CreateCategoryBlogSerializer
    permission_classes = [permissions.IsAdminUser]


class UpdateCategoryBlogAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = CategoryBlog.objects.all()
    serializer_class = UpdateCategoryBlogSerializer
    permission_classes = [permissions.IsAdminUser]
    


class ListBlogAPIView(generics.ListAPIView,):
    queryset = Blog.objects.select_related('category', 'image')
    serializer_class = ListRetriveBlogSerializer
    permissions_classes = [permissions.IsAdminUser]
    pagination_class = BlogPagination
    lookup_field = 'slug'


class RetriveBlogAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.select_related('category', 'image')
    serializer_class = ListRetriveBlogSerializer
    lookup_field = 'slug'


class CreateBlogAPIView(generics.CreateAPIView):
    queryset = Blog.objects.select_related('category', 'image')
    serializer_class = CreateBlogSerializer
    permission_classes = [permissions.IsAdminUser]
    


class UpdateBlogAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Blog.objects.select_related('category', 'image')
    serializer_class = UpdateBlogSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentBlogListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentBlogPagination

    def get_queryset(self):
        return CommentBlog.objects.filter(
            blog__slug=self.kwargs['blog_slug'],
            reply=None
        ).select_related('user', 'blog', 'reply')


class CommentBlogCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blog = get_object_or_404(Blog, slug=self.kwargs['blog_slug'])
        serializer.save(user=self.request.user, blog=blog)


class BlogReplyCreateAPIView(generics.CreateAPIView):
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blog = get_object_or_404(Blog, slug=self.kwargs['blog_slug'])
        parent_comment = get_object_or_404(CommentBlog, pk=self.kwargs['comment_id'])

        if parent_comment.reply is not None:
            raise serializers.ValidationError("ریپلای روی ریپلای مجاز نیست.")

        serializer.save(user=self.request.user, blog=blog, reply=parent_comment)


class CommentBlogUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return CommentBlog.objects.filter(
            blog__slug=self.kwargs['blog_slug'],
            reply=None
        )


class BlogReplyUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReplyUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return CommentBlog.objects.filter(
            blog__slug=self.kwargs['blog_slug']
        ).exclude(reply=None)
    