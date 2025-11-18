"""GenerateProfiles

Utilities to create student profile dictionaries and export them as JSON.

Functions:
  - profiles_to_json(profiles, output_dir=None, prefix="profile") -> List[str]
  - generate_profiles(n, start_id=10001, seed=None) -> List[Dict]

The module can be run as a script; it will generate 10 sample profiles,
write individual JSON files into a `profiles_output` folder next to the
script, and also write a combined `generated_profiles.json` file.
"""

from typing import List, Dict, Optional, Union
import json
import os
import random
from datetime import datetime


def profiles_to_json(profiles: Union[Dict, List[Dict]], output_dir: Optional[str] = None, prefix: str = "profile") -> List[str]:
    """Convert profile dict(s) to JSON string(s) and optionally write to files.

    Args:
        profiles: a single dict or a list of dicts representing profiles.
        output_dir: if provided, directory to write each profile as a file. If None, no files are written.
        prefix: filename prefix when writing files.

    Returns:
        If output_dir is None: a list of JSON strings (one per profile).
        If output_dir is provided: a list of file paths written.

    Raises:
        TypeError: if profiles is not a dict or list of dicts.
    """
    # Normalize to a list
    if isinstance(profiles, dict):
        profiles_list = [profiles]
    elif isinstance(profiles, list):
        profiles_list = profiles
    else:
        raise TypeError("profiles must be a dict or list of dicts")

    # Validate contents are dicts
    for idx, p in enumerate(profiles_list, start=1):
        if not isinstance(p, dict):
            raise TypeError(f"profile at position {idx} is not a dict")

    # Prepare output
    json_strings: List[str] = []
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    for i, p in enumerate(profiles_list, start=1):
        js = json.dumps(p, indent=2)
        json_strings.append(js)
        if output_dir:
            filename = f"{prefix}_{i}.json"
            path = os.path.join(output_dir, filename)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(js)

    if output_dir:
        # return the list of written file paths
        written_paths = [os.path.join(output_dir, f"{prefix}_{i}.json") for i in range(1, len(profiles_list) + 1)]
        return written_paths

    return json_strings


def generate_profiles(n: int, start_id: int = 10001, seed: Optional[int] = None) -> List[Dict]:
    """Generate n synthetic student profile dictionaries.

    Args:
        n: number of profiles to generate.
        start_id: numeric part of the first student_id (e.g. 10001 -> S10001).
        seed: optional random seed for reproducibility.

    Returns:
        List of profile dicts.
    """
    if seed is not None:
        random.seed(seed)

    first_names = ["Avery","Riley","Jordan","Morgan","Taylor","Casey","Dakota","Skyler","Peyton","Quinn","Emery","Hayden","Rowan","Reese","Ari","Rowan","Sloan","Parker","Finley","Elliot"]
    last_names = ["Johnson","Chen","Patel","Alvarez","Brooks","Nguyen","Rivera","Thompson","Garcia","Lee","Foster","Morgan","Brooks","Carter","Sharma","Kim","Rivera","Simmons","Ortiz","Park"]
    schools = ["Westbridge University","Northfield College","Eastlake Institute","Grandview University","Riverside College","Summit Technical University","Prairie State College","Harbor Bay University","Lakeshore University","Crestview College","Metro Arts Academy","Elmwood University","Greenfield College","Blue Ridge Institute","Silverbay University","Oakmont College","Coastal Technical","Valleyview University","Pioneer College","Metropolis University"]
    majors = ["Computer Science","Electrical Engineering","Biology","Finance","Psychology","Information Systems","Environmental Science","Mechanical Engineering","Marketing","Mathematics","Graphic Design","Chemistry","Education","History","Economics","Nursing","Civil Engineering","Anthropology","Theatre","Data Science"]
    cities = ["Maplewood","Cedar Falls","Riverton","Harbor City","Elm Grove","Lakeview","Greencroft","Northport","Briarwood","Stonebridge","Ashford","Fox Hollow","Willow Creek","Meadowbrook","Ridgeview","Harper's Glen","Mariner's Bay","Brookland","Stone Harbor","Kingsport"]
    states = ["OH","IA","NJ","CA","WI","MN","IL","WA","TX","PA","OR","MA","KY","VA","NY","NC","FL","OH","MD","CO"]
    interests_pool = ["coding","robotics","chess","hiking","photography","volunteering","running","investing","debate","art","music","community service","cycling","gaming","conservation","kayaking","design","3D printing","blogging","puzzles","teaching","illustration","theater","cooking","tutoring","reading","policy","tennis","yoga","sailing","fieldwork","acting","machine learning"]

    profiles: List[Dict] = []
    current_year = datetime.now().year
    for i in range(n):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        school = schools[i % len(schools)]
        major = majors[i % len(majors)]
        city = cities[i % len(cities)]
        state = states[i % len(states)]
        age = random.randint(18, 24)
        # graduation year between current_year and current_year + 5
        graduation_year = current_year + random.randint(0, 5)
        gpa = round(random.uniform(2.5, 4.0), 2)
        sid = f"S{start_id + i}"
        # build a simple school-based email domain
        domain = ''.join(ch for ch in school.lower() if ch.isalnum()) + ".edu"
        email = f"{first.lower()}.{last.lower()}@{domain}"
        interests = random.sample(interests_pool, k=3)

        profile = {
            "student_id": sid,
            "name": name,
            "age": age,
            "school": school,
            "major": major,
            "graduation_year": graduation_year,
            "gpa": gpa,
            "email": email,
            "city": city,
            "state": state,
            "interests": interests,
        }
        profiles.append(profile)

    return profiles


if __name__ == "__main__":
    # Generate 10 profiles with no fixed seed (different each time) and create timestamped output.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    demo_profiles = generate_profiles(10, start_id=10001, seed=None)
    out_dir = os.path.join(os.path.dirname(__file__), f"profiles_output_{timestamp}")
    written = profiles_to_json(demo_profiles, output_dir=out_dir)

    # Also write a combined JSON file for convenience with timestamp.
    combined_path = os.path.join(os.path.dirname(__file__), f"generated_profiles_{timestamp}.json")
    with open(combined_path, "w", encoding="utf-8") as fh:
        json.dump(demo_profiles, fh, indent=2)

    print(f"Wrote {len(written)} files to {out_dir}")
    for p in written:
        print(" -", p)
    print(f"Also wrote combined file: {combined_path}")
