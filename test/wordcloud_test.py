# -*- coding: utf-8 -*-


# Python program to generate WordCloud 
  
# importing all necessery modules 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import utils.porter as porter
  
# Reads 'Youtube04-Eminem.csv' file  
df = pd.read_csv(r"../data/train_final.csv", encoding ="latin-1") 
  
comment_words = '' 
stopwords = set(STOPWORDS)
stopwords.add("say")
stopwords.add("says")
stopwords.add("people")
stopwords.add("u")
stopwords.add("s")
stopwords.add("percent")
stopwords.add("one")
stopwords.add("million")
stopwords.add("billion")
stopwords.add("will")
 
subject_v = "ethics" # le sujet à traiter "" si aucun
# iterate through the csv file 
for val,subject in zip(df.statement,df.subject):

    subjects = str.lower(subject.replace("\"","")).split(",")
    if not subject_v or subject_v in subjects:
        # typecaste each val to string 
        val = str(val) 
  
        # split the value 
        tokens = val.split() 
      
        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower()
      
        comment_words += " ".join(tokens)+" "
  
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(comment_words) 
  
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 
