from PIL import Image, ImageDraw, ImageFont, ImageFilter     #PILLOW dependencies
from bidi.algorithm import get_display          #for fixing arabic text
import arabic_reshaper                          #for fixing arabic text
from Weather import Accuweather as Acc          #for values to be displayed
import datetime
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

    def drawItemAt(self,xy,path_to_item,size = -1):
        new_img = Image.open(path_to_item).convert(mode)
        if not size == -1:
            new_img = new_img.resize(size)
        self.Image.alpha_composite(new_img,xy,(0,0))

    def drawTextAt(self,xy,text,font = "Arial",size = 36,color="black",stroke = 0,isArabic=False):
            path_to_font = "assests/fonts/%s.ttf"%(font)
            font = ImageFont.truetype(path_to_font,size)
            draw = ImageDraw.Draw(self.Image)

            #renderin on some systems may cause text to get jumpled up, this fixes it
            if isArabic:
                r = arabic_reshaper.reshape(text)
                text = get_display(r)
            
            draw.text(xy,text,stroke_width=stroke,font=font,fill=color)
            
    def drawContents(self):
        #Extract first day data from weather object
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
        self.drawTextAt((1081,315),day_text,color="white",isArabic=True)
        self.drawTextAt((1081,204),day_temp,size=100,stroke=1,color="red",font = "Myriad")

        #night stuff
        self.drawItemAt((316,202),"assests/img/icons/%s.png"%(night_icon))
        self.drawTextAt((590,315),night_text,color="white",isArabic=True)
        self.drawTextAt((592,204),night_temp,size = 100,stroke=1,color="blue",font = "Myriad")
        
        #dayinbox,weekbox,iconinbox,highlow
        week_cords = [
            [(336,696),(283,673),(311,752),(333,875),(393,875)],
            [(594,696),(538,673),(569,752),(591,875),(651,875)],
            [(842,696),(791,673),(817,752),(839,875),(899,875)],
            [(1103,696),(1045,673),(1078,752),(1100,875),(1160,875)]
        ]
        #Draw boxes,temps,icons
        for i in range(0,4):
            self.drawItemAt(week_cords[i][1],"assests/img/weekbox.png")
            self.drawItemAt(week_cords[i][2],"assests/img/icons/%s.png"%(self.weather.forecasts[i+1]["day"]["icon"]),size =(115,115))
            self.drawTextAt(week_cords[i][3],self.weather.forecasts[i+1]["day"]["temp"]+"°",color="red",font="Myriad",size = 40,stroke=1) #draw high
            self.drawTextAt(week_cords[i][4],self.weather.forecasts[i+1]["night"]["temp"]+"°",color=(0,0,139),font = "Myriad",size = 40,stroke = 1) #draw night
        for i in range(0,4):
            self.drawTextAt(week_cords[i][0],self.weather.forecasts[i]["weekday"],size = 24,isArabic=True)      

    def show(self):
        self.Image.show()

