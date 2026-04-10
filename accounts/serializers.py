from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'name']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},  # Role can only be set by admin
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        logger.info(f"New user registered: {user.username}")
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError("Both username and password are required")
        
        user = authenticate(username=username, password=password)
        
        if not user:
            logger.warning(f"Failed login attempt for username: {username}")
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {username}")
            raise serializers.ValidationError("User account is disabled")
        
        logger.info(f"User logged in: {username}")
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']