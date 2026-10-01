# Dev.Rodrigo — portfólio

Site pessoal de Rodrigo Guimarães. HTML, CSS e JavaScript puro, sem build e sem
dependências: o que está no repositório é exatamente o que vai para o ar.

## Rodar localmente

```bash
python3 -m http.server 8000
# abre http://localhost:8000
```

## Estrutura

```
index.html                 página inteira (os ícones SVG ficam em <symbol> no topo)
style.css                  estilos e animações
portfolio.js               navegação da galeria e prévias ampliadas
assets/icons/              logos das tecnologias (Devicon, baixados — funcionam offline)
assets/fonts/              Bricolage Grotesque e Instrument Sans (WOFF2 + licença OFL)
assets/images/             foto (JPG original + WebP 480/960), avatar, imagem de compartilhamento
assets/images/portfolio/   capturas completas dos três projetos em WebP
assets/*.pdf               currículos (PT e EN)
favicon.ico, icon-96.png,
apple-touch-icon.png       ícones da aba, do Google e do iPhone
robots.txt, sitemap.xml    instruções para buscadores
vercel.json                cabeçalhos de cache
```

## Trocar o currículo

Substitua o PDF em `assets/` mantendo o nome do arquivo. O cache está
configurado como `must-revalidate`, então a troca vale na hora — não é
preciso esperar cache expirar.

O Google indexa PDFs e mostra o **título interno** do arquivo no resultado.
Antes de exportar, preencha em Arquivo → Propriedades (LibreOffice):
título "Currículo — Rodrigo Guimarães, Desenvolvedor Full Stack" e autor
"Rodrigo Guimarães". Depois atualize a data do PDF em `sitemap.xml`.

## SEO

- **Domínio**: o endereço completo aparece em `index.html` (canonical,
  Open Graph, JSON-LD), `robots.txt` e `sitemap.xml`. Mudou de domínio?
  Buscar-e-substituir nos três arquivos.
- **Dados estruturados**: bloco JSON-LD no `<head>` (WebSite, ProfilePage e
  Person, com links para GitHub, LinkedIn e Instagram). Valide em
  https://search.google.com/test/rich-results depois de publicar.
- **Imagem de compartilhamento**: `assets/images/og-rodrigo-guimaraes.jpg`
  (1200×630). Para testar a prévia no LinkedIn:
  https://www.linkedin.com/post-inspector/
- **Ao editar a página**: atualize `dateModified` no JSON-LD e `lastmod` no
  `sitemap.xml`.
- **Foto**: o navegador escolhe entre os WebP de 480 e 960 px e o JPG. Se
  trocar a foto, gere as três versões com o mesmo nome.

## Design

O conceito é o **degradê**: em português a mesma palavra nomeia o corte do
barbeiro e o gradiente. Daí saem os dois elementos visuais do site — o
divisor de seções (traços que rareiam da esquerda para a direita) e a
revelação do nome na home, em que um fio passa como uma navalha e o nome
aparece no rastro.

Paleta: [Kanagawa Wave](https://github.com/rebelot/kanagawa.nvim).
Tipografia: Bricolage Grotesque (títulos) e Instrument Sans (texto), servidas
localmente em `assets/fonts/` e cortadas para os pesos e caracteres usados.

## Portfólio visual

A seção `#portfolio` apresenta Virlene Alves, Barbearia Toussaint e Veener
em uma galeria horizontal. Funciona com toque, barra de rolagem, setas e
teclado (←/→, Home/End quando a galeria está focada). Ao passar o mouse,
a captura percorre a página; ao selecionar a prévia, uma janela permite
rolar a imagem completa. Feche com Escape, com o botão Fechar ou pelo fundo.
A preferência por movimento reduzido é respeitada.

Sem JavaScript, a galeria continua rolável e os links abrem as capturas.
As imagens são locais: não precisam dos projetos originais em execução.
Para atualizá-las, substitua os WebP em `assets/images/portfolio/` e ajuste
os atributos `width` e `height` no HTML se as dimensões mudarem.
As capturas refletem os arquivos locais, inclusive os espaços reservados
para fotos e o catálogo vazio da Veener. Não são links para sites publicados.
