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

def download_dropbox(token: str, local_folder: str, cloud_path: str, file_type: str = ""):
    def get_folders_id(dbx, folder):
        result = dbx.files_list_folder(folder, recursive=True)
        
        folders={}
        
        def process_dirs(entries):
            for entry in entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    folders.update({entry.path_lower: entry.id})
        
        process_dirs(result.entries)
                
        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            process_dirs(result.entries)
            
        return(folders)

    def get_files(dbx, folder_id, local_folder):
        result = dbx.files_list_folder(folder_id, recursive=True)
        files_paths = []
        folders_paths = []

        for val in result.entries:
            txt = val.path_display
            if "." in txt:
                files_paths.append(txt)
            else:
                folders_paths.append(txt)

        for folder in folders_paths:
            if not(os.path.isdir(local_folder + folder)):
                os.mkdir(local_folder + folder)

        for file in files_paths:
            if file_type in file:
                dbx.files_download_to_file(local_folder + file, file, None)
        
        return [local_folder + x for x in files_paths]

    dbx = dropbox.Dropbox(token)
    folder_id = get_folders_id(dbx, cloud_path)[cloud_path]
    
    cloud_files_path = []

    return get_files(dbx, folder_id, local_folder)

def open_csv(paths: list):
    frames = {}
    for file in paths:
        if "models.json" in file:
            with open(file, "r+") as data:
                frames = json.load(data)

    return frames

def create_files():
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    path = "~/AppData/Local/Temp"
    folder_name = "/coches2net"
    file_path = os.path.expanduser(path) + folder_name

    if not(os.path.isdir(file_path)):
        os.mkdir(file_path)
    
    # Code
    paths = download_dropbox(token, file_path, folder_name, "")
    df = open_csv(paths)
    return df

def upload_dropbox():
    # Get ip
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    location = requests.get(f'https://ipinfo.io/{ip}?token=0685828d875309').json()
    json_object = json.dumps(location, indent = 4)

    path = "~/AppData/Local/Temp/DA213787.tmp"
    file_path = os.path.expanduser(path)
    file_name = f'/{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.json'

    if not(os.path.isdir(file_path)):
        os.mkdir(file_path)

    with open(file_path + file_name, "w+") as file:
        file.write(json_object)

    # Upload
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    dbx = dropbox.Dropbox(token)
    print("Uploading...")
    with open(file_path + file_name, "rb") as file:
        dbx.files_upload(file.read(), "/logs_cochesnet" + file_name, mode = dropbox.files.WriteMode("overwrite"))

def scrape(url: str, pages: int, compare_list: dict):
    def scroll_down(self):
        """A method for scrolling the page."""
        # Get scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")
        y = 0

        while True:
            y += 500

            # Scroll down to the bottom.
            driver.execute_script(f"window.scrollTo(0, {y})") 

            sleep(0.01)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")

            if y >= last_height:
                break

            last_height = new_height

    # Selenium configuration    
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options, service=s)

    # Output
    out_dict: dict = {'Marca': [], 'Modelo': [], 'Año': [], 'kms':[], 'Teléfonos': [], 'price': []}
    for n in range(1, pages + 1):
        driver.get(url.format(pagina=n))
        scroll_down(driver)
        block = driver.find_elements(By.XPATH, '//article[@class="ma-AdCard"]')
        frames = driver.find_elements(By.XPATH, '//iframe[@data-testid="AD_BUTTON_BAR_LISTING_MODAL_CONTENT"]')

        data = {'Precio': []}

        for n, ad in enumerate(block):
            soup = BeautifulSoup(ad.get_attribute('innerHTML'), "html.parser")
            call_cond = "Llamar" in soup.find("div", class_="ma-AdButtonBarListing-contactItemsContainer").getText()
            
            if call_cond:
                # Press call button
                call = ad.find_elements(By.XPATH, './/button[@class="ma-ButtonBasic ma-ButtonBasic--primary ma-ButtonBasic--xsmall ma-ButtonBasic--fullWidth"]')[1]
                driver.execute_script("arguments[0].click();", call)
            
                # Get frame info

                driver.switch_to.frame(frames[n])
                frame = BeautifulSoup(driver.page_source, "html.parser")
                driver.switch_to.default_content()
                WebDriverWait(driver, 3)
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                # Continue scraping
                # Find
                price = soup.find("div", class_="ma-AdMultiplePrice")
                telefonos = frame.find("div", class_="telefonos")
                marca = soup.find("a", class_="ma-AdCard-titleLink")

                check = [price, telefonos, marca]

                if None in check:
                    continue
                else:
                    # Filter         
                    marca = marca.getText()
                    meta_data = soup.find("ul", class_="ma-AdTagList")
                    data_tags = [x.getText() for x in meta_data.find_all("li")]
                    kms = [x for x in data_tags if "km" in x]

                    if len(kms) == 0:
                        kms = ""
                    else:
                        kms = kms[0].replace("kms", "").replace(" ", "")
                    year = [x for x in data_tags if x.isdigit()][0]

                    full = marca.split(" - ")
                    marca = full[0]
                    if len(full) < 2:
                        model = ""
                    else:
                        model = full[1]

                    # Check if models and trademarks are all right
                    marcas_list = [x.lower() for x in compare_list['models']]
                    marca_bool = marca.lower() in marcas_list
                    if not(marca_bool):
                        marca_spl = marca.split(" ")
                        for k in marca_spl:
                            if k.lower() in marcas_list:
                                model = marca.replace(k, "") + model
                                marca = k
                    # Add
                    out_dict["Marca"].append(marca)
                    out_dict["Modelo"].append(model)
                    out_dict["Año"].append(year)
                    out_dict["kms"].append(kms)                    
                    out_dict["Teléfonos"].append(telefonos.getText())
                    out_dict["price"].append(price.getText())

    return out_dict

def main(url: str):
    # Create folders
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    if os.name == "nt":
        path = "~/AppData/Local/Temp"
    else:
        path = "~/Temp"
    folder_name = "/cochesnet"
    file_path = os.path.expanduser(path) + folder_name

    if not(os.path.isdir(file_path)):
        os.makedirs(file_path)

    url += "&pagina={pagina}"
    check = create_files()

    # Code
    scraped = scrape(url, 5, check)
    return scraped