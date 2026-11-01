#!/usr/bin/env python3
"""Gera um EPUB 3 refluível de *O Cortiço* para Kindle e outros leitores."""

from __future__ import annotations

import html
import re
import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "texto" / "reescrito"
EDITOR_NOTE = ROOT / "texto" / "editor" / "nota-do-editor.md"
COVER = ROOT / "images" / "capa.png"
OUTPUT = ROOT / "output" / "epub" / "o-cortico-edicao-revisada-versao-01.epub"
IDENTIFIER = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/GuilhermeNobre/cortico-reedicao/o-cortico-versao-01')}"
ROMAN_NUMERALS = (
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII",
)

XHTML_HEAD = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="pt-BR" lang="pt-BR">
<head><meta charset="utf-8"/><title>{title}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
"""
XHTML_FOOT = "</body></html>\n"


def page(title: str, content: str, classes: str = "") -> str:
    body_class = f' class="{classes}"' if classes else ""
    head = XHTML_HEAD.format(title=html.escape(title))
    return head.replace("<body>", f"<body{body_class}>") + content + XHTML_FOOT


def read_chapters() -> list[tuple[str, list[str]]]:
    chapters = []
    for index, numeral in enumerate(ROMAN_NUMERALS, 1):
        source = SOURCE_DIR / f"capitulo-{index:02d}.md"
        lines = source.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].strip() != f"# {numeral}":
            raise ValueError(f"Cabeçalho inesperado em {source}")
        paragraphs, accumulator = [], []
        for line in lines[1:]:
            if line.strip():
                accumulator.append(line.strip())
            elif accumulator:
                paragraphs.append(" ".join(accumulator))
                accumulator = []
        if accumulator:
            paragraphs.append(" ".join(accumulator))
        chapters.append((numeral, paragraphs))
    return chapters


def read_editor_note() -> list[str]:
    lines = EDITOR_NOTE.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "# NOTA DO EDITOR":
        raise ValueError(f"Cabeçalho inesperado em {EDITOR_NOTE}")
    paragraphs, accumulator = [], []
    for line in lines[1:]:
        if re.match(r"^\d+\.\s", line.strip()):
            if accumulator:
                paragraphs.append(" ".join(accumulator))
                accumulator = []
            paragraphs.append(line.strip())
        elif line.strip():
            accumulator.append(line.strip())
        elif accumulator:
            paragraphs.append(" ".join(accumulator))
            accumulator = []
    if accumulator:
        paragraphs.append(" ".join(accumulator))
    return paragraphs


def format_markdown(text: str) -> str:
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html.escape(text))


def write_text(root: Path, relative: str, content: str) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def build() -> Path:
    if not COVER.exists():
        raise FileNotFoundError(f"Capa não encontrada: {COVER}")
    chapters = read_chapters()
    editor_note = read_editor_note()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="cortico-epub-") as work:
        work_root = Path(work)
        oebps = work_root / "OEBPS"
        (work_root / "META-INF").mkdir()
        oebps.mkdir()
        write_text(work_root, "mimetype", "application/epub+zip")
        write_text(work_root, "META-INF/container.xml", """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
""")
        shutil.copy2(COVER, oebps / "capa.png")
        write_text(oebps, "style.css", """@charset "utf-8";
body { margin: 5%; font-family: serif; line-height: 1.55; }
body.cover { margin: 0; padding: 0; text-align: center; }
body.cover img { width: 100%; height: auto; display: block; }
body.title, body.front { text-align: center; margin-top: 20%; }
h1 { text-align: center; font-family: sans-serif; font-size: 1.7em; margin: 2.8em 0 2em; page-break-before: always; break-before: page; }
h1.first { page-break-before: avoid; break-before: avoid; }
h2 { font-family: sans-serif; font-size: 1.25em; margin: 1.6em 0 1em; }
p { margin: 0 0 1em; text-align: justify; text-indent: 1.4em; }
h1 + p, h2 + p, .front p { text-indent: 0; }
.author, .subtitle { text-align: center; text-indent: 0; }
.author { font-family: sans-serif; letter-spacing: .08em; }
.subtitle { color: #555; font-size: .9em; margin-top: 4em; }
.credit { text-align: left; text-indent: 0; }
nav ol { padding-left: 1.3em; } nav li { margin: .45em 0; }
""")
        write_text(oebps, "cover.xhtml", page("Capa", '<img src="capa.png" alt="Capa de O Cortiço, de Aluísio Azevedo"/>', "cover"))
        write_text(oebps, "title.xhtml", page("Folha de rosto", """<section class="front">
<h1 class="first">O CORTIÇO</h1><p class="author">ALUÍSIO AZEVEDO</p><p class="subtitle">Edição em linguagem atual</p>
</section>""", "title"))
        write_text(oebps, "credits.xhtml", page("Créditos da edição", """<h1 class="first">CRÉDITOS DA EDIÇÃO</h1>
<p class="credit"><strong>O Cortiço</strong>, de Aluísio Azevedo, foi publicado originalmente em 1890 e integra o domínio público.</p>
<p class="credit">Texto-base consultado: edição Ática, 1997 (30ª edição), digitalizada pela Biblioteca Virtual do Estudante Brasileiro, Escola do Futuro/USP.</p>
<p class="credit">Esta composição reúne a reescrita do romance em português atual, preservando enredo, cenas, personagens, diálogos e a força do texto original. Capa fornecida pelo projeto.</p>
<p class="credit">1ª versão de composição - outubro de 2026.</p>"""))
        write_text(oebps, "note.xhtml", page("Nota da edição", """<h1 class="first">NOTA DA EDIÇÃO</h1>
<p>Esta edição aproxima a linguagem de 1890 do leitor atual sem resumir, suavizar ou atualizar o enredo. Foram modernizados a ortografia, construções hoje pouco usuais e termos de época, sempre que isso favorece a compreensão. A moeda histórica e as marcas essenciais de fala foram preservadas.</p>
<p>O romance traz representações de raça, classe, gênero e violência próprias de seu tempo e de sua perspectiva naturalista. Elas permanecem no texto por fazerem parte da obra e de seu contexto histórico.</p>
<p>Esta é a primeira versão de composição do livro, preparada após a revisão editorial dos capítulos. Os elementos de publicação - como ISBN, ficha catalográfica e definição de editora - poderão ser incorporados na etapa de lançamento.</p>"""))

        editor_content = '<h1 class="first">NOTA DO EDITOR</h1>'
        editor_content += "\n".join(f"<p>{format_markdown(paragraph)}</p>" for paragraph in editor_note)
        write_text(oebps, "editor-note.xhtml", page("Nota do editor", editor_content))

        nav_items = '<li><a href="note.xhtml">Nota da edição</a></li><li><a href="editor-note.xhtml">Nota do editor</a></li>'
        nav_items += "\n" + "\n".join(f'<li><a href="capitulo-{index:02d}.xhtml">Capítulo {numeral}</a></li>' for index, numeral in enumerate(ROMAN_NUMERALS, 1))
        write_text(oebps, "nav.xhtml", page("Sumário", f'<nav epub:type="toc" id="toc" xmlns:epub="http://www.idpf.org/2007/ops"><h1 class="first">SUMÁRIO</h1><ol>{nav_items}</ol></nav>'))

        for index, (numeral, paragraphs) in enumerate(chapters, 1):
            body = f'<h1 class="first">CAPÍTULO {numeral}</h1>'
            body += "\n".join(f"<p>{html.escape(paragraph)}</p>" for paragraph in paragraphs)
            write_text(oebps, f"capitulo-{index:02d}.xhtml", page(f"Capítulo {numeral}", body))

        manifest_items = [
            '<item id="style" href="style.css" media-type="text/css"/>',
            '<item id="cover-image" href="capa.png" media-type="image/png" properties="cover-image"/>',
            '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="credits" href="credits.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="note" href="note.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="editor-note" href="editor-note.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        ]
        manifest_items.extend(f'<item id="chapter-{index:02d}" href="capitulo-{index:02d}.xhtml" media-type="application/xhtml+xml"/>' for index in range(1, 24))
        spine_items = ["cover", "title", "credits", "note", "editor-note", "nav"] + [f"chapter-{index:02d}" for index in range(1, 24)]
        opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="pt-BR">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:identifier id="book-id">{IDENTIFIER}</dc:identifier>
  <dc:title>O Cortiço</dc:title><dc:creator>Aluísio Azevedo</dc:creator><dc:language>pt-BR</dc:language>
  <dc:date>2026-10-31</dc:date><dc:rights>Texto original em domínio público; reedição em linguagem atual.</dc:rights>
  <meta property="dcterms:modified">2026-10-31T00:00:00Z</meta>
</metadata>
<manifest>{''.join(manifest_items)}</manifest>
<spine>{''.join(f'<itemref idref="{item}"/>' for item in spine_items)}</spine>
</package>
"""
        write_text(oebps, "content.opf", opf)

        with zipfile.ZipFile(OUTPUT, "w") as archive:
            archive.write(work_root / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
            for path in sorted(work_root.rglob("*")):
                if path.is_file() and path.name != "mimetype":
                    archive.write(path, path.relative_to(work_root).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
    return OUTPUT


if __name__ == "__main__":
    print(build())
