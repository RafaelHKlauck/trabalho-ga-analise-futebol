# Análise de Mercado e Posicionamento

> Documento da **Frente B** do pitch. Responde: *"o que já existe no mercado, o que o nosso trabalho tem de diferente, o que é melhor do que tem no mercado"* (áudio do professor).

---

## 1. Como o mercado de analytics em futebol está estruturado hoje

O mercado se divide em **três camadas** que raramente se sobrepõem:

| Camada | O que entrega | Quem usa | Faixa de preço |
|---|---|---|---|
| **Dado bruto** | Eventos anotados, vídeo, tracking | Times de elite, mídia, casas de análise | R$ 200 mil – R$ 2 milhões/ano |
| **Ferramenta de análise** | Editores de vídeo, dashboards de KPIs | Analistas e comissão técnica | R$ 30 mil – R$ 100 mil/ano |
| **Interpretação tática** | Insight pronto pro treinador | Treinadores, auxiliares | **Lacuna do mercado** — quase sempre humano caro ou inexistente |

**O grosso da indústria opera nas camadas 1 e 2.** A interpretação é jogada de volta pro analista humano, que precisa virar horas de Excel + vídeo em uma fala de 5 minutos pro treinador.

**Nossa aposta** é entrar pela camada 3, atendendo o **público que nunca conseguiu pagar a 1 nem a 2.**

---

## 2. Tabela comparativa dos principais players

| Produto | Origem | Público típico | Preço aprox. | Força principal | Onde falha |
|---|---|---|---|---|---|
| **Wyscout** | Itália (Hudl) | Times pro + olheiros + agentes | € 20–50k/ano | Catálogo gigante de vídeo + filtros de scouting | Mostra números crus; deixa toda interpretação pro analista. Caro pra mercado emergente. |
| **Hudl Sportscode** | EUA | Comissão técnica + analistas de vídeo | US$ 5–15k/ano por seat | Editor de vídeo tático melhor do mercado | Não gera insight; é só ferramenta. Curva de aprendizado alta. |
| **InStat / Stats Perform** | Rússia/Reino Unido | Times pro + mídia + apostas | Sob consulta (estimado US$ 30–80k/ano) | Cobertura ampla + API + scouting | Preço inviável fora da elite. Foco em scouting, não em adversário. |
| **StatsBomb IQ** | Reino Unido | Times pro + clubes top + analistas avançados | Sob consulta (estimado US$ 50k+/ano) | Dado de altíssima qualidade (mesmo que abrimos no open data) + visualizações avançadas | Volta toda a interpretação pro analista. Premium-only. |
| **Driblab** | Espanha | Clubes médios + departamento de scouting | Médio-alto | Modelos próprios (xG, packing, ratings) + UI moderna | Foco em **scouting** (vai contratar quem), não em **adversário** (jogar contra quem). |
| **Stats Perform Opta** | Reino Unido | Mídia + apostas + clubes | Sob consulta | Cobertura quase total dos campeonatos pro mundiais | Não tem produto vertical pro treinador — é "atacado de dados". |
| **Footovision** | França | Clubes pro | Sob consulta | Tracking via CV, sem chip nos jogadores | Pouco conhecido, foco em tracking. Não entrega interpretação. |
| **DNA Tático (nós)** | Brasil | **Clubes Série B/C/D, base, futebol feminino, amador competitivo, federações regionais** | **Tier free + assinatura acessível (R$ 200–1.000/mês)** | **Interpretação automática em PT-BR** ("joga pela direita", "pressiona alto") + integração com vídeo do clube | Cobertura inicial restrita ao open data + jogos anotados sob demanda. |

---

## 3. Mapa de competitividade (visualização para o slide)

```
                        ALTO custo
                            |
   StatsBomb IQ ━ Stats Perform
   Wyscout ━━━━━━━━━━━━━ InStat
                            |
   Hudl Sportscode ━━━━━ Driblab
                            |
                          (gap)
                            |
   Footovision ─────────────|────── Excel + vídeo (manual)
                            |
                       DNA Tático ★
                            |
                       BAIXO custo
                            └─────────────────────────
                       Mostra números                          Entrega interpretação
```

**Eixos:** custo do produto (vertical) e quão pronta pra decisão é a saída (horizontal).

**Conclusão visual:** o quadrante *"interpretação pronta + baixo custo"* está **vazio**. É onde nos posicionamos.

---

## 4. Quem é o cliente (ICP — Ideal Customer Profile)

### Perfil primário: Clube de Série B/C/D

- **Orçamento anual:** R$ 5–30 milhões.
- **Pessoal de análise:** 1–2 analistas (geralmente cumulando com outras funções).
- **Ferramentas atuais:** Excel, anotações em caderno, vídeo da SporTV/transmissão local.
- **Dor:** preparar análise de adversário em 3–5 dias entre rodadas, sem tempo nem dado pra fazer direito.
- **Disposição a pagar:** R$ 200–1.500/mês por adversário monitorado.
- **Tamanho do segmento:** Série B (20), Série C (20), Série D (64) = **104 clubes só no Brasil**. + 27 estaduais com clubes médios = **300+ potenciais**.

### Perfil secundário: Categoria de base de clubes grandes

- **Quem decide:** coordenador de base, diretor técnico.
- **Dor:** transformar categoria de base em pipeline analítico igual ao profissional, sem o mesmo orçamento.
- **Disposição a pagar:** R$ 500–3.000/mês por categoria.

### Perfil terciário: Federações e ligas regionais

- **Quem decide:** diretor de competições.
- **Dor:** valor agregado pra clubes filiados, conteúdo pra mídia, fan engagement.
- **Modelo:** white-label / licenciamento.

### Não-cliente (deliberadamente)

- **Times de elite (Série A brasileira ou europeus top)** — já têm Wyscout, têm analistas pagos, têm fluxo próprio. Esforço pra vender vs ticket não compensa no início.

---

## 5. Proposta de valor em 3 níveis

### One-liner
*"O Wyscout do clube que não pode pagar Wyscout — e em português."*

### Elevator pitch (30s)
*"Times pequenos no Brasil gastam 8 horas por semana tentando entender o próximo adversário com Excel e vídeo. Os times grandes pagam R$ 200 mil/ano por uma ferramenta que ainda exige um analista pra interpretar. Nós automatizamos a interpretação: o treinador recebe, em até 24 horas após o jogo do adversário, um diagnóstico em linguagem natural — 'joga mais pela direita, pressiona alto, depende de cruzamento' — pelo preço de uma assinatura de streaming."*

### Pitch comercial (3 frases pro fechamento)
1. **O que somos:** plataforma de análise de adversário com interpretação automática em PT-BR.
2. **Pra quem:** clubes de Série B–D, base e futebol feminino que têm vídeo mas não têm dado.
3. **Por quê agora:** visão computacional aberta + LLMs viabilizaram fazer 100x mais barato o que custava R$ 200k/ano.

---

## 6. Por que ninguém faz isso ainda? (defesa contra "mas se é fácil, alguém já fez")

| Razão | Por que não foi resolvido |
|---|---|
| **Mercado não-óbvio** | Players globais miram clubes de elite — ticket maior, ciclo de venda padronizado. Mercado brasileiro de Série B/C/D é fragmentado. |
| **Linguagem** | Wyscout/Hudl são em inglês. Treinadores brasileiros, especialmente de divisões menores, preferem PT-BR. |
| **Combinação de tecnologias é recente** | CV pra futebol em open source só amadureceu pós-2020 (SoccerNet). Modelos baseados em LLM pra texto natural só pós-2022. Janela de oportunidade aberta agora. |
| **Ninguém atacou a interpretação** | Wyscout/Hudl assumem que o cliente **já é** o analista. Nosso cliente **não é** — ele é o treinador, ou alguém que precisa entregar resumo pro treinador. |

---

## 7. Riscos competitivos e respostas

| Risco | Resposta |
|---|---|
| **Wyscout/StatsBomb descem o preço pra mercado emergente** | Eles têm estrutura de custo alta (scouts humanos). Não conseguem rentabilizar tier abaixo de R$ 30k/ano. Já tentaram, não fizeram. |
| **Concorrente brasileiro copia** | Defendemos com: (a) dataset proprietário de anotações, (b) calibração local de regras, (c) **relacionamento direto** com clubes brasileiros vs SaaS frio. |
| **Clubes preferem analista humano** | Não substituímos — **complementamos**. O analista usa o sistema pra cobrir 3x mais adversários em 1/3 do tempo. |
| **Mercado Série B/C/D não tem orçamento** | Tier free atrai (1 adversário monitorado por mês com open data). Conversão pro pago via upgrade (5 adversários, anotação assistida). |

---

## 8. Sinais de tração que valem mencionar no pitch

(Ajustar conforme o que vocês conseguirem coletar até o pitch.)

- "Conversamos com X comissões técnicas de Série B/C antes do pitch — Y deles disseram que pagariam pelo produto."
- "Validamos a interpretação automática em 2 Clásicos de 2015/16 — sistema gerou as mesmas conclusões que um analista humano teria escrito (mostrar slide com texto gerado vs leitura tática consagrada)."
- "Open data StatsBomb cobre 75 competições × 308 times — nosso MVP já roda em qualquer um deles."
- "MVP rodando: ~15 segundos do clique ao diagnóstico em texto + figuras."

---

## 9. O que dizer no pitch (resumo de 60 segundos)

> "Olhem essa tabela. Wyscout cobra duzentos mil por ano e te entrega uma planilha. Hudl te dá um editor de vídeo. Stats Perform te vende dado bruto. Todos eles assumem que do outro lado tem um analista de R$ 15 mil por mês pra traduzir. Em 99% dos clubes brasileiros, esse analista **não existe**. O que existe é um treinador, um auxiliar e um cara fazendo vídeo. Nós entregamos pra essas pessoas, em português e em 24 horas, a frase que um analista de Wyscout escreveria — 'o adversário ataca pela direita e depende de cruzamento'. **Mesma camada de cima do Wyscout, sem o Wyscout.**"
