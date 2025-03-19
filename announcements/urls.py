from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnnouncementViewSet, 
    student_announcement_details, 
    teacher_announcement_details, 
    admin_announcement_details
)

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
    # API endpoint for announcement details
    path('announcement/<int:pk>/', AnnouncementViewSet.as_view({'get': 'details'}), name='announcement_details'),
    
    # Web-specific routes for announcement details
    path('student/announcement/<int:announcement_id>/', student_announcement_details, name='student_announcement_details'),
    path('teacher/announcement/<int:announcement_id>/', teacher_announcement_details, name='teacher_announcement_details'),
    path('admin/announcement/<int:announcement_id>/', admin_announcement_details, name='admin_announcement_details'),
]
