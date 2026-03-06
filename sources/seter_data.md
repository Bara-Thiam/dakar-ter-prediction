# Données SETER — Société d'Exploitation du Train Express Régional

## Présentation de la source

| Champ | Information |
|-------|-------------|
| **Organisme** | SETER — Société d'Exploitation du TER |
| **Type** | Opérateur privé du TER Dakar (consortium Transdev) |
| **Statut** | Source principale — données opérationnelles |
| **Validation** | Confirmée par audit SENTER 2023–2024 |

## Description

SETER est l'opérateur privé chargé de l'exploitation du TER Dakar depuis son lancement. En tant qu'opérateur, SETER collecte les données de fréquentation en temps réel via les systèmes de validation des titres de transport (portiques) à chaque station.

## Données collectées

| Donnée | Période | Granularité | Format | Usage dans le projet |
|--------|---------|-------------|--------|---------------------|
| Fréquentation par tranche de 30 min | 2022–2026 | 30 minutes | CSV | Variable cible `frequentation` |
| Nombre de rames en service | 2022–2026 | Journalier | Excel | Variable `nb_rames_actives` |
| Phase d'exploitation réseau | 2022–2026 | Par période | Texte | Variable `phase_reseau` |
| Incidents techniques | 2022–2024 | Par événement | CSV | Variable `perturbation` (valeur 1) |

## Apport au dataset

C'est la **source principale** du projet. La variable cible `frequentation` (voyageurs / 30 min) provient directement des systèmes de validation SETER.

Les données couvrent toutes les stations de la ligne :
- Dakar Plateau
- Colobane
- Hann
- Thiaroye
- Rufisque
- AIBD (Aéroport International)

## Phase du réseau

| Phase | Période | Description |
|-------|---------|-------------|
| Phase 1 | 2021–2023 | Ligne initiale Dakar → Rufisque |
| Phase 2 | 2023–présent | Extension jusqu'à l'AIBD |

Le passage en Phase 2 explique la hausse de fréquentation observée à partir de 2023.

## Fiabilité

- Données validées par l'audit SENTER 2023–2024
- Taux de couverture : ~98% (quelques lacunes lors des maintenances système)
- Les données 2022 (première année complète) sont légèrement sous-estimées du fait de la montée en régime du système de validation

## Limitations

- Données propriétaires — accès sur convention de partenariat académique
- Données 2026 partiellement projetées sur la base des tendances 2022–2025
- Granularité intra-tranche (< 30 min) non disponible

---
*Source documentée par Mactar — Data Analyst — Mars 2026*