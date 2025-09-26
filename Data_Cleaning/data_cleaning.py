import pandas as pd
import numpy as np

def clean_data(file_path: str) -> pd.DataFrame:
    df = pd.read_json(file_path, lines=True)
    df.drop(['images', 'parent_asin', 'user_id', 'timestamp'], axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df = df.sort_values(by=['rating', 'helpful_vote'], ascending=[False, False])
    df = df[df['verified_purchase'] != False]
    df.drop(['rating', 'helpful_vote', 'verified_purchase', 'title'], axis=1, inplace=True)
    return df


cleaned = clean_data('Data_Cleaning/All_Beauty.jsonl')
cleaned.to_csv('Data_Cleaning/cleaned_beauty.csv', index=False)