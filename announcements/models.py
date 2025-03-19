from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # 获取自定义用户模型

class Announcement(models.Model):
    """
    Announcement model following the ER diagram:
    - Announcement_ID (PK)
    - Title
    - Content
    - Author_ID (FK -> CustomUser)
    - Publish_Date
    """
    announcement_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='author_id',
        related_name='announcements'
    )
    publish_date = models.DateTimeField()

    class Meta:
        db_table = 'announcement'
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title
