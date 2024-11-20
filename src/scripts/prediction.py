import sys
import math
import tools as tl
import pandas as pd

# Retrieve the input information entered in the dictionary as a sentence
user_input = sys.argv[1]

# Extract words from the sentence
words_list = tl.extract_words(user_input)


product_name = words_list[0]
country_name = words_list[1]
size = words_list[2]

#Work in progress : creating a list to store material_name and material_perc
materials = []
material_percs = []
for i in range(3,(len(words_list)-1),2):
    materials.append(words_list[i])
    material_percs.append(float(words_list[i+1]) / 100)

# Load the necessary CSV files into DataFrames
df_materials = tl.get_csv("materials.csv")
df_products = tl.get_csv("products.csv")
df_countries = tl.get_csv("countries.csv")
df_size = tl.get_csv("Tailles.csv")

# Get the ID or code of the predictive variable based on its name in the questionnaire
materials_id = []
for XX in materials:
    mat = tl.get_id_from_name(df_materials, 'name', XX, 'id')
    materials_id.append(mat)
    
product_id = tl.get_id_from_name(df_products, 'name', product_name, 'id')
country_making = tl.get_id_from_name(df_countries, 'name', country_name, 'code')
mass_kg = tl.get_weight_from_product(df_size, product_id, size)


list_Xpred = []
for XX in materials:
    list_var_pred = [[product_id, mass_kg, XX, country_making]]
    X_pred = pd.DataFrame(
        list_var_pred, 
        columns=['product', 'mass_kg', 'material_id', 'countryMaking']
    )
    list_Xpred.append(X_pred)
 



# Load the model
model = tl.load_model("modele_gbm_2000.pkl")
prediction = 0
for i in range(0,len(material_percs)):
    prediction = prediction + material_percs[i] * model.predict(list_Xpred[i])
    
print(str(math.ceil(prediction[0])))
