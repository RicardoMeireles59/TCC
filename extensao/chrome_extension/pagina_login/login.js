/**
 * EasyEnglish – login.js
 * Autenticação + controle de tema dark/white.
 */

document.addEventListener('DOMContentLoaded', async () => {

  const emailField    = document.getElementById('emailField');
  const passwordField = document.getElementById('passwordField');
  const loginBtn      = document.getElementById('loginBtn');
  const feedback      = document.getElementById('feedback');
  const forgotLink    = document.getElementById('forgotLink');
  const registerLink  = document.getElementById('registerLink');
  const themeToggle   = document.getElementById('themeToggle');

  // ── Tema: persiste via storage ─────────────────────────────────────────────
  const { theme } = await chrome.storage.local.get('theme');
  applyTheme(theme || 'dark');

  themeToggle.addEventListener('click', async () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'white' : 'dark';
    applyTheme(next);
    await chrome.storage.local.set({ theme: next });
  });

  function applyTheme(t) {
    if (t === 'white') {
      document.documentElement.setAttribute('data-theme', 'white');
      themeToggle.textContent = '🌙 Dark';
    } else {
      document.documentElement.removeAttribute('data-theme');
      themeToggle.textContent = '☀️ White';
    }
  }

  // ── Foco automático ────────────────────────────────────────────────────────
  emailField.focus();

  // ── Captura texto selecionado na aba atual (pré-preenche e-mail se for email)
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const [result] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection()?.toString().trim() || ''
    });
    const sel = result?.result || '';
    if (sel) {
      emailField.value = sel;
      passwordField.focus();
    }
  } catch {}

  // ── Enter nos campos dispara login ─────────────────────────────────────────
  [emailField, passwordField].forEach(input => {
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') loginBtn.click();
    });
  });

  // ── Login ──────────────────────────────────────────────────────────────────
  loginBtn.addEventListener('click', async () => {
    const email    = emailField.value.trim();
    const password = passwordField.value;

    if (!email || !password) {
      showFeedback('Preencha usuário e senha.', 'error');
      return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = 'Entrando…';

    try {
      const body = JSON.stringify({ username: email, password });
      console.log('[LOGIN] Posting to token endpoint, body:', body);
      const res = await fetch('http://localhost:8000/extensao/api/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });
      console.log('[LOGIN] Response status:', res.status, res.statusText);
      const responseText = await res.text();
      console.log('[LOGIN] Response body:', responseText);
      if (!res.ok) throw new Error('Credenciais inválidas. Verifique usuário e senha. (HTTP ' + res.status + ')');
      const { token } = JSON.parse(responseText);
      await chrome.storage.local.set({ authToken: token, userEmail: email, loggedIn: true });

      showFeedback('✓ Login realizado!', 'success');
      setTimeout(() => { window.location.href = '../pagina_flashcards/popup.html'; }, 1000);

    } catch (err) {
      showFeedback(err.message || 'Erro ao entrar. Tente novamente.', 'error');
    } finally {
      loginBtn.disabled = false;
      loginBtn.textContent = 'Entrar';
    }
  });

  // ── Esqueci a senha ────────────────────────────────────────────────────────
  forgotLink.addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://suaapp.com/recuperar-senha' });
  });
  forgotLink.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') forgotLink.click();
  });

  // ── Criar conta ────────────────────────────────────────────────────────────
  registerLink.addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://localhost:8000/register/' });
  });
  registerLink.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') registerLink.click();
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