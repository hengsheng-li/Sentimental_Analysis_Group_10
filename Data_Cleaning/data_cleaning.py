import pandas as pd
import numpy as np

def clean_data(file_path: str) -> pd.DataFrame:
    df = pd.read_json(file_path, lines=True)
    df.drop(['images', 'parent_asin', 'user_id', 'asin', 'timestamp'], axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df = df.sort_values(by=['rating', 'helpful_vote'], ascending=[False, False])
    new_order = ['rating', 'helpful_vote', 'title', 'verified_purchase', 'text']
    df = df[new_order]
    df = df[df['verified_purchase'] != False]
    return df
