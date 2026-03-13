import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository

# ---- CONFIG ----
ROBOT_URL = "http://192.168.2.70:8000"

# ---- TEST START ----
print("=== TESTING ROBOT CONNECTION ===")

api = ChildAPI(ROBOT_URL, DataRepository())
is_available = api.is_robot_available(ROBOT_URL)

assert is_available, "ERROR: Robot is not reachable! Check the URL and network connection."
print(f"Connection successful! Robot is available at {ROBOT_URL}")

print("\n=== CONNECTION TEST PASSED ===")