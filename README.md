# Trabalho Grau A — DNA tático (StatsBomb Open Data)

Análise de estilo de jogo (Barcelona vs Real Madrid, La Liga 2015/16, dois clásicos) com métricas M1–M6, figuras e relatório.

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

## Relatório e entrega

- Texto: [`relatorio/relatorio.md`](relatorio/relatorio.md)
- HTML (pandoc, sem LaTeX): `relatorio/relatorio.html` — gerar com `relatorio/gerar_pdf.sh` ou ver [`relatorio/GERAR_PDF.md`](relatorio/GERAR_PDF.md)
- Slides (roteiro): [`relatorio/slides.md`](relatorio/slides.md)
- Moodle: [`relatorio/INSTRUCOES_ENTREGA_MOODLE.md`](relatorio/INSTRUCOES_ENTREGA_MOODLE.md)

## Atribuição

Dados: **StatsBomb** — ver licença e *Media Pack* no repositório oficial.
