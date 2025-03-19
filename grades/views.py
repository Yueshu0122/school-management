from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Grade
from .serializers import GradeSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from accounts.models import Student
from course.models import Course
from accounts.views import is_teacher

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

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
                {"detail": f"Error creating grade: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

@login_required
@user_passes_test(is_teacher)
def manage_course_students(request, course_id):
    course = get_object_or_404(Course, course_id=course_id, teacher_id=request.user.linked_id)
    students = Student.objects.all()
    enrolled_students = Student.objects.filter(grades__course=course)
    
    context = {
        'course': course,
        'students': students,
        'enrolled_students': enrolled_students,
    }
    return render(request, 'teacher/manage_course_students.html', context)

@login_required
@user_passes_test(is_teacher)
@require_http_methods(["POST"])
def add_student_to_course(request, course_id, student_id):
    course = get_object_or_404(Course, course_id=course_id, teacher_id=request.user.linked_id)
    student = get_object_or_404(Student, student_id=student_id)
    
    try:
        grade = Grade.objects.create(
            student=student,
            course=course,
            final_exam=0,
            assignments=0,
            regular_quiz=0,
            attendance=0,
            gpa=0
        )
        return JsonResponse({'status': 'success', 'message': 'Student added successfully'})
    except IntegrityError:
        return JsonResponse({
            'status': 'error',
            'message': 'Student is already enrolled in this course'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@user_passes_test(is_teacher)
@require_http_methods(["POST"])
def remove_student_from_course(request, course_id, student_id):
    grade = get_object_or_404(
        Grade,
        course__course_id=course_id,
        student__student_id=student_id,
        course__teacher_id=request.user.linked_id
    )
    try:
        grade.delete()
        return JsonResponse({'status': 'success', 'message': 'Student removed successfully'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@user_passes_test(is_teacher)
@require_http_methods(["POST"])
def update_student_grade(request, grade_id):
    grade = get_object_or_404(
        Grade,
        id=grade_id,
        course__teacher_id=request.user.linked_id
    )
    try:
        grade.final_exam = request.POST.get('final_exam', grade.final_exam)
        grade.assignments = request.POST.get('assignments', grade.assignments)
        grade.regular_quiz = request.POST.get('regular_quiz', grade.regular_quiz)
        grade.attendance = request.POST.get('attendance', grade.attendance)
        grade.gpa = request.POST.get('gpa', grade.gpa)
        grade.save()
        return JsonResponse({'status': 'success', 'message': 'Grades updated successfully'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@user_passes_test(is_teacher)
def view_student_grades(request, course_id, student_id):
    grade = get_object_or_404(
        Grade,
        student__student_id=student_id,
        course__course_id=course_id,
        course__teacher_id=request.user.linked_id
    )
    return JsonResponse({
        'grade_id': grade.id,
        'final_exam': float(grade.final_exam),
        'assignments': float(grade.assignments),
        'regular_quiz': float(grade.regular_quiz),
        'attendance': float(grade.attendance),
        'gpa': float(grade.gpa)
    })
