#python3 -m venv lab1
#source lab1/bin/activate
#pip install html5lib beautifulsoup requests ipython morkdownify

from bs4 import BeautifulSoup
import requests
import html5lib
#import json
from markdownify import MarkdownConverter




def download(address = 'https://www.tiobe.com/tiobe-index/', path = './../page/doc.html'):
    response = requests.get(address)
    response.encoding = 'utf-8'
    doc = response.text
    with open(path, 'w', encoding="utf-8") as f:
        f.write(doc)

def process(path_original = './../page/doc.html', path_processed = './../page/doc_processed.html'):
    with open(path_original, 'r', encoding="utf-8") as f_html:
        content = f_html.read()

    base = '<!DOCTYPE html><html><head><title>Moja Przetworzona Strona</title></head><body></body></html>'
    out_soup = BeautifulSoup(base, 'html5lib')


    soup = BeautifulSoup(content, 'html5lib')
    tabelka = soup.find('table')
    #dodaje kolumne:
    naglowek = tabelka.thead
    l = naglowek.tr.find_all('th')
    l[0]['style'] = "width: 10%"
    l[1]['style'] = "width: 10%"
    l[2]['style'] = "width: 10%"
    ###TODO
    #soup.new_tag'<th title="Description from Wikipedia" style="width: 15%">Description</th>'
    #naglowek.tr.append()

    #przetwarzam wierszami:
    wiersze = tabelka.tbody.find_all('tr')
    for i in range(len(wiersze)):
        wiersz = wiersze[i]
        l = wiersz.find_all('td')
        nazwa = l[4].string
        print(nazwa)
        nowy_tag = soup.new_tag("a", href = ('../page/' + nazwa))
        nowy_tag.string = "<td>Co to:" + nazwa + "?</td>"
        wiersz.append(nowy_tag)

    print(tabelka)
    # <th title="Description from Wikipedia" style="width: 15%">Description</th>

    # with open(path_processed, 'w', encoding="utf-8") as f:
    #     f.write(out_soup)


def generate_markdown(path_html = './../page/doc_processed.html', path_markdown = './../page/doc.md'):
    # with open(path_html, 'r', encoding="utf-8") as f_html:
    #     content = f_html.read()

    #soup = BeautifulSoup(content, 'html5lib')
    base = '<!DOCTYPE html><html><head><title>Moja Przetworzona Strona</title></head><body></body></html>'
    soup = BeautifulSoup(base, 'html5lib')
    
    md_content = MarkdownConverter().convert_soup(soup)

    with open(path_markdown, 'w', encoding="utf-8") as f_md:
        f_md.write(md_content)
    

address = 'https://www.tiobe.com/tiobe-index/'
download(address)
process()
generate_markdown()
with open('./../page/doc.md', 'r', encoding="utf-8") as f_md:
        content = f_md.read()
        print(content)

# soup = BeautifulSoup(content, 'html5lib')

# for header in soup.find_all(['h1', 'h2', 'h3']):
#     print(header)