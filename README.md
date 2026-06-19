# Multi-Modal Evidence Review System

## Overview

This project is a multimodal claim verification system developed for the HackerRank Orchestrate Hackathon.

The system reviews insurance-style damage claims for:

* Car
* Laptop
* Package

Each claim contains:

* User conversation
* One or more submitted images
* User claim history
* Evidence requirements

The system determines whether image evidence supports, contradicts, or is insufficient to verify the claim.

---

## System Architecture

### 1. Claim Extraction Layer

The claim conversation is analyzed using a rule-based extractor.

The extractor identifies:

* Issue Type
* Object Part

Examples:

* "rear bumper dent" → dent, rear_bumper
* "screen cracked" → crack, screen
* "package corner crushed" → crushed_packaging, package_corner

---

### 2. Vision Analysis Layer

Images are analyzed using a vision-capable LLM.

The vision model determines:

* Visible damage type
* Damaged object part
* Severity
* Evidence quality

Returned information is normalized into the allowed challenge labels.

---

### 3. Verification Layer

The verifier compares:

* Claimed issue
* Visual evidence

and produces one of:

* supported
* contradicted
* not_enough_information

---

### 4. Risk Assessment Layer

User history is analyzed using:

* past_claim_count
* rejected_claim
* manual_review_claim
* history_flags

Risk flags generated:

* user_history_risk
* manual_review_required

Risk information provides context but does not override visual evidence.

---

### 5. Output Generation

The system generates:

output.csv

with the exact schema required by the challenge.

---

## Project Structure

project/

├── main.py

├── requirements.txt

├── src/

│   ├── claim_extractor.py

│   ├── image_analyzer.py

│   ├── verifier.py

│   └── utils.py

├── evaluation/

│   ├── main.py

│   └── evaluation_report.md

└── output.csv

---

## Setup Instructions

### 1. Create Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / Mac:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=YOUR_API_KEY
```

or

```env
GEMINI_API_KEY=YOUR_API_KEY
```

depending on the configured vision backend.

---

### 4. Dataset Placement

Place the provided dataset in:

```text
dataset/
├── claims.csv
├── sample_claims.csv
├── user_history.csv
├── evidence_requirements.csv
└── images/
```

---

### 5. Run Evaluation

```bash
python evaluation/main.py
```

This evaluates the claim extractor on the sample dataset.

---

### 6. Generate Predictions

```bash
python main.py
```

Generated file:

```text
output.csv
```

---

## Methodology

### Claim Extraction

A rule-based NLP layer extracts:

* issue_type
* object_part

from claim conversations.

The extractor was evaluated on the provided sample dataset.

---

### Image Understanding

Images are sent to a vision-capable LLM.

The model returns structured JSON containing:

* issue_type
* object_part
* severity
* evidence quality

The output is normalized into challenge-compliant labels.

---

### Decision Logic

The verifier applies:

* Evidence sufficiency checks
* Claim-to-image consistency checks
* Contradiction detection
* Insufficient evidence handling

---

### Risk Handling

Historical user behavior is used to generate risk flags.

Risk flags provide review context but do not override image evidence.

---

## Output Schema

Generated columns:

* user_id
* image_paths
* user_claim
* claim_object
* evidence_standard_met
* evidence_standard_met_reason
* risk_flags
* issue_type
* object_part
* claim_status
* claim_status_justification
* supporting_image_ids
* valid_image
* severity

---

## Notes

* Images are treated as the primary source of truth.
* User history is used only as contextual risk information.
* The system avoids hardcoded labels and evaluates each claim independently.
* Multiple images are supported per claim.
