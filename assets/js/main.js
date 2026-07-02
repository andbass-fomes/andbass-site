/* andbass.com — reveal on scroll + lightbox + deck fan-out + custom cursor */
(function () {
  // Reveal
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // ---------- Deck fan-out (home) ----------
  var deck = document.getElementById('deck');
  if (deck) {
    var strip = document.getElementById('strip');
    var main = document.getElementById('deckMain');
    var items = Array.prototype.slice.call(strip.querySelectorAll('.strip-item'));
    var base = 0, drag = 0, down = false, startX = 0, dragStart = 0, moved = 0;
    strip.querySelectorAll('img,a').forEach(function (el) { el.setAttribute('draggable', 'false'); });

    function apply() {
      strip.style.transform = 'translateX(' + (base + drag) + 'px)';
    }
    function layout() {
      var mainCenter = strip.offsetLeft + main.offsetLeft + main.offsetWidth / 2;
      base = deck.clientWidth / 2 - mainCenter;
      apply();
      var mc = main.offsetLeft + main.offsetWidth / 2;
      var half = items.length / 2;
      items.forEach(function (el, i) {
        var c = el.offsetLeft + el.offsetWidth / 2;
        el.style.setProperty('--dx', (mc - c) + 'px');
        var dist = i < half ? half - i : i - half + 1;
        el.style.setProperty('--d', (dist * 0.045) + 's');
      });
    }
    function openDeck() { deck.classList.add('open'); }
    function closeDeck() {
      deck.classList.remove('open');
      drag = 0; strip.classList.remove('dragging'); apply();
    }

    window.addEventListener('load', layout);
    window.addEventListener('resize', layout);
    layout();

    main.addEventListener('mouseenter', openDeck);
    deck.addEventListener('mouseleave', function () { if (!down) closeDeck(); });
    deck.addEventListener('focusin', openDeck);
    deck.addEventListener('focusout', function (e) { if (!deck.contains(e.relatedTarget)) closeDeck(); });

    deck.addEventListener('pointerdown', function (e) {
      if (!deck.classList.contains('open')) {
        if (e.target.closest && e.target.closest('#deckMain')) openDeck();
        return;
      }
      e.preventDefault();
      down = true; moved = 0; startX = e.clientX; dragStart = drag;
      strip.classList.add('dragging');
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      drag = dragStart + (e.clientX - startX);
      moved = Math.max(moved, Math.abs(e.clientX - startX));
      apply();
    });
    function endDrag() {
      if (!down) return;
      down = false; strip.classList.remove('dragging');
      if (!deck.matches(':hover')) closeDeck();
      setTimeout(function () { moved = 0; }, 0);
    }
    window.addEventListener('pointerup', endDrag);
    window.addEventListener('pointercancel', endDrag);
    deck.addEventListener('click', function (e) {
      if (moved > 6) { e.preventDefault(); e.stopPropagation(); }
      moved = 0;
    }, true);
  }

  // ---------- Custom cursor ----------
  var cur = document.getElementById('cursor');
  if (cur && window.matchMedia('(pointer:fine)').matches) {
    document.addEventListener('mousemove', function (e) {
      cur.style.left = e.clientX + 'px';
      cur.style.top = e.clientY + 'px';
      cur.classList.add('on');
    });
    document.addEventListener('mouseleave', function () { cur.classList.remove('on'); });
    document.addEventListener('mouseover', function (e) {
      var overDeck = deck && deck.classList.contains('open') && deck.contains(e.target);
      var overLink = e.target.closest && e.target.closest('a,button,.g-item');
      cur.classList.toggle('grab', !!overDeck);
      cur.classList.toggle('link', !overDeck && !!overLink);
    });
  }

  // ---------- Lightbox ----------
  var lb = document.getElementById('lightbox');
  if (!lb) return;
  var img = lb.querySelector('img');
  var count = lb.querySelector('.lb-count');
  var gitems = Array.prototype.slice.call(document.querySelectorAll('.g-item img'));
  if (!gitems.length) return;
  var idx = 0;

  function show(i) {
    idx = (i + gitems.length) % gitems.length;
    img.src = gitems[idx].getAttribute('data-full') || gitems[idx].src;
    img.alt = gitems[idx].alt;
    count.textContent = (idx + 1) + ' / ' + gitems.length;
  }
  function open(i) { show(i); lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; }
  function close() { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; img.src = ''; }

  gitems.forEach(function (el, i) { el.parentElement.addEventListener('click', function () { open(i); }); });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
  lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
})();
