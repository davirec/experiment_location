from collections import namedtuple
from bs4 import BeautifulSoup as bs
from requests import get
import unicodedata
import re

# pip install beautifulsoup4
# pip install requests

# source ~/projetos_git/live-de-python/codigo/env/bin/activate


# app = namedtuple('Vaga', 'Titulo empresa tipo local')
# base_url = 'https://f-droid.org'
# packages = f'{base_url}/en/packages'
err = []

#
def load_url_parser(url):
    """Carrega o parse do site."""
    site = get(url)
    return bs(site.text, 'html.parser')


# def list_categorias(url):
#     """Listar as categorias de aplicativos."""
#     fdroid_page = load_url_parser(url)
#     boxes = fdroid_page.find_all('div', {'class': 'post-content'})
#     cat = [c.text for c in boxes[0].find_all('h3')]
#     cat_page = boxes[0].find_all('p')
#     page = ["{}{}".format(base_url, s.find('a').get('href')) for s in cat_page]
#     return cat, page


# def extract_url(html):
#     package_list1 = html.find('div', {'id': 'package-list'})
#     pakage_list = package_list1.find_all('a', {'class': 'package-header'})
#     url_page = ["{}{}".format(base_url, s.get('href')) for s in pakage_list]
#     return url_page

# def list_page_app(url_categoria):
#     """Lista os aplicativos da categoria."""
#     fdroid_page = load_url_parser(url_categoria)
#
#     n_pages = int(fdroid_page.find_all('a', {'class': 'label'})[-2].text)
#     page = extract_url(fdroid_page)
#     for n in range(2, n_pages+1):
#         n_page = load_url_parser("{}/{}/index.html".format(url_categoria, n))
#
#         page.extend(extract_url(n_page))
#     return page


# def list_page_simples(url):
#     """Lista os aplicativos da categoria."""
#     fdroid_page = load_url_parser(url)
#     pakage_list = fdroid_page.find_all('a', {'class': 'post-link'})
#
#     page = ["https://f-droid.org{}".format(s.get('href')) for s in pakage_list[:-5]]
#
#     for n in range(2, 50):
#         n_page = load_url_parser(f'{url}{n}')
#         next_page = stop_next_page(n_page)
#         n_pakage_list = n_page.find_all('a', {'class': 'post-link'})
#         n_page = ["https://f-droid.org{}".format(s.get('href')) for s in n_pakage_list[:-5]]
#         page.extend(n_page)
#         print(f'{url}{n}')
#
#         if next_page:
#             break
#
#     return page


# def stop_next_page(n_page):
#     ul_element = n_page.find_all('ul')[0]
#     li_elements = ul_element.find_all('li')
#     # Conta o número de <li> elementos
#     if len(li_elements) > 1:
#         return False
#     else:
#         return True


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


# def web_crawling():
#     h3all, hrefall = list_categorias(packages)
#     zn = 0
#     for n in range(zn, len(h3all)):
#         print(h3all[n])
#         a = list_page_app(hrefall[n])
#         # lista_app = [link_app(app) for app in a]
#         with open(f'{h3all[n]}.csv', 'w') as f:
#             # f.write(json.dumps(lista_app))
#             for app in a:
#                 try:
#                     pkg, url_programa, desc, link, requirement, source_code, issue_tracker, version, permission  = link_app(app)
#                     f.write("{};{};{};{};{};{};{};{};{}\n".format(pkg, url_programa, desc, link, requirement, source_code, issue_tracker, version, permission))
#                 except TypeError:
#                     print('erro')


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




web_crawling_page(load_list("list.txt"), "lais")


