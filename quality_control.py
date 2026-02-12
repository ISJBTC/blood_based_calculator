"""
Quality Control Module

Handles biomarker-level quality control and validation logic.

Currently, the core QC function `validate_biomarker_inputs` is implemented
in `biomarker_input.py` and used via `app.display_quality_control` to render
warnings and critical alerts in the Streamlit UI.

This module exists as a future home for additional QC logic, for example:
- Automated flagging of inconsistent biomarker combinations
- Lab assay performance tracking and drift detection
- Cross-panel consistency checks (core/optimized/full)
"""

# See `biomarker_input.validate_biomarker_inputs` for the current implementation.

