from Weather import Accuweather as Accu
from CombineImage import CombineImage
import time

today = time.strftime("%a, %d-%b") 
token = "XiiGZhD2SDOxEKo7eZFlviOgYNTaeZ4P"

bg_path = "assests/img/bg.png"
fg_path = "assests/img/fg.png"

weather = Accu(token, 224034, lang="ar")
Image = CombineImage(
    weather.forecasts[0]["day"]["icon"],
    weather.forecasts[0]["night"]["icon"],
    weather.forecasts[0]["day"]["temp"],
    weather.forecasts[0]["night"]["temp"],
    "lol",
    "lol",
    bg_path,
    fg_path
    )

print(weather.forecasts[0])
#weather.print()

