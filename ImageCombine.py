# PILLOW dependencies
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# For fixing arabic text in Windows
from bidi.algorithm import get_display
import arabic_reshaper
# For values to be displayed (NOT necessary)
from Weather import Accuweather as Acc
# To get day date as a number or a text
import datetime,time
# To check OS
import platform

mode = "RGBA"


def textBox(text, width, align="right", fix=True):
    # This function does the following:
    #   *Add extra spaces in original string for left/center/right alignment
    #   *Add extra newlines ("\n") to write text on a box instead of a single line, width represents the width of the box

    # If no align is needed, return
    if align == "none":
        return text
    # Delete arabic decorations on the first call only
    if fix:
        text = text.translate({i: None for i in range(1611, 1649)})
    # Base case
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

    i = 0
    last_space = 0
    while i <= width:
        # Find the index of last space in the width slice
        if text[i] == " ":
            last_space = i
        i += 1

    # Return the string depending on alignment
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
        # Save background, foreground and weather data for later use
        self.bg_path = bg_path
        self.fg_path = "assests/img/fg.png"
        self.weather = weather
        # set up backround and convert to correct mode
        self.img = Image.open(bg_path).convert(mode)

        # Draw contents over background
        self.drawContents()

    # drawItemAt is a simple wrapper around PILLOW.aplhacomposite
    # Description:
    #   xy: tuple (x,y) that dictates where to draw some item on the x,y plane
    #   path_to_item: string that represents where the path of the item to be draw is on the system
    #   size(optional): tuple(width,height) that allows for resizing an Image to preffered size before drawing
    def drawItemAt(self, xy, path_to_item, size=tuple()):
        new_img = Image.open(path_to_item).convert(mode)
        if not size == ():
            new_img = new_img.resize(size)
        self.img.alpha_composite(new_img, xy, (0, 0))
    
    # drawTextAt simplifies text drawal on images
    # xy: tuple (x,y) that dictates where to draw some text on the x,y plane
    # text: string to be drawn/rendered
    # font(optional): string specifiy font name. Note: font has to be in assests/fonts
    # size(optional): int size of text to be drawn/rendered in px
    # color(optional): specify color of text to be drawn. Note: (r,g,b) values can be used
    # align(optional): string alignment of text to be drawn/rendered
    # box_width(optional): int area around text to be drawn
    def drawTextAt(self, xy, text, font="Changa", size=36, color="black", isArabic=False, align="none", box_width=11):
        text = textBox(text, box_width, align)
        path_to_font = "assests/fonts/%s.ttf" % (font)
        font = ImageFont.truetype(path_to_font, size)
        draw = ImageDraw.Draw(self.img)
        # Rendering on some systems may cause text to get jumpled up, this fixes it
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

        # Draw forground
        self.drawItemAt((237, 23), self.fg_path)

        # Day stuff
        self.drawItemAt((808, 202), "assests/img/icons/%s.png" % (day_icon))
        self.drawTextAt((1070, 315), day_text, color="white",
                        isArabic=True, font="monoBold", align="right", size=18)
        self.drawTextAt((1081, 204), day_temp, size=100,
                        color="red", font="Myriad")

        # Night stuff
        self.drawItemAt((316, 202), "assests/img/icons/%s.png" % (night_icon))
        self.drawTextAt((590, 315), night_text, color="white",
                        isArabic=True, font="monoBold", align="right", size=18)
        self.drawTextAt((601, 204), night_temp, size=100,
                        color="blue", font="Myriad")

        # Todays' date text (English)
        today = time.strftime("%A, %d/%b")
        self.drawTextAt((657,500),today,font="Myriad",color="white")
        
        # box_cords[i] is a boxes' top left cords
        box_cords = [(284, 674), (336, 689), (311, 752),
                     (387, 875), (333, 875)]

        # Drawing weekbox,dayinbox,iconinbox,high,low
        for i in range(1, 5):
            # weekbox
            self.drawItemAt(box_cords[0], "assests/img/weekbox.png")
            # dayinbox
            self.drawTextAt(
                box_cords[1], self.weather.forecasts[i]["weekday"], size=24, isArabic=True, color="white")
            # iconinbox
            self.drawItemAt(box_cords[2], "assests/img/icons/{}.png".format
                            (self.weather.forecasts[i]["day"]["icon"]), size=(115, 115))
            # high
            self.drawTextAt(box_cords[3], self.weather.forecasts[i]["day"]
                            ["temp"], color="red", font="Myriad", size=40)
            # low
            self.drawTextAt(box_cords[4], self.weather.forecasts[i]["night"]["temp"], color=(
                0, 0, 255), font="Myriad", size=40)
            # Moving to the next box cords by adding 254 to x cord
            # because each weekbox is 254px away from the other
            for j in range(len(box_cords)):
                box_cords[j] = (box_cords[j][0]+254, box_cords[j][1])

    def show(self):
        self.img.show()

    def save(self, path):
        self.img.save(path)
