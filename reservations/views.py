from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reservation
from .serializers import (
    ReservationSerializer, 
    ReservationCreateSerializer,
    ReservationReleaseSerializer
)
from accounts.permissions import IsOwnerOrAdmin, IsAdmin
import logging

logger = logging.getLogger(__name__)


class ReservationListCreateView(generics.ListCreateAPIView):
    """
    GET /api/reservations/ - List reservations (User: own, Admin: all)
    POST /api/reservations/ - Create reservation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReservationCreateSerializer
        return ReservationSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin can see all reservations
        if user.role == 'admin':
            return Reservation.objects.all()
        
        # Regular users can only see their own reservations
        return Reservation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        reservation = serializer.save()
        logger.info(f"Reservation created by {self.request.user.username}: {reservation.id}")


class ReservationDetailView(generics.RetrieveAPIView):
    """
    GET /api/reservations/<id>/ - Get reservation details
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    queryset = Reservation.objects.all()


class ReservationReleaseView(APIView):
    """
    PUT /api/reservations/<id>/release/ - Release locker (cancel reservation)
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def put(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
            
            # Check permissions
            if request.user.role != 'admin' and reservation.user != request.user:
                logger.warning(f"Unauthorized release attempt by {request.user.username}")
                return Response(
                    {'error': 'You do not have permission to release this reservation'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if reservation.status != 'active':
                return Response(
                    {'error': f'Reservation is not active. Current status: {reservation.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Release the reservation
            serializer = ReservationReleaseSerializer(
                reservation,
                data={},
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.update(reservation, {})
                return Response({
                    'message': 'Locker released successfully',
                    'reservation': ReservationSerializer(reservation).data
                })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Reservation.DoesNotExist:
            logger.warning(f"Reservation not found: {pk}")
            return Response(
                {'error': 'Reservation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error releasing reservation {pk}: {str(e)}")
            return Response(
                {'error': 'Failed to release locker'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
