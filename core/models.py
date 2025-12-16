from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


"""
Model para representar uma tarefa de usuário.
Cada tarefa tem:
- Um dono (user)
- Um título
- Um status de conclusão
- Data de criação automática
"""


class Tarefa(models.Model):
    # Exercico 1 Apostila 2
    PRIORIDADE_CHOICES = [
        ("baixa", "Baixa"),
        ("media", "Média"),
        ("alta", "Alta"),
    ]
    # ForeignKey: Relacionamento Many-to-One
    # Cada Tarefa pertence a UM usuário
    # Um usuário pode ter VÁRIAS tarefas
    # on_delete=CASCADE: Se o usuário for deletado, suas tarefas também são
    """Model de Tarefa com segurança. O campo 'user' é OBRIGATÓRIO."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tarefas", verbose_name="Usuário"
    )

    # CharField: Campo de texto com limite
    titulo = models.CharField(max_length=200, verbose_name="Título")
    # TextField: DO EXERCICIO 1
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    # BooleanField: Campo verdadeiro/falso
    concluida = models.BooleanField(default=False, verbose_name="Concluída")
    # DateTimeField: Data e hora
    # auto_now_add=True: Preenche automaticamente na criação
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")

    # Exercicio 1 Apostila 2
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default="media",
    )
    prazo = models.DateField(null=True, blank=True)
    # exercico 1 apostila 3
    data_conclusao = models.DateTimeField(null=True, blank=True)
    # exercico 1 apostila 3
    deletada = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ["-criada_em"]

        def __str__(self):
            return f"{self.titulo} ({'✓' if self.concluida else '✗'})"

    def clean(self):
        hoje = timezone.now().date()

        if self.prazo and self.prazo < hoje:
            raise ValidationError("O prazo não pode ser no passado.")

        if not self.concluida and not self.prazo:
            raise ValidationError(
                "O prazo é obrigatório quando a tarefa não está concluída."
            )