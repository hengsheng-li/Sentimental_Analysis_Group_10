import os
import re
import time
import argparse
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
import praw
from praw.models import MoreComments
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class RedditSentimentAnalyzer:
    def __init__(self):
        self.client_id = "HXZPaigOHwekwXJnzrzcpg"
        self.client_secret = "Lp_gNkS3REot4SpeYAQ7xqRm-6pZyw"
        self.user_agent =  "reddit-sentiment-vader/1.0"

        if not self.client_id or not self.lient_secret:
            raise RuntimeError(
                "Missing Reddit credentials. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET."
            )
        
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            ratelimit_seconds=5,
        )
        self.TAG_PATTERN = re.compile(r"\[(.*?)\]")  
        self.HASHTAG_PATTERN = re.compile(r"(#\w+)") 


    def extract_tags(self, title: str, flair: Optional[str]) -> List[str]:
        tags = []
        if flair:
            tags.append(flair.strip())

        if title:
            tags.extend([t.strip() for t in self.TAG_PATTERN.findall(title)])
            tags.extend([h.strip("#") for h in self.HASHTAG_PATTERN.findall(title)])

        seen = set()
        normed = []
        for t in tags:
            key = t.lower()
            if key not in seen:
                seen.add(key)
                normed.append(t)
        return normed


    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"http\S+|www\.\S+", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text


    def fetch_posts(self, reddit, query: str, subreddits: Optional[List[str]], 
                    limit_posts: int, sort: str,
                    flair: Optional[str] = None):
        if not subreddits:
            subreddits = ["all"]

        for sub in subreddits:
            subreddit = self.reddit.subreddit(sub)
            results = subreddit.search(query=query, flair=flair, sort=sort, limit=limit_posts)
            for post in results:
                yield post


    def fetch_top_comments(self, post, max_comments_per_post: int = 10) -> List[str]:
        comments = []
        post.comments.replace_more(limit=0)
        for c in post.comments[: max_comments_per_post * 2]:
            if isinstance(c, MoreComments):
                continue
            body = self.clean_text(getattr(c, "body", "") or "")
            if body and body.lower() not in ("[deleted]", "[removed]"):
                comments.append(body)
                if len(comments) >= max_comments_per_post:
                    break
        return comments


    def analyze_sentiment(self, texts: List[str], analyzer: SentimentIntensityAnalyzer):
        rows = []
        for t in texts:
            vs = analyzer.polarity_scores(t)
            rows.append({"text": t, **vs})
        return rows
    
    
    def run(self):
        reddit = self.reddit
        analyzer = SentimentIntensityAnalyzer()
        while True:
            sentence = input("Enter: 'Item' 'Sub' 'post' 'comments' 'sort'").lower()
            item = sentence.split()[0]
            subreddits = sentence.split()[1].split(",") if len(sentence.split()) > 1 else None
            limit_posts = int(sentence.split()[2]) if len(sentence.split()) > 2 else 50
            max_comments = int(sentence.split()[3]) if len(sentence.split()) > 3 else 10
            sort = sentence.split()[4] if len(sentence.split()) > 4 else 'relevance'

            records: List[Dict] = []
            seen_posts = set()

            for post in self.fetch_posts(reddit, item, subreddits, limit_posts, sort , flair="Product Review"):
                if post.id in seen_posts:
                    continue
                seen_posts.add(post.id)

                title = self.clean_text(getattr(post, "title", "") or "")
                flair = getattr(post, "link_flair_text", None)
                tags = self.extract_tags(title, flair)
                url = f"https://www.reddit.com{post.permalink}"

                body_texts = []
                selftext = self.clean_text(getattr(post, "selftext", "") or "")
                if selftext and selftext.lower() not in ("[deleted]", "[removed]"):
                    body_texts.append(selftext)

                comments = self.fetch_top_comments(post, max_comments_per_post=max_comments)
                review_texts = body_texts + comments

                if not review_texts:
                    continue

                sentiment_rows = self.analyze_sentiment(review_texts, analyzer)

                for row in sentiment_rows:
                    records.append(
                    {
                        "post_id": post.id,
                        "subreddit": str(post.subreddit),
                        "created_utc": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": title,
                        "post_url": url,
                        "post_flair": flair or "",
                        "derived_tags": ", ".join(tags),
                        "review_text": row["text"],
                        "vader_neg": row["neg"],
                        "vader_neu": row["neu"],
                        "vader_pos": row["pos"],
                        "vader_compound": row["compound"],
                    }
                )
                time.sleep(0.5)

            if not records:
                print("No results found. Try adjusting your query, subs, or limits.")
                continue



            df = pd.DataFrame.from_records(records)
            post_agg = (
            df.groupby(["post_id", "title", "subreddit", "post_url", "derived_tags"], dropna=False)
            .agg(avg_compound=("vader_compound", "mean"), n_reviews=("review_text", "count"))
            .reset_index()
            .sort_values("avg_compound", ascending=False)
            )

            ts = datetime.now().strftime("%H%M%S")
            outfile = f"reddit_{item}_{ts}.csv"
            df.to_csv(outfile, index=False)

            print("\n=== Sentiment Summary ===")
            overall_mean = df["vader_compound"].mean()
            print(f"Item: {item}")
            print(f"Posts analyzed: {post_agg.shape[0]}")
            print(f"Total reviews/comments analyzed: {df.shape[0]}")
            print(f"Overall average compound sentiment: {overall_mean:.3f}")

            print("\nTop 5 posts by average sentiment:")
            for _, r in post_agg.head(5).iterrows():
                print(f"- ({r['avg_compound']:+.3f}, n={r['n_reviews']}) ")

    
if __name__ == "__main__":
    analyzer = RedditSentimentAnalyzer()
    analyzer.run()