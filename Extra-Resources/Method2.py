import re

# Goal: Show that AI can identify sensitive data in a text block.

text = """John Doe, SSN 555-21-9876, lives at 123 Elm Street.
Credit card: 4242 4242 4242 4242 exp 02/26"""

patterns = {
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b"
}

for label, pattern in patterns.items():
    match = re.search(pattern, text)
    if match:
        print(f"Detected {label}: {match.group()}")
