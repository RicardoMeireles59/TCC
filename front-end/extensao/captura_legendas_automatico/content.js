// EasyEnglish – content.js
// Captura legendas EN+PT automaticamente e envia ao backend via background.js.
// Content scripts rodam em mundo isolado — usamos injeção de <script> para
// ler ytInitialPlayerResponse do contexto principal da página.

let parsedCaptions = { en: [], pt: [] };
let videoId = null;
let captureInterval = null;
let lastSentEn = '';
let lastSentPt = '';

// ── Injeta script no contexto da página para ler ytInitialPlayerResponse ──────
function injectTrackReader() {
  const script = document.createElement('script');
  script.textContent = `(function () {
    try {
      const tracks =
        window.ytInitialPlayerResponse
          ?.captions
          ?.playerCaptionsTracklistRenderer
          ?.captionTracks || [];
      document.dispatchEvent(
        new CustomEvent('__ee_tracks__', { detail: JSON.stringify(tracks) })
      );
    } catch {
      document.dispatchEvent(new CustomEvent('__ee_tracks__', { detail: '[]' }));
    }
  })();`;
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

// ── Processa tracks recebidos e solicita fetch ao background ──────────────────
document.addEventListener('__ee_tracks__', (e) => {
  let tracks = [];
  try { tracks = JSON.parse(e.detail); } catch {}

  const vid = getVideoId();
  if (!vid) return;
  videoId = vid;
  parsedCaptions = { en: [], pt: [] };
  lastSentEn = '';
  lastSentPt = '';

  const enTrack = tracks.find(t => t.languageCode?.startsWith('en'));
  const ptTrack = tracks.find(
    t => t.languageCode === 'pt' || t.languageCode?.startsWith('pt-')
  );

  if (enTrack) {
    // EN nativo
    chrome.runtime.sendMessage({ type: 'FETCH_CAPTIONS', lang: 'en', url: enTrack.baseUrl });
    // PT: nativo se existir, senão tradução automática do YouTube via &tlang=pt
    chrome.runtime.sendMessage({
      type: 'FETCH_CAPTIONS',
      lang: 'pt',
      url: (ptTrack?.baseUrl ?? enTrack.baseUrl) + '&tlang=pt',
    });
  } else if (ptTrack) {
    chrome.runtime.sendMessage({ type: 'FETCH_CAPTIONS', lang: 'pt', url: ptTrack.baseUrl });
    chrome.runtime.sendMessage({
      type: 'FETCH_CAPTIONS',
      lang: 'en',
      url: ptTrack.baseUrl + '&tlang=en',
    });
  }
});

function getVideoId() {
  return new URLSearchParams(window.location.search).get('v');
}

function getCurrentCaption(captions, currentTimeMs) {
  return captions.find(
    c => currentTimeMs >= c.startMs && currentTimeMs < c.startMs + c.durationMs
  ) || null;
}

// ── Captura automática: verifica legenda atual a cada 2s e envia se for nova ──
function startAutoCapture() {
  if (captureInterval) clearInterval(captureInterval);

  captureInterval = setInterval(async () => {
    const { active } = await chrome.storage.local.get('active');
    if (active === false) return;

    const video = document.querySelector('video');
    if (!video || video.paused) return;

    const currentTimeMs = video.currentTime * 1000;
    const en = getCurrentCaption(parsedCaptions.en, currentTimeMs);
    const pt = getCurrentCaption(parsedCaptions.pt, currentTimeMs);

    const enText = en?.text || '';
    const ptText = pt?.text || '';

    // Só envia se houver conteúdo novo
    if (!enText && !ptText) return;
    if (enText === lastSentEn && ptText === lastSentPt) return;

    lastSentEn = enText;
    lastSentPt = ptText;

    chrome.runtime.sendMessage({
      type: 'CAPTION_PAIR',
      en: enText,
      pt: ptText,
      videoId,
    });
  }, 2000);
}

// ── Recebe captions parsed do background ──────────────────────────────────────
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'CAPTIONS_LOADED') {
    parsedCaptions[msg.lang] = msg.captions;
  }
});

// ── Inicialização ──────────────────────────────────────────────────────────────
function init() {
  // Aguarda a página terminar de definir ytInitialPlayerResponse
  setTimeout(injectTrackReader, 1500);
  startAutoCapture();
}

// YouTube é SPA — monitora mudanças de URL
let lastUrl = location.href;
new MutationObserver(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href;
    parsedCaptions = { en: [], pt: [] };
    videoId = null;
    lastSentEn = '';
    lastSentPt = '';
    if (captureInterval) { clearInterval(captureInterval); captureInterval = null; }
    init();
  }
}).observe(document.body, { subtree: true, childList: true });

init();
