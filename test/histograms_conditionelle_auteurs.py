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

#['true','barely-true', 'false', 'half-true', 'mostly-true', 'pants-fire']

def print_histo(dico, y, order = None, proba = True, fct = np.sum):
    noms = np.unique(dico[y])
    new_dico = {y: list(noms),'true' : [],'barely-true' : [], 'false' :[],\
                'half-true' : [], 'mostly-true' : [], 'pants-fire': []}
    
    num = ['true','mostly-true', 'half-true', 'barely-true', 'false', 'pants-fire']
    for i in noms:
        indice = np.where(np.array(dico[y]) == i)[0]
        score  = dico['score'][indice]
        score  = score[:,[0,4,3,1,2,5]]
        div = 1
        if proba:
            div = np.sum(score)
            
        cum = [0]
        for i in range(6):
            cum += [cum[i] + fct(score[:,i])]
            
        new_dico['true']        += [cum[1]/div]
        new_dico['mostly-true'] += [cum[2]/div]
        new_dico['half-true']   += [cum[3]/div]
        new_dico['barely-true'] += [cum[4]/div]
        new_dico['false']       += [cum[5]/div]
        new_dico['pants-fire']  += [cum[6]/div]
        
    if order:
        sort = np.array([], dtype= np.intc)
        if order in ['pants-fire','false']:
            ran  = range(num.index(order), -1, -1);cond = 1;flip = False
        else :
            ran = range(num.index(order), 6);cond = 0;flip = True
        for i in ran:
            val = np.array(new_dico[num[i]], dtype = np.float32)
            tmp = np.where(val != cond)[0]
            sort_plus =tmp[np.argsort(val[tmp])]
            if flip:
                sort_plus = np.flip(sort_plus)    
            sort = np.concatenate((sort, sort_plus))
            if len(sort) == len(new_dico['true']):
                break
        new_dico['true']        = np.array(new_dico['true'])[sort]
        new_dico['mostly-true'] = np.array(new_dico['mostly-true'])[sort] 
        new_dico['half-true']   = np.array(new_dico['half-true'])[sort] 
        new_dico['barely-true'] = np.array(new_dico['barely-true'])[sort] 
        new_dico['false']       = np.array(new_dico['false'])[sort]
        new_dico['pants-fire']  = np.array(new_dico['pants-fire'])[sort] 
        new_dico[y] = np.array(new_dico[y], dtype = np.str)[sort]
        
    #sns.set_color_codes("pastel")
    sns.barplot(y =y, x="pants-fire",  data=new_dico,ci = None, orient = 'h',\
                label="Pants on fire", color = (1, 0, 0))
    sns.barplot(y=y, x="false",  data=new_dico,ci = None, orient = 'h',\
                label="False",         color=(0.8, 0.25, 0.25))
    sns.barplot(y=y, x="barely-true", data=new_dico,ci = None, orient = 'h',\
                label="Barely true", color=(0.85, 0.5, 0.5))
    sns.barplot(y=y, x="half-true",  data=new_dico,ci = None, orient = 'h',\
                label="Half true", color=(0.5, 1, 0.5))
    sns.barplot(y=y, x="mostly-true", data=new_dico,ci = None, orient = 'h',\
                label="Mostly true", color=(0.4, 0.8, 0.4))
    sns.barplot(y=y, x="true",  data=new_dico,ci = None, orient = 'h',\
                label="True", color=(0.1, 0.8, 0.1))

def affiche(cond, order, title = ''):
    """
    Cond  : variable conditionnelle pour un auteur (state, party, job, nbr_publi)
    Order : Trie les diagrammes par ordre croissants de valeurs 'true', 
            'mostrly-true', half-true', half-true,'false', pants-fire
    title : Titre de Cond pour le titre du graphique et le label y
    """
    plt.rcdefaults()
    sns.set_theme()
    fig, ax = plt.subplots(1,1, figsize = (15,20))
    print_histo(dico,cond, order = order)
    ax.set_title("Distribution des scores des messages par {}".format(title))
    ax.set_ylabel(title)
    ax.set_xlabel("Pourcentage de messages")
    ax.legend()
    plt.show()

affiche('party', 'false', 'parties politiques')
affiche('state', 'half-true', 'états des USA')
affiche('nbr_publi', 'half-true', 'Nombre de publication')

plt.rcdefaults()
sns.set_theme()
fig, ax = plt.subplots(1,1, figsize = (10,1))
s = np.cumsum(np.sum(dico['score'], axis = 0)).reshape(-1,1)
sns.barplot(data = s[-1],ci = None, orient = 'h',\
            label="Pants on fire", color = (1, 0, 0))
sns.barplot(data = s[4],ci = None, orient = 'h',\
            label="False",         color=(1, 0.25, 0.25))    
sns.barplot(data = s[3],ci = None, orient = 'h',\
            label="Barely true", color=(1, 0.5, 0.5))    
sns.barplot(data = s[2],ci = None, orient = 'h',\
            label="Half true", color=(0.5, 1, 0.5))    
sns.barplot(data = s[1],ci = None, orient = 'h',\
            label="Mostly true", color=(0.4, 0.8, 0.4))
sns.barplot(data = s[0],ci = None, orient = 'h',\
            label="True", color=(0.1, 0.8, 0.1))
plt.show()