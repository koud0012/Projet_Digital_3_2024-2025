import os
import pandas as pd
import joblib


def extract_words(sentence  : str):
    """
    Splits a sentence into a list of words.

    Args:
        sentence (str): A string to be split into words.

    Returns:
        list: A list of words extracted from the sentence.
    """
    words = sentence.split()
    return words


def get_csv(csv_name: str):
    """
    Loads a CSV file into a Pandas DataFrame.

    Args:
        csv_name (str): The name of the CSV file to load (including the extension).

    Returns:
        pd.DataFrame: A DataFrame containing the data from the CSV file.
    """
    if not isinstance(csv_name, str):
        raise TypeError("The argument must be a string.")
    if not csv_name.strip():
        raise ValueError("The string must not be empty or whitespace.")
    
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '..', '..', 'data', csv_name)

    df = pd.read_csv(csv_path)
    
    return df


def load_model(model_name: str):
    """
    Loads a pre-trained prediction model saved in a .pkl file.

    Args:
        model_name (str): The name of the model file to load (with the .pkl extension).

    Returns:
        object: The loaded model, ready to be used for predictions.
    """
    if not isinstance(model_name, str):
        raise TypeError("The model name must be a string.")
    if not model_name.strip():
        raise ValueError("The model name must not be empty or whitespace.")
    if not model_name.endswith(".pkl"):
        raise ValueError("The model name must have a .pkl extension.")

    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, '..', '..', 'modele', model_name)
    
    return joblib.load(model_path)


def get_id_from_name(df: pd.DataFrame, name_column: str, value_to_find: str, id_column: str):
    """
    Searches for a name in a specified column of a DataFrame and returns the associated ID.

    Args:
        df (pd.DataFrame): The DataFrame to search.
        name_column (str): The name of the column containing the names to search.
        value_to_find (str): The value to search for in the `name_column`.
        id_column (str): The name of the column containing the IDs to retrieve.

    Returns:
        object: The corresponding ID if found, otherwise None.
    """
    matching_row = df[df[name_column] == value_to_find]
    if not matching_row.empty:
        return matching_row.iloc[0][id_column]
    return None


def get_weight_from_product(df: pd.DataFrame, product_type: str, size: str):
    """
    Retrieves the weight of a product based on its type and size.

    Args:
        df (pd.DataFrame): A DataFrame containing product weights by size.
        product_type (str): The type of product (e.g., 'chemise', 'jean').
        size (str): The size of the product for which to retrieve the weight ('XS', 'S', 'M', 'L', 'XL').

    Returns:
        float: The weight in kilograms of the product for the given size, or None if not found.
    """
    if product_type in df['Type'].values:
        product_row = df[df['Type'] == product_type]
        if size in product_row.columns:
            return product_row[size].values[0] / 1000
    return None
