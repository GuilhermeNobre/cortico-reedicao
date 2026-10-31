#!/usr/bin/env python3
"""Gera a edição em PDF de *O Cortiço* a partir dos capítulos Markdown.

Uso:
    /caminho/para/python3 scripts/gerar_pdf.py --formato a4

O arquivo final é escrito em output/pdf/. Há versões A5 e A4, ambas com composição
própria para leitura digital e impressão.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "texto" / "reescrito"
COVER = ROOT / "images" / "capa.png"
OUTPUT = ROOT / "output" / "pdf" / "o-cortico-edicao-revisada-versao-01.pdf"
TEMP = ROOT / "tmp" / "pdfs"

PAGE_W, PAGE_H = A5
FORMAT_NAME = "a5"
CHAPTER_START_PAGE = 7  # capa, guarda, rosto, créditos, nota e sumário
INK = colors.HexColor("#2A1D18")
RUST = colors.HexColor("#8F260D")
SAND = colors.HexColor("#F3E8D4")
MUTED = colors.HexColor("#806D60")


def configure_format(format_name: str) -> None:
    """Configura dimensões e nome do arquivo final."""
    global PAGE_W, PAGE_H, FORMAT_NAME, OUTPUT
    FORMAT_NAME = format_name
    if format_name == "a4":
        PAGE_W, PAGE_H = A4
        OUTPUT = ROOT / "output" / "pdf" / "o-cortico-edicao-revisada-versao-01-a4.pdf"
    else:
        PAGE_W, PAGE_H = A5
        OUTPUT = ROOT / "output" / "pdf" / "o-cortico-edicao-revisada-versao-01.pdf"


def register_fonts() -> None:
    """Registra uma família de leitura com diacríticos completos para o português."""
    font_dir = Path("/System/Library/Fonts/Supplemental")
    fonts = {
        "Times": font_dir / "Times New Roman.ttf",
        "Times-Bold": font_dir / "Times New Roman Bold.ttf",
        "Times-Italic": font_dir / "Times New Roman Italic.ttf",
        "Times-BoldItalic": font_dir / "Times New Roman Bold Italic.ttf",
        "Verdana": font_dir / "Verdana.ttf",
        "Verdana-Bold": font_dir / "Verdana Bold.ttf",
    }
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily(
        "Times",
        normal="Times",
        bold="Times-Bold",
        italic="Times-Italic",
        boldItalic="Times-BoldItalic",
    )


ROMAN_NUMERALS = (
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII",
)


class ChapterHeading(Paragraph):
    def __init__(self, text: str, style: ParagraphStyle, chapter: str) -> None:
        super().__init__(text, style)
        self.chapter = chapter


class BookDoc(BaseDocTemplate):
    def __init__(self, filename: str | Path, **kwargs) -> None:
        super().__init__(str(filename), **kwargs)
        self.chapter_pages: list[tuple[str, int]] = []

    def afterFlowable(self, flowable) -> None:  # noqa: N802 (ReportLab API)
        if isinstance(flowable, ChapterHeading):
            page_number = self.page - CHAPTER_START_PAGE + 1
            self.chapter_pages.append((flowable.chapter, page_number))
            key = f"chapter-{flowable.chapter}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(f"Capítulo {flowable.chapter}", key, level=0, closed=False)


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    a4 = FORMAT_NAME == "a4"
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Times",
            fontSize=11.5 if a4 else 10.4,
            leading=16.0 if a4 else 14.25,
            textColor=INK,
            alignment=TA_JUSTIFY,
            firstLineIndent=(6.0 if a4 else 5.4) * mm,
            spaceAfter=0,
            allowWidows=0,
            allowOrphans=0,
        ),
        "chapter": ParagraphStyle(
            "Chapter",
            fontName="Verdana-Bold",
            fontSize=31 if a4 else 27,
            leading=37 if a4 else 32,
            textColor=RUST,
            alignment=TA_CENTER,
            spaceBefore=(56 if a4 else 42) * mm,
            spaceAfter=(56 if a4 else 42) * mm,
        ),
        "title": ParagraphStyle(
            "Title",
            fontName="Verdana-Bold",
            fontSize=34 if a4 else 29,
            leading=40 if a4 else 34,
            textColor=RUST,
            alignment=TA_CENTER,
        ),
        "author": ParagraphStyle(
            "Author",
            fontName="Verdana",
            fontSize=14 if a4 else 12.5,
            leading=20 if a4 else 18,
            textColor=INK,
            alignment=TA_CENTER,
            spaceBefore=10 * mm,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            fontName="Verdana",
            fontSize=9 if a4 else 7.9,
            leading=12.5 if a4 else 11.5,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=(48 if a4 else 34) * mm,
        ),
        "front-head": ParagraphStyle(
            "FrontHead",
            fontName="Verdana-Bold",
            fontSize=19 if a4 else 16,
            leading=26 if a4 else 22,
            textColor=RUST,
            alignment=TA_CENTER,
            spaceAfter=9 * mm,
        ),
        "front-body": ParagraphStyle(
            "FrontBody",
            fontName="Times",
            fontSize=11.2 if a4 else 10.1,
            leading=15.8 if a4 else 14.2,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=4.2 * mm,
        ),
        "small": ParagraphStyle(
            "Small",
            fontName="Verdana",
            fontSize=7.6,
            leading=10.3,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "toc": ParagraphStyle(
            "TOC",
            fontName="Times",
            fontSize=11.3 if a4 else 10.4,
            leading=15.5 if a4 else 14.25,
            textColor=INK,
        ),
        "back": ParagraphStyle(
            "Back",
            fontName="Times",
            fontSize=12 if a4 else 11,
            leading=17 if a4 else 16,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=4 * mm,
        ),
    }


def escaped(text: str) -> str:
    return html.escape(text, quote=False)


def read_chapters() -> list[tuple[str, list[str]]]:
    chapters = []
    for index, numeral in enumerate(ROMAN_NUMERALS, 1):
        source = SOURCE_DIR / f"capitulo-{index:02d}.md"
        lines = source.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].strip() != f"# {numeral}":
            raise ValueError(f"Cabeçalho inesperado em {source}")
        paragraphs = []
        accumulator: list[str] = []
        for line in lines[1:]:
            if line.strip():
                accumulator.append(line.strip())
            elif accumulator:
                paragraphs.append(" ".join(accumulator))
                accumulator = []
        if accumulator:
            paragraphs.append(" ".join(accumulator))
        if not paragraphs:
            raise ValueError(f"Capítulo vazio: {source}")
        chapters.append((numeral, paragraphs))
    return chapters


def front_matter(s: dict[str, ParagraphStyle], chapter_pages: list[tuple[str, int]] | None) -> list:
    story = [
        Image(str(COVER), width=PAGE_W, height=PAGE_H),
        NextPageTemplate("front"),
        PageBreak(),  # guarda
        PageBreak(),  # folha de rosto
        Spacer(1, 47 * mm),
        Paragraph("O CORTIÇO", s["title"]),
        Paragraph("ALUÍSIO AZEVEDO", s["author"]),
        Paragraph("Edição em linguagem atual", s["subtitle"]),
        PageBreak(),
        Spacer(1, 37 * mm),
        Paragraph("CRÉDITOS DA EDIÇÃO", s["front-head"]),
        Paragraph(
            "<b>O Cortiço</b>, de Aluísio Azevedo, foi publicado originalmente em 1890 e integra o domínio público.",
            s["front-body"],
        ),
        Paragraph(
            "Texto-base consultado: edição Ática, 1997 (30ª edição), digitalizada pela Biblioteca Virtual do Estudante Brasileiro, Escola do Futuro/USP.",
            s["front-body"],
        ),
        Paragraph(
            "Esta composição reúne a reescrita do romance em português atual, preservando enredo, cenas, personagens, diálogos e a força do texto original. Capa fornecida pelo projeto.",
            s["front-body"],
        ),
        Spacer(1, 8 * mm),
        Paragraph("1ª versão de composição · outubro de 2026", s["small"]),
        PageBreak(),
        Spacer(1, 27 * mm),
        Paragraph("NOTA DA EDIÇÃO", s["front-head"]),
        Paragraph(
            "Esta edição aproxima a linguagem de 1890 do leitor atual sem resumir, suavizar ou atualizar o enredo. Foram modernizados a ortografia, construções hoje pouco usuais e termos de época, sempre que isso favorece a compreensão. A moeda histórica e as marcas essenciais de fala foram preservadas.",
            s["front-body"],
        ),
        Paragraph(
            "O romance traz representações de raça, classe, gênero e violência próprias de seu tempo e de sua perspectiva naturalista. Elas permanecem no texto por fazerem parte da obra e de seu contexto histórico.",
            s["front-body"],
        ),
        Paragraph(
            "Esta é a primeira versão de composição do livro, preparada após a revisão editorial dos capítulos. Os elementos de publicação - como ISBN, ficha catalográfica e definição de editora - poderão ser incorporados na etapa de lançamento.",
            s["front-body"],
        ),
        PageBreak(),
        Spacer(1, 20 * mm),
        Paragraph("SUMÁRIO", s["front-head"]),
    ]
    entries = chapter_pages or [(numeral, 0) for numeral in ROMAN_NUMERALS]
    for numeral, page in entries:
        dots = "." * max(2, 50 - len(numeral) - len(str(page)))
        story.append(Paragraph(f"Capítulo {numeral} {dots} {page if page else ''}", s["toc"]))
    story.extend([NextPageTemplate("right"), PageBreak()])
    return story


def chapter_flowables(chapters: list[tuple[str, list[str]]], s: dict[str, ParagraphStyle]) -> list:
    story = []
    for index, (number, paragraphs) in enumerate(chapters):
        story.append(ChapterHeading(f"CAPÍTULO {number}", s["chapter"], number))
        for paragraph in paragraphs:
            story.append(Paragraph(escaped(paragraph), s["body"]))
        if index < len(chapters) - 1:
            story.append(PageBreak())
    return story


def back_cover(s: dict[str, ParagraphStyle]) -> list:
    return [
        NextPageTemplate("back"),
        PageBreak(),
        Spacer(1, 24 * mm),
        Paragraph("O CORTIÇO", s["title"]),
        Spacer(1, 18 * mm),
        Paragraph(
            "No Rio de Janeiro do fim do século XIX, a ambição de João Romão cresce junto com o cortiço que ele ergue nos fundos de sua venda. Entre casas apertadas, trabalho duro, desejo, fome, festas e disputas, a vida coletiva ganha o centro da narrativa.",
            s["back"],
        ),
        Paragraph(
            "Publicado em 1890, <i>O Cortiço</i> é um dos grandes romances do naturalismo brasileiro. Nesta edição, sua linguagem foi aproximada do português contemporâneo para tornar a leitura mais fluida, sem apagar a força, as tensões e a crueza do original.",
            s["back"],
        ),
        Spacer(1, 8 * mm),
        Paragraph("ALUÍSIO AZEVEDO (1857-1913) foi romancista, contista e jornalista. Sua obra é fundamental para a literatura brasileira.", s["small"]),
        Spacer(1, 12 * mm),
        Paragraph("EDIÇÃO REVISADA · 1ª VERSÃO DE COMPOSIÇÃO", s["small"]),
    ]


def draw_front(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(SAND)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.restoreState()


def draw_main(canvas, doc) -> None:
    margin = 26 * mm if FORMAT_NAME == "a4" else 17 * mm
    rule_y = 17 * mm if FORMAT_NAME == "a4" else 13.5 * mm
    label_y = 11.5 * mm if FORMAT_NAME == "a4" else 9.2 * mm
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#C9B9A8"))
    canvas.setLineWidth(0.35)
    canvas.line(margin, rule_y, PAGE_W - margin, rule_y)
    canvas.setFillColor(MUTED)
    canvas.setFont("Verdana", 7.2 if FORMAT_NAME == "a4" else 6.6)
    canvas.drawString(margin, label_y, "O CORTIÇO · ALUÍSIO AZEVEDO")
    logical_page = doc.page - CHAPTER_START_PAGE + 1
    page_label = str(logical_page)
    canvas.drawRightString(PAGE_W - margin, label_y, page_label)
    canvas.restoreState()


def draw_back(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(SAND)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setStrokeColor(RUST)
    canvas.setLineWidth(1.1)
    inset = 34 * mm if FORMAT_NAME == "a4" else 25 * mm
    top = 27 * mm if FORMAT_NAME == "a4" else 19 * mm
    canvas.line(inset, PAGE_H - top, PAGE_W - inset, PAGE_H - top)
    canvas.restoreState()


def make_document(path: Path, s: dict[str, ParagraphStyle]) -> BookDoc:
    full = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    front_x, front_y = (31 * mm, 28 * mm) if FORMAT_NAME == "a4" else (22 * mm, 20 * mm)
    main_x, main_y = (26 * mm, 24 * mm) if FORMAT_NAME == "a4" else (18 * mm, 19 * mm)
    back_margin = 31 * mm if FORMAT_NAME == "a4" else 22 * mm
    front = Frame(front_x, front_y, PAGE_W - 2 * front_x, PAGE_H - 2 * front_y, id="front")
    main_left = Frame(main_x, main_y, PAGE_W - 2 * main_x, PAGE_H - 2 * main_y, id="left")
    main_right = Frame(main_x, main_y, PAGE_W - 2 * main_x, PAGE_H - 2 * main_y, id="right")
    back = Frame(back_margin, back_margin, PAGE_W - 2 * back_margin, PAGE_H - 2 * back_margin, id="back")
    doc = BookDoc(path, pagesize=(PAGE_W, PAGE_H), leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0, title="O Cortiço", author="Aluísio Azevedo")
    from reportlab.platypus import PageTemplate
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[full]),
        PageTemplate(id="front", frames=[front], onPage=draw_front),
        PageTemplate(id="left", frames=[main_left], onPage=draw_main),
        PageTemplate(id="right", frames=[main_right], onPage=draw_main),
        PageTemplate(id="back", frames=[back], onPage=draw_back),
    ])
    return doc


def build(format_name: str = "a5") -> Path:
    configure_format(format_name)
    if not COVER.exists():
        raise FileNotFoundError(f"Capa não encontrada: {COVER}")
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    TEMP.mkdir(parents=True, exist_ok=True)
    chapter_data = read_chapters()
    s = styles()

    # Primeira passagem: descobre a paginação real dos capítulos para um sumário preciso.
    preliminary = TEMP / "o-cortico-paginacao.pdf"
    collector = make_document(preliminary, s)
    collector.build(front_matter(s, None) + chapter_flowables(chapter_data, s) + back_cover(s))

    # Segunda passagem: recompõe o mesmo livro com os números recolhidos no sumário.
    document = make_document(OUTPUT, s)
    document.build(front_matter(s, collector.chapter_pages) + chapter_flowables(chapter_data, s) + back_cover(s))
    return OUTPUT


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera o PDF de O Cortiço em A5 ou A4.")
    parser.add_argument("--formato", choices=("a5", "a4"), default="a5")
    args = parser.parse_args()
    result = build(args.formato)
    print(result)
