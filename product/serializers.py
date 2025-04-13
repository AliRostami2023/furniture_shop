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
        model = CommentProduct
        fields = ['id', 'body', 'create_at', 'user']


class CommentListSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title')
    user = UserSimpleSerializer()
    reply = serializers.SerializerMethodField(method_name='get_reply')

    class Meta:
        model = CommentProduct
        fields = ['id', 'body', 'create_at', 'user', 'product', 'reply']

    def get_reply(self, obj):
        replies = obj.replies.all()
        return ReplyListSerializer(replies, many=True).data
	

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentProduct
        fields = ['body']


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentProduct
        fields = ['body']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentProduct
        fields = ['body']


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentProduct
        fields = ['body']


class ListRetriveCategoryProductSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField()
	
	class Meta:
		model = CategoryProduct
		fields = '__all__'

	def get_image(self, obj):
		if isinstance(obj.image, Image):
			return obj.image.image.url if obj.image.image else None
		return None
      

class CreateCategoryProductSerializer(serializers.ModelSerializer):
      class Meta:
        model = CategoryProduct
        fields = '__all__'


class UpdateCategoryProductSerializer(serializers.ModelSerializer):
      class Meta:
        model = CategoryProduct
        fields = '__all__'


class GalleryProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = GalleryProduct
		fields = '__all__'


class ListRetriveProductSerializer(serializers.ModelSerializer):
    category = ListRetriveCategoryProductSerializer()
    comment_product = CommentListSerializer(many=True)
    final_price = serializers.IntegerField()
    product_image = GalleryProductSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'category', 'final_price', 'price', 'discount', 'image',
            'product_image', 'rating', 'width', 'lenght', 'weight', 'color',
            'meterial', 'comment_product', 'create_at', 'update_at'
        ]

    def get_image(self, obj):
        if isinstance(obj.image, Image):
            return obj.image.image.url if obj.image.image else None
        return None


class CreateProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product
          fields = '__all__'


class UpdateProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product
          fields = '__all__'



class ProductFavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductFavorite
		fields = ['id', 'user', 'product']
		read_only_fields = ['user', 'create_at']
