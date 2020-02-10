import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

ICCV_2019='http://openaccess.thecvf.com/ICCV2019.py'
#GLOVE_FILE = "data/glove.6B/glove.6B.300d.txt"
GLOVE_FILE = "data/glove.6B/glove.6B.50d.txt"

ICCV_2019_MAIN_CONFERENCE="http://iccv2019.thecvf.com/program/main_conference"


def remove_before_colon(title):
    new_title = title
    pos = title.find(":")
    if (pos != -1):
        new_title = title[pos+1:].lstrip()
    return new_title


def preprocess(text):
     new_text = remove_before_colon(text)

     # keep only words
     words_only_text = re.sub("[^a-zA-Z]", " ", new_text)

     # convert to lower case and split
     words = words_only_text.lower().split()

     # remove stopwords
     stopword_set = set(stopwords.words("english"))
     cleaned_words = list(set([w for w in words if w not in stopword_set]))

     return cleaned_words


def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    return model



def get_groups_titles_authors_from_table(table):
    groups = []
    titles = []
    authors = []

    current_group = ""

    rows = table.findAll("tr")
    row_count = len(rows)
    for i in range (2, row_count):
        cells = rows[i].findAll("td")
        group = cells[0].get_text()
        title = cells[3].get_text()
        author = cells[4].get_text()

        if len(group) > 0:
            current_group = group

        groups.append(current_group)
        titles.append(title)
        authors.append(author)

    return groups, titles, authors





def get_iccv_groups_titles_authors(iccv_url):
    page = urllib2.urlopen(iccv_url)
    soup = BeautifulSoup(page,'html.parser')

    tables = soup.find_all('table', {"class":"table program_table"})

    groups = []
    titles = []
    authors = []

    for table in tables:
        table_groups, table_titles, table_authors = get_groups_titles_authors_from_table(table)

    groups.extend(table_groups)
    titles.extend(table_titles)
    authors.extend(table_authors)

    return groups, titles, authors

'''
    dt_ptitle = soup.find_all('dt', {"class":"ptitle"})
    titles = []
    for dt in dt_ptitle:
        t = dt.get_text()
        tt = preprocess(t)
        titles.append(tt)
'''


def get_iccv_titles(iccv_url):
    page = urllib2.urlopen(iccv_url)
    soup = BeautifulSoup(page,'html.parser')

    dt_ptitle = soup.find_all('dt', {"class":"ptitle"})
    titles = []
    for dt in dt_ptitle:
        t = dt.get_text()
        tt = preprocess(t)
        titles.append(tt)
    return titles


def get_glov_embedding_for_title(model, title):
    emb = []
    title_preprocessed = preprocess(title)
    for word in title_preprocessed:
        try:
            word_emb = model[word]
            emb.append(word_emb)
        except:
            print ("No embedding for word " + word)
            continue
    embedding = np.mean(emb)
    return embedding



def get_titles_glov_embeddings(model, titles):
    embeddings = []
    for title in titles:
        emb = get_glov_embedding_for_title(model, title)
        embeddings.append(emb)
    return embeddings



def get_distance_matrix_between_titles(model, titles):
    count = len(titles)
    embeddings = []
    for i in range (count):
        emb = get_embedding_for_title(model, titles[i])
        embeddings.append(emb)
    return embeddings



def heat_map_matrix_between_titles(model, titles):
    distances = get_distance_matrix_between_titles(model, titles)
    return distances


groups , titles, authors = get_iccv_groups_titles_authors(ICCV_2019_MAIN_CONFERENCE)

model = loadGloveModel(GLOVE_FILE)
title_embeddings = get_titles_glov_embeddings(model, titles)

group_count = len(set(groups))
print (group_count)

count = len(groups)

for i in range(count):
    print (groups[i] + " " + titles[i] + " " + authors[i] + " " + str(title_embeddings[i]))
#titles = get_iccv_titles(ICCV_2019)

#model = loadGloveModel(GLOVE_FILE)


#dist = heat_map_matrix_between_titles(model, titles)

#print (dist)