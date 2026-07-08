// Ferragens Vitória — interações da página institucional (Nível 1)

document.addEventListener("DOMContentLoaded", () => {
  initHeaderScroll();
  initMobileNav();
  initCountUp();
});

/**
 * Adiciona sombra ao header quando a página é rolada,
 * para dar profundidade sem depender de JS decorativo apenas.
 */
function initHeaderScroll() {
  const header = document.getElementById("site-header");
  if (!header) return;

  const onScroll = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/**
 * Abre/fecha o menu de navegação em telas pequenas.
 */
function initMobileNav() {
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  // fecha o menu ao clicar em um link (útil em telas pequenas)
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

/**
 * Anima os números da seção de estatísticas contando de 0 até o valor
 * definido em data-count, disparado quando a seção entra na tela.
 */
function initCountUp() {
  const statNumbers = document.querySelectorAll(".stat-number");
  if (!statNumbers.length) return;

  const animate = (el) => {
    const target = Number(el.dataset.count || 0);
    const duration = 1200;
    const start = performance.now();

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cúbico
      const value = Math.round(target * eased);
      el.textContent = value.toLocaleString("pt-BR");

      if (progress < 1) {
        requestAnimationFrame(step);
      }
    };

    requestAnimationFrame(step);
  };

  if (!("IntersectionObserver" in window)) {
    statNumbers.forEach(animate);
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );

  statNumbers.forEach((el) => observer.observe(el));
}
