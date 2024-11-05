import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from sklearn.model_selection import train_test_split

test_data = pd.read_csv('donnees_essentiel_ecobalyse_test.csv')  

X_test = test_data[['product', 'mass_kg', 'material_id', 'countryMaking']]
y_test = test_data['impact_ecs']


# Charger le modèle entraîné
pipeline = joblib.load('modele_gbm_2000.pkl')

# Prédiction sur les données de test
predictions = pipeline.predict(X_test)

# Ajouter les prédictions au DataFrame de test
test_data['predicted_impact_ecs'] = predictions
print(test_data[['impact_ecs', 'predicted_impact_ecs']].head())

# Calcul des métriques d'évaluation
rmse_rf = np.sqrt(mean_squared_error(y_test, predictions))
mae_rf = mean_absolute_error(y_test, predictions)
errors = y_test - predictions

# Calcul de la variance des erreurs
variance_errors = np.var(errors)

# Calcul de l'écart-type des erreurs
sd_errors = np.std(errors)

# Calcul de la moyenne des erreurs
mean_error = np.mean(errors)

# Calcul de la moyenne des valeurs réelles pour exprimer l'erreur en pourcentage
mean_real = np.mean(y_test)

# Définition de l'intervalle en pourcentage (par exemple ±1 écart-type)
interval_low = (mean_error - sd_errors) / mean_real * 100
interval_high = (mean_error + sd_errors) / mean_real * 100

# Affichage des résultats
print(f"Intervalle d'erreur moyen en pourcentage : [{interval_low}% , {interval_high}%]")
print(f"Variance de l'erreur : {variance_errors}")
print(f"Écart-type de l'erreur : {sd_errors}")

# Calcul du R²
ss_total = np.sum((y_test - np.mean(y_test)) ** 2)
ss_residual = np.sum((y_test - predictions) ** 2)
r_squared_rf = 1 - (ss_residual / ss_total)

# Calcul du MAPE
mape_rf = np.mean(np.abs((y_test - predictions) / y_test)) * 100

# Affichage des résultats
print("Performance du modèle Gradient Boosting sur les données de test :")
print(f"MAPE (pourcentage d'erreur) : {mape_rf}%")
print(f"RMSE : {rmse_rf}")
print(f"MAE : {mae_rf}")
print(f"R² : {r_squared_rf}")

print(f"Nombre de lignes dans les données de test : {test_data.shape[0]}")
