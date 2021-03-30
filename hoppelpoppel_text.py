# This is the children's story "Hoppelpoppel - wo bist du" by my most favourite author from the last years, Hans Fallada
# as a preparation for a visualization in Tableau.

import pandas as pd
import numpy as np
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from itertools import chain
import re

# Scraping story text

my_url = 'https://www.projekt-gutenberg.org/fallada/hoppelpo/chap001.html'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'html.parser')

container = page_soup.find_all('p')
container = container[0]

title = container.find_all('h3')
title = str(title[0])

story = container.find_all('p')
paragraphs = []
for i in story:
    paragraphs.append(str(i))

for i in range(len(paragraphs)):
    paragraphs[i] = paragraphs[i].replace('<p>', '')
    paragraphs[i] = paragraphs[i].replace('</p>', '') 

words = []
try:
    for i in range(len(paragraphs)):
        for j in range(len(paragraphs[i])):
            words.append(paragraphs[j].split(' ')) 
except:
    pass

# Flatten nested lists in words

words = list(chain.from_iterable(words))

for i in range(len(words)):
        words[i] = words[i].strip()
        words[i] = words[i].replace('\xa0...', '')
        words[i] = words[i].replace('<a', '')
        words[i] = words[i].replace('</a>', '')
        words[i] = words[i].replace('\n', '')
        words[i] = words[i].replace('-', '')
        words[i] = words[i].replace('–', '')
        words[i] = words[i].replace('.', '')
        words[i] = words[i].replace(':', '')
        words[i] = words[i].replace(',', '')
        words[i] = words[i].replace('>', '')
        words[i] = words[i].replace('<', '')
        words[i] = words[i].replace('›', '')
        words[i] = words[i].replace('‹', '')
        words[i] = words[i].replace('?', '')
        words[i] = words[i].replace('!', '')
        words[i] = words[i].replace('«', '')
        words[i] = words[i].replace('»', '')
        words[i] = words[i].replace('(', '')
        words[i] = words[i].replace(')', '')
        words[i] = words[i].replace(' ', '')
        words[i] = re.sub(str('id='+'"'+'page\d'+'"'), '', words[i])
        words[i] = re.sub(str('name='+'"'+'page\d'+'"'), '', words[i])

        # Remove empty strings in words

while("" in words) :
    words.remove("")

df = pd.DataFrame(words)

df.reset_index(inplace = True)

df.columns = ['rank', 'text']
df['text2'] = ''

# Cleaning last HTML code

part1 = df[df.text == 'title="Dieter7/lac"']
part2 = df[df.text == 'title="suru/Dieter7"']
part3 = df[df.text == 'title="lac/Dieter7"']
eraser = pd.concat([part1, part2, part3])

erank = []
for i in range(len(eraser)):
    erank.append(int(eraser.index[i]))

for i in erank:
    df = df.drop([i])

df.reset_index(drop = True, inplace = True)

df = df.drop('rank', axis = 1)

df.reset_index(inplace = True)

df.columns = ['rank', 'text', 'text2']

# Fill 'text2' with text from previous row

for i in range(len(df)-1):
    if i < len(df):
        try:
            df['text2'][i] = df.text[i+1] 
        except:
            pass

df['text3_lowercase'] = df.text.str.lower()

# Setting for displaying the full dataframe 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Creating a dataframe with German words in lowercase for count of unique values

df2 = pd.Series(df.text3_lowercase.unique())
df2 = pd.DataFrame(df2)

df2.columns = ['text_unique']
df2['count_text'] = ''

# Counting the unique words

for i in range(len(df2)):
    x = df2.text_unique[i]      # x stores each single word in text_unique
    df2['count_text'][i] = df[df.text3_lowercase == x].text3_lowercase.count()

df['count_text'] = ''
df['lat'] = ''
df['lon'] = ''
df['path_ID'] = ''
df['path_start_end'] = ''

for i in range(len(df2)):
    x = df2.text_unique[i]
    for j in range(len(df)):
        if df.text3_lowercase[j] == x:
            df['count_text'][j] = df2.count_text[i] 

df.to_csv('fallada_hoppelpoppel.csv')



