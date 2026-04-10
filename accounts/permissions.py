from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class IsAdmin(permissions.BasePermission):
    """Custom permission to only allow admins"""
    
    def has_permission(self, request, view):
        is_admin = request.user and request.user.role == 'admin'
        if not is_admin:
            logger.warning(f"Unauthorized admin access attempt by: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        return is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin can modify, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level permission to only allow owners or admins"""
    
    def has_object_permission(self, request, view, obj):
        # Allow admins
        if request.user.role == 'admin':
            return True
        # Allow owners
        return obj.user == request.user
