import re
t = "8.000 Ofertas"
t = re.match(r'[\d+]?\.?\d+', t).group()

print(int(t.replace(",", "").replace(".", "")))