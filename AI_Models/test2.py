#run pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

dataset = pd.read_csv('Data_Cleaning/cleaned_beauty.csv')

def analyze_reviews(dataframe):
    reviews = dataframe['text'].tolist()
    scores = []
    for review in reviews[1000]: 
        scores.append(sentiment_scores(review)['compound'])
    dataframe["score"] = scores
    print(dataframe.head())

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict

#test function

if __name__ == "__main__":

    analyze_reviews(dataset)
