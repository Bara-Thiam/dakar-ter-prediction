# 🚆 TER Dakar — Prédiction de Fréquentation

> Système de prédiction de la fréquentation du Train Express Régional de Dakar basé sur le Machine Learning (XGBoost · R² = 0.978)

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![XGBoost](https://img.shields.io/badge/XGBoost-R²=0.978-green) ![Dataset](https://img.shields.io/badge/Dataset-67%2C562%20lignes-orange)

---

## 📋 Description

Ce projet développe un **tableau de bord interactif** pour prédire et analyser la fréquentation du TER Dakar à une granularité de 30 minutes. Il s'appuie sur 4 ans de données réelles (2022–2026) et trois modèles de Machine Learning comparés.

**Contexte :** Le TER Dakar est le premier train express régional d'Afrique subsaharienne, reliant Dakar à l'AIBD sur 55 km. Une meilleure prédiction de la fréquentation permet d'optimiser le nombre de rames en service et d'anticiper les pics de trafic.

---

## 🏗️ Architecture du Projet

```
projet-ter-ia/
│
├── data/
│   ├── schema_dataset.md               ← Schéma commun des données
│   └── dataset_ter_dakar_2022_2026.csv ← Dataset réel (67 562 lignes)
│
├── models/
│   ├── model_regression.py             ← Régression linéaire
│   ├── model_random_forest.py          ← Random Forest
│   ├── model_xgboost.py                ← XGBoost
│   ├── comparaison_modeles.py          ← Pipeline de comparaison
│   ├── optimisation.py                 ← Optimisation hyperparamètres
│   └── model_final.pkl                 ← Modèle XGBoost entraîné
│
├── app/
│   ├── dashboard.py                    ← Dashboard Streamlit
│   ├── api_prediction.py               ← API de prédiction
│   └── assets/
│       └── logo_ter.png
│
├── notebooks/
│   └── analyse_exploratoire.ipynb      ← EDA complet
│
├── visualisations/                     ← Graphiques PNG haute qualité
│
├── docs/
│   ├── rapport_evaluation.md           ← Rapport comparaison modèles ML
│   ├── rapport_analyse_donnees.md      ← Rapport analyse exploratoire
│   ├── DOCUMENTATION.md                ← Documentation technique
│   └── comparaison_resultats.csv       ← Métriques des modèles
│
├── presentation/
│   └── presentation_ter.pptx           ← Présentation PowerPoint finale
│
├── requirements.txt
└── README.md
```

---

## 👥 Équipe

| Membre | Rôle | Responsabilités |
|--------|------|-----------------|
| **Bara** | Chef de projet & ML Engineer | Dataset, modèles ML, API, coordination |
| **Mactar** | Data Analyst | Collecte données, EDA, visualisations |
| **Joanelle** | Développeur Interface | Dashboard Streamlit, PowerPoint |

---

## ⚙️ Installation

### Prérequis
- Python 3.10+
- Git

### 1. Cloner le repository

```bash
git clone https://github.com/Bara-Thiam/projet_ter_ia.git
cd projet_ter_ia
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Lancement

### Dashboard interactif

```bash
streamlit run app/dashboard.py
```

Ouvre automatiquement `http://localhost:8501`

### Notebook d'analyse

```bash
jupyter notebook notebooks/analyse_exploratoire.ipynb
```

### Entraîner les modèles

```bash
python -m models.model_regression
python -m models.model_random_forest
python -m models.model_xgboost
```

### Comparer les modèles

```bash
python -m models.comparaison_modeles
```

### Optimiser les hyperparamètres

```bash
python models/optimisation.py
```

---

## 📊 Résultats des Modèles

| Modèle | R² | MAE | RMSE |
|--------|-----|-----|------|
| Régression Linéaire | 0.1961 | 808 voy. | 991 |
| Random Forest | 0.9685 | 128 voy. | 196 |
| **XGBoost** ✅ | **0.9771** | **112 voy.** | **167** |

Le modèle XGBoost a été sélectionné comme modèle final. Il prédit la fréquentation avec une **erreur moyenne de 112 voyageurs** par tranche de 30 minutes.

---

## 📦 Dataset

- **Source :** SETER, SENTER, CETUD, Banque Mondiale
- **Période :** 2022–2026
- **Taille :** 67 562 observations
- **Granularité :** 30 minutes (5h00 → 23h30)
- **Variables :** 17 colonnes (temporelles, contextuelles, cible)

---

## 🔧 Requirements

```
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
jupyter
streamlit
joblib
plotly
pillow
```

---

*Projet Machine learning — Equipe TER — Mars 2026*
