# Schéma du Dataset Commun — TER Dakar

## Colonnes

| Colonne                | Type    | Format / Valeurs possibles                                        | Exemple    |
|------------------------|---------|-------------------------------------------------------------------|------------|
| date                   | string  | YYYY-MM-DD                                                        | 2024-01-15 |
| jour_semaine           | string  | lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche         | lundi      |
| mois                   | integer | 1 à 12                                                            | 1          |
| heure                  | integer | 5 à 23 (tranches horaires de service)                             | 8          |
| est_jour_ferie         | integer | 0 = non, 1 = oui                                                  | 0          |
| est_weekend            | integer | 0 = non, 1 = oui                                                  | 0          |
| est_vacances_scolaires | integer | 0 = non, 1 = oui                                                  | 0          |
| frequentation          | integer | nombre de passagers (variable cible)                              | 127350     |

## Règles métier

- Les heures de service vont de **5h à 23h** (19 tranches horaires par jour)
- Les heures de pointe sont **7h-9h** et **17h-20h** (fréquentation élevée)
- Le weekend a une fréquentation globalement plus basse
- Les jours fériés se comportent comme des dimanches
- Les vacances scolaires au Sénégal réduisent significativement la fréquentation aux heures de pointe
  - Grandes vacances : juillet - septembre
  - Vacances de Tabaski / Korité : variables selon le calendrier lunaire (prévoir ~1 semaine)
  - Vacances de février : 2 semaines en février

## Fichier de référence

- Séparateur : virgule (`,`)
- Encodage : UTF-8
- Header : oui (première ligne)