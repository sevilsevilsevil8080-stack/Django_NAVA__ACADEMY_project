const mobileMenu = document.getElementById("mobileMenu");
const mainNav = document.getElementById("mainNav");

mobileMenu?.addEventListener("click", () => {
  const open = mainNav.classList.toggle("open");
  mobileMenu.setAttribute("aria-expanded", open);
});

document.querySelectorAll(".main-nav a").forEach(link => {
  link.addEventListener("click", () => mainNav.classList.remove("open"));
});

const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll(".main-nav a");
window.addEventListener("scroll", () => {
  let current = "top";
  sections.forEach(section => {
    if (window.scrollY >= section.offsetTop - 160) current = section.id;
  });
  navLinks.forEach(link => link.classList.toggle("active", link.getAttribute("href") === "#" + current));

  document.getElementById("backTop")?.classList.toggle("show", window.scrollY > 500);
});

document.getElementById("backTop")?.addEventListener("click", () => {
  window.scrollTo({top:0, behavior:"smooth"});
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, {threshold: .12});

document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

const persianDigits = "۰۱۲۳۴۵۶۷۸۹";
const toPersian = n => String(n).replace(/\d/g, d => persianDigits[d]);

const counterObserver = new IntersectionObserver((entries, obs) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = Number(el.dataset.counter);
    const duration = 1200;
    const start = performance.now();
    const tick = now => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = toPersian(Math.round(target * eased));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    obs.unobserve(el);
  });
}, {threshold:.7});

document.querySelectorAll("[data-counter]").forEach(el => counterObserver.observe(el));

document.getElementById("newsletterForm")?.addEventListener("submit", e => {
  e.preventDefault();
  const msg = document.getElementById("newsletterMsg");
  msg.textContent = "ایمیل شما با موفقیت ثبت شد ✓";
  e.target.reset();
});

document.querySelectorAll(".course-card .course-footer a").forEach(a => {
  a.addEventListener("click", e => e.preventDefault());
});
