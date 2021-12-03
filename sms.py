import requests

KEY = "5Zk57EmotZ2Rq4L4z7Lp2zwHZYPzzhcJ"
FROM = "HelpMyCar"
TO = "34616160778"
MESSAGE = "Hola carapedo"

balance = f"http://api.smsarena.es/http/balance.php?&auth_key={KEY}"
sms_url = f"http://api.smsarena.es/http/sms.php?auth_key={KEY}&id=33&from={FROM}&to={TO}&text={MESSAGE}"

bal = requests.get(balance)
sms = requests.get(sms_url)

print(sms, sms.text)
print(bal, bal.text)