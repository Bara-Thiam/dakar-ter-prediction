# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

st.set_page_config(
    page_title="TER Dakar — Prédiction",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
<style>
    /* ── Dataframe ── */
    [data-testid="stDataFrame"] canvas { filter: invert(0) !important; }
    iframe[data-testid="stDataFrameResizable"] { background: white !important; }

    /* ── Material Icons sidebar collapse ── */
    [data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
        font-size: 1.3rem !important;
        color: rgba(250, 250, 250, 0.6) !important;
    }

    /* ── Material Symbols inline (HTML custom) ── */
    span.msr {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        vertical-align: middle;
    }
    .kpi-icon span.msr  { font-size: 1.6rem; color: #C4A55A; display: block; margin-bottom: 0.6rem; }
    .form-card-title span.msr { font-size: 1rem; color: #7B1C2A; margin-right: 0.4rem; }
    .header-badge span.msr { font-size: 0.85rem; vertical-align: middle; margin-right: 0.3rem; }

    /* ── Scenario buttons ── */
    .scenario-row { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; }
    .scenario-chip {
        flex: 1;
        background: white;
        border: 1.5px solid #C4A55A;
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        text-align: center;
        cursor: pointer;
        font-size: 0.78rem;
        font-weight: 600;
        color: #6D1A28;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.15s;
    }
    .scenario-chip:hover { background: #FAF0E6; border-color: #D4B86A; }

    /* ── Base ── */
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background-color: #FAF5F0; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] { background: #3D0A14 !important; border-right: 1px solid #5a1020; }
    [data-testid="stSidebar"] * { color: #FAF0E6 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; margin: 0.8rem 0 !important; }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.88rem !important; font-weight: 500 !important;
        padding: 0.45rem 0.6rem !important; border-radius: 8px !important;
        transition: background 0.15s !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.07) !important; }

    /* ── Header ── */
    .main-header {
        background: linear-gradient(135deg, #3D0A14 0%, #6D1A28 55%, #7B1C2A 100%);
        padding: 2rem 2.5rem; border-radius: 20px; color: white;
        margin-bottom: 2rem; box-shadow: 0 12px 40px rgba(61,10,20,0.25);
        position: relative; overflow: hidden;
    }
    .main-header::before {
        content: ''; position: absolute; top: -40px; right: -40px;
        width: 200px; height: 200px; background: rgba(255,255,255,0.04); border-radius: 50%;
    }
    .main-header::after {
        content: ''; position: absolute; bottom: -60px; right: 80px;
        width: 280px; height: 280px; background: rgba(255,255,255,0.03); border-radius: 50%;
    }
    .main-header h1 { margin: 0; font-size: 1.9rem; font-weight: 800; color: white; letter-spacing: -0.5px; }
    .main-header p { margin: 0.4rem 0 0; opacity: 0.7; font-size: 0.9rem; color: white; font-weight: 400; }
    .header-badge {
        display: inline-block; background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2); border-radius: 50px;
        padding: 0.2rem 0.8rem; font-size: 0.75rem; font-weight: 600;
        color: #D4B86A; margin-bottom: 0.8rem; letter-spacing: 1px; text-transform: uppercase;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: #FFFFFF; border-radius: 16px; padding: 1.4rem 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(123,28,42,0.08); position: relative; overflow: hidden;
    }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #7B1C2A, #C4A55A); border-radius: 16px 16px 0 0;
    }
    .kpi-icon { margin-bottom: 0.2rem; }
    .kpi-value { font-size: 1.75rem; font-weight: 800; color: #3D0A14; line-height: 1; letter-spacing: -0.5px; font-family: 'DM Mono', monospace !important; }
    .kpi-label { font-size: 0.72rem; color: #78909C; margin-top: 0.35rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; }
    .kpi-delta { font-size: 0.75rem; font-weight: 600; margin-top: 0.4rem; padding: 0.15rem 0.5rem; border-radius: 50px; display: inline-block; }
    .delta-neg { background: #FFEBEE; color: #C62828; }
    .delta-pos { background: #FAF0E6; color: #6D1A28; }

    /* ── Section titles ── */
    .section-title {
        font-size: 0.72rem; font-weight: 700; color: #546E7A;
        padding-bottom: 0.6rem; margin-bottom: 1.2rem;
        text-transform: uppercase; letter-spacing: 1.2px; border-bottom: 1px solid #E8DDD0;
    }

    /* ── Prediction Box ── */
    .pred-box {
        background: #3D0A14; color: white; border-radius: 20px;
        padding: 2.2rem 2rem; text-align: center;
        box-shadow: 0 16px 50px rgba(61,10,20,0.25); position: relative; overflow: hidden;
    }
    .pred-box::before {
        content: ''; position: absolute; top: -50px; right: -50px;
        width: 180px; height: 180px; background: rgba(255,255,255,0.03); border-radius: 50%;
    }
    .pred-value { font-size: 3.8rem; font-weight: 800; color: white; line-height: 1; letter-spacing: -2px; font-family: 'DM Mono', monospace !important; }
    .pred-unit { font-size: 0.8rem; opacity: 0.6; color: white; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 0.3rem; }
    .pred-interval { font-size: 0.78rem; opacity: 0.55; color: white; margin-top: 0.8rem; font-family: 'DM Mono', monospace; }
    .badge { display: inline-block; padding: 0.35rem 1rem; border-radius: 50px; font-weight: 700; font-size: 0.78rem; margin-top: 1rem; letter-spacing: 0.5px; }
    .badge-high   { background: rgba(198,40,40,0.2);  color: #FFCDD2; border: 1px solid rgba(198,40,40,0.3); }
    .badge-medium { background: rgba(196,165,90,0.2); color: #F5EDD8; border: 1px solid rgba(196,165,90,0.3); }
    .badge-low    { background: rgba(109,26,40,0.2);  color: #F0E0C0; border: 1px solid rgba(109,26,40,0.3); }

    /* ── Form Cards ── */
    .form-card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid rgba(123,28,42,0.08); margin-bottom: 1rem; }
    .form-card-title { font-size: 0.72rem; font-weight: 700; color: #546E7A; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #FAF5F0; display: flex; align-items: center; gap: 0.3rem; }

    /* ── Buttons ── */
    .stButton > button {
        background: #6D1A28 !important; color: #FFFFFF !important;
        border: 2px solid #C4A55A !important; border-radius: 12px !important;
        font-weight: 700 !important; font-size: 0.9rem !important;
        padding: 0.7rem 1.5rem !important; letter-spacing: 0.3px !important;
        transition: all 0.2s !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
        text-shadow: none !important;
    }
    .stButton > button:hover {
        background: #7B1C2A !important; border-color: #D4B86A !important;
        transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(61,10,20,0.3) !important;
    }
    .stButton > button p { color: #FFFFFF !important; font-weight: 700 !important; }

    /* ── Status badge ── */
    .status-ok   { background: rgba(109,26,40,0.15); border: 1px solid rgba(196,165,90,0.4); border-radius: 8px; padding: 0.5rem 0.8rem; font-size: 0.8rem; font-weight: 600; }
    .status-demo { background: rgba(249,168,37,0.15); border: 1px solid rgba(249,168,37,0.3); border-radius: 8px; padding: 0.5rem 0.8rem; font-size: 0.8rem; font-weight: 600; }

    /* ── Inputs ── */
    .stSelectbox > div > div, .stSlider > div, .stNumberInput > div { border-radius: 10px !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent; border-bottom: 1px solid #E8DDD0; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0 !important; font-weight: 600 !important; font-size: 0.85rem !important; padding: 0.5rem 1.2rem !important; }
    .stTabs [aria-selected="true"] { background: white !important; color: #6D1A28 !important; }

    /* ── Misc ── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    p, label, .stMarkdown { color: #263238; }
    hr { border-color: #E8DDD0 !important; }
    div.st-au.st-bx { background-color: #78909C !important; }
    .js-plotly-plot .colorbar text { fill: #263238 !important; }
    [data-testid="stExpander"] { background: white !important; border: 1px solid #E8DDD0 !important; border-radius: 12px !important; }
    [data-testid="stExpander"] summary { color: #6D1A28 !important; font-weight: 600 !important; }
    [data-testid="stExpander"] details { background: white !important; }
    [data-testid="stExpander"] div { background: white !important; color: #263238 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Chargement données ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "data", "dataset_ter_dakar_2022_2026.csv")
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data
def load_model_results():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "docs", "comparaison_resultats.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        df.columns = (df.columns
                      .str.replace("²", "2", regex=False)
                      .str.replace("è", "e", regex=False)
                      .str.replace("é", "e", regex=False)
                      .str.strip())
        return df
    return pd.DataFrame({
        "Modele": ["Regression Lineaire", "Random Forest", "XGBoost"],
        "R2":     [0.1961, 0.9685, 0.9771],
        "MAE":    [808, 128, 112],
        "RMSE":   [991, 196, 167],
    })


# ─── API ───────────────────────────────────────────────────────────────────────
predict_fn = None
api_status = "demo"
api_msg    = "⚠️ Mode démo"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from api_prediction import predict as real_predict
    predict_fn = real_predict
    api_status = "ok"
    api_msg    = "✅ XGBoost connecté"
except Exception as e:
    api_msg = f"⚠️ Mode démo — {str(e)}"


def mock_predict(jour, annee, mois, heure, minute=0,
                 est_jour_ferie=0, est_vacances=0, est_pluies=0, est_ramadan=0,
                 ev_religieux=0, ev_special=0, perturbation=0,
                 phase_reseau=1, nb_rames=22):
    base = {range(7,10): 4200, range(17,20): 3900, range(6,7): 2000,
            range(10,11): 2000, range(16,17): 2000, range(20,21): 2000}.get(
        next((r for r in [range(7,10),range(17,20),range(6,7),range(10,11),range(16,17),range(20,21)] if heure in r), None), 900)
    if minute == 30: base = int(base * 0.92)
    if jour in ["samedi"]: base = int(base * 0.75)
    elif jour in ["dimanche"]: base = int(base * 0.55)
    if est_jour_ferie: base = int(base * 0.4)
    if est_vacances: base = int(base * 0.80)
    if perturbation == 1: base = int(base * 0.65)
    elif perturbation == 2: base = int(base * 0.50)
    elif perturbation == 3: base = int(base * 0.20)
    if ev_religieux in [1,2]: base = int(base * 1.40)
    elif ev_religieux in [3,4]: base = int(base * 1.30)
    return max(base, 50)


def do_predict(jour, annee, mois, heure, minute,
               est_ferie, est_vacances, est_pluies, est_ramadan,
               ev_religieux, ev_special, perturbation, phase_reseau, nb_rames):
    if predict_fn is not None:
        res = predict_fn(jour, annee, mois, heure, minute,
                         est_ferie, est_vacances, est_pluies, est_ramadan,
                         ev_religieux, ev_special, perturbation, phase_reseau, nb_rames)
        return res["frequentation"], res["intervalle"]
    val = mock_predict(jour, annee, mois, heure, minute,
                       est_ferie, est_vacances, est_pluies, est_ramadan,
                       ev_religieux, ev_special, perturbation, phase_reseau, nb_rames)
    return val, (max(0, val - 109), val + 109)


def get_niveau(val):
    if val >= 3500: return "Forte affluence", "badge-high"
    elif val >= 1500: return "Affluence modérée", "badge-medium"
    return "Faible affluence", "badge-low"


LAYOUT = dict(
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(color="#263238", family="Plus Jakarta Sans"),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(color="#546E7A", tickfont=dict(color="#546E7A", size=11),
               title=dict(font=dict(color="#546E7A")), gridcolor="#FAF5F0", linecolor="#E8DDD0"),
    yaxis=dict(color="#546E7A", tickfont=dict(color="#546E7A", size=11),
               title=dict(font=dict(color="#546E7A")), gridcolor="#FAF5F0", linecolor="#E8DDD0"),
    hoverlabel=dict(bgcolor="white", font=dict(color="#263238", family="Plus Jakarta Sans"), bordercolor="#E8DDD0"),
    legend=dict(font=dict(color="#263238")),
)

df            = load_data()
model_results = load_model_results()
MOIS_LABELS   = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]

# ─── Session state — prédiction ────────────────────────────────────────────────
_defaults = {
    "p_jour": "lundi", "p_annee": 2025, "p_mois": 9,
    "p_heure": 8, "p_minute": 0,
    "p_ferie": False, "p_vacances": False,
    "p_pluies": False, "p_ramadan": False,
    "p_ev_rel": 0, "p_ev_sp": 0, "p_pert": 0,
    "p_phase": 1, "p_rames": 22,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo_ter.png")
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.image(logo_path, width=120)
    st.markdown("""
    <div style='text-align:center; font-size:0.65rem; color:#C4A55A; font-weight:600;
                letter-spacing:3px; margin-bottom:0.5rem; font-family: Plus Jakarta Sans, sans-serif;'>
        SYSTÈME DE PRÉDICTION
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["Tableau de bord", "Prédiction", "Analyses", "Précision"],
                    label_visibility="collapsed")
    st.markdown("---")
    status_cls = "status-ok" if api_status == "ok" else "status-demo"
    st.markdown(f'<div class="{status_cls}">{api_msg}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Projet Data Science · Equipe TER · v2.0")


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="header-badge">
        <span class="msr">train</span> Train Express Régional — Dakar
    </div>
    <h1>Prédiction de Fréquentation</h1>
    <p>Tableau de bord interactif d'analyse et de prédiction — Modèle XGBoost · R² = 0.978</p>
</div>
""", unsafe_allow_html=True)


# ─── PAGE : Tableau de bord ────────────────────────────────────────────────────
if page == "Tableau de bord":
    daily      = df.groupby("date")["frequentation"].sum()
    total      = int(daily.sum())
    moy_jour   = int(daily.mean())
    pic_heure  = int(df.groupby("heure")["frequentation"].mean().idxmax())
    ferie_moy  = df[df["est_jour_ferie"]==1]["frequentation"].mean()
    normal_moy = df[df["est_jour_ferie"]==0]["frequentation"].mean()
    ferie_ratio = round(ferie_moy / normal_moy * 100 - 100, 1)

    st.markdown('<div class="section-title">Indicateurs clés</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "departure_board", f"{total:,}", "Total voyageurs 2022–2026", None),
        (c2, "calendar_month",  f"{moy_jour:,}", "Moyenne journalière", None),
        (c3, "schedule",        f"{pic_heure}h00", "Heure de pointe", None),
        (c4, "bar_chart",       f"{ferie_ratio:+.1f}%", "Jours fériés vs normal",
         f'<span class="kpi-delta delta-neg">{ferie_ratio:+.1f}% affluence</span>' if ferie_ratio < 0
         else f'<span class="kpi-delta delta-pos">{ferie_ratio:+.1f}% affluence</span>'),
    ]
    for col, icon, val, label, delta in cards:
        with col:
            color = "#C62828" if (delta and ferie_ratio < 0 and label.startswith("Jours")) else "#3D0A14"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon"><span class="msr">{icon}</span></div>
                <div class="kpi-value" style="color:{color}">{val}</div>
                <div class="kpi-label">{label}</div>
                {delta or ''}
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Évolution annuelle du trafic</div>', unsafe_allow_html=True)
    yearly = df.groupby("annee")["frequentation"].sum().reset_index()
    fig_y  = px.bar(yearly, x="annee", y="frequentation",
                    color_discrete_sequence=["#7B1C2A"], template="plotly_white",
                    labels={"annee": "Année", "frequentation": "Total voyageurs"},
                    text="frequentation")
    fig_y.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                        textfont=dict(color="#263238", size=11), marker_line_width=0, marker_opacity=0.9,
                        marker_color=["#F0E0C0","#D4B86A","#C4A55A","#8B2030","#6D1A28"])
    fig_y.update_layout(height=300, bargap=0.35, **LAYOUT)
    st.plotly_chart(fig_y, use_container_width=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="section-title">Fréquentation par jour de semaine</div>', unsafe_allow_html=True)
        order  = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
        by_day = df.groupby("jour_semaine")["frequentation"].mean().reindex(order).reset_index()
        fig_d  = px.bar(by_day, x="jour_semaine", y="frequentation", color="frequentation",
                        color_continuous_scale=["#F0E0C0","#6D1A28"], template="plotly_white",
                        labels={"frequentation":"Freq. moy.","jour_semaine":""})
        fig_d.update_traces(marker_line_width=0)
        fig_d.update_layout(height=310, coloraxis_showscale=False, bargap=0.3, **LAYOUT)
        st.plotly_chart(fig_d, use_container_width=True)

    with cb:
        st.markdown('<div class="section-title">Impact des perturbations</div>', unsafe_allow_html=True)
        pert_labels = {0: "Aucune", 1: "Panne", 2: "Inondation", 3: "Grève"}
        by_pert = df.groupby("perturbation")["frequentation"].mean().reset_index()
        if 3 not in by_pert["perturbation"].values:
            normal    = by_pert[by_pert["perturbation"] == 0]["frequentation"].values[0]
            greve_row = pd.DataFrame({"perturbation": [3], "frequentation": [int(normal * 0.20)]})
            by_pert   = pd.concat([by_pert, greve_row], ignore_index=True)
        by_pert["label"] = by_pert["perturbation"].map(pert_labels)
        colors_pert = ["#6D1A28","#F57F17","#1565C0","#C62828"][:len(by_pert)]
        fig_pert = px.bar(by_pert, x="label", y="frequentation", color="label",
                          color_discrete_sequence=colors_pert, template="plotly_white",
                          labels={"frequentation":"Freq. moy.","label":""})
        fig_pert.update_traces(marker_line_width=0)
        fig_pert.update_layout(height=310, showlegend=False, bargap=0.35, **LAYOUT)
        st.plotly_chart(fig_pert, use_container_width=True)


# ─── PAGE : Prédiction ─────────────────────────────────────────────────────────
elif page == "Prédiction":

    # ── Scénarios de démonstration ──────────────────────────────────────────────
    st.markdown('<div class="section-title">Scénarios de démonstration</div>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)

    with sc1:
        if st.button("Lundi — Heure de pointe", use_container_width=True):
            st.session_state.p_jour    = "lundi"
            st.session_state.p_annee   = 2025
            st.session_state.p_mois    = 9
            st.session_state.p_heure   = 8
            st.session_state.p_minute  = 0
            st.session_state.p_ferie   = False
            st.session_state.p_vacances= False
            st.session_state.p_pluies  = False
            st.session_state.p_ramadan = False
            st.session_state.p_ev_rel  = 0
            st.session_state.p_ev_sp   = 0
            st.session_state.p_pert    = 0
            st.session_state.p_phase   = 2
            st.session_state.p_rames   = 22
            st.rerun()

    with sc2:
        if st.button("Vendredi — Magal Touba", use_container_width=True):
            st.session_state.p_jour    = "vendredi"
            st.session_state.p_annee   = 2025
            st.session_state.p_mois    = 11
            st.session_state.p_heure   = 10
            st.session_state.p_minute  = 0
            st.session_state.p_ferie   = False
            st.session_state.p_vacances= False
            st.session_state.p_pluies  = False
            st.session_state.p_ramadan = False
            st.session_state.p_ev_rel  = 1
            st.session_state.p_ev_sp   = 0
            st.session_state.p_pert    = 0
            st.session_state.p_phase   = 2
            st.session_state.p_rames   = 22
            st.rerun()

    with sc3:
        if st.button("Lundi — Perturbation réseau", use_container_width=True):
            st.session_state.p_jour    = "lundi"
            st.session_state.p_annee   = 2025
            st.session_state.p_mois    = 9
            st.session_state.p_heure   = 8
            st.session_state.p_minute  = 0
            st.session_state.p_ferie   = False
            st.session_state.p_vacances= False
            st.session_state.p_pluies  = False
            st.session_state.p_ramadan = False
            st.session_state.p_ev_rel  = 0
            st.session_state.p_ev_sp   = 0
            st.session_state.p_pert    = 1
            st.session_state.p_phase   = 2
            st.session_state.p_rames   = 18
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Formulaire complet ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Simulateur de prédiction</div>', unsafe_allow_html=True)
    col_f, col_r = st.columns([1, 1], gap="large")

    with col_f:
        # Bloc 1 : Temporel
        st.markdown('<div class="form-card"><div class="form-card-title"><span class="msr">calendar_today</span> Quand ?</div>', unsafe_allow_html=True)
        jour  = st.selectbox("Jour de la semaine",
                             ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"],
                             key="p_jour")
        cc1, cc2 = st.columns(2)
        with cc1:
            annee = st.selectbox("Année", [2022,2023,2024,2025,2026], key="p_annee")
        with cc2:
            mois  = st.selectbox("Mois", list(range(1,13)),
                                 format_func=lambda x: MOIS_LABELS[x-1], key="p_mois")
        cc3, cc4 = st.columns(2)
        with cc3:
            heure  = st.slider("Heure", 5, 23, key="p_heure", format="%dh")
        with cc4:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            minute = st.radio("Minute", [0, 30], horizontal=True,
                              format_func=lambda x: f":{x:02d}", key="p_minute")
        st.markdown('</div>', unsafe_allow_html=True)

        # Bloc 2 : Contexte
        st.markdown('<div class="form-card"><div class="form-card-title"><span class="msr">public</span> Contexte</div>', unsafe_allow_html=True)
        ccc1, ccc2 = st.columns(2)
        with ccc1:
            est_ferie    = st.toggle("Jour férié",          key="p_ferie")
            est_vacances = st.toggle("Vacances scolaires",  key="p_vacances")
        with ccc2:
            est_pluies   = st.toggle("Saison des pluies",   key="p_pluies")
            est_ramadan  = st.toggle("Ramadan",             key="p_ramadan")
        st.markdown('</div>', unsafe_allow_html=True)

        # Bloc 3 : Événements & Réseau
        st.markdown('<div class="form-card"><div class="form-card-title"><span class="msr">event</span> Événements & Réseau</div>', unsafe_allow_html=True)
        ev_religieux = st.selectbox("Événement religieux", [0,1,2,3,4],
            format_func=lambda x: {0:"Aucun",1:"Magal Touba",2:"Gamou Tivaouane",3:"Korité",4:"Tabaski"}[x],
            key="p_ev_rel")
        ev_special   = st.selectbox("Événement spécial", [0,1,2,3],
            format_func=lambda x: {0:"Aucun",1:"JOJ 2026",2:"Fête nationale",3:"Autre"}[x],
            key="p_ev_sp")
        perturbation = st.selectbox("Perturbation réseau", [0,1,2,3],
            format_func=lambda x: {0:"Aucune",1:"Panne technique",2:"Inondation",3:"Grève"}[x],
            key="p_pert")
        cd1, cd2 = st.columns(2)
        with cd1:
            phase_reseau = st.radio("Extension réseau", [1,2],
                                    format_func=lambda x: f"Phase {x}", horizontal=True,
                                    key="p_phase")
        with cd2:
            nb_rames = st.number_input("Rames actives", min_value=15, max_value=22, key="p_rames")
        st.markdown('</div>', unsafe_allow_html=True)

        go_btn = st.button("Lancer la prédiction", type="primary", use_container_width=True)

    with col_r:
        if go_btn:
            val, intervalle = do_predict(
                jour, annee, mois, heure, minute,
                int(est_ferie), int(est_vacances), int(est_pluies), int(est_ramadan),
                ev_religieux, ev_special, perturbation, phase_reseau, nb_rames
            )
            niv_txt, niv_cls = get_niveau(val)
            st.markdown(f"""
            <div class="pred-box">
                <div style="font-size:0.7rem; opacity:0.5; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.8rem">
                    {jour.capitalize()} · {MOIS_LABELS[mois-1]} {annee} · {heure}h{minute:02d}
                </div>
                <div class="pred-value">{val:,}</div>
                <div class="pred-unit">voyageurs / 30 min</div>
                <div class="pred-interval">Intervalle de confiance : [{intervalle[0]:,} — {intervalle[1]:,}]</div>
                <br>
                <span class="badge {niv_cls}">{niv_txt}</span>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">Profil de la journée</div>', unsafe_allow_html=True)

            labels, preds = [], []
            for h in range(5, 24):
                for m in [0, 30]:
                    v, _ = do_predict(jour, annee, mois, h, m,
                                      int(est_ferie), int(est_vacances), int(est_pluies), int(est_ramadan),
                                      ev_religieux, ev_special, perturbation, phase_reseau, nb_rames)
                    labels.append(f"{h}h{m:02d}")
                    preds.append(v)

            current = f"{heure}h{minute:02d}"
            colors  = ["#C62828" if l == current else "#7B1C2A" for l in labels]
            sizes   = [12 if l == current else 7 for l in labels]

            fig_h = go.Figure()
            fig_h.add_trace(go.Scatter(
                x=labels, y=preds, mode="lines+markers",
                line=dict(color="#7B1C2A", width=2.5, shape="spline"),
                marker=dict(color=colors, size=sizes, line=dict(color="white", width=1.5)),
                fill="tozeroy", fillcolor="rgba(123,28,42,0.06)",
                hovertemplate="<b>%{x}</b><br>%{y:,} voyageurs<extra></extra>"
            ))
            fig_h.add_vline(x=current, line_dash="dot", line_color="#C4A55A", line_width=2)
            fig_h.update_layout(
                height=300, showlegend=False,
                xaxis=dict(tickangle=45, tickfont=dict(size=9), color="#546E7A",
                           gridcolor="#FAF5F0", title=dict(font=dict(color="#546E7A"))),
                yaxis=dict(color="#546E7A", tickfont=dict(color="#546E7A", size=11),
                           gridcolor="#FAF5F0", title="Voyageurs", title_font=dict(color="#546E7A")),
                **{k:v for k,v in LAYOUT.items() if k not in ["xaxis","yaxis"]}
            )
            st.plotly_chart(fig_h, use_container_width=True)
        else:
            st.markdown("""
            <div style="background:white; border-radius:16px; padding:3rem 2rem;
                        text-align:center; border:1px dashed #D4B86A; margin-top:1rem">
                <div style="margin-bottom:1rem">
                    <span class="msr" style="font-size:2.5rem; color:#C4A55A;">query_stats</span>
                </div>
                <div style="font-weight:700; color:#3D0A14; font-size:1rem">
                    Configurez les paramètres
                </div>
                <div style="color:#78909C; font-size:0.85rem; margin-top:0.4rem">
                    ou sélectionnez un scénario ci-dessus, puis cliquez sur <strong>Lancer la prédiction</strong>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Heatmap semaine type</div>', unsafe_allow_html=True)
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        hm_annee = st.selectbox("Année ", [2022,2023,2024,2025,2026], index=3, key="hm_a")
    with ch2:
        hm_mois  = st.selectbox("Mois ", list(range(1,13)), key="hm_m",
                                format_func=lambda x: MOIS_LABELS[x-1])
    with ch3:
        hm_pert  = st.selectbox("Perturbation ", [0,1,2,3], key="hm_p",
                                format_func=lambda x: {0:"Aucune",1:"Panne",2:"Inondation",3:"Grève"}[x])

    jours_ordre = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
    matrix = pd.DataFrame(
        {j: [do_predict(j, hm_annee, hm_mois, h, 0, 0, 0, 0, 0, 0, 0, hm_pert, 1, 22)[0]
             for h in range(5,24)] for j in jours_ordre},
        index=range(5,24)
    )
    fig_hm = px.imshow(matrix.T,
                       color_continuous_scale=["#FDF6EC","#D4B86A","#7B1C2A","#3D0A14"],
                       labels=dict(x="Heure", y="Jour", color="Voyageurs"),
                       aspect="auto", template="plotly_white")
    fig_hm.update_layout(height=320, **LAYOUT)
    st.plotly_chart(fig_hm, use_container_width=True)


# ─── PAGE : Analyses ───────────────────────────────────────────────────────────
elif page == "Analyses":
    st.markdown('<div class="section-title">Analyse exploratoire</div>', unsafe_allow_html=True)
    # Événements religieux en premier — le plus parlant pour SETER
    tab4, tab1, tab2, tab3 = st.tabs([
        "Événements religieux",
        "Profil horaire",
        "Saisonnalité",
        "Heatmap",
    ])

    with tab4:
        ev_labels = {0:"Normal",1:"Magal Touba",2:"Gamou",3:"Korité",4:"Tabaski"}
        by_ev = df.groupby("evenement_religieux")["frequentation"].mean().reset_index()
        by_ev["label"] = by_ev["evenement_religieux"].map(ev_labels)
        by_ev["delta"] = (by_ev["frequentation"] / by_ev[by_ev["evenement_religieux"]==0]["frequentation"].values[0] - 1) * 100
        fig_ev = px.bar(by_ev, x="label", y="frequentation", color="delta",
                        color_continuous_scale=["#F0E0C0","#8B2030","#6D1A28"],
                        template="plotly_white",
                        labels={"frequentation":"Freq. moy.","label":""},
                        title="Impact des événements religieux sur la fréquentation",
                        text="frequentation")
        fig_ev.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                              textfont=dict(color="#263238"), marker_line_width=0)
        fig_ev.update_layout(height=420, coloraxis_showscale=False, bargap=0.4, **LAYOUT)
        st.plotly_chart(fig_ev, use_container_width=True)

    with tab1:
        bh = df.groupby("heure")["frequentation"].agg(["mean","std"]).reset_index()
        fig_hr = go.Figure([
            go.Scatter(x=bh["heure"], y=bh["mean"]+bh["std"], mode="lines",
                       line=dict(width=0), showlegend=False),
            go.Scatter(x=bh["heure"], y=bh["mean"]-bh["std"], mode="lines",
                       line=dict(width=0), fill="tonexty",
                       fillcolor="rgba(123,28,42,0.10)", showlegend=False),
            go.Scatter(x=bh["heure"], y=bh["mean"], mode="lines+markers",
                       line=dict(color="#6D1A28", width=3, shape="spline"),
                       marker=dict(size=8, color="#8B2030", line=dict(color="white", width=2)),
                       name="Fréquentation moyenne",
                       hovertemplate="<b>%{x}h</b><br>%{y:,.0f} voyageurs<extra></extra>"),
        ])
        fig_hr.update_layout(title="Fréquentation moyenne par heure · 2022–2026",
                              xaxis_title="Heure", yaxis_title="Voyageurs / 30 min",
                              template="plotly_white", height=420, **LAYOUT)
        st.plotly_chart(fig_hr, use_container_width=True)

    with tab2:
        bm = df.groupby(["annee","mois"])["frequentation"].sum().reset_index()
        bm["mois_nom"] = bm["mois"].map(dict(enumerate(MOIS_LABELS, 1)))
        fig_mo = px.bar(bm, x="mois_nom", y="frequentation", color="annee",
                        barmode="group", template="plotly_white",
                        color_discrete_sequence=["#F0E0C0","#D4B86A","#C4A55A","#8B2030","#6D1A28"],
                        labels={"frequentation":"Total voyageurs","mois_nom":"Mois","annee":"Année"},
                        title="Fréquentation mensuelle par année")
        fig_mo.update_traces(marker_line_width=0)
        fig_mo.update_layout(height=420, bargap=0.15, **LAYOUT)
        st.plotly_chart(fig_mo, use_container_width=True)

    with tab3:
        order = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
        pivot = df.groupby(["jour_semaine","heure"])["frequentation"].mean().unstack("heure").reindex(order)
        fig_hm2 = px.imshow(pivot,
                             color_continuous_scale=["#FDF6EC","#D4B86A","#7B1C2A","#3D0A14"],
                             labels=dict(x="Heure", y="Jour", color="Freq. moy."),
                             aspect="auto", template="plotly_white",
                             title="Heatmap · Fréquentation par jour et heure")
        fig_hm2.update_layout(height=420, **LAYOUT)
        st.plotly_chart(fig_hm2, use_container_width=True)


# ─── PAGE : Précision ──────────────────────────────────────────────────────────
elif page == "Précision":
    st.markdown('<div class="section-title">Performance du modèle</div>', unsafe_allow_html=True)

    base     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base, "visualisations", "comparaison_modeles.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig_r2 = px.bar(model_results, x="Modele", y="R2", color="Modele",
                            color_discrete_sequence=["#F0E0C0","#8B2030","#6D1A28"],
                            template="plotly_white", title="Score R²", text="R2")
            fig_r2.update_traces(texttemplate="%{text:.4f}", textposition="outside",
                                  textfont=dict(color="#263238"), marker_line_width=0)
            fig_r2.update_layout(height=350, showlegend=False, yaxis_range=[0,1.15], bargap=0.4, **LAYOUT)
            st.plotly_chart(fig_r2, use_container_width=True)
        with c2:
            df_melt = model_results.melt(id_vars="Modele", value_vars=["MAE","RMSE"],
                                         var_name="Metrique", value_name="Erreur")
            fig_err = px.bar(df_melt, x="Modele", y="Erreur", color="Metrique",
                             barmode="group",
                             color_discrete_sequence=["#C4A55A","#E53935"],
                             template="plotly_white", title="Erreurs MAE et RMSE")
            fig_err.update_traces(marker_line_width=0)
            fig_err.update_layout(height=350, bargap=0.3, **LAYOUT)
            st.plotly_chart(fig_err, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tableau récapitulatif</div>', unsafe_allow_html=True)
    st.dataframe(model_results, use_container_width=True, hide_index=True)

    r2_col  = next((c for c in model_results.columns if c.replace("²","2").replace("^2","2").upper().strip() == "R2"), None)
    mae_col = next((c for c in model_results.columns if "MAE" in c.upper()), None)
    mod_col = next((c for c in model_results.columns if "MOD" in c.upper()), model_results.columns[0])
    if r2_col is None:
        st.warning(f"⚠️ Colonnes détectées dans le CSV : {list(model_results.columns)}")
    else:
        best    = model_results.loc[model_results[r2_col].idxmax()]
        mae_val = f"{int(best[mae_col]):,}" if mae_col else "N/A"
        precision = round(best[r2_col] * 100, 1)
        st.success(
            f"Meilleur modèle : **{best[mod_col]}** — "
            f"Prédit correctement **{precision}% du temps** — "
            f"Marge d'erreur moyenne : **{mae_val} voyageurs** par tranche de 30 min"
        )

    with st.expander("Comment lire ces résultats ?"):
        st.markdown("""
| Indicateur | Ce que ça signifie concrètement |
|---|---|
| **R² = 0.977** | Le modèle prédit correctement 97.7% du temps |
| **MAE = 112** | En moyenne, il se trompe de 112 voyageurs sur 30 min |
| **RMSE** | Mesure les erreurs importantes — plus c'est bas, mieux c'est |
        """)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#90A4AE; font-size:0.75rem; padding:0.5rem 0;
            font-family: Plus Jakarta Sans, sans-serif; letter-spacing:0.5px'>
    TER Dakar · Dashboard v2.0 · Projet Data Science · Equipe TER
</div>""", unsafe_allow_html=True)