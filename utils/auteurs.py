# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 11:39:30 2021

@author: Dao
"""

import re
import numpy as np
import utils.TextRepresenter as tr

class Statement(object):
    def state_traitement(state):
        state = state.lower()
        if re.search("virgi", state):
            return "virginia"
        if re.match("tex", state):
            return "texas"
        if re.match("tennesse", state):
            return "tennesse"
        if re.search("pennsylvania",state):
            return "pennsylvania"
        if re.search("washington",state):
            if re.search("d.c.",state):
                return "washington DC"
            return "washington"
        return state.strip()
    
    def __init__(self,fake_note,
                 statement,subject,auteur,job,state,party,counters,context,
                 sentiment_score,sentiment_magnitude,sentiments,sentiment_code):
        """
        Stock les informations du text dans un dictionnaire "info"
        fake note : true, false, half true, mostly true, pant on fire
        statement : dictionnaire du text
        statement2 : dictionnaire du text traité par PorterStemmer
        counters : 5 valeurs, une part comptage de fake note
        sentiment_score : NEGATIVE ou POSITIVE
        sentiments_magnitude : un réel en str
        sentiments : "anger, fear, joy, disgust, sad"
        sentiment_code : '_NEF_\n' ou '_POS_\n'
        """
        st = filter(acceptable_chars, str.lower(statement))
        st = "".join(st)
        ps = tr.PorterStemmer()
        statement_2 = ps.getTextRepresentation(st) # statement with stem and stopword list
        statement = st.split()
        
        self.info = {"fake_note" : fake_note,
                     "statement" : statement,
                     "statement_2" : statement_2,
                     "subject" : str.lower(subject.replace("\"","")).split(","),
                     "context" : context,
                     
                     "author" : str.lower(auteur).split("-"),
                     "job" : job.replace("\"","").lower(),
                     "state" : Statement.state_traitement(state),
                     "party" : party,
                     "counters" : counters,
                     
                     "sentiment_score" : sentiment_score,
                     "sentiment_magnitude": sentiment_magnitude,
                     "sentiments" : sentiments,
                     "sentiment_code": sentiment_code}
        
        
        
    def length(self):
        return len(self.info["statement"])
    
    def length_stem(self):
        return sum(self.info["statement_2"].values())
    
    def length_unique(self):
        return len(np.unique(self.info["statement"]))
    
    def length_unique_stem(self):
        return len(self.info["statement_2"])

def make_dictio_author(statements, politicians = None):
    """
    Prend une liste de Statement et une liste de Politican.
    Crée deux dictionnaires pour chaque liste rangé par nom
    """
    dictio= {}
    dictio2 = {}
    num = ['true','barely-true', 'false', 'half-true', 'mostly-true', 'pants-fire']
    
    for doc in range(len(statements)):
        if statements[doc].info["job"] != '':
            
            author = " ".join(statements[doc].info['author'])
            try:
                dictio[author]
                
            except KeyError:
                dictio[author] = {}
                dictio[author]["party"] = statements[doc].info["party"]
                dictio[author]["job"]   = statements[doc].info["job"]
                dictio[author]["state"] = statements[doc].info["state"]
                dictio[author]["score"] = np.zeros(6)
                dictio[author]["counter"] = np.float32(statements[doc].info["counters"])
                dictio[author]["news"]  = np.array([], dtype = np.intc)
                        
            n = num.index(statements[doc].info['fake_note'])
            dictio[author]["score"][n] += 1
            dictio[author]["news"] = np.append(dictio[author]["news"], doc)
            
    if politicians:
        for doc in politicians:
            author = " ".join(doc.info.pop('name'))
            dictio2[author] = doc.info
        
    return dictio, dictio2
    
def make_author_database(statements):
    dict_statement, dict_politician = make_dictio_author(statements, None)
    dictio = {'author' : [], 'job' : [], 'state' : [], 'counter' : [],\
              'score' : [], 'nbr_publi' : [], 'party' : []}
    for author, values in dict_statement.items():
        dictio['author'] += [author]
        dictio['job']    += [values['job']]
        dictio['state']  += [values['state']]
        dictio['score']    += [values['score']]
        dictio['counter']    += [values['counter']]
        dictio['nbr_publi'] += [len(values['news'])]
        dictio["party"] += [values['party']]
    
    dictio['score'] = np.array(dictio['score'] ) 
    return dictio

class Politician:
    def __init__(self,name, twitter_username, account_start_time, account_id,
                 sex, birthplace, birthday, age, instagram_username, 
                 political_party):
        
        self.info = {"name" : str.lower(name).split(" "),
                     "twitter" : twitter_username,
                     "account_start_time" : account_start_time,
                     "account_id" : account_id,
                     "sex" : sex,
                     "birthplace" : birthplace,
                     "birthday" : birthday,
                     "age" : age,
                     "instagram_username" : instagram_username,
                     "political_party" : political_party}
        
        
def acceptable_chars(c):
    return str.isalnum(c) or str.isspace(c)

class Traitement:
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
