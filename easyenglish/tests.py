from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from extensao.models import Flashcard

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


class HistoricoWiringTestCase(TestCase):
    """Estudo registra sessões reais e a API de histórico as devolve."""

    def setUp(self):
        self.user = User.objects.create_user(username='estudante', password='senha12345')
        self.client.force_login(self.user)
        self.card = Flashcard.objects.create(user=self.user, phrase='hello', translation='olá')

    def test_estudar_registra_sessao_diaria(self):
        url = reverse('update_flashcard_status', kwargs={'flashcard_id': self.card.id})
        self.client.post(url, {'status': 'reviewed', 'origem': 'study'})
        self.client.post(url, {'status': 'new', 'origem': 'study'})

        sessoes = EstudoSessao.objects.filter(user=self.user)
        self.assertEqual(sessoes.count(), 1)  # agrega no mesmo dia
        sessao = sessoes.first()
        self.assertEqual(sessao.cards_estudados, 2)
        self.assertEqual(sessao.acertos, 1)
        self.assertEqual(sessao.erros, 1)

    def test_atualizar_fora_do_estudo_nao_registra_sessao(self):
        url = reverse('update_flashcard_status', kwargs={'flashcard_id': self.card.id})
        self.client.post(url, {'status': 'reviewed'})  # sem origem=study
        self.assertEqual(EstudoSessao.objects.filter(user=self.user).count(), 0)

    def test_paginas_web_renderizam(self):
        for name in ('dashboard', 'flashcards_list', 'study', 'historico'):
            with self.subTest(page=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 200)

    def test_api_historico_retorna_sessoes_reais(self):
        EstudoSessao.objects.create(user=self.user, cards_estudados=5, acertos=4, erros=1, duracao_minutos=7)
        resp = self.client.get(reverse('historico_api'))
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertTrue(payload['success'])
        self.assertEqual(len(payload['data']), 1)
        entry = payload['data'][0]
        self.assertEqual(entry['cardsStudied'], 5)
        self.assertEqual(entry['correct'], 4)
        self.assertEqual(entry['incorrect'], 1)
        self.assertEqual(entry['duration'], '7 min')
