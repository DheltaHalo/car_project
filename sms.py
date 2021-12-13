import requests
import hashlib
import pandas as pd
from time import sleep
from datetime import date, datetime
from tkinter import filedialog
from tkinter import *
from colorama import init, Fore
init()

def get_columns():
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfile(filetypes=[("Excel files", ".xlsx .xls")])

    df = pd.read_excel(path.name)
    tlf = df[["Modelo", "Teléfono"]]

    return tlf

def send_sms(tlf: str, msg: str):
    KEY = "Iq0kBwVCn9ii0ex14w87bA6LRcrl0uod"
    FROM = "HelpMyCar"

    TO = "34" + tlf
    MESSAGE = msg

    date = str(datetime.now())
    hash256 = hashlib.sha256(date.encode('utf-8'))
    val = int.from_bytes(hash256.digest(), 'big')

    balance = f"http://api.smsarena.es/http/balance.php?&auth_key={KEY}"
    sms_url = f"http://api.smsarena.es/http/sms.php?auth_key={KEY}&id={val}&from={FROM}&to={TO}&text={MESSAGE}"

    bal = requests.get(balance)
    sms = requests.get(sms_url)

    return bal.text, sms
    
def main():
    print(Fore.YELLOW + "Seleccione un archivo excel para analizar")
    sleep(1)
    try:
        df = get_columns()
    except KeyError:
        print(Fore.RED + "El archivo que ha intentado abrir no era el correcto.")
        input("Pulse Enter para cerrar.")
        exit()

    msg = 'Hola, estamos interesados en tu coche. Te adelantamos el 60% de su valor y el resto hasta el total cuando se venda. Sin gastos ni comisiones.\n\n'+\
        'Para concretar cantidades, no dude en contactar.\n\n'+\
        'Atentamente,\n\n'+\
        'Alberto Torres\n'+\
        '911229127\n'+\
        '674343184\n'+\
        'www.helpmycar.es\n\n'+\
        'bit.ly/3ysixeb'

    for k in df["Teléfono"]:
        send = msg
        r = send_sms(str(k), send)
        credit = int(float(r[0].replace("OK;", "")))
        print(k)

        if credit <= 100:
            if credit == 1:
                print(Fore.RED + "Te queda solo 1 crédito.")
            elif credit == 0:
                print(Fore.RED + "Te has quedado sin créditos. Compra más en la página web.")
                break
            else:
                print(Fore.LIGHTRED_EX + f"CUIDADO!!! Te quedan {credit} créditos")

    print(Fore.MAGENTA + f"Te quedan {credit} créditos\n")
    print(Fore.CYAN + "El programa ha finalizado.")
    input("Pulse enter para cerrar")
    
if __name__ == "__main__":
    main()
