from rest_framework import serializers
from .models import *



class CommentSerializer(serializers.ModelSerializer):
	product = serializers.CharField(source='product.title')

	class Meta:
		model = CommentProduct
		fields = "__all__"


class CreateCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentProduct
		fields = ['body']
		
	def create(self, validated_data):
		product = Product.objects.get(slug=self.context['product_slug'])
		return CommentProduct.objects.create(product=product, **validated_data)


class CategoryProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = CategoryProduct
		fields = '__all__'


class GalleryProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = GalleryProduct
		fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
	category = CategoryProductSerializer(source='category.title')
	comment_product = CommentSerializer(many=True)
	final_price = serializers.SerializerMethodField()
	gallery_product = GalleryProductSerializer(many=True)

	class Meta:
		model = Product
		fields = ['title', 'slug', 'category', 'final_price', 'discount', 'image',
					 'gallery_product', 'rating', 'width', 'lenght', 'weight', 'color',
					   'meterial', 'create_at', 'update_at']


	def get_total_price(self, obj):
		return obj.final_price()


class EditProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['title', 'category', 'price', 'image', 'discount', 'width', 'lenght',
					 'weight', 'color', 'meterial']



class ProductFavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductFavorite
		fields = ['id', 'user', 'product']
		read_only_fields = ['user', 'create_at']
