/* LearnHub — Main JS */

// ── Auto-dismiss flash messages ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Fade out alerts after 5s
  setTimeout(() => {
    document.querySelectorAll('#flash-messages .alert').forEach(el => {
      el.classList.remove('show');
      setTimeout(() => el.remove(), 400);
    });
  }, 5000);

  // ── OTP Input: auto-focus digits ────────────────────────────────────────
  const otpInput = document.querySelector('.otp-input');
  if (otpInput) {
    otpInput.addEventListener('input', e => {
      e.target.value = e.target.value.replace(/\D/g, '').slice(0, 6);
      if (e.target.value.length === 6) {
        e.target.closest('form').submit();
      }
    });
  }

  // ── Course thumbnail preview ────────────────────────────────────────────
  const thumbInput = document.getElementById('id_thumbnail');
  const thumbPreview = document.getElementById('thumbnail-preview');
  if (thumbInput && thumbPreview) {
    thumbInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = ev => { thumbPreview.src = ev.target.result; thumbPreview.style.display = 'block'; };
        reader.readAsDataURL(file);
      }
    });
  }

  // ── Navbar scroll effect ────────────────────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.background = window.scrollY > 20
        ? 'rgba(9,9,18,0.97)'
        : 'rgba(15,15,26,0.85)';
    });
  }

  // ── Confirm delete dialogs ──────────────────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });

  // ── Animated counter for stat cards ────────────────────────────────────
  document.querySelectorAll('.stat-value[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count, 10);
    let current = 0;
    const increment = Math.ceil(target / 40);
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = current.toLocaleString();
    }, 30);
  });
});
