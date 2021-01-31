# Monty Hall Problem. 
# Ohjelmointi 1 Kevät 2020
# Konsta Puranen

from tkinter import *
from random import *
from tkinter import messagebox

DOORPICS = ['closed.gif','open.gif','money.gif']
DOORNUMBER = 3      # pelattavien ovien lukumäärä. Suositus 3.

class Monty_Hall:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Monty Hall Problem")
        self.__doorpics = []        # Kuvat ovista, ja palkinnosta
        self.__doornumber = 0

        for picfile in DOORPICS:        #lisätään kuvat listaan
            pic = PhotoImage(file=picfile)
            self.__doorpics.append(pic)

        self.__closed_doorpics = self.__doorpics[0]
        self.__open_doorpics = self.__doorpics[1]
        self.__money_pic = self.__doorpics[2]

        # Tehdään sekoitettu lista 0 ja ovien lukumäärän välillä.
        self.__door_order = sample(range(0, DOORNUMBER), DOORNUMBER)

        oviarvot=[]
        for value in self.__door_order: # Listan suurin alkio on voittava ovi.
            oviarvot.append(value)
        oviarvot.sort()
        self.__winning_door = oviarvot[-1]

        self.__doorpic_label = []   # Tehdään labelit kuville
        for i in range(DOORNUMBER):
            newlabel = Label(self.__window)
            newlabel.grid(row=1, column = i)
            self.__doorpic_label.append(newlabel)

        for label in self.__doorpic_label:      # Aluksi ovet on kiinni
            label.configure(image=self.__closed_doorpics)

        self.__buttons = []     # Lisätään valintanappulat listaan
        for i in range(DOORNUMBER):
            new_button = Button(self.__window, text='CHOOSE', bg='green',
                                command= lambda x=i: self.change_buttons(x))
            new_button.grid(row=2, column=i)
            self.__buttons.append(new_button)

        # play Button vie pelin asekeleella eteenpäin.
        self.__play_button=Button(text="PLAY",bg='blue',state=DISABLED,
                    command=lambda x=self.__doornumber: self.open_doors(self.__doornumber))
        self.__play_button.grid(row=0, column=0, columnspan=2, sticky=W)

        # Quit Button lopettaa pelin toiminnan
        self.__quit_button = Button(text= 'QUIT',bg='red', command=self.end_game)
        self.__quit_button.grid(row=0, column=3, columnspan=2, sticky=E)

        #Final Button selvittää lopuksi voiton tai tappion
        self.__final_button = Button(text="RESULT", bg='blue', state=DISABLED,
                                     command=self.final_winner)
        self.__final_button.grid(row=0,column=2,columnspan=2)

    def open_doors(self, chosen_door):
        """ funktio saa parametrinaan nappulalistan indeksin, joka on
        sama indeksi kuin ovi nappulan yläpuolella. Funktio avaa kaikki
        väärät ovet paitsi sen jonka käyttäjä valitsee. Jos käyttäjä valitsee
        heti oikean oven funktio jättää viereisen oven avaamatta.
        :param chosen_door:
        """
        winning_door_index = self.get_winner_index()

        self.__play_button.configure(state=DISABLED)
        self.__final_button.configure(state=NORMAL)

        for i in range(DOORNUMBER):     # Avataan kaikki ovet
            self.__doorpic_label[i].configure(
                image=self.__open_doorpics)

            # Suljetaan valittu ovi sekä voittava ovi.
            # Huomioidaan erikoistilanne jossa ekalla valittu voittava ovi

            if winning_door_index == chosen_door:
                self.__doorpic_label[winning_door_index].configure(
                    image=self.__closed_doorpics)
                if winning_door_index == 0:
                    self.__doorpic_label[winning_door_index+1].configure(
                        image=self.__closed_doorpics)
                else:
                    self.__doorpic_label[winning_door_index-1].configure(
                        image=self.__closed_doorpics)
            else:
                if i == chosen_door:
                    self.__doorpic_label[i].configure(
                        image=self.__closed_doorpics)

                if i == winning_door_index:
                    self.__doorpic_label[i].configure\
                        (image=self.__closed_doorpics)

        self.reset_buttons()    # Nollataan valintanappulat

    def change_buttons(self,buttonnumber):
        """ Funktio muuntaa valintanappuloiden tilaa. Funktio saa parametrina
        indeksin nappulalistasta, jotta tämän indeksin nappulaa voidaan
        käsitellä erikseen listan muista nappula-alkioista.

        :param buttonnumber:
        :return:
        """

        button = self.__buttons[buttonnumber]   # Nappula jota on painettu
        self.__doornumber=buttonnumber      # Lisätään tieto indeksistä oliolle

        for others in self.__buttons:   # Muutetaan jokainen nappula ei käytössä tilaan
            others.configure(bg='grey')
            others.configure(state=DISABLED)

        self.__play_button.configure(state=NORMAL) # Saatetaan play button käytettäväksi

        if button['text'] == 'CHOOSE':      # Nappula näyttää valitulta
            button.configure(text= "CHOSEN")
            button.configure(bg='red')
            button.configure(state=NORMAL)

        else:   # Jos nappulaa halutaan vaihtaa valinnan jälkeen
            self.reset_buttons()

    def final_winner(self):     # Funktio tarkastelee lopullisen ratkaisun
        win=self.get_winner_index()         # Voittavan oven indeksi
        chosen_door = self.__doornumber     # Valitun oven indeksi

        for i in range(DOORNUMBER):     # Avataan kaikki ovet ja lisätään palkinto
            self.__doorpic_label[i].configure(
                image=self.__open_doorpics)
        self.__doorpic_label[win].configure(image=self.__money_pic)

        if chosen_door==win:        # Viestit tuloksesta
            messagebox.showinfo(title='WINNER', message='GONGRATULATIONS!')
        else:
            messagebox.showinfo(title='YOU LOST', message='YOU LOST')

        for button in self.__buttons:   # Kaikki paitsi quit nappula pois käytöstä
            button.configure(state=DISABLED)
        self.__play_button.configure(state=DISABLED)
        self.__final_button.configure(state=DISABLED)

    def get_winner_index(self):    # Voittavan oven indeksi
        return self.__door_order.index(self.__winning_door)

    def reset_buttons(self):    # Funktio asettaa nappulat lähtötilaan

        for button in self.__buttons:
            button.configure(text= "CHOOSE")
            button.configure(bg='GREEN')
            button.configure(state=NORMAL)
            self.__play_button.configure(state=DISABLED)

    def end_game(self):     # Lopettaa ohjelman
        self.__window.destroy()

    def start(self):      # Aloitetaan ohjelma
        if DOORNUMBER < 3:  # Jos ovia on valittu vähemmän kuin kaksi ohjelma ei aukea
                            # Tulostetaan virheilmoitus
            messagebox.showerror(title="Error",
                                 message="Amount of doors must be 3 or more.")
            exit()
        else:   #   Pelin alkutulosteet
            messagebox.showinfo(title='Monty Hall',
            message="This is Monty Hall problem. Behind one door there is a price. "
                    "Other doors leave you with empty hands. "
                    "Choose one door, then press 'PLAY'. "
                    "You get to choose again this time false door already open."
                    " After second choice press 'RESULT' for result. GOOD LUCK!")
            self.__window.mainloop()
def main():
    ui=Monty_Hall()
    ui.start()
main()
