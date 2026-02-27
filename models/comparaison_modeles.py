import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import joblib

# Import des pipelines de chaque modèle
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model_regression import charger_donnees, construire_pipeline as pipeline_regression
from models.model_random_forest import construire_pipeline as pipeline_rf
from models.model_xgboost import construire_pipeline as pipeline_xgboost

def comparer_modeles(chemin='data/dataset_simule.csv'):
    X, y = charger_donnees(chemin)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modeles = {
        'Régression Linéaire': pipeline_regression(),
        'Random Forest':       pipeline_rf(),
        'XGBoost':             pipeline_xgboost(),
    }

    resultats = []

    for nom, pipeline in modeles.items():
        print(f"⏳ Entraînement : {nom}...")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        r2   = r2_score(y_test, y_pred)
        mae  = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Cross-validation (5 folds)
        cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='r2', n_jobs=-1)

        resultats.append({
            'Modèle':       nom,
            'R²':           round(r2, 4),
            'MAE':          round(mae, 0),
            'RMSE':         round(rmse, 0),
            'R² CV (mean)': round(cv_scores.mean(), 4),
            'R² CV (std)':  round(cv_scores.std(), 4),
        })

    df_resultats = pd.DataFrame(resultats)

    print("\n" + "=" * 65)
    print("              COMPARAISON DES MODÈLES")
    print("=" * 65)
    print(df_resultats.to_string(index=False))
    print("=" * 65)

    # Sauvegarde du tableau
    df_resultats.to_csv('docs/comparaison_resultats.csv', index=False)
    print("\n✅ Résultats sauvegardés : docs/comparaison_resultats.csv")

    # --- Graphique comparaison ---
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle('Comparaison des modèles — TER Dakar', fontsize=14, fontweight='bold')

    noms = df_resultats['Modèle']
    couleurs = ['#e74c3c', '#2ecc71', '#3498db']

    # R²
    axes[0].bar(noms, df_resultats['R²'], color=couleurs)
    axes[0].set_title('R² (plus haut = meilleur)')
    axes[0].set_ylim(0, 1)
    axes[0].tick_params(axis='x', rotation=15)
    for i, v in enumerate(df_resultats['R²']):
        axes[0].text(i, v + 0.01, str(v), ha='center', fontweight='bold')

    # MAE
    axes[1].bar(noms, df_resultats['MAE'], color=couleurs)
    axes[1].set_title('MAE (plus bas = meilleur)')
    axes[1].tick_params(axis='x', rotation=15)
    for i, v in enumerate(df_resultats['MAE']):
        axes[1].text(i, v + 200, f'{v:,.0f}', ha='center', fontweight='bold')

    # RMSE
    axes[2].bar(noms, df_resultats['RMSE'], color=couleurs)
    axes[2].set_title('RMSE (plus bas = meilleur)')
    axes[2].tick_params(axis='x', rotation=15)
    for i, v in enumerate(df_resultats['RMSE']):
        axes[2].text(i, v + 200, f'{v:,.0f}', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('visualisations/comparaison_modeles.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Graphique sauvegardé : visualisations/comparaison_modeles.png")

    return df_resultats

if __name__ == '__main__':
    comparer_modeles()