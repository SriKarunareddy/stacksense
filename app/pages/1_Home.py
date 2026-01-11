"""Home page for StackSense"""
from typing import Any
import streamlit as st


def render():
    st.title("StackSense — Choose a Tech Stack with Transparent Reasoning")
    st.write(
        "Use the controls on the Compare page to express constraints — StackSense ranks options and explains trade-offs with transparent, rule-based scoring."
    )

    st.markdown("---")
    st.header("What this is")
    st.markdown(
        "StackSense helps teams pick a frontend, backend, and database by scoring options based on simple, explicit suitability mappings. Scoring is a transparent average of per-criterion suitability values (0..1)."
    )

    st.subheader("How to use")
    st.markdown("- Open the **Compare** page to set your constraints (team size, time to market, scalability, budget).")
    st.markdown("- StackSense will rank frontends, backends, and databases and provide recommended full stacks with pros/cons and explanations.")

    st.markdown("---")
    st.write("**Design philosophy:** no black-box ML — explicit, rule-based scoring for interpretability.")
