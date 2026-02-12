"""
Clinical Decision Support Module

At present, the primary decision-support
views are implemented in `results_display.display_clinical_interpretation`
and `results_display.display_resistance_monitoring`, which use Streamlit
for interactive rendering.

Future work can refactor shared, non-UI logic into this module so that:
- The clinical rules are testable independently of the UI layer
- Multiple front-ends (web, CLI, API) can reuse the same decision logic
"""

# For now, the main implementation lives in `results_display.py`.
# This file exists as an explicit extension point and documentation anchor.

