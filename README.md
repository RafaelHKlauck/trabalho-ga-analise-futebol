# Trabalho Grau A — DNA tático (StatsBomb Open Data)

Análise de estilo de jogo (Barcelona vs Real Madrid, La Liga 2015/16, dois clásicos) com métricas M1–M6 e figuras.

## Requisitos

- Python 3.10+ (o projeto usa `.venv` local)
- Dados em `open-data-master/data/` (clone do [statsbomb/open-data](https://github.com/statsbomb/open-data))

## Uso rápido

```bash
cd trabalho-ga
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r analise/requirements.txt
python analise/run_gerar_figuras.py   # gera figuras/*.png e figuras/tabela_dna.csv
jupyter notebook analise/analise_dna_tatico.ipynb
```

## Atribuição

Dados: **StatsBomb** — ver licença e _Media Pack_ no repositório oficial.
