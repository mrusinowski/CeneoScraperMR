#import bibliotek
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

#wyświetlenie zawartości katalogu z opiniami
print(*os.listdir("./opinions.json"))

#wczytywanie identyfikatora produktu, którego opinie będą analizowane
product_id = input("Podaj kod produktu: ")

#wczytywanie z ramki danych opinii z pliku
opinions = pd.read_json("./opinions_json/"+product_id+'.json')
opinions = opinions.set_index("opinion_id")

#częstość występowania poszczególnej liczby gwiazdek
starts = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0, 5.1, 0.5)), fill_value=0)
fig, ax = plt.subplots()
stars.plot.bar(color="deepskyblue")
plt.xticks(rotation=0)
ax.set_title("Częstość występowania poszczególnych ocen")
ax.set_xlabel("Liczba gwiazdek")
ax.set_ylabel("Liczba opinii")
plt.savefig("./figures_png/"+product_id+'_bar.png')
plt.close()

#udział poszczególnych rekomendacji w ogólnej liczbie opinii
recommendation = opinions["recommendation"].value.counts()
fig, ax = plt.subplots()
recommendation.plot.pie(label="", autopct="%.1f%%", colors=['mediumseagreen', 'coral'])
ax.set_title("Udział poszczególnych rekomendacji w ogólnej liczbie opinii")
plt.savefig("./figures_png/"+product_id+'_pie.png')
plt.close()

#podstawowe statystyki
stars_average = opinions["stars"].mean()
pros = opinions["pros"].count()
cons = opinions["cons"].count()
pucharsed = opinions["pucharsed"].sum()
print(stars_average, pros, cons, pucharsed)

stars_pucharsed = pd.crosstab(opinions["stars"], opinions["pucharsed"])
print(stars_pucharsed)