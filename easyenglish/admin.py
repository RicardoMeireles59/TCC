from django.contrib import admin
from .models import EstudoSessao


@admin.register(EstudoSessao)
class EstudoSessaoAdmin(admin.ModelAdmin):
    list_display = ('user', 'data', 'cards_estudados', 'acertos', 'erros', 'taxa_acerto')
    list_filter = ('data', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('data',)

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações da Sessão', {
            'fields': ('data', 'cards_estudados', 'acertos', 'erros', 'duracao_minutos')
        }),
    )
