from rest_framework import serializers
from .models import Locker
import logging

logger = logging.getLogger(__name__)


class LockerSerializer(serializers.ModelSerializer):
    """Serializer for Locker model"""
    
    class Meta:
        model = Locker
        fields = ['id', 'locker_number', 'location', 'status', 'size', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_locker_number(self, value):
        """Ensure locker number is unique"""
        if Locker.objects.filter(locker_number=value).exists():
            raise serializers.ValidationError("Locker number already exists")
        return value


class LockerCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating lockers (Admin only)"""
    
    class Meta:
        model = Locker
        fields = ['locker_number', 'location', 'status', 'size']
    
    def validate(self, data):
        if self.instance is None:  # Creating new locker
            if Locker.objects.filter(locker_number=data.get('locker_number')).exists():
                raise serializers.ValidationError({
                    'locker_number': 'Locker number already exists'
                })
        return data
    
    def create(self, validated_data):
        locker = Locker.objects.create(**validated_data)
        logger.info(f"Locker created: {locker.locker_number}")
        return locker
    
    def update(self, instance, validated_data):
        old_status = instance.status
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"Locker updated: {instance.locker_number}, Status: {old_status} -> {instance.status}")
        return instance
