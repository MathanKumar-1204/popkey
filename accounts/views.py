from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
import logging

logger = logging.getLogger(__name__)


# 📖 API Root Documentation
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    """API Root - Smart Locker System REST API"""
    return Response({
        'message': 'Smart Locker System REST API',
        'endpoints': {
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'token_refresh': '/api/auth/token/refresh/',
                'profile': '/api/auth/profile/',
            },
            'lockers': {
                'list_create': '/api/lockers/',
                'detail': '/api/lockers/{id}/',
                'available': '/api/lockers/available/',
            },
            'reservations': {
                'list_create': '/api/reservations/',
                'detail': '/api/reservations/{id}/',
                'release': '/api/reservations/{id}/release/',
            },
            'admin': '/admin/',
        },
        'documentation': 'All endpoints require authentication except register, login, and token_refresh',
    })


# 📝 Register
class RegisterView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"User registered successfully: {user.username}")
                return Response({
                    "message": "User created successfully",
                    "user": UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            logger.warning(f"Registration failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {"error": "Registration failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 🔑 Login
class LoginView(APIView):
    """User login endpoint with JWT"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"User logged in: {user.username}")
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {"error": "Login failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 🔄 Token Refresh
class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view with logging"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            logger.info("Token refreshed successfully")
            return response
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return Response(
                {"error": "Token refresh failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


# 👤 User Profile
class UserProfileView(APIView):
    """Get current user profile"""
    
    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching user profile: {str(e)}")
            return Response(
                {"error": "Failed to fetch profile"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )