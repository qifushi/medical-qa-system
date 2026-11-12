from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='chat.html'), name='home'),
    path('api/medical/', include('medical.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 托管 Vue 前端 public/medical 下的图片等静态资源
    urlpatterns += static('/medical/', document_root=settings.BASE_DIR / 'ui' / 'public' / 'medical')
