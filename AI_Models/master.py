import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class AmazonProductSentimentAnalyzer:
    def __init__(self, input: str):
        self.input = input
        self.sid = SentimentIntensityAnalyzer()
        self.cleaned_dataset = pd.read_csv(self.input)
        #self.cleaned_dataset = self.clean_data(self.dataset)
        self.analyze_sentiments()


    def clean_data(self, data):
        data.drop(['images', 'parent_asin', 'user_id', 'timestamp'], axis=1, inplace=True)
        data.drop_duplicates(inplace=True)
        data = data.sort_values(by=['rating', 'helpful_vote'], ascending=[False, False])
        data = data[data['verified_purchase'] != False]
        data.drop(['rating', 'helpful_vote', 'verified_purchase', 'title'], axis=1, inplace=True)
        return data


    def analyze_sentiments(self):
        self.cleaned_dataset['text'] = self.cleaned_dataset['text'].fillna('').astype(str)
        self.cleaned_dataset['sentiment_score'] = self.cleaned_dataset['text'].apply(lambda s: self.sid.polarity_scores(s)['compound'])


    def product_lookup(self, asin: str):
        product_reviews = self.cleaned_dataset[self.cleaned_dataset['asin'] == asin]
        if product_reviews.empty:
            return f"No reviews found for ASIN: {asin}"
        avg_sentiment = float(product_reviews['sentiment_score'].mean()).__round__(4)
        return {
            "asin": asin,
            "average_sentiment_score": avg_sentiment,
            "number_of_reviews": len(product_reviews)
        }
    
if __name__ == "__main__":
    analyzer = AmazonProductSentimentAnalyzer('AI_Models/cleaned_electronics.csv')
    result = analyzer.product_lookup('B0DGHQ2QH6')
    print(result)