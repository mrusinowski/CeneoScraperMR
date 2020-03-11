#import bibliotek
import requests
from bs4 import BeautifulSoup

#adres URL przykładowej strony z opiniami
url = "https://www.ceneo.pl/86370800#tab=reviews"

#pobranie kodu HTML strony z podanego URL
page_respons = requests.get(url)
page_tree = BeautifulSoup(page_respons.text, 'html.parser')

#wydobycie z kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
opinions = page_tree.find_all("li", "review-box")

#wydobycie składowych dla pojedynczyej opinii
opinion = opinions.pop()

opinion_id = opinion["data-entry-id"]
author = opinion.find("div", "reviewer-name-line").string
recomendation = opinion.find("div", "product-review-summary").find("em").string
stars = opinion.find("span", "review-score-count").string
pucharsed = opinion.find("div", "product-review-pz").string
# - data wystawienia: span.review-time > time["datetime"] - pierwszy element listy
# - data zakupu: span.review-time > time["datetime"] - drugi element listy
useful = opinion.find("button", "vote-yes").find("span").string
useless = opinion.find("button", "vote-no").find("span").string
content = opinion.find("p", "product-review-body").get_text()
# - wady: div.cons-cell > ul
# - zalety: div.pros-cell > ul