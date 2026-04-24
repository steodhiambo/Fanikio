import os
import sys
import sqlite3
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"

def ok(msg):  print(f"  \033[92m✔\033[0m  {msg}")
def warn(msg): print(f"  \033[93m⚠\033[0m  {msg}")
def err(msg):  print(f"  \033[91m✘\033[0m  {msg}")

def check_python():
    print("\n── Python ──────────────────────────────")
    v = sys.version_info
    if v >= (3, 9):
        ok(f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        err(f"Python {v.major}.{v.minor} — requires 3.9+")

def check_env():
    print("\n── Environment Variables ───────────────")
    required = {"OPENAI_API_KEY": "AI content generation"}
    optional = {
        "X_BEARER_TOKEN":  "X (Twitter) discovery",
        "X_API_KEY":       "X posting",
        "X_API_SECRET":    "X posting",
        "X_ACCESS_TOKEN":  "X posting",
        "X_ACCESS_SECRET": "X posting",
    }
    for var, purpose in required.items():
        val = os.getenv(var, "")
        if val and "your_" not in val:
            ok(f"{var}  ({purpose})")
        else:
            err(f"{var} missing  — needed for {purpose}")

    for var, purpose in optional.items():
        val = os.getenv(var, "")
        if val and "your_" not in val:
            ok(f"{var}  ({purpose})")
        else:
            warn(f"{var} not set  — optional for {purpose}")

def check_db():
    print("\n── Database ────────────────────────────")
    if USE_SQLITE:
        db_path = "fanikio.db"
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                tables = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
                conn.close()
                names = [t[0] for t in tables]
                expected = {"people", "posts", "engagement_suggestions", "weekly_metrics"}
                missing = expected - set(names)
                if missing:
                    warn(f"SQLite DB found but missing tables: {missing}")
                    warn("Run: python main.py init")
                else:
                    ok(f"SQLite DB ready  ({len(names)} tables)")
            except Exception as e:
                err(f"SQLite error: {e}")
        else:
            warn("fanikio.db not found — run: python main.py init")
    else:
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", 5432),
                dbname=os.getenv("DB_NAME", "fanikio"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
            ok("PostgreSQL connection successful")
            conn.close()
        except Exception as e:
            err(f"PostgreSQL connection failed: {e}")

def check_deps():
    print("\n── Dependencies ────────────────────────")
    deps = [
        ("streamlit",    "Dashboard UI"),
        ("openai",       "AI content generation"),
        ("tweepy",       "X (Twitter) API"),
        ("pandas",       "Data processing"),
        ("dotenv",       "Environment config"),
    ]
    for pkg, purpose in deps:
        try:
            __import__(pkg if pkg != "dotenv" else "dotenv")
            ok(f"{pkg}  ({purpose})")
        except ImportError:
            err(f"{pkg} not installed  — pip install {pkg}")

def check_dashboard():
    print("\n── Dashboard Files ─────────────────────")
    files = [
        "dashboard/app.py",
        "dashboard/ui_utils.py",
        "dashboard/pages/1_Networking.py",
        "dashboard/pages/2_Content.py",
        "dashboard/pages/3_Engagement.py",
    ]
    for f in files:
        if os.path.exists(f):
            ok(f)
        else:
            err(f"{f} missing")

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════╗")
    print("║     Fanikio — Setup Check v2.0       ║")
    print("╚══════════════════════════════════════╝")
    check_python()
    check_env()
    check_db()
    check_deps()
    check_dashboard()
    print("\n── Done ────────────────────────────────")
    print("  Run:  streamlit run dashboard/app.py\n")
