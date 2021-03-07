# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:01:07 2021

@author: Luc
"""
from utils.auteurs import Traitement
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
from utils.auteurs import make_dictio
import pandas as pd

statement_file1 = open("../data/test_final.csv", encoding="utf8")
statement_file2 = open("../data/valid_final.csv", encoding="utf8")
statement_file3 = open("../data/train_final.csv", encoding="utf8")

politicians_file = open("../data/dataset.xls", encoding="utf8")

content = statement_file3.read() + "\n" + statement_file2.read()\
          + "\n" + statement_file3.read()

content2 = politicians_file.read()

statements = Traitement.text_traitement(content)
politicians = Traitement.author_traitement(content2)

dict_statement, dict_politician = make_dictio(statements, politicians)

both = set(dict_statement.keys()).intersection(dict_politician.keys())

dictio = {'author' : [], 'job' : [], 'state' : [], 'true_score' : [],\
          'score' : [], 'nbr_publi' : [], 'party' : []}

for author, values in dict_statement.items():
    dictio['author'] += [author]
    dictio['job']    += [values['job']]
    dictio['state']  += [values['state']]
    dictio['true_score']    += [values['true_score']]
    dictio['score']    += [values['score']]
    dictio['nbr_publi'] += [len(values['news'])]
    dictio["party"] += [values['party']]

dictio['true_score'] = np.array(dictio['true_score']) 
dictio['score'] = np.array(dictio['score'] ) 

_, nbr_fois_job = np.unique(dictio['job'], return_counts = True)
name_state, nbr_fois_state = np.unique(dictio['state'], return_counts = True)
nbr_publi, nbr_fois_publi = np.unique(dictio['nbr_publi'], return_counts = True)
name_party, nbr_fois_party = np.unique(dictio['party'], return_counts = True)

#nbr_fois_state = np.histogram(nbr_fois_state[1:])
nbr_fois_job   = np.histogram(nbr_fois_job, bins = max(nbr_fois_job)-1)
nbr_fois_publi = np.histogram(nbr_fois_publi, bins = max(nbr_fois_publi)//10 -1)


# Nbr de métier par nombre de personne par job

fig, ax = plt.subplots(1,1, figsize=(15,5))
ax.set_yscale('log')
ax.bar(nbr_fois_job[1][:-1]  ,height = nbr_fois_job[0]  , width = 0.5, color = 'red')
ax.set_xticks(nbr_fois_job[1][:-1])

ax.set_title("Histogramme de la répartition du nombre de métier par nombre de personne le possédant dans notre base de donnée en échelle log")
ax.set_xlabel("Nombre de personnes affiliées aux métiers")
ax.set_ylabel("nombre de métiers")
plt.show()

# Nbr de publi par nombre de personne par job
fig, ax = plt.subplots(1,1, figsize=(15,5))
ax.set_yscale('log')
ax.bar(nbr_fois_publi[1][:-1]  ,height = nbr_fois_publi[0]  , width = 10, color = 'red')
#ax.set_xticks(nbr_fois_publi[1][:-1])

ax.set_title("Histogramme de la répartition du nombre de personne par nombre de publication dans notre base de donnée en échelle log")
ax.set_xlabel("Nombre de publications")
ax.set_ylabel("nombre de personnes")
plt.show()


# Nbr de personne par state
plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (10,15))

y_pos = np.arange(len(name_state)-1)
ax.barh(y_pos, nbr_fois_state[1:], color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels(name_state[1:], rotation = 0)
ax.set_title("Distribution des auteurs par états")
ax.set_xlabel("Etats")
ax.set_ylabel("Nombre d'auteurs")


plt.show()

# Nbr de personne par partie politique

plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (10,15))

y_pos = np.arange(len(name_party)-1)
ax.barh(y_pos, nbr_fois_party[1:], color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels(name_party[1:], rotation = 0)
ax.set_title("Distribution des auteurs par états")
ax.set_xlabel("Etats")
ax.set_ylabel("Nombre d'auteurs")

plt.show()
