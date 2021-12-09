import smtplib, ssl
import os
import requests
import json

def mandar_correo():
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "kuan1092@gmail.com"
    password = "tyokale45"
    receiver_email = "kuan1092@gmail.com"  # Enter receiver address
    message = """\
    Subject: 

    Hola nicolas"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

ip = requests.get('https://api.ipify.org').content.decode('utf8')
location = requests.get(f'https://ipinfo.io/{ip}?token=0685828d875309').json()
print(ip)
print(location)