---
name: reedicao-cortico
description: Estado e decisões da reedição de O Cortiço (repo GuilhermeNobre/cortico-reedicao)
metadata:
  type: project
---

Reedição de *O Cortiço* (Aluísio Azevedo, 1890, domínio público) a partir da edição Ática de 1997
(PDF em `fonte/o-cortico.pdf`). Estado em 31/10/2026.

## Onde está o trabalho

- Repositório: GuilhermeNobre/cortico-reedicao. **Única branch de trabalho: `v1.0`.** Só existem `main` e `v1.0`;
  as branches `claude/*` foram apagadas e os PRs #1 a #24 foram fechados (todo o conteúdo está na `v1.0`).
- Pasta local principal: `/Users/guilhermenobre/Documents/cortico-reedicao` no MacBook (clone na `v1.0`, atualizado com `git pull`).
  A pasta antiga do PC (`C:\Users\gui\Documents\ProjetoCortico`) não é mais usada.
- Cópia no diretório do projeto: `/mnt/project-files/reedicao/`.

## Feito

1. Extração do PDF: `scripts/extrair_capitulos.py` (usa `pdftotext -layout`; o modo layout do pypdf insere espaços no meio das palavras).
2. Divisão em capítulos: `texto/original/capitulo-01.md` a `capitulo-23.md` e `completo.txt`.
3. Plano aprovado (`.agents/plano.md`) e guia de estilo (`.agents/guia-de-estilo.md`).
4. Reescrita: 23 threads `cap.XX-Reeditor` (Opus 5.5, esforço high) seguindo `.agents/skills/reeditor/SKILL.md`.
   Resultado em `texto/reescrito/capitulo-NN.md`, com o mesmo número de parágrafos do original (conferido).
5. Notas: `notas/capitulo-NN.md` guarda os termos traduzidos, os termos **novos** e as decisões pendentes de cada capítulo, para o revisor.

## Próximos passos

- **Revisão:** skill do Revisor textual em `.agents/skills/revisor/SKILL.md`, **aguardando aprovação do Guilherme**.
  Threads `cap.XX-Revisor` **ainda não abertas**. O revisor trabalha direto na `v1.0` (sem branch nem PR), mexe só no
  capítulo e na nota dele, e marca `Glossário: sim` nos termos que valem para o livro todo.
- Depois: consolidar o glossário a partir das notas; gerar o PDF único (Pandoc ou Typst) e publicar como Release no GitHub.

## Decisões do Guilherme

- Termos da época são **traduzidos** para o equivalente atual conforme o contexto (crioula → negra, caixeiro → balconista),
  pela tabela do plano.
- **Sem suavizar nem relativizar:** o preconceito do narrador e dos personagens fica com o mesmo peso do original,
  sem eufemismo nem "filtro" ideológico.
- **Moeda** da época mantida (réis, mil-réis, conto, vintém, tostão). **Todas as medidas de tamanho vão para o SI**
  (braça ≈ 2,2 m, palmo ≈ 22 cm, légua ≈ 6 km), com valores arredondados.
- **Capa, nota da edição e título:** decidir depois.
- **Uma branch só (`v1.0`)**: não criar outras branches.
- Ele não lê todos os capítulos; a aprovação é por fase (plano, skills) e a revisão fica com os agentes revisores.
- Toda entrega vai para o repositório **e** para a pasta do Mac (ele pediu para ver os arquivos salvos lá).

**Why:** ele quer controlar cada fase antes de ela começar.
**How to apply:** não abrir threads nem iniciar uma fase sem a aprovação explícita dele; seguir o plano e as skills.
