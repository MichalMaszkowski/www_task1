#python3 -m venv lab1
#source lab1/bin/activate
#pip install html5lib beautifulsoup requests ipython morkdownify
#pip install -U duckduckgo_search

from bs4 import BeautifulSoup
import requests
import html5lib
#import json
#from markdownify import MarkdownConverter
from mdutils import MdUtils
import wikipediowanie




def download(address = 'https://www.tiobe.com/tiobe-index/', path = '../tiobe.html'):
    response = requests.get(address)
    response.encoding = 'utf-8'
    doc = response.text
    with open(path, 'w', encoding="utf-8") as f:
        f.write(doc)

def scrap(path_original = '../tiobe.html'):
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


text = """One can wonder what are the most popular programming languages and what \
are their characcteristics. For each of those questions there are websites \
trying to answer it. Below you can find a link to a website compiling that \
information. It's based on the data from 
[https://www.tiobe.com/tiobe-index/](https://www.tiobe.com/tiobe-index/) \
for the relative language popularity and on the wikipedia for the short descriptions \
of respective languages that you can navigate from the table you can find \
[here](./table.md)"""

def generate_index():
    mdFile = MdUtils(file_name='../index', title='1. zadanie z www')
    mdFile.new_header(level=1, title='What it is about')  # style is set 'atx' format by default.
    
    mdFile.new_paragraph(text)

    mdFile.create_md_file()
    return


def generate_table():
    nazwy, obrazki, procenty = scrap()

    #stworzenie opisow:
    ile_jezykow = len(nazwy)
    for i in range(ile_jezykow):
        wikipediowanie.create_description(nazwy[i], (i + 1))


    mdFile = MdUtils(file_name='../table',title='Popularity table')
    #tabelka:
    list_of_strings = ["Index", "Language", "Logo", "Popularity", "Description"]
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
download(address)
generate_index()
generate_table()