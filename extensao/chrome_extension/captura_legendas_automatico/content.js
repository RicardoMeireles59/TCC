// EasyEnglish – content.js
// Captura as legendas LENDO O TEXTO RENDERIZADO na tela (.ytp-caption-segment).
// Baixar o arquivo timedtext deixou de funcionar (YouTube exige token POT),
// então lemos o que o próprio player exibe e acumulamos uma transcrição.

let videoId = null;
let captureInterval = null;

// Acumulador da transcrição EN do vídeo atual.
let transcriptWords = [];   // todas as palavras já vistas
let emittedWords = 0;       // quantas já foram enviadas ao backend

const SCRAPE_MS = 1000;     // lê a legenda na tela a cada 1s
const MAX_WORDS = 14;       // sem pontuação (ASR), envia em blocos de ~14 palavras

console.log('[CS] content.js loaded on', location.href);

// ── Detecta extensão recarregada (orphaned content script) ────────────────────
function isExtensionAlive() {
  try {
    return Boolean(chrome.runtime && chrome.runtime.id);
  } catch {
    return false;
  }
}

function stopEverything(reason) {
  console.warn('[CS] stopEverything:', reason, '— content script órfão. Recarregue a aba (F5).');
  if (captureInterval) {
    clearInterval(captureInterval);
    captureInterval = null;
  }
}

function getVideoId() {
  return new URLSearchParams(window.location.search).get('v');
}

function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ── Pede ao page_reader (MAIN world) para LIGAR as legendas EN do player ───────
// Sem captions visíveis, não há o que ler no DOM. O page_reader ativa a trilha EN.
function requestCaptions(vid) {
  console.log('[CS] requesting EN captions enable from page_reader for videoId=', vid);
  document.dispatchEvent(new CustomEvent('__ee_request_tracks__', { detail: vid }));
}

document.addEventListener('__ee_tracks__', (e) => {
  if (!isExtensionAlive()) {
    stopEverything('extension context invalidated (__ee_tracks__)');
    return;
  }
  let tracks = [];
  try { tracks = JSON.parse(e.detail); } catch (err) {
    console.error('[CS] __ee_tracks__: parse falhou', err);
  }
  const langs = tracks.map(t => t.languageCode);
  console.log('[CS] __ee_tracks__ received:', tracks.length, 'tracks', langs);

  const hasEn = tracks.some(t => t.languageCode?.startsWith('en'));
  if (!hasEn) {
    console.warn('[CS] vídeo não tem legenda EN — captura por DOM não terá conteúdo.');
  } else {
    console.log('[CS] legenda EN disponível — page_reader vai ativá-la. Lendo do DOM...');
  }
});

// ── Lê a legenda EN exibida na tela ───────────────────────────────────────────
function readVisibleCaption() {
  const segs = document.querySelectorAll('.ytp-caption-segment');
  if (!segs.length) return '';
  return Array.from(segs)
    .map(s => s.textContent)
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// ── Funde a legenda visível na transcrição, evitando repetir o que rola ───────
// As legendas ASR rolam: "A B C" → "B C D". Detectamos a sobreposição (overlap)
// entre o fim da transcrição e o início do texto visível e só anexamos o novo.
function mergeVisible(visible) {
  const incoming = visible.split(' ').filter(Boolean);
  if (!incoming.length) return;
  if (!transcriptWords.length) {
    transcriptWords = incoming.slice();
    return;
  }
  const maxK = Math.min(transcriptWords.length, incoming.length);
  let overlap = 0;
  for (let k = maxK; k > 0; k--) {
    let match = true;
    for (let i = 0; i < k; i++) {
      const a = transcriptWords[transcriptWords.length - k + i].toLowerCase();
      const b = incoming[i].toLowerCase();
      if (a !== b) { match = false; break; }
    }
    if (match) { overlap = k; break; }
  }
  for (let i = overlap; i < incoming.length; i++) {
    transcriptWords.push(incoming[i]);
  }
}

// ── Decide quando "fechar" um trecho e enviar ao backend ──────────────────────
// Se há pontuação (legenda manual), envia frases completas.
// Sem pontuação (ASR), envia quando acumula ~MAX_WORDS palavras.
function flushReady() {
  if (emittedWords >= transcriptWords.length) return;
  const pending = transcriptWords.slice(emittedWords);

  let lastPunct = -1;
  for (let i = 0; i < pending.length; i++) {
    if (/[.!?]$/.test(pending[i])) lastPunct = i;
  }

  let count = 0;
  if (lastPunct >= 0) {
    count = lastPunct + 1;            // até a última pontuação
  } else if (pending.length >= MAX_WORDS) {
    count = pending.length;           // bloco de ASR sem pontuação
  }

  if (count > 0) {
    const chunk = pending.slice(0, count).join(' ').trim();
    emittedWords += count;
    if (chunk) sendCaption(chunk);
  }
}

function sendCaption(en) {
  console.log('[CS] enviando trecho EN ao background:', en);
  try {
    chrome.runtime.sendMessage({ type: 'CAPTION_EN', en, videoId });
  } catch {
    stopEverything('chrome.runtime.sendMessage falhou');
  }
}

// ── Loop de captura ───────────────────────────────────────────────────────────
function startAutoCapture() {
  if (captureInterval) clearInterval(captureInterval);
  console.log('[CS] startAutoCapture: lendo legendas do DOM a cada', SCRAPE_MS, 'ms');

  captureInterval = setInterval(async () => {
    if (!isExtensionAlive()) {
      stopEverything('extension context invalidated');
      return;
    }
    let active, authToken;
    try {
      ({ active, authToken } = await chrome.storage.local.get(['active', 'authToken']));
    } catch {
      stopEverything('chrome.storage.local.get falhou');
      return;
    }
    if (active === false) return;
    if (!authToken) return; // só captura quem estiver logado na extensão

    const video = document.querySelector('video');
    if (!video || video.paused) return;

    const visible = readVisibleCaption();
    if (!visible) return;

    mergeVisible(visible);
    flushReady();
  }, SCRAPE_MS);
}

// ── Inicialização ─────────────────────────────────────────────────────────────
function resetTranscript() {
  transcriptWords = [];
  emittedWords = 0;
}

function init() {
  const vid = getVideoId();
  console.log('[CS] init() — videoId=', vid);
  videoId = vid;
  resetTranscript();
  if (vid) {
    setTimeout(() => requestCaptions(vid), 1500);
  } else {
    console.log('[CS] init(): sem videoId na URL, captura inativa');
  }
  startAutoCapture();
}

// YouTube é SPA — monitora mudança de URL
let lastUrl = location.href;
new MutationObserver(() => {
  if (location.href !== lastUrl) {
    console.log('[CS] URL changed:', lastUrl, '->', location.href);
    lastUrl = location.href;
    videoId = null;
    resetTranscript();
    if (captureInterval) { clearInterval(captureInterval); captureInterval = null; }
    init();
  }
}).observe(document.body, { subtree: true, childList: true });

init();
