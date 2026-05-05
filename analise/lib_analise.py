"""Carregamento e normalização de eventos StatsBomb (Open Data) em DataFrame tabular."""

import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "open-data-master" / "data"
FIGURAS_DIR = Path(__file__).resolve().parent.parent / "figuras"
MATCHES = {
    266424: {"label": "Bernabeu (21/11/2015)", "home": "Real Madrid", "away": "Barcelona"},
    267533: {"label": "Camp Nou (02/04/2016)", "home": "Barcelona", "away": "Real Madrid"},
}
TEAMS = ["Barcelona", "Real Madrid"]


def load_events(match_id: int) -> pd.DataFrame:
    """Lê events/<match_id>.json e retorna um DataFrame com uma linha por evento e colunas planas."""
    with open(DATA_DIR / "events" / f"{match_id}.json", encoding="utf-8") as f:
        raw = json.load(f)
    rows = []
    for e in raw:
        loc = e.get("location") or [None, None]
        pass_ = e.get("pass") or {}
        end = pass_.get("end_location") or [None, None]
        shot = e.get("shot") or {}
        rows.append(
            {
                "match_id": match_id,
                "id": e.get("id"),
                "index": e.get("index"),
                "period": e.get("period"),
                "minute": e.get("minute"),
                "second": e.get("second"),
                "type": e.get("type", {}).get("name"),
                "team": e.get("team", {}).get("name"),
                "player": (e.get("player") or {}).get("name"),
                "position": (e.get("position") or {}).get("name"),
                "possession": e.get("possession"),
                "possession_team": (e.get("possession_team") or {}).get("name"),
                "play_pattern": (e.get("play_pattern") or {}).get("name"),
                "duration": e.get("duration"),
                "x": loc[0],
                "y": loc[1],
                "pass_end_x": end[0],
                "pass_end_y": end[1],
                "pass_length": pass_.get("length"),
                "pass_height": (pass_.get("height") or {}).get("name"),
                "pass_cross": bool(pass_.get("cross")),
                "pass_outcome": (pass_.get("outcome") or {}).get("name"),  # None = completo
                "pass_recipient": (pass_.get("recipient") or {}).get("name"),
                "shot_xg": shot.get("statsbomb_xg"),
                "shot_outcome": (shot.get("outcome") or {}).get("name"),
            }
        )
    return pd.DataFrame(rows)


def load_all() -> pd.DataFrame:
    """Concatena os eventos dos dois clásicos definidos em MATCHES."""
    return pd.concat([load_events(m) for m in MATCHES], ignore_index=True)


def _possession_sequences(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por sequência de posse (match + id de posse + time)."""
    posses = (
        df.groupby(["match_id", "possession", "possession_team"], dropna=False)
        .agg(
            eventos=("id", "count"),
            passes=("type", lambda s: (s == "Pass").sum()),
            ini=("minute", "min"),
            fim=("minute", "max"),
        )
        .reset_index()
        .rename(columns={"possession_team": "team"})
    )
    posses["duracao_min_aprox"] = posses["fim"] - posses["ini"]
    return posses


def metric_m1(df: pd.DataFrame) -> pd.DataFrame:
    """M1: estilo de construção — posses (incl. por jogo), passes/posse, duração média da posse."""
    posses = _possession_sequences(df)
    m1 = posses.groupby("team").agg(
        posses_total=("possession", "count"),
        media_passes_por_posse=("passes", "mean"),
        mediana_passes_por_posse=("passes", "median"),
        posses_longas_5plus=("passes", lambda s: (s >= 5).mean()),
        duracao_media_min_posse=("duracao_min_aprox", "mean"),
    )
    pj = posses.groupby(["team", "match_id"]).size().reset_index(name="posses_no_jogo")
    posses_por_jogo = pj.groupby("team")["posses_no_jogo"].mean().rename("posses_por_jogo_media")
    return m1.join(posses_por_jogo)


def _passes_completos(df: pd.DataFrame) -> pd.DataFrame:
    p = df[(df["type"] == "Pass") & (df["pass_outcome"].isna())].copy()
    p["dx"] = p["pass_end_x"] - p["x"]
    p["progressivo"] = p["dx"] >= 10
    return p


def metric_m2(df: pd.DataFrame) -> pd.DataFrame:
    """M2: progressão — avanço médio em x (m) e % de passes completos com dx >= 10 m."""
    passes = _passes_completos(df)
    return passes.groupby("team").agg(
        avanco_medio_m=("dx", "mean"),
        pct_progressivos=("progressivo", "mean"),
        passes_completos=("id", "count"),
    )


def metric_m3(df: pd.DataFrame) -> pd.DataFrame:
    """M3: lateralização no terço de ataque (x 80–120) — % eventos à esquerda (y >= 40) vs direita."""
    ataq = df[df["x"].between(80, 120, inclusive="both")].copy()
    ataq["lado"] = np.where(ataq["y"] >= 40, "esquerdo", "direito")
    m3 = (
        ataq.groupby(["team", "lado"])
        .size()
        .unstack(fill_value=0)
        .assign(total=lambda d: d.sum(axis=1))
        .assign(
            pct_esq=lambda d: d["esquerdo"] / d["total"],
            pct_dir=lambda d: d["direito"] / d["total"],
        )
    )
    return m3


def metric_m4(df: pd.DataFrame) -> pd.DataFrame:
    """M4: passes que entram na grande área (fim x >= 102) — cruzamentos e % sobre o total nessa região."""
    passes = _passes_completos(df)
    passes_ataq = passes[passes["pass_end_x"] >= 102]
    m4 = passes_ataq.groupby("team").agg(
        cruzamentos=("pass_cross", "sum"),
        total_passes_para_area=("id", "count"),
    )
    m4 = m4.assign(
        passes_centro_ou_pela_area=lambda d: d["total_passes_para_area"] - d["cruzamentos"],
        pct_cruzamentos=lambda d: d["cruzamentos"] / d["total_passes_para_area"].replace(0, np.nan),
    )
    return m4


def metric_m5(df: pd.DataFrame) -> pd.DataFrame:
    """M5: altura média (x) de recuperação/duelos/pressão/interceptação (proxy de linha defensiva)."""
    recs = df[df["type"].isin(["Ball Recovery", "Pressure", "Interception", "Duel"])]
    return recs.groupby("team").agg(
        x_medio_recuperacao=("x", "mean"),
        n_eventos_defensivos=("id", "count"),
        pressure_count=("type", lambda s: (s == "Pressure").sum()),
    )


def metric_m6(df: pd.DataFrame) -> pd.DataFrame:
    """M6: ameaça — chutes e xG por jogo (média dos dois clásicos) e gols totais."""
    shots = df[df["type"] == "Shot"].copy()
    m6 = (
        shots.groupby(["team", "match_id"])
        .agg(
            chutes=("id", "count"),
            xg_total=("shot_xg", "sum"),
            gols=("shot_outcome", lambda s: (s == "Goal").sum()),
        )
        .reset_index()
    )
    return m6.groupby("team").agg(
        chutes_por_jogo=("chutes", "mean"),
        xg_por_jogo=("xg_total", "mean"),
        gols_total=("gols", "sum"),
    )


def build_dna_table(df: pd.DataFrame) -> pd.DataFrame:
    """Consolida M1–M6 numa única tabela por time (dois clásicos agregados)."""
    m1 = metric_m1(df)
    m2 = metric_m2(df)
    m3 = metric_m3(df)
    m4 = metric_m4(df)
    m5 = metric_m5(df)
    m6 = metric_m6(df)
    return (
        m1.join(m2[["avanco_medio_m", "pct_progressivos", "passes_completos"]])
        .join(m3[["pct_esq", "pct_dir"]])
        .join(m4[["pct_cruzamentos", "cruzamentos", "total_passes_para_area"]])
        .join(m5[["x_medio_recuperacao", "pressure_count", "n_eventos_defensivos"]])
        .join(m6)
    )


def export_dna_table_csv(
    df: pd.DataFrame,
    *,
    path: Path | None = None,
    decimals: int = 2,
) -> Path:
    """Grava a tabela DNA (build_dna_table) em CSV; destino padrão: figuras/tabela_dna.csv."""
    out = path or FIGURAS_DIR / "tabela_dna.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    dna = build_dna_table(df)
    dna.round(decimals).to_csv(out)
    return out
