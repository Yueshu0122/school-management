from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Announcement
from .serializers import AnnouncementSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only admin users can modify announcements.
    Others have read-only access.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-publish_date')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return Response(
                {"detail": f"Database integrity error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error creating announcement: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            return Response(
                {"detail": f"Database integrity error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error updating announcement: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
