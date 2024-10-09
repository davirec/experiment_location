from bs4 import BeautifulSoup as bs
from requests import get
import unicodedata
import re

# pip install beautifulsoup4
# pip install requests

# source ~/projetos_git/live-de-python/codigo/env/bin/activate

err = []

#
def load_url_parser(url):
    """Carrega o parse do site."""
    site = get(url)
    return bs(site.text, 'html.parser')


def tratar_string(text):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', text)
    tratamento01 = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', tratamento01)


def link_app(url_programa):
    """Retorna o nome do aplicativo, a descrição e o link para download."""
    print(url_programa)
    try:
        page = load_url_parser(url_programa)
        boxes = page.find('p', {'class': 'package-version-download'})
        pkg = page.find('h3', {'class': 'package-name'}).text.strip()
        desc1 = page.find('div', {'class': 'package-description'}).text.strip()
        # desc = tratar_string(desc1)
        link = boxes.find('a').get('href')
        requirement = page.find('p', {'class': 'package-version-requirement'}).text.strip()
        source_code, issue_tracker = link_package(page.find('ul', {'class': 'package-links'}))
        version = page.find('li', {'id': 'latest'}).findAll('a')[1].get('name')

        permission_list = page.find('li', {'id': 'latest'}).findAll('div', {'class': 'permission-label'})
        permission = ''
        for p in permission_list:
            permission += p.text.replace('\n', '').replace('\t', '').strip() + ' <-> '


        return pkg, url_programa, link, requirement, source_code, issue_tracker, version, permission
    except AttributeError:
        print('erro')
        err.append((page, url_programa))


def link_package(html):
    """Recupera o link do projeto."""
    source_code, issue_tracker = None, None
    for ref in html.find_all('a'):
        if ref.text == "Source Code":
            source_code = ref.get('href')
        if ref.text == "Issue Tracker":
            issue_tracker = ref.get('href')
    return source_code, issue_tracker

def web_crawling_page(links, name):

    with open(f'{name}.csv', 'w') as f:
        # f.write(json.dumps(lista_app))
        for app in links:
            try:
                pkg, url_programa, link, requirement, source_code, issue_tracker, version, permission = link_app(app)
                f.write("{};{};{};{};{};{};{};{}\n".format(pkg, url_programa, link, requirement, source_code,
                                                            issue_tracker, version, permission))
            except TypeError:
                print('erro')

def load_list(file):
    f = open(file, 'r')
    links = []
    for linha in f.readlines():
        links.append(linha.strip())
    f.close()
    return links




web_crawling_page(load_list("list.txt"), "apks")


