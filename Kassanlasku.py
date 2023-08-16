from decimal import Decimal, InvalidOperation

class KASSA: 
    def __init__(self): 
        self.valuutat = {
            "s": [Decimal('500'), Decimal('200'), Decimal('100'), Decimal('50'), Decimal('20'), Decimal('10'), Decimal('5')], 
            "k": [Decimal('2'), Decimal('1'), Decimal('0.5'), Decimal('0.2'), Decimal('0.1'), Decimal('0.05')] 
        }
        self.kassa = self.alusta_kassa()

    def alusta_kassa(self): 
        return {
            "s": dict.fromkeys(self.valuutat["s"], 0),
            "k": dict.fromkeys(self.valuutat["k"], 0)
        }

    def lisaa_rahaa(self, tyyppi, arvo, maara): 
        self.kassa[tyyppi][Decimal(arvo)] += maara

    def laske_tase(self): 
        tase = Decimal('0')
        for tyyppi in ["s", "k"]:
            for arvo, maara in self.kassa[tyyppi].items():
                tase += arvo * Decimal(maara)
        return tase

    def tyhjenna_kassa(self):
        self.kassa = self.alusta_kassa()
        

    def tulosta_kassa(self): 
        print("\n{:<10}{:<15}{:<10}".format('Arvo €', 'Määrä kpl', 'Summa €'))
        print("\nSetelit:")
        for arvo, maara in self.kassa["s"].items(): 
            print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), Decimal(arvo)*Decimal(maara)))
        
        print("\nKolikot:")
        for arvo, maara in self.kassa["k"].items(): 
            print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), Decimal(arvo)*Decimal(maara)))
        
        kassan_tase = Decimal(self.laske_tase())
        print("Kassan tase on: " + str(kassan_tase) + "€")

        if kassan_tase > Decimal('400'): 
            ylimaaraiset = kassan_tase - Decimal('400')
            ylimaaraiset_setelit_kolikot = {"s": {}, "k": {}}
            tilitettava_summa = {"s": Decimal('0'), "k": Decimal('0')}
            print("\nTilitettävät rahat (yli 400€):")
            print("{:<10}{:<15}{:<10}".format('Arvo €', 'Määrä kpl', 'Summa €'))
            
            minimaalinen_maara = {500: 0, 200: 0, 100: 0, 50: 8, 20: 5, 10: 3, 5: 2, 
                    2: 6, 1: 6, 0.5: 6, 0.2: 6, 0.1: 6, 0.05: 10}

            # Yhdistä setelit ja kolikot yhdeksi listaksi ja käytä Decimal-arvoja
            kaikki_rahat = []
            for tyyppi in ["s", "k"]:
                for arvo in self.valuutat[tyyppi]:
                    kaikki_rahat.append((tyyppi, Decimal(arvo)))

            kaikki_rahat.sort(key=lambda x: x[1], reverse=True)

            # Lasketaan ylimääräiset rahat
            for tyyppi, arvo in kaikki_rahat:
                maara = self.kassa[tyyppi][arvo] - minimaalinen_maara.get(arvo, 0)
                while maara > 0 and ylimaaraiset - arvo >= Decimal('0'):
                    if arvo not in ylimaaraiset_setelit_kolikot[tyyppi]:
                        ylimaaraiset_setelit_kolikot[tyyppi][arvo] = 0
                    ylimaaraiset_setelit_kolikot[tyyppi][arvo] += 1
                    ylimaaraiset -= arvo
                    tilitettava_summa[tyyppi] += arvo
                    maara -= 1
                    self.kassa[tyyppi][arvo] -= 1

            # Ota lisää rahoja, jos tarpeen
            if ylimaaraiset > Decimal('0'):
                for tyyppi, arvo in sorted(kaikki_rahat, key=lambda x: abs(self.kassa[x[0]][x[1]] - Decimal(minimaalinen_maara.get(x[1], 0)))):
                    while self.kassa[tyyppi][arvo] > 0 and ylimaaraiset - arvo >= Decimal('0'):
                        if arvo not in ylimaaraiset_setelit_kolikot[tyyppi]:
                            ylimaaraiset_setelit_kolikot[tyyppi][arvo] = 0
                        ylimaaraiset_setelit_kolikot[tyyppi][arvo] += 1
                        ylimaaraiset -= arvo
                        tilitettava_summa[tyyppi] += arvo
                        self.kassa[tyyppi][arvo] -= 1

            # Tulostetaan tilitettävät setelit ja kolikot
            for tyyppi in ["s", "k"]:
                print("\n" + ("Setelit:" if tyyppi == "s" else "Kolikot:"))
                for arvo, maara in sorted(ylimaaraiset_setelit_kolikot[tyyppi].items(), key=lambda item: item[0], reverse=True):
                    print("{:<10}{:<15}{:<10.2f}".format(arvo, int(maara), Decimal(arvo)*Decimal(maara)))
                print("Tilitettävä summa " + ("seteleissä:" if tyyppi == "s" else "kolikoissa:") + " " + str(tilitettava_summa[tyyppi]) + "€")

            print("Tilitettävä kokonaissumma on: " + str(sum(tilitettava_summa.values())) + "€")


    def muokkaa_rahaa(self, tyyppi, arvo, uusi_maara): 
        arvo_decimal = Decimal(str(arvo))
        if arvo_decimal in self.kassa[tyyppi]:
            self.kassa[tyyppi][arvo_decimal] = uusi_maara
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
                        summa = Decimal(input(f"Syötä summa rahalle {arvo}: "))
                        arvo_decimal = Decimal(str(arvo))
                        
                        # Jos kokonaissumma on jaollinen setelin/kolikon arvolla,
                        # laske setelien/kolikoiden lukumäärä.
                        if summa % arvo_decimal == 0:
                            maara = int(summa / arvo_decimal)
                        else:
                            # Jos kokonaissumma ei ole jaollinen setelin/kolikon arvolla,
                            # tulosta virheilmoitus ja pyydä setelin/kolikon summa uudelleen.
                            print("Summan pitää olla jaollinen annetulla kolikolla/setelillä. Yritä uudelleen.")
                            continue
                    break
                except (ValueError, InvalidOperation):
                    # Jos käyttäjän syöte ei ole numero, tulosta virheilmoitus ja kysy syötettä uudelleen.
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
            arvo = Decimal(input("Syötä arvo, jonka määrää haluat muokata: "))
            if arvo in kassa.kassa[tyyppi]:
                while True:
                    try:
                        if maara_vai_summa == "m":
                            uusi_maara = int(input("Syötä uusi kappalemäärä: "))
                        else:
                            summa = Decimal(input(f"Syötä uusi summa rahalle {int(arvo)}€: "))
                            arvo_decimal = Decimal(str(arvo))
                            if summa % arvo_decimal == 0:
                                uusi_maara = int(summa / arvo_decimal)
                            else:
                                print("Summan pitää olla jaollinen annetulla kolikolla/setelillä. Yritä uudelleen.")
                                continue
                        break
                    except (ValueError, InvalidOperation):
                        print("Virheellinen syöte. Yritä uudelleen.")
                kassa.muokkaa_rahaa(tyyppi, arvo, uusi_maara)
                break
            else:
                print(f"Arvoa {int(arvo)}€ ei löydy " + ("seteleistä" if tyyppi == "s" else "kolikoista") + " yritä uudelleen.")
        except (ValueError, InvalidOperation):
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
