# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

st.set_page_config(
    page_title="TER Dakar - Prediction Frequentation",
    page_icon="TER",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background-color: #F7FAF7;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 60%, #388E3C 100%);
        border-right: none;
        box-shadow: 4px 0 15px rgba(0,0,0,0.15);
    }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.25) !important; }
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #43A047 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(27,94,32,0.3);
    }
    .main-header h1 { margin: 0; font-size: 2.1rem; font-weight: 700; color: white; }
    .main-header p  { margin: 0.5rem 0 0; opacity: 0.85; font-size: 1rem; color: white; font-weight: 300; }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.5rem 1.2rem;
        box-shadow: 0 4px 20px rgba(46,125,50,0.10);
        border-top: 4px solid #43A047;
        text-align: center;
    }
    .kpi-value { font-size: 1.9rem; font-weight: 800; color: #1B5E20; }
    .kpi-label { font-size: 0.8rem; color: #555555; margin-top: 0.4rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .pred-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white;
        border-radius: 18px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(27,94,32,0.30);
    }
    .pred-box .pred-value { font-size: 3.5rem; font-weight: 900; color: white; }
    .pred-box .pred-label { font-size: 0.95rem; opacity: 0.85; color: white; text-transform: uppercase; letter-spacing: 1px; }
    .badge { display: inline-block; padding: 0.4rem 1.2rem; border-radius: 50px; font-weight: 700; font-size: 0.85rem; margin-top: 1rem; }
    .badge-high   { background: rgba(255,255,255,0.2); color: #FFD6D6; border: 1px solid rgba(255,100,100,0.4); }
    .badge-medium { background: rgba(255,255,255,0.2); color: #FFE9A0; border: 1px solid rgba(255,200,50,0.4); }
    .badge-low    { background: rgba(255,255,255,0.2); color: #C8F5CB; border: 1px solid rgba(150,255,150,0.4); }
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1B5E20;
        border-bottom: 2px solid #A5D6A7;
        padding-bottom: 0.5rem;
        margin-bottom: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #43A047) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(46,125,50,0.3) !important;
    }
    hr { border-color: #E8F5E9 !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def generate_simulated_data():
    np.random.seed(42)
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    rows = []
    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    for d in dates:
        jour = jours_semaine[d.dayofweek]
        mois = d.month
        if mois in [1, 2, 7, 8, 12]:
            periode = "haute_saison"
        elif mois in [6, 9]:
            periode = "vacances_scolaires"
        else:
            periode = "basse_saison"
        est_ferie = 1 if (mois == 1 and d.day == 1) else 0
        for heure in range(5, 23):
            if heure in [7, 8, 9]:
                base = 120000 + np.random.normal(0, 10000)
            elif heure in [17, 18, 19]:
                base = 100000 + np.random.normal(0, 8000)
            elif heure in [6, 10, 16, 20]:
                base = 60000 + np.random.normal(0, 6000)
            else:
                base = 30000 + np.random.normal(0, 5000)
            if jour == "Samedi":
                base *= 0.75
            elif jour == "Dimanche":
                base *= 0.55
            if periode == "haute_saison":
                base *= 1.2
            elif periode == "vacances_scolaires":
                base *= 0.85
            if est_ferie:
                base *= 0.4
            rows.append({
                "date": d, "jour_semaine": jour, "heure": heure,
                "periode_annee": periode, "est_jour_ferie": est_ferie,
                "frequentation": max(int(base), 500),
                "mois": d.month, "num_semaine": int(d.isocalendar().week),
            })
    return pd.DataFrame(rows)


@st.cache_data
def load_model_results():
    return pd.DataFrame({
        "Modele": ["Regression Lineaire", "Random Forest", "XGBoost"],
        "R2": [0.79, 0.93, 0.96],
        "MAE": [8200, 4100, 3300],
        "RMSE": [11500, 5900, 4700],
    })


def mock_predict(jour, heure, periode, est_ferie):
    if heure in [7, 8, 9]:
        base = 118000
    elif heure in [17, 18, 19]:
        base = 98000
    elif heure in [6, 10, 16, 20]:
        base = 58000
    else:
        base = 28000
    if jour == "Samedi":
        base = int(base * 0.75)
    elif jour == "Dimanche":
        base = int(base * 0.55)
    if periode == "haute_saison":
        base = int(base * 1.2)
    elif periode == "vacances_scolaires":
        base = int(base * 0.85)
    if est_ferie:
        base = int(base * 0.4)
    return max(base, 500)


def get_niveau(val):
    if val >= 90000:
        return "Forte affluence", "badge-high"
    elif val >= 50000:
        return "Affluence moderee", "badge-medium"
    else:
        return "Faible affluence", "badge-low"


LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#111111", family="Segoe UI"),
    margin=dict(l=10, r=10, t=30, b=10)
)

df = generate_simulated_data()
model_results = load_model_results()

predict_fn = mock_predict
api_status = "Mode demo (API non connectee)"
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from api_prediction import predict as real_predict
    predict_fn = lambda j, h, p, f: real_predict(j, h, p)
    api_status = "API de prediction connectee"
except ImportError:
    pass

with st.sidebar:
    st.markdown("## TER Dakar")
    st.markdown("---")
    page = st.radio("Navigation", ["Accueil et KPIs", "Prediction", "Analyses", "Modeles ML"])
    st.markdown("---")
    st.markdown(f"**Statut API :** {api_status}")
    st.markdown("---")
    st.caption("Projet Data Science - Equipe TER - v1.0")

st.markdown("""
<div class="main-header">
    <h1>TER Dakar - Prediction de Frequentation</h1>
    <p>Tableau de bord interactif d analyse et de prediction du Train Express Regional</p>
</div>
""", unsafe_allow_html=True)

# ─── PAGE : Accueil et KPIs ───────────────────────────────────────────────────
if page == "Accueil et KPIs":
    st.markdown('<div class="section-title">Indicateurs cles</div>', unsafe_allow_html=True)

    total = int(df["frequentation"].sum())
    moy_jour = int(df.groupby("date")["frequentation"].sum().mean())
    pic_heure = int(df.groupby("heure")["frequentation"].mean().idxmax())
    ferie_ratio = round(
        df[df["est_jour_ferie"] == 1]["frequentation"].mean() /
        df[df["est_jour_ferie"] == 0]["frequentation"].mean() * 100 - 100, 1)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total:,}</div><div class="kpi-label">Total voyageurs 2024</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{moy_jour:,}</div><div class="kpi-label">Moyenne journaliere</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{pic_heure}h</div><div class="kpi-label">Heure de pointe</div></div>', unsafe_allow_html=True)
    with c4:
        color_val = "#C62828" if ferie_ratio < 0 else "#2E7D32"
        st.markdown(f'<div class="kpi-card"><div class="kpi-value" style="color:{color_val}">{ferie_ratio:+.1f}%</div><div class="kpi-label">Jours feries vs normal</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Frequentation hebdomadaire</div>', unsafe_allow_html=True)
    weekly = df.groupby("num_semaine")["frequentation"].sum().reset_index()
    fig_w = px.area(weekly, x="num_semaine", y="frequentation",
                    color_discrete_sequence=["#43A047"], template="plotly_white",
                    labels={"num_semaine": "Semaine", "frequentation": "Total voyageurs"})
    fig_w.update_traces(fill="tozeroy", line_color="#1B5E20", fillcolor="rgba(67,160,71,0.15)")
    fig_w.update_layout(height=270, **LAYOUT)
    st.plotly_chart(fig_w, use_container_width=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="section-title">Par jour de la semaine</div>', unsafe_allow_html=True)
        order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        by_day = df.groupby("jour_semaine")["frequentation"].mean().reindex(order).reset_index()
        fig_d = px.bar(by_day, x="jour_semaine", y="frequentation",
                       color="frequentation", color_continuous_scale=["#C8E6C9", "#1B5E20"],
                       template="plotly_white", labels={"frequentation": "Freq. moy.", "jour_semaine": ""})
        fig_d.update_layout(height=300, coloraxis_showscale=False, **LAYOUT)
        st.plotly_chart(fig_d, use_container_width=True)
    with cb:
        st.markdown('<div class="section-title">Par periode annuelle</div>', unsafe_allow_html=True)
        by_per = df.groupby("periode_annee")["frequentation"].sum().reset_index()
        fig_p = px.pie(by_per, names="periode_annee", values="frequentation",
                       color_discrete_sequence=["#1B5E20", "#43A047", "#A5D6A7"], hole=0.45, template="plotly_white")
        fig_p.update_layout(height=300, **LAYOUT)
        st.plotly_chart(fig_p, use_container_width=True)

# ─── PAGE : Prediction ────────────────────────────────────────────────────────
elif page == "Prediction":
    st.markdown('<div class="section-title">Simulateur de prediction</div>', unsafe_allow_html=True)
    col_f, col_r = st.columns([1, 1], gap="large")
    with col_f:
        st.markdown("#### Parametres")
        jour = st.selectbox("Jour", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        heure = st.slider("Heure", 5, 22, 8, format="%dh")
        periode = st.selectbox(
            "Periode",
            ["haute_saison", "basse_saison", "vacances_scolaires"],
            format_func=lambda x: {
                "haute_saison": "Haute saison",
                "basse_saison": "Basse saison",
                "vacances_scolaires": "Vacances scolaires"
            }[x]
        )
        est_ferie = st.toggle("Jour ferie", value=False)
        go_btn = st.button("Lancer la prediction", type="primary", use_container_width=True)

    with col_r:
        if go_btn:
            val = predict_fn(jour, heure, periode, int(est_ferie))
            niv_txt, niv_cls = get_niveau(val)
            st.markdown(f"""<div class="pred-box">
                <div class="pred-label">Frequentation estimee</div>
                <div class="pred-value">{val:,}</div>
                <div class="pred-label">voyageurs</div>
                <br><span class="badge {niv_cls}">{niv_txt}</span>
            </div>""", unsafe_allow_html=True)
            st.markdown("#### Profil horaire du jour")
            heures = list(range(5, 23))
            preds = [predict_fn(jour, h, periode, int(est_ferie)) for h in heures]
            fig_h = go.Figure()
            fig_h.add_trace(go.Scatter(
                x=heures, y=preds, mode="lines+markers",
                line=dict(color="#2E7D32", width=2.5),
                marker=dict(color=["#C62828" if h == heure else "#43A047" for h in heures], size=9)
            ))
            fig_h.add_vline(x=heure, line_dash="dot", line_color="#A5D6A7", line_width=2)
            fig_h.update_layout(height=230, xaxis_title="Heure", yaxis_title="Voyageurs",
                                 template="plotly_white", showlegend=False, **LAYOUT)
            st.plotly_chart(fig_h, use_container_width=True)
        else:
            st.info("Configurez les parametres puis cliquez sur Lancer la prediction.")

    st.markdown("---")
    st.markdown('<div class="section-title">Heatmap semaine type</div>', unsafe_allow_html=True)
    periode_b = st.selectbox(
        "Periode :",
        ["haute_saison", "basse_saison", "vacances_scolaires"],
        format_func=lambda x: {
            "haute_saison": "Haute saison",
            "basse_saison": "Basse saison",
            "vacances_scolaires": "Vacances scolaires"
        }[x]
    )
    jours_ordre = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    heures_r = list(range(5, 23))
    matrix = pd.DataFrame(
        {j: [predict_fn(j, h, periode_b, 0) for h in heures_r] for j in jours_ordre},
        index=heures_r
    )
    fig_hm = px.imshow(matrix.T, color_continuous_scale=["#F1F8E9", "#43A047", "#1B5E20"],
                       labels=dict(x="Heure", y="Jour", color="Voyageurs"), aspect="auto", template="plotly_white")
    fig_hm.update_layout(height=330, **LAYOUT)
    st.plotly_chart(fig_hm, use_container_width=True)

# ─── PAGE : Analyses ──────────────────────────────────────────────────────────
elif page == "Analyses":
    st.markdown('<div class="section-title">Analyse exploratoire</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Profil horaire", "Saisonnalite", "Heatmap"])

    with tab1:
        bh = df.groupby("heure")["frequentation"].agg(["mean", "std"]).reset_index()
        fig_hr = go.Figure([
            go.Scatter(x=bh["heure"], y=bh["mean"] + bh["std"], mode="lines", line=dict(width=0), showlegend=False),
            go.Scatter(x=bh["heure"], y=bh["mean"] - bh["std"], mode="lines", line=dict(width=0),
                       fill="tonexty", fillcolor="rgba(67,160,71,0.12)", showlegend=False),
            go.Scatter(x=bh["heure"], y=bh["mean"], mode="lines+markers",
                       line=dict(color="#1B5E20", width=3),
                       marker=dict(size=8, color="#43A047", line=dict(color="white", width=1.5)),
                       name="Frequentation moyenne"),
        ])
        fig_hr.update_layout(title="Frequentation moyenne par heure",
                              xaxis_title="Heure", yaxis_title="Voyageurs",
                              template="plotly_white", height=400, **LAYOUT)
        st.plotly_chart(fig_hr, use_container_width=True)

    with tab2:
        bm = df.groupby("mois")["frequentation"].sum().reset_index()
        bm["mois_nom"] = bm["mois"].map({
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Jun",
            7: "Jul", 8: "Aou", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        })
        fig_mo = px.bar(bm, x="mois_nom", y="frequentation",
                        color="frequentation", color_continuous_scale=["#C8E6C9", "#1B5E20"],
                        template="plotly_white",
                        labels={"frequentation": "Total voyageurs", "mois_nom": "Mois"},
                        title="Frequentation totale par mois")
        fig_mo.update_layout(height=400, coloraxis_showscale=False, **LAYOUT)
        st.plotly_chart(fig_mo, use_container_width=True)

    with tab3:
        order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        pivot = df.groupby(["jour_semaine", "heure"])["frequentation"].mean().unstack("heure").reindex(order)
        fig_hm2 = px.imshow(pivot, color_continuous_scale=["#F1F8E9", "#43A047", "#1B5E20"],
                             labels=dict(x="Heure", y="Jour", color="Freq. moy."),
                             aspect="auto", template="plotly_white",
                             title="Heatmap Frequentation par jour et heure")
        fig_hm2.update_layout(height=400, **LAYOUT)
        st.plotly_chart(fig_hm2, use_container_width=True)

# ─── PAGE : Modeles ML ────────────────────────────────────────────────────────
elif page == "Modeles ML":
    st.markdown('<div class="section-title">Comparaison des modeles ML</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_r2 = px.bar(model_results, x="Modele", y="R2",
                        color="Modele", color_discrete_sequence=["#A5D6A7", "#43A047", "#1B5E20"],
                        template="plotly_white", title="Score R2", text="R2")
        fig_r2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_r2.update_layout(height=330, showlegend=False, yaxis_range=[0, 1.15], **LAYOUT)
        st.plotly_chart(fig_r2, use_container_width=True)
    with c2:
        df_melt = model_results.melt(id_vars="Modele", value_vars=["MAE", "RMSE"], var_name="Metrique", value_name="Erreur")
        fig_err = px.bar(df_melt, x="Modele", y="Erreur", color="Metrique", barmode="group",
                         color_discrete_sequence=["#F9A825", "#E53935"],
                         template="plotly_white", title="Erreurs MAE et RMSE")
        fig_err.update_layout(height=330, **LAYOUT)
        st.plotly_chart(fig_err, use_container_width=True)

    st.markdown("#### Tableau recapitulatif")
    st.dataframe(model_results, use_container_width=True, hide_index=True)
    best = model_results.loc[model_results["R2"].idxmax()]
    st.success(f"Meilleur modele : {best['Modele']} - R2 = {best['R2']:.2f} | MAE = {int(best['MAE']):,} voyageurs")

    with st.expander("Interpretation des metriques"):
        st.markdown("""
- **R2** : proportion de variance expliquee. Plus proche de 1 = meilleur modele.
- **MAE** : erreur absolue moyenne en voyageurs. Facile a interpreter.
- **RMSE** : sensible aux grandes erreurs. Un RMSE faible = predictions stables.
        """)

st.markdown("---")
st.markdown("<div style='text-align:center; color:#888; font-size:0.78rem;'>TER Dakar - Dashboard v1.0 | Projet Data Science | Equipe TER</div>", unsafe_allow_html=True)
