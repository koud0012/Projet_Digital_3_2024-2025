from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import joblib

# Chargement des données
train_data = pd.read_csv('donnees_essentiel_ecobalyse_train.csv') 
test_data = pd.read_csv('donnees_essentiel_ecobalyse_test.csv')  

# Les caractéristiques (X) et la cible (y)
X_train = train_data[['product', 'impact_ecs', 'material_id', 'countryMaking']]
y_train = train_data['mass_kg']

X_test = test_data[['product', 'impact_ecs', 'material_id', 'countryMaking']]
y_test = test_data['mass_kg']


# Prétraitement des variables catégorielles
categorical_features = ['product', 'material_id', 'countryMaking']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)


# Modèle de régression linéaire
model_lr = LinearRegression()

# Pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model_lr)
])


# Validation croisée pour évaluer les performances
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
mean_cv_score = -np.mean(cv_scores)
print(f"Score MSE moyen (validation croisée) : {mean_cv_score}")

# Entraînement du pipeline
pipeline.fit(X_train, y_train)

# Enregistrement du modèle entraîné
nom_fichier_pkl = 'modele_lr.pkl'
joblib.dump(pipeline, nom_fichier_pkl)

# Prédiction sur les données d'entraînement
train_predictions = pipeline.predict(X_train)
train_data['predicted_mass_kg'] = train_predictions

# Évaluation sur les données d'entraînement
rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
mae = mean_absolute_error(y_train, train_predictions)
r2 = r2_score(y_train, train_predictions)

# Affichage des métriques
print("Performance du modèle de régression linéaire sur les données d'entraînement :")
print(f"RMSE : {rmse}")
print(f"MAE : {mae}")
print(f"R² : {r2}")


# Affichage des premières lignes avec les prédictions
print(train_data[['mass_kg', 'predicted_mass_kg']].head())


# Évaluation sur les données de test
test_predictions = pipeline.predict(X_test)
rmse_test = np.sqrt(mean_squared_error(y_test, test_predictions))
mae_test = mean_absolute_error(y_test, test_predictions)
r2_test = r2_score(y_test, test_predictions)

print("Performance du modèle de régression linéaire sur les données de test :")
print(f"RMSE : {rmse_test}")
print(f"MAE : {mae_test}")
print(f"R² : {r2_test}")




# Importance des caractéristiques (coefficients)
coefficients = model_lr.coef_
feature_names = preprocessor.get_feature_names_out()

plt.figure(figsize=(12, 12))
sns.barplot(x=coefficients, y=feature_names, palette="viridis")
plt.title("Importance des caractéristiques (Coefficients du modèle)")
plt.xlabel("Coefficient")
plt.ylabel("Caractéristiques")
plt.grid(True)
plt.show()



# Réel vs Prédit sur l'ensemble d'entraînement
plt.figure(figsize=(8, 6))
plt.scatter(y_train, train_predictions, alpha=0.6, edgecolor='k', label="Données d'entraînement")
plt.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2, label="Ligne idéale (y=x)")
plt.title("Réel vs Prédit (Ensemble d'entraînement)")
plt.xlabel("Valeurs réelles")
plt.ylabel("Valeurs prédites")
plt.legend()
plt.grid(True)
plt.show()


# Distribution des erreurs sur l'ensemble d'entraînement
train_errors = y_train - train_predictions

plt.figure(figsize=(8, 6))
sns.histplot(train_errors, kde=True, bins=30, color='blue')
plt.axvline(x=0, color='red', linestyle='--', label="Erreur = 0")
plt.title("Distribution des erreurs (Ensemble d'entraînement)")
plt.xlabel("Erreur (Valeurs réelles - Valeurs prédites)")
plt.ylabel("Fréquence")
plt.legend()
plt.grid(True)
plt.show()


# Résidus vs Valeurs prédites
plt.figure(figsize=(8, 6))
plt.scatter(train_predictions, train_errors, alpha=0.6, edgecolor='k')
plt.axhline(y=0, color='red', linestyle='--', lw=2)
plt.title("Graphique des résidus (Ensemble d'entraînement)")
plt.xlabel("Valeurs prédites")
plt.ylabel("Résidus (Erreur)")
plt.grid(True)
plt.show()


# Courbe des valeurs réelles vs prédites
plt.figure(figsize=(10, 6))
plt.plot(y_train.values[1570:1620], label="Valeurs réelles", marker='o', linestyle='-', color='blue')
plt.plot(train_predictions[1570:1620], label="Valeurs prédites", marker='x', linestyle='--', color='orange')
plt.title("Courbe des valeurs réelles vs prédites (50 premières observations)")
plt.xlabel("Index")
plt.ylabel("Valeurs")
plt.legend()
plt.grid(True)
plt.show()


# Résidus sur l'ensemble de test
test_errors = y_test - test_predictions

plt.figure(figsize=(8, 6))
sns.histplot(test_errors, kde=True, bins=30, color='green')
plt.axvline(x=0, color='red', linestyle='--', label="Erreur = 0")
plt.title("Distribution des erreurs (Ensemble de test)")
plt.xlabel("Erreur (Valeurs réelles - Valeurs prédites)")
plt.ylabel("Fréquence")
plt.legend()
plt.grid(True)
plt.show()