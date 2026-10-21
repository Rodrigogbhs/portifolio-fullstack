/* Melhoria progressiva: navegação e notícias complementam o HTML estático. */
(() => {
  const portraits = Array.from(document.querySelectorAll('.portrait-reveal'));
  const clearPortraits = () => portraits.forEach(portrait => portrait.classList.remove('mouse-over'));
  portraits.forEach(portrait => {
    const trackPointer = event => portrait.classList.toggle('mouse-over', event.pointerType === 'mouse');
    portrait.addEventListener('pointerenter', trackPointer);
    portrait.addEventListener('pointermove', trackPointer);
    portrait.addEventListener('pointerleave', () => portrait.classList.remove('mouse-over'));
    portrait.addEventListener('pointercancel', () => portrait.classList.remove('mouse-over'));
  });
  document.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse') clearPortraits();
  }, {passive: true});
  window.addEventListener('blur', clearPortraits);

  const tabs = Array.from(document.querySelectorAll('.os-tabs [role="tab"]'));
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  if (tabs.length && panels.every(Boolean)) {
    function selectTab(index, focus = false) {
      tabs.forEach((tab, position) => {
        const selected = position === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[position].hidden = !selected;
      });
      if (focus) tabs[index].focus();
    }
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => selectTab(index));
      tab.addEventListener('keydown', event => {
        const next = {ArrowRight: (index + 1) % tabs.length, ArrowLeft: (index + tabs.length - 1) % tabs.length, Home: 0, End: tabs.length - 1}[event.key];
        if (next === undefined) return;
        event.preventDefault();
        selectTab(next, true);
      });
    });
    selectTab(0);
    document.querySelector('.os-tabs').hidden = false;
  }

  const menuButton = document.querySelector('.menu-toggle');
  const header = document.querySelector('.site-header');
  if (menuButton && header) {
    function setMenu(open) {
      header.classList.toggle('menu-open', open);
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.textContent = open ? 'Fechar −' : 'Menu +';
    }
    menuButton.hidden = false;
    document.documentElement.classList.add('root-ready');
    menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
    document.querySelectorAll('.site-nav a').forEach(link => link.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuButton.focus();
      }
    });
    matchMedia('(min-width: 621px)').addEventListener('change', event => {
      if (event.matches) setMenu(false);
    });
  }

  const listing = document.getElementById('recent-posts');
  if (!listing) return;
  const dateLabel = new Intl.DateTimeFormat('pt-BR', {timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit', year: 'numeric'});
  fetch('blog/posts.json', {cache: 'no-cache'})
    .then(response => response.ok ? response.json() : null)
    .then(posts => {
      if (!Array.isArray(posts)) return;
      const visible = posts.filter(post =>
        post && typeof post.slug === 'string' && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(post.slug) &&
        typeof post.title === 'string' && typeof post.category === 'string' &&
        typeof post.published_at === 'string' && Number.isFinite(Date.parse(post.published_at)) &&
        Date.parse(post.published_at) <= Date.now()
      ).sort((a, b) => Date.parse(b.published_at) - Date.parse(a.published_at)).slice(0, 3);
      if (!visible.length) return;
      const links = visible.map(post => {
        const link = document.createElement('a');
        link.className = 'blog-entry';
        link.href = `blog/${post.slug}.html`;
        const time = document.createElement('time');
        time.dateTime = post.published_at;
        time.textContent = dateLabel.format(new Date(post.published_at)).replaceAll('/', '.');
        const text = document.createElement('div');
        const category = document.createElement('p');
        category.textContent = post.category;
        const title = document.createElement('h3');
        title.textContent = post.title;
        const arrow = document.createElement('span');
        arrow.textContent = '↗';
        arrow.setAttribute('aria-hidden', 'true');
        text.append(category, title);
        link.append(time, text, arrow);
        return link;
      });
      listing.replaceChildren(...links);
    })
    .catch(() => {
      // Sem rede, continuam disponíveis as notícias e o link do blog no HTML.
    });
})();
