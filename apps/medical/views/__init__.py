from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings
from ..api.chat import medical_chat, reset_history, get_last_sources


@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '')
            smart_search = data.get('smart_search', False)
            deep_think = data.get('deep_think', False)
            kb_type = data.get('kb_type', None)
            if not content:
                return JsonResponse({'code': 400, 'message': 'Content is required', 'data': ''})
            
            response = medical_chat(content, smart_search, deep_think, kb_type)
            return JsonResponse({'code': 200, 'message': 'success', 'data': response, 'sources': get_last_sources()})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': str(e), 'data': ''})
    else:
        return JsonResponse({'code': 405, 'message': 'Method not allowed', 'data': ''})


@csrf_exempt
def reset_history_view(request):
    if request.method == 'POST':
        try:
            reset_history()
            return JsonResponse({'code': 200, 'message': 'success', 'data': '对话历史已重置'})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': str(e), 'data': ''})
    else:
        return JsonResponse({'code': 405, 'message': 'Method not allowed', 'data': ''})


@csrf_exempt
def image_upload_view(request):
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({'code': 400, 'message': 'No image file provided', 'data': ''})
            
            image_file = request.FILES['image']
            
            # 确保上传目录存在
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'images')
            os.makedirs(upload_dir, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(upload_dir, image_file.name)
            with open(file_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            
            # 生成文件URL
            image_url = f'/media/images/{image_file.name}'
            return JsonResponse({'code': 200, 'message': 'success', 'data': image_url})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': str(e), 'data': ''})
    else:
        return JsonResponse({'code': 405, 'message': 'Method not allowed', 'data': ''})


@csrf_exempt
def file_upload_view(request):
    if request.method == 'POST':
        try:
            if 'file' not in request.FILES:
                return JsonResponse({'code': 400, 'message': 'No file provided', 'data': ''})
            
            upload_file = request.FILES['file']
            
            # 确保上传目录存在
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'files')
            os.makedirs(upload_dir, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(upload_dir, upload_file.name)
            with open(file_path, 'wb') as f:
                for chunk in upload_file.chunks():
                    f.write(chunk)
            
            # 生成文件URL
            file_url = f'/media/files/{upload_file.name}'
            return JsonResponse({'code': 200, 'message': 'success', 'data': file_url})
        except Exception as e:
            return JsonResponse({'code': 500, 'message': str(e), 'data': ''})
    else:
        return JsonResponse({'code': 405, 'message': 'Method not allowed', 'data': ''})