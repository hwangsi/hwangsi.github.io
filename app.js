(() => {
  'use strict';
  const cards = [...document.querySelectorAll('.project')];
  const search = document.querySelector('#search');
  const origin = document.querySelector('#origin');
  const sort = document.querySelector('#sort');
  const buttons = [...document.querySelectorAll('.category')];
  const grid = document.querySelector('#project-grid');
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty');
  const validCategories = new Set(buttons.map(b => b.dataset.category));
  let category = 'all';
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
  const originalOrder = new Map(cards.map((card, i) => [card, i]));
  function readState() {
    const p = new URLSearchParams(location.search);
    search.value = p.get('q') || '';
    category = validCategories.has(p.get('category')) ? p.get('category') : 'all';
    origin.value = ['all', 'original', 'fork'].includes(p.get('type')) ? p.get('type') : 'all';
    sort.value = ['featured', 'recent', 'name'].includes(p.get('sort')) ? p.get('sort') : 'featured';
  }
  function apply(updateUrl = true) {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    const ordered = [...cards].sort((a, b) => {
      if (sort.value === 'recent') return b.dataset.updated.localeCompare(a.dataset.updated);
      if (sort.value === 'name') return a.dataset.name.localeCompare(b.dataset.name, 'en', {sensitivity:'base'});
      return originalOrder.get(a) - originalOrder.get(b);
    });
    let visible = 0;
    ordered.forEach(card => {
      const match = (category === 'all' || card.dataset.category === category)
        && (origin.value === 'all' || card.dataset.type === origin.value)
        && terms.every(t => normalize(card.textContent).includes(t));
      card.hidden = !match;
      if (match) visible++;
      grid.append(card);
    });
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.category === category)));
    count.textContent = `${visible}개 프로젝트 / 전체 ${cards.length}개`;
    empty.hidden = visible !== 0;
    if (updateUrl) {
      const p = new URLSearchParams();
      if (search.value.trim()) p.set('q', search.value.trim());
      if (category !== 'all') p.set('category', category);
      if (origin.value !== 'all') p.set('type', origin.value);
      if (sort.value !== 'featured') p.set('sort', sort.value);
      history.replaceState(null, '', location.pathname + (p.size ? '?' + p.toString() : '') + location.hash);
    }
  }
  search.addEventListener('input', () => apply());
  origin.addEventListener('change', () => apply());
  sort.addEventListener('change', () => apply());
  buttons.forEach(b => b.addEventListener('click', () => { category = b.dataset.category; apply(); }));
  document.querySelectorAll('[data-reset]').forEach(b => b.addEventListener('click', () => {
    search.value = ''; category = 'all'; origin.value = 'all'; sort.value = 'featured'; apply(); search.focus();
  }));
  window.addEventListener('popstate', () => { readState(); apply(false); });
  readState(); apply(false);
})();
