#!/usr/bin/env python3
"""Convert the saved Effective Go HTML page to a clean Markdown document."""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class ArticleCleaner(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.in_article = False
        self.article_depth = 0
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        classes = set((attrs_dict.get("class") or "").split())

        if not self.in_article:
            if tag == "article" and "Article" in classes:
                self.in_article = True
                self.article_depth = 1
            return

        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth += 1
            return

        if (
            tag == "ol"
            and "SiteBreadcrumb" in classes
            or tag == "div"
            and attrs_dict.get("id") == "nav"
            or tag == "a"
            and "Article-idLink" in classes
        ):
            if tag not in VOID_TAGS:
                self.skip_depth = 1
            return

        if tag not in {"article", "div"}:
            self.parts.append(self._start_tag(tag, attrs))

        if tag not in VOID_TAGS:
            self.article_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.in_article and not self.skip_depth:
            self.parts.append(self._start_tag(tag, attrs, self_closing=True))

    def handle_endtag(self, tag: str) -> None:
        if not self.in_article:
            return

        if self.skip_depth:
            self.skip_depth -= 1
            return

        self.article_depth -= 1
        if self.article_depth == 0:
            self.in_article = False
            return

        if tag not in {"article", "div"}:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self.in_article and not self.skip_depth:
            self.parts.append(html.escape(data, quote=False))

    def handle_entityref(self, name: str) -> None:
        if self.in_article and not self.skip_depth:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.in_article and not self.skip_depth:
            self.parts.append(f"&#{name};")

    def _start_tag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
        *,
        self_closing: bool = False,
    ) -> str:
        kept: list[str] = []
        for key, value in attrs:
            if key == "href" or key == "id" and tag.startswith("h"):
                escaped = html.escape(value or "", quote=True)
                kept.append(f'{key}="{escaped}"')
        attr_text = f" {' '.join(kept)}" if kept else ""
        suffix = " />" if self_closing else ">"
        return f"<{tag}{attr_text}{suffix}"


def extract_article(source: Path) -> str:
    cleaner = ArticleCleaner()
    cleaner.feed(source.read_text(encoding="utf-8"))
    cleaner.close()
    return "".join(cleaner.parts)


def convert_to_markdown(article_html: str) -> str:
    result = subprocess.run(
        [
            "pandoc",
            "--from=html",
            "--to=gfm",
            "--wrap=none",
            "--markdown-headings=atx",
        ],
        input=article_html,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        default="Effective Go - The Go Programming Language.html",
        help="saved Effective Go HTML file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="effective-go.md",
        help="Markdown output path",
    )
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)
    article_html = extract_article(source)
    if not article_html.strip():
        print(f"Could not find the article body in {source}", file=sys.stderr)
        return 1

    markdown = convert_to_markdown(article_html)
    output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
