import json
import anthropic
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
import time

class ProductReviewAttributeAnalyzer:
    def __init__(self, claude_api_key: str):
        self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
        self.rate_limit_delay = 1  # seconds between API calls
        
    def load_reviews_from_csv(self, csv_path: str, product_name: str = None) -> List[Dict]:
        """
        Load reviews from CSV file
        Maps Reddit post data to review format
        """
        try:
            # Read CSV directly
            df = pd.read_csv(csv_path)
            
            print(f"CSV columns found: {list(df.columns)}")
            
            # Convert DataFrame to list of dictionaries with Reddit-specific mapping
            reviews = []
            for _, row in df.iterrows():
                # Skip if no review text
                if pd.isna(row.get('review_text')) or str(row.get('review_text')).strip() == '':
                    continue
                    
                review = {
                    'review_id': str(row.get('post_id', '')),
                    'product_name': product_name if product_name else 'Apple Watch Series 7',
                    'rating': None,  # Reddit posts don't have star ratings
                    'title': str(row.get('title', '')),
                    'review_text': str(row.get('review_text', '')),
                    'reviewer_name': str(row.get('subreddit', 'Reddit User')),
                    'review_date': str(row.get('created_utc', '')),
                    'verified_purchase': False,
                    'vader_sentiment': {
                        'negative': float(row.get('vader_neg', 0)),
                        'neutral': float(row.get('vader_neu', 0)),
                        'positive': float(row.get('vader_pos', 0)),
                        'compound': float(row.get('vader_compound', 0))
                    }
                }
                reviews.append(review)
            
            print(f"Successfully loaded {len(reviews)} reviews with content")
            
            return reviews
            
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_path}")
            return []
        except Exception as e:
            print(f"Error loading reviews: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def analyze_product_attributes(self, review_data: Dict, product_name: str) -> Dict:
        """
        Analyze how the review discusses product attributes across 8 factors
        """
        # Combine review text components
        text_parts = []
        if review_data.get('title'):
            text_parts.append(f"Title: {review_data['title']}")
        if review_data.get('rating'):
            text_parts.append(f"Rating: {review_data['rating']} stars")
        if review_data.get('review_text'):
            # Limit content to avoid token limits
            content = review_data['review_text'][:4000]
            text_parts.append(f"Review: {content}")
        
        full_text = '\n\n'.join(text_parts)
        
        if len(full_text.strip()) < 20:
            return {
                'product': product_name,
                'review_id': review_data.get('review_id', ''),
                'battery_life': 5,
                'customer_service': 5,
                'user_interface': 5,
                'aesthetic': 5,
                'processor_speed': 5,
                'material': 5,
                'price': 5,
                'longevity_reliability': 5,
                'error': 'Insufficient content for analysis'
            }
        
        prompt = f"""You are a helpful assistant that analyzes product reviews and returns results in JSON format. You specialize in evaluating specific product attributes mentioned in reviews.

                Analyze this csv of review about {product_name}, only consider the in the review_text column for your analysis, then provide ONLY a JSON response with scores for how the review discusses these eight product attributes:

**Scoring Scale (1-10):**
- 1-2 = Very negative or major problems mentioned
- 3-4 = Somewhat negative or minor issues mentioned
- 5-6 = Neutral, not mentioned, or mixed feedback
- 7-8 = Somewhat positive or good performance mentioned
- 9-10 = Very positive or excellent performance mentioned

**Attributes to Score:**

1. **Battery Life** - How does the review describe the battery performance, charging time, or battery longevity?
2. **User Interface** - How does the review describe the ease of use, software, navigation, or user experience?
3. **Aesthetic** - Does the review comment on appearance, design, look, style, or visual appeal?
4. **Material** - Does the review discuss build quality, materials used, durability, or construction?
5. **Price** - Does the review mention value for money, cost, pricing, affordability, or whether it's worth the price?

**Required JSON Format:**
{{
  "product": "{product_name}",
  "review_id": "{review_data.get('review_id', '')}",
  "battery_life": X,
  "customer_service": X,
  "user_interface": X,
  "aesthetic": X,
  "processor_speed": X,
  "material": X,
  "price": X,
  "longevity_reliability": X
}}

**Review to analyze:**
Product: {product_name}
Reviewer: {review_data.get('reviewer_name', 'Anonymous')}
Date: {review_data.get('review_date', '')}

{full_text}

Respond ONLY with the JSON object, no additional text."""

        try:
            #time.sleep(self.rate_limit_delay)  Rate limiting
            
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                temperature=0.3,  # Set temperature to 0.3 for consistent analysis
                messages=[{
                    "role": "user", 
                    "content": prompt
                }]
            )
            
            response_text = response.content[0].text
            
            # Extract JSON from response
            try:
                # Look for JSON object in response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis_data = json.loads(json_match.group())
                else:
                    analysis_data = json.loads(response_text)
                
                # Validate required fields and ensure they're in the correct range
                required_fields = ['product', 'review_id', 'battery_life', 'customer_service', 'user_interface', 'aesthetic', 'processor_speed', 'material', 'price', 'longevity_reliability']
                for field in required_fields:
                    if field not in analysis_data:
                        if field == 'product':
                            analysis_data[field] = product_name
                        elif field == 'review_id':
                            analysis_data[field] = review_data.get('review_id', '')
                        else:
                            analysis_data[field] = 5  # Default neutral score
                
                # Ensure scores are within 1-10 range
                score_fields = ['battery_life', 'customer_service', 'user_interface', 'aesthetic', 'processor_speed', 'material', 'price', 'longevity_reliability']
                for field in score_fields:
                    if not isinstance(analysis_data[field], (int, float)) or analysis_data[field] < 1 or analysis_data[field] > 10:
                        analysis_data[field] = 5  # Default to neutral if invalid
                
                return analysis_data
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing Claude response: {e}")
                print(f"Raw response: {response_text[:500]}")
                return self._fallback_analysis(review_data.get('review_id', ''), product_name)
                
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            #return self._fallback_analysis(review_data.get('review_id', ''), product_name)
    
    def _fallback_analysis(self, review_id: str, product_name: str) -> Dict:
        """Fallback when API fails - returns neutral scores"""
        return {
            'product': product_name,
            'review_id': review_id,
            'battery_life': 5,
            'customer_service': 5,
            'user_interface': 5,
            'aesthetic': 5,
            'processor_speed': 5,
            'material': 5,
            'price': 5,
            'longevity_reliability': 5,
            'error': 'API failed - neutral scores assigned'
        }
    
    def analyze_reviews_batch(self, reviews: List[Dict], product_name: str = None) -> List[Dict]:
        """Analyze product attributes for a batch of reviews"""
        results = []
        
        # Determine product name from reviews if not provided
        if not product_name and reviews:
            product_name = reviews[0].get('product_name', 'Product')
        
        print(f"Analyzing {len(reviews)} reviews for product attributes of '{product_name}'...")
        
        for i, review in enumerate(reviews):
            print(f"Processing review {i+1}/{len(reviews)}: {review.get('title', 'No title')[:60]}...")
            
            # Analyze product attributes
            attribute_data = self.analyze_product_attributes(review, product_name)
            
            # Combine results
            result = {
                'review_metadata': {
                    'review_id': review.get('review_id'),
                    'title': review.get('title'),
                    'rating': review.get('rating'),
                    'reviewer_name': review.get('reviewer_name'),
                    'review_date': review.get('review_date'),
                    'verified_purchase': review.get('verified_purchase')
                },
                'attribute_analysis': attribute_data,
                'content_summary': {
                    'has_content': bool(review.get('review_text')),
                    'content_length': len(review.get('review_text', '')),
                    'has_error': 'error' in attribute_data
                }
            }
            
            results.append(result)
            
            # Rate limiting
            #if i < len(reviews) - 1:
                #time.sleep(0.5)
        
        return results
    
    def generate_comprehensive_report(self, results: List[Dict], product_name: str = None) -> Dict:
        """Generate detailed product attribute analysis report"""
        if not results:
            return {
                'summary': {'total_reviews': 0, 'error': 'No reviews to analyze'},
                'analysis_date': datetime.now().isoformat()
            }
        
        # Extract product name from results if not provided
        if not product_name and results:
            product_name = results[0].get('attribute_analysis', {}).get('product', 'Product')
        
        # Extract all attribute scores
        valid_results = [r for r in results if 'error' not in r['attribute_analysis']]
        
        if not valid_results:
            print("Warning: No valid analyses found")
            valid_results = results  # Use all results as fallback
        
        # Calculate average scores for each attribute
        attributes = ['battery_life', 'customer_service', 'user_interface', 'aesthetic', 'processor_speed', 'material', 'price', 'longevity_reliability']
        attribute_scores = {}
        
        for attribute in attributes:
            scores = [r['attribute_analysis'][attribute] for r in valid_results if attribute in r['attribute_analysis']]
            if scores:
                attribute_scores[attribute] = {
                    'average': round(sum(scores) / len(scores), 2),
                    'min': min(scores),
                    'max': max(scores),
                    'count': len(scores),
                    'std_dev': round(pd.Series(scores).std(), 2) if len(scores) > 1 else 0
                }
            else:
                attribute_scores[attribute] = {'average': 5.0, 'min': 5, 'max': 5, 'count': 0, 'std_dev': 0}
        
        # Categorize reviews by overall sentiment
        positive_reviews = []
        negative_reviews = []
        neutral_reviews = []
        
        for result in valid_results:
            aa = result['attribute_analysis']
            # Calculate overall sentiment based on average of all attributes
            all_scores = [
                aa.get('battery_life', 5),
                aa.get('customer_service', 5),
                aa.get('user_interface', 5),
                aa.get('aesthetic', 5),
                aa.get('processor_speed', 5),
                aa.get('material', 5),
                aa.get('price', 5),
                aa.get('longevity_reliability', 5)
            ]
            average_score = sum(all_scores) / len(all_scores)
            
            if average_score >= 7:
                positive_reviews.append(result)
            elif average_score <= 4:
                negative_reviews.append(result)
            else:
                neutral_reviews.append(result)
        
        # Calculate rating distribution if available
        ratings = [r['review_metadata'].get('rating', 0) for r in results if r['review_metadata'].get('rating')]
        rating_distribution = {}
        if ratings:
            for rating in [1, 2, 3, 4, 5]:
                count = ratings.count(rating)
                rating_distribution[f"{rating}_star"] = {
                    'count': count,
                    'percentage': round((count / len(ratings)) * 100, 1)
                }
            avg_rating = round(sum(ratings) / len(ratings), 2)
        else:
            avg_rating = None
        
        # Create comprehensive report
        report = {
            'summary': {
                'product_analyzed': product_name,
                'total_reviews_analyzed': len(results),
                'valid_analyses': len(valid_results),
                'average_rating': avg_rating,
                'rating_distribution': rating_distribution,
                'review_categorization': {
                    'positive': len(positive_reviews),
                    'negative': len(negative_reviews),
                    'neutral': len(neutral_reviews)
                }
            },
            'attribute_analysis': attribute_scores,
            'detailed_breakdown': {
                'positive_reviews': [
                    {
                        'title': r['review_metadata']['title'],
                        'rating': r['review_metadata']['rating'],
                        'reviewer': r['review_metadata']['reviewer_name'],
                        'review_id': r['review_metadata']['review_id'],
                        'scores': r['attribute_analysis']
                    }
                    for r in positive_reviews[:5]  # Top 5 positive
                ],
                'negative_reviews': [
                    {
                        'title': r['review_metadata']['title'],
                        'rating': r['review_metadata']['rating'],
                        'reviewer': r['review_metadata']['reviewer_name'],
                        'review_id': r['review_metadata']['review_id'],
                        'scores': r['attribute_analysis']
                    }
                    for r in negative_reviews[:5]  # Top 5 negative
                ]
            },
            'all_reviews': [
                {
                    'review_id': r['review_metadata']['review_id'],
                    'title': r['review_metadata']['title'],
                    'rating': r['review_metadata']['rating'],
                    'reviewer': r['review_metadata']['reviewer_name'],
                    'battery_life': r['attribute_analysis'].get('battery_life', 5),
                    'customer_service': r['attribute_analysis'].get('customer_service', 5),
                    'user_interface': r['attribute_analysis'].get('user_interface', 5),
                    'aesthetic': r['attribute_analysis'].get('aesthetic', 5),
                    'processor_speed': r['attribute_analysis'].get('processor_speed', 5),
                    'material': r['attribute_analysis'].get('material', 5),
                    'price': r['attribute_analysis'].get('price', 5),
                    'longevity_reliability': r['attribute_analysis'].get('longevity_reliability', 5)
                }
                for r in valid_results
            ],
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'model_used': 'claude-3-5-haiku-20241022',
                'data_source': 'External CSV file'
            }
        }
        
        return report
    
    def save_report(self, report: Dict, filename: str = None) -> str:
        """Save report to JSON file"""
        if filename is None:
            filename = "Json_Results/claude_review_output.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Report saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving report: {e}")
            return ""
    
    def print_summary_stats(self, report: Dict):
        """Print formatted summary statistics"""
        print("\n" + "="*60)
        print(f"PRODUCT ATTRIBUTE ANALYSIS SUMMARY")
        print("="*60)
        
        summary = report['summary']
        print(f"\nProduct: {summary['product_analyzed']}")
        print(f"Total Reviews Analyzed: {summary['total_reviews_analyzed']}")
        
        if summary.get('average_rating'):
            print(f"Average Rating: {summary['average_rating']}/5.0")
            
        print(f"\nSentiment Distribution:")
        cats = summary['review_categorization']
        total = cats['positive'] + cats['negative'] + cats['neutral']
        if total > 0:
            print(f"  Positive: {cats['positive']} ({cats['positive']/total*100:.1f}%)")
            print(f"  Negative: {cats['negative']} ({cats['negative']/total*100:.1f}%)")
            print(f"  Neutral:  {cats['neutral']} ({cats['neutral']/total*100:.1f}%)")
        
        print(f"\n" + "-"*40)
        print("ATTRIBUTE SCORES (1-10 scale)")
        print("-"*40)
        
        # Format attribute names for display
        attribute_display_names = {
            'battery_life': 'Battery Life',
            'customer_service': 'Customer Service',
            'user_interface': 'User Interface',
            'aesthetic': 'Aesthetic',
            'processor_speed': 'Processor Speed',
            'material': 'Material',
            'price': 'Price',
            'longevity_reliability': 'Longevity/Reliability'
        }
        
        for attribute, data in report['attribute_analysis'].items():
            # Create visual bar
            score = data['average']
            bar_length = int(score * 3)  # Scale to 30 chars max
            bar = "█" * bar_length + "░" * (30 - bar_length)
            
            display_name = attribute_display_names.get(attribute, attribute.replace('_', ' ').title())
            print(f"{display_name:22} {score:4.1f}  {bar}")
            print(f"                       (min: {data['min']}, max: {data['max']}, std: {data.get('std_dev', 0):.1f})")
