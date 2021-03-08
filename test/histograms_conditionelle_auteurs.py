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
new_dico['true']          = list(dico['score'][:,[0]].sum(axis = 1))
new_dico['mostly-true']   = list(dico['score'][:,[0,4]].sum(axis = 1))
new_dico['half-true']     = list(dico['score'][:,[0,4, 3]].sum(axis = 1))
new_dico['barely-true']   = list(dico['score'][:,[0,4,3,1]].sum(axis = 1))
new_dico['false']         = list(dico['score'][:,[0,4,3,1,2]].sum(axis = 1))
new_dico['pants-fire']    = list(dico['score'].sum(axis = 1))
new_dico['job']           = dico["job"]
new_dico['state']         = dico["state"]
new_dico['nb_post']       = list(dico['score'].sum(axis = 1))
new_dico['party']         = dico["party"]

def print_histo(y):

    
    #sns.set_color_codes("pastel")
    sns.barplot(y, x="pants-fire",  data=new_dico,ci = None, orient = 'h',\
                label="Pants on fire", color = (1, 0, 0))
    sns.barplot(y, x="false",  data=new_dico,ci = None, orient = 'h',\
                label="False",         color=(1, 0.25, 0.25))
    sns.barplot(y, x="barely-true", data=new_dico,ci = None, orient = 'h',\
                label="Barely true", color=(1, 0.5, 0.5))
    sns.barplot(y, x="half-true",  data=new_dico,ci = None, orient = 'h',\
                label="Half true", color=(0.5, 1, 0.5))
    sns.barplot(y, x="mostly-true", data=new_dico,ci = None, orient = 'h',\
                label="Mostly true", color=(0.4, 0.8, 0.4))
    sns.barplot(y, x="true",  data=new_dico,ci = None, orient = 'h',\
                label="True", color=(0.1, 0.8, 0.1))
# Plot the crashes where alcohol was involved

"""
Afficher les états
"""
plt.rcdefaults()
sns.set_theme()
fig, ax = plt.subplots(1,1, figsize = (15,20))
print_histo("party")
ax.set_title("Distribution des auteurs par partie")
ax.set_ylabel("Parties")
ax.set_xlabel("Nombre de message")
ax.legend()
plt.show()


plt.rcdefaults()
sns.set_theme()
fig, ax = plt.subplots(1,1, figsize = (10,1))

#sns.set_color_codes("pastel")
sns.barplot(x="pants-fire",  data=new_dico,ci = None, orient = 'h',\
            label="Pants on fire", color = (1, 0, 0))
sns.barplot(x="false",  data=new_dico,ci = None, orient = 'h',\
            label="False",         color=(1, 0.25, 0.25))    
sns.barplot(x="barely-true", data=new_dico,ci = None, orient = 'h',\
            label="Barely true", color=(1, 0.5, 0.5))    
sns.barplot(x="half-true",  data=new_dico,ci = None, orient = 'h',\
            label="Half true", color=(0.5, 1, 0.5))    
sns.barplot(x="mostly-true", data=new_dico,ci = None, orient = 'h',\
            label="Mostly true", color=(0.4, 0.8, 0.4))
sns.barplot(x="true",  data=new_dico,ci = None, orient = 'h',\
            label="True", color=(0.1, 0.8, 0.1))
plt.show()