from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='myapp/index.html'), name='logout'),
    path('register/', views.register, name='register'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'myapp.views.custom_404_view'