from django.contrib import admin
from .models import Major

class MajorAdmin(admin.ModelAdmin):
    list_display = ['major_id', 'major_name', 'college_id']
    search_fields = ['major_id', 'major_name']

admin.site.register(Major, MajorAdmin)
