from rest_framework import serializers
from .models import *



class UserSimpleSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            return request.build_absolute_uri(profile.avatar.url) if request else profile.avatar.url
        return None


class ReplyListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name')

    class Meta:
        model = CommentBlog
        fields = ['id', 'body', 'create_at', 'user']


class CommentListSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title')
    user = UserSimpleSerializer()
    reply = serializers.SerializerMethodField(method_name='get_reply')

    class Meta:
        model = CommentBlog
        fields = ['id', 'body', 'create_at', 'user', 'product', 'reply']

    def get_reply(self, obj):
        replies = obj.repliess.all()
        return ReplyListSerializer(replies, many=True).data
	

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ['body']


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ['body']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ['body']


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ['body']


class ListRetriveCategoryBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = CategoryBlog
		fields = '__all__'
            

class CreateCategoryBlogSerializer(serializers.ModelSerializer):
      class Meta:
        model = CategoryBlog
        fields = '__all__'


class UpdateCategoryBlogSerializer(serializers.ModelSerializer):
      class Meta:
        model = CategoryBlog
        fields = '__all__'


class ListRetriveBlogSerializer(serializers.ModelSerializer):
	category = ListRetriveCategoryBlogSerializer(source='category.title')
	comment_blog = CommentListSerializer(many=True)

	class Meta:
		model = Blog
		fields = ['title', 'slug', 'category', 'image', 'content', 'comment_blog', 'create_at', 'update_at']

	def get_image(self, obj):
		if isinstance(obj.image, Image):
			return obj.image.image.url if obj.image.image else None
		return None


class UpdateBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ['title', 'category', 'image', 'content']
            

class CreateBlogSerializer(serializers.ModelSerializer):
     class Meta:
          model = Blog
          fields = '__all__'

		