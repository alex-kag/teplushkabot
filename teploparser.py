import requests
from datetime import datetime, timedelta

def validator(valuegroup):
    current_datetime_to_compare = datetime.now() - timedelta(minutes=20)
    value_datetime = datetime.strptime(valuegroup['timestamp'], '%Y-%m-%dT%H:%M:%S.%f+00:00') + timedelta(hours=3)
    if value_datetime > current_datetime_to_compare:
        return f'{valuegroup["value"]}'
    else:
        return f'<s>{valuegroup["value"]}</s>'


def getDataFromServer(url):
    result = requests.get(url)
    current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    rezout = f"Данные теплосети по состоянию на {current_datetime} \n\n"
    if result.status_code == 200:
        rezout += f"G ТЭЦ Город прм {validator(result.json()['1S0P003'])}\n"
        rezout += f"G ТЭЦ Город обр {validator(result.json()['1S0P004'])}\n"
        rezout += f"G ТЭЦ Аэропорт прм {validator(result.json()['1S0P200'])}\n"
        rezout += f"G ТЭЦ Аэропорт обр {validator(result.json()['1S0P201'])}\n"
        rezout += f"G подпитки ТЭЦ {validator(result.json()['1S0P160'])}\n"
        rezout += f"G Мариненко КСТЫ прм {validator(result.json()['2S0P010'])}\n"
        rezout += f"G Мариненко КСТЫ обр {validator(result.json()['2S0P011'])}\n"
        rezout += f"G Аэропорт КСТЫ прм {validator(result.json()['2S0P030'])}\n"
        rezout += f"G подпитки 50 КСТЫ {validator(result.json()['2S0P090'])}\n"
        rezout += f"G подпитки 80 КСТЫ {validator(result.json()['2S0P050'])}\n"
    return rezout

