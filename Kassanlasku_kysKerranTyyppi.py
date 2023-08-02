class Kassa: 
    def __init__(self): 
        self.valuutat = {
            "s": [500, 200, 100, 50, 20, 10, 5], 
            "k": [2, 1, 0.5, 0.2, 0.1, 0.05] 
        }
        self.kassa = self.alusta_kassa()

    def alusta_kassa(self):
        return {
            "s": dict.fromkeys(self.valuutat["s"], 0),
            "k": dict.fromkeys(self.valuutat["k"], 0)
        }

    def lisaa_rahaa(self, tyyppi, arvo, maara):
        self.kassa[tyyppi][arvo] += maara

    def laske_tase(self):
        tase = 0
        for tyyppi in ["s", "k"]:
            for arvo, maara in self.kassa[tyyppi].items():
                tase += arvo * maara
        return round(tase, 2)

    def tyhjenna_kassa(self):
        self.kassa = self.alusta_kassa()

    def tulosta_kassa(self):
        print("\n{:<10}{:<15}{:<10}".format('Arvo €', 'Määrä kpl', 'Summa €'))
        print("\nSetelit:")
        for arvo, maara in self.kassa["s"].items(): 
            print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), arvo*maara))
    
        print("\nKolikot:")
        for arvo, maara in self.kassa["k"].items(): 
            print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), arvo*maara))

        print("Kassan tase on: " + str(self.laske_tase()) + "€")

        if self.laske_tase() > 400:
            ylimaaraiset = self.laske_tase() - 400
            ylimaaraiset_setelit_kolikot = {"s": {}, "k": {}}
            print("\nTilitettävät rahat (yli 400€):")
            print("{:<10}{:<15}{:<10}".format('Arvo €', 'Määrä kpl', 'Summa €'))
            for tyyppi in ["s", "k"]:
                for arvo in sorted(self.valuutat[tyyppi], reverse=True):
                    maara = self.kassa[tyyppi][arvo]
                    while maara > 0 and ylimaaraiset - arvo >= 0:
                        if arvo not in ylimaaraiset_setelit_kolikot[tyyppi]:
                            ylimaaraiset_setelit_kolikot[tyyppi][arvo] = 0
                        ylimaaraiset_setelit_kolikot[tyyppi][arvo] += 1
                        ylimaaraiset -= arvo
                        maara -= 1
            for tyyppi in ["s", "k"]:
                print("\n" + ("Setelit:" if tyyppi == "s" else "Kolikot:"))
                for arvo, maara in ylimaaraiset_setelit_kolikot[tyyppi].items():
                    print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), arvo*maara))

            print("Tilitettävä summa on: " + str(self.laske_tase()-400) + "€")

    def muokkaa_rahaa(self, tyyppi, arvo, uusi_maara):
        if arvo in self.kassa[tyyppi]:
            self.kassa[tyyppi][arvo] = uusi_maara
        else:
            print(f"Arvoa {arvo} ei löydy kassasta.")


def lisaa_rahaa(kassa, maara_vai_summa):
    for tyyppi in ["s", "k"]:
        print(f"\n{tyyppi.upper()} - {'Setelit' if tyyppi == 's' else 'Kolikot'}")
        for arvo in kassa.valuutat[tyyppi]:
            while True:
                try:
                    if maara_vai_summa == "m":
                        maara = int(input(f"Syötä kappalemäärä rahalle {arvo}: "))
                    else:
                        summa = float(input(f"Syötä summa rahalle {arvo}: "))
                        if abs(summa % arvo) < 1e-5 or abs(summa % arvo - arvo) < 1e-5:
                            maara = round(summa / arvo)
                        else:
                            print("Summan pitää olla jaollinen annetulla kolikolla/setelillä. Yritä uudelleen.")
                            continue
                    break
                except ValueError:
                    print("Virheellinen syöte. Yritä uudelleen.")
            kassa.lisaa_rahaa(tyyppi, arvo, maara)

def muokkaa_rahaa(kassa, maara_vai_summa):
    tyyppi = ""
    while tyyppi not in ["s", "k"]:
        tyyppi = input("Muokataanko seteleitä vai kolikoita? (s/k): ").lower()
        if tyyppi not in ["s", "k"]:
            print("Virheellinen syöte. Yritä uudelleen.")
    while True:
        try:
            arvo = float(input("Syötä arvo, jonka määrää haluat muokata: "))
            if arvo in kassa.kassa[tyyppi]:
                while True:
                    try:
                        if maara_vai_summa == "m":
                            uusi_maara = int(input("Syötä uusi kappalemäärä: "))
                        else:
                            summa = float(input(f"Syötä uusi summa rahalle {arvo}: "))
                            if abs(summa % arvo) < 1e-5 or abs(summa % arvo - arvo) < 1e-5:
                                uusi_maara = round(summa / arvo)
                            else:
                                print("Summan pitää olla jaollinen annetulla kolikolla/setelillä. Yritä uudelleen.")
                                continue
                        break
                    except ValueError:
                        print("Virheellinen syöte. Yritä uudelleen.")
                kassa.muokkaa_rahaa(tyyppi, arvo, uusi_maara)
                break
            else:
                print(f"Arvoa {arvo} ei löydy kassasta. Yritä uudelleen.")
        except ValueError:
            print("Virheellinen syöte. Yritä uudelleen.")

def laske_tase(kassa):
    print("Kassan tase on: " + str(kassa.laske_tase()) + "€")


def paaohjelma():
    kassa = Kassa()

    maara_vai_summa = ""
    while maara_vai_summa not in ["m", "s"]: 
        maara_vai_summa = input("Haluatko syöttää kappalemäärän vai summan? (m/s): ").lower()
        if maara_vai_summa not in ["m", "s"]: 
            print("Virheellinen syöte. Yritä uudelleen.")

    while True:
        print("\n1. Lisää rahaa")
        print("2. Laske tase")
        print("3. Tulosta kassa")
        print("4. Muokkaa rahamäärää")
        print("0. Lopeta")
        valinta = input("Valitse toiminto: ").lower()

        if valinta == '1':
            lisaa_rahaa(kassa, maara_vai_summa)
        elif valinta == '2':
            laske_tase(kassa)
        elif valinta == '3':
            kassa.tulosta_kassa()
        elif valinta == '4':
            muokkaa_rahaa(kassa, maara_vai_summa)
        elif valinta == '0':
            print("Kiitos ohjelman käytöstä.")
            kassa.tyhjenna_kassa()
            break
        else:
            print("Virheellinen syöte. Yritä uudelleen.")

paaohjelma()

## joe