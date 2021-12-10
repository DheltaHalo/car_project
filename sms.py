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
    sleep(3)
    try:
        df = get_columns()
    except KeyError:
        print(Fore.RED + "El archivo que ha intentado abrir no era el correcto.")
        input("Pulse Enter para cerrar.")
        exit()

    msg = 'Hola, somos Automóviles Help My Car.\n\n'+\
        'Como responsable del departamento de compras le informo'+\
        'sobre nuestra Gestión de Venta para el vehículo que tiene anunciado.\n\n'+\
        'HelpMyCar le adelanta de inmediato el 60% del valor del vehículo y el '+\
        'resto hasta el total de su precio, cuando se haga la venta definitiva.\n\n'+\
        'Venderemos el automóvil dentro del margen habitual, de 30 a 40 días, '+\
        'por lo que no se tendría que preocupar de;\n'+\
        'Los trámites de la venta o post-venta.\n'+\
        'Gastos de transferencia e impuestos.\n'+\
        'Responsabilidades como averías, vicios ocultos, etc...\n\n'+\
        'Nuestro compromiso es tan grande que no cobramos nada hasta'+\
        'que su coche se haya vendido, teniendo en cuenta que usted'+\
        'está exento del pago de la comisión.\n\n'+\
        'Para cualquier consulta y concretar cantidades, no dude en'+\
        'ponerse en contacto con nosotros.\n\n'+\
        'Atentamente,\n\n'+\
        'Alberto Torres\n'+\
        '911 229 127\n'+\
        '674 343 184\n'+\
        'www.helpmycar.es\n'+\
        'https://www.dropbox.com/s/6oh80khe8no1adj/HELPMYCAR.mp4?dl=0'

    for k in range(len(df["Modelo"])):
        send = msg
        r = send_sms(str(df["Teléfono"][k]), send)
        credit = int(float(r[0].replace("OK;", "")))

        if credit <= 100:
            if credit == 1:
                print(Fore.RED + "Te queda solo 1 crédito.")
            elif credit == 0:
                print(Fore.RED + "Te has quedado sin créditos. Compra más en la página web.")
                break
            else:
                print(Fore.LIGHTRED_EX + f"CUIDADO!!! Te quedan {credit} créditos")
    print(Fore.CYAN + "El programa ha finalizado.")
    input("Pulse enter para cerrar")
    
if __name__ == "__main__":
    main()
