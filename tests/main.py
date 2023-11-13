import gsheet #Librairie pour Google Sheet -> FIchier gsheet.py
from instabot import Bot
import time
import random
from check_proxies import check_proxy
import os

username = "ibrahima.gnf@gmail.com"
password = "m5Mey5eydw"

os.remove(f"config/{username}_uuid_and_cookie.json")

personne_cible = "simulegal"


list_followers = False

if (os.path.exists(f"data/{personne_cible}.txt")):
    value = input("La liste des followers a été trouvé, voulez-vous RE-lister les followers (cela peut-être long dû au délai entre les requêtes) ? (oui, non): ")
    if (value.startswith("oui")):
        list_followers = True
else:
    with open(f"data/{personne_cible}.txt", "w") as f:
        f.write("FICHIER VIDE !")

print("[INFO] Get valid proxies...")
with open("proxies/valid_proxies.txt", "r") as f:
    proxies = f.read().split('\n')
print("[INFO] Proxies got...")

bot = Bot()

print("[INFO] Login...")
bot.login(username=username, password=password)

print("CONNEXION Effectuée !")

if (list_followers):
    followers = bot.get_user_followers(personne_cible)

    with open(f"data/{personne_cible}.txt", "w") as file:
        for f in followers:
            file.write(f"{f}\n")
    print(f"[INFO] followers saved in data/{personne_cible}.txt")
else:
    followers = []
    with open(f"data/{personne_cible}.txt", "r") as file:
        followers.append(file.read().split("\n"))
    print("[INFO] followers got in file.")


nb_followers = len(followers)


save_in_sheet = input("Sauvegarder dans Google Sheet ? (oui, non): ")

if (save_in_sheet.startswith("oui")):
    gsheet.insert_lines([["ID", "USERNAME"]], 1)

    i = 2
    for f in followers:
        if bot.check_not_bot(f):
            f_name = bot.get_username_from_user_id(f)
            gsheet.insert_lines([[f, f_name]], i)
            i += 1
            time.sleep(random.randint(0, 4))
        else:
            print(f"[INFO] SKIP {f} -> Bot detection")



bot.logout()
print("BYE")
