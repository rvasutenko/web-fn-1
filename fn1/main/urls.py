from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about_page, name='about'),
    path('materials/', views.materials_page, name='materials')
]

'''if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''