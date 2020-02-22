from Weather import Accuweather as Accu
from ImageCombine import ImageCombine
import time
import pickle
import os

# Important constants

today = time.strftime("%a, %d-%b") # Todays date
token = "XiiGZhD2SDOxEKo7eZFlviOgYNTaeZ4P" # Accuweather API token
lang = "ar" # Language of the text responses the Accuweather API should give
location_id = 224034 # Accuweather provides each supported location with a location-id, to change location change this
bg_path = "assests/img/bg_nogov.png" # Path to background img
fg_path = "assests/img/fg.png"  # Path to foreground img

# This part exists mainly for testing purposes right now
# Save/Load pickle responses to avoid getting 401ed ;=;

load_pickle=  os.path.exists("./weather.pickle")
if load_pickle:
    print("WARNING: Using pickled weather")
    with open("./weather.pickle","rb") as f:
        weather= pickle.load(f)
else:
    weather = Accu(token, location_id, lang=lang)
    with open("./weather.pickle","wb") as f:
        pickle.dump(weather,f)
w = ImageCombine(weather, bg_path, fg_path)
w.show()

print(weather.forecasts)