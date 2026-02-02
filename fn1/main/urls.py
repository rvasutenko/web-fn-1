from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.about_page, name='about'),
    path('materials/', views.materials_page, name='materials'),
    path('aboutFn/', views.aboutFn_page, name='about'),
    path('fnmaterials/', views.fn_materials_page, name='fn_materials'),
    path('news/<int:news_id>/', views.news_detail_page, name='news_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)