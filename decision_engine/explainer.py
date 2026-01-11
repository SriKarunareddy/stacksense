"""
Explanation utilities for StackSense

Functions to turn numeric score breakdowns into human-readable reasoning and to
assemble combined recommendations for full stacks (frontend + backend + DB).
"""

from typing import List, Dict


def explain_option_scoring(scored_option: Dict) -> str:
    """Return a readable explanation for a scored option."""
    name = scored_option.get("name")
    breakdown = scored_option.get("breakdown", {})
    score = scored_option.get("score", 0.0)

    parts = [f"**{name}** scores **{score:.3f}** overall because:"]
    for crit, val in breakdown.items():
        parts.append(f"- {crit.replace('_', ' ').title()}: {val:.2f}")

    # Summarize key strengths and weaknesses
    pros = scored_option.get("pros", [])
    cons = scored_option.get("cons", [])
    if pros:
        parts.append("**Key strengths:**")
        for p in pros[:3]:
            parts.append(f"- {p}")
    if cons:
        parts.append("**Key trade-offs:**")
        for c in cons[:3]:
            parts.append(f"- {c}")

    return "\n".join(parts)


def recommend_stacks(frontends: List[Dict], backends: List[Dict], dbs: List[Dict], top_n: int = 3) -> List[Dict]:
    """Build combined stacks from the top candidates and rank them by average score.

    Strategy: take the top 3 of each category to keep the combination space reasonable,
    compute the mean of the three component scores as the combined stack score,
    and assemble combined pros/cons and an explanation that highlights trade-offs.
    """
    top_f = frontends[:3]
    top_b = backends[:3]
    top_d = dbs[:3]

    combos: List[Dict] = []
    for f in top_f:
        for b in top_b:
            for d in top_d:
                combined_score = (f["score"] + b["score"] + d["score"]) / 3.0
                pros = list({*f.get("pros", []), *b.get("pros", []), *d.get("pros", [])})
                cons = list({*f.get("cons", []), *b.get("cons", []), *d.get("cons", [])})

                explanation_lines = [
                    f"Combined score is {combined_score:.3f} (mean of component scores).",
                    f"Front-end: {f['name']} (score {f['score']:.3f}).",
                    f"Back-end: {b['name']} (score {b['score']:.3f}).",
                    f"Database: {d['name']} (score {d['score']:.3f}).",
                ]

                # Short trade-off summary
                tradeoffs = [
                    "This stack favors rapid development" if (f['score'] + b['score']) / 2 > 0.8 else "This stack prioritizes stability and scaling",
                ]

                explanation = "\n".join(explanation_lines + tradeoffs)

                combos.append(
                    {
                        "frontend_id": f["id"],
                        "frontend_name": f["name"],
                        "backend_id": b["id"],
                        "backend_name": b["name"],
                        "database_id": d["id"],
                        "database_name": d["name"],
                        "score": float(combined_score),
                        "pros": pros,
                        "cons": cons,
                        "explanation": explanation,
                    }
                )

    combos.sort(key=lambda c: c["score"], reverse=True)
    return combos[:top_n]
