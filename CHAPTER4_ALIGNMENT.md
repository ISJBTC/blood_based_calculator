# Chapter 4 ↔ Calculator Alignment

This document confirms **perfect alignment** between `chapter4.tex.tex` and the Blood-Based Calculator.

**Note:** Changed/new parts in `chapter4.tex.tex` are marked in **blue** using `\color{blue}`. Ensure your main document loads `\usepackage{color}` or `\usepackage{xcolor}`. All formulae are scientifically consistent and implementation matches the thesis exactly.

## Aligned Elements

| Element | Chapter 4 | Calculator |
|---------|-----------|------------|
| **47 biomarkers** | Panel as defined in §4.2.1 | `biomarkers_data.py` |
| **37 parameters** | Derived in §4.3.3–4.3.7 | `calculations.py` |
| **s_activation** | (1/2)×(IFN-γ/5 + CD4/1200); 47-panel does not include IL-2 | `calculations.py` L167–172 |
| **s_stress** | = s_metabolic | `calculations.py` L164 |
| **s_quiescence** | (1/2)×(max(0,(100-Glucose)/100) + min(1, Lactate/4)) | `calculations.py` L185–188 |
| **f_CYP2D6** | min(1.0, CYP2D6/2.0) | `calculations.py` L302 |
| **f_general (η_E)** | Same as η_C, η_I: Albumin/4 + glucose term | `calculations.py` L294–298 |
| **η bounds** | 0.1 ≤ η_i ≤ 0.95 | All η formulas use max(0.1, min(0.95, …)) |
| **f_immune_ctx** | IL-10 term: max(0, 1 − IL-10/15) | `calculations.py` L318 |
| **α_acid** | max(0.01, min(0.5, 2×(7.4 − Blood pH))) | `calculations.py` L405–406 |
| **Imputation** | "median value specific to category" | Reference values for missing; Full panel imputes |

## Chapter 4 Edits Applied (for alignment)

1. **s_activation**: Changed from (1/3)(IFN-γ/5 + IL-2/2.5 + CD4/1200) to (1/2)(IFN-γ/5 + CD4/1200) with note that IL-2 is not in the 47-panel.
2. **s_stress**: Added explicit definition s_stress = s_metabolic.
3. **s_quiescence**: Added full formula (nutrient + metabolic stress).
4. **f_CYP2D6**: Added f_CYP2D6 = min(1.0, CYP2D6/2.0).
5. **f_general in η_E**: Added definition (same as chemotherapy).
6. **η bounds**: Changed all min(0.9, …) to min(0.95, …) to match validation text.
7. **f_immune_ctx**: Changed (1 − IL-10/15) to max(0, 1 − IL-10/15).
8. **α_acid**: Added derivation from Blood pH in new "ODE Supplementary" subsection.

## Scientific Completeness

- All composite scores used in parameter formulae are defined.
- All factors (f_CYP2D6, f_general, f_immune_ctx) are defined.
- All α symbols: α_A (parameter 22); α_acid (ODE, from Blood pH).
- Biological constraints (hierarchy, bounds) enforced.
