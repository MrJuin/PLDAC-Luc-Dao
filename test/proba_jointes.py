# -*- coding: utf-8 -*-

import seaborn as sns
import pandas as pd
from utils.auteurs import Traitement
import matplotlib.pyplot as plt
notes = ['true','mostly-true', 'barely-true', 'half-true', 'false', 'pants-fire']
def make_data(statements):
   dictio = {'subjects' : [], 
             'true_count' : [], 
             'mostly-true_count' : [], 
             'barely-true_count' : [],
             'half-true_count' : [],
             'false_count' : [],
             'pant-on-fire_count' : []
             
             }
   subjects = dict()
   for state in statements:
       subject = state.info['subject']
       for sub in subject:
           if state.info['fake_note'] == 'true':
                try:
                    subjects[sub][0] += 1
                except KeyError:
                    subjects[sub] = [1,0,0,0,0,0]
           elif  state.info['fake_note'] == 'mostly-true':
               try:
                    subjects[sub][1] += 1
               except KeyError:
                    subjects[sub] = [0,1,0,0,0,0]
           elif state.info['fake_note'] == 'barely-true':
                try:
                    subjects[sub][2] += 1
                except KeyError:
                    subjects[sub] = [0,0,1,0,0,0]
           elif state.info['fake_note'] == 'half-true':
                try:
                    subjects[sub][3] += 1
                except KeyError:
                    subjects[sub] = [0,0,0,1,0,0]
           elif state.info['fake_note'] == 'false':
                try:
                    subjects[sub][4] += 1
                except KeyError:
                    subjects[sub] = [0,0,0,0,1,0]
           elif state.info['fake_note'] == 'pant-on-fire': 
               try:
                    subjects[sub][5] += 1
               except KeyError:
                    subjects[sub] = [0,0,0,0,0,1]
   for s,notes in subjects.items():
       dictio['subjects'] += [s]
       dictio['true_count'] += [notes[0]]
       dictio['mostly-true_count']+= [notes[1]] 
       dictio['barely-true_count']+= [notes[2]]
       dictio['half-true_count'] += [notes[3]]
       dictio['false_count'] += [notes[4]]
       dictio['pant-on-fire_count'] += [notes[5]]


   return pd.DataFrame(dictio)

statement_file1 = open("../data/test_final.csv", encoding="utf8")
statement_file2 = open("../data/valid_final.csv", encoding="utf8")
statement_file3 = open("../data/train_final.csv", encoding="utf8")

content = statement_file3.read() + "\n" + statement_file2.read()\
          + "\n" + statement_file3.read()

statements = Traitement.text_traitement(content)

data = make_data(statements)

plt.rcdefaults()
sns.set_theme()
fig, ax = plt.subplots(1,1, figsize = (20,50))

sns.set_color_codes("pastel")
sns.barplot(y="subjects", x="true_count", data=data,ci = None,orient = 'h', label="true", color="green")
sns.barplot(y="subjects", x="mostly-true_count", data=data,ci = None, orient = 'h', label="mostly true", color="lime")
sns.barplot(y="subjects", x="barely-true_count", data=data,ci = None, orient = 'h', label="barely-true", color="mediumspringgreen")
sns.barplot(y="subjects", x="half-true_count", data=data,ci = None, orient = 'h', label="half true", color="b")
sns.barplot(y="subjects", x="false_count", data=data,ci = None, orient = 'h', label="false", color="r")
sns.barplot(y="subjects", x="pant-on-fire_count", data=data,ci = None, orient = 'h', label="pant-on-fire", color="darkred")

# Plot the crashes where alcohol was involved

"""
ax.set_yticks(y_pos)
ax.set_yticklabels(name_party[1:], rotation = 0)
ax.set_title("Distribution des auteurs par partie")
"""
ax.set_ylabel("sujets")
ax.set_xlabel("Nombre de message")

ax.legend()
plt.show()