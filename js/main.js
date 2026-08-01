/* TravelDore — main.js */
document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Loading screen ---------- */
  const loader = document.getElementById('loader');
  window.addEventListener('load', () => {
    setTimeout(() => loader && loader.classList.add('hide'), 400);
  });
  // fallback in case 'load' already fired
  setTimeout(() => loader && loader.classList.add('hide'), 1800);

  /* ---------- Scroll progress bar ---------- */
  const progress = document.getElementById('scroll-progress');
  const onScroll = () => {
    if (progress) {
      const h = document.documentElement;
      const scrolled = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
      progress.style.width = scrolled + '%';
    }
    const header = document.getElementById('site-header');
    if (header) header.classList.toggle('scrolled', window.scrollY > 60);
  };
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Cursor glow (desktop only) ---------- */
  const glow = document.getElementById('cursor-glow');
  if (glow && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    window.addEventListener('mousemove', (e) => {
      glow.style.left = e.clientX + 'px';
      glow.style.top = e.clientY + 'px';
    });
  } else if (glow) {
    glow.style.display = 'none';
  }

  /* ---------- Mobile nav ---------- */
  const navToggle = document.getElementById('nav-toggle');
  const mobilePanel = document.getElementById('mobile-panel');
  const mobileClose = document.getElementById('mobile-close');
  if (navToggle && mobilePanel) {
    navToggle.addEventListener('click', () => mobilePanel.classList.add('open'));
    mobileClose && mobileClose.addEventListener('click', () => mobilePanel.classList.remove('open'));
    mobilePanel.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobilePanel.classList.remove('open')));
  }

  /* ---------- Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('.reveal, .reveal-scale, .stagger > *');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach((el, i) => {
    if (el.classList.contains('stagger') === false) el.style.setProperty('--i', i % 8);
    io.observe(el);
  });
  document.querySelectorAll('.stagger').forEach(group => {
    Array.from(group.children).forEach((child, i) => {
      child.classList.add('reveal');
      child.style.setProperty('--i', i);
      io.observe(child);
    });
  });

  /* ---------- Testimonials carousel ---------- */
  const track = document.getElementById('testi-slides');
  if (track) {
    const slides = track.children.length;
    let idx = 0;
    const dotsWrap = document.getElementById('testi-dots');
    for (let i = 0; i < slides; i++) {
      const b = document.createElement('button');
      if (i === 0) b.classList.add('active');
      b.addEventListener('click', () => go(i));
      dotsWrap.appendChild(b);
    }
    function go(i) {
      idx = (i + slides) % slides;
      track.style.transform = `translateX(-${idx * 100}%)`;
      dotsWrap.querySelectorAll('button').forEach((d, di) => d.classList.toggle('active', di === idx));
    }
    document.getElementById('testi-prev')?.addEventListener('click', () => go(idx - 1));
    document.getElementById('testi-next')?.addEventListener('click', () => go(idx + 1));
    let auto = setInterval(() => go(idx + 1), 6000);
    track.closest('.testi-wrap').addEventListener('mouseenter', () => clearInterval(auto));
    track.closest('.testi-wrap').addEventListener('mouseleave', () => auto = setInterval(() => go(idx + 1), 6000));
  }

  /* ---------- Gallery filters + lightbox ---------- */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const items = document.querySelectorAll('.masonry-item');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.filter;
      items.forEach(it => {
        const show = cat === 'all' || it.dataset.category === cat;
        it.style.display = show ? '' : 'none';
      });
    });
  });
  const lightbox = document.getElementById('lightbox');
  if (lightbox) {
    const lbImg = document.getElementById('lb-img');
    items.forEach(it => {
      it.addEventListener('click', () => {
        lbImg.src = it.querySelector('img').src;
        lightbox.classList.add('open');
      });
    });
    lightbox.addEventListener('click', () => lightbox.classList.remove('open'));
  }

  /* ---------- Purpose chip selector (inquiry form) ---------- */
  const chips = document.querySelectorAll('.purpose-chip');
  const purposeInput = document.getElementById('purpose-value');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      if (purposeInput) purposeInput.value = chip.dataset.value;
    });
  });

  /* ---------- Inquiry form submit (demo) ---------- */
  const inquiryForm = document.getElementById('inquiry-form');
  if (inquiryForm) {
    inquiryForm.addEventListener('submit', (e) => {
      e.preventDefault();
      inquiryForm.style.display = 'none';
      document.getElementById('form-success')?.classList.add('show');
    });
  }

  /* ---------- WhatsApp chat box ---------- */
  const waFloat = document.getElementById('wa-float');
  const waBox = document.getElementById('wa-box');
  const waClose = document.getElementById('wa-close');
  waFloat?.addEventListener('click', () => waBox.classList.toggle('open'));
  waClose?.addEventListener('click', () => waBox.classList.remove('open'));

  /* ---------- Set active nav link ---------- */
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-panel a').forEach(a => {
    const href = a.getAttribute('href').split('/').pop();
    if (href === path) a.classList.add('active');
  });

});
