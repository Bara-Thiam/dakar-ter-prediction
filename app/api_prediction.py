import pandas as pd
import numpy as np
import joblib
import os

# Chargement du modèle final
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'model_final.pkl')
modele = joblib.load(MODEL_PATH)

JOURS_SEMAINE = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

def predict(jour_semaine: str, mois: int, heure: int,
            est_jour_ferie: int = 0,
            est_vacances_scolaires: int = 0) -> dict:
    """
    Prédit la fréquentation du TER Dakar.

    Paramètres :
    - jour_semaine         : 'lundi', 'mardi', ..., 'dimanche'
    - mois                 : entier 1 à 12
    - heure                : entier 5 à 23
    - est_jour_ferie       : 0 ou 1
    - est_vacances_scolaires : 0 ou 1

    Retourne :
    - dict avec 'frequentation' (int) et 'intervalle' (tuple)
    """

    # Validation des entrées
    assert jour_semaine in JOURS_SEMAINE, f"jour_semaine invalide : {jour_semaine}"
    assert 1 <= mois <= 12, f"mois invalide : {mois}"
    assert 5 <= heure <= 23, f"heure invalide : {heure}"
    assert est_jour_ferie in [0, 1], "est_jour_ferie doit être 0 ou 1"
    assert est_vacances_scolaires in [0, 1], "est_vacances_scolaires doit être 0 ou 1"

    est_weekend = 1 if jour_semaine in ['samedi', 'dimanche'] else 0

    X = pd.DataFrame([{
        'jour_semaine':           jour_semaine,
        'mois':                   mois,
        'heure':                  heure,
        'est_jour_ferie':         est_jour_ferie,
        'est_weekend':            est_weekend,
        'est_vacances_scolaires': est_vacances_scolaires,
    }])

    prediction = int(modele.predict(X)[0])

    # Intervalle de confiance approximatif (± MAE du modèle)
    MAE = 6953
    borne_basse = max(0, prediction - MAE)
    borne_haute = prediction + MAE

    return {
        'frequentation': prediction,
        'intervalle':    (borne_basse, borne_haute),
        'parametres':    X.to_dict(orient='records')[0]
    }

def predict_journee(jour_semaine: str, mois: int,
                    est_jour_ferie: int = 0,
                    est_vacances_scolaires: int = 0) -> pd.DataFrame:
    """
    Prédit la fréquentation pour toutes les heures de service d'une journée.
    Retourne un DataFrame avec une ligne par heure.
    """
    resultats = []
    for heure in range(5, 24):
        res = predict(jour_semaine, mois, heure, est_jour_ferie, est_vacances_scolaires)
        resultats.append({
            'heure':         heure,
            'frequentation': res['frequentation'],
            'borne_basse':   res['intervalle'][0],
            'borne_haute':   res['intervalle'][1],
        })
    return pd.DataFrame(resultats)


# --- Test rapide ---
if __name__ == '__main__':
    print("=== Test prédiction unique ===")
    res = predict('lundi', mois=1, heure=8)
    print(f"Lundi, janvier, 8h → {res['frequentation']:,} passagers")
    print(f"Intervalle : [{res['intervalle'][0]:,} — {res['intervalle'][1]:,}]")

    print("\n=== Test journée complète ===")
    df = predict_journee('lundi', mois=1)
    print(df.to_string(index=False))