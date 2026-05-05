#!/usr/bin/env python3
"""Gera figuras/ e figuras/tabela_dna.csv a partir do Open Data local (reproducível, sem notebook)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch

_ROOT = Path(__file__).resolve().parent.parent
_FIG = _ROOT / "figuras"
_FIG.mkdir(parents=True, exist_ok=True)

if str(_ROOT / "analise") not in sys.path:
    sys.path.insert(0, str(_ROOT / "analise"))

from lib_analise import MATCHES, TEAMS, build_dna_table, export_dna_table_csv, load_all, _passes_completos  # noqa: E402


def main() -> None:
    df = load_all()
    export_dna_table_csv(df, path=_FIG / "tabela_dna.csv")
    dna = build_dna_table(df)

    passes = _passes_completos(df)

    # --- V1 heatmap toques ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, team in zip(axes, TEAMS):
        pitch = Pitch(pitch_type="statsbomb", line_color="black")
        pitch.draw(ax=ax)
        sub = df[(df["team"] == team) & df["x"].notna()]
        pitch.kdeplot(sub["x"], sub["y"], ax=ax, fill=True, levels=50, thresh=0.05)
        ax.set_title(f"Heatmap de toques — {team}")
    fig.tight_layout()
    fig.savefig(_FIG / "v1_heatmap_toques.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # --- V2 recuperações / pressão ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, team in zip(axes, TEAMS):
        pitch = Pitch(pitch_type="statsbomb", line_color="black")
        pitch.draw(ax=ax)
        sub = df[
            (df["team"] == team)
            & df["type"].isin(["Ball Recovery", "Pressure", "Interception"])
            & df["x"].notna()
        ]
        pitch.scatter(sub["x"], sub["y"], ax=ax, alpha=0.45, s=22, color="darkred")
        xm = sub["x"].mean()
        ax.axvline(xm, linestyle="--", color="black", linewidth=1)
        ax.set_title(f"Recuperação / pressão — {team} (x médio = {xm:.1f})")
    fig.tight_layout()
    fig.savefig(_FIG / "v2_recuperacoes.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # --- V3 passes progressivos ---
    prog = passes[passes["progressivo"]]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, team in zip(axes, TEAMS):
        pitch = Pitch(pitch_type="statsbomb", line_color="black")
        pitch.draw(ax=ax)
        sub = prog[prog["team"] == team]
        pitch.arrows(
            sub["x"],
            sub["y"],
            sub["pass_end_x"],
            sub["pass_end_y"],
            ax=ax,
            width=1,
            headwidth=4,
            alpha=0.55,
            color="navy",
        )
        ax.set_title(f"Passes progressivos (Δx≥10 m) — {team} (n={len(sub)})")
    fig.tight_layout()
    fig.savefig(_FIG / "v3_passes_progressivos.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # --- V4 rede de passes por jogo ---
    def passing_network(df_match, team, ax) -> None:
        pitch = Pitch(pitch_type="statsbomb", line_color="black")
        pitch.draw(ax=ax)
        pa = df_match[
            (df_match["team"] == team)
            & (df_match["type"] == "Pass")
            & (df_match["pass_outcome"].isna())
        ].copy()
        media = pa.groupby("player").agg(x=("x", "mean"), y=("y", "mean"), n=("id", "count")).reset_index()
        pares = (
            pa.dropna(subset=["pass_recipient"])
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
            nodes["x"],
            nodes["y"],
            s=nodes["n"] * 6,
            ax=ax,
            zorder=5,
            edgecolors="black",
            facecolors="lightblue",
        )
        ax.set_title(f"Rede de passes — {team}")

    for mid in MATCHES:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        for ax, team in zip(axes, TEAMS):
            passing_network(df[df["match_id"] == mid], team, ax)
        fig.suptitle(MATCHES[mid]["label"], fontsize=12)
        fig.tight_layout()
        fig.savefig(_FIG / f"v4_rede_{mid}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # --- V5 barras DNA ---
    metricas = {
        "Passes/posse": dna["media_passes_por_posse"],
        "% prog.": dna["pct_progressivos"] * 100,
        "x rec. médio": dna["x_medio_recuperacao"],
        "% cruzamentos": dna["pct_cruzamentos"] * 100,
        "xG/jogo": dna["xg_por_jogo"],
    }
    fig, axes = plt.subplots(1, len(metricas), figsize=(18, 4))
    palette = {"Barcelona": "#A50044", "Real Madrid": "#004D98"}
    for ax, (nome, serie) in zip(axes, metricas.items()):
        cols = [palette[str(t)] for t in serie.index]
        ax.bar(serie.index.astype(str), serie.values, color=cols, edgecolor="black")
        ax.set_title(nome)
        ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(_FIG / "v5_barras_dna.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print("Arquivos gerados em", _FIG)
    print(dna.round(3))


if __name__ == "__main__":
    main()
