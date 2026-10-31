---
name: reedicao-cortico
description: Estado e decisões da reedição de O Cortiço (repo GuilhermeNobre/cortico-reedicao)
metadata:
  type: project
---

Reedição de O Cortiço (Aluísio Azevedo, domínio público) a partir da edição Ática 1997 (PDF em /mnt/project-files/o-cortico.pdf, copiado para fonte/ no repo). Branch de trabalho: **v1.0** (desde 2026-10-31; antes era claude/project-thread-9ivjk2).

Em 2026-10-31: extração feita com scripts/extrair_capitulos.py (pdftotext -layout; o modo layout do pypdf insere espaços no meio das palavras). 23 capítulos em texto/original/capitulo-NN.md. Plano em .agents/plano.md aprovado em 2026-10-31; originais copiados também para /mnt/project-files/reedicao/original/ (o Guilherme quer tudo no diretório do projeto E no repositório); regras em .agents/guia-de-estilo.md. Em 2026-10-31 os 23 capítulos foram reescritos (PRs #2 a #24, um por thread cap.XX-Reeditor) e reunidos na branch v1.0, com o mesmo número de parágrafos do original. Próximo passo: agentes de revisão, consolidar texto/reescrito/notas/ no glossário, depois o PDF.

Decisões do Guilherme:
- Pasta de trabalho principal: /Users/guilhermenobre/Documents/cortico-reedicao no MacBook (clone do repo, na branch v1.0), desde 2026-10-31. A pasta antiga do PC (C:\Users\gui\Documents\ProjetoCortico) não é mais usada. Toda entrega vai para o repositório e é puxada no Mac com git pull.
- **Não reescrever nenhum capítulo antes de ele aprovar o plano.** Ele pediu para parar quando comecei o capítulo II.
- Termos da época devem ser TRADUZIDOS para equivalentes atuais conforme o contexto (crioula → negra, caixeiro → balconista, braça → metros). Ele corrigiu quando entendi "manter os termos".
- Moeda da época fica como no original; TODAS as medidas de tamanho (braça, palmo, légua, polegada) vão para o SI. Decidido em 2026-10-31.
- Ele não vai ler todos os capítulos e vai propor o próprio modelo de aprovação; esperar isso antes de reescrever. Capa e nota da edição ficam para depois.
- Modelo de trabalho (2026-10-31): uma thread por capítulo, título cap.XX-Reeditor, seguindo .agents/skills/reeditor/SKILL.md (skill aprovada em 2026-10-31; ele pediu as 23 threads de uma vez, no Opus 5.5 com esforço high, partindo da branch claude/project-thread-9ivjk2). Agentes revisores vêm depois, não agora.
- **Branches (pedido de 2026-10-31):** não criar várias branches. Quando os 23 capítulos terminarem, juntar tudo (PR #1 + PRs de capítulo) numa única branch `v1.0`; daí em diante trabalhar SOMENTE na `v1.0`.
- Mas sem suavizar nem relativizar: preconceito do narrador fica com o mesmo peso, sem "filtro woke" ou eufemismo.

**Why:** ele quer controlar o plano e o tom antes do loop.
**How to apply:** esperar aprovação explícita antes de cada fase; seguir a tabela de termos do plano.
