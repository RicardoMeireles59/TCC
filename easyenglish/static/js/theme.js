// Alternância de tema (claro/escuro) unificada — [data-theme="white"] no <html>.
(function () {
  const KEY = 'theme';
  const root = document.documentElement;

  function apply(theme) {
    if (theme === 'white') root.setAttribute('data-theme', 'white');
    else root.removeAttribute('data-theme');
  }

  // Aplica cedo para reduzir flash.
  apply(localStorage.getItem(KEY) || 'dark');

  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      const next = root.getAttribute('data-theme') === 'white' ? 'dark' : 'white';
      apply(next);
      localStorage.setItem(KEY, next);
    });
  });
})();
