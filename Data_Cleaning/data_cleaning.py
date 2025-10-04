import json
import csv
from typing import Optional
import pandas as pd


def clean_data_stream(input_path: str, output_csv: str, dedupe_on: Optional[str] = 'text') -> int:
    """Stream a JSON Lines file, apply filters and field drops, and write cleaned rows to CSV incrementally.

    - Drops fields: images, parent_asin, user_id, timestamp, rating, helpful_vote, verified_purchase, title
    - Keeps other fields as-is
    - Filters out records where verified_purchase is exactly False
    - Normalizes missing 'text' to empty string
    - Deduplicates on the `dedupe_on` field (if present) to avoid storing duplicates in output

    Returns the number of rows written to `output_csv`.
    """
    drop_early = ['images', 'parent_asin', 'user_id', 'timestamp']
    drop_late = ['rating', 'helpful_vote', 'verified_purchase', 'title']

    rows_written = 0
    seen = set()
    writer = None

    with open(input_path, 'r', encoding='utf-8') as fin, open(output_csv, 'w', newline='', encoding='utf-8') as fout:
        for line_number, line in enumerate(fin, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                # skip malformed lines
                continue

            # drop early-unneeded fields
            for k in drop_early:
                obj.pop(k, None)

            # filter: drop if verified_purchase is explicitly False
            if obj.get('verified_purchase', True) is False:
                continue

            # normalize text
            obj['text'] = str(obj.get('text', '') or '')

            # drop later fields we don't want in output
            for k in drop_late:
                obj.pop(k, None)

            # dedupe on provided key (safe if key missing)
            if dedupe_on and dedupe_on in obj:
                key = obj.get(dedupe_on, '')
            else:
                # fallback dedupe on full text
                key = obj.get('text', '')

            if key in seen:
                continue
            seen.add(key)

            # initialize CSV writer using the first object's keys
            if writer is None:
                fieldnames = list(obj.keys())
                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writeheader()

            # Ensure writer has all fields present (missing -> empty string)
            row = {fn: obj.get(fn, '') for fn in writer.fieldnames}
            writer.writerow(row)
            rows_written += 1

    return rows_written


if __name__ == '__main__':
    input_file = 'AI_Models/Electronics.jsonl'
    output_file = 'AI_Models/cleaned_electronics.csv'
    n = clean_data_stream(input_file, output_file)
    print(f'Wrote {n} cleaned rows to {output_file}')