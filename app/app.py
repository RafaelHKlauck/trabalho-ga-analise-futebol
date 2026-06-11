"""Interface Streamlit do DNA tático — pitch demo do Grau B.

Rodar com:
    streamlit run app/app.py

Fluxo:
1. Usuário escolhe o NOME do time.
2. O sistema lista as temporadas em que esse time aparece.
3. Usuário escolhe temporada + número de jogos + (opcional) time de referência.
4. Clica em "Gerar diagnóstico" → sistema carrega eventos, calcula DNA e gera frases.
5. Figuras são lazy (botão à parte) para não travar a primeira renderização.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import streamlit as st


def _log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] [app] {msg}", flush=True)

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
if str(_ROOT / "analise") not in sys.path:
    sys.path.insert(0, str(_ROOT / "analise"))

from lib_analise import build_dna_table  # noqa: E402

from app.data_loader import (  # noqa: E402
    carregar_eventos,
    indice_completo_open_data,
    indice_time_temporada,
    jogos_do_time,
    listar_todos_times,
    temporadas_do_time,
    times_da_mesma_temporada,
)
from app.scout import comparar, diagnosticar  # noqa: E402
from app.visualizacoes import (  # noqa: E402
    fig_barras_dna,
    fig_heatmap_toques,
    fig_passes_progressivos,
    fig_recuperacoes,
    fig_rede_passes,
)

st.set_page_config(
    page_title="DNA Tático — Análise de Adversário",
    page_icon="⚽",
    layout="wide",
)


# --- Cache layer -------------------------------------------------------------


@st.cache_data(show_spinner=False)
def _indice_demo_cached():
    return indice_time_temporada()


@st.cache_data(show_spinner="Varrendo todos os jogos do open-data (uma vez por sessão)...")
def _indice_completo_cached():
    return indice_completo_open_data()


@st.cache_data(show_spinner=False)
def _jogos_time_cached(competition_id: int, season_id: int, time: str):
    return jogos_do_time(competition_id, season_id, time)


@st.cache_data(show_spinner="Carregando eventos dos jogos selecionados...")
def _eventos_cached(match_ids: tuple[int, ...]):
    return carregar_eventos(list(match_ids))


# --- Header ------------------------------------------------------------------

st.title("⚽ DNA Tático — Análise de Adversário")
st.caption(
    "Diagnóstico tático automático em linguagem natural. "
    "Escolha o time, depois a temporada, e o sistema gera frases tipo "
    "*“joga mais pela direita”* ou *“constrói pela posse”* a partir dos eventos StatsBomb."
)

# --- Sidebar: fonte de dados ------------------------------------------------

st.sidebar.header("0. Fonte de dados")
modo_completo = st.sidebar.toggle(
    "🌐 Mostrar todos os times do open-data",
    value=False,
    help=(
        "Por padrão, mostramos um catálogo curado de 7 times conhecidos para a demo. "
        "Ative para varrer ~300 times de todas as competições disponíveis localmente."
    ),
)

if modo_completo:
    idx_ativo = _indice_completo_cached()
    st.sidebar.caption(
        f"📊 Modo completo: **{idx_ativo['time'].nunique()} times** em "
        f"**{idx_ativo[['competition_id','season_id']].drop_duplicates().shape[0]} temporadas**."
    )
else:
    idx_ativo = _indice_demo_cached()
    st.sidebar.caption(f"⚡ Catálogo curado: **{idx_ativo['time'].nunique()} times**.")

# --- Sidebar: fluxo time → temporada → jogos --------------------------------

st.sidebar.header("1. Time-alvo")
todos_times = listar_todos_times(idx_ativo)
default_idx = todos_times.index("Barcelona") if "Barcelona" in todos_times else 0
time_alvo = st.sidebar.selectbox(
    "Time que você quer estudar",
    todos_times,
    index=default_idx,
    help="Digite no campo para filtrar." if modo_completo else None,
)

temporadas = temporadas_do_time(time_alvo, idx_ativo)
if temporadas.empty:
    st.sidebar.warning("Sem temporadas no open-data para esse time.")
    st.stop()

st.sidebar.header("2. Temporada")
opcoes_temp = [
    f"{r['competicao']} — {r['temporada']} ({r['n_jogos']} jogos)"
    for _, r in temporadas.iterrows()
]
idx_temp = st.sidebar.selectbox(
    "Em qual competição/temporada?",
    range(len(opcoes_temp)),
    format_func=lambda i: opcoes_temp[i],
)
linha_temp = temporadas.iloc[idx_temp]
competition_id = int(linha_temp["competition_id"])
season_id = int(linha_temp["season_id"])
n_jogos_disponiveis = int(linha_temp["n_jogos"])

st.sidebar.header("3. Amostra")
if n_jogos_disponiveis <= 1:
    limite = n_jogos_disponiveis  # 1 jogo só — sem slider.
    st.sidebar.caption(
        f"Apenas **{n_jogos_disponiveis} jogo** disponível nessa temporada — "
        "amostra muito pequena, leitura puramente indicativa."
    )
else:
    limite = st.sidebar.slider(
        "Quantos jogos do time-alvo usar?",
        min_value=1,
        max_value=n_jogos_disponiveis,
        value=min(n_jogos_disponiveis, 3),
        help="Mais jogos = leitura mais robusta, porém carregamento mais lento.",
    )

st.sidebar.header("4. Comparação (opcional)")
times_mesma_temp = times_da_mesma_temporada(competition_id, season_id, idx_ativo)
ref_opcoes = ["(sem comparação)"] + [t for t in times_mesma_temp if t != time_alvo]
time_ref = st.sidebar.selectbox("Time de referência (mesma temporada)", ref_opcoes, index=0)
usar_ref = time_ref != "(sem comparação)"

gerar = st.sidebar.button("🚀 Gerar diagnóstico", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Tudo roda em cima dos JSONs locais do **StatsBomb Open Data**. "
    "Nada vai pra internet."
)

# --- Estado de sessão -------------------------------------------------------

if "diagnostico_pronto" not in st.session_state:
    st.session_state["diagnostico_pronto"] = False
if "figuras_geradas" not in st.session_state:
    st.session_state["figuras_geradas"] = False

if gerar:
    _log(
        f"Usuário clicou 'Gerar diagnóstico' — time={time_alvo}, "
        f"temporada={linha_temp['competicao']} {linha_temp['temporada']}, "
        f"jogos={limite}, ref={time_ref if usar_ref else '—'}"
    )
    st.session_state["diagnostico_pronto"] = True
    st.session_state["figuras_geradas"] = False
    st.session_state["match_ids_alvo"] = (
        _jogos_time_cached(competition_id, season_id, time_alvo)
        .sort_values("data")
        .tail(limite)["match_id"]
        .tolist()
    )
    if usar_ref:
        st.session_state["match_ids_ref"] = (
            _jogos_time_cached(competition_id, season_id, time_ref)
            .sort_values("data")
            .tail(limite)["match_id"]
            .tolist()
        )
    else:
        st.session_state["match_ids_ref"] = []

if not st.session_state["diagnostico_pronto"]:
    st.info(
        "👈 Escolha time, temporada e clique em **Gerar diagnóstico** na barra lateral."
    )
    st.stop()

# --- Carregamento e DNA -----------------------------------------------------

match_ids_alvo = st.session_state["match_ids_alvo"]
match_ids_ref = st.session_state["match_ids_ref"]
todos_match_ids = sorted(set(match_ids_alvo) | set(match_ids_ref))

try:
    eventos = _eventos_cached(tuple(todos_match_ids))
except FileNotFoundError as e:
    st.error(
        f"Algum jogo selecionado não tem arquivo de eventos no open-data local: {e}. "
        "Reduza o número de jogos ou escolha outra temporada."
    )
    st.stop()

if eventos.empty:
    st.warning("Nenhum evento carregado.")
    st.stop()

dna = build_dna_table(eventos)

# --- Diagnóstico textual ----------------------------------------------------

st.subheader(f"📋 Diagnóstico — {time_alvo}")
st.caption(
    f"Competição: **{linha_temp['competicao']} {linha_temp['temporada']}** · "
    f"amostra: **{len(match_ids_alvo)} jogo(s)** do time-alvo"
    + (f" + {len(match_ids_ref)} do {time_ref}." if usar_ref else ".")
)

col_a, col_b = (st.columns(2) if usar_ref else (st.container(), None))

with col_a:
    if time_alvo in dna.index:
        diag_alvo = diagnosticar(dna, time_alvo, len(match_ids_alvo))
        st.markdown(diag_alvo.como_markdown())
    else:
        st.warning(f"Não foi possível calcular o DNA do {time_alvo} (eventos insuficientes).")

if usar_ref:
    with col_b:
        if time_ref in dna.index:
            diag_ref = diagnosticar(dna, time_ref, len(match_ids_ref))
            st.markdown(diag_ref.como_markdown())
        else:
            st.warning(f"Sem eventos suficientes do {time_ref}.")

    if time_alvo in dna.index and time_ref in dna.index:
        st.markdown("---")
        st.markdown("**Comparação direta:**")
        st.info(comparar(dna, time_alvo, time_ref, len(match_ids_alvo)))

# --- Tabela DNA --------------------------------------------------------------

st.subheader("🔢 Tabela DNA (números crus)")
st.dataframe(dna.round(3), use_container_width=True)

# --- Figuras (lazy) ---------------------------------------------------------

st.subheader("📊 Visualizações")

if not st.session_state["figuras_geradas"]:
    if st.button("📈 Gerar figuras (pode levar alguns segundos)"):
        _log("Usuário clicou 'Gerar figuras' — iniciando renderização.")
        st.session_state["figuras_geradas"] = True
        st.rerun()
else:
    times_no_grafico = [t for t in [time_alvo, time_ref if usar_ref else None] if t and t in dna.index]
    cores = {time_alvo: "#A50044"}
    if usar_ref:
        cores[time_ref] = "#004D98"

    with st.expander("Barras comparativas do DNA", expanded=True):
        st.pyplot(fig_barras_dna(dna, times_no_grafico, cores=cores), clear_figure=True)

    with st.expander("Heatmap de toques", expanded=False):
        with st.spinner("Calculando heatmap..."):
            st.pyplot(fig_heatmap_toques(eventos, times_no_grafico), clear_figure=True)

    with st.expander("Recuperação / pressão (altura média)", expanded=False):
        st.pyplot(fig_recuperacoes(eventos, times_no_grafico), clear_figure=True)

    with st.expander("Passes progressivos (Δx ≥ 10 m)", expanded=False):
        st.pyplot(fig_passes_progressivos(eventos, times_no_grafico), clear_figure=True)

    with st.expander("Rede de passes (por jogo)", expanded=False):
        for mid in match_ids_alvo[:3]:
            st.markdown(f"**Jogo `{mid}`**")
            sub = eventos[eventos["match_id"] == mid]
            st.pyplot(fig_rede_passes(sub, time_alvo), clear_figure=True)

# --- Footer ------------------------------------------------------------------

st.markdown("---")
st.caption(
    "Fonte de dados: **StatsBomb Open Data**. Diagnóstico gerado por regras determinísticas "
    "(`app/regras.py`). Limitações: anotação humana de eventos, sem tracking contínuo, "
    "amostras pequenas = leitura indicativa."
)
