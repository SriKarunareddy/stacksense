# StackSense

StackSense helps teams choose a technology stack (frontend, backend, database)
based on clear, rule-based scoring of requirements such as team size, time-to-market, scalability needs, and budget.

Key design goals
- Transparent and rule-based (no black-box AI).
- Compares multiple options and explains trade-offs.
- Clean, modular code suitable for production hardening.

Quick start
1. Create a virtual environment and install dependencies:

   python -m venv .venv
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt

2. Run the app (simple):

   streamlit run streamlit_app.py  # single-file, self-contained entrypoint

   # Or use the refactored package entrypoint:
   streamlit run app/main.py

   # Backwards-compatible launcher:
   python run_app.py  # runs the same UI when not using Streamlit pages

How it works
- `decision_engine/data.py`: defines candidates and explicit numeric suitability values (0..1) for each criterion and option.
- `decision_engine/scorer.py`: computes per-option scores by averaging the per-criterion suitability values. The breakdown is returned to ensure transparency.
- `decision_engine/explainer.py`: converts numeric breakdowns into human readable explanations and composes full-stack recommendations.
- `app/`: refactored Streamlit package with a `pages/` folder for `1_Home.py` and `2_Compare.py`, `components/` for UI building blocks, and `utils/` for analysis helpers. Use `streamlit run app/main.py` to start the app.

Transparency & Extensibility
- The scoring model uses explicit numeric inputs for each option and criterion — change the numbers in `decision_engine/data.py` to reflect team preferences or new options.
- You can extend categories, add additional criteria, or modify weighting logic in `decision_engine/scorer.py`.

License & Contact
- MIT-style usage and attribution is fine — adapt as necessary for your organization.
