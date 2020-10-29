from product.models import User, Product
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['id','firstname', 'lastname', 'mobile', 'birthdate', 'city', 'email', 'products']


class ProductSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(many=False, read_only=True)
    # user_id_firstname = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'user_id', 'product_name', 'product_type']


class CustomUserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id','firstname', 'lastname', 'mobile', 'birthdate', 'city', 'email', 'products']
