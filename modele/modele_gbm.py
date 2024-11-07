from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

train_data = pd.read_csv('donnees_essentiel_ecobalyse_train.csv') 
test_data = pd.read_csv('donnees_essentiel_ecobalyse_test.csv')  


X_train = train_data[['product', 'mass_kg', 'material_id', 'countryMaking']]
y_train = train_data['impact_ecs']

X_test = test_data[['product', 'mass_kg', 'material_id', 'countryMaking']]
y_test = test_data['impact_ecs']


# Prétraitement des variables catégorielles
categorical_features = ['product', 'material_id', 'countryMaking']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

n_estimator = 2000
# Créer et entraîner le modèle GBM avec pipeline
model_gbm = GradientBoostingRegressor(
    loss='squared_error',
    n_estimators=n_estimator,
    max_depth=4,
    learning_rate=0.01,
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model_gbm)
])

# Ajustement du modèle avec validation croisee
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
mean_cv_score = -np.mean(cv_scores)

# Entraînement final
pipeline.fit(X_train, y_train)

nom_fichier_pkl = f'modele_gbm_{n_estimator}.pkl'

# Enregistrer le modèle entraîné
joblib.dump(pipeline, nom_fichier_pkl)

# Prédiction sur les données d'entraînement
predictions = pipeline.predict(X_train)

# Ajouter les prédictions au DataFrame d'entraînement
train_data['predicted_impact_ecs'] = predictions
print(train_data[['impact_ecs', 'predicted_impact_ecs']].head())

# Calcul des métriques d'évaluation
rmse_rf = np.sqrt(mean_squared_error(y_train, predictions))
mae_rf = mean_absolute_error(y_train, predictions)
errors = y_train - predictions

# Calcul de la variance des erreurs
variance_errors = np.var(errors)

# Calcul de l'écart-type des erreurs
sd_errors = np.std(errors)

# Calcul de la moyenne des erreurs
mean_error = np.mean(errors)

# Calcul de la moyenne des valeurs réelles pour exprimer l'erreur en pourcentage
mean_real = np.mean(y_train)

# Définition de l'intervalle en pourcentage (par exemple ±1 écart-type)
interval_low = (mean_error - sd_errors) / mean_real * 100
interval_high = (mean_error + sd_errors) / mean_real * 100

# Affichage des résultats
print(f"Intervalle d'erreur moyen en pourcentage : [{interval_low}% , {interval_high}%]")
print(f"Variance de l'erreur : {variance_errors}")
print(f"Écart-type de l'erreur : {sd_errors}")

# Calcul du R²
ss_total = np.sum((y_train - np.mean(y_train)) ** 2)
ss_residual = np.sum((y_train - predictions) ** 2)
r_squared_rf = 1 - (ss_residual / ss_total)

# Calcul du MAPE
mape_rf = np.mean(np.abs((y_train - predictions) / y_train)) * 100

# Affichage des résultats
print("Performance du modèle Gradient Boosting sur les données d'entraînement :")
print(f"MAPE (pourcentage d'erreur) : {mape_rf}%")
print(f"RMSE : {rmse_rf}")
print(f"MAE : {mae_rf}")
print(f"R² : {r_squared_rf}")

print(f"Nombre de lignes dans les données d'entraînement : {train_data.shape[0]}")
