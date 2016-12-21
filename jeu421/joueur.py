from jeu421.interface import Interface
from jeu421.combinaison import *
from random import randint


class Joueur:
    """
    Classe représentant un joueur de 421. Un joueur a les attributs
    - nom: son nom
    - nb_jetons: son nombre de jetons, entier entre 0 et 21
    - combinaison actuelle: un objet de la classe Combinaison
    - participe_au_tour: Boléen indiquant si le joueur participe au tour courant
    La classe a un attribut static interface qui est l'interface de communication entre les joueurs et le programme

    """
    interface = Interface()


    def __init__(self, nom):
        """
        Constructeur de la classe, doit initialiser le nom du joueur à la valeur passée en paramètre.
        Le nombre de jetons à zéro, et la combinaison_actuelle à None
        :param nom: nom du joueur
        """
        self.nom = nom
        self.nb_jetons = 0
        self.combinaison_actuelle = None
        self.participe_au_tour = True

    def lancer_des(self, nombre_des):
        """
        Méthode permettant à un joeur de lancer dés
        :param nombre_des: nombre de dés à lancer
        :return: une liste de longueur nombre_des contenant les valeurs de chaque dés selon le lancé
        """
        return [randint(1, 6) for _ in range(nombre_des)]

    def jouer_tour(self, nb_maximum_lancer=3):
        """
        Cette méthode permet à un joueur de jouer lorsque c'est son tour dans une partie, en lançant les dés.
        Vous devez demandez au joueur de lancer des dés, de choisir les dés à relancer et puis changer l'attribut combinaison actuelle du
        :param nb_maximum_lancer: le nombre maximum de lancés auquel le joueur a droit lors de ce tour.
        :return: retourne le nombre de lancés que le joueur a fait.
        """
        no_lancer = 1

        while no_lancer <= nb_maximum_lancer:

            if no_lancer == 1:
                result_tour = self.lancer_des(NOMBRE_DES_DU_JEU)    # on lance tous les dés
            else:
                result_tour += self.lancer_des(len(des_a_relancer))   # on relance les dés choisis


            if no_lancer < nb_maximum_lancer:       # ne s'execute pas au dernier lancer
                des_a_relancer = self.interface.choisir_des_a_relancer(result_tour)
                if len(des_a_relancer) == 0:
                    no_lancer += 1
                    break        # lorsque le joueur choisi de ne pas utiliser tous ses lancers
                for de in des_a_relancer:
                    result_tour.remove(de)  # on conserve les dés non-relancés

            no_lancer += 1

        self.combinaison_actuelle = Combinaison(result_tour)
        return no_lancer-1      # on soustrait la dernière incrementation de no_lancer


    def ajouter_jetons(self, nb_jetons):
        """
        Cette méthode permet d'ajouter un nombre de jetons à ceux déjà détenus par le joueur
        :param nb_jetons: nombre de jetons à ajouter
        :return aucun
        """
        self.nb_jetons += nb_jetons

    def retirer_jetons(self, nb_jetons):
        """
        Cette méthode permet de retirer un nombre de jetons de ceux détenus par le joueur
        :param nb_jetons: nombre de jetons à retirer
        :return aucun
        """
        self.nb_jetons -= nb_jetons

    def __str__(self):
        """
        Cette méthode retourne une représentation d'un joueur. le format est "nom_du_joueur - nombre_de_jetons"
        Cette méthode est appelée lorsque vous faites print(A) où A est un joueur
        :return: retourne une chaine de caractère qui est une représentation.
            Exemple: "Joueur1 - 12"
        """
        return "{} - {}".format(self.nom, self.nb_jetons)

    def __le__(self, other):
        """
        Comparaison ( <= ) entre deux joueurs sur la base de leur nombre de jetons.
        :param other: le joueur auquel on se compare
        :return: True si le nombre de jetons de self est inférieur ou égal à celui de other
        """
        return self.nb_jetons <= other.nb_jetons

    def __ge__(self, other):
        """
        Comparaison ( >= ) entre deux joueurs sur la base de leur nombre de jetons.
        :param other: le joueur auquel on se compare
        :return: True si le nombre de jetons de self est supérieur ou égal à celui de other
        """
        return self.nb_jetons >= other.nb_jetons

    def __lt__(self, other):
        """
        Comparaison ( < ) entre deux joueurs sur la base de leur nombre de jetons.
        :param other: le joueur auquel on se compare
        :return: True si le nombre de jetons de self est inférieur à celui de other
        """
        return self.nb_jetons < other.nb_jetons

    def __gt__(self, other):
        """
        Comparaison ( > ) entre deux joueurs sur la base de leur nombre de jetons.
        :param other: le joueur auquel on se compare
        :return: True si le nombre de jetons de self est supérieur à celui de other
        """
        return self.nb_jetons > other.nb_jetons

    def __eq__(self, other):
        """
        Comparaison ( == ) entre deux joueurs sur la base de leur nombre de jetons.
        :param other: le joueur auquel on se compare
        :return: True si le nombre de jetons de self est égal à celui de other
        """
        return self.nb_jetons == other.nb_jetons

    def verifier_invariants(self):
        assert 0 <= self.nb_jetons <= NOMBRE_DE_JETONS_DU_JEU, "Le nombre de jetons du joueur est incorrect"



class JoueurAlgo(Joueur):
    """
    Joueur contrôlé par ordinateur avec stratégie de type 1 avec objectif 421
    """

    def __init__(self, nom):
        super().__init__(nom)


    def choisir_des_algo(self):
        """
        Choisi les dés qui fonf partie de la combinaison 421
        :return: liste des valeurs de dés à relancer
        """
        obj = [4, 2, 1]
        val_a_relancer = []
        for i, d in enumerate(self.combinaison_actuelle.representant):
            if d in obj:  # on ne relance pas le dés
                obj.remove(d)
            else:
                val_a_relancer.append(d)  # on relance le dés
        return val_a_relancer


if __name__ == '__main__':

    J1 = Joueur('Mic')
    J2 = Joueur('Will')
    assert len(J1.lancer_des(3)) == 3

    J2.ajouter_jetons(10)
    assert J2.nb_jetons == 10
    J2.retirer_jetons(1)
    assert J2.nb_jetons == 9


    assert J1 != J2
    assert J1 < J2
    assert J1 <= J2
    assert J2 > J1
    assert J2 >= J1
    assert J1 >= J1