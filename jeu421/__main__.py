#from random import seed
#from jeu421.partie import Partie
#from jeu421.interface import Interface
from jeu421.gamewindow import MainWindow


if __name__ == "__main__":
    #seed(52) # pour correction ou tests (fixer un seed)
    #interface = Interface()

    main_window = MainWindow()
    main_window.mainloop()
