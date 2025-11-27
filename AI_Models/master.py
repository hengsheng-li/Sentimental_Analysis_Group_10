from reviews import Reddit
from analysis import AIModelAnalyzer
from typing import List, Dict, Optional
import json
from pathlib import Path
from datetime import datetime
import json
import re


class SentimentAnalyzer:
    def __init__(self, api_key: str):
        self.reddit_client = Reddit()
        self.analyzer = AIModelAnalyzer(api_key=api_key)


    def run_analysis(self):
        item = input("Enter the product name: ")
        outfile = self.reddit_client.get_csv_reviews(item)
        reviews = self.analyzer.load_reviews_from_csv(outfile, product_name=item)
        result = self.analyzer.analyze_reviews(reviews)
        print(result)
        # Figure out what type result is and get the data accordingly

    


    
if __name__ == "__main__":
    analyzer = SentimentAnalyzer('your_api_key_here')
    analyzer.run_analysis()
















# --- IGNORE --- run with claude api key
'''
    def run(self, key):
        analyzer = SentimentIntensityAnalyzer()
        while True:
            item = input("Enter Item: ")
            if not item or item.lower() in ("exit", "quit", "q"):
                print("Exiting.")
                break

            records: List[Dict] = []
            seen_posts = set()

            for post in self.fetch_posts(reddit=self.reddit, query=f'{item} review', limit_posts=25, sort='relevance'):
                if post.id in seen_posts:
                    continue
                seen_posts.add(post.id)

                post_flair = getattr(post, "link_flair_text", None)
                title = self.clean_text(getattr(post, "title", "") or "")
                tags = self.extract_tags(title, post_flair)
                url = f"https://www.reddit.com{post.permalink}"

                body_texts = []
                selftext = self.clean_text(getattr(post, "selftext", "") or "")
                if selftext and selftext.lower() not in ("[deleted]", "[removed]"):
                    body_texts.append(selftext)

                comments = self.fetch_top_comments(post, max_comments_per_post=1)
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
                        "post_flair": post_flair or "",
                        "derived_tags": ", ".join(tags),
                        "review_text": row["text"],
                        "vader_neg": row["neg"],
                        "vader_neu": row["neu"],
                        "vader_pos": row["pos"],
                        "vader_compound": row["compound"],
                    }
                )

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

            ts = datetime.now().strftime("%H:%M:%S")
            outfile = f"reddit_{item}_{ts}.csv"
            df.to_csv(outfile, index=False)

            time.sleep(5)

            """=== Starting Product Review Attribute Analysis ==="""

            # Configuration - Replace with your actual Claude API key and CSV path
            CONFIG = {
                'claude_api_key': key,
                'csv_file_path': outfile,
                'product_name': item  # Specify the product name
            }
            
            # Initialize analyzer
            analyzer = ProductReviewAttributeAnalyzer(
                claude_api_key=CONFIG['claude_api_key']
            )
            
            try:
                # Load reviews from CSV file
                print(f"=== PRODUCT REVIEW ATTRIBUTE ANALYSIS ===")
                print(f"Loading reviews from {CONFIG['csv_file_path']}...")
                
                reviews = analyzer.load_reviews_from_csv(
                    csv_path=CONFIG['csv_file_path'],
                    product_name=CONFIG['product_name']
                )
                
                if not reviews:
                    print("No reviews found. Please check your CSV file path and format.")
                    return
                
                print(f"Loaded {len(reviews)} reviews")
                
                # Optionally limit number of reviews to analyze (for testing/cost management)
                max_reviews = 50  # Adjust as needed
                if len(reviews) > max_reviews:
                    print(f"Limiting analysis to first {max_reviews} reviews")
                    reviews = reviews[:max_reviews]
                
                # Analyze reviews
                results = analyzer.analyze_reviews_batch(reviews, CONFIG['product_name'])
                
                # Generate comprehensive report
                print("\nGenerating comprehensive report...")
                report = analyzer.generate_comprehensive_report(results, CONFIG['product_name'])
                
                # Display formatted summary
                analyzer.print_summary_stats(report)
                
                # Save detailed report
                filename = analyzer.save_report(report, filename=f'Json_Results/{item}_claude_review_output_{ts}.json')
                print(f"\nDetailed report saved as: {filename}")
                
            except Exception as e:
                print(f"Error during analysis: {e}")
                import traceback
                traceback.print_exc()
'''