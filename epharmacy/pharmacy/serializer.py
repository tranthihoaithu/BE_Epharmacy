from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Medicine, User, Order, Cart


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'last_name', 'first_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        return user


class MedicineSerializer(ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
