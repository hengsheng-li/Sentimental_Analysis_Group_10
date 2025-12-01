from openai import OpenAI
import json
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
import time
from pydantic import BaseModel



class AIModelAnalyzer:
    def __init__(self, api_key: str, rate_limit_delay: float = 1.0):
        if not api_key:
            raise RuntimeError("OpenAI API key is required. Set OPENAI_API_KEY or pass --api-key")
        self.client = OpenAI(api_key=api_key)
        self.rate_limit_delay = rate_limit_delay

    def load_reviews_from_csv(self, csv_path: str, product_name: str = None) -> List[Dict]:
        try:
            df = pd.read_csv(csv_path)
            
            reviews: List[Dict] = []
            for _, row in df.iterrows():
        
                review = {
                    'product_name': product_name or str(row.get('product_name', '')),
                    'title': str(row.get('title', '')),
                    'review_text': row.get('review_texts'),
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

    def analyze_reviews(self, reviews: List[Dict], save_path: Optional[str] = None) -> Dict:
        if not reviews:
            raise ValueError("No reviews provided to analyze")

        prompt_text = (
            f'''
			You are an assistant that analyzes product reviews. Analyze this dataframe of review {reviews}.
			Do a a general postive or negative analysis, 1-10 and a specifice analysis to evaluate any features that are talked about in each review then give the feature a score of 1-10.
            
			**Scoring Scale (1-10):**
			- 1-2 = Very negative or major problems mentioned
			- 3-4 = Somewhat negative or minor issues mentioned
			- 5-6 = Neutral, not mentioned, or mixed feedback
			- 7-8 = Somewhat positive or good performance mentioned
			- 9-10 = Very positive or excellent performance mentioned           
             
            If no features are mentioned, don't include it in feature analysis but include it in general analysis.
            
			**Example Features to Score:**

			1. **Battery Life** - How does the review describe the battery performance, charging time, or battery longevity?
			2. **User Interface** - How does the review describe the ease of use, software, navigation, or user experience?
			3. **Aesthetic** - Does the review comment on appearance, design, look, style, or visual appeal?
			4. **Material** - Does the review discuss build quality, materials used, durability, or construction?
			5. **Price** - Does the review mention value for money, cost, pricing, affordability, or whether it's worth the price?
					
            '''
        )

        # Call the OpenAI Responses API
        try:
            response = self.client.responses.parse(
    			model="gpt-5-nano-2025-08-07",
    			input=[
        			{"role": "user", "content": prompt_text},
    			],
    		text_format=Summary,
			)
                        
            try:
                result_text = response.output_parsed
            except Exception:
                result_text = None
        
            return result_text

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
        
        
class Feature(BaseModel):
    feature: str
    score: int
    analysis: str
    
class Summary(BaseModel):
    product_name: str
    general_analysis: str
    results: list[Feature]

