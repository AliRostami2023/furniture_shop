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
	image = serializers.SerializerMethodField()
	
	class Meta:
		model = CategoryProduct
		fields = '__all__'

	def get_image(self, obj):
		if isinstance(obj.image, Image):
			return obj.image.image.url if obj.image.image else None
		return None


class GalleryProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = GalleryProduct
		fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer()
    comment_product = CommentSerializer(many=True)
    final_price = serializers.SerializerMethodField()
    product_image = GalleryProductSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'title', 'slug', 'category', 'final_price', 'discount', 'image',
            'product_image', 'rating', 'width', 'lenght', 'weight', 'color',
            'meterial', 'comment_product', 'create_at', 'update_at'
        ]

    def get_image(self, obj):
        if isinstance(obj.image, Image):
            return obj.image.image.url if obj.image.image else None
        return None

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
