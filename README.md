# Evaluation du coût environnemental d'un vêtement


## Objectif du projet

L’objectif de notre application est d'aider toute personne qui le souhaite à pouvoir évaluer le coût environnemental de son vêtement. 


## Structure du dépôt

Le dépôt est structuré de la manière suivante : 

- Le dossier `Docs`comprend le rapport final de notre projet ;  
- Le dossier `models` qui contient les données et les scripts Python qui ont permis d’élaborer les modèles de prédiction ;  
- Le dossier `src`contient l’ensemble des scripts Python destinés à la science des données et à la manipulation des données. Ce répertoire comprend :  
  - Le sous-dossier `app` qui comprend les scripts et les fonctions ;  
  - Le sous-dossier `data` comprend des fichiers Excel au format `.csv` qui représentent les dictionnaires des données de notre projet ;  
  - Le fichier `interface`, fichiers Excel au format `.xlsm` qui représente l'interface de notre application ;   
- Le dossier `tests` contient l’ensemble des tests unitaires réalisés sur nos scripts Python afin de s’assurer du bon fonctionnement de ces derniers et améliorer la qualité du code ;   
- Le dossier `vizualisation` contient le script ayant permis à l'analyse des données ;  
- Le fichier `README.md ` décrit l’organisation et l’utilisation du projet ;  
- Le fichier `requirements.txt`:Recense les paquets Python nécessaires pour exécuter notre application.


## Comment configurer 
### Prérequis
Assurez-vous d'avoir installé Python sur votre machine. Si ce n'est pas le cas, vous pouvez le télécharger depuis le site officiel de Python.
### Installation des dépendances
1. Ajoutez le chemin d'installation de Python à la variable d'environnement `PYTHON_HOME`. Vous pouvez le faire en suivant ces étapes :
   
   - Sur Windows :
     - Allez dans les Paramètres système avancés.
     - Cliquez sur "Variables d'environnement".
     - Dans la section "Variables système", recherchez la variable "Path" et cliquez sur "Modifier".
     - Cliquez sur "Nouveau" et ajoutez le chemin d'installation de Python (par exemple, `C:\Python39`).
     - Cliquez sur "OK" pour fermer les fenêtres.

   - Sur Linux/Mac :
     - Ouvrez votre fichier de profil shell (comme `~/.bashrc` ou `~/.zshrc`).
     - Ajoutez la ligne suivante :
       ```bash
       export PYTHON_HOME=/chemin/vers/votre/python
       ```
     - Sourcez votre fichier de profil ou redémarrez votre terminal.
2. Exécutez la commande suivante depuis votre terminal pour installer les dépendances nécessaires à l'aide du fichier `requirements.txt` :

```markdown
pip install -r requirements.txt
```
## Comment éxecuter  
Pour utiliser cette application, suivez les étapes ci-dessous :  
- ouvrez le fichier `interface.xlmx` du dossier `interface` ;  
- cliquez sur le bouton ‘Formulaire' ;  
- cliquez sur l’un des boutons entre ‘Haut de corps’,’ Bas du corps’ et ‘Divers’ afin de sélectionner le type de vêtement dont vous souhaitez évaluer le coût environnemental ;  
- remplissez le formulaire ;  
- cliquez ensuite sur le bouton ‘Analyse’ afin d'avoir les résultats.


## Contributeurs

Les contributeurs de ce projet sont des étudiants du master « Statistique pour l’Évaluation et la Prévision » (SEP) de l’Université de Reims Champagne-Ardenne (promotion 2024-2025). 

Leurs noms et leurs rôles sont les suivants: 
- Christelle KOUDORO : Product Owner ;   
- Bastien DEMARIN : Data Engineer et Scrum Master ;  
- Ruxandra ILIESCU : Data Analyst/Data Governance ;   
- Nicolas YACKOB : Data Scientist ;  
- Killian NICOLAS : Front End/User Interface.

## Contacts

Si vous avez des questions ou des remarques sur l'application, vous pouvez nous contacter ici :[fjchristellekoudoro@gmail.com], [bastiendemarin@gmail.com], [ruxandracristianailiescu@gmail.com], [yackobnicolas@gmail.com], [killian7nicolas@gmail.com]

  ----
