"""
Health Fundamentals — Exercise GIF Downloader
Run from the root of your HealthFundamentals repo:
    python download_gifs.py
"""

import urllib.request
import os
import time

DEST = "assets/exercises"
BASE_URL = "https://wger.de/static/images/exercises/main"

GIFS = {
    "bench-press":       "105",
    "incline-db-press":  "305",
    "cable-fly":         "172",
    "chest-dip":         "202",
    "pec-deck":          "314",
    "db-chest-press":    "301",
    "lat-pulldown":      "122",
    "barbell-row":       "109",
    "cable-row":         "175",
    "db-row":            "213",
    "pull-up":           "194",
    "face-pull":         "313",
    "back-squat":        "111",
    "rdl":               "191",
    "leg-press":         "126",
    "split-squat":       "206",
    "leg-curl":          "128",
    "leg-extension":     "127",
    "ohp":               "113",
    "db-shoulder-press": "115",
    "lateral-raise":     "130",
    "rear-delt-fly":     "312",
    "arnold-press":      "197",
    "cable-lateral":     "232",
    "barbell-curl":      "108",
    "hammer-curl":       "123",
    "incline-curl":      "350",
    "close-grip-bench":  "121",
    "tricep-pushdown":   "133",
    "overhead-tri":      "220",
    "hip-thrust":        "370",
    "glute-bridge":      "198",
    "cable-kickback":    "222",
    "hanging-leg-raise": "124",
    "cable-crunch":      "173",
    "plank":             "187",
    "bicycle-crunch":    "168",
    "pallof-press":      "371",
    "crunch-machine":    "185",
    "band-walk":         "372",
    "goblet-squat":      "209",
    "reverse-lunge":     "200",
    "step-up":           "255",
    "push-up":           "192",
    "cable-curl":        "176",
    "woodchop":          "373",
}

os.makedirs(DEST, exist_ok=True)
print(f"Saving to: {os.path.abspath(DEST)}\n")

total   = len(GIFS)
ok      = 0
skipped = 0
failed  = []

for key, wger_id in GIFS.items():
    out_path = os.path.join(DEST, f"{key}.gif")
    url      = f"{BASE_URL}/{wger_id}.gif"

    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"  skip  {key}.gif  (already exists, {size//1024}KB)")
        skipped += 1
        continue

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HealthFundamentals/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(out_path, "wb") as f:
            f.write(data)
        size = len(data)
        print(f"  ok    {key}.gif  ({size//1024}KB)")
        ok += 1
    except Exception as e:
        print(f"  FAIL  {key}.gif  ({e})")
        failed.append(key)

    time.sleep(0.4)

print(f"\n{'='*50}")
print(f"Downloaded : {ok}")
print(f"Skipped    : {skipped}")
print(f"Failed     : {len(failed)}")

if failed:
    print(f"\nFailed downloads:")
    for k in failed:
        print(f"  {k}  (ID: {GIFS[k]})")
    print(f"\nFor failed ones, go to https://wger.de/en/exercise/{{}}/view/")
    print("Download the GIF manually and save it as assets/exercises/<name>.gif")

print(f"""
Next steps:
  1. git add assets/exercises/
  2. git commit -m "Add exercise GIFs"
  3. git push

Done! Your GIFs will be live at:
  https://cjrochest.github.io/HealthFundamentals/assets/exercises/<name>.gif
""")
