
# DOCUMENTATION TECHNIQUE — TER Dakar · Prédiction de Fréquentation

**Date :** Mars 2026  
**Auteur :** Joanelle — Développeur Interface  

---

## Table des matières

1. [Vue d'ensemble de l'architecture](#1-vue-densemble-de-larchitecture)
2. [Description des composants](#2-description-des-composants)
3. [Le Dashboard Streamlit](#3-le-dashboard-streamlit)
4. [Flux de données](#4-flux-de-données)
5. [API de Prédiction](#5-api-de-prédiction)
6. [Format des données](#6-format-des-données)
7. [Guide de déploiement](#7-guide-de-déploiement)
8. [Tests et validation](#8-tests-et-validation)
9. [Décisions techniques](#9-décisions-techniques)
10. [Considérations éthiques](#10-considérations-éthiques)

---

## 1. Vue d'ensemble de l'architecture

Le projet suit une architecture en couches clairement séparées, permettant à chaque membre de travailler de manière indépendante.

```
┌─────────────────────────────────────────────────┐
│               COUCHE PRÉSENTATION                │
│          Dashboard Streamlit (app/dashboard.py)  │
└──────────────────────┬──────────────────────────┘
                       │ appelle
┌──────────────────────▼──────────────────────────┐
│               COUCHE PRÉDICTION                  │
│          API de Prédiction (api_prediction.py)   │
│  predict(jour, heure, periode, ferie) → dict     │
└──────────────────────┬──────────────────────────┘
                       │ charge
┌──────────────────────▼──────────────────────────┐
│               COUCHE MODÈLES ML                  │
│   model_final.pkl (Random Forest / XGBoost)      │
│   Entraîné sur dataset_ter_dakar.csv             │
└──────────────────────┬──────────────────────────┘
                       │ produit par
┌──────────────────────▼──────────────────────────┐
│               COUCHE DONNÉES                     │
│   data/dataset_ter_dakar.csv                     │
│   Sources : CETUD, SETER, GTFS, météo            │
└─────────────────────────────────────────────────┘
```

---

## 2. Description des composants

### `app/dashboard.py`
Interface utilisateur principale. Développée avec **Streamlit** et **Plotly**. Contient 4 pages :
- **Accueil & Prédiction** : formulaire interactif + graphique journalier
- **Analyses & Statistiques** : 4 onglets (Jour, Heure, Saisonnalité, Heatmap)
- **Carte des Stations** : carte OpenStreetMap avec fréquentation par station
- **À propos** : description du projet et de l'équipe

### `app/api_prediction.py`
Interface entre le dashboard et les modèles ML. Expose une unique fonction `predict()`. Permet d'isoler le dashboard de la complexité des modèles.

### `models/`
Contient les scripts d'entraînement des 3 algorithmes et le pipeline de comparaison. Le modèle final est sérialisé dans `model_final.pkl`.

### `data/dataset_ter_dakar.csv`
Dataset principal collecté via OSINT. Contient les données historiques de fréquentation enrichies avec des variables contextuelles.

---

## 3. Le Dashboard Streamlit

### Structure du code

```
dashboard.py
├── Configuration de la page (set_page_config)
├── CSS personnalisé (st.markdown)
├── Fonction mock predict() [à remplacer]
├── Données simulées (charger_donnees_simulees)
├── Barre latérale (navigation + paramètres)
└── Pages
    ├── Page 1 : Accueil & Prédiction
    │   ├── KPI cards
    │   ├── Formulaire de prédiction (st.form)
    │   └── Graphique journalier (Plotly Bar)
    ├── Page 2 : Analyses & Statistiques
    │   ├── Onglet 1 : Fréquentation par jour (Bar)
    │   ├── Onglet 2 : Profil horaire (Scatter + fill)
    │   ├── Onglet 3 : Saisonnalité (Bar + Box)
    │   └── Onglet 4 : Heatmap Jour×Heure
    ├── Page 3 : Carte des Stations (Mapbox)
    └── Page 4 : À propos
```

### Bibliothèques utilisées

| Bibliothèque | Rôle dans le dashboard |
|---|---|
| `streamlit` | Framework UI, routing, composants |
| `plotly.express` | Graphiques haut niveau (bar, scatter, box) |
| `plotly.graph_objects` | Graphiques bas niveau (heatmap, fills, scatter_mapbox) |
| `pandas` | Agrégation des données pour les graphiques |
| `numpy` | Calcul des données simulées |

### Paramètres CSS customisés

Le dashboard utilise du CSS injecté via `st.markdown(..., unsafe_allow_html=True)` pour personnaliser :
- Le header dégradé bleu (`.main-header`)
- Les cartes de métriques (`.metric-card`)
- La boîte de résultat de prédiction (`.prediction-box`)
- Les badges de niveau d'affluence (`.badge-high`, `.badge-medium`, `.badge-low`)

---

## 4. Flux de données

### Prédiction (flux principal)

```
Utilisateur remplit le formulaire
        ↓
[jour, heure, periode, est_ferie]
        ↓
predict(jour, heure, periode, est_ferie)
        ↓
Chargement du modèle (.pkl)
        ↓
Encodage des variables catégorielles
        ↓
model.predict([[features]])
        ↓
Post-traitement (arrondi, classification du niveau)
        ↓
{frequentation: int, niveau: str, couleur: str, badge: str}
        ↓
Affichage dans le dashboard
```

### Analyses statistiques (flux secondaire)

```
data/dataset_ter_dakar.csv
        ↓
pd.read_csv()
        ↓
groupby() + agg() selon l'onglet
        ↓
Plotly figure
        ↓
st.plotly_chart()
```

---

## 5. API de Prédiction

### Contrat d'interface

La fonction `predict()` est le seul point d'entrée entre le dashboard et les modèles ML.

**Signature :**
```python
def predict(
    jour_semaine: str,     # "lundi" | "mardi" | ... | "dimanche"
    heure: int,            # 6 à 21 inclus
    periode_annee: str,    # "haute_saison" | "saison_normale" | "basse_saison"
    est_ferie: bool        # True | False
) -> dict
```

**Valeur de retour :**
```python
{
    "frequentation": 127350,        # int – nombre de voyageurs estimés
    "niveau": "Très forte affluence",  # str – label lisible
    "couleur": "#e74c3c",           # str – code couleur hex
    "badge": "badge-high"           # str – classe CSS pour le badge
}
```

**Niveaux d'affluence :**

| Seuil | Niveau | Couleur |
|---|---|---|
| > 120 000 | Très forte affluence | `#e74c3c` (rouge) |
| 80 000 – 120 000 | Forte affluence | `#f39c12` (orange) |
| 40 000 – 80 000 | Affluence normale | `#2e86c1` (bleu) |
| < 40 000 | Faible affluence | `#27ae60` (vert) |

---

## 6. Format des données

### Schéma du dataset principal

| Colonne | Type | Description | Exemple |
|---|---|---|---|
| `date` | date | Date de la mesure | `2024-03-15` |
| `jour_semaine` | str | Jour en français minuscule | `lundi` |
| `heure` | int | Heure (6–21) | `8` |
| `periode_annee` | str | Saison | `haute_saison` |
| `est_jour_ferie` | int | 0 ou 1 | `0` |
| `frequentation` | int | Nombre de voyageurs | `127350` |

### Encodage pour les modèles ML

Les variables catégorielles sont encodées avant d'entrer dans les modèles :

```python
# Encodage One-Hot pour jour_semaine
pd.get_dummies(df["jour_semaine"])

# Encodage ordinal pour periode_annee
{"basse_saison": 0, "saison_normale": 1, "haute_saison": 2}
```

---

## 7. Guide de déploiement

### Déploiement local (développement)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le dashboard
streamlit run app/dashboard.py

# 3. Accéder au dashboard
# → http://localhost:8501
```

### Déploiement sur Streamlit Cloud (production)

1. Pousser le code sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter le dépôt GitHub
4. Renseigner le fichier principal : `app/dashboard.py`
5. Cliquer sur **Deploy**

### Variables d'environnement (si nécessaire)

Créer un fichier `.streamlit/secrets.toml` pour les secrets :

```toml
[general]
model_path = "models/model_final.pkl"
```

---

## 8. Tests et validation

### Tests du dashboard

| Test | Méthode | Résultat attendu |
|---|---|---|
| Chargement de la page | Ouvrir le navigateur | Dashboard visible sans erreur |
| Formulaire de prédiction | Remplir et soumettre | Affichage d'une valeur numérique |
| Navigation entre pages | Cliquer sur les liens | Changement de page sans rechargement |
| Responsive | Redimensionner la fenêtre | Layout adapté |

### Tests de l'API de prédiction

```python
# test_api.py
from app.api_prediction import predict

def test_predict_retourne_dict():
    result = predict("lundi", 8, "haute_saison", False)
    assert isinstance(result, dict)
    assert "frequentation" in result
    assert result["frequentation"] > 0

def test_predict_jour_ferie():
    r_normal = predict("vendredi", 18, "haute_saison", False)
    r_ferie  = predict("vendredi", 18, "haute_saison", True)
    assert r_ferie["frequentation"] < r_normal["frequentation"]
```

---

## 9. Décisions techniques

### Pourquoi Streamlit ?

Streamlit a été choisi pour sa rapidité de développement, sa compatibilité native avec l'écosystème Python data science (Pandas, Plotly, Scikit-learn) et sa capacité à déployer facilement un dashboard sans connaissances en frontend (HTML/CSS/JS).

### Pourquoi Plotly ?

Plotly offre des graphiques interactifs (zoom, hover, téléchargement) sans configuration supplémentaire, ce qui enrichit l'expérience utilisateur lors de la démonstration.

### Pourquoi un mock de prédiction ?

Conformément au **principe d'indépendance** défini dans le plan de projet, le dashboard a été développé sans attendre que les modèles de Bara soient finalisés. Le mock respecte exactement le contrat d'interface défini, ce qui rend l'intégration finale triviale (remplacement d'une seule fonction).

### Séparation des responsabilités

Le dashboard ne contient **aucune logique ML**. Il délègue 100% des calculs à `api_prediction.py`. Cela facilite les tests, la maintenance et le remplacement futur du modèle.

---

## 10. Considérations éthiques

### Biais potentiels dans les données

Les données collectées peuvent refléter des inégalités d'accès au transport selon les zones géographiques. Les prédictions doivent être interprétées avec prudence et ne pas être utilisées pour réduire le service sur des lignes déjà sous-desservies.

### Confidentialité des données

Aucune donnée personnelle n'est collectée par ce dashboard. Les données de fréquentation sont des agrégats anonymisés.

### Usage responsable des prédictions

Les prédictions sont des **estimations statistiques** basées sur des données historiques. Elles ne tiennent pas compte d'événements imprévus (pannes, grèves, événements exceptionnels). Toute décision opérationnelle doit être validée par des experts du domaine.

### Transparence algorithmique

Les algorithmes utilisés (Random Forest, XGBoost) sont des modèles de type "boîte noire" relativement difficiles à interpréter. Pour une utilisation en production, il est recommandé d'intégrer des outils d'explicabilité comme **SHAP** ou **LIME**.

---

*Documentation rédigée par Joanelle — Développeur Interface*  
*Dernière mise à jour : Mars 2026*
