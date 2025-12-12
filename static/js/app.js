// static/js/app.js
// Versión completa y robusta: inicializaciones, audio lazy-load, feedback y modal de etiquetado.
// Sustituya el contenido actual de static/js/app.js por este.

(function () {
  "use strict";

  /* -------------------- Helpers -------------------- */
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));
  const on = (el, event, selOrFn, fnIfSel) => {
    // on(element, 'click', '.btn', fn)  OR on(document, 'click', fn)
    if (!el) return;
    if (typeof selOrFn === "string" && typeof fnIfSel === "function") {
      el.addEventListener(event, (ev) => {
        const t = ev.target.closest ? ev.target.closest(selOrFn) : null;
        if (t) fnIfSel.call(t, ev, t);
      });
    } else if (typeof selOrFn === "function") {
      el.addEventListener(event, selOrFn);
    }
  };

  const ready = (fn) => {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  };

  /* -------------------- Background Particles (light) -------------------- */
  function initParticles() {
    const canvas = $("#bg-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let w = (canvas.width = innerWidth);
    let h = (canvas.height = innerHeight);
    let parts = [];

    function rand(min, max) {
      return Math.random() * (max - min) + min;
    }

    function make(n) {
      parts = [];
      for (let i = 0; i < n; i++) {
        parts.push({
          x: rand(0, w),
          y: rand(0, h),
          r: rand(0.6, 2.8),
          vx: rand(-0.25, 0.25),
          vy: rand(-0.12, 0.12),
          a: rand(0.06, 0.26),
        });
      }
    }

    function resize() {
      w = canvas.width = innerWidth;
      h = canvas.height = innerHeight;
      make(Math.max(24, Math.floor((w + h) / 140)));
    }

    function frame() {
      ctx.clearRect(0, 0, w, h);
      for (const p of parts) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < -10) p.x = w + 10;
        if (p.x > w + 10) p.x = -10;
        if (p.y < -10) p.y = h + 10;
        if (p.y > h + 10) p.y = -10;
        ctx.beginPath();
        ctx.fillStyle = `rgba(255,255,255,${p.a})`;
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
      requestAnimationFrame(frame);
    }

    resize();
    frame();
    addEventListener("resize", () => {
      // debounce quick resize
      clearTimeout(initParticles._rt);
      initParticles._rt = setTimeout(resize, 160);
    });
  }

  /* -------------------- UI Initialization -------------------- */
  function initUI() {
    // autofocus textarea
    const textarea = $("#texto_usuario");
    if (textarea) {
      try { textarea.focus({ preventScroll: true }); } catch(e) { textarea.focus(); }
    }

    // small demo stats filler (visual)
    const statDet = $("#stat-detections");
    const statEmo = $("#stat-emotions");
    if (statDet) statDet.textContent = Math.floor(Math.random() * 420 + 40).toString();
    if (statEmo) statEmo.textContent = Math.floor(Math.random() * 28 + 6).toString();

    // quick phrase fill
    const quick = $("#quick-phrase");
    if (quick && textarea) {
      quick.addEventListener("click", () => {
        const samples = [
          "Me siento muy ansioso y no puedo dormir",
          "Estoy en luto y no encuentro consuelo",
          "Me siento vacío y sin energía",
          "Estoy estresado por el trabajo"
        ];
        textarea.value = samples[Math.floor(Math.random() * samples.length)];
        textarea.focus();
      });
    }

    // animate sound cards in stagger
    const soundCards = $$(".sound-card");
    soundCards.forEach((c, i) => {
      c.style.opacity = 0;
      c.style.transform = "translateY(8px)";
      setTimeout(() => {
        c.style.transition = "opacity .36s ease, transform .36s cubic-bezier(.2,.9,.3,1)";
        c.style.opacity = 1;
        c.style.transform = "none";
      }, 220 + i * 80);
    });

    // scroll to results if present
    const results = $("#results");
    if (results) results.scrollIntoView({ behavior: "smooth", block: "start" });

    // lazy-load audio src attributes and single-play behavior
    const players = $$(".audio-player");
    const allPlayers = Array.from(players);
    allPlayers.forEach((p) => {
      const dataSrc = p.getAttribute("data-src");
      const sourceEl = p.querySelector("source");
      if (dataSrc && sourceEl && !sourceEl.getAttribute("src")) sourceEl.setAttribute("src", dataSrc);
      p.addEventListener("play", () => {
        allPlayers.forEach((other) => {
          if (other !== p) try { other.pause(); } catch (e) {}
        });
        const card = p.closest(".sound-card");
        if (card) card.classList.add("playing");
      });
      p.addEventListener("pause", () => {
        const card = p.closest(".sound-card");
        if (card) card.classList.remove("playing");
      });
    });

    // allow Enter key on focused sound-card to play/pause
    $$(".sound-card").forEach((card) => {
      card.addEventListener("keyup", (ev) => {
        if (ev.key === "Enter") {
          const ap = card.querySelector(".audio-player");
          if (ap) {
            try { if (ap.paused) ap.play(); else ap.pause(); } catch(e) {}
          }
        }
      });
    });
  }

  /* -------------------- Feedback Buttons -------------------- */
  function initFeedback() {
    on(document.body, "click", ".btn-feedback", async function (ev, btn) {
      ev.preventDefault();
      const sonido = btn.dataset.sonido;
      const accion = btn.dataset.accion;
      // emotion name from DOM
      const emotionElem = document.querySelector(".emotion-chip") || document.querySelector(".emotion-name") || document.querySelector(".emotion-name");
      const emocion = emotionElem ? emotionElem.textContent.trim() : null;
      if (!emocion || !sonido) return;

      btn.disabled = true;
      try {
        const res = await fetch("/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ emocion: emocion, sonido_id: sonido, accion: accion })
        });
        const j = await res.json();
        if (j.ok) {
          btn.classList.add("sent");
          // micro animation
          btn.animate([{ transform: "scale(1)" }, { transform: "scale(1.06)" }, { transform: "scale(1)" }], { duration: 380, easing: "cubic-bezier(.2,.9,.3,1)" });
        } else {
          console.warn("Feedback error:", j);
          btn.disabled = false;
        }
      } catch (err) {
        console.error("Error sending feedback:", err);
        btn.disabled = false;
      }
    });
  }

  /* -------------------- Modal: Teach / Label -------------------- */
  function initLabelModal() {
    // Open modal robustly: delegation + direct binding
    function openModalPopulate(aliasHint) {
      const modal = $("#label-modal");
      if (!modal) {
        console.warn("#label-modal not found in DOM.");
        return;
      }
      const aliasInput = $("#alias-input");
      if (aliasInput && aliasHint) aliasInput.value = aliasHint;
      modal.setAttribute("aria-hidden", "false");
      modal.style.display = "flex";
      // small focus trap: focus first interactive element
      if (aliasInput) aliasInput.focus();
    }

    // Delegated click on #open-label (works even if element added later)
    on(document.body, "click", "#open-label", (ev, btn) => {
      ev.preventDefault();
      // if server injected a global hint use it; else attempt to read from DOM
      const hint = window.__ALIAS_HINT__ || (document.querySelector(".label-suggest strong") ? document.querySelector(".label-suggest strong").textContent.trim() : "");
      openModalPopulate(hint);
    });

    // Also try to bind direct button if present
    const directOpen = $("#open-label");
    if (directOpen) directOpen.addEventListener("click", (ev) => {
      ev.preventDefault();
      const hint = window.__ALIAS_HINT__ || (document.querySelector(".label-suggest strong") ? document.querySelector(".label-suggest strong").textContent.trim() : "");
      openModalPopulate(hint);
    });

    // Cancel close
    on(document.body, "click", "#label-cancel", (ev) => {
      ev.preventDefault();
      const modal = $("#label-modal");
      if (modal) {
        modal.setAttribute("aria-hidden", "true");
        modal.style.display = "none";
      }
    });

    // Show/Hide new-target input
    const select = $("#target-select");
    if (select) {
      select.addEventListener("change", () => {
        const newInput = $("#target-new");
        if (!newInput) return;
        if (select.value === "_new") newInput.style.display = "block";
        else newInput.style.display = "none";
      });
    }

    // Submit save (delegated - button may be dynamic)
    on(document.body, "click", "#label-save", async function (ev, btn) {
      ev.preventDefault();
      const modal = $("#label-modal");
      const aliasInput = $("#alias-input");
      const targetSelect = $("#target-select");
      const targetNew = $("#target-new");
      const aliasMsg = $("#alias-msg");
      const status = $("#label-status");
      if (!aliasInput || !targetSelect || !status) {
        console.warn("Label form elements missing in DOM.");
        return;
      }
      const alias = aliasInput.value.trim();
      const chosen = targetSelect.value === "_new" ? (targetNew ? targetNew.value.trim() : "") : targetSelect.value;
      const message = aliasMsg ? aliasMsg.value.trim() : "";
      if (!alias || !chosen) {
        status.textContent = "Complete alias y emoción objetivo.";
        return;
      }

      btn.disabled = true;
      status.textContent = "Guardando...";

      try {
        const res = await fetch("/label", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ alias: alias, target_emotion: chosen, message: message })
        });
        const j = await res.json();
        if (j.ok) {
          status.textContent = "Guardado. Melody reconocerá esa palabra.";
          setTimeout(() => {
            if (modal) {
              modal.setAttribute("aria-hidden", "true");
              modal.style.display = "none";
            }
            // refresh to reflect change immediately (reload memory from server-side)
            location.reload();
          }, 900);
        } else {
          status.textContent = "Error: " + (j.error || "no se pudo guardar");
          btn.disabled = false;
        }
      } catch (err) {
        status.textContent = "Error de red: " + String(err);
        btn.disabled = false;
      }
    });

    // Allow Esc to close modal
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape") {
        const modal = $("#label-modal");
        if (modal && modal.getAttribute("aria-hidden") === "false") {
          modal.setAttribute("aria-hidden", "true");
          modal.style.display = "none";
        }
      }
    });

    // Auto-open modal if server asked for labeling by setting window.__AUTO_OPEN_LABEL__ = true and window.__ALIAS_HINT__.
    // Template engine can inject these variables before loading this script:
    // <script>window.__ALIAS_HINT__ = "{{ respuesta.alias_hint }}"; window.__AUTO_OPEN_LABEL__ = true;</script>
    if (window.__AUTO_OPEN_LABEL__) {
      const aliasHint = window.__ALIAS_HINT__ || (document.querySelector(".label-suggest strong") ? document.querySelector(".label-suggest strong").textContent.trim() : "");
      setTimeout(() => { // slight delay to ensure DOM ready
        const modal = $("#label-modal");
        if (modal) {
          modal.setAttribute("aria-hidden", "false");
          modal.style.display = "flex";
          const aliasInput = $("#alias-input");
          if (aliasInput && aliasHint) aliasInput.value = aliasHint;
          if (aliasInput) aliasInput.focus();
        }
      }, 220);
    }
  }

  /* -------------------- Initialization bootstrap -------------------- */
  ready(() => {
    try { initParticles(); } catch (e) { console.warn("Particles init failed:", e); }
    try { initUI(); } catch (e) { console.warn("UI init failed:", e); }
    try { initFeedback(); } catch (e) { console.warn("Feedback init failed:", e); }
    try { initLabelModal(); } catch (e) { console.warn("Label modal init failed:", e); }
  });

})();
