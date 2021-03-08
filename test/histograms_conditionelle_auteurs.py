# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:05:55 2021

@author: Luc
"""
from utils.auteurs import Traitement
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.auteurs import make_author_database
import seaborn as sns


statement_file1 = open("../data/test_final.csv", encoding="utf8")
statement_file2 = open("../data/valid_final.csv", encoding="utf8")
statement_file3 = open("../data/train_final.csv", encoding="utf8")

politicians_file = open("../data/dataset.xls", encoding="utf8")

content = statement_file3.read() + "\n" + statement_file2.read()\
          + "\n" + statement_file3.read()

content2 = politicians_file.read()
statements = Traitement.text_traitement(content)
politicians = Traitement.author_traitement(content2)

dico = make_author_database(statements)

num = ['true','barely-true', 'false', 'half-true', 'mostly-true', 'pants-fire']


new_dico = {}

new_dico['true_score']   = list(dico['score'][:,[0,4]].sum(axis = 1))
new_dico['neutre_score'] = list(dico['score'][:,[0,1,4,3]].sum(axis = 1))
new_dico['false_score']  = list(dico['score'][:,[2,5]].sum(axis = 1))

new_dico['nb_post'] = list(dico['score'].sum(axis = 1))

new_dico['party'] = dico["party"]


plt.rcdefaults()
sns.set_theme()
fig, ax = plt.subplots(1,1, figsize = (15,10))

sns.set_color_codes("pastel")
sns.barplot(y="party", x="nb_post", data=new_dico,ci = None,orient = 'h', label="false_score", color="r")
sns.barplot(y="party", x="neutre_score", data=new_dico,ci = None, orient = 'h', label="true_score", color="b")
sns.barplot(y="party", x="true_score", data=new_dico,ci = None, orient = 'h', label="neutre_score", color="g")

# Plot the crashes where alcohol was involved

"""
ax.set_yticks(y_pos)
ax.set_yticklabels(name_party[1:], rotation = 0)
ax.set_title("Distribution des auteurs par partie")
"""
ax.set_ylabel("Parties")
ax.set_xlabel("Nombre de message")

ax.legend()
plt.show()
