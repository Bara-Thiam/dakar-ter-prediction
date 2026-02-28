import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
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
        ('model', RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
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
    print("         RANDOM FOREST")
    print("=" * 40)
    print(f"  R²   : {r2:.4f}")
    print(f"  MAE  : {mae:,.0f} passagers")
    print(f"  RMSE : {rmse:,.0f} passagers")
    print("=" * 40)

    feature_names = (
        pipeline.named_steps['preprocessor']
        .get_feature_names_out()
    )
    importances = pipeline.named_steps['model'].feature_importances_
    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)

    print("\nImportance des variables :")
    print(feat_imp.round(4))

    joblib.dump(pipeline, 'models/random_forest.pkl')
    print("\n  Modèle sauvegardé : models/random_forest.pkl")

    return pipeline, {'r2': r2, 'mae': mae, 'rmse': rmse}

if __name__ == '__main__':
    entrainer_et_evaluer()