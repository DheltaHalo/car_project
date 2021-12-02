from types import CodeType
import requests
import re
from time import sleep
import json
from json import JSONDecodeError
import csv
import os
import pandas as pd
import subprocess
import dropbox
from dropbox.files import WriteMode

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
    with requests.Session() as sesh:
        if url[-1] == "/":
            url += "?&pg="
        else:
            url += "&pg="

        for page in range(1, n_pages + 1):
            sleep(3)

            # We create the session and extract the html
            info = sesh.get(url)
            r = requests.get(url + str(page), headers=headers)
            html = r.text
            if html == "":
                break
            else:
                if not("No hemos encontrado resultados" in html or html == ""):
                    if html_bool:
                        start = '<script>window.__INITIAL_PROPS__ = JSON.parse("'
                        end = '");</script><script>window.__INITIAL_CONTEXT_VALUE'
                        fixedtext = html[html.find(start)+len(start):html.rfind(end)].strip().replace('\\','').replace('": "{"',": {").replace('":"{"','":{"').replace('}"},','}},').replace('}"}','}}')
                        return fixedtext

                    else:
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

                            try:
                                output[n] = {k: val[k] for k in import_keys}
                            except KeyError:
                                pass

                        keys = output[0].keys()

                        # We save the data
                        with open(f'{path}/{page}.csv', 'w+', newline='') as output_file:
                            dict_writer = csv.DictWriter(output_file, keys)
                            dict_writer.writeheader()
                            dict_writer.writerows(output)
                        if os.name != "nt":
                            subprocess.call(['chmod', '7777', f'{path}/{page}.csv'])

def create_all(path: str, links: dict, n_pages: int):
    for parent in links:
        print(parent)
        parent_path = f'{path}/{parent}'

        if not(os.path.isdir(parent_path)):
            os.mkdir(parent_path)
            if os.name != "nt":
                subprocess.call(['chmod', '7777', parent_path])

        for item in links[parent]:
            print(f"\t{item}")
            if len(links[parent]) == 1:
                pass #get_url(parent_path, links[parent][item], n_pages)

            else:
                child_path = f'{parent_path}/{item}'
                if not(os.path.isdir(child_path)):
                    os.mkdir(child_path)
                    if os.name != "nt":
                        subprocess.call(['chmod', '7777', child_path])

                if len(links[parent][item]) == 1:
                    if int(item) >= 2014:
                        get_url(child_path, links[parent][item]["url"], n_pages)
                
                else:
                    for name in links[parent][item]["models"]:
                        print(f"\t\t{name}")
                        subchild_path = f'{child_path}/{name}'
                        if not(os.path.isdir(subchild_path)):
                            os.mkdir(subchild_path)
                            if os.name != "nt":
                                subprocess.call(['chmod', '7777', subchild_path])

                        get_url(subchild_path, links[parent][item]["models"][name]["url"], n_pages)

def create_urls():
    # We create the urls
    url = "https://www.coches.net/segunda-mano"
    particular = "?st=2"
    urls = {"base": {0: f"{url}/{particular}"}}

    max_year = 2021
    min_year = 1971

    years_str = "&MaxYear={year}&MinYear={year}"
    years_dict = {x: {"url": f'{url}/{particular}{years_str.format(year=x)}'} \
                  for x in range(min_year, max_year + 1)}
    years_dict = {"years": years_dict}

    # We create the "marcas"
    from modules import download
    modules_path = download.export_data(".json")
    modules_path = [k for k in modules_path if "models" in k][0]

    with open(modules_path, "r+") as file:
        data = json.load(file)

    marca_dict = {k: {"url": f'{url}/{k}/{particular}'} for k in data}
    marca_dict = {"marcas": marca_dict}

    # We create the models
    for marca in marca_dict["marcas"]:
        if len(data[marca]) > 0:
            marca_dict["marcas"][marca]["models"] = {}

        for model in data[marca]:
            model = str(model)
            model_link = model.replace(" ", "_")
            marca_dict["marcas"][marca]["models"][model] = \
            {"url": f"{url}/{marca}/{model_link}/{particular}"}
    
    print("Completados los modelos!")
    urls.update(years_dict)
    urls.update(marca_dict)
    
    return urls

def create_pandas(database_path: str):
    files_paths = []
    models_paths = []
    dataframes = []

    for root, dirs, files in os.walk(database_path):
        for file in files:
            if ".csv" in file:
                if re.match(r'\d+.csv', file):
                    files_paths.append(f'{root}/{file}')
                else:
                    models_paths.append(f'{root}/{file}')

    for file_path in files_paths:
        dataframes.append(pd.read_csv(file_path))

    df = pd.concat(dataframes)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df, models_paths

def upload_file_to_dropbox(token: str, files_paths: list, cloud_folder_path: str):
    dbx = dropbox.Dropbox(token)
    for file_path in files_paths:
        name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            dbx.files_upload(file.read(), f'{cloud_folder_path}/{name}', mode=WriteMode("overwrite"))

def main(n_pages: int):
    # We change the dir and set some constants
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    files_folder_name = "database"
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'

    # Paths
    path = os.getcwd() + "/"
    files_path = path + files_folder_name

    # Create folders
    if not(os.path.isdir(path + files_folder_name)):
        os.mkdir(files_folder_name)
        if os.name != "nt":
                subprocess.call(['chmod', '7777', files_folder_name])

    urls = create_urls()
    create_all(files_path, urls, n_pages)
    df = create_pandas(files_path)
    df[0].to_csv("car_data.csv", index=False)
    subprocess.call(['chmod', '7777', 'car_data.csv'])

    upload_file_to_dropbox(token, df[1], '/database/models')
    upload_file_to_dropbox(token, ["car_data.csv"], '/database')

if __name__ == "__main__":
    # sol = int(input("Número de páginas?\nRespuesta: "))
    main(1000)

