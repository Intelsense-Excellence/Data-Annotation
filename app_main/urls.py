from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from app_main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bad-audio', views.BadAudio, name='bad-audio'),
    path('dashboard', views.Dashboard, name='dashboard')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
