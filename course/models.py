from django.db import models

from accounts.models import Teacher


# Create your models here.
class Course(models.Model):
    """
    Course
    Fields:
      - Course_ID (PK)
      - Course_Name
      - Credits
      - Major_ID (integer, no actual College table)
      - Teacher_ID (FK -> Teacher)
    """
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=60)
    credits = models.IntegerField()
    major_id = models.IntegerField()
    teacher = models.ForeignKey(
        'accounts.Teacher',
        on_delete=models.CASCADE,
        db_column='teacher_id',
        related_name='courses'
    )

    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.course_name