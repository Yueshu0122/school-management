from django.urls import path
from .views import (
    login_view, register_view, logout_view, index_view,
    teacher_dashboard, manage_grades, update_grade,
    manage_courses, create_course, view_announcements,
    student_dashboard, student_grades, student_announcements,
    admin_dashboard, admin_announcements, create_announcement,
    edit_announcement, delete_announcement
)

urlpatterns = [
    # Web 视图
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', index_view, name='index'),
    
    # Teacher views
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/grades/<int:course_id>/', manage_grades, name='manage_grades'),
    path('teacher/grade/update/<int:grade_id>/', update_grade, name='update_grade'),
    path('teacher/courses/', manage_courses, name='manage_courses'),
    path('teacher/course/create/', create_course, name='create_course'),
    path('teacher/announcements/', view_announcements, name='teacher_announcements'),
    
    # Student views
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/grades/', student_grades, name='student_grades'),
    path('student/announcements/', student_announcements, name='student_announcements'),
    
    # Admin views
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/announcements/', admin_announcements, name='admin_announcements'),
    path('admin/announcement/create/', create_announcement, name='create_announcement'),
    path('admin/announcement/<int:announcement_id>/edit/', edit_announcement, name='edit_announcement'),
    path('admin/announcement/<int:announcement_id>/delete/', delete_announcement, name='delete_announcement'),
]
