// EasyEnglish – background.js

console.log('[BG] service worker started/woke up at', new Date().toISOString());

const API_BASE = 'http://localhost:8000/extensao';

async function getAuthHeaders() {
  const { authToken } = await chrome.storage.local.get('authToken');
  if (authToken) {
    console.log('[BG] getAuthHeaders: token found', authToken.slice(0, 8) + '...');
    return { 'Content-Type': 'application/json', 'Authorization': `Token ${authToken}` };
  }
  console.warn('[BG] getAuthHeaders: NO token in storage — request will fail with 401');
  return { 'Content-Type': 'application/json' };
}

// ── Tradução EN→PT via Google Translate (endpoint gtx, sem chave) ─────────────
// Feita no service worker (sem CSP de página). O YouTube não serve mais a trilha
// PT (token POT), então traduzimos o EN capturado da tela.
async function translateToPt(text) {
  try {
    const url =
      'https://translate.googleapis.com/translate_a/single' +
      '?client=gtx&sl=en&tl=pt&dt=t&q=' + encodeURIComponent(text);
    const res = await fetch(url);
    if (!res.ok) throw new Error('gtx status ' + res.status);
    const data = await res.json();
    return (data[0] || []).map(chunk => chunk[0]).join('');
  } catch (err) {
    console.warn('[BG] translateToPt falhou:', err);
    return '';
  }
}

chrome.runtime.onInstalled.addListener(() => {
  console.log('[BG] Extension installed/updated — setting active=true');
  chrome.storage.local.set({ active: true });
});

chrome.runtime.onMessage.addListener((msg, sender, respond) => {
  console.log('[BG] onMessage received:', msg.type, msg);

  // ── Recebe trecho EN da tela → traduz → envia o par ao Django ──────────────
  if (msg.type === 'CAPTION_EN') {
    console.log('[BG] CAPTION_EN received — en:', msg.en?.slice(0, 80), '| videoId:', msg.videoId);
    (async () => {
      const { authToken } = await chrome.storage.local.get('authToken');
      if (!authToken) {
        console.warn('[BG] CAPTION_EN ignorado — usuário não está logado na extensão.');
        return;
      }
      const pt = await translateToPt(msg.en);
      console.log('[BG] traduzido PT:', pt.slice(0, 80));
      const headers = await getAuthHeaders();
      const body = JSON.stringify({ en: msg.en, pt, video_id: msg.videoId || '' });
      try {
        const r = await fetch(`${API_BASE}/api/captions/`, { method: 'POST', headers, body });
        const json = await r.json().catch(() => null);
        if (r.ok) {
          console.log('[BG] CAPTION_EN backend OK:', json);
        } else {
          console.error('[BG] CAPTION_EN backend error', r.status, json);
        }
      } catch (err) {
        console.error('[BG] CAPTION_EN fetch failed (backend offline?):', err);
      }
    })();
    return true;
  }

  // ── Flashcard manual enviado pelo popup ────────────────────────────────────
  if (msg.type === 'SAVE_FLASHCARD') {
    console.log('[BG] SAVE_FLASHCARD:', msg.flashcard);
    getAuthHeaders().then(headers => {
      fetch(`${API_BASE}/api/flashcards/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(msg.flashcard),
      })
        .then(r => {
          console.log('[BG] SAVE_FLASHCARD response:', r.status);
          respond({ ok: r.ok });
        })
        .catch(err => {
          console.error('[BG] SAVE_FLASHCARD fetch failed:', err);
          respond({ ok: false });
        });
    });
    return true;
  }

  console.warn('[BG] onMessage: unhandled message type:', msg.type);
});
