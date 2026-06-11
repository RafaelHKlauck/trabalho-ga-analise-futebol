"""Catálogo de regras de interpretação automática do DNA tático.

Cada regra é um (predicado, tag, gerador-de-frase). O predicado recebe uma linha
do DataFrame DNA (uma Series) e um dicionário de contexto (n_jogos etc.) e
retorna bool. O gerador devolve a frase final em PT-BR, podendo formatar
valores da linha.

Mantemos limiares como constantes nomeadas para facilitar calibração — eventualmente
viram média da liga (roadmap).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd

# --- Limiares (calibrados na amostra Barça × Real 2015/16) -------------------

LIMIAR_CONSTRUCAO_ELABORADA = 6.0   # passes por posse
LIMIAR_JOGO_DIRETO = 4.0            # passes por posse
LIMIAR_POSSES_LONGAS = 0.45         # fração de posses com >=5 passes
LIMIAR_POSSE_DEMORADA_MIN = 0.35    # duração média da posse (min)

LIMIAR_VERTICAL = 0.25              # % de passes progressivos
LIMIAR_CIRCULACAO = 0.18            # idem (limite inferior)
LIMIAR_TRANSICAO_AVANCO_M = 3.5     # avanço médio em metros

LIMIAR_CORREDOR_DOMINANTE = 0.53    # fração de eventos no terço de ataque por lado
LIMIAR_BILATERAL = 0.06             # |pct_dir − pct_esq| < isso → bilateral

LIMIAR_DEPENDE_CRUZAMENTO = 0.25
LIMIAR_INFILTRACAO = 0.10

LIMIAR_BLOCO_ALTO = 55.0            # x médio de recuperação (campo 0..120)
LIMIAR_BLOCO_BAIXO = 45.0
LIMIAR_PRESSAO_INTENSA_POR_JOGO = 150  # contagem de Pressure por jogo

LIMIAR_AMEACA_CONSISTENTE_XG = 1.5  # xG por jogo
LIMIAR_FINALIZACAO_EFICIENTE = 0.10  # gols / chutes

# --- Estrutura de uma regra ---------------------------------------------------


@dataclass(frozen=True)
class Regra:
    tag: str
    grupo: str           # construcao | progressao | lateralizacao | area | bloco | ameaca
    peso: int            # ordenação no resumo (1 = mais relevante)
    aplica: Callable[[pd.Series, dict], bool]
    frase: Callable[[pd.Series, dict], str]


# --- Catálogo ----------------------------------------------------------------

REGRAS: list[Regra] = [
    # ---- Construção / posse (M1) --------------------------------------------
    Regra(
        tag="construcao_elaborada",
        grupo="construcao",
        peso=1,
        aplica=lambda r, ctx: r["media_passes_por_posse"] >= LIMIAR_CONSTRUCAO_ELABORADA,
        frase=lambda r, ctx: (
            f"Constrói pela posse — {r['media_passes_por_posse']:.1f} passes por posse em média."
        ),
    ),
    Regra(
        tag="jogo_direto",
        grupo="construcao",
        peso=1,
        aplica=lambda r, ctx: r["media_passes_por_posse"] < LIMIAR_JOGO_DIRETO,
        frase=lambda r, ctx: (
            f"Jogo direto — troca de posse frequente "
            f"({r['media_passes_por_posse']:.1f} passes por posse)."
        ),
    ),
    Regra(
        tag="muitas_posses_longas",
        grupo="construcao",
        peso=3,
        aplica=lambda r, ctx: r["posses_longas_5plus"] >= LIMIAR_POSSES_LONGAS,
        frase=lambda r, ctx: (
            f"{r['posses_longas_5plus']*100:.0f}% das posses passam de 5 passes."
        ),
    ),
    Regra(
        tag="posse_demorada",
        grupo="construcao",
        peso=3,
        aplica=lambda r, ctx: r["duracao_media_min_posse"] > LIMIAR_POSSE_DEMORADA_MIN,
        frase=lambda r, ctx: "Posse demorada — tende a controlar o ritmo de jogo.",
    ),
    # ---- Progressão (M2) ----------------------------------------------------
    Regra(
        tag="vertical",
        grupo="progressao",
        peso=2,
        aplica=lambda r, ctx: r["pct_progressivos"] > LIMIAR_VERTICAL,
        frase=lambda r, ctx: (
            f"Ataque vertical — {r['pct_progressivos']*100:.0f}% dos passes ganham 10 m ou mais."
        ),
    ),
    Regra(
        tag="circulacao",
        grupo="progressao",
        peso=2,
        aplica=lambda r, ctx: r["pct_progressivos"] < LIMIAR_CIRCULACAO,
        frase=lambda r, ctx: (
            f"Circula muito sem verticalizar — só {r['pct_progressivos']*100:.0f}% "
            "de passes progressivos."
        ),
    ),
    Regra(
        tag="transicao_rapida",
        grupo="progressao",
        peso=4,
        aplica=lambda r, ctx: r["avanco_medio_m"] > LIMIAR_TRANSICAO_AVANCO_M,
        frase=lambda r, ctx: (
            f"Avanço médio alto ({r['avanco_medio_m']:.1f} m por passe) — favorece transição."
        ),
    ),
    # ---- Lateralização (M3) -------------------------------------------------
    Regra(
        tag="corredor_direito",
        grupo="lateralizacao",
        peso=1,
        aplica=lambda r, ctx: r["pct_dir"] >= LIMIAR_CORREDOR_DOMINANTE,
        frase=lambda r, ctx: (
            f"Joga mais pela direita — {r['pct_dir']*100:.0f}% do ataque pelo corredor direito."
        ),
    ),
    Regra(
        tag="corredor_esquerdo",
        grupo="lateralizacao",
        peso=1,
        aplica=lambda r, ctx: r["pct_esq"] >= LIMIAR_CORREDOR_DOMINANTE,
        frase=lambda r, ctx: (
            f"Joga mais pela esquerda — {r['pct_esq']*100:.0f}% do ataque pelo corredor esquerdo."
        ),
    ),
    Regra(
        tag="bilateral",
        grupo="lateralizacao",
        peso=4,
        # Só dispara se nenhum corredor dominar (estritamente menor que o limiar de empate).
        aplica=lambda r, ctx: (
            abs(r["pct_dir"] - r["pct_esq"]) < LIMIAR_BILATERAL
            and r["pct_dir"] < LIMIAR_CORREDOR_DOMINANTE
            and r["pct_esq"] < LIMIAR_CORREDOR_DOMINANTE
        ),
        frase=lambda r, ctx: "Ataca pelos dois corredores de forma equilibrada.",
    ),
    # ---- Entrada na área (M4) -----------------------------------------------
    Regra(
        tag="depende_de_cruzamento",
        grupo="area",
        peso=2,
        aplica=lambda r, ctx: r["pct_cruzamentos"] > LIMIAR_DEPENDE_CRUZAMENTO,
        frase=lambda r, ctx: (
            f"Depende de cruzamentos — {r['pct_cruzamentos']*100:.0f}% "
            "dos passes para a área são cruzamentos."
        ),
    ),
    Regra(
        tag="infiltra_pelo_meio",
        grupo="area",
        peso=2,
        aplica=lambda r, ctx: r["pct_cruzamentos"] < LIMIAR_INFILTRACAO,
        frase=lambda r, ctx: (
            f"Ataca por dentro — só {r['pct_cruzamentos']*100:.0f}% de cruzamentos na área."
        ),
    ),
    # ---- Bloco / pressão (M5) -----------------------------------------------
    Regra(
        tag="bloco_alto",
        grupo="bloco",
        peso=2,
        aplica=lambda r, ctx: r["x_medio_recuperacao"] > LIMIAR_BLOCO_ALTO,
        frase=lambda r, ctx: (
            f"Bloco alto — recupera bola a {r['x_medio_recuperacao']:.0f} m da própria meta."
        ),
    ),
    Regra(
        tag="bloco_baixo",
        grupo="bloco",
        peso=2,
        aplica=lambda r, ctx: r["x_medio_recuperacao"] < LIMIAR_BLOCO_BAIXO,
        frase=lambda r, ctx: (
            f"Bloco baixo — recuperação média a {r['x_medio_recuperacao']:.0f} m no próprio campo."
        ),
    ),
    Regra(
        tag="pressao_intensa",
        grupo="bloco",
        peso=3,
        aplica=lambda r, ctx: (
            ctx.get("n_jogos", 1)
            and (r["pressure_count"] / max(ctx["n_jogos"], 1)) > LIMIAR_PRESSAO_INTENSA_POR_JOGO
        ),
        frase=lambda r, ctx: (
            f"Alta intensidade de pressão — {r['pressure_count']/max(ctx['n_jogos'],1):.0f} "
            "ações de pressão por jogo."
        ),
    ),
    # ---- Ameaça (M6) --------------------------------------------------------
    Regra(
        tag="geracao_consistente",
        grupo="ameaca",
        peso=1,
        aplica=lambda r, ctx: r["xg_por_jogo"] > LIMIAR_AMEACA_CONSISTENTE_XG,
        frase=lambda r, ctx: (
            f"Gera ameaça consistente — {r['xg_por_jogo']:.2f} xG por jogo."
        ),
    ),
    Regra(
        tag="finalizacao_eficiente",
        grupo="ameaca",
        peso=3,
        aplica=lambda r, ctx: (
            ctx.get("n_jogos", 1)
            and r["chutes_por_jogo"] > 0
            and (r["gols_total"] / (r["chutes_por_jogo"] * ctx["n_jogos"]))
            >= LIMIAR_FINALIZACAO_EFICIENTE
        ),
        frase=lambda r, ctx: (
            "Eficiência ofensiva acima da média — "
            f"{r['gols_total']} gols em {int(r['chutes_por_jogo']*ctx['n_jogos'])} chutes."
        ),
    ),
]


# --- Assinaturas (combinações de tags → rótulo de estilo) --------------------

ASSINATURAS: list[tuple[set[str], str]] = [
    # Mais específicas primeiro (3 tags) — ordem importa: a primeira que casa vence.
    (
        {"construcao_elaborada", "circulacao", "bloco_alto"},
        "Estilo posicional de posse com pressão pós-perda.",
    ),
    (
        {"jogo_direto", "vertical", "bloco_baixo"},
        "Estilo de transição / contra-ataque clássico.",
    ),
    (
        {"construcao_elaborada", "infiltra_pelo_meio", "geracao_consistente"},
        "Posicional pelo meio com finalização eficiente.",
    ),
    (
        {"jogo_direto", "depende_de_cruzamento", "pressao_intensa"},
        "Pressão alta com chegada por cruzamento.",
    ),
    (
        {"vertical", "transicao_rapida", "pressao_intensa"},
        "Transição vertical com pressão de volume.",
    ),
    # Fallbacks mais soltos (2 tags) — pegam casos que não bateram com nenhuma combinação acima.
    (
        {"construcao_elaborada", "geracao_consistente"},
        "Posse com finalização eficiente.",
    ),
    (
        {"jogo_direto", "pressao_intensa"},
        "Jogo direto com pressão de volume.",
    ),
    (
        {"vertical", "transicao_rapida"},
        "Verticalidade e transição rápida.",
    ),
]


def assinatura_para(tags: set[str]) -> str | None:
    """Retorna a primeira assinatura cuja combinação está contida em `tags`, se houver."""
    for combo, rotulo in ASSINATURAS:
        if combo.issubset(tags):
            return rotulo
    return None
