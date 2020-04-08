#import bibliotek
import os
import pandas as pd

#wyświetlenie zawartości katalogu z opiniami
print(*os.listdir("./opinions.json"))

#wczytywanie identyfikatora produktu, którego opinie będą analizowane
product_id = input("Podaj kod produktu: ")

#wczytywanie z ramki danych opinii z pliku
opinions = pd.read_json("./opinions_json/"+product_id+'.json')

print(opinions)