import os
import json

from pixelbot_backend.pixelbot_storage.DataLoader import DataLoader
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository

# ---- CONFIG ----
DATA_ROOT = "C:/Users/kelly/Desktop/Uni/PSE/pse_data_example/saved_drawing"
OUTPUT_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "pixelbot_storage",
    "children_data.json"
)


# ---- TEST START ----
print("=== STARTING FULL PIPELINE TEST ===")

# 1. Load from disk using your DataLoader
# If you're connected to Pixelbot, you can use RemoteDataLoader instead.
print("\n[1] Loading children using DataLoader...")
loader = DataLoader(DATA_ROOT)
children = loader.load_all_children()

assert len(children) > 0, "ERROR: No children loaded! Check data_root."
print(f"Loaded {len(children)} children.")

for child in children:
    print(f" - Child: {child.child_id}, sessions: {len(child.sessions)}")

# 2. Save using your DataRepository
print("\n[2] Saving children to JSON using DataRepository...")
repo = DataRepository()
repo.save_children(children)

assert os.path.exists(OUTPUT_JSON), "ERROR: children_data.json was not saved!"
print(f"JSON saved successfully: {OUTPUT_JSON}")

# 3. Load JSON back
print("\n[3] Loading children from JSON...")
reloaded = repo.load_children()

assert reloaded is not None, "ERROR: Reload failed: DataRepository returned None."
assert len(reloaded) == len(children), "ERROR: Number of children mismatch after reload."

print(f"Reloaded {len(reloaded)} children.")

# 4. Validate JSON content
print("\n[4] Validating JSON structure...")
with open(OUTPUT_JSON, "r") as f:
    data = json.load(f)

assert isinstance(data, list), "ERROR: JSON top-level should be a list"
assert "sessions" in data[0], "ERROR: Missing sessions in JSON output"
assert "speechWidth" in data[0]["sessions"][0], "ERROR: Missing speechWidth in session JSON"

print("JSON structure is VALID.")

# ---- FINAL RESULT ----
print("\n=== ALL TESTS PASSED SUCCESSFULLY ===")