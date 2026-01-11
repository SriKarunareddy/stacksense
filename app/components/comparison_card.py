"""Component to render scored options consistently"""
from typing import List, Dict
import streamlit as st
import pandas as pd


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
            # Keep explanation text short
            from decision_engine.explainer import explain_option_scoring

            st.markdown(explain_option_scoring(s))
