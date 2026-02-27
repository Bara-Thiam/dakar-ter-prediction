import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model_regression import charger_donnees
from models.model_random_forest import construire_pipeline as pipeline_rf
from models.model_xgboost import construire_pipeline as pipeline_xgboost

def optimiser_random_forest(X_train, y_train):
    print("⏳ Optimisation Random Forest...")

    param_grid = {
        'model__n_estimators': [100, 200, 300],
        'model__max_depth': [10, 15, 20],
        'model__min_samples_split': [2, 5],
    }

    grid_search = GridSearchCV(
        pipeline_rf(),
        param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        verbose=1
    )
    grid_search.fit(X_train, y_train)

    print(f"  Meilleurs paramètres : {grid_search.best_params_}")
    print(f"  Meilleur R² CV       : {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_

def optimiser_xgboost(X_train, y_train):
    print("\n⏳ Optimisation XGBoost...")

    param_grid = {
        'model__n_estimators': [200, 300, 400],
        'model__max_depth': [4, 6, 8],
        'model__learning_rate': [0.03, 0.05, 0.1],
    }

    grid_search = GridSearchCV(
        pipeline_xgboost(),
        param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        verbose=1
    )
    grid_search.fit(X_train, y_train)

    print(f"  Meilleurs paramètres : {grid_search.best_params_}")
    print(f"  Meilleur R² CV       : {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_

def evaluer(modele, X_test, y_test, nom):
    y_pred = modele.predict(X_test)
    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"\n  📊 {nom} après optimisation :")
    print(f"     R²   : {r2:.4f}")
    print(f"     MAE  : {mae:,.0f} passagers")
    print(f"     RMSE : {rmse:,.0f} passagers")

    return {'r2': r2, 'mae': mae, 'rmse': rmse}

if __name__ == '__main__':
    X, y = charger_donnees()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Optimisation
    best_rf = optimiser_random_forest(X_train, y_train)
    best_xgb = optimiser_xgboost(X_train, y_train)

    # Évaluation
    print("\n" + "=" * 50)
    print("     RÉSULTATS APRÈS OPTIMISATION")
    print("=" * 50)
    evaluer(best_rf, X_test, y_test, "Random Forest")
    evaluer(best_xgb, X_test, y_test, "XGBoost")

    # Sauvegarde du meilleur modèle
    rf_r2  = r2_score(y_test, best_rf.predict(X_test))
    xgb_r2 = r2_score(y_test, best_xgb.predict(X_test))

    if xgb_r2 >= rf_r2:
        joblib.dump(best_xgb, 'models/model_final.pkl')
        print("\n✅ Modèle final sauvegardé : XGBoost → models/model_final.pkl")
    else:
        joblib.dump(best_rf, 'models/model_final.pkl')
        print("\n✅ Modèle final sauvegardé : Random Forest → models/model_final.pkl")