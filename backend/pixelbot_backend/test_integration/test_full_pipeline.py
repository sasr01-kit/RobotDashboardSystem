import sys
import os
import json
import tempfile

from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI

""" This is a full integration test that simulates the entire data pipeline from loading data from the Pixelbot robot, saving it to JSON, 
    and reloading it back. It verifies that the data structure is consistent throughout the process. """

# Update this URL to match your Pixelbot robot's IP address and port. This is the same URL used in main.py for the ChildAPI connection.
ROBOT_URL = "http://192.168.2.70:8000"

# ---- CONNECTION TEST ----
print("=== TESTING ROBOT CONNECTION ===")

repo = DataRepository()
api = ChildAPI(ROBOT_URL, repo)
assert api.is_robot_available(ROBOT_URL), "ERROR: Robot is not reachable!"
print(f"Connection successful! Robot is available at {ROBOT_URL}")

# ---- TEST START ----
print("=== STARTING FULL PIPELINE TEST ===")

with tempfile.TemporaryDirectory() as tmp_dir:
    repo.DATA_FILE = os.path.join(tmp_dir, "children_data.json")
    repo.META_FILE = os.path.join(tmp_dir, "children_meta.json")

    # 1. Load from Pixelbot
    loader = RemoteDataLoader(ROBOT_URL)
    raw_children = loader.load_all_children()
    print("\n[1] Loading children using RemoteDataLoader...")
    print(f"Loaded {len(raw_children)} children.")
    for child in raw_children:
        print(f" - Child: {child.name}, sessions: {len(child.sessions)}")

    # 2. Save to temporary directory
    print("\n[2] Saving children to JSON using DataRepository...")
    children = repo.update_children(raw_children)
    tmp_json = os.path.join(tmp_dir, "children_data.json")
    assert os.path.exists(tmp_json), "ERROR: children_data.json was not saved!"
    print(f"JSON saved successfully: {tmp_json}")

    # 3. Load JSON back
    print("\n[3] Loading children from JSON...")
    reloaded = repo.load_children()
    assert reloaded is not None, "ERROR: Reload failed."
    assert len(reloaded) == len(children), "ERROR: Number of children mismatch after reload."
    print(f"Reloaded {len(reloaded)} children.")

    # 4. Validate JSON structure
    print("\n[4] Validating JSON structure...")
    with open(tmp_json, "r") as f:
        data = json.load(f)
    assert isinstance(data, list), "ERROR: JSON top-level should be a list"
    assert "sessions" in data[0], "ERROR: Missing sessions in JSON output"
    assert "speechWidth" in data[0]["sessions"][0], "ERROR: Missing speechWidth in session JSON"
    print("JSON structure is VALID.")

    # ---- FINAL RESULT ----
    print("\n=== ALL TESTS PASSED SUCCESSFULLY ===")