"""
Decision data for StackSense

This module defines candidate options (frontends, backends, databases) and
explicit per-criterion suitability scores along with human-readable pros/cons.
Each option contains a `suitability` mapping from each criterion to a mapping of
user choices to a numeric score (0..1). These numbers are the transparent
rule-based inputs used by the scorer.
"""

from typing import List, Dict

CRITERIA = ["team_size", "time_to_market", "scalability", "budget"]


# Frontend options
FRONTENDS: List[Dict] = [
    {
        "id": "react",
        "name": "React",
        "suitability": {
            "team_size": {"Small": 0.7, "Medium": 0.8, "Large": 0.8},
            "time_to_market": {"Fast": 0.85, "Moderate": 0.8, "Slow": 0.7},
            "scalability": {"Low": 0.75, "High": 0.88},
            "budget": {"Low": 0.7, "Medium": 0.8, "High": 0.85},
        },
        "pros": [
            "Large ecosystem and component libraries",
            "Strong community and tooling",
            "Good for complex single-page apps",
        ],
        "cons": [
            "Requires build tooling and more JS knowledge",
            "Frequent ecosystem churn",
        ],
    },
    {
        "id": "angular",
        "name": "Angular",
        "suitability": {
            "team_size": {"Small": 0.6, "Medium": 0.75, "Large": 0.9},
            "time_to_market": {"Fast": 0.6, "Moderate": 0.7, "Slow": 0.9},
            "scalability": {"Low": 0.7, "High": 0.9},
            "budget": {"Low": 0.6, "Medium": 0.7, "High": 0.75},
        },
        "pros": [
            "Full-featured framework with conventions",
            "Great for large teams and long-lived apps",
        ],
        "cons": ["Steeper learning curve", "More boilerplate"],
    },
    {
        "id": "vue",
        "name": "Vue",
        "suitability": {
            "team_size": {"Small": 0.9, "Medium": 0.85, "Large": 0.7},
            "time_to_market": {"Fast": 0.9, "Moderate": 0.85, "Slow": 0.75},
            "scalability": {"Low": 0.8, "High": 0.75},
            "budget": {"Low": 0.85, "Medium": 0.8, "High": 0.75},
        },
        "pros": ["Easy to learn", "Rapid prototyping", "Flexible integration"],
        "cons": ["Smaller enterprise adoption than React/Angular"],
    },
]


# Backend options
BACKENDS: List[Dict] = [
    {
        "id": "node",
        "name": "Node.js",
        "suitability": {
            "team_size": {"Small": 0.9, "Medium": 0.85, "Large": 0.7},
            "time_to_market": {"Fast": 0.9, "Moderate": 0.8, "Slow": 0.65},
            "scalability": {"Low": 0.75, "High": 0.85},
            "budget": {"Low": 0.9, "Medium": 0.85, "High": 0.8},
        },
        "pros": ["Fast development", "Rich npm ecosystem", "Good for event-driven APIs"],
        "cons": ["Single-threaded model requires careful design for CPU-heavy tasks"],
    },
    {
        "id": "django",
        "name": "Django",
        "suitability": {
            "team_size": {"Small": 0.85, "Medium": 0.85, "Large": 0.75},
            "time_to_market": {"Fast": 0.9, "Moderate": 0.85, "Slow": 0.7},
            "scalability": {"Low": 0.8, "High": 0.78},
            "budget": {"Low": 0.85, "Medium": 0.85, "High": 0.82},
        },
        "pros": ["Batteries-included, fast for CRUD and admin UIs", "Strong security defaults"],
        "cons": ["Can be heavy for microservices without adjustments"],
    },
    {
        "id": "spring",
        "name": "Spring Boot",
        "suitability": {
            "team_size": {"Small": 0.6, "Medium": 0.8, "Large": 0.95},
            "time_to_market": {"Fast": 0.6, "Moderate": 0.75, "Slow": 0.9},
            "scalability": {"Low": 0.8, "High": 0.95},
            "budget": {"Low": 0.6, "Medium": 0.75, "High": 0.9},
        },
        "pros": ["Industrial-grade scalability", "Strong typing and tooling"],
        "cons": ["Slower to develop and steeper learning curve"],
    },
]


# Database options
DATABASES: List[Dict] = [
    {
        "id": "mongodb",
        "name": "MongoDB",
        "suitability": {
            "team_size": {"Small": 0.9, "Medium": 0.85, "Large": 0.75},
            "time_to_market": {"Fast": 0.95, "Moderate": 0.85, "Slow": 0.7},
            "scalability": {"Low": 0.75, "High": 0.9},
            "budget": {"Low": 0.88, "Medium": 0.85, "High": 0.8},
        },
        "pros": ["Flexible schema for rapid iteration", "Easy horizontal scaling"],
        "cons": ["Less strict consistency guarantees than relational DBs"],
    },
    {
        "id": "postgres",
        "name": "PostgreSQL",
        "suitability": {
            "team_size": {"Small": 0.85, "Medium": 0.9, "Large": 0.9},
            "time_to_market": {"Fast": 0.8, "Moderate": 0.9, "Slow": 0.9},
            "scalability": {"Low": 0.9, "High": 0.85},
            "budget": {"Low": 0.8, "Medium": 0.85, "High": 0.9},
        },
        "pros": ["Strong consistency", "Rich feature set and extensions"],
        "cons": ["More upfront schema work than document DBs"],
    },
    {
        "id": "dynamodb",
        "name": "DynamoDB",
        "suitability": {
            "team_size": {"Small": 0.7, "Medium": 0.8, "Large": 0.85},
            "time_to_market": {"Fast": 0.85, "Moderate": 0.8, "Slow": 0.7},
            "scalability": {"Low": 0.8, "High": 0.95},
            "budget": {"Low": 0.6, "Medium": 0.75, "High": 0.9},
        },
        "pros": ["Managed, virtually infinite scale", "Great for serverless usage patterns"],
        "cons": ["Different data modeling mindset; can be expensive for heavy R/W patterns"],
    },
]


def get_frontend_options() -> List[Dict]:
    return FRONTENDS


def get_backend_options() -> List[Dict]:
    return BACKENDS


def get_database_options() -> List[Dict]:
    return DATABASES


def get_all_options() -> List[Dict]:
    return FRONTENDS + BACKENDS + DATABASES

