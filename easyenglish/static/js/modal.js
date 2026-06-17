/* EasyEnglish — modal de confirmação global (substitui confirm()/alert()).
 *
 * Uso programático:
 *   const ok = await EasyModal.confirm({
 *     title: 'Excluir flashcard?',
 *     message: 'Esta ação não pode ser desfeita.',
 *     confirmText: 'Excluir', cancelText: 'Cancelar', danger: true,
 *   });
 *
 * Uso declarativo (formulários destrutivos, sem JS extra na página):
 *   <form data-confirm="Excluir este flashcard?" data-confirm-danger="true">
 * O submit é interceptado, o modal aparece e o form só é enviado se confirmado.
 */
(function () {
  "use strict";

  const overlay = document.getElementById("modalOverlay");
  if (!overlay) return;

  const panel = overlay.querySelector(".modal-panel");
  const iconEl = document.getElementById("modalIcon");
  const titleEl = document.getElementById("modalTitle");
  const messageEl = document.getElementById("modalMessage");
  const cancelBtn = document.getElementById("modalCancelBtn");
  const confirmBtn = document.getElementById("modalConfirmBtn");

  let activeResolve = null;
  let lastFocused = null;

  function close(result) {
    overlay.hidden = true;
    document.body.classList.remove("modal-open");
    if (lastFocused) lastFocused.focus();
    if (activeResolve) {
      const resolve = activeResolve;
      activeResolve = null;
      resolve(result);
    }
  }

  function open({
    title = "Confirmar ação",
    message = "",
    confirmText = "Confirmar",
    cancelText = "Cancelar",
    danger = false,
  } = {}) {
    return new Promise((resolve) => {
      activeResolve = resolve;
      lastFocused = document.activeElement;

      titleEl.textContent = title;
      messageEl.textContent = message;
      confirmBtn.textContent = confirmText;
      cancelBtn.textContent = cancelText;
      confirmBtn.classList.toggle("btn-danger", !!danger);
      iconEl.classList.toggle("danger", !!danger);

      overlay.hidden = false;
      document.body.classList.add("modal-open");
      confirmBtn.focus();
    });
  }

  cancelBtn.addEventListener("click", () => close(false));
  confirmBtn.addEventListener("click", () => close(true));
  overlay.addEventListener("mousedown", (e) => {
    if (e.target === overlay) close(false);
  });
  document.addEventListener("keydown", (e) => {
    if (overlay.hidden) return;
    if (e.key === "Escape") close(false);
    // Laço de foco simples entre os dois botões do modal.
    if (e.key === "Tab") {
      const focusables = [cancelBtn, confirmBtn];
      const i = focusables.indexOf(document.activeElement);
      if (i !== -1) {
        e.preventDefault();
        const next = e.shiftKey ? (i - 1 + focusables.length) % focusables.length : (i + 1) % focusables.length;
        focusables[next].focus();
      }
    }
  });

  window.EasyModal = { confirm: open };

  // ----- Interceptor declarativo para formulários destrutivos -----
  document.addEventListener(
    "submit",
    (e) => {
      const form = e.target;
      if (!(form instanceof HTMLFormElement) || !form.hasAttribute("data-confirm")) return;
      if (form.dataset.confirmed === "true") return; // já confirmado, deixa enviar

      e.preventDefault();
      open({
        title: form.dataset.confirmTitle || "Confirmar ação",
        message: form.dataset.confirm,
        confirmText: form.dataset.confirmText || "Confirmar",
        cancelText: form.dataset.confirmCancelText || "Cancelar",
        danger: form.dataset.confirmDanger === "true",
      }).then((ok) => {
        if (ok) {
          form.dataset.confirmed = "true";
          if (form.requestSubmit) form.requestSubmit();
          else form.submit();
        }
      });
    },
    true
  );
})();
