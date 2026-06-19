import pandas as pd

from src.claim_extractor import extract_claim
from src.verifier import (
    determine_status,
    build_risk_flags
)
from src.image_analyzer import analyze_image
print("REAL IMAGE ANALYZER LOADED")

claims = pd.read_csv(
    "dataset/claims.csv"
)

history = pd.read_csv(
    "dataset/user_history.csv"
)

rows = []

# Process claims
for _, row in claims.iterrows():
    claim = extract_claim(
        row["user_claim"]
    )

    result = analyze_image(
        row["image_paths"],
        claim
    )

    user_hist = history[
        history["user_id"]
        ==
        row["user_id"]
    ]

    if len(user_hist):
        user_hist = (
            user_hist.iloc[0]
        )

    risk_flags = (
        build_risk_flags(
            user_hist
        )
    )

    status, justification = (
        determine_status(
            claim["issue_type"],
            result["issue_type"],
            result[
                "evidence_standard_met"
            ]
        )
    )

    rows.append({
        "user_id":
            row["user_id"],
        "image_paths":
            row["image_paths"],
        "user_claim":
            row["user_claim"],
        "claim_object":
            row["claim_object"],
        "evidence_standard_met":
            str(
                result[
                    "evidence_standard_met"
                ]
            ).lower(),
        "evidence_standard_met_reason":
            result[
                "evidence_reason"
            ],
        "risk_flags":
            risk_flags,
        "issue_type":
            claim["issue_type"],
        "object_part":
            claim["object_part"],
        "claim_status":
            status,
        "claim_status_justification":
            justification,
        "supporting_image_ids":
            ";".join(result.get("supporting_images", [])) if result.get("supporting_images") else "none",
        "valid_image":
            str(
                result[
                    "valid_image"
                ]
            ).lower(),
        "severity":
            result[
                "severity"
            ]
    })

# Save generated outputs to output.csv
pd.DataFrame(rows).to_csv(
    "output.csv",
    index=False
)

print(
    "output.csv generated"
)
