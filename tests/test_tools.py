import pytest
import joblib
import pandas as pd
from src.app.tools import get_category_code, get_csv, load_model, extract_words, get_id_from_name, get_weight_from_product


@pytest.fixture(scope="module")
def sample_csv(tmp_path_factory):
    """
    Fixture to create a temporary CSV file in a normalized path.
    """
    temp_dir = tmp_path_factory.mktemp("data")  # Crée un répertoire temporaire sécurisé
    csv_path = temp_dir / "test_file.csv"  # Nom du fichier dans ce répertoire
    df = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })
    df.to_csv(csv_path, index=False)  # Crée un fichier CSV
    return str(csv_path)  # Retourne le chemin complet du fichier



@pytest.fixture(scope="module")
def sample_model_file(tmp_path_factory):
    """
    Fixture to create a temporary .pkl file in a normalized path.
    """
    temp_dir = tmp_path_factory.mktemp("models")  # Crée un répertoire temporaire sécurisé
    model_path = temp_dir / "test_model.pkl"  # Nom du fichier dans ce répertoire
    sample_model = {"model": "test_model"}
    joblib.dump(sample_model, model_path)  # Sauvegarde un modèle fictif
    return str(model_path)  # Retourne le chemin complet du fichier


def test_valid_csv(sample_csv):
    """
    Test loading a valid CSV file.
    """
    df = get_csv(sample_csv)  # Passez le chemin complet
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ['column1', 'column2']

def test_invalid_type():
    """
    Test passing a non-string argument.
    """
    with pytest.raises(TypeError):
        get_csv(123)


def test_empty_string():
    """
    Test passing an empty string as the filename.
    """
    with pytest.raises(ValueError):
        get_csv("")


def test_file_not_found():
    """
    Test passing a filename that does not exist.
    """
    with pytest.raises(FileNotFoundError):
        get_csv("nonexistent.csv")


def test_valid_model(sample_model_file):
    """
    Test loading a valid model file.
    """
    model = load_model(sample_model_file)  # Passez le chemin complet
    assert isinstance(model, dict)
    assert model.get("model") == "test_model"


def test_model_file_not_found():
    """
    Test when the model file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        load_model('nonexistent_model.pkl')


def test_model_invalid_argument_type():
    """
    Test when the argument is not a string.
    """
    with pytest.raises(TypeError):
        load_model(123)


def test_model_empty_model_name():
    """
    Test when the model name is an empty string.
    """
    with pytest.raises(ValueError):
        load_model("")


def test_model_invalid_file_extension():
    """
    Test when the model name does not have a .pkl extension.
    """
    with pytest.raises(ValueError):
        load_model('test_model.txt')


@pytest.mark.parametrize("sentence, expected_result", [
    ("pull coton 100 chine", ["pull", "coton", "100", "chine"]),
    ("", []),
    ("     ", []),
    ("   pull    coton  100   chine   ", ["pull", "coton", "100", "chine"]),
    ("pull-coton 100!@# chine?", ["pull-coton", "100!@#", "chine?"]),
    ("123 456 789", ["123", "456", "789"]),
])
def test_extract_words(sentence, expected_result):
    """
    Test splitting sentences with various cases.
    """
    result = extract_words(sentence)
    assert result == expected_result


@pytest.fixture
def sample_dataframe():
    """
    Fixture to provide a sample DataFrame.
    """
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 40]
    })


def test_get_id_from_name_valid(sample_dataframe):
    """
    Test finding an ID for a valid name.
    """
    result = get_id_from_name(sample_dataframe, 'name', 'Bob', 'id')
    assert result == 2


def test_get_id_from_name_not_found(sample_dataframe):
    """
    Test when the name is not found in the DataFrame.
    """
    result = get_id_from_name(sample_dataframe, 'name', 'Eve', 'id')
    assert result is None


def test_get_weight_from_product():
    """
    Test retrieving weight for a valid product and size.
    """
    test_df = pd.DataFrame({
        'Type': ['chemise', 'jean', 'tshirt'],
        'XS': [150, 400, 100],
        'S': [200, 450, 120],
        'M': [250, 500, 150],
        'L': [300, 550, 180],
        'XL': [350, 600, 200],
    })
    result = get_weight_from_product(test_df, 'jean', 'M')
    assert result == 0.5  # 500g -> 0.5kg

