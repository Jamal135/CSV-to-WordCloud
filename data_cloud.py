
from wordcloud import WordCloud
import pandas as pd
import os

# Specify Location Current Folder.
LOCATION = os.path.dirname(os.path.abspath(__file__)) + "\\data_folder\\%s"

# Read Review Text Only from Sample.
reviews = pd.read_csv(LOCATION % "reviews_sample.csv",
                      usecols=["Review"], low_memory=True)

# Remove New Lines.
reviews['Review'] = reviews['Review'].str.replace(r'\\r\\n', ' ', regex=True)
reviews['Review'] = reviews['Review'].str.replace(r'\\n', '', regex=True)
reviews['Review'] = reviews['Review'].str.replace(r'\\r', ' ', regex=True)

# Remove Punctuation.
reviews['Review'] = reviews['Review'].str.replace('[^\w\s]', '', regex=True)

# Remove Capitalisation.
reviews['Review'] = reviews['Review'].map(lambda x: x.lower())

# Join Reviews Together.
reviews_string = ','.join(list(reviews['Review'].values))

# Create WordCloud Object.
wordcloud = WordCloud(width=1600, height=800, background_color="black", max_words=5000,
                      contour_width=3)

# Generate a word cloud
wordcloud.generate(reviews_string)

# Visualize the word cloud
wordcloud.to_file('output_folder/cloud_image.png')

# Print out the first rows of papers
reviews.to_csv('output_folder/cleaned_reviews.csv')
