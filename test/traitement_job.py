from utils.auteurs import Traitement
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.auteurs import make_author_dico, make_author_database
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

dico,_ = make_author_dico(statements)
jobs = np.unique(make_author_database(statements)['job'])

def remove_sym(l):
    return l.replace('-', ' ')

jobs = list(map(remove_sym,jobs))
