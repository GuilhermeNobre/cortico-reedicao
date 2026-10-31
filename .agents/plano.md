# Plano da reedição de O Cortiço

Texto-base: *O Cortiço*, de Aluísio Azevedo (1890, domínio público), na edição Ática de 1997
(30ª ed.), PDF em `fonte/o-cortico.pdf`.

Objetivo: uma nova edição com linguagem de 2026, compreensível, simples e funcional para o
leitor atual, seguindo a ABL e o Acordo Ortográfico de 1990, sem perder enredo, cenas, ritmo e
o tom cru do original.

Situação: **plano aprovado em 31/10/2026.** Textos originais por capítulo prontos; a reescrita começa quando o Guilherme liberar.

---

## Etapa 1. Extração do texto (feita)

- Script `scripts/extrair_capitulos.py` (Python + `pdftotext`).
- Reconstrói os parágrafos a partir do recuo do PDF e junta palavras quebradas no fim da linha.
- Resultado: 23 capítulos, cerca de 81 mil palavras, 2.243 parágrafos.

## Etapa 2. Divisão em capítulos (feita)

- Um arquivo Markdown por capítulo: `texto/original/capitulo-01.md` a `capitulo-23.md`.
- Markdown foi escolhido porque o GitHub mostra o texto formatado, o histórico do Git mostra
  cada mudança palavra por palavra e o mesmo arquivo serve de entrada para gerar o PDF.
- Antes da Etapa 3, faço uma conferência rápida do texto extraído contra o PDF
  (parágrafos colados ou partidos, erros de digitalização da fonte, como "Mirada" por "Miranda").

## Etapa 3. Loop por capítulo

Para cada capítulo, de I a XXIII, em ordem:

### 3.1 Leitura
Ler o capítulo original inteiro e anotar os termos da época que aparecem, consultando o
glossário de termos (`docs/glossario.md`) para manter a mesma tradução em todo o livro.
Termos novos entram no glossário.

### 3.2 Reescrita
Reescrever seguindo as regras abaixo e gravar em `texto/reescrito/capitulo-NN.md`.

**Mantém:**
- enredo, cenas, ordem dos fatos e todos os parágrafos (um parágrafo novo para cada original);
- diálogos com travessão;
- nomes de pessoas, apelidos e lugares;
- as imagens naturalistas (bichos, cheiros, calor, lama) e a ironia do narrador;
- o que o narrador e os personagens pensam e dizem, inclusive o preconceito, com o mesmo peso.
  Nada é suavizado, cortado ou relativizado por receio de ofender.

**Atualiza:**
- ortografia pelo Acordo de 1990 e pelo VOLP da ABL (tranqüilo → tranquilo, idéia → ideia);
- pronomes no uso brasileiro atual ("mudar-se-ia" → "ia se mudar");
- palavras em desuso por equivalentes atuais (refolhos → recantos, labutação → trabalho);
- frases longas demais, divididas quando ajuda a leitura;
- **termos da época, traduzidos para o equivalente atual conforme o contexto** (tabela abaixo).

**Proposta de tradução dos termos da época** (vai para o glossário e vale para o livro todo):

| Termo de época | Tradução atual | Observação |
| --- | --- | --- |
| crioula / crioulo | negra / negro | no século XIX, negro nascido no Brasil |
| cafuza / cafuzo | mestiça / mestiço de negro com indígena | |
| moleque (criado) | menino negro, criado | quando indica o menino escravizado ou criado da casa |
| forra / forro | liberta / liberto | |
| caixeiro | balconista, empregado do comércio | |
| casa de pasto | restaurante popular | |
| venda, taverna, bodega | venda, armazém, bar | conforme a cena |
| secos e molhados | armazém de secos e molhados | ainda compreensível |
| corte (o Rio) | capital | o Rio era a sede do Império |
| bexigas | varíola | |
| preparatórios | exames preparatórios | equivalente ao vestibular da época |
| Lei Rio Branco | Lei do Ventre Livre | |
| braça (≈ 2,2 m) | metros | "oitenta braças de fundo" → "uns 175 metros de fundo" |
| palmo (≈ 22 cm) | palmo ou metros | palmo ainda é compreensível; muro de "dez palmos" → "mais de dois metros" |
| légua (≈ 6 km) | quilômetros | "meia légua" → "uns três quilômetros" |
| réis, mil-réis, conto, vintém, tostão | mantidos | moeda da época, sem equivalente atual; converter para reais seria impreciso |

Falas com marcas de dialeto (por exemplo, "Óia, que eu me queixo ao juiz de orfe!") ficam como
estão, porque mostram o jeito de falar do personagem.

### 3.3 Revisão (agente revisor)
Um agente separado, que não participou da reescrita, revisa cada capítulo e confere:

1. ortografia e acentuação (Acordo de 1990, VOLP);
2. gramática: concordância, regência, crase, colocação pronominal;
3. pontuação e diálogos;
4. fidelidade: compara parágrafo a parágrafo com o original e aponta sentido alterado,
   trecho faltando, trecho inventado ou termo suavizado;
5. consistência: termos traduzidos iguais ao glossário e aos capítulos anteriores.

O revisor entrega uma lista de correções; eu aplico, e o capítulo é marcado como revisado.

### Ritmo e aprovação
- O capítulo I é feito primeiro e vai para sua aprovação como amostra de tom e de tradução dos termos.
- Aprovado o tom, sigo em lotes (por exemplo, 3 a 4 capítulos por vez), com um commit por
  capítulo, e aviso ao fim de cada lote.
- Cada lote vira um pull request no GitHub, para você ler e aprovar antes de juntar ao `main`.

## Etapa 4. PDF único no GitHub

- Montagem: capa, folha de rosto com crédito ao autor e à fonte (Ática, 1997; Biblioteca Virtual
  do Estudante Brasileiro/USP), nota da edição explicando os critérios, os 23 capítulos e o glossário.
- Geração com Pandoc + LaTeX (ou Typst), a partir dos arquivos Markdown, com script no repositório
  para refazer o PDF a qualquer momento.
- Publicação: o PDF fica em `dist/` e também como anexo de uma Release do GitHub
  (por exemplo, `v1.0`), que é o link de download para os leitores.

---

## Pontos para você confirmar

1. A tabela de tradução dos termos da época está como você quer?
2. Medidas (braça, légua) convertidas para metros e quilômetros, e moeda (mil-réis) mantida?
3. Ritmo em lotes com um pull request por lote, ou prefere aprovar capítulo por capítulo?
4. O PDF final leva capa e nota da edição? Algum nome de editor ou título para a edição?
