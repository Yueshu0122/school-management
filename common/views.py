from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import is_teacher
from .models import Major
from django.db import IntegrityError

@login_required
@user_passes_test(is_teacher)
@require_http_methods(["POST"])
def create_major(request):
    try:
        major = Major.objects.create(
            major_id=request.POST['major_id'],
            major_name=request.POST['major_name'],
            college_id=request.POST['college_id']
        )
        return JsonResponse({
            'status': 'success',
            'message': 'Major created successfully',
            'major': {
                'id': major.major_id,
                'name': major.major_name
            }
        })
    except IntegrityError:
        return JsonResponse({
            'status': 'error',
            'message': 'Major ID already exists'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400) 