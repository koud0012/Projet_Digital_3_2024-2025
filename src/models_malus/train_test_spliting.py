import pandas as pd
from sklearn.model_selection import train_test_split
# Chargement des données
data = pd.read_csv('./data/transformed_data_difference_simple_multi.csv') 

# Encodage des variables catégoriques
data['product'] = data['product'].astype('category').cat.codes
data['material_id'] = data['material_id'].astype('category').cat.codes

# Préparation des données pour le modèle
features = ['product', 'material_id', 'material_share', 'nb_materiaux']
target = 'malus_per_mass_kg'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Enregistrer le jeu d'entraînement dans un fichier
train_data = X_train.copy()
train_data[target] = y_train
train_data.to_csv('data/transformed_data_difference_simple_multi_train.csv', index=False)

# Enregistrer le jeu de test dans un fichier
test_data = X_test.copy()
test_data[target] = y_test
test_data.to_csv('data/transformed_data_difference_simple_multi_test.csv', index=False)
