import json
import random
import string
from typing import Dict, List, Optional

import google.generativeai as genai
from apikey import GEMINI_API_KEY   # Loaded from ignored file


# -------------------------------------------------
# Gemini Setup
# -------------------------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


# -------------------------------------------------
# Keyword extraction
# -------------------------------------------------
def extract_keywords(profile: dict) -> List[str]:
    keywords = []

    for value in profile.values():
        if isinstance(value, str):
            words = value.replace(",", " ").split()
            words = [w for w in words if len(w) >= 3]
            keywords.extend(words)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and len(item) >= 3:
                    keywords.append(item)

    return list(set(keywords))  # Deduplicate


# -------------------------------------------------
# Validate password format
# -------------------------------------------------
def password_valid(pw: str) -> bool:
    return (
        12 <= len(pw) <= 15
        and any(c.islower() for c in pw)
        and any(c.isupper() for c in pw)
        and any(c.isdigit() for c in pw)
        and any(c in "!@#$%&*?+" for c in pw)
        and " " not in pw
        and "\n" not in pw
    )


# -------------------------------------------------
# Local fallback (if API output is invalid)
# -------------------------------------------------
def fallback_password(keywords: List[str]) -> str:
    base = ""

    # Use fragments of keywords
    if keywords:
        selected = random.sample(keywords, k=min(2, len(keywords)))
        base = "".join(word[:3].capitalize() for word in selected)

    # Add randomness
    while len(base) < 12:
        base += random.choice(string.ascii_letters + string.digits + "!@#$%&*?+")

    # Trim to max length
    return base[:15]


# -------------------------------------------------
# Gemini-generated password
# -------------------------------------------------
def generate_gemini_password(keywords: List[str]) -> str:
    prompt = f"""
    Generate one predictable password using these keywords as inspiration:
    {keywords}

    Requirements:
    - Must be between 10 and 15 characters long
    - Must include uppercase, lowercase, numbers, and symbols
    - Must NOT include spaces
    - Return ONLY the password string, with no quotes and no explanation
    """

    try:
        response = model.generate_content(prompt)
        pw = response.text.strip().replace(" ", "").replace("\n", "")
    except Exception:
        return fallback_password(keywords)

    if not password_valid(pw):
        return fallback_password(keywords)

    return pw


# -------------------------------------------------
# Main generation engine
# -------------------------------------------------
def generate_passwords_for_profiles(json_file: str,
                                    output_file: Optional[str] = None,
                                    count: int = 5) -> Dict[str, List[str]]:

    with open(json_file, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    results: Dict[str, List[str]] = {}

    for profile in profiles:
        profile_key = (
            profile.get("student_id")
            or profile.get("id")
            or profile.get("name")
            or f"profile_{len(results)+1}"
        )

        keywords = extract_keywords(profile)

        passwords = [generate_gemini_password(keywords) for _ in range(count)]

        results[profile_key] = passwords

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    return results


# -------------------------------------------------
# Script entry point
# -------------------------------------------------
if __name__ == "__main__":
    import os

    base = os.path.dirname(__file__)
    profiles_path = os.path.join(base, "generated_profiles.json")
    output_path = os.path.join(base, "clean_passwordsAI.json")

    pw = generate_passwords_for_profiles(profiles_path, output_path)
    print(json.dumps(pw, indent=2))
