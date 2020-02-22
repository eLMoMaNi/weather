from Weather import Accuweather as Accu
from ImageCombine import ImageCombine
import time
import pickle
import os

today = time.strftime("%a, %d-%b")
token = "XiiGZhD2SDOxEKo7eZFlviOgYNTaeZ4P"
bg_path = "assests/img/bg_nogov.png"
fg_path = "assests/img/fg.png"
load_pickle=True

if load_pickle:
    print("WARNING: Using Pickled Weather")
    weather=pickle.load(open("./weather.pickle","rb"))
else:
    weather = Accu(token, 224034, lang="ar")
    pickle.dump(weather,open("./weather.pickle","wb"))
w = ImageCombine(weather, bg_path, fg_path)
w.show()

print(weather.forecasts)
# weather.print()
