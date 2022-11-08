import csv
import os
from pickle import TRUE
import requests
import re

albumi_url = r'https://github.com/JasaPavcic/Najboljsi-svetovni-albumi.git'
ime_file = '500_najboljših_albumov.html'
ime_mape = 'Albumi'


    #-------------------shranim URL link kot tekstovno datoteko

def url_v_niz(url):
    try:
        vsebina_strani = requests.get(url)
    except Exception as e:
        print("Napaka pri prenosu: {url} :", e)
        return None
    return vsebina_strani.text

    #-------------------ustvari datoteko, jo poimenuje, in ji dodam se novo tekstovno datoteko

def niz_v_file(text, ime_mape, ime_file):
    os.makedirs(ime_mape, exist_ok=TRUE)
    path = os.path.join(ime_mape, ime_file)
    
    #odprem tekstovno datoteko in na njo zapisem url

    with open(path,'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

    #-------------------shranim stran v lokalno datoteko

def shrani_stran(ime_mape, ime_file):
    url = url_v_niz(albumi_url)
    niz_v_file(url,ime_mape,ime_file)

    #-------------------odprem in preberem file
def preberi_file(ime_mape, ime_file):
    path = os.path.join(ime_mape, ime_file)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

    #------------------razčlenim stran na posamične albume

##r'<div class="c-gallery-vertical__slide-wrapper" data-slide-id="106\d{4}" data-slide-index="0" data-slide-position-display="\d{3}">'
##                   r'(.*?)</div>


def razčleni_stran(stran):
    rx = re.compile(r'.*<div class=".*',
                    re.DOTALL)
    album = re.findall(rx,stran)
    return album


    #-----------------zberem podatke posamičnega albuma

#PRIMER 1: <h2 class="c-gallery-vertical-album__title">Rufus, Chaka Khan, ‘Ask Rufus’</h2>
#PRIMER 2: <span class="c-gallery-vertical-album__number" style="background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);">499</span>
#PRIMER 3: <span class="c-gallery-vertical-album__subtitle-1">ABC, 1977</span>
def podatki_albuma(album):
    rx = re.compile(r'<span class="c-gallery-vertical-album__number" style="background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);">(?P<uvrstitev>)</span>'
                    r'<h2 class="c-gallery-vertical-album__title"> (?P<naslov>) , \'(?P<izvajalec>)\'</h2>'
                    r'<span class="c-gallery-vertical-album__subtitle-1">(?P<založba>) , (?P<izdaja>) </span>')
    podatki = re.search(rx,album)
    slovar_albuma = podatki.groupdict()

    return slovar_albuma

    #----------------preberem podatke posamičnega albuma

def preberi_podatke(ime_mape,ime_file):
    stran = preberi_file(ime_mape,ime_file)
    albumi = razčleni_stran(stran)
    podatki_albuma = [podatki_albuma(albumi) for album in albumi]
    
    return podatki_albuma

def albumi():
    return preberi_podatke(ime_mape, ime_file)

    #---------------funkcija, ki zapiše stvari v csv

def zapiši_csv(imena_stolpcev,vrstice, ime_mape, ime_file):
    os.makedirs(ime_mape,exist_ok =TRUE)
    path = os.path.join(ime_mape, ime_file)
    with open(path, 'w', encoding='utf-8') as csv_file:
        zapisovalnik = csv.DictWriter(csv_file, fieldnames = imena_stolpcev)
        zapisovalnik.writeheader()
        for vrstica in vrstice:
            zapisovalnik.writerow()
    return None

    #----------------ustvarim csv datoteko

def ustvari_csv(albumi, ime_mape, ime_file):
    albumi = TRUE
    assert albumi and (all(j.keys() == albumi[0].keys() for j in albumi))
    zapiši_csv(albumi[0].keys, albumi, ime_mape, ime_file)



def main(redownload=True, reparse=True):

    #------------------shranim glavno stran v datoteko

    shrani_stran(ime_mape, ime_file)

    #------------------preberemo podatke iz lokalne datoteke
    stran = preberi_file(ime_mape,ime_file)


    albumi = razčleni_stran(stran)


    #------------------podatke preberem v lepšo obliko

    albumi_lepsi = [podatki_albuma(albumi) for album in albumi]

    print(albumi_lepsi)

    #------------------podatke shranim v csv

    ustvari_csv(albumi_lepsi, ime_mape, ime_file)

if __name__ == '__main__':
    main()