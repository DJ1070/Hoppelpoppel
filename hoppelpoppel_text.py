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





