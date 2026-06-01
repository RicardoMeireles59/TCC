// EasyEnglish – popup.js
// Popup serve apenas para inserção manual de flashcards.
// A captura de legendas ocorre automaticamente em background.

const API_BASE = 'http://localhost:8000/extensao';

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

  // ── Enviar flashcard manual ────────────────────────────────────────────────
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
      const res = await fetch(`${API_BASE}/flashcards/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phrase, translation, deck }),
      });

      if (!res.ok) throw new Error();

      showFeedback('✓ Flashcard salvo!', 'success');
      phraseField.value = '';
      transField.value  = '';
      deckSelect.value  = '';
      deckSelect.classList.remove('has-value');
    } catch {
      showFeedback('Erro ao enviar. Backend offline?', 'error');
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
});
