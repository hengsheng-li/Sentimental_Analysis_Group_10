import json
import re
from pathlib import Path

def extract_numeric_info(json_path: str):
    # Load the outer JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        outer_data = json.load(f)

    # Get the raw_output string
    raw_output = outer_data.get("raw_output", "")

    # Remove the ```json ... ``` fences if present
    cleaned = raw_output.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # Parse the inner JSON
    inner_data = json.loads(cleaned)

    # Extract only the key/value pairs where the value is numeric
    numeric_info = {
        key: value
        for key, value in inner_data.items()
        if isinstance(value, (int, float))
    }

    return numeric_info

if __name__ == "__main__":
    # Path to your file (adjust if needed)
    json_file = "AI_Models/Analysis_Apple Airpod Pros_21-10-14.json"

    info = extract_numeric_info(json_file)

    # Print results in a readable way
    print("Numeric fields and their values:")
    for key, value in info.items():
        print(f"{key}: {value}")