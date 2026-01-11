"""Analysis helpers that wrap decision_engine scoring and explanation."""
from typing import Dict, List, Tuple
from decision_engine.data import get_frontend_options, get_backend_options, get_database_options
from decision_engine.scorer import rank_options, score_options
from decision_engine.explainer import recommend_stacks as _recommend_stacks


CRITERIA = ["team_size", "time_to_market", "scalability", "budget"]


def analyze(constraints: Dict[str, str]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    frontends = get_frontend_options()
    backends = get_backend_options()
    dbs = get_database_options()

    fe_scores = rank_options(frontends, constraints)
    be_scores = rank_options(backends, constraints)
    db_scores = rank_options(dbs, constraints)

    return fe_scores, be_scores, db_scores


def recommend_stacks(frontends, backends, dbs, top_n: int = 3):
    return _recommend_stacks(frontends, backends, dbs, top_n=top_n)
