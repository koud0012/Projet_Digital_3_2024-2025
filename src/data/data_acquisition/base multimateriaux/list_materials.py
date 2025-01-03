import json

# Étape 2 : Stocker les données JSON dans une chaîne
json_data = '''
[
  {
    "id": "coton-rdpc",
    "name": "Production de coton recyclé (recyclage mécanique) pré-filature, traitement de déchets textiles post-consommation, inventaire partiellement agrégé"
  },
  {
    "id": "coton-rdp",
    "name": "Production de coton recyclé (recyclage mécanique) pré-filature, traitement de déchets de production textiles, inventaire partiellement agrégé"
  },
  {
    "id": "ei-chanvre",
    "name": "Chanvre"
  },
  {
    "id": "ei-coton",
    "name": "Coton"
  },
  {
    "id": "ei-coton-organic",
    "name": "Coton biologique"
  },
  {
    "id": "elasthane",
    "name": "Elasthane (Lycra)"
  },
  {
    "id": "ei-acrylique",
    "name": "Acrylique"
  },
  {
    "id": "ei-jute-kenaf",
    "name": "Jute"
  },
  {
    "id": "ei-laine-par-defaut",
    "name": "Laine par défaut"
  },
  {
    "id": "ei-laine-nouvelle-filiere",
    "name": "Laine nouvelle filière"
  },
  {
    "id": "ei-lin",
    "name": "Lin"
  },
  {
    "id": "ei-pa",
    "name": "Nylon"
  },
  {
    "id": "ei-pp",
    "name": "Polypropylène"
  },
  {
    "id": "ei-pet",
    "name": "Polyester"
  },
  {
    "id": "ei-pet-r",
    "name": "Polyester recyclé"
  },
  {
    "id": "ei-viscose",
    "name": "Viscose"
  }
]
'''

# Étape 3 : Convertir la chaîne JSON en objet Python
data = json.loads(json_data)

# Étape 4 : Extraire la liste des 'id'
id_materials_list = [item['id'] for item in data]

