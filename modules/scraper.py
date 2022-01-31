import os
import re
import time
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

url = "https://es.wallapop.com/app/search?category_ids=100&filters_source=quick_filter&order_by=newest&min_year=2004&max_year=2007"

def scrape(url):
    try:
        session = HTMLSession()
        headers = {
        "Host": "es.wallapop.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "device_id=9b249ce7-f164-46ae-add4-079faeec0138; G_ENABLED_IDPS=google; _ga=GA1.2.1963269864.1643475620; _gid=GA1.2.1073399199.1643475620; _ga=GA1.3.1963269864.1643475620; _gid=GA1.3.1073399199.1643475620; cto_bundle=PfRFwF9hcUFVdzRGbkJQWENKQTIyTjR5NmJNd01nUkZIWENMZG9BZkJraUdLWFRjcWthTyUyRmlxbmhXRE16cmVQWHFGcXlMTTRQN1F0c3VRcU12ZyUyQkNmYWY0UmhLUzY0U0p6MEV2SGklMkZQcmVSbCUyQmlUZGVycG9jN1VHQ0xTN2FhZEQ0ZkdHUkhKOHpzJTJCNEVtcW92U0JLN3V0TU5nJTNEJTNE; _pin_unauth=dWlkPVkyUmhORFUxTWpBdFkyRmpOeTAwTmpVMkxXRTNNak10WldFeU5tRmxObU0xTlRVeg; _hjSessionUser_680614=eyJpZCI6IjkwMGNkOThkLTE4MTQtNTA0Mi05NGQxLTAxZTY4NzczOTRiYiIsImNyZWF0ZWQiOjE2NDM0NzU2MzA3NDMsImV4aXN0aW5nIjp0cnVlfQ==; __stripe_mid=d963376f-18f9-48e7-a435-8e975e17f11fd87168; content=iphone%20roto; MwebSearchLayout=old; wallapop_keep_session=true; _hjSession_680614=eyJpZCI6IjM2NDQ0ODM4LTIyZjgtNDg5MS05MDU5LTllYzRhNzljODY2NyIsImNyZWF0ZWQiOjE2NDM1NjA3MzY3MzQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjIncludedInSessionSample=0; __stripe_sid=dd534f00-278a-4440-8a46-22fd99b29b19f345d1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "If-Modified-Since": "Fri, 28 Jan 2022 12:03:03 GMT",
        "If-None-Match": 'W/"ec485ed01da5bcccb48a2d0c753722f5"',
        "Cache-Control": "max-age=0",
        "TE": "trailers"
        }

        page = session.get(url)
        page.html.render()

        html = page.html.html
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all("a", class_="ItemCardList__item")

        with open("file.txt", "w+") as file:
            file.write(html)

        # Find Info
        title = [x.find("span", class_="ItemCardWide__title d-inline-block text-truncate w-100").getText() for x in cards]
        title = [" ".join(x.split()) for x in title]
        title = [re.sub(r'(?<=[^\d])\.(?=[^\d])?', '', x) for x in title]

        data = [list(map(lambda x: x.getText(), \
            x.find("div", class_="ItemExtraInfo d-flex"))) for x in cards]

        price = [x.find("span", class_="ItemCardWide__price ItemCardWide__price--bold").getText() for x in cards]

        # To find the url to each advertisement we generate it using the id (found in the image of the ad) and the title
        id = re.findall(r'"https://cdn.wallapop.com/images(.+?)"', html)
        id = list(map(lambda x: re.search(r'c10420p(.+?)\/i', x).group(1), id))
        
        ad_url = ["https://es.wallapop.com/item/" + x[0].lower().replace(" ","-") + "-" + x[1] for x in zip(title, id)]

        # Now we scrape the pones from the ad_url list
        r = requests.get()

        # End session
        r = session.post(url=url, headers={'Connection':'close'})

    except:
        print("error")
        time.sleep(3)
        scrape(url)
    
scrape(url)
print(f"\n{url}")
    


