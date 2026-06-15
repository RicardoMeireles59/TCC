// EasyEnglish – popup.js

const API_BASE = 'http://localhost:8000/extensao';

document.addEventListener('DOMContentLoaded', async () => {

  // ── Token de autenticação — redireciona para login se não existir ──────────
  const { authToken } = await chrome.storage.local.get('authToken');
  if (!authToken) {
    window.location.href = '../pagina_login/login.html';
    return;
  }

  function authHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Token ${authToken}`,
    };
  }

  const toggle = document.getElementById('toggleActive');
  const phraseField = document.getElementById('phraseField');
  const transField = document.getElementById('translationField');
  const deckSelect = document.getElementById('deckSelect');
  const sendBtn = document.getElementById('sendBtn');
  const feedback = document.getElementById('feedback');

  // ── Tema dark/white ────────────────────────────────────────────────────────
  const themeToggle = document.getElementById('themeToggle');

  function applyTheme(t) {
    if (t === 'white') {
      document.documentElement.setAttribute('data-theme', 'white');
      themeToggle.textContent = '🌙 Dark';
    } else {
      document.documentElement.removeAttribute('data-theme');
      themeToggle.textContent = '☀️ White';
    }
  }

  chrome.storage.local.get('theme', ({ theme }) => applyTheme(theme || 'dark'));

  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'white' : 'dark';
    applyTheme(next);
    chrome.storage.local.set({ theme: next });
  });

  let debounceTimer = null;

  // ── Traduz via Google Translate (endpoint interno, sem chave) ──────────────
  async function translateWithGoogle(text, targetLang) {
    const url =
      `https://translate.googleapis.com/translate_a/single` +
      `?client=gtx&sl=auto&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Google Translate error ' + res.status);
    const data = await res.json();
    const translated = data[0].map(chunk => chunk[0]).join('');
    const detectedLang = data[2];
    return { translated, detectedLang };
  }

  // ── Tenta preencher frase com texto selecionado na página ──────────────────
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  try {
    const [result] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection()?.toString().trim() || '',
    });
    if (result?.result) {
      phraseField.value = result.result;
      triggerTranslation(result.result);
    }
  } catch { }

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

  // ── Limpa tradução e inicia debounce a cada keystroke ─────────────────────
  phraseField.addEventListener('input', () => {
    transField.value = '';
    clearTimeout(debounceTimer);
    const phrase = phraseField.value.trim();
    if (!phrase) return;
    debounceTimer = setTimeout(() => triggerTranslation(phrase), 500);
  });

  phraseField.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    e.preventDefault();
    clearTimeout(debounceTimer);
    const phrase = phraseField.value.trim();
    if (phrase) triggerTranslation(phrase);
  });

  function triggerTranslation(phrase) {
    autoTranslate(phrase).catch(() => { });
  }

  // ── Auto-tradução ──────────────────────────────────────────────────────────
  async function autoTranslate(phrase) {
    if (!phrase) return;
    transField.value = '';
    transField.placeholder = 'Traduzindo…';
    try {
      const probe = await translateWithGoogle(phrase, 'en');
      const detectedLang = probe.detectedLang?.split('-')[0];
      if (detectedLang && detectedLang !== 'pt' && detectedLang !== 'en') {
        showFeedback(`Idioma "${detectedLang}" não suportado.`, 'error');
        return;
      }
      const translated = detectedLang === 'pt'
        ? probe.translated
        : (await translateWithGoogle(phrase, 'pt')).translated;
      transField.value = translated;
    } catch {
      showFeedback('Erro ao traduzir.', 'error');
    } finally {
      transField.placeholder = 'Tradução';
    }
  }

  // ── Enviar flashcard manual ────────────────────────────────────────────────
  sendBtn.addEventListener('click', async () => {
    const phrase = phraseField.value.trim();
    const translation = transField.value.trim();
    const deck = deckSelect.value;

    if (!phrase || !translation || !deck) {
      showFeedback('Preencha todos os campos.', 'error');
      return;
    }

    sendBtn.disabled = true;
    sendBtn.textContent = 'Enviando…';

    try {
      const res = await fetch(`${API_BASE}/api/flashcards/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ phrase, translation, deck }),
      });

      if (res.status === 401) {
        await chrome.storage.local.remove('authToken');
        window.location.href = '../pagina_login/login.html';
        return;
      }
      if (!res.ok) throw new Error();

      showFeedback('✓ Flashcard salvo!', 'success');
      phraseField.value = '';
      transField.value = '';
      deckSelect.value = '';
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
    feedback.className = `feedback ${type}`;
    clearTimeout(feedback._timer);
    feedback._timer = setTimeout(() => {
      feedback.className = 'feedback hidden';
    }, 3000);
  }
});
