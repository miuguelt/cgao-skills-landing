// ============================================================
// CGAO SKILLS - MAIN APPLICATION LOGIC
// ============================================================

console.log('%c🔥 CGAO SKILLS - La Fragua del Oriente 🔥', 'color: #39FF14; font-size: 20px; font-weight: bold;');
console.log('%cDesarrollado con pasión para el SENA', 'color: #FFBF00; font-size: 12px;');

// ============================================================
// COUNTDOWN TIMER
// ============================================================
(function () {
    // Target date: 5 de Mayo 2026 (Gran Final)
    const targetDate = new Date('2026-05-05T09:00:00').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = targetDate - now;

        if (distance < 0) {
            const daysEl = document.getElementById('days');
            if (daysEl) daysEl.textContent = '00';

            const hoursEl = document.getElementById('hours');
            if (hoursEl) hoursEl.textContent = '00';

            const minsEl = document.getElementById('minutes');
            if (minsEl) minsEl.textContent = '00';

            const secsEl = document.getElementById('seconds');
            if (secsEl) secsEl.textContent = '00';
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const daysEl = document.getElementById('days');
        if (daysEl) daysEl.textContent = String(days).padStart(2, '0');

        const hoursEl = document.getElementById('hours');
        if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');

        const minsEl = document.getElementById('minutes');
        if (minsEl) minsEl.textContent = String(minutes).padStart(2, '0');

        const secsEl = document.getElementById('seconds');
        if (secsEl) secsEl.textContent = String(seconds).padStart(2, '0');
    }

    // Update immediately and then every second
    updateCountdown();
    setInterval(updateCountdown, 1000);
})();

// ============================================================
// MOBILE MENU TOGGLE
// ============================================================
(function () {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
            const icon = menuBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });

        // Close menu when clicking links
        const menuLinks = mobileMenu.querySelectorAll('a');
        menuLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                mobileMenu.classList.add('hidden');
                const icon = menuBtn.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-times');
                }
            });
        });
    }
})();

// ============================================================
// NAVBAR SCROLL EFFECT
// ============================================================
(function () {
    const nav = document.querySelector('nav');

    if (nav) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 100) {
                nav.classList.add('bg-slate-900/80');
            } else {
                nav.classList.remove('bg-slate-900/80');
            }
        });
    }
})();

// ============================================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================================
(function () {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const navHeight = 64; // Height of fixed navbar
                const targetPosition = targetElement.offsetTop - navHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
})();

// ============================================================
// FORM SUBMISSION HANDLER
// ============================================================
(function () {
    const form = document.getElementById('registration-form');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Simple success animation
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                const originalText = btn.innerHTML;

                btn.innerHTML = '<i class="fas fa-check mr-2"></i> ¡Inscripción Exitosa!';
                btn.classList.remove('from-neon-green', 'to-amber-gold');
                btn.classList.add('from-green-500', 'to-green-600');

                setTimeout(function () {
                    btn.innerHTML = originalText;
                    btn.classList.add('from-neon-green', 'to-amber-gold');
                    btn.classList.remove('from-green-500', 'to-green-600');
                    form.reset();
                }, 3000);
            }
        });
    }
})();

// ============================================================
// INTERSECTION OBSERVER FOR ANIMATIONS
// ============================================================
(function () {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements (exclude fixed navbar and hero children which animate on load)
    document.querySelectorAll('section .glass, .skill-card').forEach(function (el) {
        if (!el.closest('#hero')) {
            el.style.opacity = '0';
            observer.observe(el);
        }
    });

    // Make hero elements and navbar always visible (handled by CSS animations or static)
    document.querySelectorAll('#hero .glass, #hero .animate-slide-up, nav').forEach(function (el) {
        el.style.opacity = '1';
    });
})();
