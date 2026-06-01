// EasyEnglish – background.js

const API_BASE = 'http://localhost:8000/extensao';

function parseCaptionJson(data) {
  return (data.events || [])
    .filter(e => e.segs)
    .map(e => ({
      startMs:    e.tStartMs || 0,
      durationMs: e.dDurationMs || 3000,
      text: (e.segs || []).map(s => s.utf8 || '').join('').trim(),
    }))
    .filter(c => c.text);
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ active: true });
});

chrome.runtime.onMessage.addListener((msg, sender, respond) => {

  // ── Busca arquivo de legendas e devolve ao content script ──────────────────
  if (msg.type === 'FETCH_CAPTIONS') {
    fetch(msg.url + '&fmt=json3')
      .then(r => r.json())
      .then(data => {
        const captions = parseCaptionJson(data);
        if (sender.tab?.id) {
          chrome.tabs.sendMessage(sender.tab.id, {
            type: 'CAPTIONS_LOADED',
            lang: msg.lang,
            captions,
          });
        }
      })
      .catch(() => {});
    return true;
  }

  // ── Recebe par EN+PT do content script e envia ao backend Django ───────────
  if (msg.type === 'CAPTION_PAIR') {
    fetch(`${API_BASE}/legendas/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        en:       msg.en,
        pt:       msg.pt,
        video_id: msg.videoId || '',
      }),
    }).catch(() => {});
    return true;
  }

  // ── Flashcard manual enviado pelo popup ────────────────────────────────────
  if (msg.type === 'SAVE_FLASHCARD') {
    fetch(`${API_BASE}/flashcards/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(msg.flashcard),
    })
      .then(() => respond({ ok: true }))
      .catch(() => respond({ ok: false }));
    return true;
  }
});
