"""Verifica a navegação e o limite de notícias das páginas estáticas do blog."""

import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urljoin, urlparse

import build_blog


class Listing(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.cards = []
        self.pager = []
        self.heading = False
        self.navigation = False
        self.canonical = None
        self.og_type = None
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h3":
            self.heading = True
        if tag == "nav" and attrs.get("aria-label") == "Paginação das notícias":
            self.navigation = True
        if tag == "a" and self.heading:
            self.cards.append(attrs["href"])
        if tag == "a" and self.navigation:
            self.pager.append(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs["href"]
        if tag == "meta" and attrs.get("property") == "og:type":
            self.og_type = attrs["content"]

    def handle_endtag(self, tag):
        if tag == "h3":
            self.heading = False
        if tag == "nav":
            self.navigation = False


def posts(count):
    return [
        {
            "slug": f"2020-01-noticia-{index}",
            "title": f"Notícia {index}",
            "category": "Tecnologia",
            "summary": "Resumo da notícia.",
            "published_at": (datetime(2020, 1, 31, 10, tzinfo=timezone.utc) - timedelta(days=index)).isoformat(),
            "edition": "inicial",
            "paragraphs": ["Texto da notícia."],
            "sources": [{"name": "Fonte", "url": "https://example.com/fonte", "published_on": "2020-01-01"}],
        }
        for index in range(count)
    ]


class BlogPaginationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.root_patch = patch.object(build_blog, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        (self.root / "blog").mkdir()
        (self.root / "sitemap.xml").write_text(
            f'<urlset>\n  <url><loc>{build_blog.DOMAIN}/torneioapp</loc></url>\n</urlset>', encoding="utf-8"
        )

    def test_pages_keep_all_news_in_order_with_at_most_six_cards(self):
        for count in (0, 1, 6, 7, 12, 13, 22):
            with self.subTest(count=count):
                news = posts(count)
                output = build_blog.build_pages(news)
                total = max(1, (count + 5) // 6)
                all_cards = []
                for number in range(1, total + 1):
                    file = "blog.html" if number == 1 else f"blog/pagina-{number}.html"
                    listing = Listing(output[self.root / file])
                    self.assertEqual(len(listing.cards), len(news[(number - 1) * 6:number * 6]))
                    all_cards.extend(Path(urlparse(url).path).stem for url in listing.cards)
                    self.assertEqual(bool(listing.pager), total > 1)
                self.assertEqual(all_cards, [item["slug"] for item in news])
                for item in news:
                    self.assertIn(self.root / f'blog/{item["slug"]}.html', output)

    def test_pagination_links_reach_adjacent_pages_and_article_links_resolve(self):
        output = build_blog.build_pages(posts(13))
        for number, file in enumerate(("blog.html", "blog/pagina-2.html", "blog/pagina-3.html"), start=1):
            listing = Listing(output[self.root / file])
            self.assertEqual([link["rel"] for link in listing.pager],
                             (["prev"] if number > 1 else []) + (["next"] if number < 3 else []))
            for link in [*listing.cards, *(item["href"] for item in listing.pager)]:
                path = urlparse(urljoin(build_blog.DOMAIN + "/" + file, link)).path.lstrip("/")
                self.assertIn(self.root / path, output)
            if number > 1:
                previous = next(item["href"] for item in listing.pager if item["rel"] == "prev")
                expected = "/blog.html" if number == 2 else f"/blog/pagina-{number - 1}.html"
                self.assertEqual(urlparse(urljoin(build_blog.DOMAIN + "/" + file, previous)).path, expected)

    def test_each_listing_has_its_own_metadata_and_sitemap_entry(self):
        output = build_blog.build_pages(posts(7))
        second = output[self.root / "blog/pagina-2.html"]
        listing = Listing(second)
        self.assertEqual(listing.canonical, build_blog.DOMAIN + "/blog/pagina-2")
        self.assertEqual(listing.og_type, "website")
        self.assertIn('href="../style.css"', second)
        self.assertIn('aria-current="page"', second)
        self.assertIn("Página 2 de 2", second)
        structured = json.loads(second.split('<script type="application/ld+json">')[1].split("</script>")[0])
        self.assertEqual([item["headline"] for item in structured["blogPost"]], ["Notícia 6"])
        sitemap = output[self.root / "sitemap.xml"]
        self.assertIn(f"<loc>{build_blog.DOMAIN}/blog/pagina-2</loc>", sitemap)
        self.assertIn(f"<loc>{build_blog.DOMAIN}/torneioapp</loc>", sitemap)

    def test_check_detects_and_build_removes_pages_that_are_no_longer_needed(self):
        def run(*args):
            with patch("sys.argv", ["build_blog.py", *args]), contextlib.redirect_stdout(io.StringIO()):
                build_blog.main()

        data = self.root / "blog/posts.json"
        data.write_text(json.dumps(posts(7)), encoding="utf-8")
        run()
        second = self.root / "blog/pagina-2.html"
        self.assertTrue(second.exists())
        data.write_text(json.dumps(posts(1)), encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            run("--check")
        run()
        self.assertFalse(second.exists())
        run("--check")


if __name__ == "__main__":
    unittest.main()
