# Plano — Trabalho Grau A: DNA tático com StatsBomb Open Data

**Disciplina:** computação aplicada ao futebol (Unisinos)  
**Tema:** Análise de estilo tático de times — *“Como identificar automaticamente o estilo de jogo de um time?”*  
**Fonte de dados:** [StatsBomb Open Data](https://github.com/statsbomb/open-data)  
**Entrega (conforme PDF):** até **08/05/2026**, antes do início da aula (fechamento **19h30**), via Moodle + apresentação presencial no dia.

---

## 1. Avaliação do plano do ChatGPT + complementos importantes

O plano em três partes (conceitos → proposta de sistema → integração/evolução) está **alinhado ao enunciado oficial** do trabalho (modelagem, métricas, qualidade dos dados, visualização, proposta, limitações, evolução).

**O que está muito bem encaminhado**

- Escopo enxuto (**2 times, 1–2 jogos, 4–6 métricas bem explicadas**) — combina com a rubrica (interpretação e coerência, não “volume”).
- Uso de eventos com **localização e tempo** — suficiente para posse/progressão/pressão/ataque sem inventar tracking completo.
- Destaque para **limitações** e **visualização** — itens explícitos na avaliação.

**Complementos que costumam fazer diferença na nota**

| Complemento | Por quê |
|-------------|--------|
| **Definir “posse” de forma operacional** | O JSON não entrega uma coluna “posse”; vocês precisam de uma regra (ex.: sequência de eventos do mesmo `team_id` até perda de bola). Documentem a regra no relatório. |
| **Comparar métricas “por 90 min”** quando juntarem mais de um jogo ou tempos de jogo diferentes | Evita conclusões enviesadas por duração. |
| **Escolher uma competição/temporada fixas** em `competitions.json` | Narrativa única (“La Liga 2015/16”, “mundial feminino”, etc.) e menos ruído metodológico. |
| **Atribuição StatsBomb** | O repositório pede citar **StatsBomb** e usar o **Media Pack** em trabalhos públicos — incluir no relatório ([README do repositório](https://github.com/statsbomb/open-data)). |
| **Clareza “métrica vs proxy”** | Ex.: “progressão” via passes que avançam em X — é proxy do conceito tático, não medição direta da intenção do técnico. |
| **Parte 3 (evolução)** | Amarrar explicitamente ao que a disciplina for acrescentando depois (novos conceitos nas aulas): ex. refinamento da definição de posse, mais um gráfico, revisão de limitações. |
| **Proposta de sistema** | Pode ser **dashboard conceitual** (wireframe + fluxo de dados); não precisa ser produto final — mas precisa mostrar **o que o usuário vê** e **como isso apoia decisão** (preparação de jogo / adversário). |

---

## 2. O que você vai precisar do repositório [statsbomb/open-data](https://github.com/statsbomb/open-data)

Estrutura oficial (resumo):

| Caminho no repo | Conteúdo | Uso no seu tema |
|-----------------|----------|-----------------|
| `data/competitions.json` | Lista de competições e temporadas disponíveis | Escolher **competição + temporada** e obter os IDs para achar partidas. |
| `data/matches/<competition_id>/<season_id>.json` | Metadados das partidas (times, placar, datas, IDs) | Selecionar **1–2 jogos** entre os dois times escolhidos; obter **`match_id`**. |
| `data/events/<match_id>.json` | Eventos da partida (passes, pressão, chutes, duelos, etc.) | **Núcleo da análise**: localização (`location`), tipo (`type`), time (`team`), instante (`minute`, `second`), qualificadores em `pass`, `shot`, etc. |
| `data/lineups/<match_id>.json` | Escalações / jogadores por partida | Opcional: contexto de nomes e titulares; menos crítico que `events` para DNA agregado. |
| `data/three-sixty/<match_id>.json` | Dados 360 (visão ampliada) **só em alguns jogos** | Opcional; não dependam disso para o trabalho base. |
| `doc/` (PDFs) | Especificação de eventos, partidas, etc. | **Leitura essencial:** documentação de **eventos** e, se precisarem, **matches** — para saber nomes exatos de tipos e campos no JSON. |
| `LICENSE.pdf` | Licença de uso | Saber obrigações de uso/divulgação (em conjunto com o README). |

**Ordem prática de trabalho com os arquivos**

1. Abrir `competitions.json` → escolher uma temporada com jogos que interessem.  
2. Abrir o JSON de `matches` correspondente → listar partidas e escolher **duas equipes** que se enfrentem (idealmente **dois jogos** entre os mesmos times, se existirem; senão, **um jogo** bem justificado).  
3. Para cada `match_id` escolhido, carregar `events/<match_id>.json`.  
4. Consultar `doc/Open Data Events v4.0.0.pdf` quando houver dúvida sobre tipos de evento ou campos (`pass` → `cross`, `length`, `angle`, `body_part`, etc.).

---

## 3. Modelagem de dados (Parte 1 — entrega)

**Entidades sugeridas (conceitual)**

- **Competição / Temporada** — vindas de `competitions.json` + pasta `matches`.  
- **Partida** — `match_id`, mandante/visitante, placar, data (em `matches`).  
- **Time** — `team_id` + nome (em eventos e/ou matches).  
- **Jogador** — `player_id` quando existir no evento (nem todo evento tem jogador claro).  
- **Evento** — `id`, `index`, `period`, `timestamp` ou `minute`/`second`, `type`, `team`, `location` [x,y], subtipos (`Pass`, `Pressure`, `Ball Recovery`, `Shot`, …) e dicionários específicos (`pass`, `shot`, …).

**Armazenamento no trabalho**

- **Na argumentação:** podem manter o modelo **JSON nativo** como “fonte da verdade” e mostrar **uma transformação** para **tabela** (`DataFrame`): uma linha por evento (ou por passe), colunas derivadas (ex.: `dx` da progressão, zona do campo).  
- Isso atende “estrutura de armazenamento” + “aplicação em dados” sem obrigar um banco SQL.

---

## 4. Métricas sugeridas (4–6, com interpretação)

Escolha **um bloco coeso** que responda à pergunta do DNA. Exemplo equilibrado:

| # | Métrica (proxy) | Ideia de cálculo (a detalhar no relatório) | Leitura tática |
|---|-----------------|---------------------------------------------|----------------|
| 1 | **Estilo de construção — passes por sequência / duração média da posse** | Agrupar eventos consecutivos do mesmo `team_id` até mudança de posse; média de passes e duração estimada (delta de tempo entre eventos). | Mais passes por posse e posse mais longa → tendência a **jogo de construção**; poucos passes e transições rápidas → **direto/transição**. |
| 2 | **Progressão no campo** | Para `Pass` (e opcionalmente `Carry`), média de **avanço em x** (coordenada “para frente” do campo StatsBomb) ou % de passes que ultrapassam uma linha (ex. meio-campo). | Mede **verticalidade** vs circulação lateral. |
| 3 | **Lateralização (esquerda vs direita)** | Distribuição de eventos ofensivos ou passes no terço final por **lado** (y positivo vs negativo, ou terços laterais). | **Bias de corredor** (ex.: overload pelo lado do ponta). |
| 4 | **Centro vs infiltração** | Razão entre **cruzamentos** (`pass.cross` quando aplicável) vs passes/chutes de **área central** (faixa de x,y); ou contagem de `pass` em zonas centrais vs amplas. | **Cruzamentos vs jogo pelo meio**. |
| 5 | **Altura da recuperação** | Para `Ball Recovery` (e/ou primeiros eventos defensivos após perda), média da coordenada **x** de recuperação. | Recuperação mais alta no campo → **bloco alto / pressão** (proxy). |
| 6 | **Finalização e ameaça** | xG médio por jogo (`shot` com `shot.statsbomb_xg` quando existir) e/ou chutes por 90’. | Complementa o DNA “ofensivo” sem ser só posse. |

**Visualizações (forte impacto na avaliação)**

- **Mapa de passes** ou **rede de passes** (nós = jogadores ou zonas; arestas = volume ou valor esperado).  
- **Heatmap** de recuperações ou de pressão (`Pressure`).  
- **Gráfico de barras** comparando os dois times nas 4–6 métricas (mesmo eixo, mesma escala ou normalizado).

Ferramentas comuns em Python: `pandas`, `matplotlib`/`seaborn`, e para campo: **mplsoccer** (opcional mas ajuda no visual profissional).

---

## 5. Qualidade dos dados e limitações (obrigatório na nota)

**Fontes de erro / limitação típicas**

- Codificação humana dos eventos (subjetividade, consistência entre analistas).  
- Eventos ausentes ou atrasados na sequência; nem toda “posse” é trivial de reconstruir só com eventos.  
- **Sem tracking contínuo** dos 22 jogadores — só instantes de evento (e 360 só em parte dos jogos).  
- Contexto tático parcial (marcacao, cansaco, clima, instrucoes no intervalo) **nao esta no dataset**.  
- xG e métricas derivadas são **modelos** — úteis, mas não verdades absolutas.

**Impacto:** DNA identificado é **perfil estatístico do que foi registrado**, não “a verdade única” sobre o estilo do clube em todos os contextos.

---

## 6. Proposta de sistema (Parte 2 — “ferramenta de análise de adversário”)

**Problema:** apoiar analista/técnico a **rotular e comparar** o perfil de um adversário (posse vs transição, viés lateral, progressão, altura de recuperação) com base em eventos de partidas recentes.

**Fluxo integrado (modelagem → métricas → visualização)**

1. **Ingestão:** seleção de competição/temporada e jogos (`competitions` → `matches` → `events`).  
2. **Processamento:** limpeza, definição de posse, agregação por time e por jogo.  
3. **Análise:** cálculo das 4–6 métricas + normalização.  
4. **Visualização:** dashboard com mapas + gráficos comparativos + texto interpretativo (“Time A = mais progressivo pelo corredor direito e recuperação mais alta”).

**Coleta:** dados já públicos no GitHub; **limitações:** cobertura parcial de ligas/temporadas; atualização depende do repositório; não substitui relatório de vídeo.

---

## 7. Integração e evolução (Parte 3)

- **Integração:** explicar como a **modelagem** (evento como unidade), as **métricas** (proxies do DNA) e as **visualizações** (padrões visíveis) se encadeiam para a decisão do usuário.  
- **Evolução:** lista objetiva do que mudou da primeira versão (ex.: “posse mal definida” → “regra documentada”; “um gráfico” → “mapa + barras”; métricas revisadas após novo conteúdo da disciplina).  
- **Reflexão final:** contraste explícito entre análise inicial simples e sistema proposto (o que mantiveram, o que evoluiu, o que mudou ao mudar o contexto).

---

## 8. Checklist final (alinhado ao PDF + ao tema)

- [ ] Entidades e atributos definidos (com diagrama ou tabela conceitual).  
- [ ] 4–6 métricas com **definição matemática/procedural** e **interpretação** em uma página cada (aprox.).  
- [ ] Dados reais do Open Data aplicados (mesmo que poucos jogos).  
- [ ] Pelo menos **duas** visualizações distintas (ex.: mapa + barras).  
- [ ] Limitações dos dados e do método discutidas com honestidade.  
- [ ] Proposta de sistema coerente com DNA/adversário.  
- [ ] Parte 3 com integração + evolução + reflexão.  
- [ ] Crédito **StatsBomb** + referência ao uso conforme licença/README.  
- [ ] Entrega no prazo e preparação para **apresentação** no dia.

---

## 9. Próximos passos práticos no seu computador

1. Clonar ou baixar o repositório: `git clone https://github.com/statsbomb/open-data.git` (ou ZIP).  
2. Escolher temporada em `data/competitions.json`.  
3. Escolher 1–2 jogos em `data/matches/...`.  
4. Carregar `data/events/<match_id>.json` e validar campos com `doc/Open Data Events v4.0.0.pdf`.  
5. Implementar notebook ou script mínimo que exporte as figuras para o relatório.

---

*Documento gerado como guia de planejamento para o Trabalho do Grau A — tema DNA tático com StatsBomb Open Data.*
