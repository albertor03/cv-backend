from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return {
            '_id': str(instance['_id']),
            'username': instance['username'],
            'email': instance['email'],
            'first_name': instance['first_name'],
            'last_name': instance['last_name'],
            'is_active': instance['is_active'],
            'last_login': instance['last_login'],
            'created_at': instance['created_at'],
            'updated_at': instance['updated_at'],
        }


class UserRegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']

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


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('_id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'created_at',
                  'updated_at')
