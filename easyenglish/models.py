from django.db import models
from django.contrib.auth.models import User


class EstudoSessao(models.Model):
    """Modelo para registrar sessões de estudo do usuário."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estudo_sessoes')
    data = models.DateTimeField(auto_now_add=True)
    cards_estudados = models.IntegerField(default=0)
    acertos = models.IntegerField(default=0)
    erros = models.IntegerField(default=0)
    duracao_minutos = models.IntegerField(default=0)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Sessão de Estudo'
        verbose_name_plural = 'Sessões de Estudo'

    def __str__(self):
        return f"{self.user.username} - {self.data.strftime('%d/%m/%Y %H:%M')}"

    @property
    def taxa_acerto(self):
        """Calcula a porcentagem de acertos."""
        if self.cards_estudados == 0:
            return 0
        return round((self.acertos / self.cards_estudados) * 100)
