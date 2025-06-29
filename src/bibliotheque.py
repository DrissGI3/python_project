from exceptions import *
import json,os
class Membre:
    def __init__(self, identifiant, nom):
        self.identifiant = identifiant
        self.nom = nom
        self.livres_empruntes = []

    def emprunter(self, livre):
           self.livres_empruntes.append(livre)

    def rendre(self, livre):
            self.livres_empruntes.remove(livre)

    def __str__(self):
        return f"{self.identifiant} - {self.nom} : \n-->livre_emprunte :{self.livres_empruntes}"
class Livre:
    def __init__(self, isbn, titre, auteur, annee, genre):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = "indisponible"

    def __str__(self):
        return f"LIVRE (ISBN: {self.isbn} | Titre: {self.titre} | Auteur: {self.auteur} | Statut: {self.statut})"
    def __repr__(self):
        return f"\nLIVRE (ISBN: {self.isbn} | Titre: {self.titre} | Auteur: {self.auteur} | Statut: {self.statut})"


class Bibliotheque :
    def __init__(self) :
        self.livres = {}
        self.membres = {}

#-------------Livre------------

    def emprunter_livre(self,membre,list_livre):
        exist_exception = False
        exception = f"❌ {membre.nom} :\n"
        if membre.identifiant not in self.membres:
            exception += f"membre non inscrit :impossible d'emprunter un livre"
            raise MembreEmpruntError(exception)
        for livre in list_livre :
            if livre.isbn in self.livres and self.livres[livre.isbn]["est_supprimer"] == "False" :
               if self.livres[livre.isbn]["quantite"] != 0 :
                   if livre in membre.livres_empruntes :
                       exist_exception = True
                       #print(f"{membre.nom} :\n+vous ne pouvez pas emprunter un meme livre 2 fois max 1 copie pour le livre {livre.titre}")
                       exception += f"+vous ne pouvez pas emprunter un meme livre 2 fois max 1 copie pour le livre{livre.titre}\n"
                   else :
                     membre.emprunter(livre)
                     print(f"livre {livre.titre} est emprunter avec succes\n")
                     self.livres[livre.isbn]["quantite"] -= 1
                     if self.livres[livre.isbn]["quantite"] == 0 :
                        livre.statut = "indisponible"
                   if livre not in self.membres[membre.identifiant]["historique_livre_emprunte"] :
                       self.membres[membre.identifiant]["historique_livre_emprunte"].append(livre)
               else  :
                   exist_exception = True
                   #print(f"+le livre : {livre.titre} n' est pas disponible maintenant\n")
                   exception += f"+le livre : {livre.titre} n' est pas disponible maintenant\n"
            else :
                exist_exception = True
                #print(f"+le livre : {livre.titre}  n'exicte pas\n")
                exception += f"+le livre : {livre.titre}  n'exicte pas\n" 
        if exist_exception == True :
            raise  LivreEmprunteError(exception)
    
    def rendre_livre(self,membre,list_livre):
        exist_exception = False
        exception = f"❌ {membre.nom} :\n"
        if membre.identifiant not in self.membres:
            exception += f"membre non inscrit :impossible de rendre un livre"
            raise MembreRendreError(exception)
        for livre in list_livre  :
            if livre.isbn in self.livres and  self.livres[livre.isbn]["est_supprimer"] == "False"   :
               if livre in membre.livres_empruntes :
                   membre.rendre(livre)
                   print(f"livre {livre.titre} est rendre avec succes\n")
                   self.livres[livre.isbn]["quantite"] += 1
                   if self.livres[livre.isbn]["quantite"] != 0 :
                        livre.statut = "disponible"
               else  :
                   if livre in self.membres[membre.identifiant]["historique_livre_emprunte"] :
                       exist_exception = True 
                    #    print(f"tu as déja rendre ce livre({livre.titre})\n")
                       exception += f"tu as déja rendre ce livre({livre.titre})\n"
                   else :
                      exist_exception = True
                    #   print(f"tu n'a jamais emprunter ce  livre : {livre.titre}\n")
                      exception += f"tu n'a jamais emprunter ce  livre : {livre.titre}\n"
            else :
                exist_exception = True
                print(f"le livre : {livre.titre}  n'exicte pas\n")
                exception += f"le livre : {livre.titre}  n'exicte pas\n"
        if exist_exception == True :
            raise  LivreRendreError(exception)

    def ajouter_livre(self,livre,quantite =0) :
        exist_exception = False
        exception = "❌ Bibliotheque :\n"
        if quantite < 0 :
            exist_exception = True
            # print(f"la quantite ne peut pas etre negative, quantite(default) = 0\n")
            exception += f"la quantite ne peut pas etre negative, quantite(default) = 0\n"
            quantite = 0
        if livre.isbn not in self.livres or (livre.isbn  in self.livres and self.livres[livre.isbn]["est_supprimer"] == "True")  :
           livre.statut = "disponible" if quantite != 0 else "indisponible"
           self.livres[livre.isbn] = {"livre":livre,"quantite":quantite,"est_supprimer":"False"}
           print(f"le livre {livre.titre} est enregistrer avec succe avec quantite = {quantite}\n")
        else :
            exist_exception = True
            # print(f"le livre avec ce isbn : {livre.isbn} existe deja \n")
            exception += f"le livre avec ce isbn : {livre.isbn} existe deja \n"
        if exist_exception == True :
            raise LivreAjoutError(exception)

    def ajouter_quantite_livre(self,livre,quantite) :
        exist_exception = False
        exception = "❌ Bibliotheque :\n"
        if livre.isbn  in self.livres and self.livres[livre.isbn]["est_supprimer"] == "False"  :
            if quantite <= 0 :
                if quantite < 0 :
                   exist_exception = True
                #    print("impossible de faire quantite negative")
                   exception += "impossible de faire quantite negative"
            else :
              livre.statut = "disponible"
              self.livres[livre.isbn]["quantite"] += quantite
              print(f"le quantite de livre {livre.titre} est changer : avant :{self.livres[livre.isbn]["quantite"]- quantite}    apres : {self.livres[livre.isbn]["quantite"]} ")
        else :
            exist_exception = True
            # print(f"impossible d'ajouter le quantite d'un livre n'existe pas\n")
            exception += f"impossible d'ajouter le quantite d'un livre n'existe pas\n"
        if exist_exception == True :
            raise LivreQuantityError(exception)
    
    def supprimer_livre_by_isbn(self,isbn) :
        exist_exception = False
        exception = "❌ Bibliotheque :\n"
        if isbn in self.livres and self.livres[isbn]["est_supprimer"] == "False"  :
            print(f"le Livre [{isbn}-{self.livres[isbn]["livre"].titre}] est supprimer avec succe")
            self.livres[isbn]["est_supprimer"] = "True"
            self.livres[isbn]["quantite"] = 0
            self.livres[isbn]["livre"].statut = "indisponible"
        else :
            exist_exception = True
            # print("deja il y'a pas ce livre\n")
            exception += "deja il y'a pas ce livre\n"
        if exist_exception == True :
            raise LivreSupprimerError(exception)

    def top_15_livres_empruntes(self,membres, livres):
        emprunts_counts = {}

        for membre_info in membres.values():
            historique = membre_info.get("historique_livre_emprunte", [])
            for livre in historique:
                if livre.isbn in livres and livres[livre.isbn]["est_supprimer"] == "False":
                    emprunts_counts[livre.isbn] = emprunts_counts.get(livre.isbn, 0) + 1

        if not emprunts_counts:
            print("Aucun emprunt enregistré.")
            return []

        top_15 = sorted(emprunts_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        return top_15

    def afficher_livre(self) :
        for isbn, info in self.livres.items():
            livre = info["livre"]
            quantite = info["quantite"]
            if self.livres[isbn]["est_supprimer"] == "True":
                print("❌:",end = "")
            print(f"{livre}| Quantité: {quantite}")
    
    def charger_livres(self, chemin="src/data/livres.json"):
        if not os.path.exists(chemin):
           raise FileNotFoundError(f"Fichier '{chemin}' introuvable.")
        with open(chemin, "r") as f:
            data = json.load(f)
            for isbn, info in data.items():
                livre = Livre(isbn, info["titre"], info["auteur"], info["annee"], info["genre"])
                self.livres[isbn] = {
                    "livre": livre,
                    "quantite": info["quantite"],
                    "est_supprimer": info["est_supprimer"],
                }
                if info["quantite"] != 0 :
                    livre.statut = "disponible"
            print("[✔] Livres chargés depuis", chemin)

    def sauvegarder_livres(self, chemin="src/data/livres.json"):
        data = {}
        for isbn, info in self.livres.items():
            livre = info["livre"]
            data[isbn] = {
                "titre": livre.titre,
                "auteur": livre.auteur,
                "annee": livre.annee,
                "genre": livre.genre,
                "quantite": info["quantite"],
                "est_supprimer": info["est_supprimer"]
            }
        with open(chemin, "w") as f:
            json.dump(data, f, indent=3)
        print("[✔] Livres sauvegardés dans", chemin)

#---------------Membre--------------

    def ajouter_membre(self,membre,list_livre = []):
        exist_exception = False
        exception = f"❌ {membre.nom} :\n"
        if membre.identifiant not in self.membres :
           self.membres[membre.identifiant] = {"membre":membre,"historique_livre_emprunte":[]}
           print(f"membre {membre.nom} est ajouter avec succee\n")
           self.emprunter_livre(membre,list_livre)
        else :
            exist_exception = True
            # print(f"cette membre {membre.nom} est deja inscrit\n")
            exception += f"cette membre {membre.nom} est deja inscrit\n"
        if exist_exception == True :
            raise MembreAjoutError(exception)
    
    def sauvegarder_membres(self, chemin="src/data/membres.json"):
        data = {}
        for identifiant, info in self.membres.items():
            membre = info["membre"]
            historique = [livre.isbn for livre in info["historique_livre_emprunte"]]
            data[identifiant] = {
                "nom": membre.nom,
                "livre_empruntes":[livre.isbn for livre in membre.livres_empruntes],
                "historique_livre_emprunte": historique
            }
        with open(chemin, "w") as f:
            json.dump(data, f, indent=4)
        print("[✔] Membres sauvegardés dans", chemin)

    def charger_membres(self, chemin="src/data/membres.json"):
        if not os.path.exists(chemin):
           raise FileNotFoundError(f"Fichier '{chemin}' introuvable.")
        try:
            with open(chemin, "r") as f:
                data = json.load(f)
                for identifiant, info in data.items():
                    membre = Membre(identifiant, info["nom"])
                    historique = []
                    for isbn in info["historique_livre_emprunte"]:
                        historique.append(self.livres[isbn]["livre"])
                    for isbn in info["livre_empruntes"]:
                        membre.livres_empruntes.append(self.livres[isbn]["livre"])
                    self.membres[identifiant] = {
                        "membre": membre,
                        "historique_livre_emprunte": historique
                    }
            print("[✔] Membres chargés depuis", chemin)
        except FileNotFoundError:
            print("[!] Aucun fichier de membres trouvé.")

    def afficher_membre(self) :
        for identifiant, info in self.membres.items() :
            membre = info["membre"]
            historique_livre_emprunte = info["historique_livre_emprunte"]
            print(f"{membre}| \n-->historique_livre_emprunte: {historique_livre_emprunte}")
