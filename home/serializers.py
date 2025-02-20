from rest_framework import serializers
from .models import *



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class SliderHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderHome
        fields = '__all__'


class FooterBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterBox
        fields = '__all__'


class FooterLinkSerializer(serializers.ModelSerializer):
    footer_box = FooterBoxSerializer(many=True)
    
    class Meta:
        model = FooterLink
        fields = '__all__'


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = '__all__'


class InformationShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationShop
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
