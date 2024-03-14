from bs4 import BeautifulSoup
import requests
import html5lib
#import json
from mdutils import MdUtils
from duckduckgo_search import DDGS

def create_description(nazwa, nr):
    query = nazwa + "programming language wikipedia"
    results = DDGS().text(query, region = "us-en", max_results=1)
    url = results[0]['href']

    response = requests.get(url)
    response.encoding = 'utf-8'
    content = response.text
    soup = BeautifulSoup(content, 'html5lib')

    file_path='../page/opisy/jezyk' + str(nr)
    mdFile = MdUtils(file_path, title=nazwa)


    p = soup.find(id="mw-content-text").find_all('p')[1]
    paragraf = p.get_text()
    mdFile.new_paragraph(paragraf)
    p = p.next_sibling
    while(p.name == 'p' or p.name == 'ul'):
        paragraf = p.get_text()
        mdFile.new_paragraph(paragraf)
        p = p.next_sibling

    md_content = mdFile.create_md_file()
    # path = '../page/jezyk' + str(nr) + '.md'
    # with open(path, 'w', encoding="utf-8") as f:
    #     f.write(md_content)
    
    print(url)
