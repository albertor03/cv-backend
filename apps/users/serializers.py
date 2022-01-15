from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            '_id', 'username', 'first_name', 'last_name',
            'email', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'created_at', 'updated_at'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('The passwords must match.')

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        password=validated_data['password'])
        return user
