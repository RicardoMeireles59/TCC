/* EasyEnglish — toasts de mensagens (Django messages).
 * Fecha ao clicar no "x" e remove do DOM quando a animação de saída termina,
 * evitando que o elemento invisível continue capturando cliques. */
(function () {
  "use strict";

  const container = document.getElementById("messages");
  if (!container) return;

  function dismiss(msg) {
    if (!msg || msg.dataset.dismissed) return;
    msg.dataset.dismissed = "true";
    msg.style.animation = "msg-out 0.2s ease-in forwards";
    msg.addEventListener("animationend", () => msg.remove(), { once: true });
  }

  container.querySelectorAll(".msg").forEach((msg) => {
    msg.addEventListener("animationend", (e) => {
      if (e.animationName === "msg-out") msg.remove();
    });
    const closeBtn = msg.querySelector(".msg-close");
    if (closeBtn) closeBtn.addEventListener("click", () => dismiss(msg));
  });
})();
