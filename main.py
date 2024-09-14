#build in
import time, os
from pathlib import Path
from threading import Thread

# other
from PIL import Image
import numpy as np
from tqdm import tqdm

class ImageEditor:
    def __init__(self, image_path: str) -> None:
            self.image_path = Path(image_path)

            if not Path(image_path).exists():
                raise FileNotFoundError(f"kuvaa {image_path} ei ole olemassa")

            self.current_directory = Path().cwd()

    def convert_pixles_to_emoji(self) -> Image.Image | str:
        "muuntaa kuvan pikselit emoijiksi"
        cached_colors = {}

        try:
            with Image.open(self.image_path) as analyzed_image:
                width, height = analyzed_image.size

                if analyzed_image.mode != "RGB":
                    analyzed_image = analyzed_image.convert("RGB")

                analyzed_image = np.array(analyzed_image)

                new_image_y, new_image_x = 0, 0

                with Image.new("RGBA", (width * 25, height * 25), (0,0,0,0)) as new_image:
                    for row in tqdm(analyzed_image):
                        for pixel in row:

                            if int(np.sum(pixel)) == 0:
                                new_image_x += 25

                            else:
                                n, cached_colors = self.select_emoijy(cached_colors, pixel)

                                try:
                                    with Image.open(os.path.join(self.current_directory,"emoijit",f"emoiji_{n}.png")) as copied_image:
                                        new_image.paste(copied_image, (new_image_x, new_image_y))

                                except FileNotFoundError:
                                    return f"kuvaa emoiji_{n}.png ei ole kansiossa emoiji_kuvat"

                                new_image_x += 25

                        new_image_y += 25
                        new_image_x = 0

                    return new_image

        except MemoryError:
            return "Virhe, muunettava kuvan koko on liian suuri"

    def select_emoijy(self, cached_colors, pixel):
        colors = [[152, 110, 49], [149, 106, 45], [244, 200, 75], [120, 111, 77], [195, 134, 46], [204, 158, 73], [143, 126, 72], [141, 126, 73], [247, 193, 77], [45, 145, 195], [251, 223, 108], [231, 163, 47], [231, 162, 45], [166, 134, 54], [248, 200, 94], [5, 3, 0], [217, 151, 79], [11, 7, 2], [213, 168, 64], [136, 119, 70], [245, 193, 79], [247, 200, 81], [247, 202, 82], [251, 228, 121], [250, 219, 99], [143, 125, 58], [247, 201, 64], [240, 194, 77], [215, 149, 41], [143, 101, 21], [207, 144, 50], [183, 140, 73], [253, 238, 83], [81, 70, 36], [141, 113, 41], [92, 73, 29], [60, 13, 45], [36, 33, 55], [81, 59, 118], [10, 5, 13], [9, 4, 12], [201, 78, 22], [231, 174, 71], [2, 2, 2], [134, 103, 67], [84, 72, 62], [23, 9, 5], [247, 141, 33], [66, 37, 14], [62, 32, 22], [203, 62, 35], [91, 69, 61], [3, 2, 0], [179, 44, 32], [226, 207, 184], [235, 47, 32], [196, 84, 46], [86, 37, 32], [89, 29, 29], [229, 54, 107], [61, 22, 22], [230, 44, 32], [79, 40, 40], [240, 130, 128], [234, 183, 196], [208, 112, 105], [231, 190, 199], [246, 171, 163], [99, 64, 73], [89, 61, 44], [102, 132, 102], [107, 116, 37], [69, 75, 31], [92, 112, 26], [135, 198, 84], [38, 54, 42], [85, 91, 44], [41, 54, 25], [89, 130, 12], [100, 151, 6], [42, 63, 16], [41, 60, 24], [45, 60, 20], [102, 175, 65], [31, 43, 15], [0, 2, 0], [49, 97, 53], [148, 189, 123], [75, 105, 36], [53, 55, 8], [120, 176, 49], [63, 170, 84], [187, 205, 94], [86, 143, 45], [61, 65, 67], [41, 84, 92], [43, 183, 222], [110, 201, 241], [232, 248, 254], [34, 39, 41], [122, 158, 175], [53, 124, 202], [86, 123, 198], [174, 213, 239], [42, 80, 128], [60, 93, 105], [178, 184, 196], [85, 83, 80], [221, 208, 181], [232, 244, 251], [91, 93, 96], [45, 44, 42], [117, 114, 110], [91, 91, 91], [197, 170, 135], [133, 110, 122], [243, 238, 238], [5, 4, 4], [2, 2, 2], [186, 187, 188], [180, 180, 180], [121, 86, 58], [230, 212, 196], [126, 94, 62], [221, 174, 125], [119, 87, 59], [224, 177, 122], [169, 110, 65], [119, 64, 31], [145, 100, 55], [4, 4, 5], [104, 74, 52], [11, 10, 10], [199, 184, 158], [10, 9, 7], [60, 59, 60], [48, 53, 58], [35, 34, 37], [66, 64, 75], [81, 81, 82], [103, 99, 96], [66, 66, 66], [77, 80, 88], [35, 35, 35], [77, 82, 89], [260, 260, 260]]

        if str(pixel) in cached_colors:
            selected_pixel = cached_colors[str(pixel)]
            n = colors.index(selected_pixel)

        else:
            test_colors = np.subtract(colors, pixel, dtype=np.int8)
            test_colors = np.fabs(test_colors)
            test_colors = np.sum(test_colors, axis=1)
            i = np.min(test_colors)
            n = int(np.where(test_colors == i)[0])

            cached_colors[str(pixel)] = colors[int(i)]

        return n, cached_colors

    def image_size(self) -> tuple[int, int]:
        "palauttaa kuvan koon"
        with Image.open(self.image_path) as image:
            return image.size

    def resize_image(self, width: int, height: int) -> Image.Image:
        "muuntaan kuvan koon"
        with Image.open(self.image_path) as image:
            return image.resize((width,height))

class Application:
    def __init__(self):
        pass

    def logo(self):
        print(" _____                       _     _   _         _  __                        ")
        print("| ____|  _ __ ___     ___   (_)   (_) (_)       | |/ /  _   _  __   __   __ _ ")
        print("|  _|   | '_ ` _ \   / _ \  | |   | | | |       | ' /  | | | | \ \ / /  / _` |")
        print("| |___  | | | | | | | (_) | | |   | | | |       | . \  | |_| |  \ V /  | (_| |")
        print("|_____| |_| |_| |_|  \___/  |_|  _/ | |_|       |_|\_\  \__,_|   \_/    \__,_|")
        print("                                |__/                                          ")

    def line(self, character: str, length: int, end="\n"):
        "tekee vivaan jostain merkistä"
        print(character * length, end=end)

    def box(self, text: str):
        """
        ympäröi tekstin laatikolla
        uuden rivin saa // \n
        rivin saa keskitettynä ympäröimällä sanan merkillä *\n
        """

        lines = text.split("//")

        #suurimman rivin määritys
        max_length = max(len(line) for line in lines)

        # tekstin keskitys
        for line in lines:
            if len(line) == 0:
                continue
            if line[0] == "*" and line[-1] == "*":
                n = lines.index(line)
                line = line[1:-1]
                line = line.center(max_length)
                lines[n] = line

            else:
                continue

        max_length += 2

        #laatiko tekeminen
        print("╔", end="")
        self.line("═", max_length, end="")
        print("╗")

        for line in lines:
            line = line + " "*(max_length-len(line))

            print(f"║ {line[:-2]} ║")

        print("╚", end="")
        self.line("═", max_length, end="")
        print("╝")

    def is_image_ok(self, file: str) -> bool:
        """testaa onko tiedosto sopiva kuva"""
        if file.endswith((".png", ".jpg", ".jpeg")):
            if file.startswith("emoiji"):
                return False
            else:
                return True

    def instructions(self):
        while True:
            print(" ")
            self.box("*Ohjeet*////Muuntaaksesi kuvan pikselit emojiksi kopio kaikki kuvat//kansioon ”muunnettavat kuvat”.Sen jälkeen valitse//päävalikosta ”Muuna kuva” ja ohjelma//muuntaa kuvan.////takaisin: t")
            user_choice = input("Valitse kohta: ")
            if user_choice.lower() == "t":
                break

    def image_converter(self):
        while True:
            current_path = Path().cwd()
            files = os.listdir(current_path.joinpath("muunnettavat kuvat"))

            valid_files = []
            for file in files:
                if self.is_image_ok(file):
                    valid_files.append(file)

            if len(valid_files) == 0:
                print("Muunnettavia kuvia ei ole")
                time.sleep(0.5)
                break

            files = "Tiedostot//"
            for file in valid_files:
                files = files + f"{valid_files.index(file)+1}.    {file}//"
            files = files[:-2]

            self.box(files)

            user_choice = input(f"Haluatko muuntaakuvan (k/e): ")

            if user_choice.lower() == "k":
                user_choice = int(input(f"Minkä kuvan haluat muntaa: "))

                try:
                    image = valid_files[user_choice-1]
                    converter = ImageEditor(os.path.join(current_path,"muunnettavat kuvat", image))
                    converted_image = converter.convert_pixes_to_emoji()

                    if isinstance(converted_image, Image.Image):
                        image, _ = image.rsplit(".",1)

                        converted_image.save(os.path.join(current_path,"muunnettavat kuvat",f"emoiji_{image}.png"))

                        print("Muunettu")
                        break

                    else:
                        print()
                        print()
                        print(converted_image, end="\r")
                        time.sleep(5)
                        print("                                                                   ")
                        break

                except FileNotFoundError:
                    print()
                    print("kuvia ei löytynyt", end="\r")
                    time.sleep(1)
                    print("                    ")
                    self.image_converter()

            elif user_choice.lower() == "e":
                break

    def main(self):
        self.logo()

        while True:
            print(" ")
            print(" ")

            self.box("*Pää valikko*//Muuna kuvan pikselit emoijiksi: m//Ohjeet: o//Poistu: p")
            user_choice = input("Valitse kohta: ")

            if user_choice == "o":
                self.instructions()

            elif user_choice.lower() == "m":
                print()
                self.image_converter()

            elif user_choice.lower() == "p":
                break

            else:
                pass

class Startup():
    def __init__(self) -> None:
        self.is_booting = True
        self.is_everything_ok = False
        self.error = ""
        self.current_directory = Path().cwd()

    def main(self):
        t_1 = Thread(target=self.processing)
        t_2 = Thread(target=self.check_everything)
        t_1.start()
        t_2.start()
        t_1.join()
        t_2.join()

        if self.is_everything_ok:
            app = Application()
            app.main()

        else:
            print(self.error)

    def check_everything(self):
        folder_error, is_folder_error = self.check_folders()
        emoji_image_error, is_emoji_error = self.check_emoji_images()

        self.is_booting = False

        if not is_emoji_error and not is_folder_error:
            self.is_everything_ok = True

        if is_folder_error:
            self.error += folder_error + "\n"

        if is_emoji_error and "emoijit" not in self.error:
            self.error += emoji_image_error + "\n"

    def processing(self):
        while self.is_booting:
            print("käynistyy   ", end="\r")
            time.sleep(0.2)
            print("käynistyy.  ", end="\r")
            time.sleep(0.2)
            print("käynistyy.. ", end="\r")
            time.sleep(0.2)
            print("käynistyy...", end="\r")
            time.sleep(0.2)

    def check_folders(self) -> tuple[str, bool]:
        folders = os.listdir(self.current_directory)

        error_message = ""

        if "muunnettavat kuvat" not in folders:
            error_message += "muunnettavat kuvat, "

        if "emoijit" not in folders:
            error_message += "emoijit, "

        if error_message == "":
            return "", False

        else:
            return f"Virhe, kansioita {error_message[:-2]} ei ole", True

    def check_emoji_images(self) -> bool:
        images = os.listdir(self.current_directory.joinpath("emoijit"))

        is_error = False

        error_message = "   "
        for i in range(146):
            if f"emoiji_{i}.png" not in images:
                error_message += f"emoiji_{i}.png, "
                is_error = True

        error_message = f"Virhe, Kuvia ei ole: {error_message[3:-2]} kansiossa emoijit"

        return error_message, is_error

if __name__ == "__main__":
    start = Startup()
    start.main()
