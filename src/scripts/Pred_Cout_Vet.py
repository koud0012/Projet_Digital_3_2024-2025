import sys

def traiter_note(caracteristiques):
    return f"Notation de votre vetement : {caracteristiques}"

def extraire_mots(phrase):
  mots = phrase.split()
  return mots

def model(liste_mots):
   if liste_mots[1] == "France":
      return f"Parfait"
   else:
      return f"Bof"

if __name__ == "__main__":
  user_input = sys.argv[1] 
  liste_mots = extraire_mots(user_input)
  Note = model(liste_mots)
  print(traiter_note(Note))