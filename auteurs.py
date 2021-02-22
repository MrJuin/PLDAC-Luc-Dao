# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 11:39:30 2021

@author: Dao
"""

import re
import numpy as np
import TextRepresenter as tr

file1 = open("test_final.csv", encoding="utf8")
file2 = open("valid_final.csv", encoding="utf8")
file3 = open("train_final.csv", encoding="utf8")

politicians_info = open("dataset.xls", encoding="utf8")

content = file3.read() + "\n" + file2.read() + "\n" + file3.read()
content2 = politicians_info.read()

class Statement(object):
    def __init__(self,fake_note,
                 statement,subject,auteur,job,state,party,counters,context,
                 sentiment_score,sentiment_magnitude,sentiments,sentiment_code):
        self.fake_note = fake_note
        
        self.statement = filter(acceptable_chars, str.lower(statement))
        self.statement = "".join(self.statement)
        ps = tr.PorterStemmer()
        self.statement_2 = ps.getTextRepresentation(self.statement) # statement with stem and stopword list
        self.statement = self.statement.split()
        
        self.subject = subject.replace("\"","")
        self.subject = str.lower(self.subject).split(",")
        
        self.auteur = str.lower(auteur).split("-")
        
        self.job = job.replace("\"","")
        self.state = state
        self.party = party
        self.counters = counters
        self.context = context
        self.sentiment_score = sentiment_score
        self.sentiment_magnitude = sentiment_magnitude
        self.sentiments = sentiments
        self.sentiment_code = sentiment_code
    def length(self):
        return len(self.statement)
    
    def length_stem(self):
        return sum(self.statement_2.values())
    
    def length_unique(self):
        return len(np.unique(self.statement))
    
    def length_unique_stem(self):
        return len(self.statement_2)
    
    
class Politician:
    def __init__(self,name, twitter_username, account_start_time, account_id,
                 sex, birthplace, birthday, age, instagram_username, 
                 political_party):
        self.name = str.lower(name).split(" ")
        self.twitter = twitter_username
        self.account_start_time = account_start_time
        self.account_id = account_id
        self.sex = sex
        self.birthplace = birthplace
        self.birthday = birthday
        self.age = age
        self.instagram_username = instagram_username
        self.political_party = political_party
    
def acceptable_chars(c):
    return str.isalnum(c) or str.isspace(c)

def text_traitement(content):
    l = 1
    statements = []
    useless = r".*"
    useless_2 = r"([^,]*,[^,]*|[^.]*),\"[^\"]*\","
    note = r",(barely-true|pants-fire|half-true|false|true|mostly-true),"
    statement = "((\"([^\"]*(\"\")*)*\")|([^,\"]*)),"
    subject = r"((\"+[^\"]*\"+)|([^,\"]*)),"
    auteur = r"([^,]*),"
    job = r"((\"([^\"]*(\"\")*)*\")|([^,\"]*)),"
    state = r"((\"+[^\"]*\"+)|([^,\"]*)),"
    party = r"([^,]*),"
    counters = r"([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),"
    context = r"((\"([^\"]*(\"\")*)*\")|([^,\"]*)),"
    sentiment_score = r"([^,]*),"
    sentiment_magnitude = r"([^,]*),"
    sentiments = r"([^,]*),([^,]*),([^,]*),([^,]*),([^,]*),"
    sentiment_code = r"([^,]*)\n"
    
    
    # sentiment_score,sentiment_magnitude,anger,fear,joy,disgust,sad,speaker_id,list,sentiment_code
    for i in re.findall(r"^"+useless +note  +\
                        statement +subject +auteur +\
                        job +state +party +counters +\
                        context +sentiment_score +\
                        sentiment_magnitude +\
                        sentiments +useless_2 + sentiment_code
                        ,content,re.MULTILINE):
        # print(i)
        # 0: fake note
        # 1: statement
        # 6: subject
        # 9: auteur
        # 10: job
        # 15: state
        # 18: party
        # 19-20-21-22-23 : barely_true_counts/false_counts/half_true_counts/mostly_true_counts/pants_on_fire_counts
        # 24 : context
        # 29 : sentiment_score
        # 30 : sentiment_magnitude
        # 31-32-33-34-35 : anger,fear,joy,disgust,sad
        # 37 : sentiment_code
        statements += [
                Statement(
                i[0],i[1],i[6],i[9],i[10],i[15],i[18],
                [i[19],i[20],i[21],i[22],i[23]],i[24],i[29],i[30],
                [i[31],i[32],i[33],i[34],i[35]],i[37])]
        l+=1

    return statements

def author_traitement(content):
    name = r"((\"+[^\"]*\"+)|([^,\"]*)),"
    twitter_username =r"([^,]*),"
    account_start_time = r"([^,]*),"
    account_id = r"([^,]*),"
    sex = r"([^,]*),"
    birthplace = r"([^,]*),"
    birthday = r"([^,]*),"
    age = r"([^,]*),"
    instagram_username = r"([^,]*),"
    political_party = r"([^,]*)\n"
    col = []
    for i in re.findall(r"^"+name+twitter_username+\
                         account_start_time+\
                         account_id+sex+birthplace+\
                         birthday+age+instagram_username+\
                         political_party,content,re.MULTILINE):
         col+=[Politician(i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11])]
    return col

# collection
col = text_traitement(content)
col_author = author_traitement(content2)


# dictionnaire des auteurs avec leur nombre de messages
auteur_dic = dict()
party_dic = dict()
job_dic = dict()

for doc in col:
    try:
        auteur_dic[" ".join(doc.auteur)]+=1
    except KeyError:
        auteur_dic[" ".join(doc.auteur)]=1
        try:
            party_dic[doc.party]+=1
        except KeyError:
            party_dic[doc.party]=1
        if doc.job!="":
            try:
                job_dic[doc.job]+=1
            except KeyError:
                job_dic[doc.job]=1
            
print(party_dic)
print("mean of the number of message of authors",np.array(list(auteur_dic.values())).mean(),"(variance",np.array(list(auteur_dic.values())).var(),")")
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
            for v2 in author.name:
                if v1==v2: same+=1
        if same >= 2:
            try:    
                match[i]+=[j]
            except KeyError:
                match[i]=[j]
                
print("number of author found in our database of authors :",len(match))

# on regare le nombre de messages perdus
taille = len(col)
col = [x for x in col if " ".join(x.auteur) in interesting_authors] 
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
    words = doc.statement
    for word in words:
        try:
            words_dic[word]+=1
        except KeyError:
            words_dic[word]=1
    try:
        fake_dic[doc.fake_note]+=1
    except KeyError:
        fake_dic[doc.fake_note]=1
    try:
        neg_pos_dic[doc.sentiment_code]+=1
    except KeyError:
        neg_pos_dic[doc.sentiment_code]=1
    sentiments = sentiments + np.float64(doc.sentiments)

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
    for s in doc.subject:
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