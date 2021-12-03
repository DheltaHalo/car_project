import requests
import hashlib
import pandas as pd
from datetime import date, datetime
from tkinter import filedialog
from tkinter import *

def get_columns():
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfile(filetypes=[("Excel files", ".xlsx .xls")])

    df = pd.read_excel(path.name)
    tlf = df[["Modelo", "Teléfono"]]

    return tlf

def send_sms(tlf: str, msg: str):
    KEY = "5Zk57EmotZ2Rq4L4z7Lp2zwHZYPzzhcJ"
    FROM = "HelpMyCar"

    TO = "34" + tlf
    MESSAGE = msg

    date = str(datetime.now())
    hash256 = hashlib.sha256(date.encode('utf-8'))
    val = int.from_bytes(hash256.digest(), 'big')

    balance = f"http://api.smsarena.es/http/balance.php?&auth_key={KEY}"
    sms_url = f"http://api.smsarena.es/http/sms.php?auth_key={KEY}&id={val}&from={FROM}&to={TO}&text={MESSAGE}"

    bal = requests.get(balance)
    sms=1#sms = requests.get(sms_url)

    return bal.text, sms
    
def main():
    try:
        df = get_columns()
    except KeyError:
        print(input("El archivo que ha intentado abrir no era el correcto.\nPulse Enter para cerrar."))
        exit()

    msg = 'Buenos días,\n\nLe mandamos un mensaje desde nuestra compañía HelpMyCar\n' +\
    'para comprar su "{car}". Si le interesa nuestra oferta' +\
    'puede contactar con nostros en lmao@gmail.com.\n\nMuchas gracias.'

    for k in range(len(df["Modelo"])):
        send = msg.format(car=df["Modelo"][k])
        r = send_sms("616160778", send)
        credit = int(float(r[0].replace("OK;", "")))

        if credit <= 100:
            if credit == 1:
                print("Te queda solo 1 crédito.")
            elif credit == 0:
                print("Te has quedado sin créditos. Compra más en la página web.")
                break
            else:
                print(f"CUIDADO!!! Te quedan {credit} créditos")
    
if __name__ == "__main__":
    main()
