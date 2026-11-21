-- Research Ideas Database Schema and Data
-- Generated: 2026-11-20
-- 100 Cardiovascular AI Research Ideas for UK Data Ecosystem

CREATE TABLE research_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    impact_level TEXT NOT NULL,
    data_sources TEXT NOT NULL,
    ai_approach TEXT NOT NULL,
    uk_ecosystem_fit TEXT NOT NULL,
    priority INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_category ON research_ideas(category);
CREATE INDEX idx_priority ON research_ideas(priority DESC);
CREATE INDEX idx_impact ON research_ideas(impact_level);

-- Categories reference
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    idea_count INTEGER DEFAULT 0
);

INSERT INTO categories (name, description, idea_count) VALUES
('Prevention & Risk Stratification', 'Primary and secondary prevention, risk prediction, health equity', 20),
('Early Detection & Diagnosis', 'Screening, diagnosis, phenotyping, early intervention', 20),
('Treatment Optimization & Personalized Medicine', 'Therapy selection, dosing, device optimization, lifelong care', 20),
('Health System & Implementation', 'Population health, quality improvement, pathways, workforce', 20),
('Novel Modalities & Emerging Technologies', 'Foundation models, digital twins, quantum, synthetic data, governance', 20);

-- Views for analysis
CREATE VIEW critical_ideas AS
SELECT * FROM research_ideas WHERE impact_level = 'Critical' ORDER BY priority DESC;

CREATE VIEW high_priority_ideas AS
SELECT * FROM research_ideas WHERE priority >= 90 ORDER BY priority DESC;

CREATE VIEW ideas_by_category AS
SELECT category, COUNT(*) as count, AVG(priority) as avg_priority, MAX(priority) as max_priority
FROM research_ideas GROUP BY category ORDER BY avg_priority DESC;

-- Data quality check
-- SELECT COUNT(*) as total_ideas FROM research_ideas; -- Should be 100
-- SELECT category, COUNT(*) FROM research_ideas GROUP BY category; -- Should be 20 each
