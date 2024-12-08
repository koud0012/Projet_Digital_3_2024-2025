import pandas as pd
from sklearn.model_selection import train_test_split
# Chargement des données
data = pd.read_csv('data/data_essentials_ecobalyse.csv')  

# Splitter les données en un jeu d'entraînement et un jeu de test
X = data[['product', 'mass_kg', 'material_id', 'countryMaking']]
y = data['impact_ecs']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Enregistrer le jeu d'entraînement dans un fichier
train_data = X_train.copy()
train_data['impact_ecs'] = y_train
train_data.to_csv('data/data_essentials_ecobalyse_train.csv', index=False)

# Enregistrer le jeu de test dans un fichier
test_data = X_test.copy()
test_data['impact_ecs'] = y_test
test_data.to_csv('data/data_essentials_ecobalyse_test.csv', index=False)
