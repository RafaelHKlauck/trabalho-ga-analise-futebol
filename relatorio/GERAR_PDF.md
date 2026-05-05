# Como gerar o PDF do relatório

No ambiente atual **não há `pdflatex`/`xelatex` instalado**. O arquivo **`relatorio.html`** já foi (ou pode ser) gerado com:

```bash
cd trabalho-ga
pandoc relatorio/relatorio.md -o relatorio/relatorio.html --standalone \
  --resource-path=".:relatorio:figuras"
```

## Opção A — PDF via Pandoc + LaTeX (recomendado no Mac)

1. Instale uma distribuição LaTeX (ex.: MacTeX ou BasicTeX).  
2. Rode:

```bash
cd trabalho-ga
pandoc relatorio/relatorio.md -o relatorio/relatorio.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=2.5cm \
  --resource-path=".:relatorio:figuras"
```

## Opção B — PDF a partir do HTML

Abra `relatorio/relatorio.html` no navegador e use **Imprimir → Salvar como PDF**.

## Opção C — Google Docs / Word

Importe `relatorio.md` ou copie as seções e insira as imagens da pasta `figuras/`.
