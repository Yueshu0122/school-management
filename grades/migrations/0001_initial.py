# Generated by Django 5.1.7 on 2025-03-06 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_exam', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('assignments', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('gpa', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('regular_quiz', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('attendance', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('course', models.ForeignKey(db_column='course_id', on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='course.course')),
                ('student', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='accounts.student')),
            ],
            options={
                'verbose_name': 'Grade',
                'verbose_name_plural': 'Grades',
                'db_table': 'grade',
            },
        ),
    ]
