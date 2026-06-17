/* EasyEnglish — telas de autenticação (login / cadastro).
 * Porta de um componente React para JS puro:
 *   - efeito "typewriter" na citação do painel de imagem;
 *   - botão mostrar/ocultar senha (funciona com 1+ campos de senha).
 * Sem dependências externas. */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ----- Efeito typewriter -----
  function runTypewriter(el) {
    const text = el.dataset.typewriter || "";
    const speed = parseInt(el.dataset.speed || "60", 10);

    const cursor = document.createElement("span");
    cursor.className = "tw-cursor";
    cursor.textContent = "|";
    cursor.setAttribute("aria-hidden", "true");

    if (reduceMotion || !text) {
      el.textContent = text;
      el.after(cursor);
      return;
    }

    el.after(cursor);
    let i = 0;
    (function type() {
      if (i <= text.length) {
        el.textContent = text.slice(0, i);
        i += 1;
        setTimeout(type, speed);
      }
    })();
  }

  document.querySelectorAll(".typewriter[data-typewriter]").forEach(runTypewriter);

  // ----- Mostrar / ocultar senha -----
  document.querySelectorAll("[data-password-toggle]").forEach((toggle) => {
    const wrap = toggle.closest("[data-password-field]");
    if (!wrap) return;
    const input = wrap.querySelector("input");
    if (!input) return;

    const openIcon = toggle.querySelector("[data-eye-open]");
    const closedIcon = toggle.querySelector("[data-eye-closed]");

    toggle.addEventListener("click", () => {
      const reveal = input.type === "password";
      input.type = reveal ? "text" : "password";
      if (openIcon) openIcon.hidden = reveal;
      if (closedIcon) closedIcon.hidden = !reveal;
      input.focus();
    });
  });
})();
