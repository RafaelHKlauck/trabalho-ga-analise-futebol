"""Geração on-the-fly de figuras a partir de um DataFrame de eventos (sem salvar em disco)."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend não-interativo (necessário em servidor sem display)
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from mplsoccer import Pitch  # noqa: E402


def _log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT / "analise") not in sys.path:
    sys.path.insert(0, str(_ROOT / "analise"))
from lib_analise import _passes_completos  # noqa: E402

PALETTE_PADRAO = {"alvo": "#A50044", "referencia": "#004D98"}
MAX_PONTOS_HEATMAP = 3000  # kdeplot fica lento acima disso; subamostra preserva a forma


def _pitch(ax) -> Pitch:
    pitch = Pitch(pitch_type="statsbomb", line_color="black")
    pitch.draw(ax=ax)
    return pitch


def fig_heatmap_toques(df: pd.DataFrame, times: list[str]) -> plt.Figure:
    _log(f"Gerando heatmap de toques ({', '.join(times)})...")
    t0 = time.time()
    fig, axes = plt.subplots(1, len(times), figsize=(7 * len(times), 5))
    if len(times) == 1:
        axes = [axes]
    for ax, nome in zip(axes, times):
        pitch = _pitch(ax)
        sub = df[(df["team"] == nome) & df["x"].notna()]
        if len(sub) > MAX_PONTOS_HEATMAP:
            _log(f"  Subamostra: {nome} {len(sub)} → {MAX_PONTOS_HEATMAP} pontos (kdeplot).")
            sub = sub.sample(n=MAX_PONTOS_HEATMAP, random_state=42)
        if len(sub):
            pitch.kdeplot(sub["x"], sub["y"], ax=ax, fill=True, levels=50, thresh=0.05)
        ax.set_title(f"Heatmap de toques — {nome}")
    fig.tight_layout()
    _log(f"  Heatmap pronto em {time.time()-t0:.2f}s")
    return fig


def fig_recuperacoes(df: pd.DataFrame, times: list[str]) -> plt.Figure:
    _log(f"Gerando mapa de recuperações ({', '.join(times)})...")
    fig, axes = plt.subplots(1, len(times), figsize=(7 * len(times), 5))
    if len(times) == 1:
        axes = [axes]
    for ax, nome in zip(axes, times):
        pitch = _pitch(ax)
        sub = df[
            (df["team"] == nome)
            & df["type"].isin(["Ball Recovery", "Pressure", "Interception"])
            & df["x"].notna()
        ]
        if len(sub):
            pitch.scatter(sub["x"], sub["y"], ax=ax, alpha=0.45, s=22, color="darkred")
            xm = sub["x"].mean()
            ax.axvline(xm, linestyle="--", color="black", linewidth=1)
            ax.set_title(f"Recuperação / pressão — {nome} (x médio = {xm:.1f})")
        else:
            ax.set_title(f"Recuperação / pressão — {nome} (sem dados)")
    fig.tight_layout()
    return fig


def fig_passes_progressivos(df: pd.DataFrame, times: list[str]) -> plt.Figure:
    _log(f"Gerando mapa de passes progressivos ({', '.join(times)})...")
    passes = _passes_completos(df)
    prog = passes[passes["progressivo"]]
    fig, axes = plt.subplots(1, len(times), figsize=(7 * len(times), 5))
    if len(times) == 1:
        axes = [axes]
    for ax, nome in zip(axes, times):
        pitch = _pitch(ax)
        sub = prog[prog["team"] == nome]
        if len(sub):
            pitch.arrows(
                sub["x"], sub["y"], sub["pass_end_x"], sub["pass_end_y"],
                ax=ax, width=1, headwidth=4, alpha=0.55, color="navy",
            )
        ax.set_title(f"Passes progressivos (Δx≥10 m) — {nome} (n={len(sub)})")
    fig.tight_layout()
    return fig


def fig_rede_passes(df_match: pd.DataFrame, nome: str, ax=None) -> plt.Figure:
    _log(f"Gerando rede de passes — {nome}...")
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(8, 5))
    else:
        fig = ax.figure
    pitch = _pitch(ax)
    passes = df_match[
        (df_match["team"] == nome)
        & (df_match["type"] == "Pass")
        & (df_match["pass_outcome"].isna())
    ].copy()
    if len(passes) == 0:
        ax.set_title(f"Rede de passes — {nome} (sem dados)")
        if own_fig:
            fig.tight_layout()
        return fig
    media = (
        passes.groupby("player")
        .agg(x=("x", "mean"), y=("y", "mean"), n=("id", "count"))
        .reset_index()
    )
    pares = (
        passes.dropna(subset=["pass_recipient"])
        .groupby(["player", "pass_recipient"])
        .size()
        .reset_index(name="w")
    )
    nodes = media.set_index("player")
    for _, r in pares.iterrows():
        if r["player"] in nodes.index and r["pass_recipient"] in nodes.index and r["w"] >= 3:
            x1, y1 = nodes.loc[r["player"], ["x", "y"]]
            x2, y2 = nodes.loc[r["pass_recipient"], ["x", "y"]]
            ax.plot([x1, x2], [y1, y2], linewidth=float(r["w"]) / 4, alpha=0.5, color="gray")
    pitch.scatter(
        nodes["x"], nodes["y"], s=nodes["n"] * 6, ax=ax,
        zorder=5, edgecolors="black", facecolors="lightblue",
    )
    ax.set_title(f"Rede de passes — {nome}")
    if own_fig:
        fig.tight_layout()
    return fig


def fig_barras_dna(dna: pd.DataFrame, times: list[str], cores: dict[str, str] | None = None) -> plt.Figure:
    _log(f"Gerando barras DNA ({', '.join(times)})...")
    cores = cores or {}
    metricas = {
        "Passes/posse": dna["media_passes_por_posse"],
        "% prog.": dna["pct_progressivos"] * 100,
        "x rec. médio": dna["x_medio_recuperacao"],
        "% cruzamentos": dna["pct_cruzamentos"] * 100,
        "xG/jogo": dna["xg_por_jogo"],
    }
    fig, axes = plt.subplots(1, len(metricas), figsize=(4 * len(metricas), 4))
    for ax, (nome, serie) in zip(axes, metricas.items()):
        serie_filtrada = serie.loc[[t for t in times if t in serie.index]]
        cols = [cores.get(str(t), "#444444") for t in serie_filtrada.index]
        ax.bar(serie_filtrada.index.astype(str), serie_filtrada.values, color=cols, edgecolor="black")
        ax.set_title(nome)
        ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    return fig
