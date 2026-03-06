# Données CETUD — Conseil Exécutif des Transports Urbains de Dakar

## Présentation de la source

| Champ | Information |
|-------|-------------|
| **Organisme** | CETUD — Conseil Exécutif des Transports Urbains de Dakar |
| **Type** | Autorité publique de régulation des transports urbains |
| **Site** | https://www.cetud.sn |
| **Statut** | Source officielle — données publiques |

## Description

Le CETUD est l'autorité sénégalaise chargée de l'organisation et de la régulation des transports urbains dans la région de Dakar. Il supervise l'ensemble des modes de transport urbain incluant le TER, les bus Dakar Dem Dikk, les taxis et les cars rapides.

## Données collectées

| Donnée | Période | Format | Usage dans le projet |
|--------|---------|--------|---------------------|
| Statistiques de fréquentation annuelles TER | 2022–2024 | PDF / Excel | Validation des totaux annuels |
| Calendrier des jours fériés nationaux | 2022–2026 | PDF | Variable `est_jour_ferie` |
| Calendrier scolaire officiel | 2022–2026 | PDF | Variable `est_vacances_scolaires` |
| Incidents et perturbations réseau | 2022–2024 | Rapport PDF | Variable `perturbation` |

## Apport au dataset

- **Jours fériés** : liste complète des jours fériés nationaux sénégalais 2022–2026
- **Vacances scolaires** : calendrier officiel académie de Dakar
- **Validation** : comparaison des totaux annuels générés vs statistiques officielles CETUD

## Limitations

- Les rapports CETUD sont publiés avec 6 à 12 mois de décalage
- Données 2025–2026 partiellement estimées sur la base des tendances 2022–2024
- Granularité horaire non disponible publiquement — fournie par SETER

## Accès

Les rapports annuels du CETUD sont disponibles sur demande auprès de l'organisme ou via leur site officiel. Certains rapports sont accessibles via la Banque Mondiale (transport Sénégal).

---
*Source documentée par Mactar — Data Analyst — Mars 2026*