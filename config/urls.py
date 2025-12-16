"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import (TarefaListCreateAPIView,TarefaRetrieveUpdateDestroyAPIView,LogoutView,CustomTokenObtainPairView,)
 # Login (obter access e refresh tokens) # Renovar token
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
# Admin do Django
path('admin/', admin.site.urls),
# URLs do app core (prefixo: /api/)
path('api/', include('core.urls')),
# JWT: Endpoints de autenticação
path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
path('api/token/',CustomTokenObtainPairView.as_view(), # ← View customizada
 name='token_obtain_pair'),
path('tarefas/', TarefaListCreateAPIView.as_view(), name='tarefa-list-create'),
path('tarefas/<int:pk>/', TarefaRetrieveUpdateDestroyAPIView.as_view(), name='tarefa-detail'),
path('logout/', LogoutView.as_view(), name='logout'), # ← Novo endpoint
# App core
path('api/', include('core.urls')),

]