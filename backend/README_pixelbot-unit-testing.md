# Running Unit Tests — Pixelbot Backend
## This guide walks you through everything you need to do after cloning the repository to run the unit tests locally.
## Prerequisites
You need Python 3.10 or higher installed on your machine. To check, open a terminal and run:

python3 --version

## Step 1 — Navigate to the repository
 
Open a terminal and navigate to the root of the cloned repository:
 
```bash
cd ~/ros2_ws/src/RobotDashboardSystem
```

Make sure you have the following installed (inside your virtual environment if you are using one):

```bash
pip install pytest pytest-cov requests
```
Or install everything at once using the requirements file:
```bash
bashpip install -r requirements.txt
```

## Step 2 - Running Unit Tests
Run the unit tests from the backend folder:

```bash
python -m pytest pixelbot_backend/test/ --cov=pixelbot_backend --cov-report=term-missing
```

Notes:
Unit tests use MagicMock and @patch to isolate classes, so no real robot or files are needed.

Integration tests write to a tempfile.TemporaryDirectory(), so no real data files are modified.

The conftest.py in the backend root folder is required for Python imports to work correctly, do not delete it.

If you see ModuleNotFoundError: No module named 'pixelbot_backend', make sure you are running commands from the backend folder and not from a parent directory.
