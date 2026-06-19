import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from src.claim_extractor import extract_claim

df = pd.read_csv(
    "dataset/sample_claims.csv"
)

issue_correct = 0
part_correct = 0

for _, row in df.iterrows():

    pred = extract_claim(
        row["user_claim"]
    )

    if pred["issue_type"] == row["issue_type"]:

        issue_correct += 1

    if pred["object_part"] == row["object_part"]:

        part_correct += 1

n = len(df)

print(
    "Issue Accuracy:",
    issue_correct / n
)

print(
    "Part Accuracy:",
    part_correct / n
)