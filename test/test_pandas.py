# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 10:55:44 2021

@author: Luc
"""
import seaborn as sns
import pandas as pd
from auteurs import Traitement

"""
sns.set_theme(style="darkgrid")
df = sns.load_dataset("penguins")
sns.displot(
    df, x="flipper_length_mm", col="species", row="sex",
    binwidth=3, height=3, facet_kws=dict(margin_titles=True),
)
"""
file1 = open("./data/test_final.csv", encoding="utf8")
file2 = open("./data/valid_final.csv", encoding="utf8")
file3 = open("./data/train_final.csv", encoding="utf8")

politicians_info = open("./data/dataset.xls", encoding="utf8")

content = file3.read() + "\n" + file2.read() + "\n" + file3.read()
content2 = politicians_info.read()

col = Traitement.text_traitement(content)
col_author = Traitement.author_traitement(content2)

dict = {}
for i in col:
    for key, val in i.info.items():
        try:
            dict[key] += [val]
        except:
            dict[key] = [val]
df = pd.DataFrame(data = dict)

sns.set_theme(style="darkgrid")
sns.displot(
    df, x="job", col="fake_note",
    binwidth=3, height=3)