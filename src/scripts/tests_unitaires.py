import unittest
import pandas as pd
import os
import sys
import joblib
from unittest.mock import patch


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

class TestFunctions(unittest.TestCase):

    # ---------------------- Test de extraire_mots ----------------------
    def test_extraire_mots(self):
        phrase = "chemise france M 100"
        result = extraire_mots(phrase)
        expected = ['chemise', 'france', 'M', '100']
        self.assertEqual(result, expected)
        
        # Test avec une phrase vide
        result = extraire_mots("")
        expected = []
        self.assertEqual(result, expected)

        # Test avec une phrase avec plusieurs espaces
        phrase = "chemise   france  M   100"
        result = extraire_mots(phrase)
        expected = ['chemise', 'france', 'M', '100']
        self.assertEqual(result, expected)

    # ---------------------- Test de get_csv ----------------------
    @patch('pandas.read_csv')  # Patch de la fonction read_csv pour éviter d'avoir besoin de fichiers réels
    def test_get_csv(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            'Type': ['chemise', 'jean', 'manteau'],
            'XS': [175, 400, 800],
            'S': [225, 475, 950],
            'M': [275, 550, 1100],
            'L': [325, 650, 1300],
            'XL': [375, 750, 1500]
        })

        # Test avec un fichier CSV
        result = get_csv("products.csv")
        self.assertTrue(isinstance(result, pd.DataFrame))  # Vérifier que la fonction retourne un DataFrame

    # ---------------------- Test de model_loader ----------------------
    @patch('joblib.load')  # Patch de joblib.load pour ne pas avoir besoin d'un fichier modèle réel
    def test_model_loader(self, mock_load):
        mock_load.return_value = "mock_model"

        result = model_loader("modele_gbm_2000.pkl")
        self.assertEqual(result, "mock_model")

    # ---------------------- Test de get_id_from_name ----------------------
    def test_get_id_from_name(self):
        # Création d'un DataFrame factice
        df = pd.DataFrame({
            'name': ['chemise', 'jean', 'manteau'],
            'id': [1, 2, 3]
        })
        
        # Test avec un nom existant
        result = get_id_from_name(df, 'name', 'jean', 'id')
        self.assertEqual(result, 2)

        # Test avec un nom inexistant
        result = get_id_from_name(df, 'name', 'robe', 'id')
        self.assertIsNone(result)

    # ---------------------- Test de get_weight_from_product ----------------------
    def test_get_weight_from_product(self):
        # Création d'un DataFrame factice
        df = pd.DataFrame({
            'Type': ['chemise', 'jean', 'manteau'],
            'XS': [175, 400, 800],
            'S': [225, 475, 950],
            'M': [275, 550, 1100],
            'L': [325, 650, 1300],
            'XL': [375, 750, 1500]
        })

        # Test avec un produit et une taille existants
        result = get_weight_from_product(df, 'chemise', 'M')
        self.assertEqual(result, 0.275)  # Poids de 275g = 0.275kg

        # Test avec un produit existant mais une taille inexistante
        result = get_weight_from_product(df, 'chemise', 'XXL')
        self.assertIsNone(result)

        # Test avec un produit inexistant
        result = get_weight_from_product(df, 'robe', 'M')
        self.assertIsNone(result)

        # Test avec un DataFrame vide
        empty_df = pd.DataFrame(columns=['Type', 'XS', 'S', 'M', 'L', 'XL'])
        result = get_weight_from_product(empty_df, 'chemise', 'M')
        self.assertIsNone(result)

    # ---------------------- Test du main (en passant les arguments) ----------------------
    @patch('builtins.print')  # Patch print pour éviter d'afficher dans le terminal
    @patch('sys.argv', new=['script.py', 'chemise france M 100'])
    @patch('pandas.read_csv')  # Patch read_csv pour éviter de charger des fichiers CSV
    @patch('joblib.load')  # Patch joblib.load pour éviter de charger un modèle réel
    def test_main(self, mock_load, mock_read_csv, mock_print):
        mock_read_csv.return_value = pd.DataFrame({
            'Type': ['chemise', 'jean', 'manteau'],
            'XS': [175, 400, 800],
            'S': [225, 475, 950],
            'M': [275, 550, 1100],
            'L': [325, 650, 1300],
            'XL': [375, 750, 1500]
        })
        mock_load.return_value = "mock_model"

        # Appel de la fonction main
        from Pred_Cout_Vet import main  # On suppose que votre code est dans un fichier appelé script.py
        main()

        # Vérification de l'appel de la fonction print pour afficher le score
        mock_print.assert_called_with("Score : mock_score")  # Changez "mock_score" pour le résultat de votre modèle

if __name__ == '__main__':
    unittest.main()
