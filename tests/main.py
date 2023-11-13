import gsheet #Librairie pour Google Sheet -> FIchier gsheet.py
from instabot import Bot
import time
import random
from check_proxies import check_proxy

username = "ibrahima.gnf@gmail.com"
password = "m5Mey5eydw"
personne_cible = "simulegal"

with open("proxies/valid_proxies.txt", "r") as f:
    proxies = f.read().split('\n')

bot = Bot()

bot.login(username=username, password=password)

print("CONNEXION Effectuée !")

followers = bot.get_user_followers(personne_cible)

with open("data/followers.txt", "w") as file:
    for f in followers:
        file.write(f"{f}\n")

nb_followers = len(followers)

print("[INFO] followers saved in data/followers.txt")
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
