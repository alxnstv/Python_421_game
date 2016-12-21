class Interface:

    def __init__(self):
        self.message = 'Lancer un dé pour débuter la partie'

    def choisir_des_a_relancer(self, resultat_du_lancer):
        """
        Méthode permettant de choisir selon un résultat de lancé de dés les dés qu'il veut relancer.
        Dans cette méthode, doit demander à l'utilisateur les valeurs de dés à relancer.
        Tant que les valeurs entrées ne sont pas dans la liste en paramètre, vous devez le redemander au joueur.
        :param resultat_du_lancer:  la liste des valeurs des dés où il faut choisir les valeurs de dés  à relancer
        :return: la liste des valeurs des dés choisis pour le relancement
        """
        n = len(resultat_du_lancer)
        choisir = True
        while choisir:
            choisir = False
            resultat_du_lancer_copie = resultat_du_lancer[:]
            temp = input("Choississez les dés à relancer. Exemple: 24 pour relancer les dés de valeurs 2 et 4\n"
                         "(Laissez vide pour garder votre combinaison actuelle):")
            temp = list(map(int, list(temp)))
            if len(temp) > n:
                choisir = True
            else:
                for v in temp:
                    if v in resultat_du_lancer_copie:
                        resultat_du_lancer_copie.remove(v)
                    else:
                        choisir = True
                        break
            if choisir:
                print("Trop de valeurs ou un des dés à relancer est invalide!")
        return temp

    def demander_entree(self, message_demande=""):
        return input(message_demande)

    def afficher(self, message=""):
        self.message = message