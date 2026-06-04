// EasyEnglish – page_reader.js
// Roda no MAIN world (contexto da página) — declarado no manifest com "world":"MAIN".
// Tem acesso direto a window.ytInitialPlayerResponse SEM violar a CSP do YouTube,
// pois é carregado como recurso da extensão (não é inline script).
//
// Comunicação com o content script (isolated world) via CustomEvent no document:
//   - recebe  '__ee_request_tracks__'  (detail = videoId alvo)
//   - responde '__ee_tracks__'         (detail = JSON.stringify(captionTracks))

(function () {
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
      const en = tracks.find(t => (t.languageCode || '').startsWith('en'));
      if (!en) {
        console.warn('[PAGE] sem trilha EN para ativar');
        return;
      }
      player.setOption('captions', 'track', { languageCode: en.languageCode });
      console.log('[PAGE] legendas EN ativadas via setOption (', en.languageCode, ')');
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
          console.log('[PAGE] tracks found:', tracks.length, tracks.map(t => t.languageCode));
          document.dispatchEvent(new CustomEvent('__ee_tracks__', { detail: JSON.stringify(tracks) }));
          enableEnglishCaptions(tracks);
          return;
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
})();
