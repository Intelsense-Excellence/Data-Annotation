from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from app_main import views

urlpatterns = [
    path('', views.home, name='home', )
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)