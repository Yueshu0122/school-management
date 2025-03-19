# grades/models.py
from django.db import models
from accounts.models import Teacher, Student
from course.models import Course
class Grade(models.Model):
    """
    Grade
    Fields:
      - Student_ID (PK, FK)
      - Course_ID (PK, FK)
      - Final_Exam
      - Assignments
      - GPA
      - Regular_Quiz
      - Attendance
    """
    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE,
        db_column='student_id',
        related_name='grades',

    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        db_column='course_id',
        related_name='grades',

    )
    final_exam = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    assignments = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    regular_quiz = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attendance = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'grade'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        # If you want a composite primary key across (student, course):
        unique_together = (('student', 'course'),)


