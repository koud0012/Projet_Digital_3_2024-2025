import sys
import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import os
import math



def extraire_mots(phrase):
    """
    Cette fonction prend une phrase en entrée et la sépare en une liste de mots.
    
    Parameters:
    - phrase : Une chaîne de caractères à séparer en mots
    
    Returns:
    - Une liste de mots extraits de la phrase
    """
    mots = phrase.split()  # Sépare la phrase en mots en utilisant l'espace comme délimiteur
    return mots  # Retourne la liste de mots séparés



def get_csv(csv_name):
    """
    Cette fonction charge un fichier CSV dans un DataFrame et retourne le DataFrame associé au nom du fichier.
    
    Parameters:
    - csv_name : Le nom du fichier CSV à charger (avec l'extension)
    
    Returns:
    - Un DataFrame contenant les données du fichier CSV
    """
    current_dir = os.path.dirname(__file__)  # Récupère le chemin du script actuel
    csv_path = os.path.join(current_dir, '..', '..', 'data', csv_name)  # Chemin complet du fichier CSV
    csv_name = os.path.splitext(os.path.basename(csv_path))[0]  # Récupère le nom du fichier sans extension pour le nom du dataframe
    
    df = pd.read_csv(csv_path)  # Charge le CSV dans un DataFrame

    # Nommer dynamiquement le DataFrame en fonction du nom du CSV
    dataframes = {}  # Dictionnaire pour stocker le DataFrame avec son nom
    dataframes[csv_name] = df  # Associe le DataFrame au nom du CSV
    
    return dataframes[csv_name]  # Retourne le DataFrame associé au nom du fichier



def model_loader(model_name):
    """
    Cette fonction charge un modèle de prédiction sauvegardé dans un fichier .pkl.
    
    Parameters:
    - model_name : Le nom du fichier du modèle à charger (avec l'extension .pkl)
    
    Returns:
    - Le modèle chargé, prêt à être utilisé pour des prédictions
    """
    current_dir = os.path.dirname(__file__)  # Récupère le chemin du script actuel
    model_path = os.path.join(current_dir, '..', '..', 'modele', model_name)  # Chemin complet du fichier du modèle pkl
    
    return joblib.load(model_path)  # Charge et retourne le modèle sauvegardé dans le fichier pkl




def get_id_from_name(df, name_column, value_to_find, id_column):
    """
    Cette fonction recherche un nom dans une colonne d'un DataFrame et retourne l'ID associé.

    Parameters:
    - df : DataFrame dans lequel effectuer la recherche
    - name_column : Nom de la colonne contenant les noms à rechercher
    - value_to_find : Valeur à rechercher dans la colonne 'name'
    - id_column : Nom de la colonne contenant les ID à récupérer

    Returns:
    - L'ID correspondant si trouvé, sinon None
    """
    matching_row = df[df[name_column] == value_to_find]
    
    if not matching_row.empty:
        return matching_row.iloc[0][id_column]  # Retourner l'ID trouvé
    return None  # Si aucune correspondance n'est trouvée



def get_weight_from_product(df, product_type, size):
    """
    Cette fonction récupère le poids du produit en fonction de son type et de la taille.
    
    Parameters:
    - df : DataFrame contenant les poids des produits par taille
    - product_type : Le type de produit (par exemple 'chemise', 'jean')
    - size : La taille du produit pour laquelle on veut obtenir le poids ('XS', 'S', 'M', 'L', 'XL')
    
    Returns:
    - Le poids en kilogrammes du produit pour la taille donnée, ou None si non trouvé.
    """
    # Vérifier si le produit existe dans la colonne 'Type'
    if product_type in df['Type'].values:
        # Trouver la ligne correspondant au produit
        product_row = df[df['Type'] == product_type]
        
        # Vérifier si la taille existe dans les colonnes
        if size in product_row.columns:
            # Récupérer le poids en fonction de la taille
            return product_row[size].values[0] / 1000  # Retourner le poids en kg (divisé par 1000)
    
    # Retourner None si aucune correspondance n'est trouvée
    return None

def main():
    # Récuperation des information saisie dans le dictionnaire sous forme d'une phrase
   user_input = sys.argv[1] 

   # Extraction des mots de la phrase
   liste_mots = extraire_mots(user_input)
   product_name = liste_mots[0]
   countrie_name = liste_mots[1]
   taille = liste_mots[2]
   material_name = liste_mots[3]
   material_perc = float(liste_mots[4]) / 100

   # Chargement des fichiers CSV necessaires dans des DataFrame
   df_materials = get_csv("materials.csv")
   df_products = get_csv("products.csv")
   df_countries = get_csv("countries.csv")
   df_taille = get_csv("Tailles.csv")


   # Obtenir l'id ou le code de la variable prédictive en fonction de son nom dans le questionnaire
   material_id = get_id_from_name(df_materials,'name',material_name,'id')
   product_id  = get_id_from_name(df_products,'name',product_name,'id')
   countryMaking = get_id_from_name(df_countries,'name',countrie_name,'code')
   mass_kg = get_weight_from_product(df_taille, material_id, taille)


   # Création du vecteur de variables explicatives pour la prédiction
   list_var_pred = [[product_id, 0.115, material_id, countryMaking]]
   X_pred = pd.DataFrame(list_var_pred, columns=['product', 'mass_kg', 'material_id', 'countryMaking'])

   # Charger le modèle
   model =  model_loader("modele_gbm_2000.pkl")
   prediction = model.predict(X_pred)

   print("Score : " + str(math.ceil(prediction[0])))


if __name__ == "__main__":
   main()
   