// A galeria e os links das imagens funcionam também sem JavaScript.
(function () {
  var galeria = document.getElementById('portfolio-galeria');
  if (galeria) {

    var projetos = Array.from(galeria.querySelectorAll('.projeto'));
    var anterior = document.getElementById('portfolio-anterior');
    var proximo = document.getElementById('portfolio-proximo');
    var contador = document.getElementById('portfolio-atual');
    var total = document.getElementById('portfolio-total');
    if (total) total.textContent = String(projetos.length).padStart(2, '0');
    var movimentoReduzido = matchMedia('(prefers-reduced-motion: reduce)');
    var atual = 0;

    function destinos() {
      var limite = galeria.scrollWidth - galeria.clientWidth;
      var inicio = projetos[0].offsetLeft;
      return projetos.map(function (projeto) {
        return Math.min(projeto.offsetLeft - inicio, limite);
      });
    }

    function atualizar() {
      var posicoes = destinos();
      atual = posicoes.reduce(function (maisPerto, posicao, indice) {
        return Math.abs(posicao - galeria.scrollLeft) < Math.abs(posicoes[maisPerto] - galeria.scrollLeft) ? indice : maisPerto;
      }, 0);
      anterior.disabled = atual === 0;
      proximo.disabled = atual === projetos.length - 1;
      contador.textContent = String(atual + 1).padStart(2, '0');
    }

    function irPara(indice) {
      galeria.scrollTo({ left: destinos()[indice], behavior: movimentoReduzido.matches ? 'instant' : 'smooth' });
    }

    anterior.addEventListener('click', function () { irPara(Math.max(0, atual - 1)); });
    proximo.addEventListener('click', function () { irPara(Math.min(projetos.length - 1, atual + 1)); });
    galeria.addEventListener('keydown', function (evento) {
      if (evento.target !== galeria) return;
      if (evento.key === 'ArrowRight') { evento.preventDefault(); irPara(Math.min(projetos.length - 1, atual + 1)); }
      if (evento.key === 'ArrowLeft') { evento.preventDefault(); irPara(Math.max(0, atual - 1)); }
      if (evento.key === 'Home') { evento.preventDefault(); irPara(0); }
      if (evento.key === 'End') { evento.preventDefault(); irPara(projetos.length - 1); }
    });
    galeria.addEventListener('scroll', atualizar, { passive: true });

    function redimensionar() {
      projetos.forEach(function (projeto) {
        var tela = projeto.querySelector('.projeto-tela');
        tela.style.setProperty('--previa-altura', tela.clientHeight + 'px');
      });
      atualizar();
    }
    if ('ResizeObserver' in window) new ResizeObserver(redimensionar).observe(galeria);
    else window.addEventListener('resize', redimensionar);
    redimensionar();
    document.querySelector('.portfolio-controles').hidden = false;
  }

  var dialog = document.getElementById('portfolio-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var conteudo = dialog.querySelector('.portfolio-dialog-conteudo');
  var titulo = document.getElementById('portfolio-dialog-titulo');

  document.querySelectorAll('.projeto-previa[data-projeto]').forEach(function (link) {
    link.addEventListener('click', function (evento) {
      if (evento.ctrlKey || evento.metaKey || evento.shiftKey || evento.altKey) return;
      evento.preventDefault();
      var imagem = link.querySelector('img').cloneNode();
      imagem.loading = 'eager';
      conteudo.replaceChildren(imagem);
      titulo.textContent = link.dataset.projeto;
      dialog.showModal();
      document.body.classList.add('portfolio-aberto');
      conteudo.scrollTop = 0;
    });
  });
  dialog.addEventListener('click', function (evento) {
    var caixa = dialog.getBoundingClientRect();
    if (evento.target === dialog && (evento.clientX < caixa.left || evento.clientX > caixa.right || evento.clientY < caixa.top || evento.clientY > caixa.bottom)) dialog.close();
  });
  dialog.addEventListener('close', function () {
    document.body.classList.remove('portfolio-aberto');
    conteudo.replaceChildren();
  });
})();
