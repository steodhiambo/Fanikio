# Fanikio — AI Personal Brand Growth System

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your keys in .env
```

### 3. Create PostgreSQL database
```bash
psql -U postgres -c "CREATE DATABASE fanikio;"
```

### 4. Initialize database
```bash
python main.py init
```

---

## Usage

```bash
# Run full pipeline
python main.py all

# Or run each agent individually
python main.py discover    # Find people on X
python main.py score       # Score and rank people
python main.py content     # Generate posts
python main.py engage      # Generate comment suggestions

# Add LinkedIn person manually
python agents/discovery_agent.py linkedin

# Launch dashboard
streamlit run dashboard/app.py
```

---

## Architecture

```
Data Sources (X API, LinkedIn manual)
        ↓
agents/discovery_agent.py   → finds people
        ↓
agents/scoring_agent.py     → ranks people by opportunity score
        ↓
database/ (PostgreSQL)
        ↓
agents/content_agent.py     → generates LinkedIn + X posts
agents/engagement_agent.py  → suggests daily comments
        ↓
dashboard/app.py            → Streamlit weekly dashboard
```

---

## Weekly Goals

| Metric | Target |
|---|---|
| New quality connections | 20/week |
| Comments made | 30/week |
| Posts published | 3–5/week |
| Recruiter replies | increasing |
| Profile visits | increasing |
