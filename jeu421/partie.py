from jeu421.interface import Interface
from jeu421.combinaison import *
from jeu421.joueur import Joueur, JoueurAlgo


class Partie:
    """
    Classe représentant une partie de 421. Une partie a les attributs suivants:
    - nb_joueurs: le nombre de joueurs dans la partie
    - joueurs: la liste des joueurs de la partie
    - nb_jetons_du_pot: le nombre de jetons dans le pot de la partie
    - nb_maximum_lancer: le nombre maximum de lancés permis pendant la décharge
    - premier: index du premier joueur pour le tour courant, donc change possiblement
    - joueur_courant: joueur qui est en train de jouer (type: Joueur)
    - phase: 0=choix premier joueur, 1=Phase1, 2=Phase 2 (type:int)
    - end_tour: True = Le joueur décide de terminer son tour, False = tour normal
    """
    interface = Interface()

    def __init__(self, noms_joueurs, nb_human=0, nb_ai=0, ):
        """
        Constructeur de la classe. Vous devez initialisez les attributs
        :param nb_joueurs: le nombre de joueur de la partie
        """
        self.nb_joueurs = nb_human + nb_ai
        #assert self.nb_joueurs >= 2
        self.nb_human = nb_human
        self.joueurs = [Joueur(str(noms_joueurs[i])) for i in range(nb_human)]

        if nb_ai > 0:
            for i in range(nb_ai):
                self.joueurs.append(JoueurAlgo(str(noms_joueurs[nb_human+i])))

        self.nb_jetons_du_pot = NOMBRE_DE_JETONS_DU_JEU
        self.premier = 0
        self.joueur_courant = None
        self.phase = 0
        self.nb_maximum_lancer = 3
        self.end_tour = False

    def determiner_premier_lanceur(self):
        """
        Cette méthode permet de déterminer le premier joueur qui lancera dans la partie.
        Tous les joueurs sont sensé lancer un dé et c'est celui qui a le plus petit nombre qui jouera plus tard le
        premier tour.
        En cas d'égalité, les joueurs concernés répètent l'opération
        L'attribut premier de la classe est initialisé à l'appel de cette méthode
        :return:
        """
        best_valeur = 0
        premiers = []
        for i in range(len(self.joueurs)):
            valeur = self.joueurs[i].combinaison_actuelle.representant[0]
            if valeur > best_valeur:
                best_valeur = valeur
                premiers = [i]
            elif valeur == best_valeur:
                premiers += [i]
        return premiers

    def jouer_tour_premiere_phase(self):
        """
        Cette méthode permet de faire le tour de tous les joueurs et leur permet de jouer pendant la charge.
        Rappel: pendant la charge chaque joueur ne peut lancer les dés qu'une seule fois et le perdant du tour doit
        prendre dans le pot un nombre de jetons égale au nombre de points du gagnant du tour.
        Vous devez afficher à l'interface un récapitulatif des jetons des joueurs après chaque tour
        :return: un tuple d'entier qui correspond aux index (perdant_tour, gagnant_tour, jetons_tour)
        """
        nb_maximum_lancer = 1
        for i in range(self.nb_joueurs):
            pos = (self.premier+i) % self.nb_joueurs
            # routine pour déterminer le gagnant et le perdant après que ce joueur ait joué
            if i == 0:
                gagnant = pos
                perdant = pos
            else:
                if self.joueurs[pos].combinaison_actuelle < self.joueurs[perdant].combinaison_actuelle:
                    perdant = pos
                if ((self.joueurs[pos].combinaison_actuelle > self.joueurs[gagnant].combinaison_actuelle) or
                    (self.joueurs[pos].combinaison_actuelle == self.joueurs[gagnant].combinaison_actuelle)) :
                    gagnant = pos

        # le perdant prends autant de jetons dans le pot que le gagnant a de point
        v = min(self.joueurs[gagnant].combinaison_actuelle.valeur, self.nb_jetons_du_pot)
        self.joueurs[perdant].ajouter_jetons(v)
        self.nb_jetons_du_pot -= v
        self.premier = perdant
        self.joueur_courant = self.joueurs[perdant]

        return (perdant, gagnant,v)

    def jouer_tour_deuxieme_phase(self):
        """
        Cette méthode permet de faire le tour de tous les joueurs et leur permet de jouer pendant la décharge.
        Rappel: pendant la décharge chaque joueur peut lancer les  dés autant de fois que le premier joueur
        de la charge l'a fait. De plus, le gagnant du tour doit donner un nombre de jetons égale à son nombre de points au perdant du tour.
        Vous devez afficher à l'interface un récapitulatif des jetons des joueurs après le tour
        :return: un tuple d'entier qui correspond aux indexs (perdant_tour, gagnant_tour, jetons_tour)
        """

        nb_maximum_lancer = 3
        for i in range(self.nb_joueurs):
            #n = 3 if i == 0 else nb_maximum_lancer
            pos = (self.premier + i) % self.nb_joueurs
            #Partie.interface.afficher("Tour du {}".format(self.joueurs[pos].nom))
            #nb_lancer = self.joueurs[pos].jouer_tour(n)
            if i == 0:
                #nb_maximum_lancer = nb_lancer
                gagnant, perdant = pos, pos
                #Partie.interface.afficher("Le premier premier lanceur ayant fait {}, le nombre de "
                      #"lancées pour ce tour est {}".format(nb_lancer, nb_lancer))
            else:
                if self.joueurs[pos].combinaison_actuelle < self.joueurs[perdant].combinaison_actuelle:
                    perdant = pos

                if ((self.joueurs[pos].combinaison_actuelle > self.joueurs[gagnant].combinaison_actuelle) or
                    (self.joueurs[pos].combinaison_actuelle == self.joueurs[gagnant].combinaison_actuelle)):
                    gagnant = pos
        assert self.nb_joueurs > 1 and gagnant != perdant
        v = min(self.joueurs[gagnant].combinaison_actuelle.valeur, self.joueurs[gagnant].nb_jetons)
        self.joueurs[perdant].ajouter_jetons(v)
        self.joueurs[gagnant].retirer_jetons(v)
        self.premier = perdant
        self.joueur_courant = self.joueurs[perdant]
        self.verifie_invariants()
        return (perdant, gagnant,v)

    def verifier_nenette(self, joueur):
        if joueur.combinaison_actuelle.type == TypeComb.NENETTE:  # Nénette donne 2 jetons automatiquement
            jetons_nenette = 2
            if jetons_nenette > self.nb_jetons_du_pot:
                jetons_nenette = self.nb_jetons_du_pot
            joueur.ajouter_jetons(jetons_nenette)
            self.nb_jetons_du_pot -= jetons_nenette
            return True
        else:
            return False


    def verifier_gagnant(self, joueur):
        """
        Cette méthode permet de déterminer si un joueur a gagné la partie, i.e qu'il n'a plus de jetons
        :param joueur: le joueur en question
        :return: True si le joueur n'a plus de jetons, False sinon
        """
        return joueur.nb_jetons == 0

    def verifier_perdant(self, joueur):
        """
        Cette méthode permet de déterminer si un joueur a perdu la partie
        :param joueur: le joueur en question
        :return: True si le joueur a tous les jetons de la partie, False sinon
        """
        return joueur.nb_jetons == NOMBRE_DE_JETONS_DU_JEU

    def retirer_joueur(self, position):
        """
        Retirer un joueur du jeu
        :param position: la position du joueur dans la liste des joueurs à retirer
        :return:
        """
        self.joueurs.pop(position)
        self.nb_joueurs -= 1
        print("DEBUG{}:".format(len(self.joueurs)))

    def afficher_recapitulatif(self):
        """
        Affiche un tableau récapitulatif de la partie
        """
        n = 40
        Partie.interface.afficher()
        Partie.interface.afficher("{}\n|{:^38}|\n{}".format("_"*n, "Récapitulatif de la partie", "-"*n))
        s = "|{:^27s}|{:^10d}|"
        Partie.interface.afficher(s.format("POT DE JETONS", self.nb_jetons_du_pot))
        for j in sorted(self.joueurs, key=lambda x: x.nb_jetons, reverse=True):
            Partie.interface.afficher(s.format(j.nom, j.nb_jetons))
        Partie.interface.afficher("{}\n".format("-" * n))

    def verifie_invariants(self):
        assert (sum([j.nb_jetons for j in self.joueurs]) + self.nb_jetons_du_pot) == NOMBRE_DE_JETONS_DU_JEU, \
            "Le nombre de jetons dans le jeu est actuellement différent de {}".format(NOMBRE_DE_JETONS_DU_JEU)

        assert len(self.joueurs) == self.nb_joueurs, "Le nombre de joueurs dans la partie est inexacte"
        assert self.premier < self.nb_joueurs
