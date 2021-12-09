import os
import pandas as pd
import dropbox
from time import sleep
import re
import requests
import json
from json import JSONDecodeError
import csv
import sys
from PyQt5.QtCore import QEventLoop, QTimer
from datetime import datetime

def get_url(path: str, url: str, n_pages: int, html_bool: bool = False):
    headers = {
        'authority': 'www.coches.net',
        'method': 'GET',
        'path': '/ztkieflaaxcvaiwh2',
        'scheme': 'https',
        'accept': '*/*',
        'acce  pt-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_hjid=ed2929df-46cf-4aa6-93b5-420db0a8309f; borosTcf=eyJwb2xpY3lWZXJzaW9uIjoyLCJjbXBWZXJzaW9uIjozNSwicHVycG9zZSI6eyJjb25zZW50cyI6eyIxIjp0cnVlLCIyIjp0cnVlLCIzIjp0cnVlLCI0Ijp0cnVlLCI1Ijp0cnVlLCI2Ijp0cnVlLCI3Ijp0cnVlLCI4Ijp0cnVlLCI5Ijp0cnVlLCIxMCI6dHJ1ZX19LCJzcGVjaWFsRmVhdHVyZXMiOnsiMSI6dHJ1ZX0sInZlbmRvciI6eyJjb25zZW50cyI6eyI1NjUiOnRydWV9fX0=; ajs_anonymous_id=%22468ceb25-0512-4df6-a1ea-fcbbf37e2c92%22; _pbjs_userid_consent_data=7427440918879690; _gcl_au=1.1.610503440.1636470475; _fbp=fb.1.1636470475835.898329892; __gads=ID=42ab5ae8a63e0fdb-221111a6dacc0027:T=1636470476:RT=1636470476:S=ALNI_MZtgJZqAfPHblQrkurUPLOsGBGhrw; gig_bootstrap_3_ejKPtiTCoMZOmiD2PJgl0GYbIQOdeBma77joBheqTs15Nx5EkD9evJSOuefj2S6H=_gigya_ver4; _hjSessionUser_48459=eyJpZCI6ImNjNDcxMWVjLTI1ZWEtNTc0Yi1hZmE1LTA5M2I2YzM0NDgzMSIsImNyZWF0ZWQiOjE2MzcxNTcwNDY4NjgsImV4aXN0aW5nIjp0cnVlfQ==; euconsent-v2=CPP-lwrPP-lwrCBAjAESB2CoAP_AAP_AAAiQIXtf_X__bX9n-_79__t0eY1f9_r3v-QzjhfNt-8F2L_W_L0X_2E7NF36pq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2cpyNKJ7LkmnsZe2dYGHtPn9lT-ZKZ7_7___f73z___9_-39z3_9f___d__-v_-_v___9_____________________-CF7X_1__21_Z_v-_f_7dHmNX_f697_kM44XzbfvBdi_1vy9F_9hOzRd-qauCrkeJLt2wSEDbRzJ1E1JsWqJVa8x7GpNnKcjSiey5Jp7GXtnWBh7T5_ZU_mSme_-___3-98____f_t_c9__X___3f__r__v7____f_____________________gAAA; cfg=1; _hjSession_48459=eyJpZCI6ImU4ZTcyZjdmLTFkOWUtNDc2Ni1iM2YwLWY3ZWRkYmM4MDQ1YiIsImNyZWF0ZWQiOjE2Mzc2NzUzODE5MzF9; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; reese84=3:SJWrgjMzYo+VzT/2IAl2oQ==:XXgqIAIdqRs01jKFhlWZn3KxzvFs0weGy+FIvyxoNaGykJ9npCWiP0JLjXdj7HoCHvNWfq0neWjaFB1S0pXZzgNb14N53V+G2Z1tOpIoPJle8DUCR61zBtzaAIR0XRNsfyZztZs1TMFy05AaZqjxijClnzmXcRvfWI0Sa4eryYaYswjkUau1Ps95zpp3jwBYM1ZbLI2auUnsFx7Sjjpmj6X0J/HySVEymFsQ5/UGRyGP9ba10UN/Voa0PC9TigWSS0vCUKkNPHR182xDJISqT1Pwn9F4H5aaAsNkK1uTkEEWITXT9oOYOAT7kVgzERzaP5QtF06aZsdlGnQhh30VV7QovGaVnqe08h6Zlm6Je9vNxDNPN6BLcCMLsXc/7SBKfZWK8zYnOrmKxknk+tYYHIGA7KdTaDxVyrE1cMR7CQDcopAsARtMeVtpFy4CQgw9:fMNtATf0Of4RGZdleNEJ+7s0sziXILn88PPyghpUyf8=; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; AMCV_05FF6243578784B37F000101%40AdobeOrg=-408604571%7CMCIDTS%7C18955%7CMCMID%7C44515756373560126224607294549045551812%7CMCAAMLH-1638280182%7C6%7CMCAAMB-1638280182%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1637682582s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; cto_bundle=L3zjWl9ZNUdRdEhodWY2ZGw1NXkzRGNha3NtdmlqSDM4aWpTeHR5VyUyQmZRRyUyQlRqcU1vSDhjMlZ4dGNkMVFCY2FDeGZPM3BONndsTGNJSW85VDRyUVFJcXc5TmU5enJZeGZRWSUyRlpOJTJGTHRoaGNTJTJCem8yWXlpc3dnQ1BwS1dkbTZ5YXNTRldhVXJzOVJQWjdGalJvNHlhaHNyRFdnJTNEJTNE',
        'pragma': 'no-cache',
        'referer': 'https://www.coches.net/segunda-mano/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    sesh = requests.Session()
    url += "&pg="
    car_data = []
    for page in range(1, n_pages + 1):
        print(n_pages)
        print(page)
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec_()

        # We create the session and extract the html
        info = sesh.get(url)
        r = requests.get(url + str(page), headers=headers)
        html = r.text

        if not("No hemos encontrado resultados" in html or html == ""):
            # We parse the text file to anice json version
            output = []
            start = '<script>window.__INITIAL_PROPS__ = JSON.parse("'
            end = '");</script><script>window.__INITIAL_CONTEXT_VALUE'

            fixedtext = html[html.find(start)+len(start):html.rfind(end)].strip().replace('\\','').replace('": "{"',": {").replace('":"{"','":{"').replace('}"},','}},').replace('}"}','}}')

            # We filter the data
            try:
                data = json.loads(fixedtext)

            except JSONDecodeError:
                openBr = 0
                pos = fixedtext.index("initialResults")
                new_text = fixedtext[pos:]
                for k in range(len(new_text)):
                    if new_text[k] == "{":
                        openBr += 1

                    if new_text[k] == "}":
                        openBr -= 1

                        if openBr == 0:
                            break
                    
                match = [x for x in re.findall(r'(?<=,"title":")(.+?)(?=",")', fixedtext[pos:k+1+pos]) if "\"" in x]
                for error in match:
                    fixedtext = fixedtext.replace(error,  error.replace("\"", ""))

                data = json.loads(fixedtext)

            for car in data['initialResults']['items']:
                output.append(car)
                keys_list = list(output[0].keys())

            import_keys = ["marca", "title", "year", "phone", "isProfessional", "url"]

            remove_key = []

            for n, val in enumerate(output):
                for key in list(val.keys()):
                    if not(key in import_keys):
                        val.pop(key, None)
                    else:
                        if key == "title":
                            val["marca"] = val[key].split(" ")[0]

                output[n] = {k: val[k] for k in import_keys}

            keys = output[0].keys()
            car_data.extend(output)

        else:
            break

    if html_bool:
        keys = list(car_data[0].keys())
        df = {key: [] for key in keys}
        for car in car_data:
            for key in car:
                df[key].append(car[key])
        return df

    else:
        # We save the data
        with open(f'{path}\\{page}.csv', 'w+', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(car_data)

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

def open_csv(paths: list):
    frames = {"main": "", "models": {}}
    for file in paths:
        if ".json" in file:
            with open(file, "r+") as data:
                frames["models"] = json.load(data)
        
        if ".csv" in file:
            df = pd.read_csv(file)
            frames["main"] = df

    return frames

def create_files():
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    path = "~/AppData/Local/Temp"
    folder_name = "/cochesnet"
    file_path = os.path.expanduser(path) + folder_name

    if not(os.path.isdir(file_path)):
        os.mkdir(file_path)
    
    # Code
    paths = download_dropbox(token, file_path, folder_name, "")
    df = open_csv(paths)
    return df
    
def filter(df: pd.DataFrame, key: str, filter: str):
    df = df[df[key] == filter]

    return df

def clean(df: pd.DataFrame):
    df = df.loc[df["isProfessional"] == False]
    df = df.drop("isProfessional", 1)
    df = df.drop("url", 1)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df["phone"] = df["phone"].apply(str)
    match_frame = df["phone"].apply(str).str.match(r"9\d{8}", case=True, flags=0, na=None)
    match_list = [i for i, val in enumerate(match_frame) if val == True]
    df = df.drop(match_list)
    df = df.rename(columns={'marca': 'Marca', 'title': 'Modelo', 'year': 'Año', 'phone': 'Teléfono'})

    return df