# Slides — Trabalho Grau A | DNA tático (StatsBomb)

**[Capa]** Disciplina · Integrantes · Maio/2026

---

## Problema e pergunta

- Identificar **automaticamente** o estilo de jogo (DNA tático) de um time.
- Ex.: posse vs transição · corredores · cruzamentos vs infiltração.

---

## Dados e recorte

- **Fonte:** StatsBomb Open Data (eventos JSON).
- **La Liga 2015/16** — `competition_id=11`, `season_id=27`.
- **Dois Clásicos:** `266424` (0–4) e `267533` (1–2).

---

## Modelagem (Parte 1)

- Entidades: **Partida**, **Time**, **Evento** (`type`, `x`,`y`, tempo, posse).
- **DataFrame** tabular: `analise/lib_analise.py` → uma linha por evento.

---

## Métrica M1 — Construção

- Passes por **posse** (`possession`) + duração aproximada.
- **Barcelona:** mais passes/posse e posse mais longa → construção.

---

## Métrica M2 — Progressão

- $\Delta x$ em passes completos; **progressivo** se $\Delta x \geq 10$ m.
- **Real Madrid:** maior avanço médio e % de progressivos → verticalidade.

---

## Métrica M3 — Lateralização

- Terço de ataque (x ≥ 80): esquerda vs direita (y ≥ 40).
- **Barcelona** puxa corredor **direito**; **Real** mais **esquerdo**.

---

## Métricas M4–M6

- **M4:** cruzamentos / passes para área (`x \geq 102`).
- **M5:** altura média de recuperação/pressão (proxy de bloco).
- **M6:** chutes/jogo, **xG**, gols.

---

## Visualização 1–2

- **Heatmap** de toques (densidade no campo).
- **Dispersão** de recuperação/pressão + x médio.

---

## Visualização 3–4

- **Mapa** de passes progressivos (setas).
- **Rede de passes** por jogo (hubs e ligações frequentes).

---

## Visualização 5 + tabela DNA

- **Barras** comparativas (passes/posse, % prog., x rec., % cruz., xG).
- Export: `figuras/tabela_dna.csv`.

---

## Qualidade e limitações

- Anotação humana · sem tracking contínuo · **n=2 jogos**.
- Métricas = **proxies** — não substituem vídeo tático.

---

## Parte 2 — Sistema proposto

- **Ferramenta de análise de adversário:** ingestão → métricas → dashboard.
- Usuário: analista / auxiliar técnico.

---

## Dashboard (wireframe)

- Barras DNA + mapas + rede + texto gerado por regras.
- Disclaimer de amostra e fonte StatsBomb.

---

## Parte 3 — Integração

- Modelagem → métricas → visualização → **decisão** em campo.

---

## Evolução e reflexão

- De contagens simples a **pipeline reprodutível** (notebook + script).
- Próximo passo: mais jogos, tracking, ou xThreat.

---

## Conclusão e entrega

- DNA sintetizado para **Barcelona** vs **Real Madrid** na amostra.
- **Entrega:** Moodle até **08/05/2026 19h30** + apresentação.
- **Atribuição:** StatsBomb + licença / Media Pack.
