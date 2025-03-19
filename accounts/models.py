from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# 添加自定义用户管理器
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('邮箱是必填项')
        
        # 确保用户名和邮箱相同
        username = email
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        
        return self.create_user(username, email, password, **extra_fields)
    
    def get_by_natural_key(self, username_or_email):
        # 尝试通过电子邮件查找用户
        try:
            return self.get(email=username_or_email)
        except self.model.DoesNotExist:
            # 如果通过邮箱找不到用户，则尝试通过用户名查找
            return self.get(username=username_or_email)

# CustomUser 模型，严格按照 ER 图中的字段：
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    CustomUser model following the ER diagram fields:
    - user_id (PK)
    - role
    - username
    - password
    - email
    - linked_id
    """
    user_id = models.IntegerField(primary_key=True, db_column='user_id')
    role = models.CharField(max_length=20, db_column='role')  # 'admin', 'teacher', 'student'
    username = models.CharField(max_length=128, unique=True, db_column='username')
    password = models.CharField(max_length=128, db_column='password')
    email = models.CharField(max_length=255, db_column='email')
    linked_id = models.IntegerField(null=True, blank=True, db_column='linked_id')

    # 添加自定义管理器
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # 下面这些属性不会存入数据库，仅用于 Django 权限系统
    @property
    def is_staff(self):
        return self.role == 'admin'

    @property
    def is_superuser(self):
        return self.role == 'admin'

    @property
    def is_active(self):
        return True

    @property
    def date_joined(self):
        return timezone.now()

    def __str__(self):
        return f"{self.username} ({self.role})"


# Teacher 模型，严格按照 ER 图中的字段定义：
class Teacher(models.Model):
    """
    Teacher
    Fields:
      - Teacher_ID (PK)
      - Full_Name
      - Email
      - Phone_No
      - Title
      - Department
      - Office_Location
    """
    teacher_id = models.IntegerField(primary_key=True, db_column='Teacher_ID')
    full_name = models.CharField(max_length=255, db_column='Full_Name')
    email = models.CharField(max_length=255, db_column='Email')
    phone_no = models.CharField(max_length=15, db_column='Phone_No')
    title = models.CharField(max_length=50, db_column='Title')
    department = models.CharField(max_length=150, db_column='Department')
    office_location = models.CharField(max_length=100, db_column='Office_Location')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


# Student 模型，严格按照 ER 图中的字段定义：
class Student(models.Model):
    """
    Student
    Fields:
      - Student_ID (PK)
      - Full_Name
      - Phone_No
      - Email
      - Degree_Programme
      - Year_of_Study
      - GPA
      - Enrollment_Status
    """
    student_id = models.IntegerField(primary_key=True, db_column='Student_ID')
    full_name = models.CharField(max_length=255, db_column='Full_Name')
    phone_no = models.CharField(max_length=15, db_column='Phone_No')
    email = models.CharField(max_length=255, db_column='Email')
    degree_programme = models.CharField(max_length=150, db_column='Degree_Programme')
    year_of_study = models.IntegerField(db_column='Year_of_Study')
    gpa = models.DecimalField(max_digits=4, decimal_places=2, db_column='GPA')
    enrollment_status = models.CharField(max_length=50, db_column='Enrollment_Status')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
