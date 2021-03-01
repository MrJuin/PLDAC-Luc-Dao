# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:35:35 2021

@author: Luc
"""


from auteurs import Traitement
import numpy as np

file1 = open("./data/test_final.csv", encoding="utf8")
file2 = open("./data/valid_final.csv", encoding="utf8")
file3 = open("./data/train_final.csv", encoding="utf8")

politicians_info = open("./data/dataset.xls", encoding="utf8")

content = file3.read() + "\n" + file2.read() + "\n" + file3.read()
content2 = politicians_info.read()

col = Traitement.text_traitement(content)
col_author = Traitement.author_traitement(content2)


# dictionnaire des auteurs avec leur nombre de messages
auteur_dic = dict()
party_dic = dict()
job_dic = dict()

for doc in col:
    try:
        auteur_dic[" ".join(doc.info["author"])]+=1
    except KeyError:
        auteur_dic[" ".join(doc.info["author"])]=1
        try:
            party_dic[doc.info["party"]]+=1
        except KeyError:
            party_dic[doc.info["party"]]=1
        if doc.info["job"]!="":
            try:
                job_dic[doc.info["job"]]+=1
            except KeyError:
                job_dic[doc.info["job"]]=1
     
print(party_dic)
print("\nMean of the number of message of authors {} (variance {})"\
      .format(np.mean(list(auteur_dic.values())),np.var((list(auteur_dic.values())))))
# on trie les personnes qui appairessent plusieurs fois
minimal_message = 1
authors = np.array(list(auteur_dic.items()))
interesting_authors = authors[np.intc(authors[:,1]) >= minimal_message]
print("number of author with at least",minimal_message,"messages:",len(interesting_authors))

# on regarde ceux dans la seconde base de donnée

match = dict()
for i,[x,_] in enumerate(interesting_authors):
    for j,author in enumerate(col_author):
        same = 0
        for v1 in x.split(" "):
            for v2 in author.info["name"]:
                if v1==v2: same+=1
        if same >= 2:
            try:    
                match[i]+=[j]
            except KeyError:
                match[i]=[j]
                
print("number of author found in our database of authors :",len(match))

# on regare le nombre de messages perdus
taille = len(col)
col = [x for x in col if " ".join(x.info["author"]) in interesting_authors] 
print("number of messages :",len(col))
print("loss of",taille-len(col),"messages")
            
# moyenne de taille en nombre de mots des messages
mean_length = []
mean_length_stem = []
mean_length_uniq = []
mean_length_uniq_stem = []
for doc in col:
    mean_length+=[doc.length()]
    mean_length_uniq+=[doc.length_unique()]
    mean_length_stem+=[doc.length_stem()]
    mean_length_uniq_stem+=[doc.length_unique_stem()]

mean_length = np.array(mean_length)
mean_length_stem = np.array(mean_length_stem)
mean_length_uniq = np.array(mean_length_uniq)
mean_length_uniq_stem = np.array(mean_length_uniq_stem)

print("mean length :",mean_length.mean(),"variance (",mean_length.var(),")")
print("mean length with différent words :",mean_length_uniq.mean(),"variance (",mean_length_uniq.var(),")")
print("with stem and stopword list:")
print("mean length :",mean_length_stem.mean(),"variance (",mean_length_stem.var(),")")
print("mean length with différent words :",mean_length_uniq_stem.mean(),"variance (",mean_length_uniq_stem.var(),")")


# dictionnaire des mots
words_dic = dict()
fake_dic = dict()
neg_pos_dic = dict()
sentiments = np.array([0,0,0,0,0])
for doc in col:
    words = doc.info["statement"]
    for word in words:
        try:
            words_dic[word]+=1
        except KeyError:
            words_dic[word]=1
    try:
        fake_dic[doc.info["fake_note"]]+=1
    except KeyError:
        fake_dic[doc.info["fake_note"]]=1
    try:
        neg_pos_dic[doc.info["sentiment_code"]]+=1
    except KeyError:
        neg_pos_dic[doc.info["sentiment_code"]]=1
    sentiments = sentiments + np.float64(doc.info["sentiments"])

sentiments /= len(col)


print("number of different words :",len(words_dic))

print("labels")
for x,y in fake_dic.items():
    print(x,":",y,"(",(y/len(col))*100,"%)")

# les labels positif/négatif
print("positive/negative label")
for x,y in neg_pos_dic.items():
    print(x,":",y,"(",(y/len(col))*100,"%)")

# les scores de sentiments
print("sentiment score mean (anger,fear,joy,disgust,sad):")
print(sentiments)

subject_dic = dict()
for doc in col:
    for s in doc.info["subject"]:
        try:
            subject_dic[s]+=1
        except KeyError:
            subject_dic[s]=1
            
print("number of subject :",len(subject_dic))

tmp = np.array(list(subject_dic.values()))
print("number of subject with at least 5 messages:",len(np.where(tmp>=5)[0]))
print("mean and variance of messages by subject :",tmp.mean(),"(variance",tmp.var(),")")

# les jobs
print("nombre de jobs différents",len(job_dic))
tmp = np.array(list(job_dic.values()))
print("moyenne du nombre de personnes par job",tmp.mean(),"(ecart type",tmp.std(),")")
print("nombre de job avec au moins 5 personnes",len(np.where(tmp>=5)[0]))