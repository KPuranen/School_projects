"""
Ohjelmoinnin harjoitustyö syksy 2020.
Konsta Puranen 

Ohjelma tarjoaa käyttäjälle sopivaa yhtiötä käyttäjän määrittämien tunnuslukujen perusteella.
Alkutiedoston lista koostuu Inderes:n seuraamista 120 yhtiöstä helsingin pörssissä 2019.
"""

STOCKS = {} #Tallennetaan osakket olioina key= osakkeen nimi : value = olio

class Osake:
    def __init__(self,name, pb_luku, pe_luku, roi):
        self.__stock_name = name    #osakkeen nimi
        self.__pb_luku = pb_luku    #osakkeen p/b-arvo
        self.__pe_luku = pe_luku    #osakkeen p/e-arvo
        self.__roi = roi            #osakkeen roi-%

    def print_list(self):   #Funktio tulostaa yhtiön nimen ja tunnusluvut vierekkäin
        return("{:25s} {:5.1f} {:5.1f} {:5.1f}" .format(self.__stock_name,self.__pb_luku,self.__pe_luku,self.__roi))


    def check_pe(self, pe): #Funktio tarkastaa onko yhtiön p/e-arvo annettua rajaa pienempi
        if 0 < self.__pe_luku <= pe:
            return True

    def check_pb(self, pb):  #Funktio tarkastaa onko yhtiön p/b-arvo annettua rajaa pienempi
        if 0 < self.__pb_luku <= pb:
            return True
    
    def check_roi(self, roi):   #Funktio tarkastaa onko yhtiön roi-% annettua rajaa suurempi
        if self.__roi >= roi:
            return True

    def get_name(self): #funktio palauttaa olion nimen
        return self.__stock_name

    def get_pe(self):   #funktio palauttaa olion p/e-arvon
        return self.__pe_luku

    def get_pb(self):   #funktio palauttaa olion p/b-arvon
        return self.__pb_luku

    def get_roi(self):  #funktio palauttaa olion roi-%
        return self.__roi

def read_file(tiedosto):
    """
    param: lähtötiedosto
    return: yhtiöt listan muodossa
    
    funktio lukee csv-tiedostosta alkutiedot ja palauttaa sisennetyn listan yhtiöistä
    """
    yhtiöt = []
    file = open(tiedosto, 'r')
    for rivi in file:
        rivit = rivi.split(';')
        yhtiöt.append(rivit)
    file.close()

    del yhtiöt[0:2] #Poistetaan ylimääräiset tunnukset csv-tiedoston alkutiedoista
    return yhtiöt

def tulostelistaus():   #funktio tulostaa otsikot tulosteen selkeyttämiseksi
    print()
    print("{:27s} {:5s} {:5s} {:5s}" .format("Osake", "P/B", "P/E", "ROI-%"))

def convert_float(luku):
    """
    param: luku string muodossa
    return: sama luku floatina

    Funktio muuttaa tiedoston desimaalierottimena käyttämän pilkun pisteeksi ja tekee luvusta float typen.
    """
    eka,toka = luku.split(',')
    eka = int(eka)
    toka = int(toka)
    tulos = "{:d}.{:1d}".format(eka,toka)
    return float(tulos)
   

def yhtiö_olio(yhtiöt): #Funktio luo oliot alkutiedoista ja tallettaa ne hajautustauluun
    for yhtiö in yhtiöt:
        nimi = yhtiö[0]

        pb_luku = convert_float(yhtiö[15])
        
        pe = yhtiö[24].replace(" ", "")
        pe_luku = convert_float(pe)
        
        roi = yhtiö[21].replace("%","")
        roi_pr = convert_float(roi)

        STOCKS[nimi] = Osake(nimi,pb_luku,pe_luku,roi_pr)

def search_stock():

    result = []     #yhtiöt jotka täyttävät kaikki ehdot

    pe_good = []    #Yhtiöt joiden p/e on rajaa pienempi tai yhtäsuuri
    pb_good = []    #yhtiöt joiden p/b on rajaa pienempi tai yhtäsuuri
    roi_good = []   #yhtiöt joiden roi-% on rajaa suurempi

    pe = input("Give p/e threshold: ")
    if pe != '':
        pe = float(pe)

        for stock in STOCKS:
            osake_pe = STOCKS[stock].check_pe(pe)   #tarkistetaan kuuluvuus

            if osake_pe:
                pe_good.append(STOCKS[stock])   #lisätään osake listaan jos kuuluvuus tosi

    else:   #jos rajaa ei anneta lisätään kaikki yhtiöt listaan
        for stock in STOCKS:   
            pe_good.append(STOCKS[stock])

    pb = input("Give p/b threshold: ")
    if pb != '':
        pb = float(pb)

        for stock in STOCKS:
            osake_pb = STOCKS[stock].check_pb(pb)   #tarkistetaan kuuluvuus

            if osake_pb:
                pb_good.append(STOCKS[stock])       #lisätään osake listaan jos kuuluvuus tosi

    else:   #jos rajaa ei anneta lisätään kaikki yhtiöt listaan
        for stock in STOCKS:
            pb_good.append(STOCKS[stock])

    roi = input("Give ROI-% threshold: ")
    if roi != '':
        roi = float(roi)

        for stock in STOCKS:
            osake_roi = STOCKS[stock].check_roi(roi)    #tarkistetaan kuuluvuus

            if osake_roi:
                roi_good.append(STOCKS[stock])      #lisätään osake listaan jos kuuluvuus tosi

    else:   #jos rajaa ei anneta lisätään kaikki yhtiöt listaan. Tällöin arvolla ei ole merkitystä tulosteeseen.
        for stock in STOCKS:
            roi_good.append(STOCKS[stock])

    STOCKS_sorted = sorted(STOCKS)  #järjestää listan aakkosjärjestykseen
    for stock in STOCKS_sorted:
        if STOCKS[stock] in pe_good and STOCKS[stock] in pb_good and STOCKS[stock] in roi_good:
            result.append(STOCKS[stock])    # Luodaan lista yhtiöistä jotka löytyvät kaikista tunnuslukulistoista

    tulostelistaus()        #Tulostaa listan tunnuslukuihin sopivista yhtiöistä 
    for stock in result:
        print("{:25s} {:5.1f} {:5.1f} {:5.1f}" .format(stock.get_name(),stock.get_pb(),stock.get_pe(),stock.get_roi()))

def listaus():  #Tulostaa kaikki alkutiedoston yhtiöt aakkosjärjestyksessä
    Stocks = sorted(STOCKS)
    tulostelistaus()
    for key in Stocks:
        print(STOCKS[key].print_list())

def show_help():    #Funktio joka tulostaa mahdolliset komennot
    print("COMMANDS:")
    print("LA: (list all)")
    print("Q: (quit)")
    print("SS: (search stock)")

def main():
    yhtiöt = read_file("company_history_data.csv")
    yhtiö_olio(yhtiöt)

    print("Command 'help' to see available commands")
    while True:     #looppi joka pyörii niin kauan kunnes 'Q' annetaan komennoksi
        command = input(">") 
        command = command.upper()   #mikä tahansa komento tehdään isoiksi kirjaimiksi

        if command == "LA": #Listataan kaikki yhtiöt
            listaus()
        
        elif command == "HELP" :    #tulosta mahdolliset komennot
            show_help()
        
        elif command == "SS":   #etsi yhtiöitä tunnuslukujen avulla
            search_stock()
        
        elif command == "Q":    # Lopettaa ohjelman pyörimisen
            return
        
        else:
            print("available commands are:")    #Tyhjä komento tulostaa listan komennoista
            show_help()

main()
