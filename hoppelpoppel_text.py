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

    



