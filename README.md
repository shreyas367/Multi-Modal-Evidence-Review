# AI Claims Verification System

An automated insurance claims verification pipeline that evaluates customer claim transcripts and submitted image evidence using Google Gemini's multimodal LLM.

## Project Structure

```
project/
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── claim_extractor.py
│   ├── image_analyzer.py
│   ├── verifier.py
│   └── utils.py
│
├── evaluation/
│   ├── main.py
│   └── evaluation_report.md
```

## Setup & Configuration

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your Gemini API Key in the `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

## Running the Pipeline

To run the verification pipeline on a claims dataset (defaults to `dataset/claims.csv`):
```bash
python main.py
```

### Options:
- `--input`: Custom input CSV file name in the `dataset/` directory (e.g. `--input sample_claims.csv`).
- `--output`: Custom output CSV file name to save in the `dataset/` directory (e.g. `--output verified_claims.csv`).

## Running Evaluation

To evaluate the system against the ground truth dataset (`dataset/sample_claims.csv`) and output accuracy metrics:
```bash
python evaluation/main.py
```
This command runs the evaluation pipeline and generates a markdown report detailing the performance metrics and case breakdowns at `evaluation/evaluation_report.md`.
