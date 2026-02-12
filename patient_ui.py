"""
Patient Data UI Module
Streamlit components for save, load, export, import, and comparison.
"""

import streamlit as st
import pandas as pd
from patient_data import (
    save_patient,
    load_patient,
    list_patients,
    delete_patient,
    export_to_json,
    import_from_json,
    load_record_for_import,
)
from patient_comparison import compute_comparison, get_summary_stats


def _apply_biomarkers_to_session(biomarkers: dict):
    """Load biomarkers into session state and clear widget cache for refresh."""
    from biomarkers_data import ALL_BIOMARKERS
    st.session_state.biomarkers = {k: float(biomarkers.get(k, 0) or 0) for k in ALL_BIOMARKERS}
    for key in ALL_BIOMARKERS:
        widget_key = f"input_{key}"
        if widget_key in st.session_state:
            del st.session_state[widget_key]


def display_patient_save_load():
    """
    Sidebar section: Save current, Load patient, Export, Import.
    Returns (load_triggered, loaded_biomarkers) or (False, None).
    """
    patients = list_patients()
    panel_type = "core" if st.session_state.get("panel_core_markers") else "full"

    with st.sidebar.expander("Patient data", expanded=True):
        st.caption("Save, load, or compare biomarker records")

        # Save
        if st.session_state.get("biomarkers"):
            with st.popover("Save current"):
                pid = st.text_input("Patient ID (optional)", placeholder="e.g. P001")
                pname = st.text_input("Patient name (optional)", placeholder="e.g. John Doe")
                notes = st.text_area("Notes (optional)", placeholder="Visit, treatment, etc.")
                if st.button("Save"):
                    rid = save_patient(
                        st.session_state.biomarkers,
                        patient_id=pid or None,
                        patient_name=pname or None,
                        notes=notes,
                        panel_type=panel_type,
                    )
                    st.success(f"Saved as {rid}")
                    st.rerun()

        # Load
        if patients:
            selected = st.selectbox(
                "Load patient",
                options=["— Select —"] + [f"{p['patient_name']} ({p['date'][:10]})" for p in patients],
                key="patient_load_select",
            )
            if selected and selected != "— Select —":
                idx = [f"{p['patient_name']} ({p['date'][:10]})" for p in patients].index(selected)
                rec = load_patient(patients[idx]["patient_id"])
                if rec and st.button("Load into form", key="patient_load_btn"):
                    _apply_biomarkers_to_session(rec["biomarkers"])
                    st.session_state.patient_loaded_from = rec.get("patient_name", rec.get("patient_id", ""))
                    st.session_state.patient_baseline = rec["biomarkers"]
                    st.success(f"Loaded {rec.get('patient_name', rec.get('patient_id'))}")
                    st.rerun()

        st.divider()

        # Export
        if st.session_state.get("biomarkers"):
            rec = {
                "patient_id": "export",
                "patient_name": "",
                "date": __import__("datetime").datetime.now().isoformat(),
                "notes": "",
                "panel_type": panel_type,
                "biomarkers": st.session_state.biomarkers,
            }
            json_str = export_to_json(rec)
            st.download_button(
                "Export JSON",
                data=json_str,
                file_name=f"patient_biomarkers_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key="patient_export",
            )

        # Import
        uploaded = st.file_uploader("Import JSON", type=["json"], key="patient_import")
        if uploaded:
            try:
                data = uploaded.read().decode("utf-8")
                rec = import_from_json(data)
                if rec:
                    biomarkers = load_record_for_import(rec)
                    if st.button("Import into form", key="patient_import_btn"):
                        _apply_biomarkers_to_session(biomarkers)
                        st.session_state.patient_baseline = biomarkers.copy()
                        st.success("Imported")
                        st.rerun()
                else:
                    st.error("Invalid JSON format")
            except Exception as e:
                st.error(f"Import failed: {e}")


def display_comparison(current: dict, previous: dict, prev_label: str = "Previous"):
    """Display biomarker comparison (47) and parameter comparison (37)."""
    # --- Biomarker comparison (47 biomarkers) ---
    rows = compute_comparison(current, previous)
    stats = get_summary_stats(rows)

    st.subheader("Biomarker comparison (47 biomarkers)")
    st.caption(f"Current vs {prev_label} — blood values with clinical interpretation")

    # Summary metrics (all 47: improved + worsened + unchanged + changed)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Improved", stats["improved"], help="Change in favorable direction")
    with c2:
        st.metric("Worsened", stats["worsened"], help="Change in unfavorable direction")
    with c3:
        st.metric("Unchanged", stats["unchanged"])
    with c4:
        changed = stats["improved"] + stats["worsened"]
        st.metric("Total changed", changed)
    with c5:
        other = stats.get("changed", 0)
        st.metric("Other", other, help="TNF-α, Ang-2, HER2 circ, CYP2D6 — changed but no target for improved/worsened")

    # Table
    df = pd.DataFrame([
        {
            "Biomarker": r["name"],
            "Current": f"{r['current']:.2f}",
            prev_label: f"{r['previous']:.2f}",
            "Δ": f"{r['delta']:+.2f}",
            "% Δ": f"{r['pct_change']:+.1f}%" if r["previous"] != 0 else "—",
            "Trend": r["trend"].capitalize(),
            "Interpretation": r["interpretation"],
        }
        for r in rows
    ])

    # Color by trend
    def trend_style(row):
        t = row["Trend"].lower()
        if t == "improved":
            return ["background-color: #d4edda"] * len(row)
        if t == "worsened":
            return ["background-color: #f8d7da"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df.style.apply(trend_style, axis=1),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Interpretation": st.column_config.TextColumn("Clinical interpretation", width="medium"),
        },
    )

    # --- Parameter comparison (37 parameters) ---
    st.subheader("Parameter comparison (37 parameters)")
    st.caption("Calculated model parameters: current vs previous reading")

    from calculations import calculate_all_parameters

    core_markers = st.session_state.get("panel_core_markers")
    with st.spinner("Computing parameters for comparison..."):
        calc_current = calculate_all_parameters(current, core_markers=core_markers)
        calc_prev = calculate_all_parameters(previous, core_markers=core_markers)

    p_current = calc_current["parameters"]
    p_prev = calc_prev["parameters"]

    # Build parameter comparison (exclude G and alpha_acid from the 37)
    PARAM_KEYS = [k for k in p_current if k not in ("G", "alpha_acid") and k in p_prev]
    param_rows = []
    for k in PARAM_KEYS:
        c, p = p_current.get(k, 0), p_prev.get(k, 0)
        d = c - p
        pct = 100 * (d / p) if p != 0 else (100.0 if c != 0 else 0.0)
        param_rows.append({
            "Parameter": k,
            "Current": f"{c:.4f}" if isinstance(c, float) else str(c),
            prev_label: f"{p:.4f}" if isinstance(p, float) else str(p),
            "Δ": f"{d:+.4f}",
            "% Δ": f"{pct:+.1f}%" if p != 0 else "—",
        })

    df_param = pd.DataFrame(param_rows)
    st.dataframe(df_param, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(PARAM_KEYS)} calculated parameters (λ₁, λ₂, η_E, η_C, η_H, η_I, etc.)")


def display_compare_selector(current: dict):
    """
    Show 'Compare with' selector and comparison when a baseline is chosen.
    Uses session_state.patient_baseline if set; else lets user pick from saved.
    """
    baseline = st.session_state.get("patient_baseline")
    prev_label = st.session_state.get("patient_loaded_from", "Baseline")

    if baseline:
        # Compare with loaded baseline
        with st.expander("Compare with previous reading", expanded=True):
            display_comparison(current, baseline, prev_label=prev_label)
        return

    # Offer to select a saved patient for comparison
    patients = list_patients()
    if not patients:
        st.caption("Save a patient record first to enable comparison.")
        return

    with st.expander("Compare with saved reading"):
        opts = ["— Select —"] + [f"{p['patient_name']} ({p['date'][:10]})" for p in patients]
        sel = st.selectbox("Compare current with", opts, key="compare_select")
        if sel and sel != "— Select —":
            idx = [f"{p['patient_name']} ({p['date'][:10]})" for p in patients].index(sel)
            rec = load_patient(patients[idx]["patient_id"])
            if rec:
                display_comparison(current, rec["biomarkers"], prev_label=rec.get("patient_name", rec.get("patient_id", "Saved")))
            else:
                st.warning("Record not found")
