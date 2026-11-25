/**
 * PRAHARIX 3.0 - Accessibility Controller
 * WCAG 2.2 AA Compliance - Items #11-18
 */

(function() {
  'use strict';

  // ── #15: High Contrast Mode ─────────────────────────────
  const contrastBtn = document.getElementById('toggle-contrast');
  if (contrastBtn) {
    const isHighContrast = localStorage.getItem('praharix-high-contrast') === '1';
    if (isHighContrast) document.body.classList.add('high-contrast');
    contrastBtn.setAttribute('aria-pressed', String(isHighContrast));
    contrastBtn.addEventListener('click', function() {
      document.body.classList.toggle('high-contrast');
      const active = document.body.classList.contains('high-contrast');
      localStorage.setItem('praharix-high-contrast', active ? '1' : '0');
      contrastBtn.setAttribute('aria-pressed', String(active));
      announce(active ? 'High contrast mode enabled' : 'High contrast mode disabled');
    });
  }

  // ── #16: Font Size Adjustment ───────────────────────────
  const fontBtns = document.querySelectorAll('[data-font-size]');
  fontBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const size = btn.getAttribute('data-font-size');
      document.documentElement.setAttribute('data-font-size', size);
      const sizes = { 'sm': '14px', 'md': '16px', 'lg': '18px', 'xl': '20px' };
      document.documentElement.style.fontSize = sizes[size] || '16px';
      localStorage.setItem('praharix-font-size', size);
      fontBtns.forEach(b => b.setAttribute('aria-pressed', 'false'));
      btn.setAttribute('aria-pressed', 'true');
      announce('Font size changed to ' + size);
    });
  });
  // Restore saved font size
  const savedFont = localStorage.getItem('praharix-font-size');
  if (savedFont) {
    const sizes = { 'sm': '14px', 'md': '16px', 'lg': '18px', 'xl': '20px' };
    document.documentElement.style.fontSize = sizes[savedFont] || '16px';
  }

  // ── #17: Language Switcher ──────────────────────────────
  const langBtns = document.querySelectorAll('[data-lang]');
  langBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const lang = btn.getAttribute('data-lang');
      localStorage.setItem('praharix-lang', lang);
      langBtns.forEach(b => {
        b.setAttribute('aria-pressed', 'false');
        b.classList.remove('active');
      });
      btn.setAttribute('aria-pressed', 'true');
      btn.classList.add('active');
      // Update SITREP text if present
      updateSitrepLang(lang);
      announce('Language changed to ' + (lang === 'en' ? 'English' : lang === 'hi' ? 'Hindi' : 'Marathi'));
    });
  });
  // Restore saved lang
  const savedLang = localStorage.getItem('praharix-lang');
  if (savedLang) {
    langBtns.forEach(b => {
      if (b.getAttribute('data-lang') === savedLang) {
        b.setAttribute('aria-pressed', 'true');
        b.classList.add('active');
      }
    });
  }

  function updateSitrepLang(lang) {
    const sitrepEl = document.getElementById('sitrep-text');
    if (!sitrepEl) return;
    fetch('/api/sitrep/text?lang=' + lang)
      .then(r => r.json())
      .then(data => { sitrepEl.textContent = data.text; })
      .catch(function() {});
  }

  // ── ARIA Live Region Announcer ──────────────────────────
  function announce(msg) {
    let region = document.getElementById('a11y-announcer');
    if (!region) {
      region = document.createElement('div');
      region.id = 'a11y-announcer';
      region.setAttribute('aria-live', 'polite');
      region.setAttribute('aria-atomic', 'true');
      region.className = 'sr-only';
      document.body.appendChild(region);
    }
    region.textContent = '';
    setTimeout(function() { region.textContent = msg; }, 50);
  }

  // ── #13: Keyboard Navigation Enhancements ───────────────
  document.addEventListener('keydown', function(e) {
    // ESC closes modals
    if (e.key === 'Escape') {
      const openModals = document.querySelectorAll('.modal.show');
      openModals.forEach(function(m) {
        const closeBtn = m.querySelector('[data-bs-dismiss="modal"], .btn-close');
        if (closeBtn) closeBtn.click();
      });
    }
  });

  // ── #18: Form Accessibility ─────────────────────────────
  document.querySelectorAll('form').forEach(function(form) {
    // Add aria-required to required fields
    form.querySelectorAll('[required]').forEach(function(field) {
      field.setAttribute('aria-required', 'true');
      const label = form.querySelector('label[for="' + field.id + '"]');
      if (label && !label.querySelector('.required-mark')) {
        const mark = document.createElement('span');
        mark.className = 'required-mark';
        mark.setAttribute('aria-hidden', 'true');
        mark.textContent = ' *';
        label.appendChild(mark);
      }
    });

    // Client-side validation with error descriptions
    form.addEventListener('submit', function(e) {
      let valid = true;
      form.querySelectorAll('[required]').forEach(function(field) {
        if (!field.value.trim()) {
          valid = false;
          field.setAttribute('aria-invalid', 'true');
          let errId = field.id + '-error';
          let errEl = document.getElementById(errId);
          if (!errEl) {
            errEl = document.createElement('span');
            errEl.id = errId;
            errEl.className = 'text-danger small';
            errEl.setAttribute('role', 'alert');
            field.parentNode.appendChild(errEl);
          }
          errEl.textContent = field.getAttribute('data-error') || 'This field is required';
          field.setAttribute('aria-describedby', errId);
        } else {
          field.setAttribute('aria-invalid', 'false');
        }
      });
      if (!valid) e.preventDefault();
    });
  });

})();
