from django.urls import path
from .views import chat_view, reset_history_view, image_upload_view, file_upload_view

urlpatterns = [
    path('chat/', chat_view, name='medical_chat'),
    path('reset_history/', reset_history_view, name='reset_history'),
    path('upload/image/', image_upload_view, name='image_upload'),
    path('upload/file/', file_upload_view, name='file_upload'),
]