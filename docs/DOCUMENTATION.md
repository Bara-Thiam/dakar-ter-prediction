# Documentation Technique — TER Dakar

**Projet :** Prédiction de la Fréquentation du Train Express Régional de Dakar  
**Version :** 2.0  
**Date :** Mars 2026  

---

## Table des matières

1. [Architecture technique](#1-architecture-technique)
2. [Dataset et schéma des données](#2-dataset-et-schéma-des-données)
3. [Modèles ML](#3-modèles-ml)
4. [API de prédiction](#4-api-de-prédiction)
5. [Dashboard Streamlit](#5-dashboard-streamlit)
6. [Workflow Git](#6-workflow-git)
7. [Réentraînement du modèle](#7-réentraînement-du-modèle)
8. [Dépendances](#8-dépendances)

---

## 1. Architecture Technique

### Stack technologique

| Couche | Technologie | Usage |
|--------|-------------|-------|
| Langage | Python 3.10+ | Tout le projet |
| ML | scikit-learn, XGBoost | Modèles prédictifs |
| Données | pandas, numpy | Manipulation des données |
| Visualisation | matplotlib, seaborn, plotly | Graphiques |
| Interface | Streamlit | Dashboard interactif |
| Persistance | joblib | Sauvegarde des modèles .pkl |
| Notebooks | Jupyter | Analyse exploratoire |

### Flux de données

```
dataset_ter_dakar_2022_2026.csv
        │
        ▼
models/model_xgboost.py  ──── entraînement ────►  model_final.pkl
        │
        ▼
app/api_prediction.py    ──── expose predict() ──► app/dashboard.py
        │
        ▼
localhost:8501  (Streamlit)
```

---

## 2. Dataset et Schéma des Données

### Fichier principal

```
data/dataset_ter_dakar_2022_2026.csv
```

**Format :** CSV, encodage UTF-8, séparateur virgule  
**Taille :** 67 562 lignes × 17 colonnes  

### Schéma complet

```python
{
    # Temporel
    "date":                  "datetime64",  # Date (YYYY-MM-DD)
    "annee":                 "int64",       # 2022–2026
    "mois":                  "int64",       # 1–12
    "jour_semaine":          "object",      # lundi–dimanche
    "heure":                 "int64",       # 5–23
    "minute":                "int64",       # 0 ou 30

    # Contextuel binaire
    "est_weekend":           "int64",       # 0 ou 1
    "est_jour_ferie":        "int64",       # 0 ou 1
    "est_vacances_scolaires":"int64",       # 0 ou 1
    "est_saison_pluies":     "int64",       # 0 ou 1 (juil–oct)
    "est_ramadan":           "int64",       # 0 ou 1

    # Contextuel catégoriel
    "evenement_religieux":   "int64",       # 0=Aucun, 1=Magal, 2=Gamou, 3=Korité, 4=Tabaski
    "evenement_special":     "int64",       # 0=Aucun, 1=JOJ 2026, 2=Fête nat., 3=Autre
    "perturbation":          "int64",       # 0=Aucune, 1=Panne, 2=Inondation, 3=Grève

    # Réseau
    "phase_reseau":          "int64",       # 1 ou 2
    "nb_rames_actives":      "int64",       # 15–22

    # Cible
    "frequentation":         "int64",       # voyageurs / 30 min
}
```

---

## 3. Modèles ML

### Pipeline commun

Tous les modèles utilisent le même pipeline de prétraitement :

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Variables catégorielles → OneHotEncoder
# Variables numériques   → StandardScaler (pour régression linéaire)
# Variables binaires     → passthrough
```

### 3.1 Régression Linéaire

**Fichier :** `models/model_regression.py`  
**Usage :** Modèle baseline — démontre la complexité non-linéaire du problème  
**Performances :** R² = 0.1961 | MAE = 808 | RMSE = 991  

```python
from sklearn.linear_model import LinearRegression
```

### 3.2 Random Forest

**Fichier :** `models/model_random_forest.py`  
**Hyperparamètres optimisés :**

```python
RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
```

**Performances :** R² = 0.9685 | MAE = 128 | RMSE = 196  
**Feature importance principale :** heure (74.6%), est_weekend (9.9%)

### 3.3 XGBoost — Modèle Final ✅

**Fichier :** `models/model_xgboost.py`  
**Hyperparamètres optimisés :**

```python
XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
```

**Performances :** R² = 0.9771 | MAE = 112 | RMSE = 167  
**Feature importance principale :** heure (30.9%), est_weekend (18.4%), evenement_special (8.5%)  
**Modèle sauvegardé :** `models/model_final.pkl`

### 3.4 Comparaison et Optimisation

```bash
# Générer le graphique comparatif
python -m models.comparaison_modeles

# Optimisation GridSearchCV (10–20 min)
python models/optimisation.py
```

Sortie : `visualisations/comparaison_modeles.png` et `docs/comparaison_resultats.csv`

---

## 4. API de Prédiction

**Fichier :** `app/api_prediction.py`

### Fonction `predict()`

```python
def predict(
    jour_semaine: str,        # "lundi"–"dimanche"
    annee: int,               # 2022–2026
    mois: int,                # 1–12
    heure: int,               # 5–23
    minute: int,              # 0 ou 30
    est_jour_ferie: int,      # 0 ou 1
    est_vacances_scolaires: int,
    est_saison_pluies: int,
    est_ramadan: int,
    evenement_religieux: int, # 0–4
    evenement_special: int,   # 0–3
    perturbation: int,        # 0–3
    phase_reseau: int,        # 1 ou 2
    nb_rames_actives: int     # 15–22
) -> dict:
    # Retourne :
    # {
    #     "frequentation": int,        # voyageurs prédits
    #     "intervalle": (int, int)     # [min, max] ± MAE
    # }
```

### Exemple d'utilisation

```python
from api_prediction import predict

result = predict(
    jour_semaine="lundi",
    annee=2025, mois=3,
    heure=8, minute=0,
    est_jour_ferie=0, est_vacances_scolaires=0,
    est_saison_pluies=0, est_ramadan=0,
    evenement_religieux=0, evenement_special=0,
    perturbation=0, phase_reseau=1, nb_rames_actives=22
)
# {'frequentation': 4374, 'intervalle': (4265, 4483)}
```

### Fonction `predict_journee()`

Génère les 38 prédictions (19 heures × 2 tranches) d'une journée complète.

```python
def predict_journee(jour, annee, mois, **kwargs) -> list[dict]:
    # Retourne une liste de 38 dictionnaires
    # [{heure, minute, frequentation, intervalle}, ...]
```

---

## 5. Dashboard Streamlit

**Fichier :** `app/dashboard.py`

### Lancement

```bash
streamlit run app/dashboard.py
```

### Pages disponibles

| Page | Description |
|------|-------------|
| **Accueil et KPIs** | Indicateurs clés, évolution annuelle, patterns journaliers |
| **Prédiction** | Simulateur de prédiction avec tous les paramètres |
| **Analyses** | EDA interactive — profil horaire, saisonnalité, heatmap, événements |
| **Modèles ML** | Comparaison des 3 modèles avec métriques et graphiques |

### Connexion au modèle

Le dashboard tente d'importer `api_prediction.py` au démarrage :
- ✅ Si l'import réussit → prédictions via le vrai modèle XGBoost
- ⚠️ Si l'import échoue → mode démo avec `mock_predict()` (règles simples)

### Assets requis

```
app/assets/logo_ter.png    ← Logo TER (fond transparent recommandé)
```

---

## 6. Workflow Git

### Branches

| Branche | Propriétaire | Usage |
|---------|-------------|-------|
| `main` | Tous | Version finale stable |
| `bara` | Bara | ML, API, coordination |
| `mactar` | Membre 2 | EDA, visualisations |
| `joanelle` | Membre 3 | Dashboard, présentation |

### Commandes quotidiennes

```bash
# Récupérer les dernières modifications
git pull origin bara

# Sauvegarder son travail
git add .
git commit -m "feat: description du travail"
git push origin bara

# Récupérer un fichier spécifique d'une autre branche
git checkout joanelle -- app/dashboard.py
```

### Récupérer le travail de toute l'équipe (merge final)

```bash
git checkout main
git merge bara
git merge membre2
git merge joanelle
git push origin main
```

---

## 7. Réentraînement du Modèle

Pour réentraîner le modèle sur de nouvelles données :

```bash
# 1. Placer le nouveau dataset dans data/
cp nouveau_dataset.csv data/dataset_ter_dakar_2022_2026.csv

# 2. Réentraîner XGBoost
python -m models.model_xgboost

# 3. Vérifier les performances
python -m models.comparaison_modeles

# 4. Optimiser si nécessaire
python models/optimisation.py
```

Le nouveau `model_final.pkl` sera automatiquement utilisé par le dashboard au prochain démarrage.

---

## 8. Dépendances

### Installation

```bash
pip install -r requirements.txt
```

### Liste complète

```
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
xgboost>=2.0
matplotlib>=3.7
seaborn>=0.12
jupyter>=1.0
streamlit>=1.28
joblib>=1.3
plotly>=5.15
pillow>=10.0
```

### Versions testées

- Python 3.14 (Windows)
- Streamlit 1.x
- XGBoost 2.x

---

## 9. Problèmes Connus et Solutions

| Problème | Cause | Solution |
|----------|-------|----------|
| `KeyError: 'date'` | Colonne date absente ou dataset corrompu | Vérifier le CSV avec `python -c "import pandas as pd; print(pd.read_csv('data/dataset_ter_dakar_2022_2026.csv').columns.tolist())"` |
| `Import api_prediction could not be resolved` | Avertissement VS Code uniquement | Ignorer — fonctionne à l'exécution |
| Texte blanc sur graphiques | Thème sombre Streamlit | Voir CSS dans `dashboard.py` — LAYOUT dict avec `font=dict(color="#263238")` |
| Mode démo au lieu de XGBoost | `model_final.pkl` absent ou erreur import | Vérifier que `models/model_final.pkl` existe et relancer depuis la racine |

---

*Documentation technique — Projet Data Science — Equipe TER — Mars 2026*