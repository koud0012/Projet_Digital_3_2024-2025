import joblib
import pandas as pd
import tools as tl
import mappings as mp
import numpy as np


# import des modeles et des données 

malus_model_path = "xgb_model_1032_depth_5.pkl"
model_path = "xgb_model_29751_depth_8.pkl"

malus_model = joblib.load(malus_model_path)
model = joblib.load(model_path)

test_data = pd.read_csv('./data/test_data_multimateriaux.csv')


#>> adapte les material_id_X en et material_share_X en liste

material_ids_list = []
material_shares_list = []

for row in range(len(test_data)):
    material_ids = []
    material_shares = []
    for index in range(1,4):
        if test_data[f'material_share_{index}'][row] != 0:
            material_ids.append(tl.get_category_code(test_data[f'material_id_{index}'][row],mp.material_id_mapping))
            material_shares.append(test_data[f'material_share_{index}'][row])
    material_ids_list.append(material_ids)
    material_shares_list.append(material_shares)


#  combinaison des deux modeles

impact_ecs_predicted_list = []

mape = []

for row in range(1000): # or range(len(test_data))
    nb_materials = len(material_shares_list[row])
    impact_ecs_predicted = 0
    malus = 0
    cost = 0
    for index in range(nb_materials):
        input_data_malus_model = {'product': tl.get_category_code(test_data['product'][row],mp.product_mapping), 'material_id': material_ids_list[row][index], 'material_share': material_shares_list[row][index],'nb_materiaux': nb_materials}
        input_df_malus_model = pd.DataFrame([input_data_malus_model])
        malus += test_data['mass_kg'][row] * material_shares_list[row][index] * malus_model.predict(input_df_malus_model)

        input_data_model = {'product': tl.get_category_code(test_data['product'][row],mp.product_mapping), 'mass_kg': test_data['mass_kg'][row], 'material_id': material_ids_list[row][index], 'countryMaking': tl.get_category_code(test_data['countryMaking'][row], mp.country_making_mapping)}
        input_df_model = pd.DataFrame([input_data_model])
        cost += material_shares_list[row][index] * model.predict(input_df_model)
        
    impact_ecs_predicted = cost + malus
    
    impact_ecs_predicted_list.append(impact_ecs_predicted)
    
    mape.append(abs(test_data['impact_ecs'][row]-impact_ecs_predicted)/test_data['impact_ecs'][row])
    
    print(row)


print(np.mean(mape))