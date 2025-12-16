import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from .models import Tarefa
from .serializers import TarefaSerializer, CustomTokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

logger = logging.getLogger(__name__)

class TarefaListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tarefa.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TarefaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tarefa.objects.filter(user=self.request.user)

class ContagemTarefasAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = Tarefa.objects.filter(user=request.user).count()
        concluidas = Tarefa.objects.filter(
            user=request.user, concluida=True
        ).count()
        pendentes = total - concluidas

        return Response(
            {
                "total": total,
                "concluidas": concluidas,
                "pendentes": pendentes,
            },
            status=status.HTTP_200_OK,
        )

class DuplicarTarefaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        tarefa = get_object_or_404(Tarefa, pk=pk, user=request.user)

        tarefa.pk = None
        tarefa.concluida = False
        tarefa.save()

        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logout realizado com sucesso."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"detail": "Token inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
