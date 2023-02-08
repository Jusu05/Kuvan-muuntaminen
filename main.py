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
            self.varit = [[152, 110, 49], [149, 106, 45], [244, 200, 75], [120, 111, 77], [195, 134, 46], [204, 158, 73], [143, 126, 72], [141, 126, 73], [247, 193, 77], [45, 145, 195], [251, 223, 108], [231, 163, 47], [231, 162, 45], [166, 134, 54], [248, 200, 94], [5, 3, 0], [217, 151, 79], [11, 7, 2], [213, 168, 64], [136, 119, 70], [245, 193, 79], [247, 200, 81], [247, 202, 82], [251, 228, 121], [250, 219, 99], [143, 125, 58], [247, 201, 64], [240, 194, 77], [215, 149, 41], [143, 101, 21], [207, 144, 50], [183, 140, 73], [253, 238, 83], [81, 70, 36], [141, 113, 41], [92, 73, 29], [60, 13, 45], [36, 33, 55], [81, 59, 118], [10, 5, 13], [9, 4, 12], [201, 78, 22], [231, 174, 71], [2, 2, 2], [134, 103, 67], [84, 72, 62], [23, 9, 5], [247, 141, 33], [66, 37, 14], [62, 32, 22], [203, 62, 35], [91, 69, 61], [3, 2, 0], [179, 44, 32], [226, 207, 184], [235, 47, 32], [196, 84, 46], [86, 37, 32], [89, 29, 29], [229, 54, 107], [61, 22, 22], [230, 44, 32], [79, 40, 40], [240, 130, 128], [234, 183, 196], [208, 112, 105], [231, 190, 199], [246, 171, 163], [99, 64, 73], [89, 61, 44], [102, 132, 102], [107, 116, 37], [69, 75, 31], [92, 112, 26], [135, 198, 84], [38, 54, 42], [85, 91, 44], [41, 54, 25], [89, 130, 12], [100, 151, 6], [42, 63, 16], [41, 60, 24], [45, 60, 20], [102, 175, 65], [31, 43, 15], [0, 2, 0], [49, 97, 53], [148, 189, 123], [75, 105, 36], [53, 55, 8], [120, 176, 49], [63, 170, 84], [187, 205, 94], [86, 143, 45], [61, 65, 67], [41, 84, 92], [43, 183, 222], [110, 201, 241], [232, 248, 254], [34, 39, 41], [122, 158, 175], [53, 124, 202], [86, 123, 198], [174, 213, 239], [42, 80, 128], [60, 93, 105], [178, 184, 196], [85, 83, 80], [221, 208, 181], [232, 244, 251], [91, 93, 96], [45, 44, 42], [117, 114, 110], [91, 91, 91], [197, 170, 135], [133, 110, 122], [243, 238, 238], [5, 4, 4], [2, 2, 2], [186, 187, 188], [180, 180, 180], [121, 86, 58], [230, 212, 196], [126, 94, 62], [221, 174, 125], [119, 87, 59], [224, 177, 122], [169, 110, 65], [119, 64, 31], [145, 100, 55], [4, 4, 5], [104, 74, 52], [11, 10, 10], [199, 184, 158], [10, 9, 7], [60, 59, 60], [48, 53, 58], [35, 34, 37], [66, 64, 75], [81, 81, 82], [103, 99, 96], [66, 66, 66], [77, 80, 88], [35, 35, 35], [77, 82, 89], [260, 260, 260]]
            self.lyodetytyt_varit = {}
                           
                
    def suorita(self) -> Image.Image:
        with Image.open(self.kuva) as analysoitava_kuva:
            leveys, korkeus = analysoitava_kuva.size

            while self.pinta_ala(leveys, korkeus) < 2081281:
                leveys, korkeus = floor(leveys/2), floor(korkeus/2)

            if analysoitava_kuva.mode != "RGB":
                analysoitava_kuva=analysoitava_kuva.convert("RGB")

            analysoitava_kuva = np.array(analysoitava_kuva)       #laskee pikselin väri arvot yhteen
            y_uusi_kuva, x_uusi_kuva = 0,0
            valittu_pikseli = [260,260,260]
            with Image.new("RGBA", (korkeus*25, leveys*25), (0,0,0,0)) as uusi_kuva:
                for vaaka_rivi in tqdm(analysoitava_kuva):
                    for pikseli in vaaka_rivi:

                        pikseli = list(pikseli)

                        if sum(pikseli) == 0:
                            x_uusi_kuva += 25

                        else:
                            if str(pikseli) in self.lyodetytyt_varit:
                                valittu_pikseli = self.lyodetytyt_varit[str(pikseli)]

                            else:
                                for emoiji_vari in self.varit:
                                    if valittu_pikseli[0] > emoiji_vari[0]-pikseli[0] >= 0 and valittu_pikseli[1] > emoiji_vari[1]-pikseli[1] >= 0  and valittu_pikseli[2] > emoiji_vari[2]-pikseli[2] >= 0:
                                        valittu_pikseli = emoiji_vari
                                        self.lyodetytyt_varit[str(pikseli)] = emoiji_vari

                            numero =self.varit.index(valittu_pikseli)
                            try:
                                with Image.open(path.join(self.polku,"emoijit",f"emoiji_{numero}.png")) as kopioitava_kuva:
                                    uusi_kuva.paste(kopioitava_kuva, (x_uusi_kuva,y_uusi_kuva))
                            
                            except FileNotFoundError:
                                print(f"kuvaa emoiji_{numero}.png ei ole kansiossa emoiji_kuvat")
                                break
                                
                            x_uusi_kuva += 25

                    y_uusi_kuva += 25
                    x_uusi_kuva = 0

                    
                return uusi_kuva

    def pinta_ala(self, leveys: int, korkeus: int) -> int:
        return leveys*korkeus*625         
    
    def __pyorista(self, n: float | int, tarkkuus: int = 0) -> int:
        "tarkkuus kertoo kuinka monen desimaalin tarkuuteen pyoristää"
        tarkkuus += 1
        _, b = modf(n)
        if b >= float(f"0"*tarkkuus+".5"):
            return ceil(n)
        else:
            return floor(n)
                

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