from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# On importe les vues directement ici pour simplifier, ou via un urls.py dans website
from website import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('boutique/', views.boutique, name='boutique'),
    path('inscription/<int:atelier_id>/', views.inscription_atelier, name='inscription'),
    
    # Login/Logout natif Django
    path('accounts/login/', auth_views.LoginView.as_view(template_name='website/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)