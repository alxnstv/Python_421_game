from tkinter import *


class Ruleswindow():

    def __init__(self, frame_param):

        self.quit_window = False

        #Frame 1
        labelframe = LabelFrame(frame_param, text="Règles du jeu")
        labelframe.pack(fill="both", expand="yes")
        game_conditions = Label(labelframe, text="-Être minimum deux joueurs.\n-3 dés\n-Un « pot » de 21 jetons.", justify=LEFT)
        game_conditions.pack(side=LEFT)
        #Frame 2
        labelframe2 = LabelFrame(frame_param, text="Comment gagner")
        labelframe2.pack(fill="both", expand="yes")
        win_condition = Label(labelframe2, text="On joue généralement le 421 en deux manches, la « charge » et la « décharge ». L’ensemble des jetons est appelé le « pot ».\n\nLors de la première partie du jeu, la « charge », les joueurs vont se répartir les 21 jetons entre eux en espérant en récupérer le moins possible. Lors de la deuxième partie, la « décharge », les joueurs devront se débarrasser du plus de jetons possible.\n\nLe joueur ayant remporté le jeu de dés démarrera la partie en lançant les trois dés. Pour chacun des trois dés il peut choisir de relancer ou non. S’il ne relance pas il aura effectué un seul lancer. Le joueur peut, si il le désire, relancer une deuxième et une troisième fois tout ou partie des trois dés. Ceci va influer sur le reste de la manche car les autres joueurs devront effectuer le même nombre de lancers que le premier joueur.\n\nAinsi, si le premier joueur à lancé trois fois les dés les autres joueurs devront faire de même. Si le deuxième joueur réussis un 421 dès son premier lancer, il devra tout de même relancer les dés pour respecter les trois lancers.\n\nDans certaines variantes cette règle est assouplie. En effet, lorsqu’un joueur est satisfait de sa combinaison il peut taper sur la table en disant « le bon ». Cela lui permet de valider sa combinaison sans avoir à faire le même nombre de lancer que le premier joueur. Bien sûr, le nombre maximum de lancer est toujours de trois. Ceci doit être annoncé avant le début de la partie pour que tous les joueurs soit d’accord sur les règles.\n\nAu cours de la « charge », celui qui fait la moins bonne combinaison reçoit des jetons du « pot ». Le nombre de jetons distribué au joueur est déterminé par la meilleure combinaison (voir les valeurs des combinaisons ci-dessous).\n\nPour gagner une partie de 421, il faut être le premier joueur à ne plus avoir de jetons au terme des deux manches. Il faut savoir qu’il existe de nombreuses variantes à la règle de base. Ainsi, il est toujours possible d’ajouter des règles pour pimenter le jeu du 421.",justify=LEFT,wraplength=750)
        win_condition.pack(side=LEFT)
        #Frame 3
        self.labelframe3 = LabelFrame(frame_param, text="Valeur des combinaisons")
        self.labelframe3.pack(fill="both", expand="yes")


        my_list = ["Le 421", "Fiche", "Baraque", "Tierce", "Nenette", "Autre"]

        self.list_combinaisons = Listbox(self.labelframe3, height=len(my_list), exportselection=False)
        self.list_combinaisons.grid(row=0, column=0)
        self.list_combinaisons.bind('<<ListboxSelect>>', self.show_rules)

        for item in my_list:
            self.list_combinaisons.insert(END, item)


        #DEBUG
        #for i in range(0, self.list_combinaisons.size()):
        #    print(self.list_combinaisons.get(i))

        self.valeur_frame = Frame(self.labelframe3)
        self.valeur_frame.grid(row=0, column=1)


    def show_rules(self, evenement=None):
        self.valeur_frame.destroy()
        self.valeur_frame = Frame(self.labelframe3)
        self.valeur_frame.grid(row=0, column=1)

        index_liste = self.list_combinaisons.curselection()[0]
        selection = self.list_combinaisons.get(index_liste)

        if selection =="Le 421":
            label = "Description: Le 421 vaut 10 points. C'est la combinaison qui vaut le plus de points."
        elif selection =="Fiche":
            label = "Description: Composées de deux 1 et d’une troisième valeur, différente de 1," \
                    " valent la valeur du troisième dé (ex : 411 vaut quatre points)."
        elif selection =="Baraque":
            label = "Description: Les baraques, composées de trois valeurs identiques, " \
                    "valent autant de points que la valeur d’un dé qui la compose, sauf la 111 qui vaut sept points " \
                    "(Notez qu’à valeur équivalente, «fiche» l’emporte sur «baraque»). "
        elif selection =='Tierce':
            label = "Description: Les tierces composées de trois chiffres successifs, " \
                    "valent deux points(notez que 654 est plus fort que 321)."
        elif selection =="Nenette":
            label = "Description: La « nénette »: 221. On dit parfois que «tout bat nénette», " \
                    "mais en fait elle est battue par les 421, fiches, baraques et tierces mais bat les autres. " \
                    "Elle vaut quatre points."
        elif selection=="Autre":
            label = "Description: les autres ne valent qu’un point. On les classe grâce au chiffre le plus fort, " \
                    "puis le deuxième et le troisième. Par exemple, 641 est plus forte que 632, etc."

        description_valeur = Label(self.valeur_frame, text=label, justify=LEFT, wraplength=350)
        description_valeur.grid(column=1)

        #Les regles proviennent de http://www.regles-de-jeux.com/regle-du-421/

