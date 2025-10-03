from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

dataset = pd.read_csv('Data_Cleaning/cleaned_beauty.csv')

def analyze_reviews(dataframe):
    sid = SentimentIntensityAnalyzer()
    dataset['text'] = dataset['text'].fillna('').astype(str)
    dataset['sentiment_score'] = dataset['text'].apply(lambda s: sid.polarity_scores(s)['compound'])
    dataset.to_csv('AI_Models/beauty_with_sentiments.csv', index=False)

if __name__ == "__main__":

    analyze_reviews(dataset)
