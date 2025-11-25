import json
import random
import string
from typing import Dict, List, Optional


def extract_keywords(profile: dict) -> List[str]:
    """
    Extract all readable keywords from the profile.
    Passwords will pick different keywords each time.
    """
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

    return keywords


def generate_clean_password(all_keywords: List[str]) -> str:
    """
    Generates a readable password using *new keywords each time*:
        <Keyword><Keyword><symbol><digit>
    If there are not enough keywords, it uses fewer.
    """

    if all_keywords:
        # Pick 1 or 2 new random keywords every time
        k = random.randint(1, min(2, len(all_keywords)))
        chosen = random.sample(all_keywords, k=k)
        core = "".join(word[:4].capitalize() for word in chosen)
    else:
        core = "User"

    symbol = random.choice("!@#$%&?")
    digit = str(random.randint(0, 9))

    return f"{core}{symbol}{digit}"


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

        # Get all keywords once
        all_keywords = extract_keywords(profile)

        # Generate a new keyword combo for every password
        passwords = [
            generate_clean_password(all_keywords)
            for _ in range(count)
        ]

        results[profile_key] = passwords

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    return results


# Example usage:
pw = generate_passwords_for_profiles("generated_profiles.json", "clean_passwords.json")
print(json.dumps(pw, indent=2))
