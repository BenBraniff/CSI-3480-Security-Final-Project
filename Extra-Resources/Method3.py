from difflib import SequenceMatcher

# Show how minimal information can identify a unique person.

known_people = {
    "John Doe": "1993, Detroit, basketball, software engineer",
    "Maria Lopez": "1998, Chicago, biology, piano",
    "Sam Carter": "1995, Troy, cybersecurity student"
}

mystery_profile = "Troy, 1995, loves computers"

best_match = max(known_people, key=lambda person:
                 SequenceMatcher(None, known_people[person], mystery_profile).ratio())

print("Most likely identity:", best_match)
