from rest_framework import serializers
from .models import Announcement
from django.utils import timezone

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['announcement_id', 'title', 'content', 'author', 'publish_date']

    # 校验公告标题：不能为空且长度不能超过200个字符（与数据库字段定义保持一致）
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Title must not exceed 200 characters.")
        return value

    # 校验公告内容：不能为空
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    # 校验发布时间：不能晚于当前时间（不允许将来时间）
    def validate_publish_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Publish date cannot be in the future.")
        return value

    def validate(self, data):
        # 如果需要做跨字段验证，可以在这里添加
        return data
