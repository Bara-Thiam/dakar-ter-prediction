import pandas as pd
import numpy as np
import joblib
import os

# Chargement du modèle final
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'model_final.pkl')
modele = joblib.load(MODEL_PATH)

JOURS_SEMAINE = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

def predict(
    jour_semaine: str,
    annee: int,
    mois: int,
    heure: int,
    minute: int = 0,
    est_jour_ferie: int = 0,
    est_vacances_scolaires: int = 0,
    est_saison_pluies: int = 0,
    est_ramadan: int = 0,
    evenement_religieux: int = 0,
    evenement_special: int = 0,
    perturbation: int = 0,
    phase_reseau: int = 1,
    nb_rames_actives: int = 22
) -> dict:
    """
    Prédit la fréquentation du TER Dakar sur une tranche de 30 minutes.

    Paramètres obligatoires :
    - jour_semaine     : 'lundi' ... 'dimanche'
    - annee            : ex 2025
    - mois             : 1 à 12
    - heure            : 5 à 23
    - minute           : 0 ou 30

    Paramètres optionnels (défaut = situation normale) :
    - est_jour_ferie         : 0 ou 1
    - est_vacances_scolaires : 0 ou 1
    - est_saison_pluies      : 0 ou 1
    - est_ramadan            : 0 ou 1
    - evenement_religieux    : 0=aucun, 1=Magal, 2=Gamou, 3=Korité, 4=Tabaski
    - evenement_special      : 0=aucun, 1=JOJ, 2=fête nationale, 3=autre
    - perturbation           : 0=aucune, 1=panne, 2=inondation, 3=grève
    - phase_reseau           : 1 ou 2
    - nb_rames_actives       : entier (15 à 22)

    Retourne un dict avec frequentation prédite et intervalle de confiance.
    """

    # Validations
    assert jour_semaine in JOURS_SEMAINE, f"jour_semaine invalide : {jour_semaine}"
    assert 1 <= mois <= 12, f"mois invalide : {mois}"
    assert 5 <= heure <= 23, f"heure invalide : {heure}"
    assert minute in [0, 30], f"minute invalide : {minute} (0 ou 30)"
    assert perturbation in [0, 1, 2, 3], "perturbation invalide"

    est_weekend = 1 if jour_semaine in ['samedi', 'dimanche'] else 0

    X = pd.DataFrame([{
        'annee':                  annee,
        'mois':                   mois,
        'jour_semaine':           jour_semaine,
        'heure':                  heure,
        'minute':                 minute,
        'est_weekend':            est_weekend,
        'est_jour_ferie':         est_jour_ferie,
        'est_vacances_scolaires': est_vacances_scolaires,
        'est_saison_pluies':      est_saison_pluies,
        'est_ramadan':            est_ramadan,
        'evenement_religieux':    evenement_religieux,
        'evenement_special':      evenement_special,
        'perturbation':           perturbation,
        'phase_reseau':           phase_reseau,
        'nb_rames_actives':       nb_rames_actives,
    }])

    prediction = int(modele.predict(X)[0])

    # Intervalle de confiance basé sur le MAE du modèle final
    MAE = 109
    borne_basse = max(0, prediction - MAE)
    borne_haute = prediction + MAE

    return {
        'frequentation': prediction,
        'intervalle':    (borne_basse, borne_haute),
        'parametres':    X.to_dict(orient='records')[0]
    }


def predict_journee(
    jour_semaine: str,
    annee: int,
    mois: int,
    est_jour_ferie: int = 0,
    est_vacances_scolaires: int = 0,
    est_saison_pluies: int = 0,
    est_ramadan: int = 0,
    evenement_religieux: int = 0,
    evenement_special: int = 0,
    perturbation: int = 0,
    phase_reseau: int = 1,
    nb_rames_actives: int = 22
) -> pd.DataFrame:
    """
    Prédit la fréquentation pour toutes les tranches de 30 min d'une journée.
    Retourne un DataFrame avec 38 lignes (19 heures × 2 tranches).
    """
    resultats = []
    for heure in range(5, 24):
        for minute in [0, 30]:
            res = predict(
                jour_semaine, annee, mois, heure, minute,
                est_jour_ferie, est_vacances_scolaires,
                est_saison_pluies, est_ramadan,
                evenement_religieux, evenement_special,
                perturbation, phase_reseau, nb_rames_actives
            )
            resultats.append({
                'heure':         f"{heure}h{minute:02d}",
                'frequentation': res['frequentation'],
                'borne_basse':   res['intervalle'][0],
                'borne_haute':   res['intervalle'][1],
            })
    return pd.DataFrame(resultats)


# --- Test rapide ---
if __name__ == '__main__':
    print("=== Test prédiction unique ===")
    res = predict('lundi', annee=2025, mois=1, heure=8, minute=0)
    print(f"Lundi, janvier 2025, 8h00 → {res['frequentation']:,} passagers")
    print(f"Intervalle : [{res['intervalle'][0]:,} — {res['intervalle'][1]:,}]")

    print("\n=== Test journée complète — Lundi janvier 2025 ===")
    df = predict_journee('lundi', annee=2025, mois=1)
    print(df.to_string(index=False))

    print("\n=== Test avec perturbation (panne technique) ===")
    res_panne = predict('lundi', annee=2025, mois=1, heure=8, minute=0, perturbation=1)
    print(f"Lundi 8h00 avec panne → {res_panne['frequentation']:,} passagers")

    print("\n=== Test Magal Touba ===")
    res_magal = predict('lundi', annee=2025, mois=9, heure=8, minute=0, evenement_religieux=1)
    print(f"Lundi 8h00 Magal → {res_magal['frequentation']:,} passagers")