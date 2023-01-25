from PIL import Image
import numpy as np
from tqdm import tqdm
from time import sleep
from os import getcwd, listdir, path
from math import modf, ceil, floor
from time import sleep
from threading import Thread

class MuunnaKuva():
    def __init__(self, kuva: str) -> None:
            self.kuva = kuva
            self.polku = getcwd()         
    
    def __pyorista(self, n: float | int, tarkkuus: int = 0) -> int:
        "tarkkuus kertoo kuinka monen desimaalin tarkuuteen pyoristää"
        tarkkuus += 1
        _, b = modf(n)
        if b >= float(f"0"*tarkkuus+".5"):
            return ceil(n)
        else:
            return floor(n)
                
    def suorita(self) -> Image.Image:
        with Image.open(self.kuva) as analysoitava_kuva:
            leveys, korkeus = analysoitava_kuva.size

            if leveys > 2000 or korkeus > 2000:
                analysoitava_kuva.info
                leveys, korkeus = self.__pyorista(leveys/2), self.__pyorista(korkeus/2)

            if analysoitava_kuva.mode != "RGB":
                analysoitava_kuva=analysoitava_kuva.convert("RGB")

            analysoitava_kuva = self.analysoi_kuva(analysoitava_kuva)

            y_uusi_kuva, x_uusi_kuva = 0,0

            with Image.new("RGBA",(leveys*25,korkeus*25), (0,0,0,0)) as uusi_kuva:
                for lista in tqdm(analysoitava_kuva):
                    for pikselin_vari_arvo in lista:
                        pikselin_vari_arvo = int(pikselin_vari_arvo)

                        if pikselin_vari_arvo == 0:
                            x_uusi_kuva += 25

                        else:
                            varit = [614, 939, 606, 985, 1098, 964, 967, 810, 896, 957, 797, 521, 934, 987, 994, 936, 807, 755, 936, 895, 865, 1028, 896, 551, 984, 723, 696, 909, 804, 754, 873, 877, 485, 362, 1040, 323, 392, 922, 556, 1237, 985, 349, 481, 518, 972, 640, 582, 224, 380, 596, 312, 471, 402, 348, 480, 577, 404, 475, 344, 659, 365, 219, 410, 969, 1085, 826, 418, 1100, 932, 427, 825, 468, 708, 199, 585, 764, 523, 408, 615, 327, 444, 449, 562, 213, 545, 444, 601, 399, 560, 473, 439, 670, 495, 561, 1319, 1157, 1170, 1106, 1405, 1323, 1328, 790, 767, 966, 332, 975, 1046, 489, 626, 1379, 564, 1265, 693, 1370, 1023, 718, 1449, 1000, 609, 1259, 1286, 554, 816, 338, 492, 511, 528, 379, 199, 446, 509, 373, 401, 567, 761, 261, 324, 394, 207, 90, 80, 313, 399, 725, 673, 854]
                            lyodetytyt_varit = {}
                            valittu_vari_arvo = 2000
                            
                            if pikselin_vari_arvo in lyodetytyt_varit:
                                valittu_vari_arvo = lyodetytyt_varit[pikselin_vari_arvo]

                            else:
                                for laskettu_vari_arvo  in varit:
                                    if valittu_vari_arvo > abs(pikselin_vari_arvo -  laskettu_vari_arvo) > 0:
                                        valittu_vari_arvo = laskettu_vari_arvo
                                        lyodetytyt_varit[pikselin_vari_arvo] = laskettu_vari_arvo

                            numero=varit.index(valittu_vari_arvo)
                            try:
                                with Image.open(path.join(self.polku,"emoijit",f"emoiji_{numero}.png")) as kopioitava_kuva:
                                    uusi_kuva.paste(kopioitava_kuva, (x_uusi_kuva,y_uusi_kuva))
                            except FileNotFoundError:
                                print(f"kuvaa emoiji_{numero}.png ei ole kansiossa emoiji_kuvat")
                                
                            x_uusi_kuva += 25

                    y_uusi_kuva += 25
                    x_uusi_kuva = 0

                return uusi_kuva

    def analysoi_kuva(self, analysoitava_kuva: Image) -> np.array:
        """laskee kuvan pikselit yhteen"""
        #kuvan pikselit
        analysoitava_kuva = np.array(analysoitava_kuva)*[1,2,3]

        #laskee pikselin väri arvot yhteen
        return analysoitava_kuva.sum(axis=2)


class Aplikaatio:
    def __init__(self) -> None:
        pass

    def logo(self):
        print(" _____                       _     _   _         _  __                        ")
        print("| ____|  _ __ ___     ___   (_)   (_) (_)       | |/ /  _   _  __   __   __ _ ")
        print("|  _|   | '_ ` _ \   / _ \  | |   | | | |       | ' /  | | | | \ \ / /  / _` |")
        print("| |___  | | | | | | | (_) | | |   | | | |       | . \  | |_| |  \ V /  | (_| |")
        print("|_____| |_| |_| |_|  \___/  |_|  _/ | |_|       |_|\_\  \__,_|   \_/    \__,_|")
        print("                                |__/                                          ")

    def viiva(self, merkki: str, pituus: int):
        for i in range(pituus):
            print(merkki, end="")

        

    def laatikko(self, teksti: str):
        """
        ympäröi tekstin laatikolla
        uuden rivin saa // \n
        rivin saa keskitettynä ympäröimällä sanan merkillä *\n
        """

        n = 0
        pisin_pituus = 0
        teksti=teksti.split("//") #rivien jako

        #suuriman rivin määritys
        for rivi in teksti:
            rivin_pituus = len(rivi)

            if rivin_pituus == 0:
                teksti[n] = " "
                rivi = " "
                rivin_pituus = 1

            if rivi[0] == "*" and rivi[-1] == "*":
                rivin_pituus -= 2

            if rivin_pituus > pisin_pituus:
                pisin_pituus = rivin_pituus

            n += 1

        # tekstin keskitys
        for rivi in teksti:
            if rivi[0] == "*" and rivi[-1] == "*":
                n = teksti.index(rivi)
                rivi = rivi[1:-1]
                rivi = rivi.center(pisin_pituus)
                teksti[n] = rivi

            else:
                continue


        pisin_pituus += 2

        #laatiko tekeminen
        print("╔", end="")
        self.viiva("═",pisin_pituus)
        print("╗")

        for rivi in teksti:
            rivi = rivi + " "*(pisin_pituus-len(rivi))

            print(f"║ {rivi[:-2]} ║")


        print("╚", end="")
        self.viiva("═",pisin_pituus)
        print("╝")

    def onko_kuva(self, tiedosto: str) -> bool:
        """testaa onko tiedosto kuva"""
        if tiedosto.endswith(".png") or tiedosto.endswith(".jpg") or tiedosto.endswith(".jpeg"):
            return True
        else:
            return False

    def main(self):
        self.logo()
        while True:
            print(" ")

            print(" ")
            self.laatikko("*Pää valikko*//Muuna kuva: m//Ohjeet: o//Poistu: p")
            valittu_kohta = input("Valitse kohta: ")

            if valittu_kohta == "o":
                while True:
                    print(" ")
                    self.laatikko("*Ohjeet*////Muuntaaksesi kuvan pikselit emojiksi kopio kaikki kuvat//kansioon ”muunnettavat kuvat”.Sen jälkeen valitse//päävalikosta ”Muuna kuva” ja ohjelma//muuntaa kuvan.////takaisin: t")
                    valittu_kohta = input("Valitse kohta: ")
                    if valittu_kohta.lower() == "t":
                        break

            elif valittu_kohta.lower() == "m":
                while True:
                    print(" ")
                    polku = getcwd()     
                    tiedostot = listdir(path.join(polku,"muunnettavat kuvat"))

                    for tiedosto in tiedostot:
                        if self.onko_kuva(tiedosto):
                            continue
                        else:
                            tiedostot.pop(tiedosto.index(tiedosto))
                            
                    if len(tiedostot) == 0:
                        print("Muunettavia kuvia ei ole")
                        sleep(.5)
                        break

                    tiedostott = "Tiedostot//"
                    for tiedosto in tiedostot:
                        tiedostott = tiedostott + f"    {tiedosto}//"

                    tiedostott = tiedostott[:-2]

                    self.laatikko(tiedostott)

                    valittu_kohta = input("Haluatko muuntaakuvat (k/e): ")
                    
                    if valittu_kohta.lower() == "k":
                        for kuva in tiedostot:
                            muunna_kuva = MuunnaKuva(path.join(polku,"muunnettavat kuvat",kuva))
                            muunnettu_kuva = muunna_kuva.suorita()

                            kuva, _ = kuva.rsplit(".",1)
                            
                            muunnettu_kuva.save(path.join(polku,"muunnettavat kuvat",f"emoiji_{kuva}.png"))

                        print("Muunettu")
                        break


                    elif valittu_kohta.lower() == "e":
                        break


            elif valittu_kohta.lower() == "p":
                break

            else:
                pass


class Kaynistys():
    def __init__(self) -> None:
        self.onko_kaynissa = True
        self.onko_kaiki_ok = False
        self.virhe = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
        self.polku = getcwd()        

    def main(self):

        t_1 = Thread(target=self.prosessointi)
        t_2 = Thread(target=self.kaikki_ok)
        t_1.start()
        t_2.start()        
        t_1.join()
        t_2.join()

        if self.onko_kaiki_ok:
            appi = Aplikaatio()
            appi.main()
             

    def kaikki_ok(self):
        kansiot_virhe, onko_kansiot_virhe = self.kansiot_ok()
        emoiji_kuva_virhe, onko_kaikki_emoiji_kuvat = self.emoiji_kuvat_ok()

        self.onko_kaynissa = False
        
        if not onko_kaikki_emoiji_kuvat  and not onko_kaikki_emoiji_kuvat:
            self.onko_kaiki_ok = True


        if onko_kansiot_virhe:
            self.virhe += kansiot_virhe+"\n"

        
        if onko_kaikki_emoiji_kuvat:
            self.virhe += emoiji_kuva_virhe+"\n"

        

    def prosessointi(self):
        while self.onko_kaynissa:  
            print("käynistyy⠀⠀⠀", end="\r")
            sleep(.2)
            print("käynistyy.⠀⠀", end="\r")
            sleep(.2)
            print("käynistyy..⠀", end="\r")
            sleep(.2)
            print("käynistyy...", end="\r")
            sleep(.2)

        print(self.virhe, end="\r")
    def kansiot_ok(self) -> tuple[str, bool]:
        kansiot = listdir(self.polku)
        
        virhe_viesti = ""
        if "muunnettavat kuvat" not in kansiot:
            virhe_viesti += "muunnettavat kuvat, "

        if "emoijit" not in kansiot:
            virhe_viesti += "emoijit, "
        
        
        if virhe_viesti == "":
            return "", False
        else:
            return f"Kansioita {virhe_viesti[:-2]} ei ole", True
            
    
    def emoiji_kuvat_ok(self) -> bool:
        try:
            kuvat = listdir(path.join(self.polku, "emoijit"))
        except FileNotFoundError:
            return "", False
            
        n = False

        virhe_viesti = ""
        for i in range(146):
            if f"emoiji_{i}.png" not in kuvat:
                virhe_viesti += f"emoiji_{i}.png, "
                n = True

        if n:    
            virhe_viesti = f"Kuvia ei ole {virhe_viesti[:-2]}"   
            return "", True
        else:         
            return virhe_viesti, False

   

if __name__ == "__main__":
    kaynista = Kaynistys()
    kaynista.main()