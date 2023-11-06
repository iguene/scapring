import requests
from bs4 import BeautifulSoup

def get_instagram_followers(username):
    url = f'https://www.instagram.com/{username}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        followers_section = soup.find('meta', {'name': 'description'})
        
        if followers_section and followers_section.get('content'):
            followers_text = followers_section.get('content').split('Followers')[0].strip()
            followers_list = [follower.strip() for follower in followers_text.split(',')]
            return followers_list
        else:
            print("Unable to find followers information on the page.")
            return []
    else:
        print(f"Failed to retrieve followers. Status code: {response.status_code}")
        return []

# Exemple d'utilisation
username = 'ibra.gnf'
followers_list = get_instagram_followers(username)

if followers_list:
    print(f"Followers de {username}:")
    for follower in followers_list:
        print(f"- {follower}")
else:
    print("Erreur lors de la récupération des followers.")
print(followers_list)