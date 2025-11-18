# get json as input, calculate likely passwords

import json
import random
import string
import hashlib

def generate_passwords(json_file_path):
    """
    Takes a JSON file containing a list of 10 user profiles
    and returns a list of 5 generated passwords.
    """

    # --- Load profiles ---
    with open(json_file_path, 'r') as f:
        profiles = json.load(f)

    # Ensure we have at least 10 profiles
    if len(profiles) < 10:
        raise ValueError("JSON file must contain at least 10 profiles.")

    # --- Helper: extract some words from profile fields ---
    def extract_keywords(profile):
        keywords = []
        for value in profile.values():
            if isinstance(value, str):
                parts = value.replace(",", " ").split()
                for p in parts:
                    if len(p) > 2:
                        keywords.append(p)
        return keywords

    # --- Generate passwords ---
    passwords = []
    for _ in range(5):

        # Pick a random profile for inspiration
        profile = random.choice(profiles)
        words = extract_keywords(profile)

        # Pick up to 2 elements from the profile data
        if words:
            base = "".join(random.sample(words, k=min(2, len(words))))
        else:
            base = ''.join(random.choices(string.ascii_letters, k=8))

        # Add randomness: digits + punctuation
        random_part = ''.join(random.choices(
            string.ascii_letters + string.digits + "!@#$%^&*",
            k=6
        ))

        # Hash element to ensure uniqueness
        hash_suffix = hashlib.sha1((base + random_part).encode()).hexdigest()[:4]

        password = base.capitalize() + random_part + hash_suffix
        passwords.append(password)

    return passwords


# Example usage:
result = generate_passwords("profiles.json")
print(result)
