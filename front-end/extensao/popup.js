/**
 * EasyEnglish – popup.js (versão simples)
 */

document.addEventListener('DOMContentLoaded', async () => {

  const toggle      = document.getElementById('toggleActive');
  const phraseField = document.getElementById('phraseField');
  const transField  = document.getElementById('translationField');
  const deckSelect  = document.getElementById('deckSelect');
  const sendBtn     = document.getElementById('sendBtn');
  const feedback    = document.getElementById('feedback');

  // ── Tenta preencher frase com texto selecionado na página ──────────────────
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  try {
    const [result] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection()?.toString().trim() || ''
    });
    if (result?.result) phraseField.value = result.result;
  } catch {}

  // ── Estado do toggle (persistido) ─────────────────────────────────────────
  const { active } = await chrome.storage.local.get('active');
  toggle.checked = active ?? true;

  toggle.addEventListener('change', () => {
    chrome.storage.local.set({ active: toggle.checked });
  });

  // ── Cor do select quando tem valor ────────────────────────────────────────
  deckSelect.addEventListener('change', () => {
    deckSelect.classList.toggle('has-value', deckSelect.value !== '');
  });

  // ── Enviar ─────────────────────────────────────────────────────────────────
  sendBtn.addEventListener('click', async () => {
    const phrase      = phraseField.value.trim();
    const translation = transField.value.trim();
    const deck        = deckSelect.value;

    if (!phrase || !translation || !deck) {
      showFeedback('Preencha todos os campos.', 'error');
      return;
    }

    sendBtn.disabled = true;
    sendBtn.textContent = 'Enviando…';

    try {
      // ── Substitua pela sua chamada de API real: ──────────────────────────
      // await fetch('https://suaapi.com/flashcard', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ phrase, translation, deck })
      // });
      // ────────────────────────────────────────────────────────────────────

      await delay(700); // simulação — remova em produção

      showFeedback('✓ Flashcard salvo!', 'success');
      phraseField.value = '';
      transField.value  = '';
      deckSelect.value  = '';
      deckSelect.classList.remove('has-value');
    } catch {
      showFeedback('Erro ao enviar. Tente novamente.', 'error');
    } finally {
      sendBtn.disabled = false;
      sendBtn.textContent = 'Enviar';
    }
  });

  // ── Helpers ────────────────────────────────────────────────────────────────
  function showFeedback(msg, type) {
    feedback.textContent = msg;
    feedback.className   = `feedback ${type}`;
    clearTimeout(feedback._timer);
    feedback._timer = setTimeout(() => {
      feedback.className = 'feedback hidden';
    }, 3000);
  }

  function delay(ms) {
    return new Promise(r => setTimeout(r, ms));
  }
});
