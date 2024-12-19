import tools as tl
import math
import pandas as pd


def trigger(user_clothing_data : str):
    """
    trigger the 4 steps to predict the environnement cost of a cloth.

    Args:
        sentence (str): A string conaining the users answer to the VBA userform.
    """
    product_name, country_name, mass_kg, materials, material_percs = Processing_data(user_clothing_data)
    product_id, country_id, material_ids = Translating_data(product_name, country_name, materials)
    list_Xpred = Creating_prediction_df(product_id, mass_kg, country_id, material_ids)
    prediction = Predicting_cost(list_Xpred, material_percs)
    print(prediction)



#Processing data received from VBA entered into the form
def Processing_data(user_clothing_data : str):
    """
    Parses and processes the input data received from the VBA form.
    
    Args:
        user_clothing_data (str): A string containing the clothing data input by the user.
                                  It includes product name, country, size, and material 
                                  composition (materials and their respective percentages).

    Returns:
        tuple: A tuple containing:
            - product_name (str): The name of the product.
            - country_name (str): The country of origin/manufacture.
            - size (str): The size of the product.
            - materials (list): A list of materials used in the product.
            - material_percs (list): A list of material percentages in decimal form (e.g., 0.5 for 50%).
    """
    words_list = tl.extract_words(user_clothing_data)
    product_name = words_list[0]
    country_name = words_list[1]
    mass_kg = float(words_list[2])/1000
    materials = []
    material_percs = []
    for i in range(3,(len(words_list)-1),2):
        materials.append(words_list[i])
        material_percs.append(float(words_list[i+1]) / 100)

    return product_name, country_name, mass_kg, materials, material_percs


#Transform the data to translate it into terms of the explanatory vector
def Translating_data(product_name : str, country_name : str , materials : list):
    """
    Maps the parsed data to their respective IDs or predictive variables 
    based on reference datasets.

    Args:
        product_name (str): The name of the product.
        country_name (str): The country of origin/manufacture.
        size (str): The size of the product.
        materials (list): A list of materials used in the product.

    Returns:
        tuple: A tuple containing:
            - product_id (int): The ID associated with the product name.
            - mass_kg (float): The weight of the product in kilograms based on its size and type.
            - country_id (int): The code or ID representing the country of manufacture.
            - material_ids (list): A list of IDs for the materials used in the product.
    """
    df_materials = tl.get_csv("materials.csv")
    df_products = tl.get_csv("products.csv")
    df_countries = tl.get_csv("countries.csv")

    # Get the ID or code of the predictive variable based on its name in the questionnaire
    material_ids = []
    for material in materials:
        mat = tl.get_id_from_name(df_materials, 'name', material, 'id')
        material_ids.append(mat)
        
    product_id = tl.get_id_from_name(df_products, 'name', product_name, 'id')
    country_id = tl.get_id_from_name(df_countries, 'name', country_name, 'code')

    return product_id, country_id,material_ids


# Create the dataframes used for the prediction
def Creating_prediction_df(product_id : str, mass_kg : float , country_making : str, materials : list):
    """
    Constructs a list of explanatory variable datasets for prediction.

    Args:
        product_id (str): The ID of the product.
        mass_kg (float): The weight of the product in kilograms.
        country_making (str): The code or ID of the manufacturing country.
        materials (list): A list of material IDs used in the product.

    Returns:
        list: A list of Pandas DataFrames, each containing the explanatory variables 
              for a specific material used in the product.
    """
    list_Xpred = []
    for material in materials:
        list_var_pred = [[product_id, mass_kg, material, country_making]]
        X_pred = pd.DataFrame(
            list_var_pred, 
            columns=['product', 'mass_kg', 'material_id', 'countryMaking']
        )
        list_Xpred.append(X_pred)
    return list_Xpred

# Load the model to predict the environnemental cost of a cloth
def Predicting_cost(list_Xpred : list, material_percs : list):
    """
    Predicts the output based on the explanatory variables and material percentages.

    Args:
        list_Xpred (list): A list of Pandas DataFrames containing explanatory variables 
                           for each material.
        material_percs (list): A list of material percentages in decimal form (e.g., 0.5 for 50%).

    Returns:
        int: The rounded prediction result from the model, combining contributions 
             from all materials based on their percentages.
    """
    model = tl.load_model("xgb_model_30000.pkl")
    prediction = 0
    for i in range(0,len(material_percs)):
        prediction = prediction + material_percs[i] * model.predict(list_Xpred[i])
    return math.ceil(prediction[0])
