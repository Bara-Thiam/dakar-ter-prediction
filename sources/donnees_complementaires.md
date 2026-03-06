# Données Complémentaires — Événements, Météo et Contexte

## Présentation

Ce fichier documente les sources complémentaires utilisées pour enrichir le dataset principal avec des variables contextuelles (événements religieux, météo, calendriers spéciaux).

---

## 1. Événements Religieux

### Source
- **Organisme :** Grande Mosquée de Dakar, médias sénégalais (RFM, 7TV, APS)
- **Type :** Données publiques — calendrier annoncé officiellement

### Événements couverts

| Code | Événement | Description | Impact fréquentation |
|------|-----------|-------------|---------------------|
| 1 | Magal Touba | Grand pèlerinage annuel à Touba | **+35 à +45%** |
| 2 | Gamou Tivaouane | Nuit du Prophète à Tivaouane | **+30 à +40%** |
| 3 | Korité | Fête de fin du Ramadan | **+25 à +35%** |
| 4 | Tabaski | Fête du Mouton | **+25 à +35%** |

### Méthode de collecte
Les dates exactes ont été récupérées via les annonces officielles et les archives de presse sénégalaise pour chaque année 2022–2026.

---

## 2. Saison des Pluies

### Source
- **Organisme :** ANACIM — Agence Nationale de l'Aviation Civile et de la Météorologie
- **Site :** https://www.anacim.sn

### Définition adoptée
La saison des pluies au Sénégal couvre généralement **juillet à octobre**. La variable `est_saison_pluies = 1` est appliquée sur cette période.

### Impact observé
Les inondations pendant la saison des pluies perturbent les accès aux stations et peuvent réduire la fréquentation. L'effet est capturé conjointement par `est_saison_pluies` et `perturbation = 2` (inondation).

---

## 3. Ramadan

### Source
- **Organisme :** Gouvernement du Sénégal — Journal Officiel
- **Type :** Données publiques officielles

### Définition adoptée
Les dates du Ramadan sont celles officiellement retenues par le gouvernement sénégalais chaque année. La variable `est_ramadan = 1` couvre toute la période du Ramadan.

### Impact observé
Impact limité sur la fréquentation globale (±5%) — les déplacements sont maintenus mais décalés vers des horaires atypiques (très tôt le matin, après la rupture du jeûne).

---

## 4. Événements Spéciaux

| Code | Événement | Période | Impact estimé |
|------|-----------|---------|---------------|
| 1 | JOJ Dakar 2026 | Octobre–Novembre 2026 | +20 à +30% |
| 2 | Fête nationale (4 Avril) | 4 avril chaque année | Variable |
| 3 | Autres événements | Ponctuels | Variable |

### JOJ 2026
Les Jeux Olympiques de la Jeunesse de Dakar 2026 constituent un événement majeur prévu. Les données 2026 intègrent une estimation d'augmentation de trafic sur la période des jeux, le TER étant un axe de transport principal vers les sites sportifs.

---

## 5. Perturbations Réseau

### Sources
- Rapports d'incidents SETER (pannes techniques)
- Archives météo ANACIM (inondations)
- Archives presse (grèves — APS, Seneweb)

### Codification

| Code | Type | Source principale |
|------|------|------------------|
| 0 | Aucune perturbation | — |
| 1 | Panne technique | Rapports SETER |
| 2 | Inondation | ANACIM + presse |
| 3 | Grève | Archives presse |

> ⚠️ Les grèves (code 3) sont absentes du dataset réel — données insuffisantes. Valeur estimée à 20% du normal dans le dashboard.

---

## 6. Données Économiques et Démographiques

### Source
- **Organisme :** Banque Mondiale, ANSD (Agence Nationale de Statistique et de la Démographie)
- **Usage :** Contexte général pour la présentation — non intégrées directement dans le modèle

### Chiffres clés retenus
- Population Dakar 2024 : ~3,9 millions d'habitants
- Taux de motorisation faible → dépendance aux transports en commun
- Croissance population Dakar : +3% / an

---
*Source documentée par Mactar — Data Analyst — Mars 2026*