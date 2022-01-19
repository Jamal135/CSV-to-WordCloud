''' Creation date: 18/01/2022'''


import os
import re
import itertools
import pandas as pd
from tqdm import tqdm
from textblob import TextBlob
from wordcloud import WordCloud
from collections import Counter
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
#import nltk
#nltk.download('stopwords')

LOCATION = os.path.dirname(os.path.abspath(__file__)) + "\\%s"
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])


def remove_stop_words(text: str):
    ''' Returns: String with Stop Words Removed. '''
    return [word for word in simple_preprocess(str(text))
            if word not in stop_words]


def get_adjectives(text: str, tags: list, strict: bool):
    ''' Returns: String Cut to Relevant Adjective Data. '''
    blob = TextBlob(text)  # Corpora: python -m textblob.download_corpora
    if strict:
        return [word for (word, tag) in blob.tags if tag in tags]
    else:
        return [word for (word, tag) in blob.tags if tag.startswith(tuple(tags))]


def clean_data(input_list: str, tags: list, adjectives: bool,
               strict: bool, correct: bool, stopwords: bool):
    ''' Returns: Cleaned and Lowered List Data. '''
    for index, _ in enumerate(input_list):
        input_list[index] = re.sub(r"[^\S ]+", "", input_list[index])
        input_list[index] = re.sub(r"[^\w ]", "", input_list[index])
        input_list[index] = input_list[index].lower()
        if correct:
            input_list[index] = str(TextBlob(input_list[index]).correct())
        if stopwords:
            input_list[index] = " ".join(
                remove_stop_words(input_list[index]))
        if adjectives:
            input_list[index] = " ".join(
                get_adjectives(input_list[index], tags, strict))
    return input_list


def read_data(input_name, columns, tags, only_adjectives, strict, correct, stopwords):
    ''' Returns: Loaded Data List from CSV File. '''
    df = pd.read_csv(LOCATION % input_name + ".csv", keep_default_na=False,
                     usecols=columns, low_memory=True)
    return [clean_data(val, tags, only_adjectives, strict, correct, stopwords)
            for val in tqdm(df.astype(str).values.tolist())]


def gen_wordcloud(df_string, words):
    ''' Returns: Generated Word Cloud. '''
    wordcloud = WordCloud(width=1600, height=800, background_color="black",
                          max_words=words, contour_width=3)
    return wordcloud.generate(df_string)


def gen_cloud(input_name: str, output_name: str, columns: list, tags: list,
              adjectives: bool = True, stopwords: bool = True,
              strict: bool = False, correct: bool = True, words: int = 5000):
    ''' Returns: Built Word Cloud and Cleaned + Frequency Data. '''
    data_list = read_data(input_name, columns, tags, adjectives,
                          strict, correct, stopwords)
    df_string = " ".join(list(itertools.chain.from_iterable(data_list)))
    wordcloud = gen_wordcloud(df_string, words)
    wordcloud.to_file(output_name + '.png')
    clean_df = pd.DataFrame(data_list, columns=columns)
    clean_df.to_csv(output_name + '-data.csv')
    frequency_list = Counter(df_string.split()).most_common()
    frequency_df = pd.DataFrame(frequency_list, columns=['Word', 'Count'])
    frequency_df.to_csv(output_name + '-frequency.csv')

# Tags: https://en.wikipedia.org/wiki/Brown_Corpus#Part-of-speech_tags_used
#gen_cloud("Reviews-Data", "cloud-image",
          #["Review", "Title", "Pros", "Cons"], ["JJ", "NN", "RB", "VB"])
gen_cloud("Reviews-Data", "JJ-cloud-image",
          ["Review", "Title", "Pros", "Cons"], ["JJ"])
