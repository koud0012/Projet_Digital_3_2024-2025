import random
import sys
from itertools import combinations

def generer_partitions(n, k):
    """
    Gènère n partitions aléatoires de la quantité 1 en k parts.

    Args:
        n (int): Nombre de partitions.
        k (int): Nombre de parts dans chaque partition.

    Returns:
        list: Liste contenant n sous-listes de k valeurs dont la somme = 1.
    """
    partitions = []
    for _ in range(n):
        parts = sorted([random.uniform(0, 1) for _ in range(k - 1)])
        parts = [parts[0]] + [parts[i] - parts[i-1] for i in range(1, len(parts))] + [1 - parts[-1]]
        parts = [round(part, 4) for part in parts]  # Limite à 2 décimales
        partitions.append(parts)
    

    txt_filename = f"table_n_{n}_k_{k}.py"
    
    with open(txt_filename, 'w') as f:
        # Redirect standard output to the file
        original_stdout = sys.stdout
        sys.stdout = f
    
        print(f"table_n_{n}_k_{k} = {partitions}")
        
    # Restore standard output
    sys.stdout = original_stdout
    
    return partitions

def generer_partitions_1(n, k):
    """
    Gènère n partitions aléatoires de la quantité 1 en k parts.

    Args:
        n (int): Nombre de partitions.
        k (int): Nombre de parts dans chaque partition.

    Returns:
        list: Liste contenant n sous-listes de k valeurs dont la somme = 1.
    """
    partitions = []
    for _ in range(n):
        parts = [1]  # Limite à 2 décimales
        partitions.append(parts)
    

    txt_filename = f"table_n_{n}_k_{k}.py"
    
    with open(txt_filename, 'w') as f:
        # Redirect standard output to the file
        original_stdout = sys.stdout
        sys.stdout = f
    
        print(f"table_n_{n}_k_{k} = {partitions}")
        
    # Restore standard output
    sys.stdout = original_stdout
    
    return partitions



def combinaisons_k_parmi_n(n, k):
    """
    Renvoie toutes les combinaisons de k éléments parmi n.

    Args:
        n (int): Total des éléments.
        k (int): Nombre d'éléments à choisir.

    Returns:
        list: Liste des combinaisons possibles sous forme de listes.
    """
    resultat = [list(comb) for comb in combinations(range(n), k)]
    
    txt_filename = f"table_k_{k}_parmi_n_{n}.py"

    with open(txt_filename, 'w') as f:
        # Redirect standard output to the file
        original_stdout = sys.stdout
        sys.stdout = f

        print(f"table_k_{k}_parmi_n_{n} = {resultat}")
        
    # Restore standard output
    sys.stdout = original_stdout

    return resultat

# Exemple d'utilisation de generer_partitions
# n = 176
# k = 1
# resultat = generer_partitions_1(n, k)
# # print(resultat)

# # Exemple d'utilisation de combinaisons_k_parmi_n
# total_elements = 16
# k_elements = 1
# combinaisons = combinaisons_k_parmi_n(total_elements, k_elements)
# # print("Combinaisons de k parmi n :", combinaisons)