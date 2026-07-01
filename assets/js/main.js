/* andbass.com — reveal on scroll + lightbox */
(function () {
  // Reveal
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // Lightbox
  var lb = document.getElementById('lightbox');
  if (!lb) return;
  var img = lb.querySelector('img');
  var count = lb.querySelector('.lb-count');
  var items = Array.prototype.slice.call(document.querySelectorAll('.g-item img'));
  if (!items.length) return;
  var idx = 0;

  function show(i) {
    idx = (i + items.length) % items.length;
    img.src = items[idx].getAttribute('data-full') || items[idx].src;
    img.alt = items[idx].alt;
    count.textContent = (idx + 1) + ' / ' + items.length;
  }
  function open(i) { show(i); lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; }
  function close() { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; img.src = ''; }

  items.forEach(function (el, i) { el.parentElement.addEventListener('click', function () { open(i); }); });
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
