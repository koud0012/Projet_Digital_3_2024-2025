import requests
import pandas as pd
import numpy as np

from list_materials import id_materials_list
from list_countries import code_countries_list
from list_products import id_product_list


from table_n_176_k_1 import table_n_176_k_1 as list_mat_balance
from table_k_1_parmi_n_16 import table_k_1_parmi_n_16 as list_mat_nb
from intervalle_poids_product import intervalle_poids_product


from datetime import datetime

# Obtenir l'heure actuelle
run_time = datetime.now().strftime("%H:%M:%S")

print(f"run time : {run_time}")

nb_diff_balance = int(len(list_mat_balance)/(len(list_mat_nb)*len(id_product_list)))

country = "---"

#--------------------------
count_balance = 0

for k in range(len(id_product_list)):
    
    # Initialiser des listes vides pour stocker les résultats
    all_results = []
    all_essential_results = []

    poids = (intervalle_poids_product[k][0] + intervalle_poids_product[k][1])/2
    
    
    product = id_product_list[k]

    nb_materials = len(list_mat_balance[0])
    for mat_nb in list_mat_nb:
    # for mat_nb, mat_balance in zip(list_mat_nb, list_mat_balance):
    

        
        for i in range(nb_diff_balance):
            
            api_key = "0b20be33-1816-427f-9304-212d9a6154bb"
            
            # URL de base de l'API et endpoint spécifique
            base_url = "https://ecobalyse.beta.gouv.fr/api"
            endpoint = "/textile/simulator/ecs"
            
            materials_tab = []
            for j in range(nb_materials):
                material_dictionary = {
                    "id": id_materials_list[mat_nb[j]],
                    "share": list_mat_balance[count_balance][j],  # Proportion du matériau
                    "country": "---"  # Pays d'origine
                }
                materials_tab.append(material_dictionary)
            count_balance += 1
            # Corps de la requête avec les paramètres
            data = {
                "mass": poids,  # Poids du produit en kg
                "materials": materials_tab,
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
                # table_data = {
                #     "product": response_data["query"]["product"],
                #     "mass_kg": response_data["query"]["mass"],
                #     "material_id_1": response_data["query"]["materials"][0]["id"],
                #     "material_share_1": response_data["query"]["materials"][0]["share"],
                #     "material_country": '---',
                #     "countryDyeing": "---",
                #     "countryFabric": "---",
                #     "countryMaking": country,
                #     "countrySpinning": "---",
                #     "upcycled": response_data["query"]["upcycled"],
                #     "impact_ecs": response_data["impacts"]["ecs"],
                #     "description": response_data["description"],
                #     "webUrl": response_data["webUrl"]
                # }
                
                materials_dic = {}
                
                for h in range(nb_materials):
                    new_key = {
                        f"material_id_{h+1}": response_data["query"]["materials"][h]["id"],
                        f"material_share_{h+1}": response_data["query"]["materials"][h]["share"]
                        }
                
                    materials_dic.update(new_key)
                
                essential_table_data = {
                    "product": response_data["query"]["product"],
                    "mass_kg": response_data["query"]["mass"],
                    }
                    
                last_key = { "countryMaking": country,
                    "impact_ecs": response_data["impacts"]["ecs"]
                    }
                
                essential_table_data.update(materials_dic)
                essential_table_data.update(last_key)

                # Ajouter les données aux listes
                # all_results.append(table_data)
                all_essential_results.append(essential_table_data)
                
            except requests.exceptions.RequestException as e:
                print(f"Erreur à {product}_{country}g lors de la requête POST : {e}")
                continue  # Passe à la prochaine itération en cas d'erreur
        
        # Après la boucle, créer les DataFrames
    # df_result = pd.DataFrame(all_results)
    df_essential_result = pd.DataFrame(all_essential_results)
    
    le_poids=int(1000*poids)
    # nom_fichier = f'data_multi_{nb_materials}/data_multimat_{product}_multimateriaux_{nb_materials}.csv'
    # nom_fichier_essentiel = f'data_{product}/donnees_essentiel_multimateriaux_{product}_{country}_{id_materials_list[u]}_{nb_materials}.csv'
    nom_fichier_essentiel = f'data_essential_multi_{nb_materials}/donnees_essential_multimat_{product}_multimateriaux_{nb_materials}.csv'

    # nom_fichier_essentiel = f'data_{product}/donnees_essentiel_multimateriaux_{product}_{country}_{nb_materials}.csv'

    # df_result.to_csv(nom_fichier, index=False, encoding='utf-8')
    df_essential_result.to_csv(nom_fichier_essentiel, index=False, encoding='utf-8')
    
    time_now = datetime.now().strftime("%H:%M:%S")

    print(f"Product scrapped {product} {k+1}/11 : {time_now}")


print("extraction terminée")