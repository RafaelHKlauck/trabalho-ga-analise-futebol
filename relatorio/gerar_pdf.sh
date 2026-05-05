#!/usr/bin/env bash
# Gera relatorio.pdf se pdflatex estiver disponível; senão gera apenas HTML.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if command -v pdflatex >/dev/null 2>&1; then
  pandoc relatorio/relatorio.md -o relatorio/relatorio.pdf \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    --resource-path=".:relatorio:figuras"
  echo "OK: relatorio/relatorio.pdf"
else
  pandoc relatorio/relatorio.md -o relatorio/relatorio.html --standalone \
    --resource-path=".:relatorio:figuras"
  echo "pdflatex não encontrado; gerado relatorio/relatorio.html (veja GERAR_PDF.md)"
fi
