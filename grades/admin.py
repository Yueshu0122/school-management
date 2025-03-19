from django.contrib import admin
from .models import Course, Grade

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'course_name', 'credits', 'major_id']
    search_fields = ['course_id', 'course_name']

class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'final_exam', 'assignments', 'gpa', 'regular_quiz', 'attendance']
    search_fields = ['student__full_name', 'course__course_name']

admin.site.register(Course, CourseAdmin)
admin.site.register(Grade, GradeAdmin)
