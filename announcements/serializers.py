from rest_framework import serializers
from .models import Announcement
from django.utils import timezone

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['announcement_id', 'title', 'content', 'author', 'publish_date']

    ## Validate the announcement title: It should not be empty and its length should not exceed 200 characters (consistent with the database field definition).
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Title must not exceed 200 characters.")
        return value

    # # Validate the announcement content: It should not be empty.
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    # Validate the publication time: It should not be later than the current time (future dates are not allowed).
    def validate_publish_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Publish date cannot be in the future.")
        return value

    def validate(self, data):
        # If cross-field validation is needed, it can be added here.
        return data
