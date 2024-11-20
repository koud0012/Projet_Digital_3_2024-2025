import unittest
import os
import joblib
import pandas as pd
from tools import get_csv, load_model, extract_words, get_id_from_name, get_weight_from_product

class TestGetCSV(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for the tests. Creates a temporary directory and a sample CSV file.
        """
        cls.test_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(cls.test_dir, exist_ok=True)
        cls.sample_csv = os.path.join(cls.test_dir, 'test_file.csv')

        # Create a sample CSV file for testing
        df = pd.DataFrame({
            'column1': [1, 2, 3],
            'column2': ['a', 'b', 'c']
        })
        df.to_csv(cls.sample_csv, index=False)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after all tests are done.
        """
        if os.path.exists(cls.sample_csv):
            os.remove(cls.sample_csv)

    def test_valid_csv(self):
        """
        Test loading a valid CSV file.
        """
        df = get_csv('test_file.csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertListEqual(df.columns.tolist(), ['column1', 'column2'])

    def test_invalid_type(self):
        """
        Test passing a non-string argument.
        """
        with self.assertRaises(TypeError):
            get_csv(123)

    def test_empty_string(self):
        """
        Test passing an empty string as the filename.
        """
        with self.assertRaises(ValueError):
            get_csv("")

    def test_file_not_found(self):
        """
        Test passing a filename that does not exist.
        """
        with self.assertRaises(FileNotFoundError):
            get_csv("nonexistent.csv")

class TestLoadModel(unittest.TestCase):
    """
    Test cases for the load_model function.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for the tests. Creates a sample .pkl file.
        """
        cls.test_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'modele')
        os.makedirs(cls.test_dir, exist_ok=True)
        cls.sample_model_path = os.path.join(cls.test_dir, 'test_model.pkl')

        # Create a sample model file
        sample_model = {"model": "test_model"}
        joblib.dump(sample_model, cls.sample_model_path)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after the tests are done.
        """
        if os.path.exists(cls.sample_model_path):
            os.remove(cls.sample_model_path)

    def test_valid_model(self):
        """
        Test loading a valid model file.
        """
        model = load_model('test_model.pkl')
        self.assertIsInstance(model, dict)
        self.assertEqual(model.get("model"), "test_model")

    def test_file_not_found(self):
        """
        Test when the model file does not exist.
        """
        with self.assertRaises(FileNotFoundError):
            load_model('nonexistent_model.pkl')

    def test_invalid_argument_type(self):
        """
        Test when the argument is not a string.
        """
        with self.assertRaises(TypeError):
            load_model(123)

    def test_empty_model_name(self):
        """
        Test when the model name is an empty string.
        """
        with self.assertRaises(ValueError):
            load_model("")

    def test_invalid_file_extension(self):
        """
        Test when the model name does not have a .pkl extension.
        """
        with self.assertRaises(ValueError):
            load_model('test_model.txt')

class TestExtractWords(unittest.TestCase):
    """
    Test cases for the extract_words function.
    """

    def test_regular_sentence(self):
        """
        Test splitting a regular sentence into words.
        """
        sentence = "pull coton 100 chine"
        expected_result = ["pull", "coton", "100", "chine"]
        result = extract_words(sentence)
        self.assertListEqual(result, expected_result)

    def test_empty_string(self):
        """
        Test splitting an empty string.
        """
        sentence = ""
        expected_result = []
        result = extract_words(sentence)
        self.assertListEqual(result, expected_result)

    def test_only_spaces(self):
        """
        Test splitting a string with only spaces.
        """
        sentence = "     "
        expected_result = []
        result = extract_words(sentence)
        self.assertListEqual(result, expected_result)

    def test_sentence_with_extra_spaces(self):
        """
        Test splitting a sentence with multiple spaces between words.
        """
        sentence = "   pull    coton  100   chine   "
        expected_result = ["pull", "coton", "100", "chine"]
        result = extract_words(sentence)
        self.assertListEqual(result, expected_result)

    def test_special_characters(self):
        """
        Test splitting a sentence with special characters.
        """
        sentence = "pull-coton 100!@# chine?"
        expected_result = ["pull-coton", "100!@#", "chine?"]
        result = extract_words(sentence)
        self.assertListEqual(result, expected_result)

    def test_numbers_only(self):
        """
        Test splitting a string containing only numbers.
        """
        sentence = "123 456 789"
        expected_result = ["123", "456", "789"]
        result = extract_words(sentence)
        self.assertListEqual(result, expected_result)


class TestGetIDFromName(unittest.TestCase):
    """
    Test cases for the get_id_from_name function.
    """

    def setUp(self):
        """
        Set up resources for the tests.
        """
        self.test_df = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
            'age': [25, 30, 35, 40]
        })

    def test_valid_name(self):
        """
        Test finding an ID for a valid name.
        """
        result = get_id_from_name(self.test_df, 'name', 'Bob', 'id')
        self.assertEqual(result, 2)

    def test_name_not_found(self):
        """
        Test when the name is not found in the DataFrame.
        """
        result = get_id_from_name(self.test_df, 'name', 'Eve', 'id')
        self.assertIsNone(result)

    def test_empty_dataframe(self):
        """
        Test with an empty DataFrame.
        """
        empty_df = pd.DataFrame(columns=['id', 'name', 'age'])
        result = get_id_from_name(empty_df, 'name', 'Alice', 'id')
        self.assertIsNone(result)

    def test_invalid_name_column(self):
        """
        Test with an invalid name column.
        """
        with self.assertRaises(KeyError):
            get_id_from_name(self.test_df, 'invalid_name', 'Alice', 'id')

    def test_invalid_id_column(self):
        """
        Test with an invalid ID column.
        """
        with self.assertRaises(KeyError):
            get_id_from_name(self.test_df, 'name', 'Alice', 'invalid_id')

    def test_multiple_matches(self):
        """
        Test with multiple rows matching the search value.
        """
        df_with_duplicates = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Alice', 'Alice', 'Charlie', 'Diana'],
            'age': [25, 30, 35, 40]
        })
        result = get_id_from_name(df_with_duplicates, 'name', 'Alice', 'id')
        self.assertEqual(result, 1)  # The first match is returned

    def test_case_sensitivity(self):
        """
        Test with case sensitivity in the search.
        """
        result = get_id_from_name(self.test_df, 'name', 'bob', 'id')
        self.assertIsNone(result)  # Default behavior is case-sensitive

    def test_numeric_search_value(self):
        """
        Test searching for a numeric value in a string column.
        """
        result = get_id_from_name(self.test_df, 'name', 123, 'id')
        self.assertIsNone(result)  # Numeric values shouldn't match strings


class TestGetWeightFromProduct(unittest.TestCase):
    """
    Test cases for the get_weight_from_product function.
    """

    def setUp(self):
        """
        Set up resources for the tests.
        """
        self.test_df = pd.DataFrame({
            'Type': ['chemise', 'jean', 'tshirt'],
            'XS': [150, 400, 100],
            'S': [200, 450, 120],
            'M': [250, 500, 150],
            'L': [300, 550, 180],
            'XL': [350, 600, 200],
        })

    def test_valid_product_and_size(self):
        """
        Test retrieving weight for a valid product and size.
        """
        result = get_weight_from_product(self.test_df, 'jean', 'M')
        self.assertEqual(result, 0.5)  # 500g -> 0.5kg

    def test_product_not_found(self):
        """
        Test when the product type is not found in the DataFrame.
        """
        result = get_weight_from_product(self.test_df, 'robe', 'M')
        self.assertIsNone(result)

    def test_size_not_found(self):
        """
        Test when the size column is not found in the DataFrame.
        """
        result = get_weight_from_product(self.test_df, 'jean', 'XXL')
        self.assertIsNone(result)

    def test_empty_dataframe(self):
        """
        Test with an empty DataFrame.
        """
        empty_df = pd.DataFrame(columns=['Type', 'XS', 'S', 'M', 'L', 'XL'])
        result = get_weight_from_product(empty_df, 'jean', 'M')
        self.assertIsNone(result)

    def test_invalid_product_column(self):
        """
        Test when the 'Type' column is missing.
        """
        df_missing_type = pd.DataFrame({
            'XS': [150, 400, 100],
            'S': [200, 450, 120],
            'M': [250, 500, 150],
            'L': [300, 550, 180],
            'XL': [350, 600, 200],
        })
        with self.assertRaises(KeyError):
            get_weight_from_product(df_missing_type, 'jean', 'M')

    def test_invalid_size_column(self):
        """
        Test when the specified size column is missing.
        """
        df_missing_size = pd.DataFrame({
            'Type': ['chemise', 'jean', 'tshirt'],
            'XS': [150, 400, 100],
            'S': [200, 450, 120],
            'M': [250, 500, 150],
        })  # Missing L and XL
        result = get_weight_from_product(df_missing_size, 'jean', 'L')
        self.assertIsNone(result)

    def test_multiple_matches(self):
        """
        Test behavior when there are multiple rows with the same product type.
        """
        df_with_duplicates = pd.DataFrame({
            'Type': ['jean', 'jean'],
            'XS': [400, 500],
            'S': [450, 550],
            'M': [500, 600],
            'L': [550, 650],
            'XL': [600, 700],
        })
        result = get_weight_from_product(df_with_duplicates, 'jean', 'M')
        self.assertEqual(result, 0.5)  # First match is returned

    def test_weight_conversion(self):
        """
        Test that weight conversion from grams to kilograms is correct.
        """
        result = get_weight_from_product(self.test_df, 'chemise', 'XS')
        self.assertEqual(result, 0.15)  # 150g -> 0.15kg


if __name__ == "__main__":
    unittest.main()
