import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])

from instabot import Bot
import time
import random
from bs4 import BeautifulSoup
import gsheet
from gsheet import *

from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import Flow


username = "email"
password = "XXXXXXXX"
personne_cible = "idpersonne cible"

bot = Bot()

def login():
    bot.login(username=username, password=password)

def logout():
    bot.logout()

def follow_user(username):
    bot.follow(username)
    print(f"Abonnement à {username} réussi.")


def unfollow_user(username):
    bot.unfollow(username)
    print(f"Désabonnement à {username} réussi")

def liste_followers_account(username):
    return bot.get_user_followers(username)


def liste_username_followers(username, followers_dict):
    #lst,lst_followers=[],[]
    #lst=liste_followers_account(username)
    #time.sleep(random.randint(5,15))
    followers= liste_followers_account(username)
    lst=[]
    for i in followers:
        #print(bot.get_username_from_user_id(i))
        lst.append(bot.get_username_from_user_id(i))
        time.sleep(random.randint(1,2))
    followers_dict[username]=lst
    return followers_dict

#suivre tous les comptes qui sont abonnés au compte ciblé qui prend en parametre le nom d'utilisateur et la liste de ses followers
def following_accounts(username,followers_dict): 
    lst=liste_followers_account(username)

def lst_fll(user,lst):
    
    user=[]
    user=bot.get_username_from_user_id(lst)
    return user

#fonction qui va suivre tous les followers d'un compte donné qui prend en paramètre le username et la liste de compte à raison de 16

def follow_list_users(username,followers_dict,follow_dict):
    follow_dict[username]=[]
    i=0
    while i<16:
        follow_user(followers_dict[username][0])
        follow_dict[username].append(followers_dict[username][0])
        time.sleep(random.randint(1,2))
        followers_dict [username].remove(followers_dict[username][0])
        i+=1
    return follow_dict,followers_dict




def follow_list_and_move(username, lst, follow_list, sheet):
    count = min(len(lst), 16)
    follow_list.extend(lst[:count])

    for i in range(count):
        follow_user(lst[i])
        time.sleep(random.randint(1, 2))

        # Mettre à jour la deuxième colonne avec "Abonné"
        gsheet.update_cell(sheet, 2, i + 2, "Abonné")
        
    # Supprimer les comptes de la liste originale
    del lst[:count]



def switch_lists_and_reset_counter(lists, current_list_index, follow_counter):
    # Fonction pour passer à la liste suivante et réinitialiser le compteur après chaque heure
    current_list_index = (current_list_index + 1) % len(lists)
    follow_counter = 0
    return current_list_index, follow_counter


#fonction pour mettre les differentes listes dans un google sheet
def inc_gsheet(username, followers_dict):
    save_in_sheet = input("Sauvegarder dans Google Sheet ? (oui, non): ")

    if save_in_sheet.startswith("oui"):
        gsheet.insert_lines([["USERNAME", "STATUT","FOLLOW_BACK"]], 1)

        i = 2
        for f in followers_dict[username]:
            if bot.check_not_bot(f):
                gsheet.insert_lines([[f, "En attente", "En attente"]], i)
                i += 1
                time.sleep(random.randint(0, 4))
            else:
                print(f"[INFO] SKIP {f} -> Bot detection")


def mark_done_in_second_column():
    # Lecture des éléments de la première colonne
    values = read_gsheet(spreadsheet, "A:A")
    
    if values and values[0]:  # Vérifiez que la liste n'est pas vide et qu'elle a au moins un élément
        update_values = [["IS_FOLLOW"]]  # Première ligne
        for value in values[0][1:]:  # Ignore la première valeur
            if value:  # Assurez-vous que cela ne s'exécute pas pour les cellules vides
                update_values.append(["Done"])

        # Écrire les valeurs mises à jour dans la deuxième colonne
        insert_lines(update_values, 1, column=2)
    else:
        print("Aucune donnée à traiter.")



def get_elements_except_first():
    # Lecture des éléments de la première ligne
    values = gsheet.read_gsheet(spreadsheet, "1:1")[0]  # Assurez-vous que "1:1" est la plage correcte pour votre première ligne

    # Retourner les éléments à l'exception du premier
    return values[1:] if len(values) > 1 else []


def update_cell(spreadsheet, row, col, value):
    worksheet = spreadsheet.sheet1
    worksheet.update_cell(row, col, value)


def update_followers_list(bot, username, followers_list, followers_sheet):
    current_followers = bot.get_user_followers(username)
    followers_list[username] = current_followers

    # Mettre à jour la nouvelle page avec les followers
    values_to_insert = [[username] + current_followers]
    gsheet.insert_lines(values_to_insert, 1, column=1, worksheet=followers_sheet)

    return followers_list



def check_and_update_status(spreadsheet, bot, username, followers_list):
    # Lecture du statut actuel de l'utilisateur
    status = gsheet.read_gsheet(spreadsheet, f"B{username}:B{username}")[0][0]

    if status.lower() == "done":
        print(f"Vous êtes déjà abonné à {username}.")
        return False
    else:
        # Mettre à jour la liste des followers
        followers_list = update_followers_list(bot, username, followers_list)

        # Vérifier si l'utilisateur est dans la liste des followers
        if username in followers_list[username]:
            # Mettre à jour la colonne STATUT avec "Done"
            gsheet.update_cell(spreadsheet, username, 2, "Done")
            return True
        else:
            print(f"Skip {username} car il ne vous suit pas.")
            return False

def check_and_follow(spreadsheet, followers_dict):
    # Lecture des éléments de la première colonne
    usernames, statuses = gsheet.read_gsheet(spreadsheet, "A:B")

    # Vérifier que la liste des utilisateurs n'est pas vide
    if len(usernames) > 1:  # La première ligne est le titre, donc on vérifie qu'il y a au moins un utilisateur

        # Appeler la fonction follow_list_users avec le premier utilisateur de la liste
        follow_dict, updated_followers_dict = follow_list_users(usernames[1], followers_dict, {})

        # Mettre à jour la colonne STATUT avec "Done" pour chaque utilisateur dans la liste suivie
        for i, (username, status) in enumerate(zip(usernames[1:], statuses[1:]), start=2):
            if status.lower() != "done":
                # Vérifier si on est déjà abonné avant de suivre
                if check_and_update_status(spreadsheet, i):
                    print(f"Suivre {username}.")
                    # Ici, vous pouvez ajouter la logique pour suivre l'utilisateur
                else:
                    print(f"Skip {username} car déjà abonné.")

        return follow_dict, updated_followers_dict

    else:
        print("La liste des utilisateurs est vide.")
        return None, followers_dict



if __name__=="__main__":
    login()
    #followers_dict={}
    #time.sleep(random.randint(5,15))
    #followers_dict=liste_username_followers(personne_cible,{})
    #time.sleep(random.randint(5,15))
    #print(followers_dict)
   # time.sleep(random.randint(5,15))

    #inc_gsheet(personne_cible,followers_dict)
    followers_list = {}  # Initialisation de la liste des followers
    followers_sheet = "followers_compte"  # Nom de la nouvelle page

    # Utiliser la fonction update_followers_list avec la nouvelle page spécifiée
    update_followers_list(bot, "ib.gnf", followers_list, followers_sheet)

    #readread_gsheet(spreadsheet, range_name)
    #followed_accounts = []
   #follow_list_and_move(personne_cible, followers_dict[username], followed_accounts, sheet)
    
    logout()
    #mark_done_in_second_column()
    
