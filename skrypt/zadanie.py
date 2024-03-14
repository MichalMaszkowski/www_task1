#python3 -m venv lab1
#source lab1/bin/activate
#pip install html5lib beautifulsoup requests ipython morkdownify

from bs4 import BeautifulSoup
import requests
import html5lib
#import json
#from markdownify import MarkdownConverter
from mdutils import MdUtils
import wikipediowanie




def download(address = 'https://www.tiobe.com/tiobe-index/', path = '../page/doc.html'):
    response = requests.get(address)
    response.encoding = 'utf-8'
    doc = response.text
    with open(path, 'w', encoding="utf-8") as f:
        f.write(doc)

def scrap(path_original = '../page/doc.html'):
    with open(path_original, 'r', encoding="utf-8") as f_html:
        content = f_html.read()

    nazwy = []
    obrazki = [] #"https://www.tiobe.com" + "/wp-content/themes/tiobe/tiobe-index/images/Python.png"
    procenty = []

    soup = BeautifulSoup(content, 'html5lib')
    tabelka = soup.find('table')

    #przetwarzam wierszami:
    wiersze = tabelka.tbody.find_all('tr')
    for wiersz in wiersze:
        l = wiersz.find_all('td')
        nazwy.append(l[4].string)
        obrazki.append("https://www.tiobe.com" + ((l[3]).img['src']))
        procenty.append(l[5].string)

    # for n in nazwy:
    #     print(n)
    # for p in procenty:
    #     print(p)
    # for o in obrazki:
    #     print(o)
    return nazwy, obrazki, procenty


def generate_markdown():
    nazwy, obrazki, procenty = scrap()

    #stworzenie opisow:
    ile_jezykow = len(nazwy)
    for i in range(ile_jezykow):
        wikipediowanie.create_description(nazwy[i], (i + 1))


    mdFile = MdUtils(file_name='../page/index',title='Popularne Jezyki')
    #tabelka:
    list_of_strings = ["Miejsce", "Jezyk", "Logo", "Popularność", "Opis"]
    for i in range(ile_jezykow):
        podpis = "Logo " + nazwy[i]
        url_obrazka = obrazki[i]
        obrazek = f'![logo]({url_obrazka} "{podpis}")'
        link_do_opisu = f"[{nazwy[i]}](./opisy/jezyk{(i + 1)}.md)"
        list_of_strings.extend([str(i + 1), nazwy[i], obrazek, procenty[i], link_do_opisu])
    mdFile.new_line()
    mdFile.new_table(columns=5, rows=(1 + ile_jezykow), text=list_of_strings, text_align='center')
    
    md_content = mdFile.create_md_file()
    return
    

address = 'https://www.tiobe.com/tiobe-index/'
#download(address)
scrap()
generate_markdown()