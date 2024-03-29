import logging

from bson import ObjectId
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import User


def check_is_user_exists(user) -> None:
    if not user.exists():
        raise NotFound({'data': {}, 'errors': ['User not exist.']})


def check_is_user_is_active(user, has_to=True) -> None:
    if has_to:
        if user.first().is_active:
            raise serializers.ValidationError({'data': {}, 'errors': ['The user is already activated.']})
    else:
        if not user.first().is_active:
            raise serializers.ValidationError({'data': {}, 'errors': ['The user is not activated.']})


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            '_id', 'username', 'first_name', 'last_name',
            'email', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        print(attrs, self._kwargs)
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            '_id', 'username', 'first_name', 'last_name',
            'email', 'is_active', 'is_staff', 'is_superuser'
        ]



class UserRegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'data': {}, 'errors': ['The passwords must match.']})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        password=validated_data['password'])
        return user


class RestorePasswordSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(max_length=255, write_only=True)
    old_password = serializers.CharField(max_length=255, write_only=True)
    new_password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        fields = ['user_id', 'old_password', 'new_password', 'confirm_password']
        model = User

    def validate(self, attrs):
        user = User.objects.filter(_id=ObjectId(attrs['user_id']))
        auth = authenticate(
            username=user.first().username,
            password=attrs['old_password']
        )
        if not auth:
            raise serializers.ValidationError({'data': {}, 'errors': ['The current password is not correct.']})

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'data': {}, 'errors': ['The passwords must match.']})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class SendActiveLinkUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ['username']
        model = User

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username'])
        check_is_user_exists(user)
        check_is_user_is_active(user)
        return user.first()


class SendResetPwdLinkUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ['username']
        model = User

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username'])
        check_is_user_exists(user)
        check_is_user_is_active(user, False)
        return user.first()
