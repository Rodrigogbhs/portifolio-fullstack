#!/usr/bin/env python3
"""Gera páginas estáticas do blog usando apenas a biblioteca padrão."""

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://devrodfullstack-portifolio.vercel.app"
TIMEZONE = ZoneInfo("America/Sao_Paulo")
MONTHS = ("jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez")


def escape(value):
    return html.escape(str(value), quote=True)


def read_posts():
    posts = json.loads((ROOT / "blog/posts.json").read_text(encoding="utf-8"))
    if not isinstance(posts, list):
        raise ValueError("blog/posts.json precisa conter uma lista de posts.")
    slugs, editions = set(), set()
    for post in posts:
        for field in ("slug", "title", "category", "summary", "published_at", "edition"):
            if not isinstance(post.get(field), str) or not post[field].strip():
                raise ValueError(f"Campo obrigatório inválido: {field}")
        slug = post["slug"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in slugs:
            raise ValueError(f"Slug inválido ou duplicado: {slug}")
        slugs.add(slug)
        published = datetime.fromisoformat(post["published_at"])
        if published.utcoffset() is None:
            raise ValueError(f"Data sem fuso horário: {slug}")
        if post["edition"] not in ("07:00", "13:00", "inicial"):
            raise ValueError(f"Edição inválida: {slug}")
        if post["edition"] != "inicial":
            key = (published.astimezone(TIMEZONE).date(), post["edition"])
            if key in editions:
                raise ValueError(f"Já existe um post para a edição {key}.")
            editions.add(key)
        if not isinstance(post.get("paragraphs"), list) or not post["paragraphs"]:
            raise ValueError(f"Post sem conteúdo: {slug}")
        if any(not isinstance(p, str) or not p.strip() for p in post["paragraphs"]):
            raise ValueError(f"Parágrafo inválido: {slug}")
        if not isinstance(post.get("sources"), list) or not post["sources"]:
            raise ValueError(f"Post sem fontes: {slug}")
        for source in post["sources"]:
            url = urlparse(source["url"])
            if url.scheme not in ("http", "https") or not url.netloc or not source["name"]:
                raise ValueError(f"Fonte inválida: {slug}")
            date.fromisoformat(source["published_on"])
    now = datetime.now(TIMEZONE)
    return sorted(
        (post for post in posts if datetime.fromisoformat(post["published_at"]) <= now),
        key=lambda post: datetime.fromisoformat(post["published_at"]),
        reverse=True,
    )


def date_label(value, include_time=False):
    local = date.fromisoformat(value) if len(value) == 10 else datetime.fromisoformat(value).astimezone(TIMEZONE)
    label = f"{local.day} {MONTHS[local.month - 1]} {local.year}"
    return label + (f" · {local:%H:%M} (Brasília)" if include_time and isinstance(local, datetime) else "")


def metadata(post):
    minutes = max(1, (len(" ".join(post["paragraphs"]).split()) + 199) // 200)
    edition = "Edição inicial" if post["edition"] == "inicial" else f"Edição das {post['edition']}"
    return f'<div class="blog-meta"><time datetime="{escape(post["published_at"])}">{date_label(post["published_at"], True)}</time><span>{edition}</span><span>{minutes} min de leitura</span></div>'


def page(title, description, path, body, structured):
    prefix = "../" if path.startswith("/blog/") else ""
    structured_json = json.dumps(structured, ensure_ascii=False).replace("<", "\\u003c")
    return f'''<!DOCTYPE html>
<!-- Gerado por scripts/build_blog.py. Edite o conteúdo em blog/posts.json. -->
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} — Dev.Rodrigo</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#1f1f28">
  <link rel="canonical" href="{DOMAIN}{path}">
  <meta property="og:type" content="{'article' if path.startswith('/blog/') else 'website'}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Dev.Rodrigo">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{DOMAIN}{path}">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-rodrigo-guimaraes.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(description)}">
  <meta name="twitter:image" content="{DOMAIN}/assets/images/og-rodrigo-guimaraes.jpg">
  <link rel="icon" href="{prefix}favicon.ico">
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
  <link rel="preload" href="{prefix}assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}style.css">
  <link rel="stylesheet" href="{prefix}blog.css">
  <script type="application/ld+json">{structured_json}</script>
</head>
<body>
  <a class="pular-conteudo" href="#conteudo">Pular para o conteúdo</a>
  <header class="topo">
    <div class="container navbar">
      <a href="{prefix}index.html" class="marca"><img class="marca-avatar" src="{prefix}assets/images/avatar-rodrigo.webp" alt="" width="40" height="40"><span>Dev<span class="ponto">.</span>Rodrigo</span></a>
      <nav class="blog-menu" aria-label="Navegação principal"><a href="{prefix}index.html#portfolio">Portfólio</a><a href="{prefix}blog.html" aria-current="{'page' if path == '/blog' else 'true'}">Blog</a><a class="blog-contato" href="{prefix}index.html#contato">Contato</a></nav>
    </div>
  </header>
  <main id="conteudo">{body}
  </main>
  <footer class="rodape container blog-rodape"><p>© {datetime.now(TIMEZONE).year} Rodrigo Guimarães.</p><a href="{prefix}index.html">Conheça meu trabalho <span aria-hidden="true">↗</span></a></footer>
</body>
</html>
'''


def build_pages(posts):
    cards = []
    for post in posts:
        url = f'blog/{post["slug"]}.html'
        cards.append(f'''<article class="blog-card">
          <p class="blog-categoria">{escape(post["category"])}</p>
          <h3><a href="{url}">{escape(post["title"])}</a></h3>
          <p class="blog-resumo">{escape(post["summary"])}</p>
          {metadata(post)}
          <a class="blog-ler" href="{url}" aria-label="Ler: {escape(post["title"])}">Ler notícia <span aria-hidden="true">↗</span></a>
        </article>''')
    count = f"{len(posts)} {'notícia' if len(posts) == 1 else 'notícias'} · Mais recentes primeiro"
    listing = '<div class="blog-grade">' + "\n".join(cards) + '</div>' if cards else '<p class="blog-vazio">A primeira edição está chegando. Volte em breve para acompanhar as notícias de tecnologia.</p>'
    body = f'''
    <section class="blog-hero container" aria-labelledby="titulo-blog">
      <p class="blog-sobretitulo">Blog · Radar de tecnologia</p>
      <h1 id="titulo-blog">O que move<br>a <span>tecnologia.</span></h1>
      <p class="blog-intro">Duas notícias para acompanhar o que importa. Uma curadoria em português, com contexto e links para você ir direto às fontes.</p>
      <div class="degrade" aria-hidden="true"></div>
    </section>
    <section class="blog-edicoes container" aria-labelledby="titulo-edicoes">
      <div class="blog-lista-topo"><h2 id="titulo-edicoes">Últimas notícias</h2><p>{count}</p></div>
      {listing}
    </section>'''
    structured = {"@context": "https://schema.org", "@type": "Blog", "name": "Radar de tecnologia — Dev.Rodrigo", "url": DOMAIN + "/blog", "inLanguage": "pt-BR", "blogPost": [{"@type": "BlogPosting", "headline": post["title"], "url": f'{DOMAIN}/blog/{post["slug"]}', "datePublished": post["published_at"]} for post in posts]}
    outputs = {ROOT / "blog.html": page("Blog de tecnologia", "Notícias de tecnologia em português: inteligência artificial, desenvolvimento, segurança e inovação, com contexto e fontes.", "/blog", body, structured)}
    for post in posts:
        paragraphs = "\n".join(f'<p>{escape(text)}</p>' for text in post["paragraphs"])
        sources = "\n".join(f'<li><a href="{escape(source["url"])}" target="_blank" rel="noopener noreferrer">{escape(source["name"])} <span aria-hidden="true">↗</span></a><small>Fonte publicada em {date_label(source["published_on"])}</small></li>' for source in post["sources"])
        body = f'''
    <article class="blog-artigo container">
      <a class="blog-voltar" href="../blog.html">← Todas as notícias</a>
      <header><p class="blog-categoria">{escape(post["category"])}</p><h1>{escape(post["title"])}</h1>{metadata(post)}<p class="blog-resumo">{escape(post["summary"])}</p></header>
      <div class="blog-texto">{paragraphs}</div>
      <aside class="blog-fontes" aria-labelledby="titulo-fontes"><h2 id="titulo-fontes">Fontes para continuar a leitura</h2><ul>{sources}</ul></aside>
    </article>'''
        structured = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"], "description": post["summary"], "datePublished": post["published_at"], "inLanguage": "pt-BR", "url": f'{DOMAIN}/blog/{post["slug"]}', "author": {"@type": "Person", "name": "Rodrigo Guimarães", "url": DOMAIN}, "image": DOMAIN + "/assets/images/og-rodrigo-guimaraes.jpg", "isPartOf": {"@type": "Blog", "url": DOMAIN + "/blog"}, "citation": [source["url"] for source in post["sources"]]}
        outputs[ROOT / f'blog/{post["slug"]}.html'] = page(post["title"], post["summary"], f'/blog/{post["slug"]}', body, structured)
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap = re.sub(r"  <url>\s*<loc>" + re.escape(DOMAIN) + r"/blog(?:/[^<]*)?</loc>.*?</url>\n", "", sitemap, flags=re.S)
    lastmod = datetime.fromisoformat(posts[0]["published_at"]).astimezone(TIMEZONE).date().isoformat() if posts else datetime.now(TIMEZONE).date().isoformat()
    entries = f"  <url>\n    <loc>{DOMAIN}/blog</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>\n"
    for post in posts:
        modified = datetime.fromisoformat(post["published_at"]).astimezone(TIMEZONE).date().isoformat()
        entries += f'  <url>\n    <loc>{DOMAIN}/blog/{post["slug"]}</loc>\n    <lastmod>{modified}</lastmod>\n  </url>\n'
    outputs[ROOT / "sitemap.xml"] = sitemap.replace("</urlset>", entries + "</urlset>")
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verifica se as páginas estão atualizadas, sem escrever.")
    args = parser.parse_args()
    try:
        posts = read_posts()
        outputs = build_pages(posts)
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Conteúdo inválido: {error}\n")
    changed = [path for path, value in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != value]
    if args.check and changed:
        parser.exit(1, "Páginas desatualizadas: " + ", ".join(str(p.relative_to(ROOT)) for p in changed) + "\n")
    if not args.check:
        for path in changed:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(outputs[path], encoding="utf-8")
    print(f"Blog verificado: {len(posts)} posts, {len(changed)} arquivos {'pendentes' if args.check else 'atualizados'}.")


if __name__ == "__main__":
    main()
