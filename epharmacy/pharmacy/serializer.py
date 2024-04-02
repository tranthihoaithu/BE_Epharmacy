from rest_framework.serializers import ModelSerializer
from .models import Medicine, User


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



class MedicineSerializer(ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'