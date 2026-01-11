"""
StackSense - Streamlit app

Interactive tool to compare frontend, backend, and database options
based on transparent, rule-based scoring of user constraints.
"""

from typing import Dict, List
import streamlit as st
import pandas as pd

from decision_engine.data import (
    get_frontend_options,
    get_backend_options,
    get_database_options,
)
from decision_engine.scorer import rank_options, score_options
from decision_engine.explainer import explain_option_scoring, recommend_stacks


st.set_page_config(page_title="StackSense", layout="wide")

CRITERIA = ["team_size", "time_to_market", "scalability", "budget"]


@st.cache_data
def analyze(constraints: Dict[str, str]):
    frontends = get_frontend_options()
    backends = get_backend_options()
    dbs = get_database_options()

    fe_scores = rank_options(frontends, constraints)
    be_scores = rank_options(backends, constraints)
    db_scores = rank_options(dbs, constraints)

    return fe_scores, be_scores, db_scores


def df_from_scores(scores: List[Dict]) -> pd.DataFrame:
    rows = []
    for s in scores:
        row = {
            "Option": s["name"],
            "Score": round(s["score"], 3),
            "team_size": s["breakdown"]["team_size"],
            "time_to_market": s["breakdown"]["time_to_market"],
            "scalability": s["breakdown"]["scalability"],
            "budget": s["breakdown"]["budget"],
        }
        rows.append(row)
    return pd.DataFrame(rows)


def show_category(title: str, scores: List[Dict]):
    st.subheader(title)
    df = df_from_scores(scores)
    st.dataframe(df.sort_values("Score", ascending=False).reset_index(drop=True))

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


def main():
    st.title("StackSense — Choose a Tech Stack with Transparent Reasoning")
    st.write(
        "Use the controls to express constraints — StackSense ranks options and explains trade-offs with transparent, rule-based scoring."
    )

    with st.sidebar:
        st.header("Constraints")
        team_size = st.selectbox("Team size", ["Small", "Medium", "Large"], index=1)
        time_to_market = st.selectbox("Time to market", ["Fast", "Moderate", "Slow"], index=1)
        scalability = st.selectbox("Scalability need", ["Low", "High"], index=0)
        budget = st.selectbox("Budget", ["Low", "Medium", "High"], index=1)

        st.markdown("---")
        st.markdown("**About:** StackSense uses rule-based suitability scores for each option to ensure transparency. No black-box AI.")

    constraints = {
        "team_size": team_size,
        "time_to_market": time_to_market,
        "scalability": scalability,
        "budget": budget,
    }

    fe_scores, be_scores, db_scores = analyze(constraints)

    col1, col2, col3 = st.columns(3)

    with col1:
        show_category("Frontends", fe_scores)
    with col2:
        show_category("Backends", be_scores)
    with col3:
        show_category("Databases", db_scores)

    st.header("Recommended Full Stacks")
    recommended = recommend_stacks(fe_scores, be_scores, db_scores, top_n=3)
    for r in recommended:
        st.subheader(f"Score: {r['score']:.3f} — {r['frontend_name']} / {r['backend_name']} / {r['database_name']}")
        st.markdown(r"**Why this stack:**")
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
    # Backwards-compatible launcher that calls the refactored app
    from app.main import main as _main

    _main()

