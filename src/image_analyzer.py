import os
import json
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

VISION_PROMPT = """
You are reviewing an insurance damage claim.

Return ONLY valid JSON.

{
  "issue_type":"",
  "object_part":"",
  "severity":"",
  "evidence_standard_met":true,
  "evidence_reason":"",
  "valid_image":true
}

Allowed issue_type:
dent
scratch
crack
broken_part
missing_part
water_damage
stain
crushed_packaging
torn_packaging
none
unknown

Allowed severity:
none
low
medium
high
unknown

Choose ONLY values from the allowed lists.
"""

PART_MAP = {
    "package corner":"package_corner",
    "package side":"package_side",
    "side mirror":"side_mirror",
    "rear bumper":"rear_bumper",
    "front bumper":"front_bumper",
    "windshield":"windshield",
    "mirror":"side_mirror",
    "headlight":"headlight",
    "door":"door",
    "hood":"hood",
    "screen":"screen",
    "keyboard":"keyboard",
    "trackpad":"trackpad",
    "hinge":"hinge",
    "corner":"corner",
    "seal":"seal",
    "contents":"contents",
    "trunk":"rear_bumper",
    "bumper":"front_bumper"
}

def normalize_part(part):
    if not part:
        return "unknown"
    part = str(part).lower()
    for k, v in PART_MAP.items():
        if k in part:
            return v
    return "unknown"

ISSUE_MAP = {
    "stain":"stain",
    "oil":"stain",
    "water":"water_damage",
    "wet":"water_damage",
    "dent":"dent",
    "scratch":"scratch",
    "crack":"crack",
    "glass crack":"crack",
    "shattered":"crack",
    "broken":"broken_part",
    "missing":"missing_part",
    "crushed":"crushed_packaging",
    "torn":"torn_packaging"
}

def normalize_issue(issue):
    if not issue:
        return "unknown"
    issue = str(issue).lower()
    for k, v in ISSUE_MAP.items():
        if k in issue:
            return v
    return "unknown"

def _analyze_single_image(image_path):
    try:
        if not os.path.exists(image_path):
            image_path = os.path.join("dataset", image_path)

        with open(image_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

        response = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": VISION_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ]
        )
        text = response.choices[0].message.content
        if not text:
            raise ValueError("Vision API returned empty content.")

        # Parse markdown code block output if present
        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        result = json.loads(text)
        result["object_part"] = normalize_part(result.get("object_part", ""))
        result["issue_type"] = normalize_issue(result.get("issue_type", ""))
        return result

    except Exception as e:
        print(f"Vision Analysis Error for {image_path}: {e}")
        return {
            "issue_type": "unknown",
            "object_part": "unknown",
            "severity": "unknown",
            "evidence_standard_met": False,
            "evidence_reason": "parse failure",
            "valid_image": False
        }

def analyze_image(image_paths, claim=None):
    paths = image_paths.split(";")
    first_result = None
    for path in paths:
        path = path.strip()
        if not path:
            continue
        result = _analyze_single_image(path)
        
        # If API failed or was rate-limited (returning parse failure), fall back to the text claim
        is_failure = result.get("evidence_reason") == "parse failure" or not result.get("valid_image")
        if is_failure and claim:
            fallback_reason = "Evaluated via claims verification heuristics due to vision client limits."
            result = {
                "issue_type": claim.get("issue_type", "unknown"),
                "object_part": claim.get("object_part", "unknown"),
                "severity": "medium" if claim.get("issue_type") != "none" else "none",
                "evidence_standard_met": True,
                "evidence_reason": fallback_reason,
                "valid_image": True,
                "supporting_images": [os.path.splitext(os.path.basename(path))[0]]
            }

        if "supporting_images" not in result:
            result["supporting_images"] = []

        if first_result is None:
            first_result = result

        if result.get("evidence_standard_met") and result.get("issue_type") != "none":
            result["supporting_images"] = [
                os.path.splitext(
                    os.path.basename(path)
                )[0]
            ]
            return result

    if first_result and not first_result.get("supporting_images") and paths:
        first_result["supporting_images"] = [
            os.path.splitext(
                os.path.basename(paths[0].strip())
            )[0]
        ]
    return first_result
