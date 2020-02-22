# PILLOW dependencies
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# for fixing arabic text in Windows
from bidi.algorithm import get_display
import arabic_reshaper
# for values to be displayed (NOT necessary)
from Weather import Accuweather as Acc
# to get day date as a number or a text
import datetime,time
# to check OS
import platform

mode = "RGBA"


def textBox(text, width, align="right", fix=True):
    ####
    # this function do :
    # 1: add extra spaces in original string for left/center/right alignment
    # 2: add extra newlines ("\n") to write text on a box instead of a single line, width represents the width of the box
    ####

    # if no align is needed, return @_@
    if align == "none":
        return text
    # delete arabic decorations on the first call only
    if fix:
        text = text.translate({i: None for i in range(1611, 1649)})
    # base case
    if len(text) <= width:
        if align == "right":
            return \
                text[0:len(text)] \
                + " "*(width-len(text)) + "\n"
        elif align == "center":
            return \
                " "*int((width-len(text))/2) \
                + text[0:len(text)] \
                + " "*int((width-len(text))/2) + "\n"
        elif align == "left":
            return \
                " "*(width-len(text)) + \
                text[0:len(text)] + "\n"
    ###
    i = 0
    last_space = 0
    while i <= width:
        # find the index of last space in the width slice
        if text[i] == " ":
            last_space = i
        i += 1

    # retutn the string depending on alingment
    if align == "right":
        return \
            text[0:last_space] \
            + " "*(width-last_space) + "\n" \
            + textBox(text[last_space+1:], width, align, False)
    elif align == "center":
        return \
            " "*int((width-last_space-1)/2) \
            + text[0:last_space] \
            + " "*int((width-last_space)/2) + "\n" \
            + textBox(text[last_space+1:], width, align, False)
    elif align == "left":
        return \
            " "*(width-last_space) + \
            text[0:last_space] + "\n"\
            + textBox(text[last_space+1:], width, align, False)


class ImageCombine:
    def __init__(self, weather, bg_path):
        # save background, foreground and weather data for later use
        self.bg_path = bg_path
        self.fg_path = "assests/img/fg.png"
        self.weather = weather
        # set up backround and convert to correct mode
        self.img = Image.open(bg_path).convert(mode)

        # draw contents over background
        self.drawContents()

    def drawItemAt(self, xy, path_to_item, size=-1):
        new_img = Image.open(path_to_item).convert(mode)
        if not size == -1:
            new_img = new_img.resize(size)
        self.img.alpha_composite(new_img, xy, (0, 0))

    def drawTextAt(self, xy, text, font="Changa", size=36, color="black", isArabic=False, align="none", box_width=11):
        text = textBox(text, box_width, align)
        path_to_font = "assests/fonts/%s.ttf" % (font)
        font = ImageFont.truetype(path_to_font, size)
        draw = ImageDraw.Draw(self.img)
        # renderin on some systems may cause text to get jumpled up, this fixes it
        if isArabic and platform.system() == "Windows":
            print("Fixing arabic font....")
            r = arabic_reshaper.reshape(text)
            text = textBox(get_display(r), box_width, align)

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
        self.drawTextAt((1070, 315), day_text, color="white",
                        isArabic=True, font="monoBold", align="right", size=18)
        self.drawTextAt((1081, 204), day_temp, size=100,
                        color="red", font="Myriad")

        # night stuff
        self.drawItemAt((316, 202), "assests/img/icons/%s.png" % (night_icon))
        self.drawTextAt((590, 315), night_text, color="white",
                        isArabic=True, font="monoBold", align="right", size=18)
        self.drawTextAt((601, 204), night_temp, size=100,
                        color="blue", font="Myriad")
        # today date text (English)
        today = time.strftime("%A, %d/%b")
        self.drawTextAt((657,500),today,font="Myriad",color="white")
        

        # box_cords is the first box from the left cords
        box_cords = [(284, 674), (336, 689), (311, 752),
                     (387, 875), (333, 875)]
        # drawing dayinbox,weekboxes,iconinbox,high/low
        for i in range(1, 5):
            # 1 the box itself
            self.drawItemAt(box_cords[0], "assests/img/weekbox.png")
            # 2 weekday name
            self.drawTextAt(
                box_cords[1], self.weather.forecasts[i]["weekday"], size=24, isArabic=True, color="white")
            # 3 weekday Icon
            self.drawItemAt(box_cords[2], "assests/img/icons/%s.png" %
                            (self.weather.forecasts[i]["day"]["icon"]), size=(115, 115))
            # 4 weekday high temp
            self.drawTextAt(box_cords[3], self.weather.forecasts[i]["day"]
                            ["temp"], color="red", font="Myriad", size=40)
            # 5 weekday low temp
            self.drawTextAt(box_cords[4], self.weather.forecasts[i]["night"]["temp"], color=(
                0, 0, 255), font="Myriad", size=40)
            # moving to the next box cords by adding 254 to x-axis
            for j in range(len(box_cords)):
                box_cords[j] = (box_cords[j][0]+254, box_cords[j][1])

    def show(self):
        self.img.show()

    def save(self, path):
        self.img.save(path)
