from rest_framework import serializers
from .models import *



class CommentSerializer(serializers.ModelSerializer):
	blog = serializers.CharField(source='blog.title')

	class Meta:
		model = CommentBlog
		fields = "__all__"


class CreateCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentBlog
		fields = ['body']
		
	def create(self, validated_data):
		blog = Blog.objects.get(slug=self.context['blog_slug'])
		return CommentBlog.objects.create(blog=blog, **validated_data)


class CategoryBlogSerializers(serializers.ModelSerializer):
	class Meta:
		model = CategoryBlog
		fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
	category = CategoryBlogSerializers(source='category.title')
	comment_blog = CommentSerializer(many=True)

	class Meta:
		model = Blog
		fields = ['title', 'slug', 'category', 'image', 'content', 'comment_blog', 'create_at', 'update_at']


class EditBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ['title', 'category', 'image', 'content']
		