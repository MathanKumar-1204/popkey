from rest_framework import serializers
from .models import Reservation
from lockers.models import Locker
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer for Reservation model"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    locker_number = serializers.CharField(source='locker.locker_number', read_only=True)
    locker_location = serializers.CharField(source='locker.location', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_name', 'locker', 'locker_number', 
            'locker_location', 'status', 'reserved_at', 'released_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'reserved_at', 'released_at', 'created_at', 'updated_at']


class ReservationCreateSerializer(serializers.Serializer):
    """Serializer for creating a reservation"""
    locker_id = serializers.IntegerField()
    
    def validate_locker_id(self, value):
        try:
            locker = Locker.objects.get(id=value)
        except Locker.DoesNotExist:
            raise serializers.ValidationError("Locker does not exist")
        
        if locker.status != 'available':
            raise serializers.ValidationError(f"Locker is not available. Current status: {locker.status}")
        
        # Check if user already has an active reservation
        user = self.context['request'].user
        active_reservation = Reservation.objects.filter(
            user=user,
            status='active'
        ).exists()
        
        if active_reservation:
            raise serializers.ValidationError("You already have an active reservation")
        
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        locker = Locker.objects.get(id=validated_data['locker_id'])
        
        # Use database transaction to prevent race conditions
        from django.db import transaction
        
        with transaction.atomic():
            # Lock the locker row to prevent concurrent bookings
            locker = Locker.objects.select_for_update().get(id=locker.id)
            
            if locker.status != 'available':
                raise serializers.ValidationError("Locker is no longer available")
            
            # Create reservation
            reservation = Reservation.objects.create(
                user=user,
                locker=locker,
                status='active',
                reserved_at=timezone.now()
            )
            
            # Update locker status
            locker.status = 'occupied'
            locker.save()
            
            logger.info(f"Reservation created: {reservation.id}, User: {user.username}, Locker: {locker.locker_number}")
            # Cache will expire naturally (no manual invalidation per requirements)
        
        return reservation



class ReservationReleaseSerializer(serializers.Serializer):
    """Serializer for releasing a reservation"""
    
    def update(self, instance, validated_data):
        from django.db import transaction
        
        with transaction.atomic():
            # Update reservation status
            instance.status = 'completed'
            instance.released_at = timezone.now()
            instance.save()
            
            # Update locker status back to available
            locker = instance.locker
            locker.status = 'available'
            locker.save()
            
            logger.info(f"Reservation released: {instance.id}, Locker: {locker.locker_number}")
            # Cache will expire naturally (no manual invalidation per requirements)
        
        return instance
