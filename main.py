from urllib.request import urlopen
import json
import os
from datetime import datetime
from github import Github

covid_values = {
    "2020": {"ric": [], "ter": [], "tot": [], "pos": []},
    "2021": {"ric": [], "ter": [], "tot": [], "pos": []},
    "2022": {"ric": [], "ter": [], "tot": [], "pos": []},
    "2023": {"ric": [], "ter": [], "tot": [], "pos": []}
}


def rolling_mean(array):
    window = 7
    n = len(array)
    rolling_mean_list = []
    for i in range(n - window + 1):
        mean = sum(array[i:i + window]) / window
        rolling_mean_list.append(round(mean))
    return rolling_mean_list


def enrich_data(year, covid_row):
    covid_values[year]["ric"].append(covid_row["ricoverati_con_sintomi"])
    covid_values[year]["ter"].append(covid_row["terapia_intensiva"])
    covid_values[year]["tot"].append(covid_row["totale_positivi"])
    covid_values[year]["pos"].append(covid_row["nuovi_positivi"])


def handler(request):
    url = os.environ.get('DATA_URL')
    git = Github(os.environ.get('GIT_KEY'))
    repo = git.get_repo(os.environ.get('GIT_REPO'))

    response = urlopen(url)
    data_json = json.loads(response.read())

    for value in data_json:
        data = datetime.fromisoformat(value["data"]).date()

        # bad way to avoid leap year problem
        if data != datetime(2020, 2, 29).date():
            if data < datetime(2021, 2, 24).date():
                enrich_data("2020", value)
            elif datetime(2021, 2, 24).date() <= data < datetime(2022, 2, 24).date():
                enrich_data("2021", value)
            elif datetime(2022, 2, 24).date() <= data < datetime(2023, 2, 24).date():
                enrich_data("2022", value)
            else:
                enrich_data("2023", value)

    covid_values["2020"]["pos"] = rolling_mean(covid_values["2020"]["pos"])
    covid_values["2021"]["pos"] = rolling_mean(covid_values["2021"]["pos"])
    covid_values["2022"]["pos"] = rolling_mean(covid_values["2022"]["pos"])
    covid_values["2023"]["pos"] = rolling_mean(covid_values["2023"]["pos"])

    new_data = json.dumps(covid_values)
    content = repo.get_contents("output.json")
    repo.update_file(path=content.path, message="Auto update",
                     content=new_data, sha=content.sha, branch="master")

    return f'OK!'
