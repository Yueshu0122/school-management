# Generated by Django 5.1.7 on 2025-03-19 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='college_id',
            new_name='major_id',
        ),
    ]
