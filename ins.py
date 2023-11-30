import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])

from instabot import Bot
import time
import random
from bs4 import BeautifulSoup
import gsheet



username = "ibrahima.gnf@gmail.com"
password = "m5Mey5eydw"
personne_cible = "ibra.gnf"

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
def inc_gsheet(username,followers_dict):
    save_in_sheet = input("Sauvegarder dans Google Sheet ? (oui, non): ")

    if (save_in_sheet.startswith("oui")):
        gsheet.insert_lines([["USERNAME"]], 1)

        i = 2
        for f in followers_dict[username]:
            if bot.check_not_bot(f):
                gsheet.insert_lines([[f]], i)
                i += 1
                time.sleep(random.randint(0, 4))
            else:
                print(f"[INFO] SKIP {f} -> Bot detection")


def mark_done_in_second_column():
    # Lecture des éléments de la première colonne
    values = gsheet.read_gsheet(spreadsheet, "A:A")[0]  # Assurez-vous que "A:A" est la plage correcte pour votre première colonne

    # Écriture de "Done" dans la deuxième colonne
    for i, value in enumerate(values, start=1):
        if value:  # Assurez-vous que cela ne s'exécute pas pour les cellules vides
            if i == 1:
                gsheet.insert_lines([["IS_FOLLOW"]], i, column=2)  # Première ligne
            else:
                gsheet.insert_lines([["Done"]], i, column=2)  # Assurez-vous que 2 est la colonne correcte
            time.sleep(random.uniform(0.1, 0.5))

def get_elements_except_first():
    # Lecture des éléments de la première ligne
    values = gsheet.read_gsheet(spreadsheet, "1:1")[0]  # Assurez-vous que "1:1" est la plage correcte pour votre première ligne

    # Retourner les éléments à l'exception du premier
    return values[1:] if len(values) > 1 else []




if __name__=="__main__":
    login()
    #followers_dict={}
    #time.sleep(random.randint(5,15))
    #followers_dict=liste_username_followers(personne_cible,{})
    time.sleep(random.randint(5,15))
    #inc_gsheet(personne_cible,followers_dict)
    readread_gsheet(spreadsheet, range_name)
    
    
    logout()

    
