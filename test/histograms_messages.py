# -*- coding: utf-8 -*-

from utils.auteurs import Traitement
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
from utils.auteurs import make_dictio
import pandas as pd

def make_dictio_statement(statements):
    """
    Prend une liste de Statement et une liste de Politican.
    Crée deux dictionnaires pour chaque liste rangé par nom
    """
    dictio_subject = {}
    dictio_context = {}
    dictio_fake = {}
    max_sentiment = {}
    sentiment_mean = {}
    
    sent = ["anger","fear","joy","disgust","sad"]
    for x in sent:
        max_sentiment[x] = 0
        sentiment_mean[x] = 0
        
    for doc in range(len(statements)):
        for sub in statements[doc].info["subject"]:
            try:
                dictio_subject[sub] += 1
            except KeyError:
                dictio_subject[sub] = 1
        if statements[doc].info["context"] != "":
            try:
                dictio_context[statements[doc].info["context"]] += 1
            except KeyError:
                dictio_context[statements[doc].info["context"]] = 1
            
        if statements[doc].info["fake_note"] != "":
            try:
                dictio_fake[statements[doc].info["fake_note"]] += 1
            except KeyError:
                dictio_fake[statements[doc].info["fake_note"]] = 1
        sentiments = statements[doc].info["sentiments"]
        for i,s in enumerate(sentiments):
            sentiment_mean[sent[i]] +=float(s)
        argmax = sent[np.argmax(sentiments)]
        max_sentiment[argmax] += 1
        
    for s in sentiment_mean.keys():
        sentiment_mean[s]/=len(statements)
    return dictio_subject, dictio_fake, max_sentiment, sentiment_mean, dictio_context

statement_file1 = open("../data/test_final.csv", encoding="utf8")
statement_file2 = open("../data/valid_final.csv", encoding="utf8")
statement_file3 = open("../data/train_final.csv", encoding="utf8")

politicians_file = open("../data/dataset.xls", encoding="utf8")

content = statement_file3.read() + "\n" + statement_file2.read()\
          + "\n" + statement_file3.read()

content2 = politicians_file.read()

statements = Traitement.text_traitement(content)
politicians = Traitement.author_traitement(content2)

dictio_subject,dictio_fake, max_sentiment, sentiment_mean, dictio_context = make_dictio_statement(statements)
    
dictio_context_inv = {}
for v in dictio_context.values():
    try:
        dictio_context_inv[v] += 1
    except KeyError:
        dictio_context_inv[v] = 1
'''    
# Nbr de messages par theme
plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (10,30))

space = 1
y_pos = np.arange(0,len(dictio_subject)*space,space)
ax.barh(y_pos, list(dictio_subject.values()), color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels( list(dictio_subject.keys()), rotation = 0)
ax.set_title("Distribution des contextes")
ax.set_xlabel("Nombre de messages")
ax.set_ylabel("Sujets")
plt.show()
'''

'''
# Nbr de messages par vérité
plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (15,10))

space = 1
y_pos = np.arange(0,len(dictio_fake)*space,space)
ax.barh(y_pos, list(dictio_fake.values()), color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels( list(dictio_fake.keys()), rotation = 0)
ax.set_title("Distribution des vérités des messages")
ax.set_xlabel("Nombre de messages")
ax.set_ylabel("Vérité des messages")
plt.show()
'''
'''
# Nbr de messages par sentiments dominants
plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (15,10))

space = 1
y_pos = np.arange(0,len(max_sentiment)*space,space)
ax.barh(y_pos, list(max_sentiment.values()), color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels( list(max_sentiment.keys()), rotation = 0)
ax.set_title("Distribution des sentiments dominants des messages")
ax.set_xlabel("Nombre de messages")
ax.set_ylabel("Sentiments dominants")
plt.show()


# moyenne des valeurs par sentiments
plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (15,10))

space = 1
y_pos = np.arange(0,len(sentiment_mean)*space,space)
ax.barh(y_pos, list(sentiment_mean.values()), color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels( list(sentiment_mean.keys()), rotation = 0)
ax.set_title("Moyenne des sentiments")
ax.set_xlabel("Valeurs")
ax.set_ylabel("Sentiments")
plt.show()
'''

# nombre de sujets avec un certain nombre de messages
plt.rcdefaults()
fig, ax = plt.subplots(1,1, figsize = (15,10))

sort = np.argsort(list(dictio_context_inv.keys()))[::-1]
k = np.array(list(dictio_context_inv.keys()))[sort]
v = np.array(list(dictio_context_inv.values()))[sort]
space = 1
y_pos = np.arange(0,len(dictio_context_inv)*space,space)
ax.barh(y_pos, v, color = 'red')
ax.set_yticks(y_pos)
ax.set_yticklabels( k, rotation = 0)
ax.set_title("Nombre de contextes avec un certains nombre de messages associés")
ax.set_xlabel("Nombre de contextes")
ax.set_ylabel("Nombre de messages")
plt.show()