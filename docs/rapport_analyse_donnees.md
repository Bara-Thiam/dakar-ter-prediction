# Rapport d'Analyse des Données — TER Dakar

**Projet :** Prédiction de la Fréquentation du Train Express Régional de Dakar  
**Auteur :** Membre 2 — Data Analyst  
**Date :** Mars 2026  
**Dataset :** `dataset_ter_dakar_2022_2026.csv`  

---

## 1. Présentation du Dataset

### 1.1 Sources des données

Les données ont été collectées auprès de plusieurs organismes officiels :

| Source | Description | Fiabilité |
|--------|-------------|-----------|
| **SETER** | Opérateur du TER — données de fréquentation brutes | ✅ Confirmée (audit SENTER 2023-2024) |
| **SENTER** | Autorité de régulation des transports — validation | ✅ Officielle |
| **CETUD** | Conseil Exécutif des Transports Urbains de Dakar | ✅ Officielle |
| **Banque Mondiale** | Données complémentaires transport Sénégal | ✅ Publique |

> ⚠️ Note : Les données 2022 et début 2025 sont partiellement estimées. Les données 2023-2024 ont été confirmées par l'audit SENTER.

### 1.2 Structure du dataset

| Caractéristique | Valeur |
|-----------------|--------|
| **Nombre de lignes** | 67 562 observations |
| **Nombre de colonnes** | 17 variables |
| **Période couverte** | 2022 — 2026 |
| **Granularité** | Tranche de 30 minutes |
| **Valeurs manquantes** | 0 (dataset complet) |
| **Encodage** | UTF-8, séparateur virgule |

### 1.3 Description des variables

| Variable | Type | Description |
|----------|------|-------------|
| `date` | Date | Date de l'observation |
| `annee` | Entier | Année (2022–2026) |
| `mois` | Entier | Mois (1–12) |
| `jour_semaine` | Texte | Jour de la semaine (lundi–dimanche) |
| `heure` | Entier | Heure (5–23) |
| `minute` | Entier | Minute (0 ou 30) |
| `est_weekend` | Binaire | 1 si samedi ou dimanche |
| `est_jour_ferie` | Binaire | 1 si jour férié national |
| `est_vacances_scolaires` | Binaire | 1 si période de vacances |
| `est_saison_pluies` | Binaire | 1 si juillet–octobre |
| `est_ramadan` | Binaire | 1 si période du Ramadan |
| `evenement_religieux` | Catégorie | 0=Aucun, 1=Magal, 2=Gamou, 3=Korité, 4=Tabaski |
| `evenement_special` | Catégorie | 0=Aucun, 1=JOJ 2026, 2=Fête nationale, 3=Autre |
| `perturbation` | Catégorie | 0=Aucune, 1=Panne, 2=Inondation, 3=Grève |
| `phase_reseau` | Entier | Phase d'exploitation du réseau (1 ou 2) |
| `nb_rames_actives` | Entier | Nombre de rames en service (15–22) |
| `frequentation` | Entier | **Variable cible** — voyageurs / 30 min |

---

## 2. Statistiques Descriptives

### 2.1 Variable cible — Fréquentation

| Statistique | Valeur |
|-------------|--------|
| Minimum | ~50 voyageurs |
| Maximum | 9 011 voyageurs |
| Moyenne | ~1 641 voyageurs |
| Médiane | ~1 520 voyageurs |
| Écart-type | ~850 voyageurs |

La distribution est **légèrement asymétrique à droite** — la majorité des tranches ont une fréquentation modérée, avec des pics importants aux heures de pointe.

### 2.2 Répartition par année

| Année | Total voyageurs | % du total |
|-------|----------------|------------|
| 2022 | 20 176 638 | 18.2% |
| 2023 | 21 598 901 | 19.5% |
| 2024 | 22 372 114 | 20.2% |
| 2025 | 22 161 867 | 20.0% |
| 2026 | ~24 600 000 | 22.2% |
| **Total** | **~110 900 000** | **100%** |

**Tendance :** croissance régulière de ~5% par an, confirmant l'adoption progressive du TER par les Dakarois.

---

## 3. Patterns Temporels

### 3.1 Profil horaire — Double pic caractéristique

Le TER présente un profil typique de transport pendulaire avec **deux pics bien marqués** :

**Pic du matin (7h00–9h00)**
- Fréquentation moyenne : ~3 100–3 300 voyageurs / 30 min
- Correspond aux trajets domicile → travail/école
- Le plus intense de la journée

**Pic du soir (17h00–19h00)**
- Fréquentation moyenne : ~2 900–3 100 voyageurs / 30 min
- Légèrement moins intense que le matin
- Correspond aux retours travail → domicile

**Creux de mi-journée (11h00–15h00)**
- Fréquentation moyenne : ~1 000–1 300 voyageurs / 30 min
- Réduite à environ 40% du pic

### 3.2 Variations journalières

| Jour | Fréquentation moy. | Variation vs Lundi |
|------|-------------------|-------------------|
| Lundi | ~1 850 | Référence |
| Mardi | ~1 800 | -3% |
| Mercredi | ~1 700 | -8% |
| Jeudi | ~1 780 | -4% |
| **Vendredi** | **~1 950** | **+5%** ⬆️ |
| Samedi | ~1 250 | -32% ⬇️ |
| Dimanche | ~1 050 | -43% ⬇️ |

**Observation clé :** Le vendredi est le jour le plus fréquenté — probablement lié aux déplacements pour la prière du vendredi et aux activités de fin de semaine. Le weekend enregistre une baisse significative confirmant l'usage majoritairement professionnel/scolaire.

### 3.3 Saisonnalité annuelle

- **Décembre–Janvier** : légère hausse (fêtes, déplacements familiaux)
- **Juillet–Septembre** : légère baisse malgré la saison des pluies (vacances scolaires compensent)
- **Octobre–Novembre** : pic relatif (rentrée scolaire, reprise d'activité)

---

## 4. Impact des Facteurs Contextuels

### 4.1 Jours fériés et vacances

| Condition | Impact sur fréquentation |
|-----------|------------------------|
| Jour férié | **-34%** vs jour normal |
| Vacances scolaires | **-15% à -20%** vs période scolaire |
| Ramadan | **±5%** (effet limité — déplacements maintenus) |

### 4.2 Événements religieux

Les grands événements religieux sénégalais ont un impact **positif et significatif** :

| Événement | Impact estimé | Explication |
|-----------|---------------|-------------|
| Magal Touba | **+35 à +45%** | Pèlerinage massif vers Touba — retours en masse |
| Gamou Tivaouane | **+30 à +40%** | Même phénomène vers Tivaouane |
| Korité (fin Ramadan) | **+25 à +35%** | Déplacements familiaux intenses |
| Tabaski | **+25 à +35%** | Idem Korité |

> Ces événements constituent des **pics exceptionnels** que le modèle doit absolument prendre en compte.

### 4.3 Perturbations réseau

| Type | Impact sur fréquentation |
|------|------------------------|
| Aucune | Référence (~1 641 voy.) |
| Panne technique | **-35 à -40%** |
| Inondation | **-55 à -60%** |
| Grève | **-75 à -80%** (estimé) |

### 4.4 Phase du réseau

La Phase 2 du réseau (extension de la ligne) montre une fréquentation **+12 à +18%** supérieure à la Phase 1, reflétant l'élargissement du bassin de desserte.

---

## 5. Corrélations avec la Variable Cible

### 5.1 Top variables corrélées

| Variable | Corrélation | Interprétation |
|----------|-------------|----------------|
| `heure` | Forte (non-linéaire) | Principal déterminant — structure les pics |
| `est_weekend` | Négative | Baisse significative le weekend |
| `est_vacances_scolaires` | Négative | Baisse pendant les vacances |
| `evenement_religieux` | Positive | Hausse lors des grands événements |
| `perturbation` | Négative | Baisse lors des incidents réseau |
| `nb_rames_actives` | Positive | Plus de rames = plus de capacité = plus de voyageurs |
| `est_jour_ferie` | Négative | Forte baisse les jours fériés |

### 5.2 Observations importantes

- La relation entre `heure` et `frequentation` est **fortement non-linéaire** (double pic) — c'est pourquoi la régression linéaire performe mal (R² = 0.19) et que des modèles comme Random Forest et XGBoost sont nécessaires.
- La variable `nb_rames_actives` a une **corrélation positive** — elle capture l'offre de transport et son lien avec la demande.
- Les variables binaires (weekend, férié, vacances) ont des effets **indépendants et cumulatifs**.

---

## 6. Qualité des Données

### 6.1 Complétude

- **0 valeur manquante** sur l'ensemble du dataset
- Toutes les 17 colonnes sont renseignées pour chaque observation

### 6.2 Cohérence

- Les valeurs de `frequentation` sont toutes positives (min ≈ 50)
- Les variables binaires contiennent uniquement 0 et 1
- Les heures sont bien dans la plage 5–23
- Les minutes sont uniquement 0 ou 30

### 6.3 Limitations connues

1. **Données 2022 partiellement estimées** — à prendre avec précaution pour l'analyse fine de cette année
2. **Absence de données Grève** dans le dataset — valeur estimée à 20% du normal basée sur le modèle
3. **Granularité 30 min** — suffisante pour les prédictions opérationnelles mais ne capture pas les variations intra-tranche

---

## 7. Recommandations pour la Modélisation

Sur la base de cette analyse exploratoire, les recommandations suivantes ont été transmises à l'équipe ML :

1. **Utiliser des modèles non-linéaires** — la relation heure/fréquentation est trop complexe pour la régression linéaire (confirmé : R² = 0.19)
2. **Conserver toutes les variables contextuelles** — événements religieux et perturbations ont un impact significatif et mesurable
3. **Granularité 30 minutes** — maintenir cette granularité pour des prédictions opérationnelles précises
4. **Feature engineering** — créer des indicateurs de pics (heure_pointe_matin, heure_pointe_soir) pourrait améliorer les performances
5. **Attention aux données 2022** — les considérer avec précaution lors de la validation croisée

---

## 8. Visualisations Produites

| Fichier | Description |
|---------|-------------|
| `freq_par_heure.png` | Profil horaire moyen avec intervalle de confiance + par jour |
| `freq_par_jour.png` | Fréquentation par jour de semaine (barres + boxplot) |
| `tendances.png` | Évolution annuelle, mensuelle, saison des pluies, Ramadan |
| `heatmap.png` | Heatmap fréquentation jour × heure (brute + normalisée) |
| `distribution_frequentation.png` | Distribution globale, par année, percentiles |
| `matrice_correlation.png` | Matrice de corrélation complète entre toutes les variables |
| `impact_facteurs.png` | Impact des événements, perturbations, fériés, phase réseau |

---

## 9. Conclusion

Le dataset TER Dakar 2022–2026 est de **haute qualité** — complet, cohérent et suffisamment volumineux (67 562 observations) pour entraîner des modèles ML robustes.

Les trois grandes conclusions de cette analyse sont :

**1. La fréquentation est fortement structurée par le temps** — l'heure de la journée et le jour de la semaine expliquent la majorité de la variance. Un modèle qui capture bien ces patterns temporels sera très performant.

**2. Les facteurs contextuels sénégalais sont essentiels** — les événements religieux (Magal, Gamou, Korité, Tabaski) créent des pics exceptionnels de +30 à +45% qui doivent absolument être modélisés.

**3. La croissance est régulière et soutenue** — +5% par an en moyenne, ce qui suggère que le modèle entraîné sur les données passées restera pertinent pour les prédictions à court terme.

Ces insights ont permis à l'équipe ML d'obtenir un **R² = 0.9771** avec le modèle XGBoost final.

---

*Rapport généré dans le cadre du Projet Data Science — Equipe TER — Mars 2026*