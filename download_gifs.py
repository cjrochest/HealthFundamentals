"""
Health Fundamentals — Exercise Image Downloader v5
Targets only the 8 remaining failures using free-exercise-db (public domain JPGs)
which has hip thrust, glute bridge, overhead press, lateral raise etc.
Run from root of your HealthFundamentals repo:
    python download_gifs.py
"""

import urllib.request
import urllib.parse
import json
import os
import time

DEST = "assets/exercises"

# Source 1: Wger API (name search)
WGER_API = "https://wger.de/api/v2"

# Source 2: free-exercise-db on GitHub (public domain, ~800 exercises as JPG)
FREE_DB = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises"

# Only the 8 still-missing exercises
# Format: key -> [ (source, value), ... ]
# source "wger" = search term, source "freedb" = exact folder name in free-exercise-db
EXERCISES = {
    "ohp":               [("freedb", "Barbell_Full_Squat"),          ("wger", "Push Press")],
    "db-shoulder-press": [("freedb", "Dumbbell_Shoulder_Press"),     ("wger", "Dumbbell Shoulder Press")],
    "lateral-raise":     [("freedb", "Side_Lateral_Raise"),          ("wger", "Dumbbell Lateral Raise")],
    "rear-delt-fly":     [("freedb", "Seated_Bent_Over_Rear_Delt_Raise"), ("wger", "Bent Over Lateral Raise")],
    "cable-lateral":     [("freedb", "Cable_Shoulder_Press"),        ("wger", "Cable Lateral Raise")],
    "incline-curl":      [("freedb", "Alternate_Incline_Dumbbell_Curl"), ("wger", "Incline Dumbbell Curl")],
    "overhead-tri":      [("freedb", "Seated_Triceps_Press"),        ("wger", "Triceps Extension")],
    "hip-thrust":        [("freedb", "Barbell_Hip_Thrust"),          ("wger", "Hip Thrust")],
    "glute-bridge":      [("freedb", "Glute_Bridge"),                ("wger", "Glute Bridge")],
    "cable-kickback":    [("freedb", "Cable_Hip_Adduction"),         ("wger", "Cable Kickback")],
    "hanging-leg-raise": [("freedb", "Hanging_Leg_Raise"),           ("wger", "Hanging Leg Raise")],
    "plank":             [("freedb", "Front_Plank_with_Elbows"),     ("wger", "Front Plank")],
    "step-up":           [("freedb", "Dumbbell_Step_Ups"),           ("wger", "Step Up")],
    "cable-curl":        [("freedb", "Cable_Hammer_Curls_-_Rope_Attachment"), ("wger", "Cable Curl")],
}

os.makedirs(DEST, exist_ok=True)
print("Health Fundamentals — Exercise Image Downloader v5")
print("=" * 52)
print(f"Saving to: {os.path.abspath(DEST)}\n")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HealthFundamentals/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read()

def fetch_json(url):
    return json.loads(fetch(url))

def try_freedb(folder):
    """Try downloading from free-exercise-db using folder name."""
    for idx in ["0", "1"]:
        for ext in ["jpg", "jpeg", "png", "gif"]:
            url = f"{FREE_DB}/{folder}/{idx}.{ext}"
            try:
                data = fetch(url)
                if len(data) > 5000:  # real image, not error page
                    return data, url
            except:
                pass
    return None, None

def try_wger(search_term):
    """Try downloading from Wger via name search."""
    try:
        encoded = urllib.parse.quote(search_term)
        url = f"{WGER_API}/exercise/search/?term={encoded}&language=english&format=json"
        data = fetch_json(url)
        suggestions = data.get("suggestions", [])
        if not suggestions:
            return None, None
        exercise_id = suggestions[0].get("data", {}).get("base_id")
        if not exercise_id:
            return None, None
        imgs_url = f"{WGER_API}/exerciseimage/?exercise={exercise_id}&format=json"
        imgs = fetch_json(imgs_url).get("results", [])
        if not imgs:
            return None, None
        img_url = next((i["image"] for i in imgs if i.get("is_main")), imgs[0]["image"])
        img_data = fetch(img_url)
        return img_data, img_url
    except:
        return None, None

ok = 0
skipped = 0
failed = []

for key, sources in EXERCISES.items():
    out_path = os.path.join(DEST, f"{key}.gif")

    if os.path.exists(out_path):
        size = os.path.getsize(out_path) // 1024
        print(f"  skip  {key}  ({size}KB)")
        skipped += 1
        continue

    found = False
    for source_type, value in sources:
        try:
            if source_type == "freedb":
                data, src_url = try_freedb(value)
            else:
                data, src_url = try_wger(value)

            if data and len(data) > 5000:
                with open(out_path, "wb") as f:
                    f.write(data)
                fname = src_url.split("/")[-1] if src_url else "?"
                print(f"  ok    {key}.gif  ({len(data)//1024}KB)  [{fname}]")
                ok += 1
                found = True
                break
        except Exception as e:
            pass
        time.sleep(0.3)

    if not found:
        print(f"  FAIL  {key}")
        failed.append(key)

    time.sleep(0.4)

print(f"\n{'=' * 52}")
print(f"Downloaded : {ok}")
print(f"Skipped    : {skipped}")
print(f"Failed     : {len(failed)}")

if failed:
    print(f"\nStill failed: {failed}")
    print("For these, manually find a GIF online, name it <key>.gif")
    print("and drop it into assets/exercises/")

if ok > 0 or skipped > 0:
    print("""
Next steps:
  git add assets/exercises/
  git commit -m "Add exercise images"
  git push
""")
