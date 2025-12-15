from django.urls import path
from .views import ListaTarefasAPIView
from .views import LogoutView, TarefaListCreateAPIView, TarefaRetrieveUpdateDestroyAPIView

app_name = 'core'
urlpatterns = [
    path('tarefas/', ListaTarefasAPIView.as_view(), name='lista-tarefas'),
    path('tarefas/<int:pk>/', TarefaRetrieveUpdateDestroyAPIView.as_view(), name='tarefa-detail'),
    path('logout/', LogoutView.as_view(), name='logout'), # ← Novo endpoint
]