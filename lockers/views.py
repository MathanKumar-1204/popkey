from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Locker
from .serializers import LockerSerializer, LockerCreateUpdateSerializer
from accounts.permissions import IsAdminOrReadOnly, IsAdmin
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class LockerListCreateView(generics.ListCreateAPIView):
    """
    GET /api/lockers/ - List all lockers
    POST /api/lockers/ - Create locker (Admin only)
    """
    queryset = Locker.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LockerCreateUpdateSerializer
        return LockerSerializer
    
    def get_queryset(self):
        queryset = Locker.objects.all()
        status_filter = self.request.query_params.get('status', None)
        location_filter = self.request.query_params.get('location', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if location_filter:
            queryset = queryset.filter(location__icontains=location_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        locker = serializer.save()
        logger.info(f"Admin {self.request.user.username} created locker: {locker.locker_number}")
        # Cache will expire naturally (no manual invalidation per requirements)


class LockerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/lockers/<id>/ - Get locker details
    PUT /api/lockers/<id>/ - Update locker (Admin only)
    DELETE /api/lockers/<id>/ - Delete locker (Admin only)
    """
    queryset = Locker.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LockerCreateUpdateSerializer
        return LockerSerializer
    
    def perform_update(self, serializer):
        old_status = serializer.instance.status
        locker = serializer.save()
        logger.info(f"Admin {self.request.user.username} updated locker: {locker.locker_number}")
        # Cache will expire naturally (no manual invalidation per requirements)
    
    def perform_destroy(self, instance):
        # Soft delete by setting status to deactivated
        instance.status = 'deactivated'
        instance.save()
        logger.info(f"Admin {self.request.user.username} deactivated locker: {instance.locker_number}")
        # Cache will expire naturally (no manual invalidation per requirements)


class AvailableLockersView(APIView):
    """
    GET /api/lockers/available/ - List available lockers (Redis cached)
    """
    permission_classes = [permissions.IsAuthenticated]
    CACHE_KEY = 'available_lockers'
    CACHE_TIMEOUT = 60  # 60 seconds
    
    def get(self, request):
        try:
            # Try to get from cache first
            cached_lockers = None
            try:
                cached_lockers = cache.get(self.CACHE_KEY)
            except Exception as e:
                logger.warning(f"Cache get failed (Redis may not be running): {str(e)}")
            
            if cached_lockers is not None:
                logger.info("Returning cached available lockers")
                return Response({
                    'count': len(cached_lockers),
                    'cached': True,
                    'results': cached_lockers
                })
            
            # If not in cache, query database
            logger.info("Cache miss - querying database for available lockers")
            available_lockers = Locker.objects.filter(status='available')
            serializer = LockerSerializer(available_lockers, many=True)
            
            # Store in cache
            try:
                cache.set(self.CACHE_KEY, serializer.data, timeout=self.CACHE_TIMEOUT)
            except Exception as e:
                logger.warning(f"Cache set failed (Redis may not be running): {str(e)}")
            
            return Response({
                'count': len(serializer.data),
                'cached': False,
                'results': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Error fetching available lockers: {str(e)}")
            return Response(
                {'error': 'Failed to fetch available lockers'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
