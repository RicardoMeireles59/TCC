// Sidebar: recolher/expandir (desktop, persistido) e abrir/fechar (mobile).
(function () {
  const KEY = 'sidebar-collapsed';
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  if (localStorage.getItem(KEY) === '1') {
    sidebar.classList.add('collapsed');
  }

  const collapseBtn = document.getElementById('sidebarCollapseBtn');
  collapseBtn?.addEventListener('click', function () {
    const collapsed = sidebar.classList.toggle('collapsed');
    localStorage.setItem(KEY, collapsed ? '1' : '0');
  });

  const mobileToggle = document.getElementById('sidebarMobileToggle');
  mobileToggle?.addEventListener('click', function () {
    sidebar.classList.toggle('mobile-open');
  });

  document.addEventListener('click', function (e) {
    if (window.innerWidth > 1024) return;
    if (!sidebar.classList.contains('mobile-open')) return;
    if (sidebar.contains(e.target) || e.target.closest('#sidebarMobileToggle')) return;
    sidebar.classList.remove('mobile-open');
  });
})();
