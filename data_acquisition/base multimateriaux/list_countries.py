import json

# Étape 2 : Stocker les données JSON dans une chaîne
json_data = '''
[
  {
    "code": "---",
    "name": "Pays inconnu (par défaut)"
  },
  {
    "code": "REO",
    "name": "Région - Europe de l'Ouest"
  },
  {
    "code": "REE",
    "name": "Région - Europe de l'Est"
  },
  {
    "code": "RAS",
    "name": "Région - Asie"
  },
  {
    "code": "RAF",
    "name": "Région - Afrique"
  },
  {
    "code": "RME",
    "name": "Région - Moyen-Orient"
  },
  {
    "code": "RLA",
    "name": "Région - Amérique Latine"
  },
  {
    "code": "RNA",
    "name": "Région - Amérique du nord"
  },
  {
    "code": "ROC",
    "name": "Région - Océanie"
  },
  {
    "code": "MM",
    "name": "Myanmar"
  },
  {
    "code": "BD",
    "name": "Bangladesh"
  },
  {
    "code": "CN",
    "name": "Chine"
  },
  {
    "code": "FR",
    "name": "France"
  },
  {
    "code": "IN",
    "name": "Inde"
  },
  {
    "code": "KH",
    "name": "Cambodge"
  },
  {
    "code": "MA",
    "name": "Maroc"
  },
  {
    "code": "PK",
    "name": "Pakistan"
  },
  {
    "code": "TN",
    "name": "Tunisie"
  },
  {
    "code": "TR",
    "name": "Turquie"
  },
  {
    "code": "VN",
    "name": "Vietnam"
  }
]
'''

# Étape 3 : Convertir la chaîne JSON en objet Python
data = json.loads(json_data)

# Étape 4 : Extraire la liste des 'id'
code_countries_list = [item['code'] for item in data]


