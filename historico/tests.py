from django.test import TestCase
from django.contrib.auth.models import User
from .models import EstudoSessao


class EstudoSessaoTestCase(TestCase):
    """Testes para o modelo EstudoSessao."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_criar_estudo_sessao(self):
        """Testa a criação de uma sessão de estudo."""
        sessao = EstudoSessao.objects.create(
            user=self.user,
            cards_estudados=15,
            acertos=12,
            erros=3,
            duracao_minutos=12
        )
        
        self.assertEqual(sessao.user, self.user)
        self.assertEqual(sessao.cards_estudados, 15)
        self.assertEqual(sessao.taxa_acerto, 80)
    
    def test_taxa_acerto_calculo(self):
        """Testa o cálculo da taxa de acerto."""
        sessao = EstudoSessao.objects.create(
            user=self.user,
            cards_estudados=10,
            acertos=7,
            erros=3,
            duracao_minutos=8
        )
        
        self.assertEqual(sessao.taxa_acerto, 70)
    
    def test_taxa_acerto_zero_cards(self):
        """Testa taxa de acerto quando não há cards estudados."""
        sessao = EstudoSessao.objects.create(
            user=self.user,
            cards_estudados=0,
            acertos=0,
            erros=0,
            duracao_minutos=0
        )
        
        self.assertEqual(sessao.taxa_acerto, 0)
