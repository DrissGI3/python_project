from bibliotheque import Bibliotheque,Livre,Membre
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import tkinter as tk
import random
from tkinter import messagebox
from exceptions import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
couleurs = [
    '#00ced1',  # DarkTurquoise
    '#4682b4',  # SteelBlue
    '#dc143c',  # Crimson
    '#7fffd4',  # Aquamarine
    '#ff69b4',  # HotPink
    '#708090',  # SlateGray
    '#00fa9a',  # MediumSpringGreen
    '#ff4500',  # OrangeRed
    '#6a5acd',  # SlateBlue
    '#20b2aa',  # LightSeaGreen
    '#d2691e',  # Chocolate
    '#ff1493',  # DeepPink
    '#2e8b57',  # SeaGreen
    '#f0e68c',  # Khaki
    '#8b0000',  # DarkRed
    '#ffdead',  # NavajoWhite
    '#9932cc',  # DarkOrchid
    '#00bfff',  # DeepSkyBlue
    '#adff2f',  # GreenYellow
    '#b0c4de',  # LightSteelBlue
    '#da70d6',  # Orchid
    '#7b68ee',  # MediumSlateBlue
    '#ff6347',  # Tomato
    '#afeeee',  # PaleTurquoise
    '#40e0d0'   # Turquoise
]

class App(tk.Tk):
    def __init__(self,bib):
        super().__init__()

        self.title("Bibliothèque")
        self.state('zoomed')  # Mode plein écran
        self.bib = bib

        # Conteneur principal
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Barre de navigation
        self.menu_bar = tk.Frame(self.container, bg="#E8CB82", height=50)
        self.menu_bar.pack(side="top", fill="x")

        self.frames = {}

        # Créer les frames
        for FrameClass in (LivreFrame, MembreFrame, VisualisationFrameLivre1,VisualisationFrameLivre2,VisualisationFrameMembre):
            page_name = FrameClass.__name__
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.92)

        # Créer les boutons de navigation
        buttons = [
            ("Livres", "LivreFrame"),
            ("Membres", "MembreFrame"),
            ("Visualisation Livre(1)", "VisualisationFrameLivre1"),
            ("Visualisation Livre(2)", "VisualisationFrameLivre2"),
            ("Visualisation Membre & Author", "VisualisationFrameMembre")
        ]

        for idx, (text, frame_name) in enumerate(buttons):
            btn = tk.Button(self.menu_bar, text=text, bg="#6EA5D9", fg="white",
                            activebackground="#1abc9c", padx=20, pady=10,
                            command=lambda name=frame_name: self.show_frame(name))
            btn.pack(side="left", padx=2, pady=5)

        self.show_frame("LivreFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class VisualisationFrameMembre(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")


        # Extraire les livres valides (non supprimés)
        emprunts_par_membre = [
        (info["membre"].nom, len(info.get("historique_livre_emprunte", [])))
        for info in bib.membres.values()
        ]

    # Trier par ordre décroissant du nombre d'emprunts
        emprunts_par_membre.sort(key=lambda x: x[1], reverse=True)

    # Prendre les top N membres
        top = emprunts_par_membre[:15]

    # Séparer les noms et les nombres d'emprunts
        noms = [nom for nom, count in top]
        nb_emprunts = [count for _, count in top]
    # Affichage du graphique
        fig1, ax1 = plt.subplots()
        ax1.bar(noms, nb_emprunts, color = couleurs)
        ax1.set_title("Top Membres les Plus Actifs", pad=20)
        ax1.set_xlabel("Nom du Membre")
        ax1.set_ylabel("Nombre Total d'Emprunts")
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()



        # Chart 3: Pie chart of product data
        titres = []
        emprunts = []
        Top_15_livres = bib.top_15_livres_empruntes(bib.membres,bib.livres)
        for isbn, nombre_emprunts in Top_15_livres:
            titres.append(bib.livres[isbn]["livre"].auteur)
            emprunts.append(nombre_emprunts)

    

        fig2, ax2 = plt.subplots()
        ax2.bar(titres, emprunts, color=couleurs[:len(titres)])
        ax2.set_title("Top des Auteurs les Plus Populaires", pad=20)
        ax2.set_xlabel("Auteur")
        ax2.set_ylabel("Nombre total d'emprunts")
        ax2.tick_params(axis='x', rotation=45)
        fig2.tight_layout()


        # Affichage dans la frame
        charts_frame = tk.Frame(self, bg="white")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)

        upper_frame = tk.Frame(charts_frame, bg="white")
        upper_frame.pack(fill="both", expand=True)

        for fig in (fig1, fig2):
            canvas = FigureCanvasTkAgg(fig, master=upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10, pady=10)

class VisualisationFrameLivre1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")


        # Extraire les livres valides (non supprimés)
        livres_valides = [
            (info["livre"].titre, info["quantite"])
            for info in bib.livres.values()
            if info.get("est_supprimer", "False") == "False"
        ]

        # Trier par quantité décroissante
        livres_valides.sort(key=lambda x: x[1], reverse=True)

        # Limiter à 25 livres maximum
        livres_valides = livres_valides[:15]

        # Extraire titres et quantités
        titres = [titre for titre, _ in livres_valides]
        quantites = [quantite for _, quantite in livres_valides]

        # Mélanger les couleurs dans l’ordre des livres
        couleurs_dispo = couleurs[:len(titres)]
        random.shuffle(couleurs_dispo)

        # Paramètres de style


        # Affichage du graphique
        fig1, ax1 = plt.subplots()
        ax1.bar(titres, quantites, color=couleurs_dispo)
        ax1.set_xlabel("Titre du Livre", labelpad=15)
        ax1.set_ylabel("Quantité Disponible", labelpad=20)
        ax1.set_title("Les Livres les plus Disponibles", pad=25)
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()



        # Chart 3: Pie chart of product data
        genre_counts = {}

        # Compter les livres valides par genre
        for info in bib.livres.values():
            livre = info["livre"]
            genre = livre.genre
            quantite = info["quantite"]

            if info.get("est_supprimer", "False") == "False" and quantite != 0:
                genre_counts[genre] = genre_counts.get(genre, 0) + quantite

        # Cas où aucun livre valide n'existe
        if not genre_counts:
            genre_counts = {"aucun livre": 100}

        # Si plus de 10 genres, prendre 9 plus grands + "Autres"
        if len(genre_counts) > 9:
            sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
            top_9 = sorted_genres[:8]
            autres = sorted_genres[8:]
            autres_total = sum(q for _, q in autres)
            top_genres = top_9 + [(f"Autre", autres_total)]
        else:
            top_genres = genre_counts.items()

        # Mélanger les éléments pour désordonner visuellement
        items = list(top_genres)
        random.shuffle(items)

        # Séparer labels et valeurs
        labels = [label for label, _ in items]
        sizes = [size for _, size in items]


        random.shuffle(couleurs)

        # Affichage du graphique
        fig3, ax3 = plt.subplots()
        #ax3.pie(product_data.values(), labels=product_data.keys(), autopct='%1.1f%%')
        ax3.pie(sizes, labels=labels, autopct="%1.1f%%", colors=couleurs[:len(labels)], startangle=120)
        ax3.set_title("Répartition des Livres par Genre", pad=25)

        # Affichage dans la frame
        charts_frame = tk.Frame(self, bg="white")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)

        upper_frame = tk.Frame(charts_frame, bg="white")
        upper_frame.pack(fill="both", expand=True)

        for fig in (fig1, fig3):
            canvas = FigureCanvasTkAgg(fig, master=upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10, pady=10)

class VisualisationFrameLivre2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")


        # Chart 2: Horizontal bar chart of inventory data
        titres = []
        emprunts = []
        Top_15_livres = bib.top_15_livres_empruntes(bib.membres,bib.livres)
        for isbn, nombre_emprunts in Top_15_livres:
            titres.append(bib.livres[isbn]["livre"].titre)
            emprunts.append(nombre_emprunts)


        fig2, ax2 = plt.subplots()
        ax2.bar(titres, emprunts, color=couleurs[:len(titres)])
        ax2.set_xlabel("Titres des Livres", labelpad=15)
        ax2.set_ylabel("Nombre d'Emprunts", labelpad=20)
        ax2.set_title("Top des Livres les Plus Empruntés", pad=25)
        ax2.tick_params(axis='x', rotation=45)
        fig2.tight_layout()


        # Extraire les livres valides (non supprimés)
        livres_valides = [
        (info["livre"].titre, info["quantite"])
        for info in bib.livres.values()
        if info.get("est_supprimer", "False") == "False"
        ]

    # Trier par quantité **croissante**
        livres_valides.sort(key=lambda x: x[1])

    # Limiter à 25 livres minimum
        livres_valides = livres_valides[:15]

    # Extraire titres et quantités
        titres = [titre for titre, _ in livres_valides]
        quantites = [quantite for _, quantite in livres_valides]

    # Couleurs (aléatoirement)
        couleurs_dispo = couleurs[:len(titres)]
        random.shuffle(couleurs_dispo)

    # Style matplotlib

    # Affichage du graphique
        fig4, ax4 = plt.subplots()
        ax4.bar(titres, quantites, color=couleurs)
        ax4.set_xlabel("Titre du Livre", labelpad=15)
        ax4.set_ylabel("Quantité Disponible", labelpad=20)
        ax4.set_title("Les Livres les Moins Disponibles", pad=25)
        ax4.tick_params(axis='x', rotation=45)
        fig4.tight_layout()

        # Affichage dans la frame
        charts_frame = tk.Frame(self, bg="white")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)

        upper_frame = tk.Frame(charts_frame, bg="white")
        upper_frame.pack(fill="both", expand=True)

        for fig in (fig2, fig4):
            canvas = FigureCanvasTkAgg(fig, master=upper_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10, pady=10)

class LivreFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.bib = controller.bib

        # -------------------- Partie 1 : Liste des livres --------------------
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill="both", expand=True)

        search_frame = tk.Frame(top_frame, bg="white")
        search_frame.pack(anchor="w", padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Rechercher un livre :", bg="white", font=("Arial", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)

        columns = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Quantité")
        self.tree = ttk.Treeview(top_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        section_ajoute_livre = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")
        section_supprimer = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")
        section_ajoute_quantite = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")

        for section in [section_ajoute_livre, section_supprimer, section_ajoute_quantite]:
            section.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        tk.Label(section_ajoute_livre, text="Ajouter un Livre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)

        form_frame = tk.Frame(section_ajoute_livre, bg="white")
        form_frame.pack(padx=10, pady=5)

        tk.Label(form_frame, text="ISBN:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_isbn_ajout = tk.Entry(form_frame)
        self.entry_isbn_ajout.grid(row=1, column=0, padx=50, pady=2)

        tk.Label(form_frame, text="Titre:", bg="white").grid(row=2, column=0, sticky="w")
        self.entry_nom_ajout = tk.Entry(form_frame)
        self.entry_nom_ajout.grid(row=3, column=0, padx=5, pady=2)

        tk.Label(form_frame, text="Auteur:", bg="white").grid(row=4, column=0, sticky="w")
        self.entry_auteur_ajout = tk.Entry(form_frame)
        self.entry_auteur_ajout.grid(row=5, column=0, padx=5, pady=2)

        tk.Label(form_frame, text="Année:", bg="white").grid(row=0, column=1, sticky="w")
        self.entry_annee_ajout = tk.Entry(form_frame)
        self.entry_annee_ajout.grid(row=1, column=1, padx=50, pady=2)

        tk.Label(form_frame, text="Genre:", bg="white").grid(row=2, column=1, sticky="w")
        self.entry_genre_ajout = tk.Entry(form_frame)
        self.entry_genre_ajout.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Quantité:", bg="white").grid(row=4, column=1, sticky="w")
        self.entry_quantite_ajout = tk.Entry(form_frame)
        self.entry_quantite_ajout.grid(row=5, column=1, padx=5, pady=2)

        tk.Label(section_supprimer, text="Supprimer un livre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_supprimer, text="ISBN:", bg="white").pack()
        self.entry_isbn_supprimer = tk.Entry(section_supprimer)
        self.entry_isbn_supprimer.pack(pady=2)

        tk.Label(section_ajoute_quantite, text="Ajouter Quantité", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_ajoute_quantite, text="ISBN:", bg="white").pack()
        self.entry_isbn_quantite = tk.Entry(section_ajoute_quantite)
        self.entry_isbn_quantite.pack(pady=2)

        tk.Label(section_ajoute_quantite, text="Quantité à ajouter:", bg="white").pack()
        self.entry_quantite_ajouter = tk.Entry(section_ajoute_quantite)
        self.entry_quantite_ajouter.pack(pady=2)

        tk.Button(section_ajoute_livre, text="➕ Ajouter", bg="#4CAF50", fg="white", command=self.ajouter_livre).pack(pady=5)
        tk.Button(section_supprimer, text="🔟 Supprimer", bg="#ED4040", fg="white", command=self.supprimer_livre).pack(pady=5)
        tk.Button(section_ajoute_quantite, text="↩️ Ajouter", bg="#FF5722", fg="white", command=self.ajouter_quantite).pack(pady=5)

        self.mettre_a_jour_tableau()

    def mettre_a_jour_tableau(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for isbn, info in self.bib.livres.items():
            livre = info["livre"]
            if info["est_supprimer"] == "False":
                self.tree.insert("", "end", values=(
                    livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, info["quantite"]
                ))

    def ajouter_livre(self):
        try:
            livre = Livre(
                self.entry_isbn_ajout.get(),
                self.entry_nom_ajout.get(),
                self.entry_auteur_ajout.get(),
                int(self.entry_annee_ajout.get()),
                self.entry_genre_ajout.get()
            )
            quantite = int(self.entry_quantite_ajout.get())
            self.bib.ajouter_livre(livre, quantite)
            self.mettre_a_jour_tableau()
            self.bib.sauvegarder_livres()
            messagebox.showinfo("Succès", "Livre ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_livre(self):
        isbn = self.entry_isbn_supprimer.get()
        try:
            self.bib.supprimer_livre_by_isbn(isbn)
            self.mettre_a_jour_tableau()
            self.bib.sauvegarder_livres()
            messagebox.showinfo("Succès", "Livre supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def ajouter_quantite(self):
        isbn = self.entry_isbn_quantite.get()
        try:
            quantite = int(self.entry_quantite_ajouter.get())
            if isbn not in self.bib.livres:
                raise ValueError("Le livre n'existe pas")
            livre = self.bib.livres[isbn]["livre"]
            self.bib.ajouter_quantite_livre(livre, quantite)
            self.mettre_a_jour_tableau()
            self.bib.sauvegarder_livres()
            messagebox.showinfo("Succès", "Quantité ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.bib = controller.bib  # on accède à l'objet Bibliotheque via App

        # ... [interface comme tu l'as déjà fait] ...
        # -------------------- Partie 1 : Liste des livres --------------------
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill="both", expand=True)

        # Barre de recherche
        search_frame = tk.Frame(top_frame, bg="white")
        search_frame.pack(anchor="w", padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Rechercher un livre :", bg="white", font=("Arial", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)

        # Tableau
        columns = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Quantité")
        self.tree = ttk.Treeview(top_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # -------------------- Partie 2 : Gestion des actions --------------------
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        # Sous-sections horizontales
        section_ajoute_livre = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")
        section_supprimer = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")
        section_ajoute_quantite = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")

        for section in [section_ajoute_livre, section_supprimer, section_ajoute_quantite]:
            section.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # -------- Ajouter un Livre --------
        tk.Label(section_ajoute_livre, text="Ajouter un Livre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)

        form_frame = tk.Frame(section_ajoute_livre, bg="white")
        form_frame.pack(padx=10, pady=5)

        # Colonne 1
        tk.Label(form_frame, text="ISBN:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_isbn_ajout = tk.Entry(form_frame)
        self.entry_isbn_ajout.grid(row=1, column=0, padx=50, pady=2)

        tk.Label(form_frame, text="Titre:", bg="white").grid(row=2, column=0, sticky="w")
        self.entry_nom_ajout = tk.Entry(form_frame)
        self.entry_nom_ajout.grid(row=3, column=0, padx=5, pady=2)

        tk.Label(form_frame, text="Auteur:", bg="white").grid(row=4, column=0, sticky="w")
        self.entry_auteur_ajout = tk.Entry(form_frame)
        self.entry_auteur_ajout.grid(row=5, column=0, padx=5, pady=2)

        # Colonne 2
        tk.Label(form_frame, text="Année:", bg="white").grid(row=0, column=1, sticky="w")
        self.entry_annee_ajout = tk.Entry(form_frame)
        self.entry_annee_ajout.grid(row=1, column=1, padx=50, pady=2)

        tk.Label(form_frame, text="Genre:", bg="white").grid(row=2, column=1, sticky="w")
        self.entry_genre_ajout = tk.Entry(form_frame)
        self.entry_genre_ajout.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Quantité:", bg="white").grid(row=4, column=1, sticky="w")
        self.entry_quantite_ajout = tk.Entry(form_frame)
        self.entry_quantite_ajout.grid(row=5, column=1, padx=5, pady=2)

        #tk.Button(section_ajoute_livre, text="➕ Ajouter", bg="#4CAF50", fg="white").pack(pady=5)

        # -------- Supprimer un livre --------
        tk.Label(section_supprimer, text="Supprimer un livre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_supprimer, text="ISBN:", bg="white").pack()
        self.entry_isbn_supprimer = tk.Entry(section_supprimer)
        self.entry_isbn_supprimer.pack(pady=2)
        #tk.Button(section_supprimer, text="🗑️ Supprimer", bg="#ED4040", fg="white").pack(pady=5)

        # -------- Ajouter Quantité --------
        tk.Label(section_ajoute_quantite, text="Ajouter Quantité", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_ajoute_quantite, text="ISBN:", bg="white").pack()
        self.entry_isbn_quantite = tk.Entry(section_ajoute_quantite)
        self.entry_isbn_quantite.pack(pady=2)

        tk.Label(section_ajoute_quantite, text="Quantité à ajouter:", bg="white").pack()
        self.entry_quantite_ajouter = tk.Entry(section_ajoute_quantite)
        self.entry_quantite_ajouter.pack(pady=2)

        #tk.Button(section_ajoute_quantite, text="↩️ Ajouter", bg="#FF5722", fg="white").pack(pady=5)
        # Remplace les boutons sans action par ceux qui appellent une fonction
        tk.Button(section_ajoute_livre, text="➕ Ajouter", bg="#4CAF50", fg="white", command=self.ajouter_livre).pack(pady=5)
        tk.Button(section_supprimer, text="🔟 Supprimer", bg="#ED4040", fg="white", command=self.supprimer_livre).pack(pady=5)
        tk.Button(section_ajoute_quantite, text="↩️ Ajouter", bg="#FF5722", fg="white", command=self.ajouter_quantite).pack(pady=5)

        self.mettre_a_jour_tableau()

    def mettre_a_jour_tableau(self):
        # Vider l'ancien contenu
        for item in self.tree.get_children():
            self.tree.delete(item)

        for isbn, info in self.bib.livres.items():
            livre = info["livre"]
            if info["est_supprimer"] == "False":
                self.tree.insert("", "end", values=(
                    livre.isbn,
                    livre.titre,
                    livre.auteur,
                    livre.annee,
                    livre.genre,
                    info["quantite"]
                ))

    def ajouter_livre(self):
        try:
            livre = Livre(
                self.entry_isbn_ajout.get(),
                self.entry_nom_ajout.get(),
                self.entry_auteur_ajout.get(),
                int(self.entry_annee_ajout.get()),
                self.entry_genre_ajout.get()
            )
            quantite = int(self.entry_quantite_ajout.get())
            self.bib.ajouter_livre(livre, quantite)
            self.mettre_a_jour_tableau()
            messagebox.showinfo("Succès", "Livre ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_livre(self):
        isbn = self.entry_isbn_supprimer.get()
        try:
            self.bib.supprimer_livre_by_isbn(isbn)
            self.mettre_a_jour_tableau()
            messagebox.showinfo("Succès", "Livre supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def ajouter_quantite(self):
        isbn = self.entry_isbn_quantite.get()
        try:
            quantite = int(self.entry_quantite_ajouter.get())
            livre = self.bib.livres[isbn]["livre"]
            self.bib.ajouter_quantite_livre(livre, quantite)
            self.mettre_a_jour_tableau()
            messagebox.showinfo("Succès", "Quantité ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

class MembreFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # -------------------- Partie 1 : Liste des membres --------------------
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill="both", expand=True)

        # Barre de recherche
        search_frame = tk.Frame(top_frame, bg="white")
        search_frame.pack(anchor="w", padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Rechercher un membre :", bg="white", font=("Arial", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)

        # Tableau
        columns = ("ISBN", "Nom", "Historique")
        self.tree = ttk.Treeview(top_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # -------------------- Partie 2 : Gestion des actions --------------------
        bottom_frame = tk.Frame(self, bg="#f0f0f0", height=200)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        section_ajouter = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")
        section_emprunter = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")
        section_rendre = tk.Frame(bottom_frame, bg="#ffffff", bd=1, relief="solid")

        for section in [section_ajouter, section_emprunter, section_rendre]:
            section.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # -------- Ajouter un membre --------
        tk.Label(section_ajouter, text="Ajouter un membre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_ajouter, text="ISBN:", bg="white").pack()
        self.entry_isbn_ajout = tk.Entry(section_ajouter)
        self.entry_isbn_ajout.pack()

        tk.Label(section_ajouter, text="Nom:", bg="white").pack()
        self.entry_nom_ajout = tk.Entry(section_ajouter)
        self.entry_nom_ajout.pack()

        tk.Button(section_ajouter, text="➕ Ajouter", bg="#4CAF50", fg="white", command=self.ajouter_membre).pack(pady=5)

        # -------- Emprunter un livre --------
        tk.Label(section_emprunter, text="Emprunter un livre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_emprunter, text="ISBN Membre:", bg="white").pack()
        self.entry_isbn_emprunt = tk.Entry(section_emprunter)
        self.entry_isbn_emprunt.pack()

        tk.Label(section_emprunter, text="ISBN Livre:", bg="white").pack()
        self.entry_livre_emprunt = tk.Entry(section_emprunter)
        self.entry_livre_emprunt.pack()

        tk.Button(section_emprunter, text="📚 Emprunter", bg="#2196F3", fg="white", command=self.emprunter_livre).pack(pady=5)

        # -------- Rendre un livre --------
        tk.Label(section_rendre, text="Rendre un livre", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(section_rendre, text="ISBN Membre:", bg="white").pack()
        self.entry_isbn_rendre = tk.Entry(section_rendre)
        self.entry_isbn_rendre.pack()

        tk.Label(section_rendre, text="ISBN Livre:", bg="white").pack()
        self.entry_livre_rendre = tk.Entry(section_rendre)
        self.entry_livre_rendre.pack()

        tk.Button(section_rendre, text="↩️ Rendre", bg="#FF5722", fg="white", command=self.rendre_livre).pack(pady=5)

        self.rafraichir_tableau()

    def rafraichir_tableau(self):
        self.tree.delete(*self.tree.get_children())
        for identifiant, info in self.controller.bib.membres.items():
            membre = info["membre"]
            historique = info["historique_livre_emprunte"]
            titres = ", ".join([livre.titre for livre in historique])
            self.tree.insert("", "end", values=(identifiant, membre.nom, titres))

    def ajouter_membre(self):
        try:
            identifiant = self.entry_isbn_ajout.get()
            nom = self.entry_nom_ajout.get()
            membre = Membre(identifiant, nom)
            self.controller.bib.ajouter_membre(membre)
            self.controller.bib.sauvegarder_membres()
            self.rafraichir_tableau()
            messagebox.showinfo("Succès", f"Membre {nom} ajouté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def emprunter_livre(self):
        try:
            id_membre = self.entry_isbn_emprunt.get()
            isbn_livre = self.entry_livre_emprunt.get()
            bib = self.controller.bib
            membre = bib.membres[id_membre]["membre"]
            livre = bib.livres[isbn_livre]["livre"]
            bib.emprunter_livre(membre, [livre])
            bib.sauvegarder_membres()
            bib.sauvegarder_livres()
            self.rafraichir_tableau()
            messagebox.showinfo("Succès", f"Livre '{livre.titre}' emprunté par {membre.nom}.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rendre_livre(self):
        try:
            id_membre = self.entry_isbn_rendre.get()
            isbn_livre = self.entry_livre_rendre.get()
            bib = self.controller.bib
            membre = bib.membres[id_membre]["membre"]
            livre = bib.livres[isbn_livre]["livre"]
            bib.rendre_livre(membre, [livre])
            bib.sauvegarder_membres()
            bib.sauvegarder_livres()
            self.rafraichir_tableau()
            messagebox.showinfo("Succès", f"Livre '{livre.titre}' rendu par {membre.nom}.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


bib = Bibliotheque()

try:
    bib.charger_livres()
    bib.charger_membres()

    app = App(bib)
    app.mainloop()
    bib.sauvegarder_livres()
    bib.sauvegarder_membres()

except Exception as e:
    print("Erreur :", e)


