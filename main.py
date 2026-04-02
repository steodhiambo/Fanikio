"""
Main runner — execute all agents in sequence
Usage:
    python main.py init        # Initialize database
    python main.py discover    # Run discovery agent (X)
    python main.py score       # Run scoring agent
    python main.py content     # Run content creation agent
    python main.py engage      # Run engagement agent
    python main.py all         # Run full pipeline
"""

import sys
from database.db import init_db
from agents.discovery_agent import run_x_discovery
from agents.scoring_agent import run_scoring
from agents.content_agent import generate_batch, DEFAULT_IDEAS
from agents.engagement_agent import run_engagement


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "help"

    if command == "init":
        init_db()
    elif command == "discover":
        run_x_discovery()
    elif command == "score":
        run_scoring()
    elif command == "content":
        generate_batch(DEFAULT_IDEAS)
    elif command == "engage":
        run_engagement()
    elif command == "all":
        print("=== Step 1: Initializing DB ===")
        init_db()
        print("\n=== Step 2: Discovering People ===")
        run_x_discovery()
        print("\n=== Step 3: Scoring People ===")
        run_scoring()
        print("\n=== Step 4: Generating Content ===")
        generate_batch(DEFAULT_IDEAS)
        print("\n=== Step 5: Generating Engagement Suggestions ===")
        run_engagement()
        print("\nDone. Run: streamlit run dashboard/app.py")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
