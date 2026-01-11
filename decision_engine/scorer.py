"""
Transparent rule-based scoring for StackSense

Each option includes a `suitability` mapping (see `decision_engine.data`) which maps
criteria to score values (0..1). Scoring simply averages the per-criterion
suitability values for the selected user choices; the per-criterion values are
returned with the breakdown so the scoring is transparent.
"""

from typing import Dict, List


def score_option(option: Dict, constraints: Dict[str, str]) -> Dict:
    """Score a single option given user `constraints`.

    Returns a dict with name, id, breakdown (per-criterion numeric values), and
    the final `score` (float 0..1).
    """
    breakdown = {}
    for crit, choice in constraints.items():
        crit_map = option.get("suitability", {}).get(crit, {})
        # Default to 0.5 if mapping is missing — this is explicit and transparent
        val = crit_map.get(choice, 0.5)
        breakdown[crit] = float(val)

    # Simple average across criteria (equal weights) — intentionally transparent
    score = sum(breakdown.values()) / max(len(breakdown), 1)

    return {
        "id": option.get("id"),
        "name": option.get("name"),
        "breakdown": breakdown,
        "score": float(score),
        "pros": option.get("pros", []),
        "cons": option.get("cons", []),
    }


def score_options(options: List[Dict], constraints: Dict[str, str]) -> List[Dict]:
    return [score_option(o, constraints) for o in options]


def rank_options(options: List[Dict], constraints: Dict[str, str], top_n: int = None) -> List[Dict]:
    scored = score_options(options, constraints)
    ranked = sorted(scored, key=lambda s: s["score"], reverse=True)
    if top_n:
        return ranked[:top_n]
    return ranked
