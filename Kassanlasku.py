class KASSA: 
    def __init__(self): # Määritellään setelit (s) ja kolikot (k) niiden nimellisarvojen mukaan.
        self.valuutat = {
            "s": [500, 200, 100, 50, 20, 10, 5], 
            "k": [2, 1, 0.5, 0.2, 0.1, 0.05] 
        }
        
        self.kassa = self.alusta_kassa() # Alustetaan kassa alusta_kassa -metodilla.

    def alusta_kassa(self): # Alustaa kassan määrittelemällä setelit ja kolikot
        return {
            "s": dict.fromkeys(self.valuutat["s"], 0),
            "k": dict.fromkeys(self.valuutat["k"], 0)
        }

    def lisaa_rahaa(self, tyyppi, arvo, maara): # Metodi rahan lisäämiseen kassaan. 
        self.kassa[tyyppi][arvo] += maara

    def laske_tase(self): # Laskee kassan taseen summaamalla setelien ja kolikoiden arvot.
        tase = 0
        for tyyppi in ["s", "k"]:
            for arvo, maara in self.kassa[tyyppi].items():
                tase += arvo * maara
        return round(tase, 2)

    def tyhjenna_kassa(self): # Tyhjentää kassan alustamalla sen uudelleen.
        self.kassa = self.alusta_kassa()
    def tulosta_kassa(self):# Tulostaa kassan sisällön ja laskee kassan taseen.
        print("\n{:<10}{:<15}{:<10}".format('Arvo €', 'Määrä kpl', 'Summa €'))
        print("\nSetelit:")
        for arvo, maara in self.kassa["s"].items(): 
            print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), arvo*maara))
    
        print("\nKolikot:")
        for arvo, maara in self.kassa["k"].items(): 
            print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), arvo*maara))

        print("Kassan tase on: " + str(self.laske_tase()) + "€")

        if self.laske_tase() > 400: # Jos kassan tase ylittää 400€, tulostaa ylimääräiset rahat, jotka tulee tilitettäväksi.
            ylimaaraiset = self.laske_tase() - 400
            ylimaaraiset_setelit_kolikot = {"s": {}, "k": {}}
            tilitettava_summa = {"s": 0, "k": 0}
            print("\nTilitettävät rahat (yli 400€):")
            print("{:<10}{:<15}{:<10}".format('Arvo €', 'Määrä kpl', 'Summa €'))

            # setelien ja kolikoiden minimimäärän luonti
            minimaalinen_maara = {500: 0, 200: 0, 100: 0, 50: 2, 20: 5, 10: 3, 5: 2, 
                                  2: 6, 1: 6, 0.5: 6, 0.2: 6, 0.1: 6, 0.05: 10}
            
            for tyyppi in ["s", "k"]:
                for arvo in sorted(self.valuutat[tyyppi], reverse=True):
                    maara = self.kassa[tyyppi][arvo] - minimaalinen_maara.get(arvo, 0)
                    while maara > 0 and ylimaaraiset - arvo >= -0.01:
                        if arvo not in ylimaaraiset_setelit_kolikot[tyyppi]:
                            ylimaaraiset_setelit_kolikot[tyyppi][arvo] = 0
                        ylimaaraiset_setelit_kolikot[tyyppi][arvo] += 1
                        ylimaaraiset -= arvo
                        tilitettava_summa[tyyppi] += arvo
                        maara -= 1
                print("\n" + ("Setelit:" if tyyppi == "s" else "Kolikot:"))
                for arvo, maara in ylimaaraiset_setelit_kolikot[tyyppi].items():
                    print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), arvo*maara))
                print("Tilitettävä summa " + ("seteleissä:" if tyyppi == "s" else "kolikoissa:") + " " + str(round(tilitettava_summa[tyyppi], 2)) + "€")

            print("Tilitettävä kokonaissumma on: " + str(round(sum(tilitettava_summa.values()), 2)) + "€")

    def muokkaa_rahaa(self, tyyppi, arvo, uusi_maara): # Muuttaa rahan määrää 
        if arvo in self.kassa[tyyppi]:
            self.kassa[tyyppi][arvo] = uusi_maara
        else:
            print(f"Arvoa {arvo} ei löydy kassasta.")


def lisaa_rahaa(kassa, maara_vai_summa):
    # Käy läpi sanakirjan avaimet ("s" ja "k").
    for tyyppi in ["s", "k"]:
        # Tulosta rahan tyyppi, joko setelit tai kolikot.
        print(f"\n{tyyppi.upper()} - {'Setelit' if tyyppi == 's' else 'Kolikot'}")
        # Käy läpi arvot, jotka liittyvät nykyiseen avaimen tyyppiin sanakirjassa.
        for arvo in kassa.valuutat[tyyppi]:
            while True:
                try:
                    # Riippuen käyttäjän valinnasta, pyydä joko lukumäärää tai kokonaissummaa 
                    if maara_vai_summa == "m":
                        maara = int(input(f"Syötä kappalemäärä rahalle {arvo}: "))
                    else:
                        summa = float(input(f"Syötä summa rahalle {arvo}: "))
                        # Jos kokonaissumma on jaollinen setelin/kolikon arvolla,
                        # laske setelien/kolikoiden lukumäärä.
                        if abs(summa % arvo) < 1e-5 or abs(summa % arvo - arvo) < 1e-5:
                            maara = round(summa / arvo)
                        else:
                            # Jos kokonaissumma ei ole jaollinen setelin/kolikon arvolla,
                            # tulosta virheilmoitus ja pyydä setelin/kolikon summa uudelleen.
                            print("Summan pitää olla jaollinen annetulla kolikolla/setelillä. Yritä uudelleen.")
                            continue
                    break
                except ValueError:
                    # Jos käyttäjän syöte ei ole numero, tulosta virheilmoitus ja kysy syötettä uudelleen.
                    print("Virheellinen syöte. Yritä uudelleen.")
            # Lisää lukumäärä seteleitä/kolikoita kassaan.
            kassa.lisaa_rahaa(tyyppi, arvo, maara)

def muokkaa_rahaa(kassa, maara_vai_summa):
    tyyppi = ""
    # Pyydä käyttäjältä, haluaako hän muokata seteleitä vai kolikoita.
    # Jatka kysymistä, kunnes käyttäjä antaa kelvollisen syötteen.
    while tyyppi not in ["s", "k"]:
        tyyppi = input("Muokataanko seteleitä vai kolikoita? (s/k): ").lower()
        if tyyppi not in ["s", "k"]:
            print("Virheellinen syöte. Yritä uudelleen.")
    while True:
        try:
            # Pyydä käyttäjältä setelien/kolikoiden arvo, jota hän haluaa muokata.
            arvo = float(input("Syötä arvo, jonka määrää haluat muokata: "))
            if arvo in kassa.kassa[tyyppi]:
                while True:
                    try:
                        # Riippuen käyttäjän valinnasta, pyydä joko uusi lukumäärä tai kokonaissumma seteleinä tai kolikoina.
                        if maara_vai_summa == "m":
                            uusi_maara = int(input("Syötä uusi kappalemäärä: "))
                        else:
                            summa = float(input(f"Syötä uusi summa rahalle {int(arvo)}€: "))
                            # Jos kokonaissumma on jaollinen setelin/kolikon arvolla laske setelien/kolikoiden lukumäärä.
                            if abs(summa % arvo) < 1e-5 or abs(summa % arvo - arvo) < 1e-5:
                                uusi_maara = round(summa / arvo)
                            else:
                                # Jos kokonaissumma ei ole jaollinen setelin/kolikon arvolla,
                                # tulosta virheilmoitus ja kysy uusi summa
                                print("Summan pitää olla jaollinen annetulla kolikolla/setelillä. Yritä uudelleen.")
                                continue
                        break
                    except ValueError:
                        # Jos käyttäjän syöte ei ole numero, tulosta virheilmoitus ja kysy syöte uudelleen.
                        print("Virheellinen syöte. Yritä uudelleen.")
                # Muokkaa setelien/kolikoiden lukumäärä kassassa.
                kassa.muokkaa_rahaa(tyyppi, arvo, uusi_maara)
                break
            else:
                # Jos käyttäjän antamaa arvoa ei löydy kassasta,
                # tulosta virheilmoitus ja kysy arvo uudelleen.
                print(f"Arvoa {int(arvo)}€ ei löydy " + ("seteleistä" if tyyppi == "s" else "kolikoista") + " yritä uudelleen.")
        except ValueError:
            # Jos käyttäjän syöte ei ole numero, tulosta virheilmoitus ja kysy syöte uudelleen
            print("Virheellinen syöte. Yritä uudelleen.")

def laske_tase(kassa):
    print("Kassan tase on: " + str(kassa.laske_tase()) + "€")  # Laskee kassan taseen summaamalla setelien ja kolikoiden arvot.


def paaohjelma():
    kassa = KASSA()
    print("Tämä on kassan tilitysohjelma.\n")
    maara_vai_summa = ""
    # Kysytään käyttäjältä haluaako hän syöttää rahan määrän vai summan.
    while maara_vai_summa not in ["m", "s"]: 
        maara_vai_summa = input("Haluatko syöttää rahojen kappalemäärän vai summan? (m/s): ").lower() 
        if maara_vai_summa not in ["m", "s"]: 
            print("Virheellinen syöte. Yritä uudelleen.")

    while True:
        print("\n1. Lisää rahaa")
        print("2. Laske tase")
        print("3. Tulosta kassa")
        print("4. Muokkaa rahamäärää")
        print("L. Lopeta")
        valinta = input("Valitse toiminto: ").lower()

        if valinta == '1':
            lisaa_rahaa(kassa, maara_vai_summa)
        elif valinta == '2':
            laske_tase(kassa)
        elif valinta == '3':
            kassa.tulosta_kassa()
        elif valinta == '4':
            muokkaa_rahaa(kassa, maara_vai_summa)
        elif valinta == 'l':
            print("Kiitos ohjelman käytöstä.")
            kassa.tyhjenna_kassa()
            break
        else:
            print("Virheellinen syöte. Yritä uudelleen.")

paaohjelma()
