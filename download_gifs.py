"""
Health Fundamentals — Exercise GIF Downloader v10
Final 5 remaining exercises.
Run from root of HealthFundamentals repo:
    python download_gifs.py
"""

import urllib.request
import urllib.parse
import json
import os
import time

DEST    = "assets/exercises"
HOST    = "exercisedb.p.rapidapi.com"
API_KEY = "d218665d58msha204d034a27d5f9p10d3f5jsn2cbf861a6dcf"
BASE    = f"https://{HOST}"

HEADERS = {
    "X-RapidAPI-Key":  API_KEY,
    "X-RapidAPI-Host": HOST,
    "User-Agent":      "HealthFundamentals/1.0",
}

# Final 5 — broad single-word searches to cast widest net
EXERCISES = {
    "cable-fly":         ["cable fly", "fly", "crossover", "chest cable"],
    "db-shoulder-press": ["shoulder press", "dumbbell press", "overhead dumbbell", "deltoid press"],
    "cable-crunch":      ["cable crunch", "crunch cable", "ab cable", "kneeling crunch"],
    "crunch-machine":    ["crunch machine", "ab machine", "machine ab", "abdominal machine"],
    "woodchop":          ["wood chop", "chop", "cable rotation", "twist cable"],
}

os.makedirs(DEST, exist_ok=True)
print("Health Fundamentals — Exercise GIF Downloader v10")
print("Final 5 exercises")
print("=" * 52)

def api_get(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def download_url(url, use_auth=False):
    h = HEADERS if use_auth else {"User-Agent": "HealthFundamentals/1.0"}
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def is_gif(data):
    return data[:6] in (b'GIF87a', b'GIF89a')

def try_get_gif(term):
    encoded = urllib.parse.quote(term.lower())
    try:
        results = api_get(f"/exercises/name/{encoded}?limit=10&offset=0")
        if not isinstance(results, list) or not results:
            return None, None
        for ex in results:
            ex_id   = ex.get("id", "")
            ex_name = ex.get("name", term)
            if ex_id:
                try:
                    url  = f"{BASE}/image?exerciseId={ex_id}&resolution=360&rapidapi-key={API_KEY}"
                    data = download_url(url, use_auth=True)
                    if is_gif(data) and len(data) > 5000:
                        return data, ex_name
                except:
                    pass
            gif_url = ex.get("gifUrl", "")
            if gif_url:
                try:
                    data = download_url(gif_url)
                    if len(data) > 5000:
                        return data, ex_name
                except:
                    pass
    except:
        pass
    return None, None

ok = 0
failed = []

for key, terms in EXERCISES.items():
    out_path = os.path.join(DEST, f"{key}.gif")

    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            header = f.read(6)
        if header in (b'GIF87a', b'GIF89a'):
            print(f"  skip  {key}  (already animated)")
            continue
        os.remove(out_path)

    found = False
    for term in terms:
        data, name = try_get_gif(term)
        if data and len(data) > 5000:
            with open(out_path, "wb") as f:
                f.write(data)
            tag = "GIF ✓" if is_gif(data) else "static"
            print(f"  ok    {key}.gif  ({len(data)//1024}KB)  [{tag}]  '{name}'")
            ok += 1
            found = True
            break
        time.sleep(0.4)

    if not found:
        print(f"  FAIL  {key}")
        failed.append(key)

    time.sleep(0.5)

print(f"\nDownloaded: {ok}  Failed: {len(failed)}")

if failed:
    print(f"\nStill failed: {failed}")
    print("\nManual download links:")
    links = {
        "cable-fly":         "https://www.google.com/search?q=cable+fly+exercise+animated+gif&tbm=isch",
        "db-shoulder-press": "https://www.google.com/search?q=dumbbell+shoulder+press+exercise+animated+gif&tbm=isch",
        "cable-crunch":      "https://www.google.com/search?q=cable+crunch+exercise+animated+gif&tbm=isch",
        "crunch-machine":    "https://www.google.com/search?q=ab+crunch+machine+exercise+animated+gif&tbm=isch",
        "woodchop":          "https://www.google.com/search?q=cable+woodchop+exercise+animated+gif&tbm=isch",
    }
    for k in failed:
        if k in links:
            print(f"  {k}: {links[k]}")
    print("\nSave each as assets/exercises/<key>.gif")

print("""
Next steps:
  git add assets/exercises/
  git commit -m "Add animated exercise GIFs"
  git push
""")
