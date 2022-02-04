import os
import re
import time
import json
import queue
import dropbox
import requests
import threading
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

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

class Worker(threading.Thread):
    def __init__(self, q: queue.Queue, periods: float, timeout: int, *args, **kwargs):
        self.q = q
        self.periods = periods
        # Special number -1
        if timeout == -1:
            self.timeout = 999999999
        else:
            self.timeout = timeout
        super().__init__(*args, **kwargs)
        self.daemon = True

    def run(self):
        # Time when the program will stop running
        end_time = time.time() + self.timeout
        cond = True
        while (time.time() < end_time) and cond:
            if self.q.empty():
                break
            else:
                url = self.q.get()
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                tlf = soup.find("a", {"id": "js-original-phone-number"})
                if tlf != None:
                    tlf = re.search(r'\d{9}$', tlf.attrs["href"]).group()

                result_q.put([url, tlf])
                
                self.q.task_done()

def scrape(url: str, pages: str):
    session = requests.Session()
    df = {"Marca": [], "Modelo": [], "Año": [], "Teléfono": [], "kms": [], "Cambio": []}

    for k in range(1, pages + 1):
        r = session.get(url + f"&page={k}")

        # Find all info
        html = BeautifulSoup(r.text, 'html.parser')
        cards = html.find_all("div", class_="cl-list-element cl-list-element-gap")
        counter = html.find("span", class_="sc-font-bold cl-filters-summary-counter").getText()
        counter = int(re.match(r'[\d+]?\.?\d+', counter).group().replace(",", "").replace(".", ""))

        # First we set the workers to get the phones from the urls
        pop = lambda lis, indx: [lis.pop(i) for i in sorted(indx, reverse=True)]

        ad_urls = [x.find("a", {"data-item-name": "detail-page-link"}) for x in cards]
        indx_remove = [i for i, x in enumerate(ad_urls) if x == None]
        pop(ad_urls, indx_remove)
        ad_urls = ['https://www.autoscout24.es' + x.attrs["href"] for x in ad_urls]

        workers = []
        q = queue.Queue()
        global result_q
        result_q = queue.Queue()
        for ad in ad_urls:
            q.put(ad)

        for _ in range(5):
            workers.append(Worker(q, 1, 60))

        for worker in workers:
            worker.start()

        # We continue with bs4
        titles = [x.find("div", {"class": "cldt-summary-full-item"}) for x in cards]
        kms = [x.find("li", {"data-type": "mileage"}) for x in cards]
        years = [x.find("li", {"data-type": "first-registration"}) for x in cards]
        cambio = [x.find("li", {"data-type": "transmission-type"}) for x in cards]

        # Fix lists syntax
        remove_chars = lambda x: " ".join(x.replace("\n", " ").split())

        pop(titles, indx_remove)
        pop(kms, indx_remove)
        pop(years, indx_remove)
        pop(cambio, indx_remove)

        titles = [x.attrs['data-tracking-name'] for x in titles]
        kms = [x.getText() for x in kms]
        years = [x.getText() for x in years]
        cambio = [x.getText() for x in cambio]

        kms = list(map(remove_chars, kms))
        cambio = list(map(remove_chars, cambio))
        years = list(map(remove_chars, years))

        cambio = [x if "Cambio" not in x else "" for x in cambio]
        years = [re.search(r'\d{4}', x) for x in years]
        years = ["" if x == None else x.group() for x in years]

        all = {z[0]: list(z[1:]) for z in zip(ad_urls, titles, years, kms, cambio)} 

        for worker in workers:
            worker.join()

        for k in result_q.queue:
            if k[1] == None:
                all.pop(k[0], None)
            else:
                all[k[0]].append(k[1])

        for car in all.values():
            ma, mo = car[0].split("|")
            df["Marca"].append(ma)
            df["Modelo"].append(mo)
            df["Año"].append(car[1])
            df["kms"].append(car[2])
            df["Cambio"].append(car[3])
            df["Teléfono"].append(car[4])
        
        for key in df:
            if len(df[key]) > counter:
                del df[key][counter:]

    df = pd.DataFrame(df)
    return df