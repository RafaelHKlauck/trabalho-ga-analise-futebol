# Plano de execução — Trabalho do Grau B (DNA Tático)

> **Resumo em uma linha:** evoluir o trabalho do Grau A num **MVP funcionando + pitch comercial**, em que o sistema **interpreta automaticamente** o estilo do time (gera frases do tipo *"joga mais pela direita"*, *"constrói pela posse"*, *"pressão alta"*) — sem texto digitado a mão.

---

## 1. Contexto e diferença para o Grau A

O Grau A entregou modelagem + métricas + figuras + relatório, com **conclusões escritas pelo time**. O Grau B precisa entregar um **pitch para "investidor"** com produto rodando (ou prova de conceito), foco em mercado, diferencial, e estratégia de coleta de dados em produção.

| Aspecto                | Grau A                              | Grau B                                                      |
|------------------------|-------------------------------------|-------------------------------------------------------------|
| Formato                | Relatório + apresentação            | Pitch comercial + demo                                      |
| Interpretação tática   | Escrita pelo grupo                  | **Gerada automaticamente pelo sistema**                     |
| Times analisados       | 2 fixos (Barça × Real, 15/16)       | Selecionáveis na UI                                         |
| Sistema                | Só na arquitetura conceitual        | MVP rodando (Streamlit)                                     |
| Coleta de dados        | "Veio do StatsBomb open data"       | Plano explícito de **dados de treino vs dados de produção** |
| Mercado / diferencial  | Não tratado                         | Tabela comparativa + posicionamento                         |

## 2. Princípio orientador

**Tudo que vai pro pitch como insight, número ou frase tem que sair do sistema.** Se o professor pedir, ao vivo, *"troca pra Barcelona × Atlético de Madrid"*, o sistema gera as novas frases sozinho.

Esse é o ponto que vende a tese de produto: não é um dashboard cru ("aqui estão os números, interprete você"), é um **leitor tático automático**.

---

## 3. As quatro frentes de trabalho

### Frente A — MVP Streamlit com interpretação automática

**Objetivo:** ter um `app.py` rodando localmente (e idealmente no Streamlit Cloud) que recebe seleção de competição/temporada/times e devolve diagnóstico tático automático + figuras + tabela.

**Arquivos a criar:**

- `app/app.py` — UI Streamlit.
- `app/regras.py` — catálogo de regras (predicado → tag → frase). **Coração do produto.**
- `app/scout.py` — função `gerar_diagnostico(dna_row, n_jogos) -> List[Frase]` que aplica as regras e ordena por relevância.
- `app/data_loader.py` — versão genérica do `lib_analise.load_events` que aceita `match_id` arbitrário (não só os 2 hardcoded).

**Fluxo da tela:**

1. Sidebar: seletor de competição → temporada → time-alvo + (opcional) time-referência.
2. Topo: **diagnóstico em linguagem natural** (5 a 8 frases automáticas).
3. Meio: 5 figuras já existentes (`v1..v5`), regeradas dinamicamente.
4. Base: tabela DNA + disclaimer (N jogos, fonte StatsBomb).
5. Bonus: botão "comparar dois times" → diff automático ("o adversário constrói menos / pressiona mais alto / depende mais de cruzamentos").

**Estimativa:** 6–8h de uma pessoa.

### Frente B — Análise de mercado

**Objetivo:** tabela comparativa de competidores + posicionamento defensável no pitch.

**Competidores a cobrir:**

| Produto                | Público                         | Preço aprox.          | Força                                   | Gap                                          |
|------------------------|---------------------------------|-----------------------|-----------------------------------------|----------------------------------------------|
| Wyscout                | Times pro / olheiros            | €20-50k/ano           | Catálogo gigante de vídeo + scouting    | Caro; não interpreta, só mostra              |
| Hudl Sportscode        | Comissão técnica                | US$ alto              | Edição de vídeo tático                  | Não gera insight; depende do analista        |
| InStat / Stats Perform | Times pro + mídia               | Sob consulta (alto)   | Cobertura ampla + API                   | Preço; complexidade                          |
| StatsBomb IQ           | Times pro / analistas avançados | Sob consulta          | Dado de altíssima qualidade             | Volta toda interpretação pro analista        |
| Driblab                | Clubes médios + scout           | Médio-alto            | Modelos próprios (xG, packing)          | Foco em scouting, não em adversário          |
| **Nosso produto**      | **Clubes B/C/D, base, feminino, amador competitivo** | **Free + tier pago acessível** | **Interpretação automática em PT-BR**, foco em **leitura tática** | Cobertura inicial restrita ao open data       |

**Posicionamento:** *"O Wyscout custa R$200k/ano e te dá uma planilha. Nós custamos uma fração disso e te dizemos, em português, que o adversário ataca pela direita, pressiona alto e depende de cruzamentos."*

**Nicho-alvo:** clubes que **não pagam Wyscout** — Série B/C/D nacional, futebol estadual, futebol feminino, divisões de base, ligas amadoras competitivas, federações regionais.

### Frente C — Estratégia de coleta de dados

**Este é o ponto mais cobrado pelo professor.** Não basta dizer "usamos StatsBomb". Tem que separar **treino** (validação do modelo / demonstração) de **produção** (operação real, daqui pra frente).

#### C.0 — Dados de treino e demonstração
- **StatsBomb Open Data** (clone em `open-data-master/`).
- Função: validar regras, gerar demo no pitch, calibrar limiares.
- Limitação reconhecida: amostra estática, sem cobertura recente.

#### C.1 — Aposta principal: pipeline de visão computacional sobre vídeo
- **Insumo:** transmissão da partida (TV, streaming oficial, gravação do clube).
- **Pipeline:** detecção de jogadores e bola por modelo de CV (YOLO + tracking) → homografia para coordenadas do campo → classificação de eventos (passe, chute, recuperação) → JSON no mesmo schema do StatsBomb.
- **Referências de tecnologia existente:** SoccerNet, TrackNet, narya, modelos abertos de pose/tracking.
- **Por que esta é a aposta:** clubes pequenos **têm vídeo** (transmissão estadual, câmera do clube), mas **não têm dado anotado** — é exatamente o gap que destrava o mercado-alvo.
- **Status no Grau B:** apresentamos como roadmap; **não precisamos implementar** o CV. Mostramos um diagrama do pipeline e um POC de leitura de um JSON externo simulando essa saída.

#### C.2 — Bridge: anotação humana assistida
- Operador marca eventos numa UI durante/após o jogo (ponto no campo + tipo de evento).
- Função: cobrir clientes early antes do CV maduro; gerar dado de validação pro modelo de CV.
- Tempo de anotação alvo: ~2x o tempo do jogo no MVP, reduzindo com automação.

#### C.3 — Crescimento futuro: parceria/licenciamento
- StatsBomb Pro, Wyscout API, Stats Perform — quando o produto justificar custo.
- Não é foco do pitch (vira commodity de input).

#### Pipeline pós-jogo (operação)
```
fim do jogo
    ↓
ingestão (CV ou anotação humana → JSON padronizado)
    ↓
DataFrame de eventos (mesma estrutura do open data)
    ↓
agregação M1–M6 + métricas v2 (xThreat, packing — roadmap)
    ↓
aplicação das regras (scout.py)
    ↓
notificação ao analista (e-mail / dashboard / app mobile)
    ↓
disponível para a comissão técnica antes da próxima sessão de vídeo
```

**Cadência defendida no pitch:** análise do adversário pronta em **até 24h após o último jogo dele**, com tempo de operação humana inferior a 30 min.

### Frente D — Pitch + apresentação

**Estrutura (10–12 slides + backup):**

1. **Hook** — "Análise de adversário hoje custa 10h de vídeo + planilha + intuição. Para 99% dos clubes brasileiros, isso simplesmente não acontece."
2. **Solução em 1 frase** — *"Diagnóstico tático automático em 24h após o jogo, em linguagem que o treinador entende."*
3. **Demo ao vivo do MVP** — escolhe times, mostra as frases sendo geradas, mostra figuras, deixa o "investidor" pedir outro time.
4. **Como funciona (1 slide técnico)** — pipeline de dados → métricas M1–M6 → catálogo de regras → texto natural.
5. **Mercado** — tabela comparativa + posicionamento (Frente B).
6. **Estratégia de dados em produção** — pipeline C.1/C.2 (Frente C).
7. **Tração / validação** — números reais dos Clásicos: Barça 7,45 passes/posse vs Real 4,37; Barça 60% direita vs Real 55% esquerda; etc. *"Estes números foram gerados pelo sistema, não digitados — e batem com a leitura tática histórica desses jogos."*
8. **Roadmap** — MVP atual → V1 (1 liga completa) → V2 (clustering automático de estilos) → V3 (CV pipeline).
9. **Modelo de negócio** — freemium (1 time, dados StatsBomb) + tiers pagos por número de times monitorados + serviço de anotação assistida.
10. **Time** — quem é o grupo, divisão de trabalho.
11. **Ask** — o que precisaríamos pra ir adiante (recursos, parceria com um clube piloto).
12. **Backup** — detalhes de modelagem, limiares das regras, limitações.

**Trecho gravado do João:** sugiro slides 4 + 7 (parte técnica/validação) — dá pra cortar, controlar voz, e libera quem apresenta ao vivo pra carregar o lado comercial.

---

## 4. Catálogo de regras automáticas (núcleo do produto)

Cada regra avalia uma combinação de colunas do `tabela_dna.csv` e gera uma frase. Limiares iniciais calibrados pela amostra Barça × Real; no MVP ficam como constantes em `app/regras.py`, no roadmap viram comparação contra a média da liga.

### Construção e posse (de M1)
| Predicado                                                   | Tag interna             | Frase gerada                                                |
|-------------------------------------------------------------|-------------------------|-------------------------------------------------------------|
| `media_passes_por_posse >= 6`                               | `construcao_elaborada`  | "Constrói pela posse — sequências longas de passes."        |
| `media_passes_por_posse < 4`                                | `jogo_direto`           | "Jogo direto — troca de posse frequente, sequências curtas."|
| `posses_longas_5plus >= 0.45`                               | `muitas_posses_longas`  | "Pelo menos metade das posses passa de 5 passes."           |
| `duracao_media_min_posse > 0.35`                            | `posse_demorada`        | "Posse demorada — tende a controlar ritmo de jogo."         |

### Progressão (de M2)
| Predicado                                                   | Tag interna             | Frase gerada                                                |
|-------------------------------------------------------------|-------------------------|-------------------------------------------------------------|
| `pct_progressivos > 0.25`                                   | `vertical`              | "Ataque vertical — muitos passes ganhando 10m ou mais."     |
| `pct_progressivos < 0.18`                                   | `circulacao`            | "Circula muito sem verticalizar — desestabiliza o bloco."   |
| `avanco_medio_m > 3.5`                                      | `transicao_rapida`      | "Avanço médio alto — tende a transição rápida."             |

### Lateralização (de M3) — **a frase que o cliente quer ver primeiro**
| Predicado                                                   | Tag interna             | Frase gerada                                                |
|-------------------------------------------------------------|-------------------------|-------------------------------------------------------------|
| `pct_dir > 0.55`                                            | `corredor_direito`      | "Joga mais pela direita (≈ X% do ataque pelo corredor)."    |
| `pct_esq > 0.55`                                            | `corredor_esquerdo`     | "Joga mais pela esquerda (≈ X%)."                           |
| `abs(pct_dir - pct_esq) <= 0.10`                            | `bilateral`             | "Ataca pelos dois corredores de forma equilibrada."         |

### Entrada na área (de M4)
| Predicado                                                   | Tag interna             | Frase gerada                                                |
|-------------------------------------------------------------|-------------------------|-------------------------------------------------------------|
| `pct_cruzamentos > 0.25`                                    | `depende_de_cruzamento` | "Depende de cruzamentos pra chegar na área."                |
| `pct_cruzamentos < 0.10`                                    | `infiltra_pelo_meio`    | "Ataca por dentro — pouca dependência de cruzamento."       |

### Bloco e pressão (de M5)
| Predicado                                                   | Tag interna             | Frase gerada                                                |
|-------------------------------------------------------------|-------------------------|-------------------------------------------------------------|
| `x_medio_recuperacao > 55`                                  | `bloco_alto`            | "Bloco alto — recupera bola adiantado no campo."            |
| `x_medio_recuperacao < 45`                                  | `bloco_baixo`           | "Bloco baixo — recupera bola no próprio campo."             |
| `pressure_count / n_jogos > 150`                            | `pressao_intensa`       | "Alta intensidade de pressão registrada."                   |

### Ameaça (de M6)
| Predicado                                                   | Tag interna             | Frase gerada                                                |
|-------------------------------------------------------------|-------------------------|-------------------------------------------------------------|
| `xg_por_jogo > 1.5`                                         | `geracao_consistente`   | "Gera ameaça consistente — xG acima de 1,5 por jogo."       |
| `gols_total / chutes >= 0.15`                               | `finalizacao_eficiente` | "Eficiência ofensiva acima da média."                       |

### Regras combinadas (assinatura tática)
A última camada gera uma **etiqueta-resumo** combinando 2–3 tags:

| Tags simultâneas                                            | Assinatura                                                  |
|-------------------------------------------------------------|-------------------------------------------------------------|
| `construcao_elaborada` + `circulacao` + `bloco_alto`        | "Estilo posicional de posse com pressão pós-perda."         |
| `jogo_direto` + `vertical` + `bloco_baixo`                  | "Estilo de transição / contra-ataque clássico."             |
| `construcao_elaborada` + `infiltra_pelo_meio` + `geracao_consistente` | "Posicional pelo meio com finalização eficiente."  |
| `jogo_direto` + `depende_de_cruzamento` + `pressao_intensa` | "Pressão alta com chegada por cruzamento."                  |

### Resultado esperado para os Clásicos (validação do catálogo)
Aplicando as regras na `tabela_dna.csv` atual:

- **Barcelona** → "Constrói pela posse", "Circula muito sem verticalizar", "Joga mais pela direita (60%)", "Bloco alto", "Gera ameaça consistente" → assinatura *"Posicional pelo meio com finalização eficiente"*.
- **Real Madrid** → "Jogo direto", "Ataque vertical", "Joga mais pela esquerda (55%)", "Bloco médio", "Pressão intensa" → assinatura *"Estilo de transição / contra-ataque clássico"*.

**Estes textos vão bater quase frase-a-frase com o que o relatório do Grau A escreveu à mão — é a prova de que a interpretação automática funciona.**

---

## 5. Cronograma sugerido

Sem data fixa do Grau B ainda; cronograma relativo à entrega.

| Semana antes da entrega | Trilha A (MVP)                          | Trilha B (mercado) | Trilha C (dados)   | Trilha D (pitch)    |
|-------------------------|-----------------------------------------|---------------------|---------------------|---------------------|
| **T-3 semanas**         | `regras.py` + `scout.py`                | Pesquisa concorrentes | Diagrama do pipeline | Estrutura dos slides |
| **T-2 semanas**         | `app.py` + integração com `lib_analise` | Tabela comparativa pronta | Texto de C.1/C.2/C.3 escrito | Conteúdo dos slides |
| **T-1 semana**          | Deploy Streamlit Cloud + ensaio demo    | Revisão            | Revisão            | Ensaio + gravação João |
| **Véspera**             | Smoke test                              | —                  | —                  | Ensaio cronometrado  |

## 6. Próximas decisões em aberto

1. **Divisão de tarefas no grupo** — quem assume A, B, C, D? Sugestão: A precisa de quem tem mais conforto com Python (provavelmente eu/usuário); B e D podem ser de quem tem mais traquejo de apresentação.
2. **Aposta principal de dados** — confirmar **C.1 (visão computacional) como narrativa principal + C.2 (anotação assistida) como bridge**, ou outra ordem.
3. **Modelo de negócio detalhado** — freemium vs assinatura pura vs licenciamento pra federação. Vale uma rodada de discussão.
4. **Deploy do MVP** — Streamlit Cloud (free, URL pública) vs rodar local na apresentação. Streamlit Cloud dá mais credibilidade.
5. **Trecho gravado do João** — confirmar com ele quais 2 slides assumir.

## 7. O que vou começar a fazer assim que aprovado

1. Criar `app/regras.py` com todas as regras da seção 4 codificadas.
2. Criar `app/scout.py` com função de diagnóstico.
3. Generalizar `lib_analise.load_events` para aceitar qualquer `match_id` listado em `matches/`.
4. Criar `app/app.py` com a UI Streamlit mínima descrita na Frente A.
5. Testar geração de diagnóstico nos dois Clásicos do Grau A e validar que o texto bate com o relatório.

---

**Fonte de dados:** StatsBomb Open Data — atribuição obrigatória no rodapé do app conforme licença e Media Pack.
