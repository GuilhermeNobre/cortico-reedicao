"""Extrai o texto de O Cortiço do PDF e grava um arquivo Markdown por capítulo.

Uso:
    python scripts/extrair_capitulos.py [caminho/do/livro.pdf]

Requer o pdftotext (pacote poppler-utils).

Saídas:
    texto/original/completo.txt     texto corrido, um parágrafo por linha
    texto/original/capitulo-NN.md   um arquivo por capítulo (I a XXIII)
"""

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF_PADRAO = RAIZ / "fonte" / "o-cortico.pdf"
SAIDA = RAIZ / "texto" / "original"

ROMANO = re.compile(r"^[IVXL]+$")
# No modo "layout" o PDF marca o início de cada parágrafo com recuo.
RECUO_PARAGRAFO = 3


def romano_para_int(romano):
    valores = {"I": 1, "V": 5, "X": 10, "L": 50}
    total = 0
    for atual, proximo in zip(romano, romano[1:] + " "):
        v = valores[atual]
        total += -v if valores.get(proximo, 0) > v else v
    return total


def ler_linhas(pdf):
    # pdftotext (poppler) preserva o recuo dos parágrafos sem inserir espaços
    # espúrios no meio das palavras, o que acontece com o modo layout do pypdf.
    saida = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    return saida.replace("\f", "\n").splitlines()


def montar_paragrafos(linhas):
    """Junta as linhas quebradas do PDF em parágrafos e separa os títulos de capítulo."""
    blocos = []  # ("capitulo", "XII") ou ("par", "texto do parágrafo")
    atual = []

    def fechar():
        if atual:
            blocos.append(("par", " ".join(atual)))
            atual.clear()

    for linha in linhas:
        limpa = linha.strip()
        if not limpa:
            continue
        if ROMANO.match(limpa):
            fechar()
            blocos.append(("capitulo", limpa))
            continue
        recuo = len(linha) - len(linha.lstrip())
        if recuo >= RECUO_PARAGRAFO:
            fechar()
        limpa = re.sub(r"\s+", " ", limpa)
        # Palavra hifenizada no fim da linha: "procurá-" + "la" vira "procurá-la".
        if atual and atual[-1].endswith("-"):
            atual[-1] += limpa
        else:
            atual.append(limpa)
    fechar()
    return blocos


def main():
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF_PADRAO
    blocos = montar_paragrafos(ler_linhas(pdf))

    capitulos = []
    for tipo, conteudo in blocos:
        if tipo == "capitulo":
            capitulos.append((conteudo, []))
        elif capitulos:  # ignora a ficha da fonte antes do capítulo I
            capitulos[-1][1].append(conteudo)

    esperado = list(range(1, len(capitulos) + 1))
    numeros = [romano_para_int(r) for r, _ in capitulos]
    if numeros != esperado:
        raise SystemExit(f"Sequência de capítulos inesperada: {numeros}")

    SAIDA.mkdir(parents=True, exist_ok=True)
    corrido = []
    for (romano, paragrafos), n in zip(capitulos, numeros):
        arquivo = SAIDA / f"capitulo-{n:02d}.md"
        arquivo.write_text(f"# {romano}\n\n" + "\n\n".join(paragrafos) + "\n", encoding="utf-8")
        corrido.append(romano)
        corrido.extend(paragrafos)
        palavras = sum(len(p.split()) for p in paragrafos)
        print(f"{arquivo.relative_to(RAIZ)}: {len(paragrafos)} parágrafos, {palavras} palavras")

    (SAIDA / "completo.txt").write_text("\n".join(corrido) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
