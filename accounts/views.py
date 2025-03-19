from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import Teacher, Student, CustomUser  # 请确保 Teacher 和 Student 模型已正确定义
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import IntegrityError
import random
from django.http import HttpResponse, JsonResponse
from grades.models import Grade
from course.models import Course
from common.models import Major
from announcements.models import Announcement
from django.views.decorators.http import require_http_methods
from django.utils import timezone

User = get_user_model()

# HTML Views for traditional Django authentication
def login_view(request):
    # 添加调试信息
    print("login_view 被调用")
    
    # 如果用户已经登录，根据角色重定向到相应页面
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect('teacher_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('index')
        
    if request.method == 'POST':
        email = request.POST.get('email')  # 改为使用email字段
        password = request.POST.get('password')
        
        # 尝试通过邮箱查找用户
        try:
            user = CustomUser.objects.get(email=email)
            username = user.username
            # 使用authenticate验证密码
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome，{user.username}！')
                
                # 根据用户角色重定向到不同页面
                if user.role == 'teacher':
                    return redirect('teacher_dashboard')
                elif user.role == 'student':
                    return redirect('student_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('index')
            else:
                messages.error(request, '邮箱或密码不正确。')
        except CustomUser.DoesNotExist:
            messages.error(request, '该邮箱未注册。')
            
    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        # 获取基本信息
        full_name = request.POST.get('full_name')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        # 将邮箱作为用户名
        username = email
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        
        # 检查密码是否匹配
        if password != confirm_password:
            messages.error(request, '密码不匹配')
            return redirect('register')
            
        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            messages.error(request, '该邮箱已注册')
            return redirect('register')
        
        try:
            # 生成新的用户ID
            latest_user = User.objects.order_by('-user_id').first()
            new_user_id = 1 if latest_user is None else latest_user.user_id + 1
            
            if role == 'student':
                # 获取学生额外信息
                degree_programme = request.POST.get('degree_programme')
                year_of_study = request.POST.get('year_of_study')
                
                # 生成新学生ID
                latest_student = Student.objects.order_by('-student_id').first()
                new_student_id = 1 if latest_student is None else latest_student.student_id + 1
                
                # 创建学生记录
                student = Student.objects.create(
                    student_id=new_student_id,
                    full_name=full_name,  # 保存全名
                    phone_no=phone_no,
                    email=email,
                    degree_programme=degree_programme,
                    year_of_study=year_of_study,
                    gpa=0.0,  # 默认值
                    enrollment_status='Active'  # 默认值
                )
                
                # 创建用户记录与学生关联，使用邮箱作为用户名
                user = User.objects.create_user(
                    user_id=new_user_id,
                    username=username,  # 使用邮箱作为用户名
                    email=email,
                    password=password,
                    role='student',
                    linked_id=student.student_id
                )
                
            elif role == 'teacher':
                # 获取教师额外信息
                title = request.POST.get('title')
                department = request.POST.get('department')
                office_location = request.POST.get('office_location')
                
                # 生成新教师ID
                latest_teacher = Teacher.objects.order_by('-teacher_id').first()
                new_teacher_id = 1 if latest_teacher is None else latest_teacher.teacher_id + 1
                
                # 创建教师记录
                teacher = Teacher.objects.create(
                    teacher_id=new_teacher_id,
                    full_name=full_name,  # 保存全名
                    email=email,
                    phone_no=phone_no,
                    title=title,
                    department=department,
                    office_location=office_location
                )
                
                # 创建用户记录与教师关联，使用邮箱作为用户名
                user = User.objects.create_user(
                    user_id=new_user_id,
                    username=username,  # 使用邮箱作为用户名
                    email=email,
                    password=password,
                    role='teacher',
                    linked_id=teacher.teacher_id
                )
            
            messages.success(request, '注册成功，请登录')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'注册失败: {str(e)}')
            
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def index_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'index.html', context)

# REST API Views
class RegisterView(APIView):
    """
    用户注册视图。根据传入数据创建用户，并根据角色验证 linked_id 是否存在于 Teacher 或 Student 表中，
    同时将用户添加到相应的组中，并捕获数据库异常返回友好提示。
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 获取 ER 图中的必填字段
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        role = request.data.get('role', 'student')
        linked_id = request.data.get('linked_id', None)

        # 基本字段验证
        if not user_id or not username or not password or not email:
            return Response({"detail": "Missing required fields."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(user_id=user_id).exists():
            return Response({"detail": "User ID already exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 根据角色验证 linked_id 是否存在于 Teacher 或 Student 表中
        if role == 'teacher':
            if linked_id is None:
                return Response({"detail": "Linked ID is required for teacher role."},
                                status=status.HTTP_400_BAD_REQUEST)
            if not Teacher.objects.filter(teacher_id=linked_id).exists():
                return Response({"detail": "Teacher with provided Linked ID does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        elif role == 'student':
            if linked_id is None:
                return Response({"detail": "Linked ID is required for student role."},
                                status=status.HTTP_400_BAD_REQUEST)
            if not Student.objects.filter(student_id=linked_id).exists():
                return Response({"detail": "Student with provided Linked ID does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        # 对于 admin 角色，linked_id 可选或不需要验证

        # 尝试创建用户，并捕获数据库异常
        try:
            user = User.objects.create(
                user_id=user_id,
                username=username,
                email=email,
                role=role,
                linked_id=linked_id
            )
        except IntegrityError as e:
            return Response({"detail": f"Database integrity error: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error creating user: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 根据角色将用户添加到对应组中，并捕获异常
        try:
            if role == 'teacher':
                group, _ = Group.objects.get_or_create(name='Teacher')
                user.groups.add(group)
            elif role == 'student':
                group, _ = Group.objects.get_or_create(name='Student')
                user.groups.add(group)
            elif role == 'admin':
                group, _ = Group.objects.get_or_create(name='Admin')
                user.groups.add(group)
        except Exception as e:
            return Response({"detail": f"Error assigning group: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "User registered successfully."},
                        status=status.HTTP_201_CREATED)

class AdminOnlyView(APIView):
    """
    仅限管理员访问的视图。只有 role 为 'admin' 的用户才能访问该接口。
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({"detail": "You are not authorized."},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Hello, Admin!"}, status=status.HTTP_200_OK)

def redirect_to_login(request):
    return redirect('login')

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = Teacher.objects.get(teacher_id=request.user.linked_id)
    courses = Course.objects.filter(teacher_id=teacher.teacher_id)
    announcements = Announcement.objects.all().order_by('-publish_date')[:5]
    
    context = {
        'teacher': teacher,
        'courses': courses,
        'announcements': announcements,
    }
    return render(request, 'teacher/dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def manage_grades(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    grades = Grade.objects.filter(course=course)
    
    context = {
        'course': course,
        'grades': grades,
    }
    return render(request, 'teacher/manage_grades.html', context)

@login_required
@user_passes_test(is_teacher)
@require_http_methods(["POST"])
def update_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    try:
        grade.final_exam = request.POST.get('final_exam', grade.final_exam)
        grade.assignments = request.POST.get('assignments', grade.assignments)
        grade.regular_quiz = request.POST.get('regular_quiz', grade.regular_quiz)
        grade.attendance = request.POST.get('attendance', grade.attendance)
        grade.gpa = request.POST.get('gpa', grade.gpa)
        grade.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@user_passes_test(is_teacher)
def manage_courses(request):
    teacher = Teacher.objects.get(teacher_id=request.user.linked_id)
    courses = Course.objects.filter(teacher_id=teacher.teacher_id)
    majors = Major.objects.all()
    
    context = {
        'courses': courses,
        'majors': majors,
    }
    return render(request, 'teacher/manage_courses.html', context)

@login_required
@user_passes_test(is_teacher)
@require_http_methods(["POST"])
def create_course(request):
    try:
        course = Course.objects.create(
            course_id=request.POST['course_id'],
            course_name=request.POST['course_name'],
            credits=request.POST['credits'],
            major_id=request.POST['major_id'],
            teacher_id=request.user.linked_id
        )
        return JsonResponse({'status': 'success', 'course_id': course.course_id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@user_passes_test(is_teacher)
def view_announcements(request):
    announcements = Announcement.objects.all().order_by('-publish_date')
    return render(request, 'teacher/announcements.html', {'announcements': announcements})

def is_student(user):
    return user.is_authenticated and user.role == 'student'

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = Student.objects.get(student_id=request.user.linked_id)
    grades = Grade.objects.filter(student=student)
    announcements = Announcement.objects.all().order_by('-publish_date')[:5]
    
    context = {
        'student': student,
        'grades': grades,
        'announcements': announcements,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
@user_passes_test(is_student)
def student_grades(request):
    student = Student.objects.get(student_id=request.user.linked_id)
    grades = Grade.objects.filter(student=student).select_related('course')
    
    context = {
        'student': student,
        'grades': grades,
    }
    return render(request, 'student/grades.html', context)

@login_required
@user_passes_test(is_student)
def student_announcements(request):
    announcements = Announcement.objects.all().order_by('-publish_date')
    return render(request, 'student/announcements.html', {'announcements': announcements})

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # 使用 select_related 获取相关的作者信息，并限制最近5条公告
    announcements = Announcement.objects.select_related('author').order_by('-publish_date')[:5]
    context = {
        'announcements': announcements,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_announcements(request):
    # 使用 select_related 获取相关的作者信息
    announcements = Announcement.objects.select_related('author').order_by('-publish_date')
    return render(request, 'admin/announcements.html', {'announcements': announcements})

@login_required
@user_passes_test(is_admin)
def create_announcement(request):
    if request.method == 'POST':
        try:
            # 验证必填字段
            title = request.POST.get('title')
            content = request.POST.get('content')
            
            if not title or not content:
                messages.error(request, 'Title and content are required.')
                return render(request, 'admin/create_announcement.html')
            
            # 生成新的 announcement_id
            last_announcement = Announcement.objects.order_by('-announcement_id').first()
            new_id = (last_announcement.announcement_id + 1) if last_announcement else 1
            
            # Create Announcement
            announcement = Announcement.objects.create(
                announcement_id=new_id,
                title=title,
                content=content,
                author=request.user,
                publish_date=timezone.now()  # 添加发布时间
            )
            messages.success(request, 'Announcement created successfully.')
            return redirect('admin_announcements')
        except Exception as e:
            messages.error(request, f'Error creating announcement: {str(e)}')
            return render(request, 'admin/create_announcement.html')
    
    return render(request, 'admin/create_announcement.html')

@login_required
@user_passes_test(is_admin)
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    
    if request.method == 'POST':
        try:
            announcement.title = request.POST['title']
            announcement.content = request.POST['content']
            announcement.save()
            messages.success(request, 'Announcement updated successfully.')
            return redirect('admin_announcements')
        except Exception as e:
            messages.error(request, f'Error updating announcement: {str(e)}')
    
    return render(request, 'admin/edit_announcement.html', {'announcement': announcement})

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    try:
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting announcement: {str(e)}')
    return redirect('admin_announcements')

# 学生查看公告详情
@login_required
@user_passes_test(is_student)
def student_announcement_details(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    return render(request, 'student/announcement_details.html', {'announcement': announcement})

# 管理员查看公告详情
@login_required
@user_passes_test(is_admin)
def admin_announcement_details(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    return render(request, 'admin/announcement_details.html', {'announcement': announcement})
