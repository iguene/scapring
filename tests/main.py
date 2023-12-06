import gsheet  #Librairie pour Google Sheet -> FIchier gsheet.py
from instabot import Bot
import time
import random
from check_proxies import check_proxy
import os
import datetime
import decoration
from colorama import Fore, Back, Style
import config

account_info = config.get_config()
username = account_info[0]
password = account_info[1]

if (os.path.exists(f"config/{username}_uuid_and_cookie.json")):
    os.remove(f"config/{username}_uuid_and_cookie.json")

print(decoration.logo)
print("\n*Informations:*")
print("Utilisateur à connecter: ", username)
print("\n*Légende:* ")
print(Fore.RED, "Consomme BEAUCOUP de requêtes (temps d'éxecution du code long)")
print(Fore.YELLOW, "Consommation MOYENNE.")
print(Fore.GREEN, "Consomme PEU de requêtes. (rapide)", Fore.WHITE)
personne_cible = str(input('\nEntrez une personne cible -> '))

list_followers = False

if (os.path.exists(f"data/{personne_cible}/followers.txt") and os.path.exists(f"data/{personne_cible}/following.txt")):
    date_mod = str(datetime.datetime.fromtimestamp(os.stat(f"data/{personne_cible}/followers.txt").st_mtime))
    date_modification = (date_mod[0:10], date_mod[11:19])
    value = input(f"La liste des followers a été trouvé, elle date du {date_modification[0]} à {date_modification[1]}, {Fore.RED}voulez-vous RE-lister les followers ? {Fore.WHITE}(oui, non): ")
    if (value.startswith("oui")):
        list_followers = True
else:
    with open(f"data/{personne_cible}/followers.txt", "w") as f:
        f.write("FICHIER VIDE !")
    with open(f"data/{personne_cible}/following.txt", "w") as f:
        f.write("FICHIER VIDE !")

print("[INFO] Get valid proxies...")
with open("proxies/valid_proxies.txt", "r") as f:
    proxies = f.read().split('\n')
print("[INFO] Proxies got...")

bot = Bot()

print("[INFO] Login...")
bot.login(username=username, password=password, ask_for_code=True)

print("CONNEXION Effectuée !")

if (list_followers):
    followers = bot.get_user_followers(personne_cible)
    following = bot.get_user_following(personne_cible)

    with open(f"data/{personne_cible}/followers.txt", "w") as file:
        for f in followers:
            file.write(f"{f}\n")
    print(f"[INFO] followers saved in data/{personne_cible}/followers.txt")
    with open(f"data/{personne_cible}/following.txt", "w") as file:
        for f in following:
            file.write(f"{f}\n")
    print(f"[INFO] following saved in data/{personne_cible}/following.txt")
else:
    with open(f"data/{personne_cible}/followers.txt", "r") as file:
        followers = file.read().split("\n")
    print("[INFO] Liste des Followers récupérée.")
    with open(f"data/{personne_cible}/following.txt", "r") as file:
        following = file.read().split("\n")
    print("[INFO] Liste des Abonnements récupérée.")

nb_followers = len(followers)

save_in_sheet = input(f"{Fore.YELLOW}Sauvegarder la liste des Followers dans le Google Sheet? {Fore.WHITE}(oui, non): ")

if (save_in_sheet.startswith("oui")):
    gsheet.clear_sheet()
    gsheet.insert_lines([["ID", "USERNAME", "YOU_FOLLOW"]], 1)
    i = 2
    for f in followers:
        if bot.check_not_bot(f):
            you_follow = False
            f_name = bot.get_username_from_user_id(f)
            if f in following:
                you_follow = True
            gsheet.insert_lines([[f, f_name, you_follow]], i)
            i += 1
            time.sleep(random.randint(2, 4))
        else:
            print(f"[INFO] SKIP {f} -> Bot detection")

def follow_users(userlist):
    for f in userlist:
        bot.follow(f, True)

follow_back_users = input(f"{Fore.RED}Suivre en retour tous les followers non suivi {Fore.WHITE}(à partir du compte @{username}){Fore.RED} sur le GoogleSheet? {Fore.WHITE}(oui, non): ")

if (follow_back_users.startswith("oui")):
    print("[INFO] FOLLOW ALL users...")
    accounts = gsheet.get_lines()
    line = 1
    for user in accounts:
        print(user)
        if (user[2] == "FALSE" or user[2] == "FAUX"):
            print(f'FOLLOW {user}') # FOLLOW USER
            bot.follow(user[0], True)
            gsheet.update_cells(line, 3, 'VRAI')
            print("[INFO] Mise en pause (Pas plus de 14 abonnements par heure afin d'éviter les conflits avec Instagram...)")
            time.sleep(60 * 60 / 14)
        line += 1

find_specific_users = input(f"{Fore.RED}Recherche de followers par mots clés pour ensuite les suivre en retour (BETA)? {Fore.WHITE}(oui, non): ")
if (find_specific_users.startswith("oui")):
    keywords = input("Entrez des mots clés séparés par une virgule (ex: droit,justice,avocat)")
    keywords_list = keywords.split(',')

bot.logout()
print("BYE")
