# common/models.py
from django.db import models

class Major(models.Model):
    """
    Major
    Fields:
      - Major_ID (PK)
      - Major_Name (varchar(100))
      - College_ID (integer, but no actual College table in the ER diagram)
    """
    major_id = models.IntegerField(primary_key=True)
    major_name = models.CharField(max_length=100)
    college_id = models.IntegerField()

    class Meta:
        db_table = 'common'
        verbose_name = 'Major'
        verbose_name_plural = 'Majors'

    def __str__(self):
        return self.major_name
