from pathlib import Path
import json
from datetime import datetime
from typing import Any, Dict

# Go up to backend/
BACKEND_ROOT = Path(__file__).resolve().parents[1]

# Saved JSON snapshots can be found in:
# turtlebot4_backend/turtlebot4_storage/path_history_snapshots/
SNAPSHOT_DIR = BACKEND_ROOT / "turtlebot4_storage" / "path_history_snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

def _safe_ts() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H-%M-%SZ")

def save_path_history(path_model) -> Path:
    """
    Save pathHistory into a timestamped JSON file.
    """
    payload: Dict[str, Any] = {
        "savedAt": datetime.now().astimezone().isoformat(),
        "pathHistory": [
            {
                "label": e.get_label(),
                "id": e.get_id(),
                "goalType": e.get_goal_type(),
                "timestamp": e.get_timestamp().isoformat() if e.get_timestamp() else None,
                "fuzzyOutput": e.get_fuzzy_output(),
                "userFeedback": e.get_user_feedback(),
            }
            for e in path_model.get_path_history()
        ],
    }

    file_path = SNAPSHOT_DIR / f"path_history_{_safe_ts()}.json"
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return file_path

def load_latest_path_history() -> Dict[str, Any]:
    # Find newest file by name and timestamp
    files = sorted(SNAPSHOT_DIR.glob("path_history_*.json"))
    if not files:
        return {"pathHistory": [], "savedAt": None}

    latest = files[-1]
    data = json.loads(latest.read_text(encoding="utf-8"))

    return {
        "pathHistory": data.get("pathHistory", []),
        "savedAt": data.get("savedAt"),
        "filename": latest.name,
    }