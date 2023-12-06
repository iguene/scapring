from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from random import *
import os
import time
import json 
    
COOKIES_PATH = 'auth/cookies.json'
LOCAL_STORAGE_PATH = 'auth/local_storage.json'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
options = webdriver.ChromeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
options.page_load_strategy = 'eager' #Ne pas attendre que les images aient totalement finies de charger, non utile
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option("detach", True)

s = 20 #Temps entre les étapes (en secondes)
driver = webdriver.Chrome(options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

def custom_wait(driver, timeout, condition_type, locator_tuple):
    wait = WebDriverWait(driver, timeout)
    return wait.until(condition_type(locator_tuple))


username = "zadigmclebg@gmail.com"
password = ""
login_page = "https://www.linkedin.com/login"

weekly_limit=200
weekly_limit -=5 
text_file = open("counter.txt", "r")
weekly_counter = int(text_file.readline())
text_file.close()

#LIEN DE RECHERCHE (a remplacer)
custom_search = r"https://www.linkedin.com/search/results/people/?geoUrn=%5B%22105015875%22%5D&keywords=avocat%20justice&origin=FACETED_SEARCH&sid=YPR" # change

search_link = custom_search

def click_and_wait(element, delay=1):
    action.move_to_element(element).click().perform()
    time.sleep(delay)
      
def scroll_to_bottom(delay=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            break
        last_height = new_height
    print("Scrolled to bottom.")

def load_data_from_json(path): return json.load(open(path, 'r'))
def save_data_to_json(data, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(data, open(path, 'w'))

def add_cookies(cookies): [driver.add_cookie(cookie) for cookie in cookies]
def add_local_storage(local_storage): [driver.execute_script(f"window.localStorage.setItem('{k}', '{v}');") for k, v in local_storage.items()]

def get_first_folder(path): return os.path.normpath(path).split(os.sep)[0] 

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            delete_folder(file_path) if os.path.isdir(file_path) else os.remove(file_path)
        os.rmdir(folder_path)

def success():
    try:
        custom_wait(driver, 15, EC.presence_of_element_located, (By.XPATH, '//div[contains(@class,"global-nav__me")]'))
        return True
    except:
        return False

def navigate_and_check(probe_page):
    driver.get(probe_page)
    time.sleep(15)
    if success():
        save_data_to_json(driver.get_cookies(), COOKIES_PATH)
        save_data_to_json({key: driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in driver.execute_script("return Object.keys(window.localStorage);")}, LOCAL_STORAGE_PATH)
        return True
    else: 
        return False
   
def login():
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]'))).send_keys(password)
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "S’identifier")]')))).perform()
    print("Try to login...Sleep 15s")
    time.sleep(15)
    print("Login !")
    
def check_cookies_and_login():
    driver.get(login_page)
    time.sleep(3)
    
    if os.path.exists(COOKIES_PATH) and os.path.exists(LOCAL_STORAGE_PATH):
        add_cookies(load_data_from_json(COOKIES_PATH))
        add_local_storage(load_data_from_json(LOCAL_STORAGE_PATH))
        
        if navigate_and_check(search_link):
            return 
        else: 
            delete_folder(get_first_folder(COOKIES_PATH))
    
    driver.get(login_page)
    time.sleep(3)
    login()
    navigate_and_check(search_link)
    
    
def connect(name):
    try:
        try: 
            email_demand = custom_wait(driver, 3, EC.presence_of_element_located, (By.XPATH, '//label[@for="email"]'))
            close_button = custom_wait(driver, 3, EC.element_to_be_clickable, (By.XPATH, '//button[@aria-label="Dismiss"]'))
            click_and_wait(close_button,0)
        except:
            pass
        try:
            add_a_note_button = custom_wait(driver, 5, EC.element_to_be_clickable, (By.XPATH, '//button[@aria-label="Ajouter une note"]'))
            click_and_wait(add_a_note_button,0)
        except:
            pass 
        try:
            cover_letter_textarea = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id="custom-message"]')))
        except:
            return 1
        try:
            got_it_button = custom_wait(driver, 2, EC.presence_of_element_located, (By.XPATH, '//button//span[contains(., "Got it")]'))
            click_and_wait(got_it_button,0)
        except:
            pass
        return 0 
    except:
        return 1

def find_connect_buttons_and_people_names_and_perform_connect():
    global weekly_counter
    scroll_to_bottom()
    time.sleep(1)
    try:
        connect_buttons = custom_wait(driver, 3, EC.presence_of_all_elements_located, (By.XPATH, '//button//span[contains(., "Se connecter")]'))
    except:
        return
    
    for connect_button in connect_buttons:
        person = connect_button.find_element(By.XPATH, './/ancestor::div[@class="entity-result__item"]')
        person_name = person.find_element(By.XPATH, './/span[@aria-hidden="true"]').get_attribute('innerHTML').strip("\n <!---->")
        click_and_wait(connect_button,0.5)
        
        if (weekly_counter<weekly_limit):
            sts = connect(person_name) 
            if sts == 1: continue
            elif sts == 0:
                weekly_counter +=1
                with open('counter.txt', 'w') as a:
                    a.writelines(str(weekly_counter))
                time.sleep(random.uniform(0.2, 2)) 
        elif(weekly_counter>=weekly_limit): 
            print("Tu as atteint la limite de "+ str(weekly_limit) +" requêtes de connexion.\n")
            driver.close()
            driver.quit()
                
def main():
    check_cookies_and_login()
    print("Cookies were check and logged in.")
    if not custom_search: 
        action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//section[@class="artdeco-card ember-view pv-top-card"]//a[@class="ember-view"]')))).perform()
        time.sleep(15)
    while True:
        try:
            scroll_to_bottom()
            time.sleep(5)
            test_results_presence = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="entity-result__item"]')))
        except:
            break
        if test_results_presence:

            find_connect_buttons_and_people_names_and_perform_connect()
        try:
            scroll_to_bottom()
            next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]')))
            action.move_to_element(next_page_button).perform()
            time.sleep(0.5)
            action.click(next_page_button).perform()
        except:
            break

    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()