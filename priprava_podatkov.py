from csv import text
import os
from pickle import TRUE
import requests
import re

albumi_url = r'https://github.com/JasaPavcic/Najboljsi-svetovni-albumi.git'

def url_v_niz(url):
    try:
        vsebina_strani = requests.get(url)
    except Exception as e:
        print("Napaka pri prenosu: {url} :", e)
        return None
    return vsebina_strani.txt


def niz_v_file(url, mapa, ime_mape):
    os.makedirs(mapa, exist_ok=TRUE)
    pot = os.path.join(mapa, ime_mape)

    with open(pot,"w", encoding='utf-8') as file_out:
        file_out.write(url)
    return None


