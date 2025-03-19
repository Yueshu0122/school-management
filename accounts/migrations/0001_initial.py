# Generated by Django 5.1.7 on 2025-03-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(db_column='Student_ID', primary_key=True, serialize=False)),
                ('full_name', models.CharField(db_column='Full_Name', max_length=255)),
                ('phone_no', models.CharField(db_column='Phone_No', max_length=15)),
                ('email', models.CharField(db_column='Email', max_length=255)),
                ('degree_programme', models.CharField(db_column='Degree_Programme', max_length=150)),
                ('year_of_study', models.IntegerField(db_column='Year_of_Study')),
                ('gpa', models.DecimalField(db_column='GPA', decimal_places=2, max_digits=4)),
                ('enrollment_status', models.CharField(db_column='Enrollment_Status', max_length=50)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.IntegerField(db_column='Teacher_ID', primary_key=True, serialize=False)),
                ('full_name', models.CharField(db_column='Full_Name', max_length=255)),
                ('email', models.CharField(db_column='Email', max_length=255)),
                ('phone_no', models.CharField(db_column='Phone_No', max_length=15)),
                ('title', models.CharField(db_column='Title', max_length=50)),
                ('department', models.CharField(db_column='Department', max_length=150)),
                ('office_location', models.CharField(db_column='Office_Location', max_length=100)),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'db_table': 'Teacher',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.IntegerField(db_column='user_id', primary_key=True, serialize=False)),
                ('role', models.CharField(db_column='role', max_length=20)),
                ('username', models.CharField(db_column='username', max_length=128, unique=True)),
                ('password', models.CharField(db_column='password', max_length=128)),
                ('email', models.CharField(db_column='email', max_length=255)),
                ('linked_id', models.IntegerField(blank=True, db_column='linked_id', null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
