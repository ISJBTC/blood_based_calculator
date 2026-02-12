"""
Main Streamlit Application
Blood-Based Cancer Model Calculator - Chapter 4 Implementation
"""

import streamlit as st
from biomarker_input import (
    get_biomarker_inputs,
    calculate_progress,
    display_panel_selection,
    validate_biomarker_inputs,
)
from calculations import calculate_all_parameters
from results_display import display_results
from biomarkers_data import TOTAL_BIOMARKERS
from differential_equations import display_differential_equations
from parameter_formulas import display_parameter_formulas
from patient_ui import display_patient_save_load, display_compare_selector

# Page configuration
st.set_page_config(
    page_title="Blood-Based Cancer Model Calculator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🧬 Blood-Based Cancer Mathematical Model")
st.subheader("Calculator v1.0")

# Scientific foundation and data disclaimer (per Chapter 4 specification)
st.sidebar.markdown("""
### 🔬 Scientific Foundation
**Based on:** Machine Learning-Enhanced Blood-Based Framework  
**Validation:** 5,000 synthetic patients with biologically realistic correlations  
**Accuracy:** Full panel R² = 0.98; CatBoost R² = 0.996 on 18 params (Chapter 4)  
**Mathematical:** 15-dimensional coupled differential equations with 46.7% stability
""")

st.warning("""
⚠️ **IMPORTANT SCIENTIFIC DISCLOSURE**  
This calculator is based on **synthetic patient data** designed to reflect biologically realistic biomarker correlations. 
While mathematically rigorous and based on established clinical relationships, 
**prospective clinical validation with real patients is required before clinical deployment**.
""")

def load_example_data(scenario: str = "Baseline (Moderate Hormone+ Risk)"):
    """
    Load example patient data for a given clinical scenario.
    """
    from biomarkers_data import ALL_BIOMARKERS

    # Baseline moderate-risk, hormone-receptor positive
    baseline = {
        'ca153': 45, 'ca2729': 38, 'cea': 4.2, 'tk1': 3.1, 'ctdna': 1.2, 'esr1_protein': 5.2,
        'cd8': 650, 'cd4': 950, 'nk': 180, 'ifn_gamma': 3.8, 'il10': 8, 'tnf_alpha': 6.5,
        'tgf_beta': 2.8, 'pdl1_ctc': 1.5, 'hla_dr': 75, 'ctc': 6, 'ang2': 1800, 'lymphocytes': 1800,
        'esr1_mutations': 1, 'pgr': 60, 'brca': 0, 'pik3ca': 2, 'tp53': 1, 'her2_mutations': 0,
        'her2_circ': 2.0, 'mdr1': 120, 'cyp2d6': 2.0, 'survivin': 3.0, 'hsp': 10, 'mir200': 1.0,
        'exosomes': 9, 'vegf': 250, 'mrp1': 90, 'ki67': 18,
        'glucose': 110, 'lactate': 2.1, 'ldh': 260, 'albumin': 3.8, 'beta_hydroxybutyrate': 0.2,
        'blood_ph': 7.39, 'folate': 9, 'vitamin_d': 28,
        'creatinine': 0.9, 'bun': 16, 'alt': 30, 'ast': 28, 'bilirubin': 0.7
    }

    # Scenario-specific overrides
    scenarios = {
        "Baseline (Moderate Hormone+ Risk)": {},

        # High proliferation, weak immune, low resistance
        "High Growth / Weak Immune": {
            'ca153': 80, 'ca2729': 70, 'cea': 6.0, 'tk1': 5.0, 'ctdna': 2.0,
            'cd8': 250, 'cd4': 400, 'nk': 120, 'ifn_gamma': 1.5,
            'il10': 15, 'tgf_beta': 3.5, 'pdl1_ctc': 3.0,
            'survivin': 6.0, 'ki67': 35,
        },

        # Strong multi-drug resistance, prior chemo
        "High Resistance / Late Stage": {
            'ca153': 95, 'ca2729': 85, 'ctdna': 3.5,
            'esr1_mutations': 3, 'brca': 2, 'pik3ca': 6, 'tp53': 6,
            'her2_mutations': 2, 'mdr1': 260, 'mrp1': 180,
            'survivin': 7.5, 'hsp': 18, 'mir200': 0.3,
            'ctc': 25, 'exosomes': 18, 'vegf': 420,
            'cd8': 320, 'cd4': 500, 'nk': 150, 'ifn_gamma': 2.0,
            'il10': 18, 'tgf_beta': 4.0, 'pdl1_ctc': 4.0,
        },

        # HER2-amplified, strong candidate for HER2 therapy
        "HER2-Positive / Targeted Eligible": {
            'ca153': 55, 'ca2729': 60, 'ctdna': 1.8,
            'her2_mutations': 3, 'her2_circ': 6.0,
            'mdr1': 150, 'pik3ca': 3, 'tp53': 1,
            'cd8': 700, 'cd4': 1100, 'nk': 260, 'ifn_gamma': 4.5,
            'il10': 6, 'tgf_beta': 2.2, 'pdl1_ctc': 1.2,
            'vegf': 350, 'ang2': 2600,
        },

        # Strong immune, low tumor burden, post-treatment remission-like
        "Strong Immune / Low Tumor": {
            'ca153': 20, 'ca2729': 22, 'cea': 2.0, 'tk1': 1.2, 'ctdna': 0.3,
            'cd8': 1100, 'cd4': 1300, 'nk': 420, 'ifn_gamma': 5.5,
            'il10': 3, 'tgf_beta': 1.8, 'pdl1_ctc': 0.5,
            'ctc': 1, 'exosomes': 6, 'vegf': 180,
            'survivin': 1.0, 'ki67': 8,
        },
    }

    # Start from baseline and apply scenario overrides
    example_data = baseline.copy()
    overrides = scenarios.get(scenario, {})
    example_data.update(overrides)

    # Ensure all biomarkers are present (set missing ones to 0)
    for key in ALL_BIOMARKERS.keys():
        if key not in example_data:
            example_data[key] = 0.0

    # Clear widget states to force refresh
    for key in ALL_BIOMARKERS.keys():
        widget_key = f"input_{key}"
        if widget_key in st.session_state:
            del st.session_state[widget_key]

    # Set biomarker values in session state
    # Widgets will read from st.session_state.biomarkers via existing_values
    st.session_state.biomarkers = example_data

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")

    # Compact page navigation using radio instead of multiple buttons
    # Include Results as a page (labelled 'Results', not 'Calculate Results')
    page_options = {
        "Overview": "overview",
        "Differential Equations": "equations",
        "Parameter Formulas": "formulas",
        "Input Data": "input",
        "Results": "calculate",
    }
    current_page = st.session_state.get("page", "overview")
    # Map current page to label for default selection
    reverse_map = {v: k for k, v in page_options.items()}
    default_label = reverse_map.get(current_page, "Overview")

    selected_label = st.radio(
        "Go to",
        list(page_options.keys()),
        index=list(page_options.keys()).index(default_label),
        label_visibility="collapsed",
    )
    st.session_state.page = page_options[selected_label]

    st.divider()

    # Panel selection (Full / Optimized / Core) — capture for input page
    core_markers, panel_r2 = display_panel_selection()
    st.session_state.panel_core_markers = core_markers  # list of 15 keys when Core, else None
    st.session_state.panel_r2 = panel_r2

    # Patient data: save, load, export, import
    display_patient_save_load()

    # Progress display in a collapsible block to reduce vertical depth
    if 'biomarkers' in st.session_state:
        with st.expander("Biomarker Progress", expanded=False):
            progress = calculate_progress(st.session_state.biomarkers)
            st.metric("Biomarkers Entered", f"{progress['total_filled']}/{TOTAL_BIOMARKERS}")
            st.progress(progress['percentage'] / 100)

            st.write("**By Category:**")
            for cat, counts in progress['by_category'].items():
                st.write(f"{cat.capitalize()}: {counts['filled']}/{counts['total']}")

    st.divider()

    # Example scenarios (also inside an expander to save space)
    with st.expander("Example Clinical Scenarios", expanded=True):
        example_scenario = st.selectbox(
            "Example Scenario",
            [
                "Baseline (Moderate Hormone+ Risk)",
                "High Growth / Weak Immune",
                "High Resistance / Late Stage",
                "HER2-Positive / Targeted Eligible",
                "Strong Immune / Low Tumor",
            ],
            index=0,
        )

        # Short clinical interpretation under the select box
        scenario_descriptions = {
            "Baseline (Moderate Hormone+ Risk)": (
                "Moderate tumor burden with balanced immune function and limited resistance; "
                "represents a typical hormone-receptor positive case."
            ),
            "High Growth / Weak Immune": (
                "High tumor proliferation with suppressed immune response; "
                "expected ↑ s_tumor, ↑ s_prolif, ↓ s_immune, ↑ s_suppress, ↑ f_metastatic."
            ),
            "High Resistance / Late Stage": (
                "Strong multi-drug resistance and high genetic instability; "
                "expected ↑ f_resist1, ↑ f_resist2, ↑ s_genetic, ↑ f_metastatic."
            ),
            "HER2-Positive / Targeted Eligible": (
                "HER2-driven disease with good organ function and moderate resistance; "
                "favors higher η_H (HER2 therapy effectiveness)."
            ),
            "Strong Immune / Low Tumor": (
                "Low tumor burden with strong immune surveillance; "
                "expected ↓ s_tumor, ↑ s_immune, low f_resist1 and f_metastatic."
            ),
        }
        st.caption(scenario_descriptions.get(example_scenario, ""))

        # Example data button
        if st.button("📝 Load Example Data", use_container_width=True):
            load_example_data(example_scenario)
            st.session_state.page = "input"
            st.session_state.example_loaded = example_scenario
            st.rerun()

        # Clear data button
        if st.button("🗑️ Clear All", use_container_width=True):
            # Remove stored biomarker and result data
            if 'biomarkers' in st.session_state:
                del st.session_state.biomarkers
            if 'results' in st.session_state:
                del st.session_state.results
            if 'patient_baseline' in st.session_state:
                del st.session_state.patient_baseline
            if 'patient_loaded_from' in st.session_state:
                del st.session_state.patient_loaded_from

            # Also clear all input widget states so fields visually reset to 0
            try:
                from biomarkers_data import ALL_BIOMARKERS
                for key in ALL_BIOMARKERS.keys():
                    widget_key = f"input_{key}"
                    if widget_key in st.session_state:
                        del st.session_state[widget_key]
            except Exception:
                # If anything goes wrong, still rerun without breaking the UI
                pass

            st.rerun()

def show_overview():
    """Display overview page"""
    st.header("🎯 Welcome to Calculator")
    
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Features")
        st.write("""
        - ✅ **47 Biomarkers:** Complete blood panel
          - 6 Tumor markers
          - 12 Immune function markers
          - 16 Resistance markers
          - 8 Metabolic markers
          - 5 Organ function markers
        - ✅ **37 Parameters:** All model parameters calculated from blood values
        - ✅ **Patient Data:** Save, load, export, import, and compare readings over time
        """)
    
    with col2:
        st.subheader("🚀 How to Use")
        st.write("""
        1. Click **"Input Data"** to enter biomarker values
        2. Use **"Patient Data"** in sidebar to save, load, or import records
        3. Click **"Load Example"** to see sample patient data
        4. Click **"Calculate Results"** when ready
        5. View 37 parameters + recommendations + **compare with previous** readings
        """)
    
    
    st.write("""
    - 🔧 **Biological Constraints:** Hierarchy enforced (λ₁ > λ₂ > λ_R1 > λ_R2)
    - 📐 **Full Formulas:** All treatment effectiveness with organ function
    - 🎯 **Validated:** Full panel R² = 0.98; CatBoost R² = 0.996 ± 0.003 
    """)

    # Scenario details: how example scenarios affect key composite scores
    st.subheader("🧪 Scenario Details (Key Scores)")
    with st.expander("How scenarios change s_tumor, s_immune, f_resist1, f_metastatic", expanded=False):
        st.markdown("""
        - **Baseline (Moderate Hormone+ Risk)**:
          - **s_tumor**: Moderate
          - **s_immune**: Moderate
          - **f_resist1**: Mild–moderate
          - **f_metastatic**: Low–moderate

        - **High Growth / Weak Immune**:
          - **s_tumor**: **High ↑** (elevated CA 15-3, CA 27-29, CEA, CTC, ctDNA)
          - **s_immune**: **Low ↓** (low CD4/CD8/NK, low IFN-γ)
          - **f_resist1**: Moderate (higher ESR1_mut/PGR/PIK3CA/Survivin)
          - **f_metastatic**: **High ↑** (more CTC, exosomes, low miR-200)

        - **High Resistance / Late Stage**:
          - **s_tumor**: High (high CA 15-3, CA 27-29, ctDNA)
          - **s_immune**: Moderate–low
          - **f_resist1**: **High ↑** (multiple hormone/PI3K/TP53/BRCA alterations)
          - **f_metastatic**: **High ↑** (high CTC, exosomes, VEGF, low miR-200)

        - **HER2-Positive / Targeted Eligible**:
          - **s_tumor**: Moderate–high
          - **s_immune**: Moderate–high (good CD4/CD8/NK, IFN-γ)
          - **f_resist1**: Mild–moderate
          - **f_metastatic**: Moderate (higher VEGF/Ang-2 but not extreme CTC)

        - **Strong Immune / Low Tumor**:
          - **s_tumor**: **Low ↓** (low CA markers, CTC, ctDNA)
          - **s_immune**: **High ↑** (strong CD4/CD8/NK, high IFN-γ)
          - **f_resist1**: Low (few resistance markers active)
          - **f_metastatic**: **Low ↓** (very low CTC/exosomes, favorable miR-200)
        """)

    display_scientific_documentation()
    display_patient_simulation()

def show_input_page():
    """Display input page"""
    if st.session_state.pop("example_loaded", None):
        st.success("Example data loaded. Adjust values as needed.")

    panel_markers = st.session_state.get("panel_core_markers")
    if panel_markers:
        st.header("📊 Enter Biomarker Values (Core Panel)")
        st.write("Enter values for the **15 Core Panel** biomarkers. All 37 parameters are still calculated; other biomarkers are imputed to reference values (Chapter 4 preprocessing).")
    else:
        st.header("📊 Enter Biomarker Values")
        st.write(f"Enter values for all {TOTAL_BIOMARKERS} biomarkers. Progress is tracked automatically.")
    
    # Get biomarker inputs (only Core 15 when Core Panel selected)
    biomarkers = get_biomarker_inputs(panel_markers=panel_markers)
    
    # Store in session state
    st.session_state.biomarkers = biomarkers
    
    # Calculate and show progress (over Core 15 when Core panel selected)
    progress = calculate_progress(biomarkers, panel_markers=st.session_state.get("panel_core_markers"))
    
    st.divider()
    st.subheader("Progress Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        lab = "Core Entered" if panel_markers else "Total Entered"
        st.metric(lab, f"{progress['total_filled']}/{progress['total']}")
    with col2:
        st.metric("Completion", f"{progress['percentage']:.1f}%")
    with col3:
        if progress['percentage'] >= 50:
            st.success("Ready to Calculate")
        else:
            st.warning("More data needed")

    # Biomarker quality control display
    st.divider()
    display_quality_control(biomarkers)

    # Action button to move to results page
    st.divider()
    if st.button("🧮 Calculate Results", use_container_width=True):
        st.session_state.page = "calculate"
        st.rerun()

def show_results_page():
    """Display results page"""
    # Get biomarkers from session state or from input page
    if 'biomarkers' in st.session_state and st.session_state.biomarkers:
        biomarkers = st.session_state.biomarkers
    else:
        # Try to get from input page
        biomarkers = get_biomarker_inputs()
        st.session_state.biomarkers = biomarkers
    
    if not biomarkers:
        st.warning("⚠️ Please enter biomarker data first!")
        st.info("Go to 'Input Data' page to enter biomarker values.")
        return
    
    # Check if we have enough data
    progress = calculate_progress(biomarkers)
    if progress['total_filled'] < 10:
        st.error(f"⚠️ Insufficient data! Please enter at least 10 biomarkers. Currently: {progress['total_filled']}/{progress['total']}")
        st.info("💡 Tip: Click 'Load Example Data' in the sidebar to load sample data.")
        return
    
    # Calculate parameters (Core panel: missing biomarkers imputed to reference values)
    core_markers = st.session_state.get("panel_core_markers")
    with st.spinner("Calculating parameters..."):
        try:
            calc_results = calculate_all_parameters(biomarkers, core_markers=core_markers)
            st.session_state.results = calc_results
        except Exception as e:
            st.error(f"❌ Calculation error: {str(e)}")
            st.exception(e)
            return
    
    # Display results (including interpretation, stability, export options)
    display_results(calc_results, biomarkers, progress)

    # Longitudinal comparison: current vs previous/saved reading
    st.divider()
    display_compare_selector(biomarkers)


def display_quality_control(biomarkers):
    """
    Run biomarker QC and display any warnings or critical alerts.
    """
    warnings, critical_alerts = validate_biomarker_inputs(biomarkers)

    if critical_alerts:
        st.error("🚨 **CRITICAL VALUES DETECTED**")
        for alert in critical_alerts:
            st.error(f"• {alert}")
        st.error("**Action Required:** Immediate clinical correlation and verification recommended")

    if warnings:
        st.warning("⚠️ **Values Outside Reference Range**")
        for warning in warnings:
            st.warning(f"• {warning}")


def display_scientific_documentation():
    """
    Show scientific validation, applications, limitations, and regulatory notes.
    """
    with st.expander("📖 Scientific Documentation & Validation"):
        st.write("""
        ### Validation Methodology
        - **Dataset:** 5,000 synthetic cancer patients with biologically realistic biomarker correlations  
        - **Machine Learning:** CatBoost R² = 0.996 ± 0.003   
        - **Mathematical Framework:** 15-dimensional coupled ODE system  
        - **Stability Analysis:** 46.7% complete stability across parameter ranges  
        - **Cross-Validation:** 8-algorithm comparison   

        ### Clinical Applications
        ✅ **Appropriate Use:**
        - Treatment selection guidance (adjunct to clinical judgment)  
        - Early resistance monitoring and detection  
        - Precision medicine screening (adjunct to clinical workflow)  
        - Research and clinical trial stratification  

        ❌ **Not Appropriate For:**
        - Primary cancer diagnosis (requires tissue confirmation)  
        - End-stage management without additional clinical data  
        - Standalone decision-making without physician oversight  

        ### Scientific Limitations
        - **Synthetic Data Foundation:** Requires prospective clinical validation  
        - **Model Simplification:** Cancer biology is more complex than 15 dimensions  
        - **Parameter Interdependencies:** May challenge clinical interpretation 
        """)

    with st.expander("⚖️ Regulatory and Ethical Considerations"):
        st.write("""
        ### Current Status
        - **Research Tool:** For educational and research purposes  
        - **Clinical Validation:** Required  
        """)


def display_patient_simulation():
    """
    Simple synthetic patient loader to demonstrate different biomarker patterns.
    Merges partial example into session biomarkers and switches to Input page.
    """
    from biomarkers_data import ALL_BIOMARKERS

    st.subheader("🧪 Synthetic Patient Examples")
    example_patients = {
        "High-Risk Aggressive": {
            'ca153': 45.2, 'cd8': 320, 'tk1': 4.8, 'ctdna': 3.2,
            'pik3ca': 8.5, 'glucose': 165, 'lactate': 3.8,
        },
        "Immunotherapy Candidate": {
            'ca153': 15.3, 'cd8': 890, 'cd4': 1250, 'ifn_gamma': 6.2,
            'pdl1_ctc': 2.8, 'il10': 3.1,
        },
        "Hormone-Responsive": {
            'ca153': 22.1, 'esr1_protein': 3.2, 'esr1_mutations': 0,
            'pgr': 8.5, 'glucose': 85, 'cd8': 650,
        },
    }

    selected_example = st.selectbox("Select Example Patient:", list(example_patients.keys()))
    if st.button("Load Example", key="synthetic_load_btn"):
        # Merge example into full biomarker dict (rest = 0)
        example_data = {k: 0.0 for k in ALL_BIOMARKERS}
        example_data.update(example_patients[selected_example])
        st.session_state.biomarkers = example_data
        # Clear widget keys so form shows new values
        for key in ALL_BIOMARKERS:
            widget_key = f"input_{key}"
            if widget_key in st.session_state:
                del st.session_state[widget_key]
        st.session_state.page = "input"
        st.session_state.example_loaded = selected_example
        st.rerun()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "overview"

if 'biomarkers' not in st.session_state:
    st.session_state.biomarkers = {}

# Page routing
if st.session_state.page == "overview":
    show_overview()
elif st.session_state.page == "equations":
    display_differential_equations()
elif st.session_state.page == "formulas":
    display_parameter_formulas()
elif st.session_state.page == "input":
    show_input_page()
elif st.session_state.page == "calculate":
    show_results_page()

