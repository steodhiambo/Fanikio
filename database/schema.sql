-- Run this file to initialize the database
-- psql -U your_user -d fanikio -f database/schema.sql

CREATE TABLE IF NOT EXISTS people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL,          -- 'linkedin' or 'x'
    role VARCHAR(255),
    company VARCHAR(255),
    profile_url TEXT,
    followers INTEGER DEFAULT 0,
    engagement_score NUMERIC(4,2) DEFAULT 0,
    relevance_score NUMERIC(4,2) DEFAULT 0,
    hiring_potential NUMERIC(4,2) DEFAULT 0,
    activity_score NUMERIC(4,2) DEFAULT 0,
    influence_score NUMERIC(4,2) DEFAULT 0,
    opportunity_score NUMERIC(4,2) DEFAULT 0,
    why_they_matter TEXT,
    last_contacted DATE,
    status VARCHAR(50) DEFAULT 'discovered', -- discovered, contacted, connected, replied
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    pillar VARCHAR(50) NOT NULL,             -- content pillar type
    topic TEXT NOT NULL,
    linkedin_post TEXT,
    x_post TEXT,
    status VARCHAR(50) DEFAULT 'draft',      -- draft, scheduled, published
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS engagement_suggestions (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    original_post_url TEXT,
    original_post_text TEXT,
    author_name VARCHAR(255),
    suggested_comment TEXT,
    status VARCHAR(50) DEFAULT 'pending',    -- pending, used, skipped
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS weekly_metrics (
    id SERIAL PRIMARY KEY,
    week_start DATE NOT NULL,
    new_connections INTEGER DEFAULT 0,
    comments_made INTEGER DEFAULT 0,
    posts_published INTEGER DEFAULT 0,
    recruiter_replies INTEGER DEFAULT 0,
    profile_visits INTEGER DEFAULT 0,
    top_performing_post_id INTEGER REFERENCES posts(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_people_platform ON people(platform);
CREATE INDEX IF NOT EXISTS idx_people_status ON people(status);
CREATE INDEX IF NOT EXISTS idx_people_opportunity_score ON people(opportunity_score DESC);
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
