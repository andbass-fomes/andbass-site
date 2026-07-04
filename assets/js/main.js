/* andbass.com — reveal on scroll + lightbox + deck fan-out + custom cursor */
(function () {
  // Reveal
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // ---------- Deck fan-out (home) — native scroll + snap + infinite loop ----------
  var deck = document.getElementById('deck');
  if (deck) {
    var strip = document.getElementById('strip');
    var main = document.getElementById('deckMain');
    var isTouch = window.matchMedia('(hover: none)').matches;
    var down = false, startX = 0, startL = 0, moved = 0;

    // Build 3 copies of the sequence for the infinite loop
    var seq = Array.prototype.slice.call(strip.children);
    var seqLen = seq.length;
    var mainPos = seq.indexOf(main);
    function makeClone(el) {
      var c = el.cloneNode(true);
      c.removeAttribute('id');
      c.setAttribute('aria-hidden', 'true');
      c.setAttribute('tabindex', '-1');
      return c;
    }
    for (var rep = 0; rep < 2; rep++) {
      for (var k = seqLen - 1; k >= 0; k--) strip.insertBefore(makeClone(seq[k]), strip.firstChild);
      for (var k2 = 0; k2 < seqLen; k2++) strip.appendChild(makeClone(seq[k2]));
    }
    var all = Array.prototype.slice.call(strip.children);
    strip.querySelectorAll('img,a').forEach(function (el) { el.setAttribute('draggable', 'false'); });

    var cycle = 0;
    function measure() { cycle = all[seqLen].offsetLeft - all[0].offsetLeft; }
    function centerMain(smooth) {
      var x = main.offsetLeft + main.offsetWidth / 2 - deck.clientWidth / 2;
      deck.scrollTo({ left: x, behavior: smooth ? 'smooth' : 'auto' });
    }
    function layout() {
      measure();
      all.forEach(function (el, idx) {
        var pos = idx % seqLen;
        if (pos === mainPos) return;
        var card = all[idx - pos + mainPos];
        var mc = card.offsetLeft + card.offsetWidth / 2;
        var c = el.offsetLeft + el.offsetWidth / 2;
        el.style.setProperty('--dx', (mc - c) + 'px');
        var dist = Math.abs(pos - mainPos);
        el.style.setProperty('--d', (dist * 0.045) + 's');
      });
      centerMain(false);
      updateScales();
    }
    function openDeck() { deck.classList.add('open'); }
    function closeDeck() { deck.classList.remove('open'); centerMain(true); }
    function updateScales() {
      var center = deck.scrollLeft + deck.clientWidth / 2;
      var r = Math.max(260, deck.clientWidth * 0.22);
      all.forEach(function (el) {
        var d = Math.abs(el.offsetLeft + el.offsetWidth / 2 - center);
        var t = Math.max(0, 1 - d / r);
        var img = el.querySelector('img');
        if (img) img.style.setProperty('--s', (1 + 0.53 * t).toFixed(3));
        el.style.zIndex = t > 0.5 ? 3 : (el.classList.contains('deck-card') ? 2 : 1);
      });
    }
    // Invisible re-anchor: keep the scroll inside the middle copy.
    // Never jump mid-momentum (it kills the fling on mobile): wrap when idle,
    // or as an emergency only near the real end of the track.
    function wrapNow(idle) {
      if (!cycle || cycle < deck.clientWidth) return; // geometry not ready (images still loading)
      var anchor = main.offsetLeft + main.offsetWidth / 2 - deck.clientWidth / 2;
      var off = deck.scrollLeft - anchor;
      var limit = (idle || down) ? cycle / 2 : cycle * 1.9;
      if (Math.abs(off) <= limit) return;
      var n = Math.round(off / cycle) * cycle; // recover any number of laps at once
      deck.scrollLeft -= n;
      if (down) startL -= n;
    }
    var ticking = false, wrapTimer = null;
    deck.addEventListener('scroll', function () {
      clearTimeout(wrapTimer);
      wrapTimer = setTimeout(function () { wrapNow(true); }, 140);
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { wrapNow(false); updateScales(); ticking = false; });
    });
    function snapNearest() {
      var center = deck.scrollLeft + deck.clientWidth / 2;
      var best = null, bd = Infinity;
      all.forEach(function (el) {
        var d = Math.abs(el.offsetLeft + el.offsetWidth / 2 - center);
        if (d < bd) { bd = d; best = el; }
      });
      if (best) deck.scrollTo({ left: best.offsetLeft + best.offsetWidth / 2 - deck.clientWidth / 2, behavior: 'smooth' });
    }

    window.addEventListener('load', function () {
      layout();
      setTimeout(layout, 250); // beat browser scroll restoration / late layout shifts
    });
    // Re-measure once every image has actually loaded (slow networks)
    var pendingImgs = 0;
    strip.querySelectorAll('img').forEach(function (im) {
      if (im.complete) return;
      pendingImgs++;
      var done = function () { if (--pendingImgs === 0) layout(); };
      im.addEventListener('load', done);
      im.addEventListener('error', done);
    });
    window.addEventListener('resize', layout);
    layout();

    if (isTouch) {
      // Mobile: deck always open, native swipe with CSS snap
      openDeck();
    } else {
      all.forEach(function (el) {
        if (el.classList.contains('deck-card')) el.addEventListener('mouseenter', openDeck);
      });
      deck.addEventListener('mouseleave', function () { if (!down) closeDeck(); });
      deck.addEventListener('focusin', openDeck);
      deck.addEventListener('focusout', function (e) { if (!deck.contains(e.relatedTarget)) closeDeck(); });

      // Desktop: mouse drag drives native scroll, snaps on release
      deck.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        if (!deck.classList.contains('open')) {
          if (e.target.closest && e.target.closest('.deck-card')) openDeck();
          return;
        }
        e.preventDefault();
        down = true; moved = 0; startX = e.clientX; startL = deck.scrollLeft;
        deck.classList.add('dragging');
      });
      window.addEventListener('pointermove', function (e) {
        if (!down) return;
        deck.scrollLeft = startL - (e.clientX - startX);
        moved = Math.max(moved, Math.abs(e.clientX - startX));
      });
      function endDrag() {
        if (!down) return;
        down = false; deck.classList.remove('dragging');
        if (deck.matches(':hover')) snapNearest(); else closeDeck();
        setTimeout(function () { moved = 0; }, 0);
      }
      window.addEventListener('pointerup', endDrag);
      window.addEventListener('pointercancel', endDrag);
      deck.addEventListener('click', function (e) {
        if (moved > 6) { e.preventDefault(); e.stopPropagation(); }
        moved = 0;
      }, true);
    }
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
