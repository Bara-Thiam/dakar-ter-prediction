# Rapport d'Évaluation des Modèles — TER Dakar

## Contexte

Ce rapport présente la comparaison de trois algorithmes de machine learning pour la prédiction de la fréquentation du TER Dakar. Les modèles ont été entraînés sur un dataset simulé de **6 954 lignes** couvrant l'année 2024 (19 tranches horaires × 366 jours).

**Séparation des données :** 80% entraînement / 20% test  
**Validation :** Cross-validation à 5 folds

---

## Résultats

| Modèle | R² | MAE | RMSE | R² CV (mean) | R² CV (std) |
|---|---|---|---|---|---|
| Régression Linéaire | 0.2151 | 26 291 | 31 612 | 0.1695 | 0.0458 |
| Random Forest | 0.9172 | 7 186 | 10 269 | 0.9079 | 0.0115 |
| **XGBoost** | **0.9243** | **6 891** | **9 819** | **0.9153** | **0.0120** |

---

## Analyse par modèle

### 1. Régression Linéaire Multiple
**R² = 0.21 — Performance insuffisante**

La régression linéaire n'explique que 21% de la variance de la fréquentation. Ce résultat est attendu : la relation entre les variables temporelles et la fréquentation n'est pas linéaire. Un lundi à 8h n'est pas simplement "la somme" de ses caractéristiques — c'est une combinaison complexe d'effets qui interagissent entre eux. La régression linéaire ne peut pas capturer ces interactions.

Son rôle dans ce projet est celui d'une **baseline** permettant de mesurer l'apport réel des modèles plus sophistiqués.

### 2. Random Forest
**R² = 0.92 — Très bonne performance**

Le Random Forest divise l'erreur moyenne par presque 4 par rapport à la régression linéaire (MAE : 7 186 vs 26 291). Son R² CV de 0.91 avec un écart type de 0.012 confirme qu'il est **stable et robuste** — il ne performe pas bien par chance mais généralise correctement sur des données non vues.

### 3. XGBoost
**R² = 0.92 — Meilleure performance globale**

XGBoost est légèrement supérieur au Random Forest sur les trois métriques. Son MAE de 6 891 passagers et son RMSE de 9 819 en font le **modèle retenu pour la production**. Comme le Random Forest, sa cross-validation confirme une très bonne stabilité (std = 0.012).

---

## Importance des variables

### Random Forest
| Variable | Importance |
|---|---|
| heure | 67.3% |
| est_weekend | 13.9% |
| est_vacances_scolaires | 11.7% |
| est_jour_ferie | 2.6% |
| mois | 2.1% |
| jour_semaine | 2.4% |

### XGBoost
| Variable | Importance |
|---|---|
| est_weekend | 34.0% |
| heure | 27.6% |
| est_vacances_scolaires | 18.2% |
| jour_semaine (samedi) | 6.8% |
| est_jour_ferie | 6.7% |
| mois | 1.7% |

**Observation clé :** Les deux modèles s'accordent sur les trois variables les plus importantes — `heure`, `est_weekend` et `est_vacances_scolaires`. XGBoost distribue l'importance plus équitablement entre les variables, ce qui suggère qu'il exploite mieux les interactions entre elles.

---

## Métriques — Définitions

- **R²** : proportion de la variance expliquée par le modèle. 1.0 = parfait, 0 = inutile.
- **MAE** (Mean Absolute Error) : erreur moyenne en valeur absolue, en nombre de passagers.
- **RMSE** (Root Mean Squared Error) : similaire au MAE mais pénalise davantage les grandes erreurs.
- **R² CV** : R² moyen sur 5 folds de cross-validation — mesure la stabilité du modèle.

---

## Conclusion

XGBoost est sélectionné comme modèle final avec un R² de 0.924 et une erreur moyenne de 6 891 passagers. Ce modèle sera réentraîné sur le dataset réel fourni par le Data Analyst avant la présentation finale.

**Modèle final sauvegardé :** `models/xgboost.pkl`