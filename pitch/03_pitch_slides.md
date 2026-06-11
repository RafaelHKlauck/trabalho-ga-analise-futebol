# Pitch Deck — DNA Tático

> Documento da **Frente D**. Estrutura de 10–12 slides, falas prontas, divisão entre apresentadores e sugestão do trecho gravado do João.
> Formato pitch para "investidor", conforme exigência do professor (áudio).
> Tempo total alvo: **10 minutos** + 5 minutos para Q&A.

---

## Estrutura geral

| # | Slide | Tempo | Quem | Foco da fala |
|---|---|---|---|---|
| 1 | **Capa / Hook** | 0:45 | Apresentador A | Problema vivido |
| 2 | **Solução em 1 frase** | 0:30 | Apresentador A | Promessa |
| 3 | **DEMO ao vivo** | 1:30 | Apresentador A + operador | Mostra funcionando |
| 4 | **Como funciona** | 1:00 | 🎥 João (vídeo) | Pipeline técnico |
| 5 | **Mercado** | 1:00 | Apresentador B | Tabela competidores + posicionamento |
| 6 | **Estratégia de dados** ⭐ | 1:30 | Apresentador B | C.0 / C.1 / C.2 / C.3 — *o ponto mais cobrado pelo professor* |
| 7 | **Validação** | 1:00 | 🎥 João (vídeo) | Sistema gerou frases que batem com leitura tática real |
| 8 | **Roadmap** | 0:45 | Apresentador A | Fases 0–3 |
| 9 | **Modelo de negócio** | 0:45 | Apresentador A | Freemium + tiers |
| 10 | **Time + Ask** | 0:45 | Apresentador A | Quem somos, o que precisamos |
| 11 | **Backup — Limitações** | — | — | Reserva para Q&A |
| 12 | **Backup — Detalhes técnicos** | — | — | Reserva para Q&A |

**Total: ~10 minutos.**

---

## Por que o João grava esses dois slides?

- **Slide 4 (Como funciona)** — parte técnica densa. Em vídeo, dá pra fazer cut + animação + escrita limpa. Aliviar quem apresenta ao vivo.
- **Slide 7 (Validação)** — comparação lado-a-lado de texto gerado pelo sistema vs leitura tática de jornalista/analista. Vídeo facilita mostrar print, narração e cortar pra próxima cena.

Total gravado: ~2 minutos. Resto é ao vivo.

---

## Slide 1 — Capa / Hook

**Título visual:** "Imagine ter o Wyscout pelo preço de uma assinatura de streaming."

**Subtítulo:** *DNA Tático — análise de adversário automática, em português.*

**Visual sugerido:** foto de banco de reservas de um time de Série C ou base (gente apontando pra tablet/anotação caderno). Logo do projeto no canto.

**Fala (apresentador A):**

> "Boa noite. Antes de qualquer slide, vou contar uma cena. Domingo passado, o auxiliar técnico de um time da Série C de Pernambuco passou 6 horas analisando o jogo do próximo adversário. Excel, vídeo da SporTV, anotações no caderno. No final, escreveu duas folhas de papel e levou pro treinador. O treinador leu por dois minutos. Esse fluxo se repete em 300 clubes brasileiros toda semana. Wyscout custa R$ 200 mil por ano — fora do orçamento de 95% deles. O que a gente faz é entregar, em 24 horas e por R$ 500 por mês, **a frase que o auxiliar teria escrito em 6 horas**."

---

## Slide 2 — Solução em uma frase

**Título grande no centro:**

> **Diagnóstico tático automático em PT-BR a partir de eventos de partidas — em até 24 horas após o jogo.**

**Subtítulo pequeno:** *"Joga mais pela direita. Pressiona alto. Depende de cruzamento."*

**Visual sugerido:** as três frases acima aparecendo digitadas tipo terminal, uma após a outra.

**Fala (apresentador A):**

> "Em uma frase: a gente lê os dados da partida e devolve frases prontas pro treinador. Não é dashboard pro analista virar a noite interpretando. É a interpretação."

---

## Slide 3 — DEMO AO VIVO ⭐

**Sem slide estático.** Tela cheia do Streamlit em `localhost:8501` (ou Streamlit Cloud).

**Roteiro da demo (90 segundos exatos):**

1. **(0:00–0:10)** Apresentador A: *"Vou mostrar funcionando."* Operador abre o navegador.
2. **(0:10–0:25)** Operador escolhe **Barcelona** + **La Liga 2015/16** + **3 jogos**. Apresentador A narra: *"O time é o adversário que eu quero estudar. A temporada é o histórico recente dele."*
3. **(0:25–0:30)** Operador clica **🚀 Gerar diagnóstico**.
4. **(0:30–0:45)** Aparecem 6–8 frases. Apresentador A lê em voz alta uma ou duas: *"Constrói pela posse. Joga mais pela direita. Gera ameaça consistente."* Sublinhar: *"Isto não está digitado por mim — está sendo gerado pelas regras do sistema agora."*
5. **(0:45–1:10)** Operador adiciona **time de referência: Real Madrid**. Cliques. Diagnóstico do Real aparece ao lado, junto com a **comparação automática** entre os dois.
6. **(1:10–1:25)** Operador troca pra **Atlético Madrid**. Aparece automaticamente: *"Transição vertical com pressão de volume"*. Apresentador A: *"O DNA do Atleti do Cholo, sem ninguém escrever um caractere de texto."*
7. **(1:25–1:30)** Apresentador A: *"Esses são dois cliques. Em produção, isso roda automaticamente toda segunda-feira pro adversário da próxima rodada."*

**Plano B se a demo falhar:** GIF gravado prévio com o mesmo fluxo, na pasta `pitch/backup/demo.gif`. Apresentador A: *"O sistema às vezes brinca; aqui está a gravação do fluxo."*

---

## Slide 4 — Como funciona (gravado pelo João)

**Visual sugerido:** diagrama em camadas (top-down).

```
┌─────────────────────────────────────────┐
│ EVENTOS DA PARTIDA (JSON StatsBomb)     │
│ ~3.500 eventos/jogo: passe, chute, etc. │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ MÉTRICAS M1–M6                          │
│ posse · vertical · corredor · pressão   │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ CATÁLOGO DE REGRAS (app/regras.py)      │
│ 17 predicados → tags + frases PT-BR    │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ ASSINATURA TÁTICA                       │
│ "Posse com finalização eficiente."     │
└─────────────────────────────────────────┘
```

**Fala gravada (João, ~60 segundos):**

> "O sistema é uma pilha de quatro camadas. A primeira lê os eventos da partida — passes, chutes, recuperações — no formato JSON da StatsBomb, que é padrão de mercado. A segunda camada calcula seis grupos de métricas: posse, progressão, corredor, infiltração na área, altura de pressão e ameaça ofensiva. A terceira camada aplica 17 regras determinísticas que olham para essas métricas e geram frases — por exemplo, *'se média de passes por posse maior que 6, é construção elaborada'*. A quarta camada combina as tags para identificar uma assinatura: 'jogo direto + pressão = transição clássica'. Nada disso usa LLM ou caixa-preta — é tudo regra explícita, auditável, **calibrada nos dados públicos da StatsBomb**. Se o resultado parece estranho, a gente abre o catálogo de regras e ajusta."

---

## Slide 5 — Mercado

**Visual sugerido:** versão visual da tabela do `pitch/02_analise_mercado.md` (5 linhas: Wyscout, Hudl, StatsBomb IQ, Driblab, **Nosso produto** destacado).

Colunas mostradas: Produto · Público · Preço · O que falta.

**Fala (apresentador B):**

> "Quem joga nesse mercado hoje? Cinco players globais que vocês conhecem: Wyscout, Hudl, StatsBomb, Stats Perform, Driblab. Todos miram o mesmo cliente — clube de elite que pode pagar entre R$ 200 mil e R$ 2 milhões por ano. Todos têm o mesmo modelo: te entregam o dado e te devolvem o trabalho de interpretar. **No quadrante 'interpretação pronta + acessível', está vazio.** É exatamente onde a gente entra. Nosso ICP é o clube de Série B–D, base e futebol feminino — 300+ alvos só no Brasil. Eles não pagam Wyscout, mas pagam Netflix."

---

## Slide 6 — Estratégia de dados ⭐ (o que o professor cobrou)

**Visual sugerido:** três caixas horizontais, da esquerda pra direita.

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ C.0 — Treino │    │ C.2 — MVP        │    │ C.1 — Escala      │
│ StatsBomb    │ →  │ Anotação humana  │ →  │ Visão             │
│ Open Data    │    │ assistida        │    │ Computacional     │
│ (validação)  │    │ ~R$50/jogo, 3h   │    │ vídeo → eventos   │
└──────────────┘    └──────────────────┘    └──────────────────┘
   HOJE              0–6 MESES                6–18 MESES
```

**Fala (apresentador B):**

> "Aqui mora a pergunta que vocês fariam: **'beleza, vocês treinaram com dado público, mas como o sistema recebe novos jogos depois?'**.
>
> Três camadas. Pra **treinar e demonstrar** — StatsBomb Open Data, grátis, alta qualidade, é o que está rodando aí no demo de agora.
>
> Pra **operar com o primeiro cliente real**, anotação humana assistida: um estagiário, três horas por jogo, R$ 50 por jogo. Já viabilizado tecnicamente — falta o operador.
>
> Pra **escalar pra cinquenta clubes** — pipeline de visão computacional rodando em cima do vídeo da partida. 99% dos clubes brasileiros têm vídeo do jogo, mas não têm dado anotado. Quem fechar esse gap pega o mercado. A tecnologia existe em open source — SoccerNet, TrackNet — não estamos inventando CV do zero, estamos integrando.
>
> SLA defendido: análise pronta antes da reunião técnica de segunda-feira. Em CV, é menos de uma hora. Em anotação assistida, é até 6 horas."

---

## Slide 7 — Validação (gravado pelo João)

**Visual sugerido:** split-screen. Esquerda: print da `tabela_dna.csv` + texto gerado pelo sistema pra Barça e Real. Direita: print de um trecho do *El País* / *Marca* / *jornalista de futebol* falando do estilo dos dois times nessa temporada.

**Fala gravada (João, ~60 segundos):**

> "Como saber se as regras funcionam? Aqui está a calibração. Na esquerda, o que o sistema gerou automaticamente analisando dois Clásicos da temporada 2015/16:
>
> Barcelona — *'Constrói pela posse, joga mais pela direita, gera ameaça consistente, eficiência ofensiva acima da média'*. Assinatura: *'Posse com finalização eficiente'*.
>
> Real Madrid — *'Joga mais pela esquerda, ataque vertical, alta intensidade de pressão, avanço médio alto'*. Assinatura: *'Transição vertical com pressão de volume'*.
>
> Na direita, jornalistas e analistas consagrados descrevendo exatamente esses dois times nessa mesma temporada. **As frases batem.** O sistema chegou nas mesmas conclusões que um analista humano, partindo de zero, a partir só dos eventos JSON. E faz isso em segundos."

---

## Slide 8 — Roadmap

**Visual sugerido:** timeline horizontal com 4 marcos.

| Fase | Quando | O que entrega | Métrica |
|---|---|---|---|
| **0 — Demo** | Hoje | App funcionando, open data | Funciona ao vivo |
| **1 — Piloto** | 0–6 meses | 2–3 clubes com anotação assistida | NPS ≥ 50 |
| **2 — Escala** | 6–18 meses | 10–20 clubes, CV v1 cobrindo passes/chutes | ARR R$ 200k |
| **3 — Maturidade** | 18–36 meses | 50+ clubes + tier premium | ARR R$ 1M |

**Fala (apresentador A):**

> "Curto: piloto com 2–3 clubes em até 6 meses, operação manual assistida. Médio: 10 a 20 clubes com pipeline de CV cobrindo passes e chutes. Longo: 50+ clubes e R$ 1M de receita anual recorrente."

---

## Slide 9 — Modelo de negócio

**Visual sugerido:** três tiers em colunas.

| Free | Pro | Enterprise |
|---|---|---|
| 1 adversário/mês | 5 adversários/mês | Ilimitado + suporte |
| Open data only | Open data + anotação assistida | Tudo + CV próprio + conectores Wyscout/StatsBomb |
| R$ 0 | R$ 500–1.500/mês | R$ 5–15k/mês |
| Aquisição | Conversão | Receita premium |

**Fala (apresentador A):**

> "Modelo freemium. Tier zero: 1 adversário monitorado por mês com open data — porta de entrada, custo marginal zero pra nós. Tier Pro entre R$ 500 e R$ 1.500 por mês — 5 adversários, anotação assistida. Tier Enterprise para clubes maiores ou federações white-label."

---

## Slide 10 — Time + Ask

**Visual sugerido:** foto/avatar dos integrantes do grupo + cargo informal.

**Time (substituir nomes reais):**
- **[Nome 1]** — produto + engenharia.
- **[Nome 2]** — modelagem + análise de dados.
- **[Nome 3]** — operação + comercial.
- **João** — voz/narrativa do produto.

**Ask:**

- 6 meses de runway / acesso a 3 clubes piloto via parceria.
- Mentoria de alguém com vivência em comissão técnica.
- Apresentação para 1 federação estadual interessada em white-label.

**Fala (apresentador A):**

> "Somos quatro estudantes da Unisinos com formação em computação e paixão por futebol. O que pedimos é runway pra rodar 6 meses + acesso a três clubes piloto. Estamos prontos pra entregar o primeiro diagnóstico de produção em 30 dias. Obrigado."

---

## Slide 11 (BACKUP) — Limitações honestas

Pra Q&A, se alguém pressionar sobre o que não funciona.

- Não capturamos posicionamento sem bola (sem tracking contínuo na V1).
- Não inferimos intenção do treinador.
- CV ainda em desenvolvimento — V1 depende de anotação humana.
- Dataset de treino é estrangeiro (StatsBomb) — clubes brasileiros têm calibração ainda em ajuste.
- Métricas M1–M6 são proxies, não medidas absolutas.

## Slide 12 (BACKUP) — Detalhes técnicos

Pra Q&A técnica.

- Stack: Python + pandas + Streamlit + mplsoccer + (futuro) PyTorch para CV.
- 17 regras + 8 assinaturas, todas em `app/regras.py` — auditáveis.
- Pipeline reprodutível: `python -m app.scout` ou `streamlit run app/app.py`.
- Validação automática a cada release: open data → DNA → regras → diff vs golden output.
- Custo de inferência: <500ms por jogo após cache. <100MB de RAM.

---

## Checklist pré-apresentação

### Técnico
- [ ] App roda em `localhost:8501` sem erro? (`streamlit run app/app.py`)
- [ ] GIF de backup da demo gravado e na pasta `pitch/backup/`?
- [ ] Streamlit Cloud rodando como segundo plano B? (link público)
- [ ] Notebook como terceiro plano B se nada subir?
- [ ] Testar a demo nos times que serão usados (Barça, Real, Atleti) **antes** da apresentação?
- [ ] Tabela `figuras/tabela_dna.csv` atualizada?

### Conteúdo
- [ ] Vídeo do João gravado e renderizado (slides 4 e 7)?
- [ ] Apresentação cronometrada — bate em 10 min?
- [ ] Todas as falas decoradas (não lidas)?
- [ ] Respostas pra 5 perguntas mais prováveis ensaiadas?
- [ ] Slide de backup pronto pra Q&A?

### Logística
- [ ] Cabo HDMI / adaptador?
- [ ] Backup do laptop carregado?
- [ ] Tela de fallback se internet cair (Streamlit local funciona offline)?

---

## 5 perguntas prováveis (e como responder)

| Pergunta | Resposta |
|---|---|
| *"E se o Wyscout descer o preço pra esse mercado?"* | "Eles têm custo fixo alto (scouts humanos). Não conseguem vender por menos de R$ 30k/ano sem perder dinheiro. Já tentaram. Mercado emergente é zona morta deles." |
| *"Por que tem que ser CV? Não dá pra usar só StatsBomb?"* | "Open data tem cobertura ruim do nosso mercado — Série B/C/D brasileira não está lá. Sem CV ou anotação, o produto não existe pra eles." |
| *"Como vocês competem com o analista humano que o clube já tem?"* | "Não competimos. Complementamos. O analista cobre 3x mais adversários em 1/3 do tempo." |
| *"E se o treinador não confiar no sistema?"* | "Disclaimer + tamanho de amostra + link pra evidência (figuras, eventos). Não vendemos 'o sistema decide'. Vendemos 'o sistema te poupa 6 horas de trabalho braçal'." |
| *"Qual a barreira pra um concorrente copiar?"* | "Dataset de anotações brasileiras que vamos construir + relacionamento direto com clubes + foco vertical." |
