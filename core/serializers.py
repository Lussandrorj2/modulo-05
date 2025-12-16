from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from .models import Tarefa
from rest_framework_simplejwt.views import TokenObtainPairView




class TarefaSerializer(serializers.ModelSerializer):
    """
    Serializer para o Model Tarefa.
    Responsabilidades:
    1. Converter Tarefa → JSON (serialização)
    2. Converter JSON → Tarefa (desserialização)
    3. Validar dados de entrada
    """
    """
    Serializer para Tarefa com segurança.
    O campo 'user' é exibido (read-only) mas NÃO aceito na entrada."""
    # 1. Mostra o username do usuário em vez do ID (read-only na saída)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Tarefa
        fields = ["id","user","titulo","descricao","concluida","prioridade","prazo","criada_em","data_conclusao","deletada",]
    
        read_only_fields = ["id", 'user', "criada_em"]

    
    def create(self, validated_data):
        
        concluida = validated_data.get("concluida", False)
        if concluida:
            validated_data["data_conclusao"] = timezone.now()
        return super().create(validated_data)

    
    def update(self, instance, validated_data):
        concluida = validated_data.get("concluida", instance.concluida)

        
        if concluida and not instance.data_conclusao:
            instance.data_conclusao = timezone.now()

        
        if not concluida:
            instance.data_conclusao = None

        return super().update(instance, validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer customizado para incluir campos extras no JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adicionar campos customizados ao payload
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token
class CustomTokenObtainPairView(TokenObtainPairView):
    """View que usa o serializer customizado."""

    serializer_class = CustomTokenObtainPairSerializer