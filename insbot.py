import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])

from instabot import Bot
import time
import random
from bs4 import BeautifulSoup


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
    return  bot.get_user_followers(username)


def liste_username_followers(username):
    lst,lst_followers=[],[]
    lst=liste_followers_account(username)
    time.sleep(random.randint(5,15))
    for i in range(len(lst)-1):
        follower=bot.get_user_id_from_username(lst[i])
        print(f"utilisateur{follower} est abonne a {username}\n")
        lst_followers.append(follower)
        time.sleep(random.randint(1,5))
    print (f"la liste des followers de {username} est:{lst_followers}")

#suivre tous les comptes qui sont abonnés au compte ciblé qui prend en parametre le nom d'utilisateur et la liste de ses followers
def following_accounts(username,liste): 
    liste=liste_followers_account(username)

def lst_fll(user,lst):
    
    user=[]
    user=bot.get_username_from_user_id(lst)
    return user

# mettre la liste des 
        


if __name__=="__main__":
    login()
    #lst=[]
    #user=[]
    #time.sleep(random.randint(5, 15))
    #follow_user(personne_cible)
    #lst=liste_followers_account(personne_cible)
    #print(lst_fll(personne_cible,liste=[]))
    #time.sleep(random.randint(5, 15))
    #user=lst_fll(personne_cible)

    #time.sleep(random.randint(5, 15))
    #print(lst)
    #following_accounts(personne_cible,lst)
    
    liste_username_followers(personne_cible)
    
    
    
    logout()

    