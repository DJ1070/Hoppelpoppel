{
 "metadata": {
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5-final"
  },
  "orig_nbformat": 2,
  "kernelspec": {
   "name": "python3",
   "display_name": "Python 3.8.5 64-bit (conda)",
   "metadata": {
    "interpreter": {
     "hash": "b3ba2566441a7c06988d0923437866b63cedc61552a5af99d1f4fb67d367b25f"
    }
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2,
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This is the children's story \"Hoppelpoppel - wo bist du\" by my most favourite author from the last years, Hans Fallada\n",
    "# as a preparation for a visualization in Tableau.\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import bs4\n",
    "from urllib.request import urlopen as uReq\n",
    "from bs4 import BeautifulSoup as soup\n",
    "from itertools import chain\n",
    "import re"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scraping story text\n",
    "\n",
    "my_url = 'https://www.projekt-gutenberg.org/fallada/hoppelpo/chap001.html'\n",
    "\n",
    "uClient = uReq(my_url)\n",
    "page_html = uClient.read()\n",
    "uClient.close()\n",
    "\n",
    "page_soup = soup(page_html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "container = page_soup.find_all('p')\n",
    "container = container[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "title = container.find_all('h3')\n",
    "title = str(title[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "story = container.find_all('p')\n",
    "paragraphs = []\n",
    "for i in story:\n",
    "    paragraphs.append(str(i))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "for i in range(len(paragraphs)):\n",
    "    paragraphs[i] = paragraphs[i].replace('<p>', '')\n",
    "    paragraphs[i] = paragraphs[i].replace('</p>', '') "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "words = []\n",
    "try:\n",
    "    for i in range(len(paragraphs)):\n",
    "        for j in range(len(paragraphs[i])):\n",
    "            words.append(paragraphs[j].split(' ')) \n",
    "except:\n",
    "    pass"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Flatten nested lists in words\n",
    "\n",
    "words = list(chain.from_iterable(words))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "for i in range(len(words)):\n",
    "        words[i] = words[i].strip()\n",
    "        words[i] = words[i].replace('\\xa0...', '')\n",
    "        words[i] = words[i].replace('<a', '')\n",
    "        words[i] = words[i].replace('</a>', '')\n",
    "        words[i] = words[i].replace('\\n', '')\n",
    "        words[i] = words[i].replace('-', '')\n",
    "        words[i] = words[i].replace('–', '')\n",
    "        words[i] = words[i].replace('.', '')\n",
    "        words[i] = words[i].replace(':', '')\n",
    "        words[i] = words[i].replace(',', '')\n",
    "        words[i] = words[i].replace('>', '')\n",
    "        words[i] = words[i].replace('<', '')\n",
    "        words[i] = words[i].replace('›', '')\n",
    "        words[i] = words[i].replace('‹', '')\n",
    "        words[i] = words[i].replace('?', '')\n",
    "        words[i] = words[i].replace('!', '')\n",
    "        words[i] = words[i].replace('«', '')\n",
    "        words[i] = words[i].replace('»', '')\n",
    "        words[i] = words[i].replace('(', '')\n",
    "        words[i] = words[i].replace(')', '')\n",
    "        words[i] = words[i].replace(' ', '')\n",
    "        words[i] = re.sub(str('id='+'\"'+'page\\d'+'\"'), '', words[i])\n",
    "        words[i] = re.sub(str('name='+'\"'+'page\\d'+'\"'), '', words[i])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Remove empty strings in words\n",
    "\n",
    "while(\"\" in words) :\n",
    "    words.remove(\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 163,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.DataFrame(words)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 164,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.reset_index(inplace = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 165,
   "metadata": {},
   "outputs": [],
   "source": [
    "#df.columns = ['rank', 'text']\n",
    "df.columns = ['rank', 'text']\n",
    "df['text2'] = ''"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 166,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Cleaning last HTML code\n",
    "\n",
    "part1 = df[df.text == 'title=\"Dieter7/lac\"']\n",
    "part2 = df[df.text == 'title=\"suru/Dieter7\"']\n",
    "part3 = df[df.text == 'title=\"lac/Dieter7\"']\n",
    "eraser = pd.concat([part1, part2, part3])\n",
    "\n",
    "erank = []\n",
    "for i in range(len(eraser)):\n",
    "    erank.append(int(eraser.index[i]))\n",
    "\n",
    "for i in erank:\n",
    "    df = df.drop([i])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 167,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.reset_index(drop = True, inplace = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 168,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = df.drop('rank', axis = 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.reset_index(inplace = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.columns = ['rank', 'text', 'text2']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "metadata": {},
   "outputs": [
    {
     "output_type": "stream",
     "name": "stderr",
     "text": [
      "<ipython-input-172-d31fb755fdcd>:6: SettingWithCopyWarning: \nA value is trying to be set on a copy of a slice from a DataFrame\n\nSee the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n  df['text2'][i] = df.text[i+1]\n"
     ]
    }
   ],
   "source": [
    "# Fill 'text2' with text from previous row\n",
    "\n",
    "for i in range(len(df)-1):\n",
    "    if i < len(df):\n",
    "        try:\n",
    "            df['text2'][i] = df.text[i+1] \n",
    "        except:\n",
    "            pass"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "      rank     text    text2\n",
       "0        0       Es      war\n",
       "1        1      war   einmal\n",
       "2        2   einmal      ein\n",
       "3        3      ein  kleiner\n",
       "4        4  kleiner    Junge\n",
       "...    ...      ...      ...\n",
       "1294  1294      die     Welt\n",
       "1295  1295     Welt   wieder\n",
       "1296  1296   wieder       in\n",
       "1297  1297       in  Ordnung\n",
       "1298  1298  Ordnung         \n",
       "\n",
       "[1299 rows x 3 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>rank</th>\n      <th>text</th>\n      <th>text2</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>0</td>\n      <td>Es</td>\n      <td>war</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>1</td>\n      <td>war</td>\n      <td>einmal</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2</td>\n      <td>einmal</td>\n      <td>ein</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>3</td>\n      <td>ein</td>\n      <td>kleiner</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>4</td>\n      <td>kleiner</td>\n      <td>Junge</td>\n    </tr>\n    <tr>\n      <th>...</th>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <th>1294</th>\n      <td>1294</td>\n      <td>die</td>\n      <td>Welt</td>\n    </tr>\n    <tr>\n      <th>1295</th>\n      <td>1295</td>\n      <td>Welt</td>\n      <td>wieder</td>\n    </tr>\n    <tr>\n      <th>1296</th>\n      <td>1296</td>\n      <td>wieder</td>\n      <td>in</td>\n    </tr>\n    <tr>\n      <th>1297</th>\n      <td>1297</td>\n      <td>in</td>\n      <td>Ordnung</td>\n    </tr>\n    <tr>\n      <th>1298</th>\n      <td>1298</td>\n      <td>Ordnung</td>\n      <td></td>\n    </tr>\n  </tbody>\n</table>\n<p>1299 rows × 3 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 173
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.to_csv('fallada_hoppelpoppel.csv')"
   ]
  }
 ]
}