from tkinter import *

def quitter():
    menu.destroy()
    exit(0)

def inserer(x):
    y = grille.inserer(x)
    if y != None :
        if grille.tour == 1 : 
            couleur = "red"
            grille.tour = 2
            label_tour.configure(text="Tour de "+value2.get(), fg="yellow", bg="gray")#permet d'afficher le nom du joueur a chaque tour
        else :
            couleur = "yellow"
            grille.tour = 1
            label_tour.configure(text="Tour de "+value1.get(), fg="red", bg="white")#permet d'afficher le nom du joueur a chaque tour
        cX = (Largeur-rLargeur)//2 + s*(3*x+2) # } Calcul de la position
        cY = (Hauteur-rHauteur)//2 + s*(3*(5-y)+2) # } du cercle
        Canevas.create_oval(cX-s, cY-s, cX+s, cY+s, fill=couleur)
        vainqueur = grille.test_alignement() # si un des joueurs a gagné, test_alignement renvoie le numéro de ce joueur, sinon 0
        if vainqueur != 0 :
            gagner(vainqueur)
        elif grille.est_pleine() :
            egalite()

def gagner(vainqueur):
    """Écran de victoire ; affiche le nom du vainquer et propose aux utilisateurs de quitter ou de rejouer.
    """
    jeu.destroy()
    victoire = Tk()
    victoire.title("Puissance 4")
    if vainqueur == 1:
        Label(text = "Le joueur 1 du nom de {} a gagné".format(value1.get())).pack(padx=5, pady=5)
    elif vainqueur == 2:
        Label(text = "Le joueur 2 du nom de {} a gagné".format(value2.get())).pack(padx=5, pady=5)
    
    frame = Frame(victoire)
    frame.pack(side = BOTTOM)
    Button(frame, text="Rejouer", command=lambda:[victoire.destroy(), rejouer()]).pack(side=LEFT, padx=5, pady=5)
    Button(frame, text="Quitter", command=exit).pack(side=LEFT, padx=5, pady=5)
    victoire.mainloop()

def egalite():
    """Écran qui indique qu'il y a eu une égalité et propose aux utilisateurs de quitter ou de rejouer."""
    jeu.destroy()
    victoire = Tk()
    victoire.title("Puissance 4")
    texte = Label(victoire, text = "Égalité !")
    texte.pack(padx=5, pady=5)
    frame = Frame(victoire)
    frame.pack(side = BOTTOM)
    Button(frame, text="Rejouer", command=lambda:[victoire.destroy(), rejouer()]).pack(side=LEFT, padx=5, pady=5)
    Button(frame, text="Quitter", command=exit).pack(side=LEFT, padx=5, pady=5)
    victoire.mainloop()

def rejouer():
    global continuer
    continuer = True

# On implémente la grille de puissance 4 à l'aide d'une matrice composée de 7 tableaux de 6 nombres chacun. Chaque nombre représente une case ; 0 signifie qu'il n'y a aucun jeton, 1 ou 2 indique qu'il  a un jeton du joueur x.
class Grille :
    def __init__(self):
        self.matrice = []
        for x in range(7): # les 7 colonnes de la grille
            self.matrice.append([])
            for y in range(6): # les 6 lignes de la grille
                self.matrice[x].append(0)
        self.tour = 1

    def inserer (self, colonne):
        assert type(colonne) == int
        assert 0 <= colonne < 7

        for y in range (6):
            if self.matrice[colonne][y] == 0: # On cherche la première case libre d'une colonne en partant du bas
                self.matrice[colonne][y] = self.tour # On affecte la case au numéro du joueur
                return y # Cette indication permet à la fonction inserer du programme principal de mettre à jour l'affichage de la grille
        return None

    def __str__(self):
        """
        Fonction uniquement utilisée pour du deboguage
        """
        out = ""
        for y in range (5, -1, -1):
            out = out + '| '
            for x in range(7):
                out = out + str(self.matrice[x][y]) + " "
            out = out + '|\n'
        return out


    def test_alignement(self):
        """test si 4 pions sont alignés dans la grille
        - retourne 0 si ce n'est pas le cas
        - retourne 1 si le joueur 1 a aligné 4 pions
        - retourne 2 si le joueur 2 a aligné 4 pions"""
        # On parcours le tableau ; à chaque case on récupère la couleur et on teste 4 cas différents :
        couleur_case = 0
        for y in range(6):
            for x in range(7):
                couleur_case = self.matrice[x][y]
                if couleur_case == 0 :
                    continue
                if y <= 2 : # test d'un alignement vertical
                    if self.matrice[x][y+1] == couleur_case :
                        if self.matrice[x][y+2] == couleur_case :
                            if self.matrice[x][y+3] == couleur_case :
                                return couleur_case
                if x <= 3 : # test d'un alignement horizontal
                    if self.matrice[x+1][y] == couleur_case :
                        if self.matrice[x+2][y] == couleur_case :
                            if self.matrice[x+3][y] == couleur_case :
                                return couleur_case
                if x <= 3 and y <= 2 : # test d'un alignement oblique vers le haut et vers la droite
                    if self.matrice[x+1][y+1] == couleur_case :
                        if self.matrice[x+2][y+2] == couleur_case :
                            if self.matrice[x+3][y+3] == couleur_case :
                                return couleur_case
                if x <= 3 and y >= 3 : # test d'un alignement oblique vers le bas et vers la droite
                    if self.matrice[x+1][y-1] == couleur_case :
                        if self.matrice[x+2][y-2] == couleur_case :
                            if self.matrice[x+3][y-3] == couleur_case :
                                return couleur_case
        return 0

    def est_pleine (self):
        """Test si la grille ne contient plus aucune case vide (cas d'égalité). Dans ce cas, on retourne True, autrement on retourne False."""
        pleine = True
        for x in self.matrice:
            for y in x:
                if y == 0 :
                    pleine = False
                    break
        return pleine

# Début du programme, on demande le nom des deux joueurs dans un menu

menu=Tk()
menu.title('Puissance 4')

continuer = True # Cette variable permet d'arreter le programme si l'utilisateur ferme une fenêtre. Ainsi, si la boucle ne redemarre qu'à la suite de la fonction gagner, ou de la fonction égalité (si le joueur clique sur "rejouer") 

#creation du bouton joueur 1
value1 = StringVar()
value1.set("Nom du joueur 1")
entree = Entry(menu, textvariable = value1, width=30)
entree.pack(padx=5, pady=5)

#crétion du bouton joueur 2
value2 = StringVar()
value2.set("Nom du joueur 2")
entree = Entry(menu, textvariable = value2, width=30)
entree.pack(padx=5, pady=5)

#création du bouton démarrer
Button(menu, text ='Démarrer',command=menu.destroy).pack(side=RIGHT, padx=5, pady=5)

Button(menu, text="Quitter", command=quitter).pack(side=LEFT, padx=5, pady=5)
menu.mainloop()

while(continuer): #Boucle principale du jeu

    continuer = False

    grille = Grille()
    grille.tour = 1

    # écran de jeu
    jeu=Tk()
    jeu.title("Puissance 4")

    # création de la grille dans un Canvas
    Largeur = 990
    Hauteur = 540
    Canevas = Canvas(jeu, width=Largeur, height=Hauteur)

    s = (Hauteur-50)//19 # distance séparant deux trous de la grille [s pour séparation]
    d = 2*s # diamètre d'un trou
    rLargeur = s*22 # Largeur de la grille [r pour rectangle]
    rHauteur = s*19 # Hauteur de la grille
    rX = Largeur // 2 # }Position du
    rY = Hauteur // 2 # }centre de la grille
    Canevas.create_rectangle(rX-rLargeur//2, rY-rHauteur//2, rX+rLargeur//2, rY+rHauteur//2, outline = "black", fill="blue")
    for i in range(7):
        for j in range(6):
            cX = (Largeur-rLargeur)//2 + s*(3*i+2) # } Calcul de la position
            cY = (Hauteur-rHauteur)//2 + s*(3*j+2) # } du cercle
            Canevas.create_oval(cX-s, cY-s, cX+s, cY+s, fill="white")

    Canevas.pack(padx = 5)

    #Création d'une Frame pour qu'elle affiche à qui est le tour en se référant aux deux lignes dans la méthode insérer (ligne 8 et 12)
    frame_tour = Frame(jeu, borderwidth=20, relief=GROOVE)
    frame_tour.pack(side=TOP, padx=60, pady=40)
    label_tour = Label(frame_tour, text="Tour de "+value1.get(),bg="white", fg="red")
    label_tour.pack(padx=10, pady=10)

    #création des boutons pour choisir où on va mettre son pion.
    frame = Frame(jeu)
    frame.pack(side=BOTTOM, pady = 10, padx = 10)

    Button(frame, text =str(0), font=("TkDefaultFont", 40), command=lambda:inserer(0)).pack(side=LEFT, padx=22, pady=10)
    Button(frame, text =str(1), font=("TkDefaultFont", 40), command=lambda:inserer(1)).pack(side=LEFT, padx=22, pady=10)
    Button(frame, text =str(2), font=("TkDefaultFont", 40), command=lambda:inserer(2)).pack(side=LEFT, padx=22, pady=10)
    Button(frame, text =str(3), font=("TkDefaultFont", 40), command=lambda:inserer(3)).pack(side=LEFT, padx=22, pady=10)
    Button(frame, text =str(4), font=("TkDefaultFont", 40), command=lambda:inserer(4)).pack(side=LEFT, padx=22, pady=10)
    Button(frame, text =str(5), font=("TkDefaultFont", 40), command=lambda:inserer(5)).pack(side=LEFT, padx=22, pady=10)
    Button(frame, text =str(6), font=("TkDefaultFont", 40), command=lambda:inserer(6)).pack(side=LEFT, padx=22, pady=10)




    jeu.mainloop()