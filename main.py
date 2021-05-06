from urllib.request import urlopen
import json
from datetime import datetime, date

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
response = urlopen(url)
data_json = json.loads(response.read())

ricoverati_con_sintomi = [[],[]]
terapie_intensive = [[],[]]
totale_positivi = [[],[]]
nuovi_positivi = [[],[]]
date = [[],[]]

for value in data_json:
    data = datetime.fromisoformat(value["data"]).date()

    index = 0 if data < datetime(2021, 2, 24).date() else 1

    if data != datetime(2020, 2, 29).date(): # modo poco elegante per superare l'anno bisestile
        ricoverati_con_sintomi[index].append(value["ricoverati_con_sintomi"])
        terapie_intensive[index].append(value["terapia_intensiva"])
        totale_positivi[index].append(value["totale_positivi"])
        nuovi_positivi[index].append(value["nuovi_positivi"])
        date[index].append(data.strftime("%Y-%m-%d"))

output = {}
output["ricoverati_con_sintomi"] = ricoverati_con_sintomi
output["terapie_intensive"] = terapie_intensive
output["totale_positivi"] = totale_positivi
output["nuovi_positivi"] = nuovi_positivi
output["date"] = date

print(json.dumps(output))
