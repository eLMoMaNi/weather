from Weather import Accuweather as Accu
from ImageCombine import ImageCombine
import time
import pickle
import os

today = time.strftime("%a, %d-%b") 
token = "GetYourOwnTokenPlz" 
bg_path = "assests/img/bg.png"
fg_path = "assests/img/fg.png"
weather = ""
if not os.path.exists("pickledAccu.txt"):
    weather = Accu(token, 224034, lang="ar")
    with open("pickledAccu.txt","wb") as f:
        pickle.dump(weather,f)
else:
    with open("pickledAccu.txt","rb") as f:
        weather = pickle.load(f)
w = ImageCombine(weather,bg_path,fg_path)
w.toImage().show()


