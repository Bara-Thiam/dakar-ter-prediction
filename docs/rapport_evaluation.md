# Rapport d'Évaluation des Modèles — TER Dakar

## Contexte

Ce rapport présente la comparaison de trois algorithmes de machine learning pour la prédiction de la fréquentation du TER Dakar. Les modèles ont été entraînés sur un dataset réel de **67 562 lignes** couvrant la période 2022-2026, à une granularité de **30 minutes** (sources : SETER, SENTER, CETUD, Banque Mondiale).

**Séparation des données :** 80% entraînement / 20% test  
**Validation :** Cross-validation à 5 folds

---

## Résultats

| Modèle | R² | MAE | RMSE | R² CV (mean) |
|---|---|---|---|---|
| Régression Linéaire | 0.1961 | 808 passagers | 991 passagers | — |
| Random Forest | 0.9685 → **0.9739** | 128 → **118 passagers** | 196 → **178 passagers** | 0.9726 |
| **XGBoost** | 0.9771 → **0.9781** | 112 → **109 passagers** | 167 → **163 passagers** | 0.9777 |

> Les flèches indiquent l'amélioration après optimisation des hyperparamètres.

---

## Analyse par modèle

### 1. Régression Linéaire Multiple
**R² = 0.20 — Performance insuffisante**

La régression linéaire n'explique que 20% de la variance de la fréquentation. Ce résultat est attendu : la relation entre les variables temporelles et la fréquentation n'est pas linéaire. Un lundi à 8h n'est pas simplement la somme de ses caractéristiques — c'est une combinaison complexe d'effets qui interagissent. La régression linéaire ne peut pas capturer ces interactions.

Son rôle dans ce projet est celui d'une **baseline** permettant de mesurer l'apport réel des modèles plus sophistiqués.

### 2. Random Forest
**R² = 0.9739 — Très bonne performance**

Le Random Forest divise l'erreur moyenne par 7 par rapport à la régression linéaire (MAE : 118 vs 808). Son R² CV de 0.9726 avec une très faible variance confirme qu'il **généralise très bien** sur des données non vues — il ne performe pas bien par chance.

### 3. XGBoost
**R² = 0.9781 — Meilleure performance globale**

XGBoost est le modèle retenu pour la production. Avec une MAE de **109 passagers par tranche de 30 minutes**, il prédit la fréquentation avec une précision remarquable. Sa cross-validation à 0.9777 confirme une excellente stabilité.

---

## Importance des variables

### Random Forest
| Variable | Importance |
|---|---|
| heure | 74.6% |
| est_weekend | 9.9% |
| est_vacances_scolaires | 3.8% |
| minute | 3.0% |
| evenement_special | 2.4% |
| phase_reseau | 1.4% |
| autres | 5.0% |

### XGBoost
| Variable | Importance |
|---|---|
| heure | 30.9% |
| est_weekend | 18.4% |
| evenement_special | 8.5% |
| est_vacances_scolaires | 7.2% |
| phase_reseau | 6.5% |
| est_saison_pluies | 5.1% |
| autres | 23.4% |

**Observations clés :**
- L'heure reste la variable dominante dans les deux modèles
- XGBoost distribue l'importance plus équitablement — il exploite mieux les interactions entre variables contextuelles (événements, perturbations, phase réseau)
- `phase_reseau` et `evenement_special` ont un impact significatif chez XGBoost, ce qui est cohérent avec l'ouverture de la Phase 2 AIBD et les JOJ 2026

---

## Exemples de prédictions (Lundi, janvier 2025)

| Heure | Fréquentation prédite | Intervalle |
|---|---|---|
| 5h00 | 630 passagers | [521 — 739] |
| 8h00 (pic matin) | 4 374 passagers | [4 265 — 4 483] |
| 14h00 (creux) | 1 301 passagers | [1 192 — 1 410] |
| 18h00 (pic soir) | 4 272 passagers | [4 163 — 4 381] |
| 23h00 | 270 passagers | [161 — 379] |

### Impact des événements sur le pic du matin (8h00)
| Scénario | Fréquentation prédite |
|---|---|
| Jour normal | 4 374 passagers |
| Panne technique | 3 686 passagers (-16%) |
| Magal Touba | 5 001 passagers (+14%) |

---

## Métriques — Définitions

- **R²** : proportion de la variance expliquée par le modèle. 1.0 = parfait, 0 = inutile.
- **MAE** (Mean Absolute Error) : erreur moyenne en valeur absolue, en nombre de passagers.
- **RMSE** (Root Mean Squared Error) : similaire au MAE mais pénalise davantage les grandes erreurs.
- **R² CV** : R² moyen sur 5 folds de cross-validation — mesure la robustesse du modèle.

---

## Conclusion

XGBoost est sélectionné comme modèle final avec un **R² de 0.9781** et une erreur moyenne de **109 passagers par tranche de 30 minutes**. Ce résultat est obtenu sur un dataset réel de 67 562 observations couvrant 5 ans de données TER Dakar.

**Modèle final sauvegardé :** `models/model_final.pkl`  
**Graphique comparatif :** `visualisations/comparaison_modeles.png`