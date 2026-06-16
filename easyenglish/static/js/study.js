(function () {
  const slots = Array.from(document.querySelectorAll('.card-slot'));
  const atualEl = document.getElementById('card-atual');
  const totalEl = document.getElementById('total-cards');
  const fillEl = document.getElementById('progress-fill');
  if (totalEl) totalEl.textContent = slots.length;
  if (!slots.length) return;

  let idx = 0;

  function resetSlot(slot) {
    const card = slot.querySelector('.flashcard');
    const actions = slot.querySelector('.status-resposta');
    if (card) card.classList.remove('flipped');
    if (actions) actions.hidden = true;
  }

  function show(i) {
    slots.forEach((s, k) => {
      if (k !== i) resetSlot(s);
      s.classList.toggle('is-active', k === i);
    });
    if (atualEl) atualEl.textContent = i + 1;
    if (fillEl) fillEl.style.width = ((i + 1) / slots.length) * 100 + '%';
  }

  function go(d) { idx = (idx + d + slots.length) % slots.length; show(idx); }

  slots.forEach(slot => {
    const card = slot.querySelector('.flashcard');
    if (!card) return;

    function flip() {
      if (!slot.classList.contains('is-active')) return;
      card.classList.toggle('flipped');
      const actions = slot.querySelector('.status-resposta');
      if (actions) actions.hidden = !card.classList.contains('flipped');
    }

    card.addEventListener('click', flip);
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(); }
    });
  });

  document.getElementById('btn-anterior')?.addEventListener('click', () => go(-1));
  document.getElementById('btn-proximo')?.addEventListener('click', () => go(1));

  show(0);
})();
