"""
Biomarker Input Module
Handles user input collection for all 47 biomarkers
"""

import streamlit as st
from biomarkers_data import (
    TUMOR_MARKERS, IMMUNE_MARKERS, RESISTANCE_MARKERS,
    METABOLIC_MARKERS, ORGAN_MARKERS, CATEGORY_COUNTS,
    ALL_BIOMARKERS,
)

def get_biomarker_inputs(panel_markers=None):
    """
    Collect biomarker inputs from user.

    Args:
        panel_markers: If a list of biomarker keys (e.g. Core 15), only those
            inputs are shown; others are set to 0. If None, all 47 are shown.

    Returns:
        Dictionary with all 47 biomarker keys and values (non-panel keys = 0 when panel_markers set).
    """
    import streamlit as st

    # Get existing values from session state if available
    existing_values = st.session_state.get('biomarkers', {})

    # Core Panel only: show 15 inputs, return full dict with rest 0
    if panel_markers is not None and len(panel_markers) > 0:
        st.subheader("Core Panel (15 biomarkers)")
        st.caption("Top 15 by selection frequency. All 37 parameters still calculated.")
        biomarkers = {k: 0.0 for k in ALL_BIOMARKERS}
        cols = st.columns(2)
        for idx, key in enumerate(panel_markers):
            if key not in ALL_BIOMARKERS:
                continue
            info = ALL_BIOMARKERS[key]
            with cols[idx % 2]:
                default_value = existing_values.get(key, 0.0)
                label_text = f"{info['name']} ({info['unit']})"
                biomarkers[key] = st.number_input(
                    label=label_text,
                    value=float(default_value),
                    step=0.1 if 'score' not in info['unit'].lower() and 'cells' not in info['unit'] else 1.0,
                    help=f"Standard Reference Range: {info['normal']}",
                    key=f"input_{key}",
                )
                st.caption(f"📊 {info['normal']}")
        return biomarkers

    # Full panel: all 47 in category tabs
    biomarkers = {}

    # Create tabs for different categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"🔴 Tumor Markers ({CATEGORY_COUNTS['tumor']})",
        f"🛡️ Immune Function ({CATEGORY_COUNTS['immune']})",
        f"⚠️ Resistance ({CATEGORY_COUNTS['resistance']})",
        f"⚡ Metabolic ({CATEGORY_COUNTS['metabolic']})",
        f"🏥 Organ Function ({CATEGORY_COUNTS['organ']})"
    ])
    
    # Tumor Markers Tab
    with tab1:
        st.subheader("Tumor Markers (6 biomarkers)")
        cols = st.columns(2)
        col_idx = 0
        
        for key, info in TUMOR_MARKERS.items():
            with cols[col_idx % 2]:
                default_value = existing_values.get(key, 0.0)
                # Full name already includes abbreviation in parentheses
                label_text = f"{info['name']} ({info['unit']})"
                
                # Use value parameter only, don't set widget key in session state
                biomarkers[key] = st.number_input(
                    label=label_text,
                    value=float(default_value),
                    step=0.1 if 'score' not in info['unit'].lower() else 1.0,
                    help=f"Standard Reference Range: {info['normal']}",
                    key=f"input_{key}"
                )
                # Show reference range below input
                st.caption(f"📊 Standard Reference Range: {info['normal']}")
            col_idx += 1
    
    # Immune Function Tab
    with tab2:
        st.subheader("Immune Function Markers (12 biomarkers)")
        cols = st.columns(2)
        col_idx = 0
        
        for key, info in IMMUNE_MARKERS.items():
            with cols[col_idx % 2]:
                default_value = existing_values.get(key, 0.0)
                # Full name already includes abbreviation in parentheses
                label_text = f"{info['name']} ({info['unit']})"
                
                biomarkers[key] = st.number_input(
                    label=label_text,
                    value=float(default_value),
                    step=0.1 if 'score' not in info['unit'].lower() and 'cells' not in info['unit'] else 1.0,
                    help=f"Standard Reference Range: {info['normal']}",
                    key=f"input_{key}"
                )
                st.caption(f"📊 Standard Reference Range: {info['normal']}")
            col_idx += 1
    
    # Resistance Markers Tab
    with tab3:
        st.subheader("Resistance Markers (16 biomarkers)")
        cols = st.columns(2)
        col_idx = 0
        
        for key, info in RESISTANCE_MARKERS.items():
            with cols[col_idx % 2]:
                default_value = existing_values.get(key, 0.0)
                # Full name already includes abbreviation in parentheses
                label_text = f"{info['name']} ({info['unit']})"
                
                biomarkers[key] = st.number_input(
                    label=label_text,
                    value=float(default_value),
                    step=0.1 if 'score' not in info['unit'].lower() and 'units' not in info['unit'] else 1.0,
                    help=f"Standard Reference Range: {info['normal']}",
                    key=f"input_{key}"
                )
                st.caption(f"📊 Standard Reference Range: {info['normal']}")
            col_idx += 1
    
    # Metabolic Markers Tab
    with tab4:
        st.subheader("Metabolic Markers (8 biomarkers)")
        cols = st.columns(2)
        col_idx = 0
        
        for key, info in METABOLIC_MARKERS.items():
            with cols[col_idx % 2]:
                default_value = existing_values.get(key, 0.0)
                # Full name already includes abbreviation in parentheses
                label_text = f"{info['name']} ({info['unit']})"
                
                biomarkers[key] = st.number_input(
                    label=label_text,
                    value=float(default_value),
                    step=0.1 if info['unit'] in ['mg/dL', 'g/dL', 'ng/mL', 'mmol/L', 'pH'] else 1.0,
                    help=f"Standard Reference Range: {info['normal']}",
                    key=f"input_{key}"
                )
                st.caption(f"📊 Standard Reference Range: {info['normal']}")
            col_idx += 1
    
    # Organ Function Tab
    with tab5:
        st.subheader("Organ Function Markers (5 biomarkers)")
        cols = st.columns(2)
        col_idx = 0
        
        for key, info in ORGAN_MARKERS.items():
            with cols[col_idx % 2]:
                default_value = existing_values.get(key, 0.0)
                # Full name already includes abbreviation in parentheses
                label_text = f"{info['name']} ({info['unit']})"
                
                biomarkers[key] = st.number_input(
                    label=label_text,
                    value=float(default_value),
                    step=0.01 if key == 'creatinine' else (0.1 if 'mg/dL' in info['unit'] else 1.0),
                    help=f"Standard Reference Range: {info['normal']}",
                    key=f"input_{key}"
                )
                st.caption(f"📊 Standard Reference Range: {info['normal']}")
            col_idx += 1
    
    return biomarkers

def calculate_progress(biomarkers, panel_markers=None):
    """
    Calculate completion progress.
    If panel_markers is set (e.g. Core 15), progress is over that subset only.
    """
    from biomarkers_data import ALL_BIOMARKERS

    if panel_markers is not None and len(panel_markers) > 0:
        total = len(panel_markers)
        filled = sum(1 for k in panel_markers if biomarkers.get(k, 0) > 0)
    else:
        total = len(biomarkers)
        filled = sum(1 for v in biomarkers.values() if v > 0)
    percentage = (filled / total) * 100 if total > 0 else 0

    # Count by category (over full set for by_category)
    category_counts = {
        'tumor': {'filled': 0, 'total': CATEGORY_COUNTS['tumor']},
        'immune': {'filled': 0, 'total': CATEGORY_COUNTS['immune']},
        'resistance': {'filled': 0, 'total': CATEGORY_COUNTS['resistance']},
        'metabolic': {'filled': 0, 'total': CATEGORY_COUNTS['metabolic']},
        'organ': {'filled': 0, 'total': CATEGORY_COUNTS['organ']}
    }
    keys_to_count = panel_markers if (panel_markers is not None and len(panel_markers) > 0) else biomarkers.keys()
    for key in keys_to_count:
        value = biomarkers.get(key, 0)
        if value > 0 and key in ALL_BIOMARKERS:
            cat = ALL_BIOMARKERS[key]['category']
            if cat in category_counts:
                category_counts[cat]['filled'] += 1

    return {
        'total_filled': filled,
        'total': total,
        'percentage': percentage,
        'by_category': category_counts
    }


def display_panel_selection():
    """
    Display testing panel options in the sidebar and return selection details.

    Returns:
        (core_markers, panel_r2) — core_markers is list for Core Panel or None; panel_r2 is R² from Chapter 4 validation.
    """
    st.sidebar.subheader("Testing Panel Options")
    panel_option = st.sidebar.selectbox(
        "Select Testing Strategy:",
        [
            "Full Panel (47 biomarkers)",
            "Optimized Panel (25 biomarkers)",
            "Core Panel (15 biomarkers)",
        ],
        help="Choose by clinical need; all 37 parameters formulae."
    )

    if panel_option == "Core Panel (15 biomarkers)":
        st.sidebar.caption("Core Panel (15 biomarkers). Use case: routine screening, basic treatment selection.")
        # Top 15 by selection frequency (Chapter 4 feature selection)
        core_markers = [
            'ca153', 'cd8', 'pik3ca', 'albumin', 'cea', 'cd4',
            'esr1_protein', 'il10', 'glucose', 'her2_mutations',
            'tk1', 'nk', 'lactate', 'mdr1', 'ifn_gamma',
        ]
        return core_markers, 0.87

    elif panel_option == "Optimized Panel (25 biomarkers)":
        st.sidebar.caption("Optimized Panel (25 biomarkers). Use case: treatment planning, resistance monitoring.")
        return None, 0.93

    else:
        st.sidebar.caption("Full Panel (47 biomarkers). Use case: complex cases, research protocols. R² = 0.996 per Chapter 4.")
        return None, 0.996


def validate_biomarker_inputs(biomarkers):
    """
    Basic biomarker quality control checks against extreme / abnormal values.

    Returns:
        warnings: list of non-critical issues
        critical_alerts: list of critical value alerts
    """
    warnings = []
    critical_alerts = []

    for key, value in biomarkers.items():
        if key in ALL_BIOMARKERS and value > 0:
            marker_info = ALL_BIOMARKERS[key]

            # Critical alerts
            if key == 'ca153' and value > 100:
                critical_alerts.append(
                    f"CA 15-3 extremely elevated ({value} U/mL) - immediate clinical correlation needed"
                )
            elif key == 'cd8' and value < 200:
                critical_alerts.append(
                    f"CD8+ severely low ({value} cells/μL) - immunocompromised state"
                )
            elif key == 'creatinine' and value > 3.0:
                critical_alerts.append(
                    f"Creatinine severely elevated ({value} mg/dL) - kidney dysfunction"
                )

            # Warnings (outside typical reference ranges)
            if key == 'ca153' and value > 25:
                warnings.append(
                    f"CA 15-3 elevated ({value} U/mL, normal <25)"
                )
            elif key == 'glucose' and (value < 70 or value > 180):
                warnings.append(
                    f"Glucose abnormal ({value} mg/dL, normal 70-140)"
                )

    return warnings, critical_alerts

