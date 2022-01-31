import re
import time
import queue
import requests
import threading
import pandas as pd
from bs4 import BeautifulSoup

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

        # First we set the workers to get the phones from the urls
        ad_urls = [x.find("a", {"data-item-name": "detail-page-link"}).attrs['href'] for x in cards]
        ad_urls = ['https://www.autoscout24.es' + x for x in ad_urls]

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
        titles = [x.find("div", {"class": "cldt-summary-full-item"}).attrs['data-tracking-name'] for x in cards]
        kms = [x.find("li", {"data-type": "mileage"}).getText() for x in cards]
        years = [x.find("li", {"data-type": "first-registration"}).getText() for x in cards]
        cambio = [x.find("li", {"data-type": "transmission-type"}).getText() for x in cards]

        # Fix lists syntax
        remove_chars = lambda x: " ".join(x.replace("\n", " ").split())

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

    df = pd.DataFrame(df)
    return df

url = "https://www.autoscout24.es/lst/?sort=age&desc=1&custtype=P&ustate=N%2CU&size=20&cy=E&atype=C&recommended_sorting_based_id=fc7fbe77-56cd-4431-920d-e075f31b45da"
print(scrape(url, 5))