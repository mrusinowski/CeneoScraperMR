#import bibliotek
import requests
from bs4 import BeautifulSoup
import json
import pprint

#funkcja do ekstrakcji składowych opinii
def extract_feature(opinion, tag, tag_class, child=None):
    try:
        if child:
            return opinion.find(tag,tag_class).find(child).get_text().strip()
        else:
            return opinion.find(tag,tag_class).get_text().strip()
    except AttributeError:
        return None

tags = {
            "recomendation": ["div", "product-review-summary", "em"],
            "stars": ["span", "review-score-count"],
            "content": ["p", "product-review-body"],
            "author": ["div", "reviewer-name-line"],
            "pros": ["div", "pros-cell", "ul"],
            "cons": ["div", "cons-cell", "ul"],
            "useful": ["button", "vote-yes", "span"],
            "useless": ["button", "vote-no", "span"],
            "purchased": ["div", "product-review-pz", "em"],
        }

#adres URL przykładowej strony z opiniami
url_prefix = "https://www.ceneo.pl"
product_id = input("Podaj kod produktu: ")
url_postfix = "#tab=reviews"
url = url_prefix + "/" + product_id + url_postfix

#pusta lista na wszystkie opinie o produkcie
opinions_list = []

while url:
    #pobranie kodu HTML strony z podanego URL
    page_respons = requests.get(url)
    page_tree = BeautifulSoup(page_respons.text, 'html.parser')

    #wydobycie z kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
    opinions = page_tree.find_all("li", "js_product-review")

    #wydobycie składowych dla pojedynczyej opinii
    for opinion in opinions:
        features = {key:extract_features(opinion, *args)
                    for key, arg in tags.items()}
        features["purchased"] = (features["purchased"]=="Opinia potwierdzona zakupem")           
        features["opinion_id"] = int(opinion["data-entry-id"])
        features["useful"] = int(features["useful"])
        features["useless"] = int(features["useless"])
        features["content"] = features["content"].replace("\n", ", ").replace("\r", ", ")
        features["pros"] = features["pros"].replace("\n", ", ").replace("\r", ", ")
        features["cons"] = features["cons"].replace("\n", ", ").replace("\r", ", ")
        dates = opinion.find("span", "review-time").find_all("time")
        features["opinion_date"] = dates.pop(0)["datetime"]
        try:
            features["purchase_date"] = dates.pop(0)["datetime"]
        except IndexError:
            features["purchase_date"] = None
        
        opinions_list.append(features)

    try:
        url = url_prefix+page_tree.find("a", "pagination__next")["href"]
    except TypeError:
        url = None
    print(url)

with open("./opinions_json/"+product_id+'.json', 'w', encoding="utf-8") as fp:
    json.dump(opinions_list, fp, ensure_ascii=False, indent=4, separators=(',', ': '))

print(len(opinions_list))
# pprint.pprint(opinions_list)