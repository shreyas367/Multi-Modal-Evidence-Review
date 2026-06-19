from src.claim_extractor import extract_claim

claim = """
The rear bumper has a dent.
"""

print(
    extract_claim(claim)
)