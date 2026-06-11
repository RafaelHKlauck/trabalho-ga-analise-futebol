"""Acesso ao StatsBomb Open Data local — limitado a um catálogo curado de demos do pitch.

Para o Grau B, *não* expomos as 75 competições × 308 times do open-data: isso polui a UX
da apresentação e força carga lenta. O catálogo abaixo é escolhido a dedo para mostrar
estilos contrastantes (Barça posse, Real transição, Atleti pressing, etc.).

Pra ampliar, edite a constante CATALOGO_DEMO abaixo.
"""

from __future__ import annotations

import json
import sys
import time
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import pandas as pd


def _log(msg: str) -> None:
    """Print com timestamp para acompanhar progresso no terminal do Streamlit."""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

_ROOT = Path(__file__).resolve().parent.parent
_DATA = _ROOT / "open-data-master" / "data"

# Reaproveita o load_events do Grau A (achatamento JSON → DataFrame).
if str(_ROOT / "analise") not in sys.path:
    sys.path.insert(0, str(_ROOT / "analise"))
from lib_analise import load_events  # noqa: E402  (import depois de mexer no sys.path)


# --- Catálogo curado para o pitch -------------------------------------------
# Cada entrada é (nome_time_como_aparece_no_open_data, competition_id, season_id).
# Critério de seleção: estilos contrastantes, sample suficiente, dados disponíveis localmente.
CATALOGO_DEMO: list[tuple[str, int, int]] = [
    # Clásicos 2015/16 — base de calibração do Grau A.
    ("Barcelona",       11, 27),   # La Liga 2015/2016 — posse, MSN.
    ("Real Madrid",     11, 27),   # La Liga 2015/2016 — BBC, transição.
    ("Atlético Madrid", 11, 27),   # La Liga 2015/2016 — pressing do Cholo.
    # Premier League 2015/16 — campeonato icônico do Leicester.
    ("Leicester City",  2,  27),   # campeão surpresa, contra-ataque puro.
    ("Liverpool",       2,  27),   # virada Brendan Rodgers → Klopp ao longo da temporada.
    # Seleções — bem reconhecíveis (samples menores mas marcantes).
    ("Argentina",       43, 106),  # FIFA World Cup 2022 — Messi campeão.
    ("Spain",           55, 282),  # UEFA Euro 2024 — Espanha campeã.
]


@lru_cache(maxsize=1)
def listar_competicoes() -> pd.DataFrame:
    """Retorna um DataFrame com uma linha por (competição, temporada) disponível localmente."""
    _log("Lendo competitions.json...")
    with open(_DATA / "competitions.json", encoding="utf-8") as f:
        raw = json.load(f)
    df = pd.DataFrame(raw)
    df = df[
        [
            "competition_id",
            "season_id",
            "competition_name",
            "season_name",
            "country_name",
            "competition_gender",
        ]
    ].copy()
    df["rotulo"] = (
        df["competition_name"] + " — " + df["season_name"] + " (" + df["country_name"] + ")"
    )
    return df.sort_values(["competition_name", "season_name"]).reset_index(drop=True)


@lru_cache(maxsize=64)
def listar_jogos(competition_id: int, season_id: int) -> pd.DataFrame:
    """Retorna um DataFrame com uma linha por jogo da temporada solicitada."""
    _log(f"Lendo matches/{competition_id}/{season_id}.json...")
    path = _DATA / "matches" / str(competition_id) / f"{season_id}.json"
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    rows = []
    for m in raw:
        rows.append(
            {
                "match_id": m["match_id"],
                "data": m.get("match_date"),
                "rodada": m.get("match_week"),
                "mandante": m["home_team"]["home_team_name"],
                "visitante": m["away_team"]["away_team_name"],
                "gols_mandante": m.get("home_score"),
                "gols_visitante": m.get("away_score"),
                "estadio": (m.get("stadium") or {}).get("name"),
            }
        )
    df = pd.DataFrame(rows)
    df["rotulo"] = (
        df["data"].astype(str)
        + " — "
        + df["mandante"]
        + " "
        + df["gols_mandante"].astype("Int64").astype(str)
        + " × "
        + df["gols_visitante"].astype("Int64").astype(str)
        + " "
        + df["visitante"]
    )
    return df.sort_values("data").reset_index(drop=True)


def listar_times(competition_id: int, season_id: int) -> list[str]:
    """Lista de times únicos que aparecem como mandante ou visitante na temporada."""
    jogos = listar_jogos(competition_id, season_id)
    return sorted(set(jogos["mandante"]).union(set(jogos["visitante"])))


def jogos_do_time(competition_id: int, season_id: int, time: str) -> pd.DataFrame:
    """Subset de listar_jogos onde o time aparece (mandante ou visitante)."""
    jogos = listar_jogos(competition_id, season_id)
    return jogos[(jogos["mandante"] == time) | (jogos["visitante"] == time)].reset_index(drop=True)


def _monta_indice(pares: list[tuple[int, int]], nome_modo: str) -> pd.DataFrame:
    """Constrói o índice (time, competição, temporada, n_jogos) para os pares dados."""
    _log(f"Montando índice [{nome_modo}] — {len(pares)} (cid, sid)...")
    t0 = time.time()
    comps = listar_competicoes().set_index(["competition_id", "season_id"])
    linhas: list[dict] = []
    for cid, sid in pares:
        try:
            jogos = listar_jogos(cid, sid)
            meta = comps.loc[(cid, sid)]
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            continue
        # Conta jogos por time (mandante + visitante).
        contagem: dict[str, int] = {}
        for col in ("mandante", "visitante"):
            for t, n in jogos[col].value_counts().items():
                contagem[t] = contagem.get(t, 0) + int(n)
        for time_nome, n in contagem.items():
            linhas.append(
                {
                    "time": time_nome,
                    "competition_id": cid,
                    "season_id": sid,
                    "competicao": meta["competition_name"],
                    "temporada": meta["season_name"],
                    "pais": meta["country_name"],
                    "n_jogos": n,
                    "rotulo": meta["rotulo"],
                }
            )
    out = (
        pd.DataFrame(linhas)
        .sort_values(["time", "competicao", "temporada"])
        .reset_index(drop=True)
    )
    _log(f"Índice [{nome_modo}] montado: {len(out)} entradas em {time.time()-t0:.2f}s")
    return out


@lru_cache(maxsize=1)
def indice_time_temporada() -> pd.DataFrame:
    """Índice restrito ao CATALOGO_DEMO. Roda em milissegundos."""
    # Filtra só as combinações (cid, sid) do catálogo, e depois mantém as linhas
    # cujo `time` está explicitamente listado no catálogo (não times adversários).
    pares = sorted({(cid, sid) for _, cid, sid in CATALOGO_DEMO})
    bruto = _monta_indice(pares, "demo")
    times_alvo = {nome for nome, _, _ in CATALOGO_DEMO}
    return bruto[bruto["time"].isin(times_alvo)].reset_index(drop=True)


@lru_cache(maxsize=1)
def indice_completo_open_data() -> pd.DataFrame:
    """Índice de TODOS os pares (time, temporada) presentes no open-data local.

    Mais lento (lê todos os matches/*/*.json), mas dá acesso a ~300 times. Use com
    `@st.cache_data` no Streamlit para pagar o custo só uma vez por sessão.
    """
    comps = listar_competicoes()
    pares = [(int(r["competition_id"]), int(r["season_id"])) for _, r in comps.iterrows()]
    return _monta_indice(pares, "completo")


def listar_todos_times(idx: pd.DataFrame | None = None) -> list[str]:
    """Nomes únicos de times. Por padrão usa o catálogo curado; passe `idx` pra mudar a fonte."""
    df = idx if idx is not None else indice_time_temporada()
    return sorted(df["time"].unique())


def temporadas_do_time(time: str, idx: pd.DataFrame | None = None) -> pd.DataFrame:
    """Temporadas em que o time aparece. Fonte padrão é o catálogo curado."""
    df = idx if idx is not None else indice_time_temporada()
    return df[df["time"] == time].sort_values(["competicao", "temporada"]).reset_index(drop=True)


def times_da_mesma_temporada(
    competition_id: int, season_id: int, idx: pd.DataFrame | None = None
) -> list[str]:
    """Times que aparecem na mesma (competição, temporada). Fonte padrão é o catálogo curado."""
    df = idx if idx is not None else indice_time_temporada()
    return sorted(
        df[(df["competition_id"] == competition_id) & (df["season_id"] == season_id)]["time"].tolist()
    )


def carregar_eventos(match_ids: Iterable[int]) -> pd.DataFrame:
    """Concatena os eventos dos match_ids passados (uma linha por evento, colunas planas)."""
    ids = list(match_ids)
    if not ids:
        return pd.DataFrame()
    _log(f"Carregando eventos de {len(ids)} jogo(s): {ids}")
    t0 = time.time()
    frames = []
    for i, m in enumerate(ids, start=1):
        ti = time.time()
        df = load_events(int(m))
        _log(f"  [{i}/{len(ids)}] match_id={m} → {len(df)} eventos ({time.time()-ti:.2f}s)")
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    _log(f"Total: {len(out)} eventos em {time.time()-t0:.2f}s")
    return out
