''' Creation date: 18/01/2022'''


from collections import Counter
from wordcloud import WordCloud
from textblob import TextBlob
import pandas as pd
import itertools
import re
import os

LOCATION = os.path.dirname(os.path.abspath(__file__)) + "\\data_folder\\%s"


def read_csv(input_name, columns, only_adjectives, strict):
    ''' Returns: Loaded Data List from CSV File. '''
    df = pd.read_csv(LOCATION % input_name + ".csv", keep_default_na=False,
                     usecols=columns, low_memory=True)
    return [clean_data(val, only_adjectives, strict)
            for val in df.astype(str).values.tolist()]


def get_adjectives(text: str, strict: bool):
    ''' Returns: String Cut to Relevant Adjective Data. '''
    blob = TextBlob(text) # Corpora: python -m textblob.download_corpora
    if strict:
        return [word for (word, tag) in blob.tags if tag == ("JJ")]
    else:
        return [word for (word, tag) in blob.tags if tag.startswith("JJ")]


def clean_data(input_list: str, only_adjectives: bool, strict: bool):
    ''' Returns: Cleaned and Lowered List Data. '''
    for index, _ in enumerate(input_list):
        input_list[index] = re.sub(r"[^\S ]+", "", input_list[index])
        input_list[index] = re.sub(r"[^\w ]", "", input_list[index])
        input_list[index] = ' '.join(input_list[index].split())
        input_list[index] = input_list[index].lower()
        if only_adjectives:
            input_list[index] = " ".join(
                get_adjectives(input_list[index], strict))
    return input_list


def gen_wordcloud(df_string, words):
    ''' Returns: Generated Word Cloud. '''
    wordcloud = WordCloud(width=1600, height=800, background_color="black",
                          max_words=words, contour_width=3)
    return wordcloud.generate(df_string)


def gen_cloud(input_name: str, output_name: str, columns: list,
              only_adjectives: bool = True, strict: bool = False,
              words: int = 5000):
    ''' Returns: Built Word Cloud and Cleaned + Frequency Data. '''
    data_list = read_csv(input_name, columns, only_adjectives, strict)
    df_string = " ".join(list(itertools.chain.from_iterable(data_list)))
    wordcloud = gen_wordcloud(df_string, words)
    wordcloud.to_file('output_folder/' + output_name + '.png')
    clean_df = pd.DataFrame(data_list, columns=columns)
    clean_df.to_csv('output_folder/' + output_name + '-data.csv')
    frequency_list = Counter(df_string.split()).most_common()
    frequency_df = pd.DataFrame(frequency_list, columns=['Word', 'Count'])
    frequency_df.to_csv('output_folder/' + output_name + '-frequency.csv')


gen_cloud("Reviews-Data", "cloud-image", ["Review", "Title"], strict = True)
