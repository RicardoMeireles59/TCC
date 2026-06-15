// Estudo: virar/navegar cards. Dados vêm do Django; persistência via <form> POST.
(function () {
  const slots = Array.from(document.querySelectorAll('.card-slot'));
  const atualEl = document.getElementById('card-atual');
  const totalEl = document.getElementById('total-cards');
  if (totalEl) totalEl.textContent = slots.length;
  if (!slots.length) return;

  let idx = 0;
  const flashcardOf = (i) => slots[i] && slots[i].querySelector('.flashcard');

  function show(i) {
    slots.forEach((s, k) => s.classList.toggle('is-active', k === i));
    const fc = flashcardOf(i);
    if (fc) fc.classList.remove('flip');
    if (atualEl) atualEl.textContent = i + 1;
  }
  function flip() { const fc = flashcardOf(idx); if (fc) fc.classList.toggle('flip'); }
  function go(d) { idx = (idx + d + slots.length) % slots.length; show(idx); }

  document.getElementById('btn-anterior')?.addEventListener('click', () => go(-1));
  document.getElementById('btn-proximo')?.addEventListener('click', () => go(1));
  document.getElementById('btn-virar')?.addEventListener('click', flip);
  slots.forEach((slot, k) => {
    slot.querySelector('.flashcard')?.addEventListener('click', (e) => {
      if (e.target.closest('form')) return;
      if (k === idx) flip();
    });
  });

  show(0);
})();
