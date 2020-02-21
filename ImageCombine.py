from PIL import Image, ImageDraw, ImageFont, ImageFilter     #PILLOW dependencies
from bidi.algorithm import get_display          #for fixing arabic text
import arabic_reshaper                          #for fixing arabic text
from Weather import Accuweather as Acc          #for values to be displayed

import requests
import json

mode = "RGBA"

class ImageCombine:
    def __init__(self,weather,bg_path,fg_path):
        #save background, foreground and weather data for later use
        self.bg_path = bg_path
        self.fg_path = fg_path
        self.weather = weather
        #set up backround and convert to correct mode
        self.Image = Image.open(bg_path).convert(mode)

        #draw contents over background
        self.drawContents()

    def drawItemAt(self,xy,path_to_item):
        self.Image.alpha_composite(Image.open(path_to_item).convert(mode),xy,(0,0))

    def drawTextAt(self,xy,text,font = "MyriadArabic",size = 36,color="black",stroke = 0,isArabic=False):
            path_to_font = "assests/fonts/%s.ttf"%(font)
            font = ImageFont.truetype(path_to_font,size)
            draw = ImageDraw.Draw(self.Image)

            #renderin on some systems may cause text to get jumpled up, this fixes it
            if isArabic:
                r = arabic_reshaper.reshape(text)
                text = get_display(r)
            
            draw.text(xy,text,stroke_width=stroke,font=font,fill=color)
            
    def drawContents(self):
        #Extract data from weather object
        day_temp = self.weather.forecasts[0]["day"]["temp"]+"°"
        day_icon = self.weather.forecasts[0]["day"]["icon"]
        day_text = self.weather.forecasts[0]["day"]["text"]
        
        night_temp = self.weather.forecasts[0]["night"]["temp"]+"°"
        night_icon = self.weather.forecasts[0]["night"]["icon"]
        night_text = self.weather.forecasts[0]["night"]["text"]
        
        #draw forground
        self.drawItemAt((237,23),self.fg_path)

        #day stuff
        self.drawItemAt((808,202),"assests/img/icons/%s.png"%(day_icon))
        self.drawTextAt((1081,315),day_text,color="white",isArabic=True,font="Changa")
        self.drawTextAt((1081,204),day_temp,size=100,stroke=1,color="red")

        #night stuff
        self.drawItemAt((316,202),"assests/img/icons/%s.png"%(night_icon))
        self.drawTextAt((590,315),night_text,color="white",isArabic=True,font = "Changa")
        self.drawTextAt((592,204),night_temp,size = 100,stroke=1,color="blue")
        
        #dayinbox,weekbox,iconinbox
        week_cords = [
            [(336+13,691),(283,673),(311,752)],
            [(594+13,691),(538,673),(569,752)],
            [(842+13,691),(791,673),(817,752)],
            [(1103+13,691),(1045,673),(1078,752)]
        ]
        #WIP
        for i in range(0,4):

            self.drawTextAt(week_cords[i][0],"lol",size = 60)
            self.drawItemAt(week_cords[i][1],"assests/img/weekbox.png")
            self.drawItemAt(week_cords[i][2],"assests/img/icons/1.png")
            

    def show(self):
        self.Image.show()

