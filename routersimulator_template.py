"""
Ohjelmointi 1 Kevät.
Tehtävä: Reititysprotokollasimulaattori
Konsta Puranen
278850
"""

router_dict = {}    # Avain: reitittimen nimi, Arvo: Router-olio

class Router:
    def __init__(self,name):
        self.__router_name = name
        self.__neighbours = []  # Lista naapurireitittimistä. Olioita.
        self.__routes = {}      # Avain: yhteys, Arvo: etäisyys

    def print_info(self):
        negh_names = []     # Naapuriolioiden nimet tulostamiseksi
        routes = []         # Reititysyhteydet tulostamiseksi

        for key in self.__routes:   # Luodaan lista yhteyksistä tulosteeksi
            routes.append('{:1s}:{:1d}'.format(key,self.__routes[key]))
            routes.sort()

        for olio in self.__neighbours:  # Luodaan lista naapureista tulosteeksi
            negh_names.append(olio.get_name())
            negh_names.sort()

        x = ' '         # 'x' on ulkonäköasettelua varten toteutettu muuttuja
        print("{:2s}{:2s}".format(x,self.__router_name))
        print("{:3s} N: {:5s}".format(x, ', '.join(negh_names)))
        print("{:3s} R: {:5s}".format(x,', '.join(routes)))

#Yhteyksien jakaminen naapuriolioille
    def receive_routing_table(self, send_olio):
        routes = send_olio.get_routes() # Lähettävän olion yhteydet

        for key in routes:
            if key in self.__routes:
                # Jotta reunaolion etäisyys on 0
                if not self.__routes[key] < routes[key]:
                    address = key
                    length = routes[key]
                    self.add_network(address,length)
            else:
                address = key
                length = routes[key] + 1
                self.add_network(address, length)

# Tarkistaa reitittimen yhteyden
    def has_route(self, network):
        if network in self.__routes:
            return self.__routes[network]
        else:
            return None
# Lisää naapuriolion
    def add_neighbour(self, neighbour):
        self.__neighbours.append(neighbour)
# Lisää verkkoyhteyden
    def add_network(self,address,length):
        self.__routes[str(address)] = int(length)
# Palauttaa kutsutun olion yhteydet
    def get_routes(self):
         return self.__routes
# Palauttaa kutsutun olion naapuri-oliot
    def get_neighbours(self):
        return self.__neighbours
# Palauttaa kutsutun olion nimen
    def get_name(self):
        return self.__router_name

def read_file(file):
    """
    Funktio tallentaa tiedostosta lukeman datan olioiksi
    tietorakenteeseen.
    """
    for rivi in file:
        rivi_list = rivi.split('!')
        main_olio = rivi_list[0]
        naapuri_oliot = rivi_list[1].split(';')
        router_dict[main_olio] = Router(main_olio)

        if rivi_list[-1] == '\n':   # Poistaa ylimääräisen '\n'-alkion.
            rivi_list.remove(rivi[-1])

        for naapuri in naapuri_oliot:
            if naapuri != '':
                if naapuri not in router_dict:
                    router_dict[naapuri] = Router(naapuri)
                else:
                    router_dict[main_olio].add_neighbour(router_dict[naapuri])
                    router_dict[naapuri].add_neighbour(router_dict[main_olio])

        if len(rivi_list)>2:    # jos tiedostossa on oliolle verkkoyhteys
            network_list = rivi_list[2].split(':')
            network = network_list[0]
            length = int(network_list[1])
            router_dict[main_olio].add_network(network,length)
def main():

    routerfile = input("Network file: ")
    if routerfile != '':    # Jos käyttäjä syöttää tiedoston
        try:
            file = open(routerfile,'r')
            read_file(file)     # Tiedoston luku funktiossa
            file.close()

        except FileNotFoundError: # Mahdolliset virheilmoitukset
            print("Error: the file could not be read or there is something wrong"
                  " with it.")
            return
        except IndexError:
            print("Error: the file could not be read or there is something wrong"
                  " with it.")
            return
    while True:
        command = input("> ")
        command = command.upper()

        if command == "P":
            name = input("Enter router name: ")
            if name in router_dict:     # Haetaan dictistä olion nimellä olio
                router = router_dict[name]
                router.print_info()
            else:
                print("Router was not found.")

        elif command == "PA":
            router_list = sorted(router_dict)   # Oliot aakkosjärjestyksessä
            for olio in router_list:
                router_dict[olio].print_info()

        elif command == "S":
            olio_name = input("Sending router: ")
            router = router_dict[olio_name]
            neighbourlist = router.get_neighbours()
            for neighbour in neighbourlist:
                neighbour.receive_routing_table(router)

        elif command == "C": 
            router1= input("Enter 1st router: ")
            router2= input("Enter 2nd router: ")

            router_dict[router1].add_neighbour(router_dict[router2])
            router_dict[router2].add_neighbour(router_dict[router1])

        elif command == "RR":
            routername = input("Enter router name: ")
            network = input("Enter network name: ")
            # Result on arvoltaan joko tyhjä tai etäisyys kysytystä yhteydestä
            result = router_dict[routername].has_route(network)
            # Tulosteet
            if result == None:
                print("Route to the network is unknown.")
            elif result == 0:
                print("Router is an edge router for the network.")
            else:
                print("Network {:1s} is {:1d} hops away".format(network,result))

        elif command == "NR":
            new_router = input('Enter a new name: ')
            if new_router not in router_dict: # Tarkistaa tilan uudelle oliolle
                router_dict[new_router] = (Router(new_router))

            else:
                print("Name is taken.")

        elif command == "NN":
            name = input("Enter router name: ")
            network = input("Enter network: ")
            length = input("Enter distance: ")
            router_dict[name].add_network(network,length)

        elif command == "Q":
            print("Simulator closes.")
            return

        else:
            print("Erroneous command!")
            print("Enter one of these commands:")
            print("NR (new router)")
            print("P (print)")  
            print("C (connect)")
            print("NN (new network)")
            print("PA (print all)")
            print("S (send routing tables)")
            print("RR (route request)")
            print("Q (quit)")

main()
