# Blood-Based Cancer Model Calculator

## Chapter 4 Implementation - Exact 47 Biomarkers

This is a modular Python application implementing the mathematical model from Chapter 4. It calculates all **37 parameters** from **47 blood biomarkers**; formulae and differential equations match chapter4.tex with no discrepancy.

## Features

- ✅ **Exact 47 Biomarkers** as specified in Chapter 4
- ✅ **All 37 Parameters** calculated using exact Chapter 4 formulas
- ✅ **Modular Architecture** - easy to maintain and extend
- ✅ **Streamlit Interface** - modern, user-friendly web interface
- ✅ **Biological Constraints** - automatic validation and correction

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your web browser.

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── biomarkers_data.py      # Biomarker definitions (47 biomarkers)
├── biomarker_input.py      # Input collection module
├── calculations.py         # All Chapter 4 formulas
├── results_display.py      # Results display module
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Biomarker Categories

- **Tumor Markers (6):** CA 15-3, CA 27-29, CEA, TK1, ctDNA, ESR1 protein
- **Immune Function (12):** CD8+, CD4+, NK, IFN-γ, IL-10, TNF-α, TGF-β, PD-L1 CTC, HLA-DR, CTC, Ang-2, Lymphocytes
- **Resistance (16):** ESR1 mutations, PGR, BRCA, PIK3CA, TP53, HER2 mutations, HER2_circ, MDR1, CYP2D6, Survivin, HSP, miR-200, Exosomes, VEGF, MRP1, Ki-67
- **Metabolic (8):** Glucose, Lactate, LDH, Albumin, Beta-hydroxybutyrate, Blood pH, Folate, Vitamin D
- **Organ Function (5):** Creatinine, BUN, ALT, AST, Bilirubin

**Total: 47 biomarkers**

## Parameters Calculated

All 37 parameters from Chapter 4 (formulae and equations match chapter4.tex exactly):

- **Growth (5):** λ₁, λ₂, λ_R1, λ_R2, K  
- **Immune (6):** β₁, β₂, φ₁, φ₂, φ₃, δ_I  
- **Resistance evolution (2):** ω_R1, ω_R2  
- **Treatment effectiveness (4):** η_E, η_C, η_H, η_I  
- **Pharmacokinetic (3):** k_el, k_metabolism, k_clearance  
- **Microenvironmental (8):** α_A, δ_A, κ_Q, λ_Q, κ_S, δ_S, γ, δ_P  
- **Genetic and metabolic (7):** μ, ν, δ_G, κ_M, δ_M, κ_H, δ_H  
- **Immune sensitivity (2):** ρ₁, ρ₂  

**Total: 37 parameters.** Composite scores (e.g. s_tumor, s_immune, G) are computed per Chapter 4 and used as inputs to these parameter formulae.

### Chapter 4 claims (alignment)

- **37 parameters from 47 biomarkers:** Chapter 4 derives all 37 core model parameters from the 47-biomarker blood panel; this app uses the same formula-based mapping.
- **15-dimensional ODEs:** The mathematical framework is a 15-dimensional coupled ODE system; formulae match chapter4.tex.
- **Panel accuracy (Table 4):** Full 47 → R² = 0.98; Optimized 25 → R² = 0.93; Core 15 → R² = 0.87. No cost or dollar figures are shown in the app.
- **ML validation:** Eight algorithms were compared on 18 parameters; CatBoost achieved R² = 0.996 ± 0.003 on the synthetic cohort (5,000 patients). This app implements the **formula-based** derivation for all 37 parameters, not the trained ML models.
- **Preprocessing:** Chapter 4 specifies normalization, **imputation of missing values with the median value that is specific to the category**, outlier handling, and QA. For the Core panel we impute non-entered biomarkers to reference (normal) values per biomarker, consistent with that step.

## Testing Panel Options (Full, Optimized, Core)

Chapter 4 describes reduced biomarker panels for different use cases. The app offers three choices; **all 37 parameters are always calculated** with the same Chapter 4 formulae. Choosing a reduced panel indicates which biomarkers you intend to use (e.g. only those listed below for Core); any biomarker not entered can be left at default (e.g. 0). No cost or pricing is implied.

| Panel | Biomarkers | Validation R² (Chapter 4) | Use case |
|-------|------------|---------------------------|----------|
| **Full** | 47 | 0.98 (panel table); CatBoost 0.996 on 18 params (ML) | Complex cases, research protocols |
| **Optimized** | 25 | 0.93 | Treatment planning, resistance monitoring |
| **Core** | 15 | 0.87 | Routine screening, basic treatment selection |

Chapter 4 states: full 47-panel accuracy R² = 0.98 (panel optimization table); CatBoost achieved R² = 0.996 ± 0.003 on 18 parameters in the ML comparison (5,000 synthetic patients). This app uses the **formula-based** derivation for all 37 parameters; reduced panels use imputation as below.

- **Full panel:** All 47 biomarkers; formulae and ODEs match chapter4.tex.
- **Optimized panel:** 25 biomarkers identified by feature selection in Chapter 4 (see fig. biomarker selection); the thesis does not enumerate the exact 25 in the text. The app uses the same 37-parameter model; you may enter only the biomarkers your lab runs for this tier.
- **Core panel:** 15 biomarkers by selection frequency (Chapter 4 feature selection). List: CA 15-3, CD8+, PIK3CA, Albumin, CEA, CD4+, ESR1 protein, IL-10, Glucose, HER2 mutations, TK1, NK cells, Lactate, MDR1 expression, IFN-γ.

All panels yield the same 37 parameters; reduced panels reflect fewer inputs with lower validation R² per Chapter 4, not a different model.

**How parameters are calculated from the Core Panel (scientific):**  
The same Chapter 4 formulas are used for all 37 parameters. They depend on composite scores (e.g. s_tumor, s_immune, f_resist1) and organ functions (f_liver, f_kidney), which in turn depend on many of the 47 biomarkers. If we only had 15 measured values and set the rest to **zero**, several formulas would be ill-defined or extreme (e.g. division by zero, or scores collapsed to 0). Chapter 4’s parameter pipeline specifies *"imputation of missing values with the median value that is specific to the category"* (Section 4.3). When the **Core panel** is selected, the app **imputes** the 32 non‑core biomarkers to **reference (normal) values** per biomarker (clinical normal ranges and formula denominators), in line with that preprocessing. That way:

1. **Composite scores** (s_tumor, s_prolif, s_immune, s_suppress, G, s_genetic, s_metabolic, f_resist1, f_resist2, f_metastatic, etc.) are computed from a full set of 47 values: your 15 entered + 32 reference values.
2. **Organ functions** (f_liver, f_kidney, f_clearance) use the same formulas with imputed organ markers (e.g. creatinine, ALT, AST) at reference levels when not in the Core panel.
3. **All 37 parameters** are then computed with the exact Chapter 4 expressions from these composite scores and organ functions.

So the Core panel provides **15 measured inputs**; the **structure** of the model (formulas and 37 parameters) is unchanged, and missing biomarkers are treated as **“reference/normal”** rather than zero, keeping the math stable and interpretable (validation R² ≈ 0.87 per Chapter 4).

**Which parameters can be calculated with only the 15 Core biomarkers?**  
All 37 are calculated (missing inputs imputed). Coverage: **Core-driven** (main inputs from Core 15): λ₁, β₁, φ₁, φ₃, δ_I, η_I, κ_Q, λ_Q, κ_S, δ_S, δ_P, ρ₁. **Partly Core**: λ₂, λ_R1, λ_R2, K, β₂, φ₂, ω_R1, ω_R2, η_E, η_C, η_H, μ, ν, δ_G, κ_M, δ_M, κ_H, ρ₂, G. **Imputed only** (no Core biomarkers in formula): k_el, k_metabolism, k_clearance, α_A, δ_A, γ, δ_H. See `CORE_PANEL_PARAMETER_COVERAGE` in `calculations.py` for the full mapping.

**How to use the Core Panel:** In the sidebar, select **"Core Panel (15 biomarkers)"**, then go to **Input Data**. Only the 15 core biomarkers are shown; enter values for those. The calculator imputes the other 32 to reference values and computes all 37 parameters. For the full 47 biomarkers, select **"Full Panel (47 biomarkers)"** in the sidebar.

## License

MIT-ADT University Research Project

