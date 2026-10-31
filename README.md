# O Cortiço: reedição

Nova edição de *O Cortiço* (1890), de Aluísio Azevedo, com a linguagem atualizada para o
leitor de hoje, mantendo enredo, cenas e estilo do original. O romance está em domínio
público. O texto-base vem da edição Ática de 1997 (30ª ed.), digitalizada pela Biblioteca
Virtual do Estudante Brasileiro (Escola do Futuro/USP).

## Estrutura

- `fonte/o-cortico.pdf`: PDF de origem.
- `scripts/extrair_capitulos.py`: extrai o texto do PDF e separa os capítulos.
- `texto/original/`: texto original, um arquivo Markdown por capítulo (I a XXIII).
- `texto/reescrito/`: capítulos reescritos e revisados.
- `.agents/`: plano, guia de estilo e memórias do projeto (para retomar o trabalho em outra máquina).

## Como regenerar o texto original

Requer Python 3 e o `pdftotext` (pacote `poppler-utils`).

```
python scripts/extrair_capitulos.py
```

## Andamento

| Etapa | Situação |
| --- | --- |
| 1. Extração do texto | feita |
| 2. Divisão em capítulos | feita (23 capítulos) |
| 3. Reescrita e revisão | plano aprovado, aguardando liberação |
| 4. PDF final | a fazer |
