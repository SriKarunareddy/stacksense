"""Top-level Streamlit page: Compare"""
import streamlit as st

# Try to use the refactored `app` package if it's importable; if not,
# fall back to direct imports from `decision_engine` so the page remains runnable.
try:
    from app.utils.tradeoff_analysis import analyze, recommend_stacks
    from app.components.comparison_card import show_category
except Exception:
    from decision_engine.data import get_frontend_options, get_backend_options, get_database_options
    from decision_engine.scorer import rank_options
    from decision_engine.explainer import recommend_stacks as _recommend_stacks
    from decision_engine.explainer import explain_option_scoring
    import pandas as _pd

    def analyze(constraints):
        fe_scores = rank_options(get_frontend_options(), constraints)
        be_scores = rank_options(get_backend_options(), constraints)
        db_scores = rank_options(get_database_options(), constraints)
        return fe_scores, be_scores, db_scores

    def show_category(title, scores):
        st.subheader(title)
        df_rows = []
        for s in scores:
            df_rows.append({"Option": s["name"], "Score": round(s["score"], 3)})
        st.dataframe(_pd.DataFrame(df_rows).sort_values("Score", ascending=False).reset_index(drop=True))

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


# Run when Streamlit imports this page
render()
