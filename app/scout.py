"""Orquestra DNA + regras + assinatura num diagnóstico tático automático."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


def _log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT / "analise") not in sys.path:
    sys.path.insert(0, str(_ROOT / "analise"))
from lib_analise import build_dna_table  # noqa: E402

from app.regras import REGRAS, assinatura_para  # noqa: E402


@dataclass(frozen=True)
class Frase:
    tag: str
    grupo: str
    peso: int
    texto: str

    def __str__(self) -> str:
        return self.texto


@dataclass(frozen=True)
class Diagnostico:
    time: str
    n_jogos: int
    frases: list[Frase]
    assinatura: str | None
    dna_row: pd.Series

    def como_markdown(self) -> str:
        cab = f"## {self.time}\n"
        if self.assinatura:
            cab += f"**Assinatura tática:** {self.assinatura}\n\n"
        cab += f"_Amostra: {self.n_jogos} jogo(s)._\n\n"
        bullets = "\n".join(f"- {f.texto}" for f in self.frases) or "- (Sem frases acionadas.)"
        return cab + bullets


def dna_por_time(eventos: pd.DataFrame, n_jogos_por_time: dict[str, int] | None = None) -> pd.DataFrame:
    """Calcula a tabela DNA a partir de um DataFrame de eventos (mesma assinatura do build_dna_table)."""
    return build_dna_table(eventos)


def diagnosticar(
    dna: pd.DataFrame,
    time: str,
    n_jogos: int,
) -> Diagnostico:
    """Aplica as regras na linha do time e devolve um Diagnostico com frases + assinatura."""
    if time not in dna.index:
        raise KeyError(f"Time '{time}' não está na tabela DNA — disponíveis: {list(dna.index)}")
    _log(f"Aplicando {len(REGRAS)} regras no time '{time}' (n_jogos={n_jogos})...")
    row = dna.loc[time]
    ctx = {"n_jogos": n_jogos}

    frases: list[Frase] = []
    tags: set[str] = set()
    for regra in REGRAS:
        try:
            if regra.aplica(row, ctx):
                frases.append(
                    Frase(
                        tag=regra.tag,
                        grupo=regra.grupo,
                        peso=regra.peso,
                        texto=regra.frase(row, ctx),
                    )
                )
                tags.add(regra.tag)
        except (KeyError, TypeError, ZeroDivisionError):
            # Coluna faltante ou valor nulo — regra simplesmente não dispara.
            continue

    frases.sort(key=lambda f: (f.peso, f.grupo))
    assinatura = assinatura_para(tags)
    _log(
        f"  → {len(frases)} frase(s) acionada(s)"
        + (f", assinatura: '{assinatura}'" if assinatura else ", sem assinatura")
    )
    return Diagnostico(
        time=time,
        n_jogos=n_jogos,
        frases=frases,
        assinatura=assinatura,
        dna_row=row,
    )


def comparar(
    dna: pd.DataFrame,
    time_alvo: str,
    time_referencia: str,
    n_jogos: int,
) -> str:
    """Texto curto comparando o time-alvo com o time-referência em métricas-chave."""
    a = dna.loc[time_alvo]
    b = dna.loc[time_referencia]

    diffs: list[str] = []

    def cmp(metrica: str, label_mais: str, label_menos: str, fmt: str = "{:.2f}") -> None:
        va, vb = a[metrica], b[metrica]
        if pd.isna(va) or pd.isna(vb):
            return
        if abs(va - vb) < 1e-9:
            return
        verbo = label_mais if va > vb else label_menos
        diffs.append(f"{verbo} ({fmt.format(va)} vs {fmt.format(vb)} do {time_referencia})")

    cmp("media_passes_por_posse", "constrói mais", "constrói menos")
    cmp("pct_progressivos", "verticaliza mais", "verticaliza menos", "{:.0%}")
    cmp("x_medio_recuperacao", "pressiona mais alto", "pressiona mais baixo", "{:.1f}")
    cmp("pct_cruzamentos", "depende mais de cruzamento", "depende menos de cruzamento", "{:.0%}")
    cmp("xg_por_jogo", "gera mais ameaça (xG)", "gera menos ameaça (xG)")

    return f"Comparado ao {time_referencia}, o {time_alvo} " + "; ".join(diffs) + "." if diffs else (
        f"Times com perfis muito parecidos nas métricas do DNA."
    )


# --- Utilitário pra rodar standalone -----------------------------------------

def main() -> None:
    """Aplica o diagnóstico no DNA atual (Clásicos 2015/16) e imprime no stdout — útil pra validação."""
    from app.data_loader import carregar_eventos

    match_ids = [266424, 267533]
    eventos = carregar_eventos(match_ids)
    n_jogos_por_time = (
        eventos.groupby("team")["match_id"].nunique().to_dict()
    )
    dna = build_dna_table(eventos)
    for time in sorted(dna.index):
        diag = diagnosticar(dna, time, n_jogos_por_time.get(time, 1))
        print(diag.como_markdown())
        print()


if __name__ == "__main__":
    main()
