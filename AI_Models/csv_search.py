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


def get_reddit():
    client_id = "HXZPaigOHwekwXJnzrzcpg"
    client_secret = "Lp_gNkS3REot4SpeYAQ7xqRm-6pZyw"
    user_agent =  "reddit-sentiment-vader/1.0"

    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing Reddit credentials. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET."
        )

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        ratelimit_seconds=5,
    )
    return reddit


TAG_PATTERN = re.compile(r"\[(.*?)\]")  # e.g., [Review], [Help], [Question]
HASHTAG_PATTERN = re.compile(r"(#\w+)")  # hashtags in titles/comments


def extract_tags(title: str, flair: Optional[str]) -> List[str]:
    tags = []
    if flair:
        tags.append(flair.strip())

    if title:
        tags.extend([t.strip() for t in TAG_PATTERN.findall(title)])
        tags.extend([h.strip("#") for h in HASHTAG_PATTERN.findall(title)])

    seen = set()
    normed = []
    for t in tags:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            normed.append(t)
    return normed


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_posts(
    reddit,
    query: str,
    subreddits: Optional[List[str]],
    limit_posts: int,
    sort: str = "relevance",
):
    if not subreddits:
        subreddits = ["all"]

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        results = subreddit.search(query=query, sort=sort, limit=limit_posts)
        for post in results:
            yield post


def fetch_top_comments(post, max_comments_per_post: int = 10) -> List[str]:
    comments = []
    post.comments.replace_more(limit=0)
    for c in post.comments[: max_comments_per_post * 2]:
        if isinstance(c, MoreComments):
            continue
        body = clean_text(getattr(c, "body", "") or "")
        if body and body.lower() not in ("[deleted]", "[removed]"):
            comments.append(body)
            if len(comments) >= max_comments_per_post:
                break
    return comments


def analyze_sentiment(texts: List[str], analyzer: SentimentIntensityAnalyzer):
    rows = []
    for t in texts:
        vs = analyzer.polarity_scores(t)
        rows.append({"text": t, **vs})
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Reddit product review sentiment (VADER)"
    )
    parser.add_argument(
        "query",
        help='Search keywords, e.g. "Sony WH-1000XM5 review" or "Airfryer"',
    )
    parser.add_argument(
        "--subs",
        nargs="*",
        default=None,
        help="Subreddits to search (default: all). Example: --subs headphones audiophile",
    )
    parser.add_argument(
        "--posts",
        type=int,
        default=30,
        help="Max posts to scan (default: 30)",
    )
    parser.add_argument(
        "--comments",
        type=int,
        default=8,
        help="Max comments per post to analyze (default: 8)",
    )
    parser.add_argument(
        "--sort",
        choices=["relevance", "hot", "top", "new", "comments"],
        default="relevance",
        help="Search sort (default: relevance)",
    )
    parser.add_argument(
        "--outfile",
        default=None,
        help="CSV output path (default: reddit_sentiment_<timestamp>.csv)",
    )
    args = parser.parse_args()

    reddit = get_reddit()
    analyzer = SentimentIntensityAnalyzer()

    records: List[Dict] = []
    seen_posts = set()

    for post in fetch_posts(
        reddit, query=args.query, subreddits=args.subs, limit_posts=args.posts, sort=args.sort
    ):
        if post.id in seen_posts:
            continue
        seen_posts.add(post.id)

        title = clean_text(getattr(post, "title", ""))
        flair = getattr(post, "link_flair_text", None)
        tags = extract_tags(title, flair)
        url = f"https://www.reddit.com{post.permalink}"

        body_texts = []
        selftext = clean_text(getattr(post, "selftext", "") or "")
        if selftext and selftext.lower() not in ("[deleted]", "[removed]"):
            body_texts.append(selftext)

        comments = fetch_top_comments(post, max_comments_per_post=args.comments)
        review_texts = body_texts + comments

        if not review_texts:
            continue

        sentiment_rows = analyze_sentiment(review_texts, analyzer)

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
        return

    df = pd.DataFrame.from_records(records)
    post_agg = (
        df.groupby(["post_id", "title", "subreddit", "post_url", "derived_tags"], dropna=False)
        .agg(avg_compound=("vader_compound", "mean"), n_reviews=("review_text", "count"))
        .reset_index()
        .sort_values("avg_compound", ascending=False)
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = args.outfile or f"reddit_sentiment_{ts}.csv"
    df.to_csv(outfile, index=False)

    # Print a concise summary
    print("\n=== Sentiment Summary ===")
    overall_mean = df["vader_compound"].mean()
    print(f"Query: {args.query}")
    print(f"Posts analyzed: {post_agg.shape[0]}")
    print(f"Total reviews/comments analyzed: {df.shape[0]}")
    print(f"Overall average compound sentiment: {overall_mean:.3f}")

    print("\nTop 5 posts by average sentiment:")
    for _, r in post_agg.head(5).iterrows():
        print(
            f"- ({r['avg_compound']:+.3f}, n={r['n_reviews']}) "
            #f"[r/{r['subreddit']}] {r['title']} | Tags: {r['derived_tags'] or '—'}"
        )
        #print(f"  {r['post_url']}")

    print(f"\nFull row-level results saved to: {outfile}")


if __name__ == "__main__":
    main()
