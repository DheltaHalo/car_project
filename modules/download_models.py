import os
import re
import json
import dropbox
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

os.chdir(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.milanuncios.com/coches-de-segunda-mano/?"

s = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options, service=s)
driver.get(url)

# Webdriver
dropdowns_list = driver.find_elements(By.XPATH, '//ul[@class="sui-MoleculeDropdownList sui-MoleculeDropdownList--design-solid sui-MoleculeDropdownList--small is-hidden"]')

#Soup
soup = BeautifulSoup(dropdowns_list[3].get_attribute('innerHTML'), "html.parser")
trademarks = [x.getText() for x in soup.find_all("li")][71:]

urls = []

models_dict = {}

for n, marca in enumerate(trademarks):
    urls.append(driver.current_url)

    marca_click = driver.find_element(By.XPATH, f'//span[text()="{marca}"]')

    driver.execute_script("arguments[0].click();", marca_click) 
    sleep(2)
    # Models
    dropdowns_list = driver.find_elements(By.XPATH, '//ul[@class="sui-MoleculeDropdownList sui-MoleculeDropdownList--design-solid sui-MoleculeDropdownList--small is-hidden"]')
    soup = BeautifulSoup(dropdowns_list[4].get_attribute('innerHTML'), "html.parser")
    models = [x.getText() for x in soup.find_all("li")][1:]

    for k, model in enumerate(models):
        print(model)
        if model == "":
            pass
        else:
            dropdowns_list = driver.find_elements(By.XPATH, '//ul[@class="sui-MoleculeDropdownList sui-MoleculeDropdownList--design-solid sui-MoleculeDropdownList--small is-hidden"]')
            model_click = dropdowns_list[4].find_element(By.XPATH, f'.//span[text()="{model}"]')
            driver.execute_script("arguments[0].click();", model_click)
            sleep(3)
            button = driver.find_element(By.XPATH, '//button[@class="ma-ButtonBasic ma-ButtonBasic--search ma-FormListFilters-footerButton ma-FormListFilters-formSubmitBtn ma-ButtonBasic--medium"]')
            driver.execute_script("arguments[0].click();", button)
            sleep(3)
            mar_id = re.search(r'marca=(.*?)&', driver.current_url).group(1)
            mod_id = re.search(r'modelo=(.*?)&', driver.current_url)

            if mod_id is not None:
                mod_id = mod_id.group(1)
                if marca not in models_dict.keys():
                    models_dict[marca] = {}
                    models_dict[marca]["id"] = mar_id
                    models_dict[marca]["models"] = {}
                
                models_dict[marca]["models"][model] = mod_id
                
                print(f'{n}.{k} - {marca} ({mar_id}) - {model} ({mod_id})')
            else:
                pass

    print(json.dumps(models_dict))
    print("------------------------")

with open("new_models.txt", "w+") as file:
    file.write(json.dumps(models_dict))



