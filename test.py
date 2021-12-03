import requests
from time import sleep

while True:
    sleep(1)
    try:
        t = requests.get("http://www.google.es")
        print(t)
        break
    
    except requests.exceptions.ConnectionError:
        print("ERROR")
        pass
