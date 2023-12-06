from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from random import *
import os
import time
import json
import gsheet

COOKIES_PATH = 'auth/cookies.json'
LOCAL_STORAGE_PATH = 'auth/local_storage.json'

class LinkedinBot():
    def __init__(self, username, password, weekly_limit=200) -> None:
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        self.options.use_chromium = False
        self.options.add_argument("start-maximized")
        self.options.page_load_strategy = 'eager' #Ne pas attendre que les images aient totalement finies de charger, non utile
        self.options.add_argument(f"user-agent={self.user_agent}")
        #self.options.add_experimental_option("detach", True)

        self.s = 20 #Temps entre les étapes (en secondes)
        self.driver = webdriver.Chrome(options=self.options)
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver,self.s)

        self.username = username
        self.password = password
        self.login_page = "https://www.linkedin.com/login"

        self.weekly_limit = weekly_limit
        text_file = open("counter.txt", "r")
        self.weekly_counter = int(text_file.readline())
        text_file.close()
        #LIEN DE RECHERCHE (a remplacer)
        self.custom_search = r"https://www.linkedin.com/search/results/people/?geoUrn=%5B%22105015875%22%5D&keywords=avocat%20justice&origin=FACETED_SEARCH&sid=YPR" # change
        self.search_link = self.custom_search

    def custom_wait(self, driver, timeout, condition_type, locator_tuple):
        wait = WebDriverWait(driver, timeout)
        return wait.until(condition_type(locator_tuple))

    def click_and_wait(self, element, delay=1):
        self.action.move_to_element(element).click().perform()
        time.sleep(delay)

    def scroll_to_bottom(self, delay=2):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(delay)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                break
            last_height = new_height
        print("Scrolled to bottom.")

    def load_data_from_json(self, path): return json.load(open(path, 'r'))
    def save_data_to_json(self, data, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(data, open(path, 'w'))

    def add_cookies(self, cookies): [self.driver.add_cookie(cookie) for cookie in cookies]
    def add_local_storage(self, local_storage): [self.driver.execute_script(f"window.localStorage.setItem('{k}', '{v}');") for k, v in local_storage.items()]

    def get_first_folder(self, path): return os.path.normpath(path).split(os.sep)[0] 

    def delete_folder(self, folder_path):
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                self.delete_folder(file_path) if os.path.isdir(file_path) else os.remove(file_path)
            os.rmdir(folder_path)

    def success(self):
        try:
            self.custom_wait(self.driver, 15, EC.presence_of_element_located, (By.XPATH, '//div[contains(@class,"global-nav__me")]'))
            return True
        except:
            return False

    def navigate_and_check(self, probe_page):
        print("Try to get Driver...")
        self.driver.get(probe_page)
        print("Driver got")
        print("Sleep 15s...")
        time.sleep(15)
        print("ok !")
        if self.success():
            self.save_data_to_json(self.driver.get_cookies(), COOKIES_PATH)
            self.save_data_to_json({key: self.driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in self.driver.execute_script("return Object.keys(window.localStorage);")}, LOCAL_STORAGE_PATH)
            return True
        else: 
            return False
   
    def login(self):

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]'))).send_keys(self.username)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]'))).send_keys(self.password)
        self.action.click(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "S’identifier")]')))).perform()

        self.action.click(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="gsi_838850_530161-wrapper"]')))).perform()
        print("Try to login...Sleep 15s")
        time.sleep(15)
        print("Login !")
    
    def check_cookies_and_login(self):
        self.driver.get(self.login_page)
        time.sleep(3)
    
        if os.path.exists(COOKIES_PATH) and os.path.exists(LOCAL_STORAGE_PATH):
            self.add_cookies(self.load_data_from_json(COOKIES_PATH))
            self.add_local_storage(self.load_data_from_json(LOCAL_STORAGE_PATH))
            #self.add_cookies(self.load_data_from_json('./test/gcookies.json'))
            print("Cookies ajoutés !")
            if self.navigate_and_check(self.search_link):
                return 
            else: 
                self.delete_folder(self.get_first_folder(COOKIES_PATH))
        self.driver.get(self.login_page)
        time.sleep(3)
        self.login()
        self.navigate_and_check(self.search_link)
    
    def connect(self, name):
        try:
            try: 
                email_demand = self.custom_wait(self.driver, 3, EC.presence_of_element_located, (By.XPATH, '//label[@for="email"]'))
                close_button = self.custom_wait(self.driver, 3, EC.element_to_be_clickable, (By.XPATH, '//button[@aria-label="Dismiss"]'))
                self.click_and_wait(close_button,0)
            except:
                pass
            try:
                add_a_note_button = self.custom_wait(self.driver, 5, EC.element_to_be_clickable, (By.XPATH, '//button[@aria-label="Ajouter une note"]'))
                self.click_and_wait(add_a_note_button,0)
            except:
                pass 
            try:
                cover_letter_textarea = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id="custom-message"]')))
            except:
                return 1
            try:
                got_it_button = self.custom_wait(self.driver, 2, EC.presence_of_element_located, (By.XPATH, '//button//span[contains(., "Got it")]'))
                self.click_and_wait(got_it_button,0)
            except:
                pass
            return 0 
        except:
            return 1

    def find_connect_buttons_and_people_names_and_perform_connect(self):
        global weekly_counter
        self.scroll_to_bottom()
        time.sleep(1)
        try:
            connect_buttons = self.custom_wait(self.driver, 3, EC.presence_of_all_elements_located, (By.XPATH, '//button//span[contains(., "Se connecter")]'))
        except:
            return
        
        for connect_button in connect_buttons:
            person = connect_button.find_element(By.XPATH, './/ancestor::div[@class="entity-result__item"]')
            person_name = person.find_element(By.XPATH, './/span[@aria-hidden="true"]').get_attribute('innerHTML').strip("\n <!---->")
            gsheet.insert_lines([[f"{person_name}"]])
            self.click_and_wait(connect_button,0.5)
            
            if (self.weekly_counter<self.weekly_limit):
                sts = self.connect(person_name) 
                if sts == 1: continue
                elif sts == 0:
                    self.weekly_counter +=1
                    with open('counter.txt', 'w') as a:
                        a.writelines(str(self.weekly_counter))
                    time.sleep(random.uniform(0.2, 2)) 
            elif(self.weekly_counter >= self.weekly_limit): 
                print("Tu as atteint la limite de "+ str(self.weekly_limit) +" requêtes de connexion.\n")
                self.driver.close()
                self.driver.quit()
                
    def run(self):
        self.check_cookies_and_login()
        print("Cookies were check and logged in.")
        if not self.custom_search: 
            self.action.click(self.wait.until(EC.element_to_be_clickable((By.XPATH, '//section[@class="artdeco-card ember-view pv-top-card"]//a[@class="ember-view"]')))).perform()
            time.sleep(15)
        while True:
            try:
                self.scroll_to_bottom()
                time.sleep(5)
                test_results_presence = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="entity-result__item"]')))
            except:
                break
            if test_results_presence:

                self.find_connect_buttons_and_people_names_and_perform_connect()
            try:
                self.scroll_to_bottom()
                next_page_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]')))
                self.action.move_to_element(next_page_button).perform()
                time.sleep(0.5)
                self.action.click(next_page_button).perform()
            except:
                break

        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    bot = LinkedinBot("zadigmclebg@gmail.com", "")
    bot.run()
