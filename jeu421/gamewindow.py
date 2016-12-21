from tkinter import *
from jeu421.partie import *
from jeu421.joueur import *
from jeu421.combinaison import *
from jeu421.interface import *
from jeu421.ruleswindow import *
from jeu421.playwindow import *
from tkinter.colorchooser import *
from tkinter import messagebox
import os
from time import sleep

class MainWindow(Tk):

    def __init__(self):
        super().__init__()
        with open("trace_file_name.txt", 'r+') as self.fichier_trace:
            first_line = self.fichier_trace.readline()
            self.count = (int(first_line[20:-1]))+1
            self.fichier_trace.seek(0, 0)
            self.fichier_trace.write("Compteur de parties={}\r".format(self.count))
            self.fichier_trace.seek(0, 2)
            self.fichier_trace.write("\n-------------------------------------------------- \n Partie {}".format(self.count))
            # ligne precedente a remplacer par -- * un nombre pour augmenter la lisibilite
            # self.fichier_trace = open(trace_file_name, 'w')
            # if not first_line.strip():
            #     self.fichier_trace.write("0")
            # else:
            #     self.fichier_trace.write("\nDebut de la partie : " + str(self.count))


        self.title("JEU 421")
        #self.geometry('{}x{}'.format(800, 600))
        self.welcome_text = "Bienvenue dans le JEU du 421\n" \
                            "On joue au 421 à l'aide de trois dés et d'un certain nombre de jetons.\n" \
                            "Il se joue à deux joueurs ou plus."

        self.main_frame = Frame(self, width=800, height=600)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.center_label = Label(self.main_frame, text=self.welcome_text, justify=CENTER)
        self.center_label.grid(row=0, column=0, padx=10, pady=100)
        self.center_label.pack()

        button_frame = Frame(self.main_frame, width=400, height=400)
        button_frame.pack()

        self.boutton_play = Button(button_frame, text="Play Game", state=NORMAL, command=self.play_screen)
        self.boutton_play.grid(row=1)
        self.boutton_read = Button(button_frame, text="Read rules", state=NORMAL, command=self.rules_screen)
        self.boutton_read.grid(row=2)
        self.boutton_watch = Button(button_frame, text="Watch Game", state=NORMAL, command=self.lastgame_screen)
        self.boutton_watch.grid(row=3)

        self.liste_de_nom = []

    def main_screen(self):
        self.reset_main_frame()

        self.center_label = Label(self.main_frame, text=self.welcome_text, justify=CENTER)
        self.center_label.grid(row=0, column=0, padx=10, pady=10)
        self.center_label.pack()

        button_frame = Frame(self.main_frame)
        button_frame.pack()

        self.boutton_play = Button(button_frame, text="Play Game", state=NORMAL, command=self.play_screen)
        self.boutton_play.grid(row=1)
        self.boutton_read = Button(button_frame, text="Read rules", state=NORMAL, command=self.rules_screen)
        self.boutton_read.grid(row=2)
        self.boutton_watch = Button(button_frame, text="Watch Game", state=NORMAL, command=self.lastgame_screen)
        self.boutton_watch.grid(row=3)

    def play_screen(self):

        number_window = NumberOfPlayers(self)
        self.wait_window(number_window)

        # J'ai mis des message d'erreur dans la number_window pour gèrer ces cas (Mic)
        #if number_window.valeur + num <= 1:
            #return

        self.jeu = Partie(number_window.name_list, nb_human=number_window.valeur, nb_ai=number_window.valeur_ai)
        self.jeu.joueur_courant = self.jeu.joueurs[self.jeu.premier]

        self.reset_main_frame()

        # LabelFrame des dés
        # ---
        # Display des dés:
        frame_des = LabelFrame(self.main_frame, text="Nombre de joueurs = %s"%(int(number_window.valeur)), labelanchor=N)
        frame_des.grid(row=0, column=0, padx=10, pady=20, sticky=NSEW)

        canvas_des = Playwindow(self, frame_des, self.jeu)
        canvas_des.grid(row=0, column=0, padx=10, pady=0)
        canvas_des.dessiner_canvas()

        # Bouton pour lancer les dés
        self.button_lancer = Button(master=frame_des, text="Lancer le dé", state=NORMAL)
        self.button_lancer.config(command=lambda: canvas_des.lancer_des_premier())
        self.button_lancer.grid(row=1, column=0, padx=10, pady=0)
        self.button_end_tour = Button(master=frame_des, text="Terminer le tour", state=DISABLED)
        self.button_end_tour.config(command=lambda: canvas_des.clic_button_end_tour())
        self.button_end_tour.grid(row=2, column=0, padx=10, pady=0)

        # Message de jeu
        self.message = Label(frame_des, text=self.jeu.interface.message)
        self.message.grid(row=3, column=0, padx=10, pady=10)
        # ---

        # LabelFrame des evenements
        # ---
        frame_historique = LabelFrame(self.main_frame, text="Historique de la partie:", labelanchor=N)
        frame_historique.grid(row=0, column=1, padx=10, pady=20, sticky=NSEW)

        frame_evenements = LabelFrame(frame_historique, text="Evenements:", labelanchor=N, relief=FLAT)
        frame_evenements.grid(row=0, column=0, padx=10, pady=10)
        self.listbox_evenements = Listbox(frame_evenements, exportselection=False, width=40)
        self.listbox_evenements.grid(row=0, column=0, padx=10, pady=10)

        frame_jetons = LabelFrame(frame_historique, text="Jetons:", labelanchor=N, relief=FLAT)
        frame_jetons.grid(row=0, column=1, padx=10, pady=10)
        self.listbox_jetons = Listbox(frame_jetons, exportselection=False, width=40)
        self.listbox_jetons.grid(row=0, column=1, padx=10, pady=10)

        button_retour_au_menu = Button(master=self.main_frame, text="Retour Menu", state=NORMAL)
        button_retour_au_menu.config(command=lambda: self.main_screen())
        button_retour_au_menu.grid(row=1, sticky=W)

        Button(master=self.main_frame, text="Couleur", command=self.background_color).grid(row=1, sticky=E)

    def background_color(self):
        color = askcolor()
        self.main_frame.configure(background=color[1])
        print(color[1])  # DEBUG
        return color[1]

    def display_message_jeu(self, text="", color='black'):
        if text == None:
            text = self.jeu.interface.message

        self.message.configure(text=text, foreground=color)

    # def changer_nom(self, evenement=None):
    #     choix_window = ChoixNom(self, sorte="Nom")
    #     self.wait_window(choix_window)

    def add_info_to_trace(self,text=""):
        self.fichier_trace = open("trace_file_name.txt", "r+")
        self.fichier_trace.seek(0, 2)
        self.fichier_trace.write("\n          {}".format(text))  # cause des problemes
        self.fichier_trace.close()

    def add_info_to_eventlog(self, text=""):
        self.listbox_evenements.insert(END, text)
        self.listbox_evenements.yview(END)
        self.add_info_to_trace(text)

    def clear_scorelog(self):
        self.listbox_jetons.delete(0, END)

    def add_info_to_scorelog(self, text=""):
        self.listbox_jetons.insert(END, text)

    def lastgame_screen(self):
        print("Le bouttou visionner derniere partie a ete active")

        self.reset_main_frame()

        my_canvas = Canvas(self.main_frame)
        my_canvas.pack(ipadx=10, ipady=10)

        scrollbar = Scrollbar(my_canvas)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox_match = Listbox(my_canvas, yscrollcommand=scrollbar.set, exportselection=False, width=50)
        listbox_match.pack(fill=BOTH)
        #listbox_match.grid(row=0, column=0, padx=10, pady=10)
        scrollbar.config(command=listbox_match.yview)

        fichier = open("trace_file_name.txt", "r")
        #curr_lign = self.fichier_trace.readline(END)

        choose_match = ChoixNom(self, text=1)
        self.wait_window(choose_match)

        #print(' Partie %s' % int(choose_match.valeur))
        match_number = int(choose_match.valeur)
        search_string = (" Partie %s\n" % match_number)
        self.match_begin = 0
        self.match_end = 0

        with open("trace_file_name.txt") as myFile:
            for num, line in enumerate(myFile, 1): #find begining of match
                if search_string in line:
                    print('BEGIN found at line:', num)
                    self.match_begin = num


        search_string = (" Partie %s\n" % str(match_number+1))
        with open("trace_file_name.txt") as myFile:
            for num, line in enumerate(myFile, 1): #find end of match
                if search_string in line:
                    print('END found at line:', num)
                    self.match_end = (num-1)



        lines = fichier.readlines()
        for iter in range((self.match_begin-2), self.match_end):
            print(lines[iter])
            listbox_match.insert(END, lines[iter])
            # add to listbox + slider

        button_retour_au_menu = Button(master=my_canvas, text="Retour Menu", state=NORMAL)
        button_retour_au_menu.config(command=lambda: self.main_screen())
        button_retour_au_menu.pack()
        #button_retour_au_menu.grid(row=1, pady=10, sticky=S)


    def rules_screen(self):
        self.reset_main_frame()

        my_canvas = Canvas(self.main_frame)
        my_canvas.pack()

        Ruleswindow(my_canvas)

        button_retour_au_menu = Button(master=my_canvas, text="Retour Menu", state=NORMAL)
        button_retour_au_menu.config(command=lambda: self.main_screen())
        button_retour_au_menu.pack()

    def reset_main_frame(self):
        self.main_frame.destroy()
        self.main_frame = Frame(self, width=800, height=600)
        self.main_frame.pack(fill=BOTH, expand=1)


class NumberOfPlayers(Toplevel):

    def __init__(self, master, sorte="players"):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.name_list = []

        Label(self, text="Enter the number of {}".format(sorte)).grid(sticky=N)

        Label(self, text="Humans").grid(row=1, column=0)
        self.entree = Entry(self)
        self.entree.insert(END, '0')
        self.entree.grid(row=1, column=1)

        Label(self, text="AI").grid(row=2, column=0)
        self.entree_ai = Entry(self)
        self.entree_ai.insert(END, '0')
        self.entree_ai.grid(row=2, column=1)

        self.bouton_ok = Button(self, text="OK", command=self.close)
        self.bouton_ok.grid(padx=10, pady=10)

    def close(self):
        try:
            print(type(self.entree.get()))
            self.valeur = int(self.entree.get())
            self.valeur_ai = int(self.entree_ai.get())
            if self.valeur + self.valeur_ai <= 1 or self.valeur < 0 or self.valeur_ai < 0:
                messagebox.showerror("Erreur: Nombre de joueurs", "Le nombre total de joueurs doit être de 2 ou plus!")
                return
            else:
                self.grab_release()
                self.master.focus_set()

                lobby_window = PlayerLobby(self, self.valeur, self.valeur_ai)
                self.wait_window(lobby_window)
                self.name_list = lobby_window.liste_de_nom

                self.destroy()

        except ValueError or AttributeError:
            messagebox.showerror("Erreur: Nombre de joueurs", "Le nombre de joueur doit être un entier positif!")


class PlayerLobby(Toplevel):

    def __init__(self, master, number_of_players, number_ai):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.title("Lobby")
        self.number_of_players = number_of_players
        self.number_ai = number_ai
        self.liste_de_nom = []

        self.frame = LabelFrame(self, text="Nom des joueurs :", labelanchor=N)
        self.frame.grid(sticky=NSEW)

        self.name_box = Listbox(self.frame, height=number_of_players + number_ai, exportselection=False)
        self.name_box.grid(row=0, column=0)
        self.name_box.bind('<<ListboxSelect>>', self.mettre_a_jour_joueur)

        for i in range(self.number_of_players):
            self.name_box.insert(END, "Joueur " + str(i+1))
        for j in range(self.number_ai):
            self.name_box.insert(END, "AI " + str(j+1))

        #Label(self.frame, text="Nom: ").grid(row=1, column=0)
        #Entry(self.frame, state="readonly").grid(row=1, column=1)
        self.but_changer_nom = Button(self.frame, text="Edit Name", state=DISABLED, command=self.change_name)
        self.but_changer_nom.grid(row=1, column=0)

        self.bouton_finish = Button(self, text="Start Game", command=self.close)
        self.bouton_finish.grid(padx=10, pady=10)

        #self.mettre_a_jour_interface()

    def close(self):
        liste = []

        for i, name_box_entry in enumerate(self.name_box.get(0, END)):
            liste.append(name_box_entry)

        print(liste)

        self.grab_release()
        self.master.focus_set()

        self.liste_de_nom = liste

        #for i in self.liste_de_nom:
            #print(type(self.liste_de_nom[i]))

        self.destroy()


    def change_name(self):
        try:
            name = ChoixNom(self, sorte="nom")
            self.wait_window(name)

            index = self.name_box.curselection()[0]

            if name.valeur is None:
                name.fermer()
            else:
                self.name_box.delete(index)
                self.name_box.insert(index, name.valeur)

        except AttributeError:
            print("DEBUG CHANGE_NAME ERROR")

    def mettre_a_jour_joueur(self, evenement=None):
        index_joueur = self.name_box.curselection()[0]
        nom_joueur = self.name_box.get(index_joueur)

        self.but_changer_nom['state'] = NORMAL


    def mettre_a_jour_interface(self):
        self.name_box.delete(0, END)
        for i in range(self.number_of_players):
            self.name_box.insert(END, i+1)

        #self.name_box.selection_clear(0, END)

        #self.name_box.delete(0, END)
        #self.desactiver_gestion_compte()


class ChoixNom(Toplevel):

    def __init__(self, master, sorte="nom", text=0):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.valeur = None

        if text == 1:
            Label(self, text="Choisir le numero du match. 0 = dernier match.").grid()
            self.entree = Entry(self)
            self.entree.grid()
        else:
            Label(self, text="Entrez le nouveau {}".format(sorte)).grid()
            self.entree = Entry(self)
            self.entree.grid()

        self.bouton_ok = Button(self, text="OK", command=self.fermer)
        self.bouton_ok.grid(padx=10, pady=10)

    def fermer(self):
        if self.valeur is not None: # gere le cas ou l'utilisatieur ferme la fenetre
            self.valeur = str(self.entree.get())
        self.grab_release()
        self.master.focus_set()
        self.destroy()
