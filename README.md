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
blog.html                  índice de notícias de tecnologia
blog.css                   estilos do blog, usando a paleta do portfólio
blog/posts.json            notícias aprovadas e suas fontes
blog/*.html                páginas estáticas das notícias
scripts/build_blog.py      gera o blog e atualiza o sitemap (Python 3.9+)
drafts/blog/               rascunhos locais, ignorados pelo Git e pela Vercel
torneioapp.html             funcionalidades, telas e acesso ao TorneioApp
torneioapp.css              estilos da apresentação do sistema
assets/icons/              logos das tecnologias (Devicon, baixados — funcionam offline)
assets/fonts/              Bricolage Grotesque e Instrument Sans (WOFF2 + licença OFL)
assets/images/             foto (JPG original + WebP 480/960), avatar, imagem de compartilhamento
assets/images/portfolio/   capturas dos quatro projetos em WebP
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

A seção `#portfolio` apresenta TorneioApp, Virlene Alves, Barbearia Toussaint
e Veener em uma galeria horizontal. Funciona com toque, barra de rolagem, setas e
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

### TorneioApp

A página `torneioapp.html` apresenta o sistema Laravel com telas de dashboard,
descoberta de torneios, criação de eventos, gerenciamento, inscrição e Pix,
além da interface no celular em tema escuro. As imagens em
`assets/images/portfolio/torneioapp/` foram capturadas de uma instalação
isolada do código real, com nomes, eventos e chave Pix fictícios.

O acesso inclui o [repositório](https://github.com/Rodrigogbhs/torneioapp),
o guia oficial de instalação e o fluxo de criação de conta e confirmação de
e-mail. Os pagamentos Pix são confirmados manualmente pelo organizador.
As telas podem ser ampliadas com o mesmo diálogo usado pela galeria principal;
sem JavaScript, os links abrem diretamente as imagens.

## Blog de tecnologia

A aba Blog está disponível no menu, inclusive no celular. O índice e os artigos
são HTML estático: continuam legíveis sem JavaScript, com endereço próprio,
fontes, metadados de compartilhamento e entradas no sitemap. As duas notícias
iniciais foram selecionadas em 6 de outubro de 2026; seus horários indicam
a preparação do conteúdo, sem simular as edições das 7h ou das 13h.

As edições diárias usam o fuso `America/Sao_Paulo`: uma notícia às 7h e outra
às 13h. A seleção prioriza relevância, novidades das últimas 24 horas e fontes
primárias; a segunda edição deve trazer um assunto diferente da primeira.
Os agendamentos são gerenciados em Automações no Codex. Para executar tarefas
locais, o computador precisa estar ligado e o aplicativo em execução.

Para preparar uma notícia, salve um arquivo JSON em
`drafts/blog/AAAA-MM-DD-0700.json` ou `drafts/blog/AAAA-MM-DD-1300.json`.
Esses arquivos não entram no índice público, no Git ou no upload da Vercel.
Após revisar, adicione o objeto à lista em `blog/posts.json` e gere as páginas:

```bash
python3 scripts/build_blog.py
python3 scripts/build_blog.py --check
```

Cada objeto contém `slug`, `title`, `category`, `summary`, `published_at`
(data ISO 8601 com fuso), `edition` (`07:00`, `13:00` ou `inicial`),
`paragraphs` (lista de textos, sem HTML) e `sources` (lista de objetos com
`name`, `url` e `published_on`, a data do anúncio original).
Use a hora real da aprovação em `published_at`; `edition` identifica o
agendamento. O gerador rejeita slugs repetidos, datas sem fuso, edições
duplicadas no mesmo dia e notícias sem fontes. Conteúdos com data futura
só aparecem quando esse horário chega e as páginas são geradas novamente.

Gerar os arquivos atualiza a cópia local. Para aparecerem no site publicado,
é necessário enviar as alterações pelo fluxo de publicação da Vercel.
