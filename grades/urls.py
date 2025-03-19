from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GradeViewSet, manage_course_students, add_student_to_course,
    remove_student_from_course, update_student_grade, view_student_grades
)

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('', include(router.urls)),
    path('course/<int:course_id>/students/', manage_course_students, name='manage_course_students'),
    path('course/<int:course_id>/student/<int:student_id>/add/', add_student_to_course, name='add_student_to_course'),
    path('course/<int:course_id>/student/<int:student_id>/remove/', remove_student_from_course, name='remove_student_from_course'),
    path('grade/<int:grade_id>/update/', update_student_grade, name='update_student_grade'),
    path('course/<int:course_id>/student/<int:student_id>/grades/', view_student_grades, name='view_student_grades'),
]
