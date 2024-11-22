import tkinter as tk
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import webbrowser
import re

url = "https://www.tameteo.com/meteo_Guelma-Afrique-Algerie-Provincia+de+Annaba--1-171437.html"

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def verifier(x):
    if x:
        return x.text.strip()
    return None

response = requests.get(url, headers=Headers)
response.encoding = response.apparent_encoding


if response.status_code == 200:
    texte = response.text
    f = open("metéo_code_source", "w", encoding="utf-8")
    f.write(texte)
    f.close()

    soup = BeautifulSoup(texte, "html5lib")

    jour = verifier(soup.find("span", class_="subtitle-m"))
    print(jour)
    remarque = verifier(soup.find("span", class_="descripcion"))
    print(remarque)
    direction_vents = verifier(soup.find("span", class_="velocidad veloc-day"))
    print(direction_vents)
    temperature_actuelle = verifier(soup.find("span", class_="dato-temperatura changeUnitT"))
    print(temperature_actuelle)
    temperature_ressentie = verifier(soup.find("span", class_="sensacion changeUnitT"))
    print(temperature_ressentie)
    temperature_ressentie2 = re.sub(r"[a-zA-Z]", "", temperature_ressentie)
    humidité = verifier(soup.find("span", class_="txt-strng probabilidad center"))
    print(humidité)
    quantité_pluie = verifier(soup.find("span", class_="changeUnitR"))
    print(quantité_pluie)
    temp_maximum = verifier(soup.find("span", class_="max changeUnitT"))
    print(temp_maximum)
    temp_minimum = verifier(soup.find("span", class_="min changeUnitT"))
    print(temp_minimum)
    heure = verifier(soup.find("span", class_="hour"))
    print(heure)

    dates = soup.find_all("span", class_="col", attrs="")

    s = 1
    for date in dates:
        date = date.text
        if s == 7:
            e1 = date
            print(e1)
        elif s == 10:
             e2 = date
             print(e2)
        elif s == 12:
             e3 = date
             print(e3)
        elif s == 14:
             e4 = date
             print(e4)
        elif s == 16:
             e5 = date
             print(e5)
        elif s == 18:
             e6 = date
             print(e6)
        elif s == 70:   
             break
        s += 1
    e1V2 = re.sub(r"\d+% \d+\.?\d*mm", "", e1)
    print(e1V2)
    prochains_jours = [e2, e3, e4, e5, e6]

    print("")

    fenetre = tk.Tk()
    fenetre.title("meteo python")
    fenetre.geometry("800x675")

    canvas = tk.Canvas(width=800, height=675, bg="silver")
    canvas.pack(side="bottom", padx=5, pady=5)

    image_path = r"C:\Users\Anis Djerrab\Downloads\ff.jpg"
    image = Image.open(image_path)
    image = image.resize((785, 125))
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(395, 50, image=tk_image)
    canvas.image = tk_image
    textes = [heure, jour, remarque, direction_vents, temperature_actuelle, temperature_ressentie2, humidité, quantité_pluie, temp_maximum, temp_minimum]
    textess = ["heure :", "jour :", "remarque : ", "vents : ", "temperature actuelle :", "temperature ressentie : ", "humidité : ", "quantité pluie : ", "temperature maximum : ", "temperature minimum :"]
    x = 30
    for o, i in zip(textess, textes):
            canvas.create_rectangle(10, x + 100, 350, x + 150)
            canvas.create_text(125, x+125, text=o, font=("arial", 15), fill="darkblue")
            canvas.create_text(275, x+125, text=i, font=("arial", 15), fill="darkred")
            x += 50
    x = 10

    p = prochains_jours[0]
    e1V2 = e1V2.replace("mm", "mm\n").replace("demain", "Demain : ").replace("      ", "   ")
    canvas.create_rectangle(370, 130, 760, 230)
    canvas.create_text(560, 175, text=f"""{e1V2 }""", font=("arial", 20), fill="darkgreen")
    for i in prochains_jours:
         canvas.create_rectangle(370, x+270, 760, x+320)
         canvas.create_text(560, x+295, text=i, font=("arial", 14), fill="darkblue")
         x += 50

    def site():
         webbrowser.open(url)
    def sortir():
         fenetre.destroy()
    button = tk.Button(fenetre, text="Source", font=("arial", 15), fg="darkblue", bg="lightblue", command=site)
    canvas.create_window(450, 580, window=button)
    button = tk.Button(fenetre, text="Quitter", font=("arial", 15), fg="darkred", bg="lightcoral", command=sortir)
    canvas.create_window(600, 580, window=button)
    fenetre.mainloop()


    




