from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def regression_by_product(data, target_col, product_col):
    
        """
        Calculates predictions for all product types available in the data.

        This function applies a specific regression model for each product type 
        to predict the target variable's values. The predictions are added as 
        a new column in the DataFrame.


        Args:
            
        data (pd.DataFrame): 
            Input data for which predictions will be generated.
            Must include at least the product column (`product_col`) 
            and the necessary columns for predictions.
            
        target_col (str): 
            Name of the target column (this column will be excluded 
            from the input features for prediction).
            
        product_col (str): 
            Name of the categorical column used to identify product types.
            
        model_results (dict): 
            Dictionary containing a model for each unique product type.
            Each key is a product type, and each value is a dictionary 
            with at least a 'model' key containing the trained model.


        Returns:
            
        pd.DataFrame: 
            A copy of the input DataFrame with an additional column 
            `predicted_<target_col>` containing the predictions.
        """
    
        results = {}
        unique_products = data[product_col].unique()

        for product in unique_products:
            # Filtrer les données pour le type de produit actuel
            product_data = data[data[product_col] == product]
            X = product_data.drop(columns=[target_col, product_col])
            y = product_data[target_col]

            # Prétraitement (OneHotEncoding pour les variables catégorielles restantes)
            categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
                    ],
                remainder='passthrough'
                )

            # Pipeline
            model = Pipeline([
                ('preprocessor', preprocessor),
                ('linear_model', LinearRegression())
                ])

            # Training the model
            model.fit(X, y)

            # Predictions
            predictions = model.predict(X)

            # Error metrics computation
            mse = mean_squared_error(y, predictions)
            mae = mean_absolute_error(y, predictions)
            r2 = r2_score(y, predictions)

            # Save the results
            results[product] = {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'model': model  # Keep the model
                }

            print(f"Produit : {product}")
            print(f"MSE : {mse}")
            print(f"MAE : {mae}")
            print(f"R² : {r2}")
            print('-' * 40)
            

        return results


### Import data
train_data = pd.read_csv('data_essentials_ecobalyse.csv')

### Apply function to data
resultats = regression_by_product(
    data=train_data,
    target_col='mass_kg',
    product_col='product'
)



def visualize_coefficients_by_product(model_results):
    """
    Generates visualizations of coefficients for each product's model.

    Args:
        model_results (dict): 
            Dictionary containing the model results by product. 
            Each model must include a pipeline with a linear regression model.
    """
    for product, result in model_results.items():
        model = result['model']  # Retrieve the pipeline
        linear_model = model.named_steps['linear_model']  # Extract the linear regression model
        preprocessor = model.named_steps['preprocessor']  # Extract the preprocessor
        
        # Retrieve the coefficients and the feature names
        coefficients = linear_model.coef_
        feature_names = preprocessor.get_feature_names_out()
        
        # Visualize the coefficients
        plt.figure(figsize=(10, 8))
        sns.barplot(x=coefficients, y=feature_names, palette="viridis")
        plt.title(f"Feature Importance for {product}")
        plt.xlabel("Coefficient")
        plt.ylabel("Features")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Example usage
visualize_coefficients_by_product(resultats)
