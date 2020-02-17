from PIL import Image, ImageDraw, ImageFont

""""
    weather_icon_day : (x,y) cordinates for day weather discription icon
    weather_temp_day : int() day tempreture in celcius
    weather_desc_day : (x,y) cordinates for short day weather discription 

    weather_icon_night : (x,y) cordinates for night weather discription
    weather_temp_night : int() night tempreture in celcius
    weather_desc_night : (x,y) cordinates for short night weather discription 

    current_date : (x,y) cordinates for current date
"""
cords = {
    "weather_icon_day":(),
    "weather_desc_day":"",
    "weather_temp_day":int(),

    "weather_icon_night":(),
    "weather_temp_night":int(),
    "weather_desc_night":"",

    "current_date":()
}
mode = "RGBA"
class CombineImage:
    def __init__(self,weather_icon_day,weather_icon_night,weather_temp_day,weather_temp_night,weather_desc_day,weather_desc_night,background_path,foreground_path):

        self.weather_icon_day = weather_icon_day
        self.weather_icon_night = weather_icon_night
        self.temp_day = weather_temp_day
        self.temp_night = weather_temp_night
        self.weather_desc_day = weather_desc_day
        self.weather_desc_night = weather_desc_night 
        self.bg = Image.open(background_path).convert(mode)
        self.fg = Image.open(foreground_path).convert(mode)
        
        self.combine()

    def combine(self):
            self.bg.alpha_composite(self.fg,(0,0),(0,0))
            self.bg.show()