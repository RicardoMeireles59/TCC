// Estudo: navega entre os cards e atualiza a barra de progresso. Persistência via <form> POST.
(function () {
  const slots = Array.from(document.querySelectorAll('.card-slot'));
  const atualEl = document.getElementById('card-atual');
  const totalEl = document.getElementById('total-cards');
  const fillEl = document.getElementById('progress-fill');
  if (totalEl) totalEl.textContent = slots.length;
  if (!slots.length) return;

  let idx = 0;

  function show(i) {
    slots.forEach((s, k) => s.classList.toggle('is-active', k === i));
    if (atualEl) atualEl.textContent = i + 1;
    if (fillEl) fillEl.style.width = ((i + 1) / slots.length) * 100 + '%';
  }
  function go(d) { idx = (idx + d + slots.length) % slots.length; show(idx); }

  document.getElementById('btn-anterior')?.addEventListener('click', () => go(-1));
  document.getElementById('btn-proximo')?.addEventListener('click', () => go(1));

  show(0);
})();
