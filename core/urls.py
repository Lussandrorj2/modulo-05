from django.urls import path
from .views import (
    TarefaListCreateAPIView,
    TarefaRetrieveUpdateDestroyAPIView,
    ContagemTarefasAPIView,
)

app_name = 'core'

urlpatterns = [
    path('tarefas/', TarefaListCreateAPIView.as_view(), name='lista-tarefas'),
    path('tarefas/<int:pk>/', TarefaRetrieveUpdateDestroyAPIView.as_view(), name='detalhe-tarefa'),
    path('tarefas/contagem/', ContagemTarefasAPIView.as_view(), name='contagem-tarefas'),
    
]
