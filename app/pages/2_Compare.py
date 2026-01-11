"""Compare page: main interactive Streamlit interface"""
from typing import Dict, List
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so package imports like
# `app` and `decision_engine` work even when Streamlit imports this page
# in a way that changes the working directory or import paths.
root = Path(__file__).resolve().parent
found = False
for _ in range(6):  # walk up a few levels to find the repo root
    if (root / "decision_engine").is_dir():
        found = True
        break
    root = root.parent
if found and str(root) not in sys.path:
    sys.path.insert(0, str(root))

# Prefer using the internal `app` package helpers when available; fall back
# to direct imports from `decision_engine` so the page is runnable even when
# the package import machinery isn't working (e.g., Streamlit imports this
# module as a top-level script).
try:
    from app.utils import data_loader, tradeoff_analysis
    from app.components.comparison_card import show_category
    analyze = tradeoff_analysis.analyze
    recommend_stacks = tradeoff_analysis.recommend_stacks
except Exception:
    from decision_engine.data import get_frontend_options, get_backend_options, get_database_options
    from decision_engine.scorer import rank_options
    from decision_engine.explainer import recommend_stacks as _recommend_stacks
    from decision_engine.explainer import explain_option_scoring

    def analyze(constraints: Dict[str, str]):
        fe_scores = rank_options(get_frontend_options(), constraints)
        be_scores = rank_options(get_backend_options(), constraints)
        db_scores = rank_options(get_database_options(), constraints)
        return fe_scores, be_scores, db_scores

    def show_category(title: str, scores: List[Dict]):
        st.subheader(title)
        df_rows = []
        for s in scores:
            df_rows.append({"Option": s["name"], "Score": round(s["score"], 3)})
        st.dataframe(pd.DataFrame(df_rows).sort_values("Score", ascending=False).reset_index(drop=True))

        for s in scores:
            with st.expander(f"{s['name']} — details"):
                st.markdown(f"**Score:** {s['score']:.3f}")
                st.markdown("**Breakdown:**")
                for crit, val in s["breakdown"].items():
                    st.markdown(f"- **{crit}**: {val:.2f}")
                st.markdown("**Pros:**")
                for p in s.get("pros", []):
                    st.markdown(f"- {p}")
                st.markdown("**Cons:**")
                for c in s.get("cons", []):
                    st.markdown(f"- {c}")
                st.markdown("---")
                st.markdown(explain_option_scoring(s))

    def recommend_stacks(frontends, backends, dbs, top_n: int = 3):
        return _recommend_stacks(frontends, backends, dbs, top_n=top_n)


def render():
    st.title("Compare — StackSense")
    st.write("Express constraints and compare frontends, backends, and databases.")

    with st.sidebar:
        st.header("Constraints")
        team_size = st.selectbox("Team size", ["Small", "Medium", "Large"], index=1)
        time_to_market = st.selectbox("Time to market", ["Fast", "Moderate", "Slow"], index=1)
        scalability = st.selectbox("Scalability need", ["Low", "High"], index=0)
        budget = st.selectbox("Budget", ["Low", "Medium", "High"], index=1)

        st.markdown("---")
        st.markdown("**About:** StackSense uses rule-based suitability scores for transparency. No black-box AI.")

    constraints = {
        "team_size": team_size,
        "time_to_market": time_to_market,
        "scalability": scalability,
        "budget": budget,
    }

    fe_scores, be_scores, db_scores = tradeoff_analysis.analyze(constraints)

    col1, col2, col3 = st.columns(3)
    with col1:
        show_category("Frontends", fe_scores)
    with col2:
        show_category("Backends", be_scores)
    with col3:
        show_category("Databases", db_scores)

    st.header("Recommended Full Stacks")
    recommended = tradeoff_analysis.recommend_stacks(fe_scores, be_scores, db_scores, top_n=3)

    for r in recommended:
        st.subheader(f"Score: {r['score']:.3f} — {r['frontend_name']} / {r['backend_name']} / {r['database_name']}")
        st.markdown("**Why this stack:**")
        st.markdown(r["explanation"])
        with st.expander("Combined Pros and Cons"):
            st.markdown("**Pros:**")
            for p in r["pros"]:
                st.markdown(f"- {p}")
            st.markdown("**Cons:**")
            for c in r["cons"]:
                st.markdown(f"- {c}")

    st.markdown("---")
    st.markdown("**Transparency:** scoring is a simple average of per-criterion suitability values (0..1). See breakdowns above.")


if __name__ == "__main__":
    render()
