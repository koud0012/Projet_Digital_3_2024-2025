import requests
import pandas as pd
import numpy as np

from list_materials import id_materials_list
from list_countries import code_countries_list
from list_products import id_product_list

from function import *

from datetime import datetime

# Obtenir l'heure actuelle
time_now = datetime.now().strftime("%H:%M:%S")

print(f"Run time : {time_now}")

intervalle_poids_product = [[0.05,0.5],[0.25,1.5],[0.05,1.0],[0.2,4.0],[0.1,1.5],[0.1,1.5],[0.05, 0.5],[0.005,0.2],[0.02,0.2],[0.01,0.15],[0.05,0.4]]

nb_poids = 10

country_nb = 0

for k in range(2, len(id_product_list)):
    product = id_product_list[k]
    print(f"product : {product}")    
    # Initialiser des listes vides pour stocker les résultats
    all_results = []
    all_essential_results = []

    country_nb = 0
    
    # partition = np.linspace(intervalle_poids_product[k][0], intervalle_poids_product[k][1], nb_poids)
    for country in code_countries_list:
        country_nb += 1
        for material in id_materials_list:
            partition = generate_random_values_list(nb_poids,intervalle_poids_product[k][0],intervalle_poids_product[k][1])
            # k += 1
            for poids in partition:
                # Clé API (remplace "votre_cle_api" par la clé que tu as obtenue)
                api_key = "0b20be33-1816-427f-9304-212d9a6154bb"
                
                # URL de base de l'API et endpoint spécifique
                base_url = "https://ecobalyse.beta.gouv.fr/api"
                endpoint = "/textile/simulator/ecs"
                
                # Corps de la requête avec les paramètres
                data = {
                    "mass": poids,  # Poids du produit en kg
                    "materials": [
                        {
                            "id": material,
                            "share": 1,  # Proportion du matériau
                            "country": "---"  # Pays d'origine
                        }
                    ],
                    "product": product,
                    "countrySpinning": "---",
                    "countryFabric": "---",
                    "countryDyeing": "---",
                    "countryMaking": country
                }
                
                # En-têtes avec la clé API
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # Requête POST
                try:
                    response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data)
                    response.raise_for_status()  # Vérifie les erreurs HTTP
                    response_data = response.json()  # Convertit la réponse en JSON
                    
                    # Extraire les données pour les structurer dans un DataFrame
                    table_data = {
                        "product": response_data["query"]["product"],
                        "mass_kg": response_data["query"]["mass"],
                        "material_id": response_data["query"]["materials"][0]["id"],
                        "material_share": response_data["query"]["materials"][0]["share"],
                        "material_country": '---',
                        "countryDyeing": "---",
                        "countryFabric": "---",
                        "countryMaking": country,
                        "countrySpinning": "---",
                        "upcycled": response_data["query"]["upcycled"],
                        "impact_ecs": response_data["impacts"]["ecs"],
                        "description": response_data["description"],
                        "webUrl": response_data["webUrl"]
                    }
                    
                    essential_table_data = {
                        "product": response_data["query"]["product"],
                        "mass_kg": response_data["query"]["mass"],
                        "material_id": response_data["query"]["materials"][0]["id"],
                        "material_share": response_data["query"]["materials"][0]["share"],
                        "countryMaking": country,
                        "impact_ecs": response_data["impacts"]["ecs"]
                    }
                    
                    # Ajouter les données aux listes
                    all_results.append(table_data)
                    all_essential_results.append(essential_table_data)
                    
                except requests.exceptions.RequestException as e:
                    print(f"Erreur à {product}_{country}_{le_poids}g lors de la requête POST : {e}")
                    continue  # Passe à la prochaine itération en cas d'erreur
            
            # Après la boucle, créer les DataFrames
        df_result = pd.DataFrame(all_results)
        df_essential_result = pd.DataFrame(all_essential_results)
        
        
        sheet_name = f'data/complet/data_{product}.csv'
        sheet_name_essentials = f'data/essentials/essentials_data_{product}.csv'
        
        df_result.to_csv(sheet_name, index=False, encoding='utf-8')
        df_essential_result.to_csv(sheet_name_essentials, index=False, encoding='utf-8')
        
        time_now = datetime.now().strftime("%H:%M:%S")

        print(f"Country scrapped {country_nb}/20 : {time_now}")


    
print("Scrapping end")