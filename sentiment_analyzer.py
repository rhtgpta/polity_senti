# importing packages
import pandas as pd
import re
import numpy as np
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

# reading the final output file
df = pd.read_csv('../GetOldTweets-python/final_output.csv', sep = '|')
print ('Output from Twitter read...')

# defining functiions to pre-process tweets
def clean_tweet(text):
    # capturing urls
    result = re.sub(r'http\S+', '', text)
    # because many urls have spaces which makes detection harder
    # replacing all full-stops, # and @
    result = re.sub('[.@#]', '', result)
    # broken url has '-' or '/' between words
    result = re.sub(r'\w+(?:/\w+)+',"", result)
    result = re.sub(r'\w+(?:-\w+)+',"", result)
    # deleting digits from the tweet
    result = re.sub(" \d+", " ", result)
    # removing short words with less than 3 character length
    result = " ".join([word for word in result.split() if len(word) > 2])
    return result

# applying the function to clean all tweets
df['clean_tweet'] = df['text'].apply(clean_tweet)
print ('Tweets cleaned...')

# calculating the sentiment scores
df['sentiment'] = df['clean_tweet'].apply(analyser.polarity_scores)
print ('Sentiment scores obtained...')

# function to get the compound value from resultant dictionary 
def get_compound_score(dict_row):
    result = dict_row['compound']
    return result

# get the compound value from the sentiment result
df['sentiment_score'] = df['sentiment'].apply(get_compound_score)

# creating sentiment classes based on the composite sentiment scores
def sentiment_class(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    elif score == 0.0:
        return 'Neutral'
    else:
        print ('Weird response!')

# obtaining the sentiment classes from the composite scores
df['sentiment_class'] = df['sentiment_score'].apply(sentiment_class)
print ('Saving the final output to disk...')

# saving only relevant columns
df = df[['date', 'clean_tweet', 'sentiment_score', 'sentiment_class']]
df.to_csv('final_text_sentiment.csv', index = False, sep = '|')