from PIL import Image, ImageDraw, ImageFont, ImageFilter  # PILLOW dependencies
from bidi.algorithm import get_display  # for fixing arabic text
import arabic_reshaper  # for fixing arabic text
from Weather import Accuweather as Acc  # for values to be displayed
import datetime  # to get today name
import platform  # to check OS

mode = "RGBA"


class ImageCombine:
    def __init__(self, weather, bg_path, fg_path):
        # save background, foreground and weather data for later use
        self.bg_path = bg_path
        self.fg_path = fg_path
        self.weather = weather
        # set up backround and convert to correct mode
        self.Image = Image.open(bg_path).convert(mode)

        # draw contents over background
        self.drawContents()

    def drawItemAt(self, xy, path_to_item, size=-1):
        new_img = Image.open(path_to_item).convert(mode)
        if not size == -1:
            new_img = new_img.resize(size)
        self.Image.alpha_composite(new_img, xy, (0, 0))

    def drawTextAt(self, xy, text, font="Changa", size=36, color="black", isArabic=False):
        path_to_font = "assests/fonts/%s.ttf" % (font)
        font = ImageFont.truetype(path_to_font, size)
        draw = ImageDraw.Draw(self.Image)
        # renderin on some systems may cause text to get jumpled up, this fixes it
        if isArabic and platform.system() == "Windows":
            print("Fixing arabic font....")
            r = arabic_reshaper.reshape(text)
            text = get_display(r)

        draw.text(xy, text, font=font, fill=color)

    def drawContents(self):
        # Extract first day data from weather object
        day_temp = self.weather.forecasts[0]["day"]["temp"]
        day_icon = self.weather.forecasts[0]["day"]["icon"]
        day_text = self.weather.forecasts[0]["day"]["text"]

        night_temp = self.weather.forecasts[0]["night"]["temp"]
        night_icon = self.weather.forecasts[0]["night"]["icon"]
        night_text = self.weather.forecasts[0]["night"]["text"]

        # draw forground
        self.drawItemAt((237, 23), self.fg_path)

        # day stuff
        self.drawItemAt((808, 202), "assests/img/icons/%s.png" % (day_icon))
        self.drawTextAt((1081, 315), day_text, color="white", isArabic=False)
        self.drawTextAt((1081, 204), day_temp, size=100,
                        color="red", font="Myriad")

        # night stuff
        self.drawItemAt((316, 202), "assests/img/icons/%s.png" % (night_icon))
        self.drawTextAt((590, 315), night_text, color="white", isArabic=False)
        self.drawTextAt((592, 204), night_temp, size=100,
                        color="blue", font="Myriad")
        # box_cords is the first box from the left cords
        box_cords = [(284, 674), (336, 674), (311, 752),
                     (387, 875), (333, 875)]
        # drawing dayinbox,weekboxes,iconinbox,high/low
        for i in range(1, 5):
            # 1 the box itself
            self.drawItemAt(box_cords[0], "assests/img/weekbox.png")
            # 2 weekday name
            self.drawTextAt(
                box_cords[1], self.weather.forecasts[i]["weekday"], size=24, isArabic=False)
            # 3 weekday Icon
            self.drawItemAt(box_cords[2], "assests/img/icons/%s.png" %
                            (self.weather.forecasts[i]["day"]["icon"]), size=(115, 115))
            # 4 weekday high temp
            self.drawTextAt(box_cords[3], self.weather.forecasts[i]["day"]
                            ["temp"], color="red", font="Myriad", size=40)
            # 5 weekday low temp
            self.drawTextAt(box_cords[4], self.weather.forecasts[i]["night"]["temp"], color=(
                0, 0, 139), font="Myriad", size=40)
            # moving to the next box cords by adding 254 to x-axis
            for j in range(len(box_cords)):
                box_cords[j] = (box_cords[j][0]+254, box_cords[j][1])

    def show(self):
        self.Image.show()
