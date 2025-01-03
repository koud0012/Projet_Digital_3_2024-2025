import json

# Étape 2 : Stocker les données JSON dans une chaîne
json_data = '''
[
  {
    "id": "chemise",
    "name": "Chemise"
  },
  {
    "id": "jean",
    "name": "Jean"
  },
  {
    "id": "jupe",
    "name": "Jupe / Robe"
  },
  {
    "id": "manteau",
    "name": "Manteau / Veste"
  },
  {
    "id": "pantalon",
    "name": "Pantalon / Short"
  },
  {
    "id": "pull",
    "name": "Pull"
  },
  {
    "id": "tshirt",
    "name": "T-shirt / Polo"
  },
  {
    "id": "chaussettes",
    "name": "Chaussettes"
  },
  {
    "id": "calecon",
    "name": "Caleçon (tissé)"
  },
  {
    "id": "slip",
    "name": "Boxer / Slip (tricoté)"
  },
  {
    "id": "maillot-de-bain",
    "name": "Maillot de bain"
  }
]
'''

# Étape 3 : Convertir la chaîne JSON en objet Python
data = json.loads(json_data)

# Étape 4 : Extraire la liste des 'id'
id_product_list = [item['id'] for item in data]

