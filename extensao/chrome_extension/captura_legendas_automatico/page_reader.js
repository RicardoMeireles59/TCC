// EasyEnglish – page_reader.js
// Roda no MAIN world (contexto da página) — declarado no manifest com "world":"MAIN".
// Tem acesso direto a window.ytInitialPlayerResponse SEM violar a CSP do YouTube,
// pois é carregado como recurso da extensão (não é inline script).
//
// Comunicação com o content script (isolated world) via CustomEvent no document:
//   - recebe  '__ee_request_tracks__'  (detail = videoId alvo)
//   - responde '__ee_tracks__'         (detail = JSON.stringify(captionTracks))
//
// Idempotente: pode ser reinjetado via chrome.scripting quando o usuário liga a
// extensão. Um guard impede registrar o listener mais de uma vez (evita respostas
// duplicadas ao mesmo pedido).

(function () {
  if (window.__eePageReaderLoaded) {
    console.log('[PAGE] page_reader.js já carregado — ignorando reinjeção');
    return;
  }
  window.__eePageReaderLoaded = true;

  console.log('[PAGE] page_reader.js loaded (MAIN world)');

  // Liga a trilha de legenda EN no player, para que o texto seja renderizado
  // na tela e o content script possa lê-lo do DOM.
  function enableEnglishCaptions(tracks) {
    try {
      const player = document.getElementById('movie_player');
      if (!player || typeof player.setOption !== 'function') {
        console.warn('[PAGE] player.setOption indisponível — ative o CC manualmente');
        return;
      }
      // Garante o módulo de legendas carregado (pode ter sido descarregado ao
      // desativar o toggle).
      if (typeof player.loadModule === 'function') {
        try { player.loadModule('captions'); } catch {}
      }
      // 1) Trilha nativa em inglês, se existir.
      const nativeEn = tracks.find(t => (t.languageCode || '').startsWith('en'));
      if (nativeEn) {
        player.setOption('captions', 'track', { languageCode: nativeEn.languageCode });
        console.log('[PAGE] legendas EN nativas ativadas (', nativeEn.languageCode, ')');
        return;
      }

      // 2) Sem trilha EN nativa: auto-traduzir a trilha base para inglês.
      //    Como só lemos do DOM o que o player renderiza, pedimos ao player a
      //    tradução automática (ex.: pt → en). Cobre vídeos em outras línguas que
      //    não têm trilha EN própria, mas oferecem 'en' em translationLanguages.
      const base = tracks[0];
      if (!base) {
        console.warn('[PAGE] nenhuma trilha base para traduzir');
        return;
      }
      const translated = Object.assign({}, base, {
        translationLanguage: { languageCode: 'en', languageName: 'English' },
      });
      player.setOption('captions', 'track', translated);
      console.log('[PAGE] sem EN nativo — auto-traduzindo', base.languageCode, '→ en via setOption');
    } catch (err) {
      console.warn('[PAGE] não foi possível ativar legendas automaticamente:', err, '— ative o CC manualmente');
    }
  }

  document.addEventListener('__ee_request_tracks__', (e) => {
    const targetVideoId = e.detail;
    console.log('[PAGE] request received for videoId=', targetVideoId);

    let attempt = 0;
    const MAX_ATTEMPTS = 20; // 20 x 500ms = 10s

    // Tenta obter o player response de múltiplas fontes, em ordem de confiabilidade.
    // getPlayerResponse() do #movie_player reflete o vídeo ATUAL (funciona em SPA nav);
    // ytInitialPlayerResponse só é confiável no carregamento inicial da página.
    function getPlayerResponse() {
      try {
        const player = document.getElementById('movie_player');
        if (player && typeof player.getPlayerResponse === 'function') {
          const r = player.getPlayerResponse();
          if (r) return { response: r, source: 'movie_player.getPlayerResponse()' };
        }
      } catch (err) {
        console.warn('[PAGE] getPlayerResponse() failed:', err);
      }
      if (window.ytInitialPlayerResponse) {
        return { response: window.ytInitialPlayerResponse, source: 'ytInitialPlayerResponse' };
      }
      return { response: null, source: 'none' };
    }

    function tryGetTracks() {
      attempt++;
      try {
        const { response, source } = getPlayerResponse();
        const currentVideoId = response?.videoDetails?.videoId;
        console.log('[PAGE] attempt', attempt, '— source:', source, '| videoId:', currentVideoId, '| target:', targetVideoId);

        if (response && currentVideoId === targetVideoId) {
          const tracks = response?.captions?.playerCaptionsTracklistRenderer?.captionTracks || [];
          // O videoId já bate, mas as captionTracks podem ainda não ter sido
          // populadas no player response (carregam depois do videoDetails). Só
          // finalizamos quando há trilhas; senão seguimos tentando até MAX_ATTEMPTS,
          // evitando o falso "vídeo sem legenda EN".
          if (tracks.length) {
            console.log('[PAGE] tracks found:', tracks.length, tracks.map(t => t.languageCode));
            document.dispatchEvent(new CustomEvent('__ee_tracks__', { detail: JSON.stringify(tracks) }));
            enableEnglishCaptions(tracks);
            return;
          }
          console.log('[PAGE] videoId bate mas captionTracks vazio — aguardando carregar (retry)');
        }
      } catch (err) {
        console.error('[PAGE] Error reading player response:', err);
      }

      if (attempt < MAX_ATTEMPTS) {
        setTimeout(tryGetTracks, 500);
      } else {
        console.warn('[PAGE] gave up after', MAX_ATTEMPTS, 'attempts — dispatching empty tracks');
        document.dispatchEvent(new CustomEvent('__ee_tracks__', { detail: '[]' }));
      }
    }

    tryGetTracks();
  });

  // ── Desliga as legendas no player (quando o usuário desativa o toggle) ─────────
  document.addEventListener('__ee_disable_captions__', () => {
    try {
      const player = document.getElementById('movie_player');
      if (!player) return;
      if (typeof player.setOption === 'function') player.setOption('captions', 'track', {});
      if (typeof player.unloadModule === 'function') player.unloadModule('captions');
      console.log('[PAGE] legendas desativadas (toggle off)');
    } catch (err) {
      console.warn('[PAGE] falha ao desativar legendas:', err);
    }
  });
})();
