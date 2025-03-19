from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """API endpoint for announcement details page"""
        announcement = self.get_object()
        serializer = self.get_serializer(announcement)
        return Response(serializer.data)

# Web-specific views for different user roles
@login_required
def student_announcement_details(request, announcement_id):
    """View announcement details for students"""
    print(f"Student Announcement Details - ID: {announcement_id}")
    print(f"User: {request.user}")
    print(f"User Role: {request.user.role}")
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    print(f"Announcement Found: {announcement}")
    return render(request, 'student/announcements_details.html', {
        'announcement': announcement
    })

@login_required
def teacher_announcement_details(request, announcement_id):
    """View announcement details for teachers"""
    print(f"Teacher Announcement Details - ID: {announcement_id}")
    print(f"User: {request.user}")
    print(f"User Role: {request.user.role}")
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    print(f"Announcement Found: {announcement}")
    return render(request, 'teacher/announcements_details.html', {
        'announcement': announcement
    })

@login_required
def admin_announcement_details(request, announcement_id):
    """View announcement details for admins"""
    print(f"Admin Announcement Details - ID: {announcement_id}")
    print(f"User: {request.user}")
    print(f"User Role: {request.user.role}")
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    print(f"Announcement Found: {announcement}")
    return render(request, 'admin/announcement_details.html', {
        'announcement': announcement
    })
