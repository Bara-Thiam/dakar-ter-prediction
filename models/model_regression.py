import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def charger_donnees(chemin='data/dataset_ter_dakar_2022_2026.csv'):
    df = pd.read_csv(chemin)
    X = df.drop(columns=['frequentation', 'date'])
    y = df['frequentation']
    return X, y

def construire_pipeline():
    cat_features = ['jour_semaine']
    num_features = [
        'annee', 'mois', 'heure', 'minute',
        'est_weekend', 'est_jour_ferie', 'est_vacances_scolaires',
        'est_saison_pluies', 'est_ramadan', 'evenement_religieux',
        'evenement_special', 'perturbation', 'phase_reseau', 'nb_rames_actives'
    ]

    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features),
        ('num', 'passthrough', num_features)
    ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])
    return pipeline

def entrainer_et_evaluer(chemin='data/dataset_ter_dakar_2022_2026.csv'):
    X, y = charger_donnees(chemin)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = construire_pipeline()
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("=" * 40)
    print("    RÉGRESSION LINÉAIRE MULTIPLE")
    print("=" * 40)
    print(f"  R²   : {r2:.4f}")
    print(f"  MAE  : {mae:,.0f} passagers")
    print(f"  RMSE : {rmse:,.0f} passagers")
    print("=" * 40)

    joblib.dump(pipeline, 'models/regression_lineaire.pkl')
    print("  Modèle sauvegardé : models/regression_lineaire.pkl")

    return pipeline, {'r2': r2, 'mae': mae, 'rmse': rmse}

if __name__ == '__main__':
    entrainer_et_evaluer()