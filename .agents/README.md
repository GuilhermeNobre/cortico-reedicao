# .agents

Tudo o que um agente (ou uma pessoa) precisa para retomar a reedição em outra máquina.

- `plano.md`: plano aprovado em 31/10/2026, com as etapas e a tabela de tradução dos termos da época.
- `guia-de-estilo.md`: regras da reescrita (etapa 3.2) e da revisão (etapa 3.3).
- `memorias/`: memórias do projeto, com o estado do trabalho e as decisões do Guilherme.
- `skills/reeditor/SKILL.md`: skill do Reeditor, seguida pelas threads `cap.XX-Reeditor` (uma por capítulo).
- `skills/revisor/SKILL.md`: skill do Revisor textual, para as threads `cap.XX-Revisor` (uma por capítulo), que resolvem as pendências de `notas/`.

## Retomar no MacBook

```
git clone https://github.com/GuilhermeNobre/cortico-reedicao.git
cd cortico-reedicao
git checkout claude/project-thread-9ivjk2
brew install poppler   # só se for rodar a extração de novo
python3 scripts/extrair_capitulos.py
```

Antes de qualquer passo, leia `memorias/reedicao-cortico.md`: a reescrita só começa com a
liberação explícita do Guilherme.
