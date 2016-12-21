from tkinter import *
from jeu421.interface import *
from jeu421.partie import *
from time import sleep
from jeu421.joueur import *


class Playwindow(Canvas):
    n_des_total = 3
    n_pixels_par_case = 100
    interface = Interface()

    def __init__(self, main_window, master, jeu):
        super().__init__(master, width=self.n_des_total * self.n_pixels_par_case, height=self.n_pixels_par_case)
        self.master = master
        self.main_window = main_window
        self.des = []
        self.boleen_des_relancer = [None, None, None]
        self.valeur_des = [None, None, None]
        self.bind('<Button-1>', self.select_deselect)
        self.jeu = jeu
        self.n_lancer = 1
        self.debut_partie = True
        self.joueur_gagnant = None

    def dessiner_canvas(self):

        # Dessiner les case
        self.delete('case')
        for i in range(Playwindow.n_des_total):
            debut_ligne = i * self.n_pixels_par_case
            fin_ligne = debut_ligne + self.n_pixels_par_case

            # try:
            if self.boleen_des_relancer[i] == True:
                couleur = '#83BFF3'
            else:
                couleur = 'white'
                # except:
                # couleur = "#E0E0E0"
            # finally:
            self.create_rectangle(debut_ligne, 0, fin_ligne, self.n_pixels_par_case, fill=couleur, tags='case')

        # Dessiner les dés
        self.delete('des')
        caracteres_des = {1: '\u2680', 2: '\u2681', 3: '\u2682', 4: '\u2683', 5: '\u2684', 6: '\u2685'}


        try:
            for position, d in enumerate(self.valeur_des):
                crd_y = self.n_pixels_par_case // 2
                crd_x = (position * self.n_pixels_par_case) + self.n_pixels_par_case // 2
                self.create_text(crd_x, crd_y, text=caracteres_des[d], font=('Deja Vu', self.n_pixels_par_case // 2),
                                 tags='des')
        except:
            pass

    def changer_nom(self, evenement=None):
        choix_window = choix_nom(self, sorte="Nom")
        self.wait_window(choix_window)


    def anime_lancer(self):
        faces_des = range(1, 7)
        state_lancer = self.main_window.button_lancer['state']
        state_end_tour = self.main_window.button_end_tour['state']
        self.main_window.button_lancer.configure(state=DISABLED)
        self.main_window.button_end_tour.configure(state=DISABLED)
        for x in range(5):
            x = x % 6
            gen = (i for i, d in enumerate(self.boleen_des_relancer) if (d is True or d is None))
            if self.jeu.phase == 0:  # Phase choix du premier joueur. On lance 1 seul dé.
                self.valeur_des[0] = faces_des[x]
                self.dessiner_canvas()
                self.update()
                sleep(0.12)
            else:
                for i in gen:
                    self.valeur_des[i] = faces_des[x]
                self.dessiner_canvas()
                self.update()
                sleep(0.12)
        self.main_window.button_lancer.configure(state=state_lancer)
        self.main_window.button_end_tour.configure(state=state_end_tour)

    def lancer_des_premier(self):
        """
        Lancer d'un dés pour déterminer le premier joueur
        :return:
        """


        if self.debut_partie:
            self.log_info('DEBUT DE LA PARTIE')
            self.debut_partie = False

        # DEBUG ALEX
        for j in self.jeu.joueurs:
            print("DEBUG: {}".format(j.nom))

        for j in [j for j in self.jeu.joueurs if j.participe_au_tour == False]:
            j.combinaison_actuelle == Combinaison([0, 0, 0])  # On remet à 0 les joueur qui ne participe pas au tour

        if self.jeu.joueur_courant.participe_au_tour == True:
            self.anime_lancer()
            val_lancer = self.jeu.joueur_courant.lancer_des(1)
            self.jeu.joueur_courant.combinaison_actuelle = Combinaison(val_lancer + [0, 0])
            self.valeur_des[0] = self.jeu.joueur_courant.combinaison_actuelle.representant[0]
            self.jeu.joueur_courant.participe_au_tour = False
            self.dessiner_canvas()
            self.update()

        self.log_info(('Le {} lance {}.'.format(self.jeu.joueur_courant.nom,
                                    self.jeu.joueur_courant.combinaison_actuelle.representant)))

        # On passe au prochain joueur
        index_joueur_courant = [i for (i, j) in enumerate(self.jeu.joueurs) if j is self.jeu.joueur_courant]
        index_joueur_courant = index_joueur_courant[0]
        while True:
            try:
                index_joueur_courant += 1
                self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_courant]  # prochain joueur
                if self.jeu.joueur_courant.participe_au_tour == True:
                    break
            except IndexError:
                break  # on arrête lorsqu'on a terminer la liste
        # Fin du tour de tous les joueur. Détermination du résultat
        if [j for j in self.jeu.joueurs if j.participe_au_tour == True] == []:
            premiers = self.jeu.determiner_premier_lanceur()  # index des gagnants
            if len(premiers) > 1:  # Égalité

                self.log_info("Egalite entre les joueurs: {}".format(", ".join([str(i + 1) for i in premiers])))

                for i in premiers:
                    self.jeu.joueurs[i].participe_au_tour = True
                self.jeu.joueur_courant = self.jeu.joueurs[premiers[0]]


            elif len(premiers) == 1:  # Aucune égalité
                self.jeu.premier = premiers[0]
                self.jeu.joueur_courant = self.jeu.joueurs[self.jeu.premier]
                self.jeu.phase = 1
                for j in self.jeu.joueurs:
                    j.participe_au_tour = True  # on réinitialise la participation au tour pour phase 1

                self.log_info("{} lance en premier".format(self.jeu.joueurs[premiers[0]].nom))

                self.main_window.button_lancer.configure(text="Lancer les dés",
                                                    command=lambda: self.lancer_des())

                self.log_info('DEBUT DE LA CHARGE')

        # Afficher le score a droite
        #self.afficher_score_log(main_window)

    def lancer_des(self):
        """
        Lancer de 3 dés.
        :return:
        """

        # Lancer les dés
        self.n_lancer = 1
        self.boleen_des_relancer = [None] * 3
        if self.jeu.end_tour == False:  # toujours sauf si le bouton terminer tour est pesé
            self.anime_lancer()
            self.jeu.joueur_courant.combinaison_actuelle = Combinaison(self.jeu.joueur_courant.lancer_des(3))
            self.valeur_des = self.jeu.joueur_courant.combinaison_actuelle.representant


            self.log_info(('Le {} lance {}.'.format(self.jeu.joueur_courant.nom,
                                                             self.jeu.joueur_courant.combinaison_actuelle.representant)))

        # Phase 1
        if self.jeu.phase == 1:
            self.dessiner_canvas()
            self.update()
            self.jeu.joueur_courant.participe_au_tour = False
            self.main_window.display_message_jeu("")
            if self.jeu.verifier_nenette(self.jeu.joueur_courant):
                self.log_info(('{} a fait Nenette'.format(self.jeu.joueur_courant.nom)))

            # Joueur suivant
            index_joueur_courant = [i for (i, j) in enumerate(self.jeu.joueurs) if j is self.jeu.joueur_courant]
            index_joueur_courant = index_joueur_courant[0]
            index_joueur_courant = (index_joueur_courant + 1) % self.jeu.nb_joueurs
            self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_courant]  # prochain joueur
            # Fin du tour de tous les joueurs. Détermination du résultat et transaction de jetons
            if self.jeu.joueur_courant.participe_au_tour == False:
                PGJ = self.jeu.jouer_tour_premiere_phase()
                for j in self.jeu.joueurs:
                    j.participe_au_tour = True  # on réinitialise la participation au tour

                #main_window.display_message_jeu(self.jeu.joueurs[PGJ[1]].nom + " gagne le tour.\n" + self.jeu.joueurs[PGJ[0]].nom + " perd le tour et prend " + str(PGJ[2]) + " jetons.")
                self.log_info((self.jeu.joueurs[PGJ[1]].nom + " gagne le tour."))
                self.log_info((self.jeu.joueurs[PGJ[0]].nom + " perd le tour et prend " + str(PGJ[2]) + " jetons."))
                self.log_info(("Jetons du pot: {}".format(str(self.jeu.nb_jetons_du_pot))))


            # Fin de la phase 1
            if self.jeu.nb_jetons_du_pot <= 0:
                self.log_info("FIN DE LA CHARGE")

                self.jeu.phase = 2
                self.main_window.button_end_tour.configure(state=NORMAL)
                for j in self.jeu.joueurs:
                    for j in self.jeu.joueurs:
                        if self.jeu.verifier_perdant(j) == True:  # 1 seul perdant et tous les autres sont gagnant
                            self.log_info((self.main_window.message['text'] + '\nLA PARTIE EST TERMINEE.'))
                        if self.jeu.verifier_gagnant(j):  # on retire les joueurs gagnants
                            self.jeu.retirer_joueur(self.jeu.joueurs.index(j))

        # Phase 2
        elif self.jeu.phase == 2:
            index_joueur_courant = [i for (i, j) in enumerate(self.jeu.joueurs) if j is self.jeu.joueur_courant]
            index_joueur_courant = index_joueur_courant[0]
            # Si on pèse sur le bouton terminer_tour
            if self.jeu.end_tour == True:
                self.jeu.end_tour = False
                self.jeu.joueur_courant.participe_au_tour = False
                self.log_info("Tour du joueur suivant")

                self.main_window.button_lancer.configure(text="Lancer les des", command=lambda: self.lancer_des())
                self.main_window.button_end_tour.configure(state=DISABLED)
                # premier joueur du tour détermine le nombre max de lancer
                if self.jeu.joueur_courant is self.jeu.joueurs[self.jeu.premier]:
                    self.jeu.nb_maximum_lancer = self.n_lancer
                # Joueur suivant
                index_joueur_suivant = (index_joueur_courant + 1) % self.jeu.nb_joueurs
                self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_suivant]
                if self.jeu.joueur_courant.participe_au_tour == True:  # toujours sauf si dernier joueur
                    return
            # Afficher les dés
            if self.jeu.end_tour == False:
                self.boleen_des_relancer = [False] * 3
                self.main_window.button_end_tour.configure(state=NORMAL)
                self.main_window.display_message_jeu("")
                self.dessiner_canvas()
                self.update()
                # Fin du tour du joueur
                if self.n_lancer == self.jeu.nb_maximum_lancer:
                    self.jeu.joueur_courant.participe_au_tour = False
                    self.main_window.button_end_tour.configure(state=DISABLED)
                    # Joueur suivant
                    index_joueur_suivant = (index_joueur_courant + 1) % self.jeu.nb_joueurs
                    self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_suivant]
                # Modification du bouton pour relancer les dés
                else:
                    self.log_info("Selectionnez les des à relancer et relancer.")
                    self.main_window.button_lancer.configure(text="Relancer les dés",
                                                        command=lambda: self.relancer_des())

            # Si joueur est un ordinateur.
            if isinstance(self.jeu.joueurs[index_joueur_courant], JoueurAlgo):
                # On lui fait jouer ses tours automatiquement
                for i in range(2):
                    # Si le nombre max de lancer est atteint
                    if i + 1 == self.jeu.nb_maximum_lancer:
                        self.main_window.button_end_tour.configure(state=DISABLED)
                        break  # on termine le tour
                    # Sinon on choisi les dés à relancer
                    self.main_window.button_lancer.configure(state=DISABLED)
                    self.main_window.button_end_tour.configure(state=DISABLED)
                    self.update()
                    sleep(.2)
                    dict_val_des = dict(enumerate(self.valeur_des))
                    val_a_relancer = self.jeu.joueurs[index_joueur_courant].choisir_des_algo()
                    # Si l'objectif est atteint et que l'ordinateur est le premier joueur du tour.
                    if val_a_relancer == [] and self.jeu.joueurs[index_joueur_courant] is self.jeu.joueurs[self.jeu.premier]:
                        self.jeu.nb_maximum_lancer = i+1  # On fixe le nb max de lancer
                        self.main_window.display_message_jeu("Tour du joueur suivant", color='blue')
                        self.log_info("Tour du joueur suivant.")
                        self.main_window.button_lancer.configure(text="Lancer les dés",
                                                                 command=lambda: self.lancer_des())
                        # joueur suivant
                        index_joueur_suivant = (index_joueur_courant + 1) % self.jeu.nb_joueurs
                        self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_suivant]
                        break
                    # On sélectionne les dés choisis pour relance
                    for index, value in dict_val_des.items():
                        if value in val_a_relancer:
                            self.boleen_des_relancer[index] = True
                            self.dessiner_canvas()
                            self.update()
                            sleep(.2)
                            val_a_relancer.remove(value)
                    sleep(1)
                    self.relancer_des()
                # À la fin du tour de l'ordinateur
                self.main_window.button_lancer.configure(state=NORMAL)

            # Fin du tour de tous les joueurs. Détermination du résultat et transaction de jetons
            if self.jeu.joueur_courant.participe_au_tour == False:
                PGJ = self.jeu.jouer_tour_deuxieme_phase()
                self.jeu.nb_maximum_lancer = 3

                #self.log_info('Jetons du pot: ' + str(self.jeu.nb_jetons_du_pot))  # le nb de jeton ds phase 2 tjrs =0
                self.log_info(self.jeu.joueurs[PGJ[1]].nom + " donne " + str(PGJ[2]) + " jetons à " + self.jeu.joueurs[PGJ[0]].nom)

                for j in self.jeu.joueurs:
                    j.participe_au_tour = True  # on réinitialise la participation au tour
                    if self.jeu.verifier_gagnant(j):
                        self.jeu.retirer_joueur(self.jeu.joueurs.index(j))  # on retire les joueurs gagnants
                # Fin de la partie
                if len(self.jeu.joueurs) == 1:
                    self.joueur_perdant = self.jeu.joueurs[0]
                    self.jeu.phase = 3
                    self.main_window.display_message_jeu(self.main_window.message['text'] + '\nLA PARTIE EST TERMINÉE.')
                    loose_window = choix_nom(self, sorte='loose')
                    self.wait_window(loose_window)


    def relancer_des(self):
        """
        Relancer les dés choisi
        :return:
        """

        # Lancer les dés et afficher sauf si bouton terminer_tour est pesé
        if self.jeu.end_tour == False:  # toujours sauf si le bouton terminer tour est pesé
            self.n_lancer += 1
            self.main_window.button_end_tour.configure(state=NORMAL)
            index_des_a_relancer = [i for i, relancer in enumerate(self.boleen_des_relancer) if relancer == True]
            self.anime_lancer()
            val_lancer = self.jeu.joueur_courant.lancer_des(len(index_des_a_relancer))
            for i, d in enumerate(index_des_a_relancer):
                self.valeur_des[d] = val_lancer[i]
            self.jeu.joueur_courant.combinaison_actuelle = Combinaison(self.valeur_des)
            self.boleen_des_relancer = [False] * 3
            self.main_window.display_message_jeu("Sélectionnez les des à relancer et relancer.", color='blue')

            self.dessiner_canvas()
            self.update()

            self.log_info("{} relance et obtient {}.".format(self.jeu.joueur_courant, self.jeu.joueur_courant.combinaison_actuelle.representant))

            # Fin du tour du joueur
            if self.n_lancer == self.jeu.nb_maximum_lancer:
                self.main_window.button_end_tour.configure(state=DISABLED)
                self.jeu.joueur_courant.participe_au_tour = False
                # Joueur suivant
                index_joueur_courant = [i for (i, j) in enumerate(self.jeu.joueurs) if j is self.jeu.joueur_courant]
                index_joueur_courant = index_joueur_courant[0]
                index_joueur_courant = (index_joueur_courant + 1) % self.jeu.nb_joueurs
                self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_courant]
                self.main_window.display_message_jeu("Tour du joueur suivant", color='blue')
                self.log_info("Tour du joueur suivant.")
                self.main_window.button_lancer.configure(text="Lancer les dés",
                                                    command=lambda: self.lancer_des())

        # Si bouton terminer_tour est pesé
        elif self.jeu.end_tour == True:
            self.jeu.end_tour = False
            self.jeu.joueur_courant.participe_au_tour = False
            self.main_window.button_end_tour.configure(state=DISABLED)
            self.main_window.display_message_jeu("Tour du joueur suivant", color='blue')
            self.log_info("Tour du joueur suivant.")

            self.main_window.button_lancer.configure(text="Lancer les dés",
                                                command=lambda: self.lancer_des())
            # premier joueur du tour détermine le nombre max de lancer
            if self.jeu.joueur_courant is self.jeu.joueurs[self.jeu.premier]:
                self.jeu.nb_maximum_lancer = self.n_lancer
            # Joueur suivant
            index_joueur_courant = [i for (i, j) in enumerate(self.jeu.joueurs) if j is self.jeu.joueur_courant]
            index_joueur_courant = index_joueur_courant[0]
            index_joueur_courant = (index_joueur_courant + 1) % self.jeu.nb_joueurs
            self.jeu.joueur_courant = self.jeu.joueurs[index_joueur_courant]
            if self.jeu.joueur_courant.participe_au_tour == True:  # toujours sauf si dernier joueur
                return

        # Fin du tour de tous les joueurs. Détermination du résultat et transaction de jetons
        if self.jeu.joueur_courant.participe_au_tour == False:
            PGJ = self.jeu.jouer_tour_deuxieme_phase()
            self.jeu.nb_maximum_lancer = 3

            self.main_window.display_message_jeu(
                self.jeu.joueurs[PGJ[1]].nom + " donne " + str(PGJ[2]) + " jetons à " + self.jeu.joueurs[
                    PGJ[0]].nom)
            self.log_info(self.jeu.joueurs[PGJ[1]].nom + " donne " + str(PGJ[2]) + " jetons à " + self.jeu.joueurs[PGJ[0]].nom)

            for j in self.jeu.joueurs:
                j.participe_au_tour = True  # on réinitialise la participation au tour
                if self.jeu.verifier_gagnant(j):
                    self.jeu.retirer_joueur(self.jeu.joueurs.index(j))  # on retire les joueurs gagnants

            #print('Jetons du pot: ' + str(self.jeu.nb_jetons_du_pot))  # toujour = 0 dans la décharge

            # Fin de la partie
            if len(self.jeu.joueurs) == 1:
                self.joueur_perdant = self.jeu.joueurs[0]
                self.jeu.phase = 3
                self.main_window.display_message_jeu(self.main_window.message['text'] + '\nLA PARTIE EST TERMINÉE.')
                loose_window = choix_nom(self, sorte='loose')
                self.wait_window(loose_window)
                #self.main_window.destroy()

            # Modification du bouton pour lancer les dés
            else:
                self.main_window.display_message_jeu("Tour du joueur suivant", color='blue')
                self.main_window.button_lancer.configure(text="Lancer les dés",
                                                    command=lambda: self.lancer_des())

    def select_deselect(self, event):
        """
        Cet méthode permet de sélectionner ou de déselectionner les dés à relancer
        :param event:
        :return:
        """
        num_des = event.x // self.n_pixels_par_case
        if self.boleen_des_relancer[num_des] == False:
            self.boleen_des_relancer[num_des] = True
        elif self.boleen_des_relancer[num_des] == True:
            self.boleen_des_relancer[num_des] = False
        self.dessiner_canvas()

    def clic_button_end_tour(self):
        self.jeu.end_tour = True
        if self.main_window.button_lancer['text'] == "Lancer les dés":
            self.lancer_des()
        elif self.main_window.button_lancer['text'] == "Relancer les dés":
            self.relancer_des()


    def log_info(self, text):
        print(text)
        self.main_window.display_message_jeu(text)
        self.main_window.add_info_to_eventlog(text)
        self.afficher_score_log()

    def update_score_log(self, text):
        self.main_window.add_info_to_scorelog(text)

    def afficher_score_log(self):
        self.main_window.clear_scorelog()
        for j in self.jeu.joueurs:
            self.update_score_log("{} a {} jetons".format(j.nom, j.nb_jetons))



class choix_nom(Toplevel):

    def __init__(self, master, sorte="nom"):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.grab_set()

        if sorte == "loose":
            Label(self, text="Le joueur perdant est : {}".format(master.joueur_perdant)).grid()
            #self.entree = Entry(self)
            #self.entree.grid()

            self.bouton_ok = Button(self, text="OK", command=self.fermer)
            self.bouton_ok.grid(padx=10, pady=10)

        else:
            Label(self, text="Entrez le nouveau {}".format(sorte)).grid()
            self.entree = Entry(self)
            self.entree.grid()

            self.bouton_ok = Button(self, text="OK", command=self.fermer)
            self.bouton_ok.grid(padx=10, pady=10)

    def fermer(self):
        self.destroy()