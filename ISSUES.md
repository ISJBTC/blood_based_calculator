# Systematic Issues List — Blood-Based Calculator vs Chapter 4

This document lists all known issues, deviations, and gaps between the project and **chapter4.tex** (Machine Learning-Enhanced Blood-Based Framework). Issues are grouped by category and ordered by severity where applicable.

## ✅ Solutions applied (47 biomarkers, 37 parameters unchanged)

The following fixes have been implemented so that formulae match Chapter 4 and there is no deficiency:

| Issue | Solution |
|-------|----------|
| **η_E f_general** | `f_general` for hormone therapy now uses the same formula as η_C: (1/2)×(Albumin/4.0 + glucose term). Used in `f_metabolism = (1/3)(f_liver + f_CYP2D6 + f_general)`. |
| **s_activation (IL-2 missing)** | IL-2 is not in the 47-panel; implementation uses **s_activation = (1/2)×(IFN-γ/5 + CD4/1200)** so the score is an average of the two available markers. Documented in parameter_formulas and calculations. |
| **f_CYP2D6** | Bounded as **min(1.0, cyp2d6/2.0)**; comment added that Chapter 4 does not define it explicitly. |
| **η upper bound** | All η_E, η_C, η_H, η_I now use **0.95** as upper bound (Chapter 4 validation: 0.1 ≤ η_i ≤ 0.95). |
| **f_immune_ctx** | Term (1 − IL-10/15) clamped to **max(0, 1 − IL-10/15)** so it is never negative. |
| **Full panel missing** | When Full panel is selected, **missing biomarkers are imputed to reference values** (same as Core panel), not 0. So formulae always receive a full 47-vector with no zeros for missing inputs. |
| **α_acid** | **Derived from Blood pH:** α_acid = max(0.01, min(0.5, 2×(7.4 − blood_ph))). Used in ODEs (N₁, N₂). Not one of the 37 parameters; documented in parameter_formulas and results_display. |
| **All alpha** | **α_A** = one of the 37 (angiogenesis, from VEGF/Ang-2). **α_acid** = ODE-only, from Blood pH. Chapter 4’s α₁, α₂ in Jacobian text refer to resistance evolution (ω_R1, ω_R2). |

---

## 1. Formula / Chapter 4 alignment

### 1.1 **η_E (Hormone therapy) — f_general in f_metabolism**

- **Chapter 4:**  
  `f_metabolism = (1/3)(f_liver + f_CYP2D6 + f_general)`  
  The same symbol **f_general** is defined later in the chapter for η_C and η_I as:  
  `f_general = (1/2)(Albumin/4.0 + max(0.5, 1 - 0.3×|95-Glucose|/95))`.
- **Current code:** For η_E, `f_general` is hardcoded to **1.0** (see `calculations.py` around line 295).
- **Impact:** Hormone therapy effectiveness does not reflect general health/nutrition (albumin, glucose) in the metabolism factor.
- **Recommendation:** Use the same `f_general` as for η_C (Albumin + glucose) when computing `f_metabolism` for η_E.

### 1.2 **s_activation — IL-2 missing from 47-panel**

- **Chapter 4:**  
  `s_activation = (1/3)(IFN-γ/5 + IL-2/2.5 + CD4/1200)`.
- **Current code:** IL-2 is not in the 47 biomarkers; implementation uses only IFN-γ/5 and CD4/1200 (two terms), with a comment that IL-2 is not available.
- **Impact:** φ₁ (basal immune production) is derived from an incomplete s_activation; denominator (1/3) is unchanged but one biomarker is missing.
- **Recommendation:** Either (a) document as “s_activation uses available markers only (IL-2 not in panel)” and optionally rescale to two terms, or (b) add IL-2 to the panel if the thesis intends it.

### 1.3 **f_CYP2D6 — no explicit formula in Chapter 4**

- **Chapter 4:** References `f_CYP2D6` in `f_metabolism` but does not give an explicit formula.
- **Current code:** Uses `f_CYP2D6 = cyp2d6 / 2.0` (normalization by 2.0).
- **Impact:** Implementation is a reasonable guess but not traceable to the thesis.
- **Recommendation:** Add a short comment in code and/or docs: “f_CYP2D6 not defined in Chapter 4; implementation uses cyp2d6/2.0.”

### 1.4 **Effectiveness upper bound — 0.9 vs 0.95**

- **Chapter 4:**  
  - Parameter formulas use `min(0.9, …)` for η_E, η_C, η_H, η_I.  
  - QC/validation text states: “Effectiveness: 0.1 ≤ η_i ≤ **0.95**”.
- **Current code:** Uses `min(0.9, …)` everywhere for η.
- **Impact:** Minor inconsistency: validation text allows up to 0.95, formulas cap at 0.9.
- **Recommendation:** Either change code to `min(0.95, …)` and document, or add a note in docs that “formulas use 0.9; validation text uses 0.95.”

### 1.5 **f_immune_ctx — (1 − IL-10/15) can go negative**

- **Chapter 4:**  
  `f_immune_ctx = (1/4)(CD8/700 + CD4/1050 + IFN-γ/2.0 + (1 − IL-10/15))`.
- **Current code:** Implements as written; no clamping.
- **Impact:** If IL-10 > 15, `(1 − IL-10/15)` is negative; f_immune_ctx can decrease or go negative.
- **Recommendation:** Consider clamping the IL-10 term, e.g. `max(0, 1 - il10/15)`, and document.

---

## 2. Parameters with no explicit Chapter 4 formula

Chapter 4 describes these in the ODE text but does **not** give explicit biomarker-derived formulas in the parameter-derivation section. The code uses plausible heuristics.

| Parameter | Chapter 4 description | Current implementation | Issue |
|-----------|------------------------|------------------------|--------|
| **ν** (nu) | “Rate ν captures treatment-induced mutagenesis” | `0.002 × s_genetic × (1 + s_stress)` | Heuristic; not in Chapter 4. |
| **δ_G** | “Natural DNA repair restores at rate δ_G” | `0.01 × brca_factor × G` | Heuristic; not in Chapter 4. |
| **κ_M** | “Derived from glucose, lactate, LDH”; “beta-hydroxybutyrate inversely modulates” | `0.02 × s_metabolic × beta_hydroxybutyrate_factor` | Reasonable but no explicit formula. |
| **δ_M** | “Natural metabolic normalization at rate δ_M” | `0.01 × (1 - 0.5×s_metabolic)` | Heuristic; not in Chapter 4. |
| **κ_H** | Hypoxia induction when N_total/K > 0.5 | `0.02 × max(0, s_tumor - 0.5)` | Interpretable but no explicit formula. |
| **δ_H** | “Natural oxygenation… rate δ_H” | `0.05 × (1 + f_clearance)` | Heuristic; not in Chapter 4. |
| **ρ₁, ρ₂** | Ranges only: ρ₁ ∈ [0.6, 0.9], ρ₂ ∈ [0.3, 0.6] | Formulas in code that keep values in range | No formulas in Chapter 4. |

**Recommendation:** In code and/or docs, label these as “heuristic / not explicitly given in Chapter 4” so reviewers know they are implementation choices.

---

## 3. Composite scores

### 3.1 **s_quiescence — undefined in Chapter 4**

- **Chapter 4:** Uses `s_quiescence` in κ_Q and λ_Q formulas but does **not** define it.
- **Current code:**  
  `(nutrient_stress + metabolic_stress) / 2` with nutrient_stress = max(0, (100−glucose)/100), metabolic_stress = min(1, lactate/4).
- **Impact:** Implementation is a biological approximation; not traceable to thesis.
- **Recommendation:** Document as “s_quiescence not defined in Chapter 4; implementation uses glucose/lactate stress.”

### 3.2 **s_stress — not separately defined in Chapter 4**

- **Chapter 4:** Uses `s_stress` in δ_I, ω_R1, ω_R2, κ_S; only **s_metabolic** is explicitly defined.
- **Current code:** Sets `s_stress = s_metabolic`.
- **Impact:** Reasonable and consistent; no bug.
- **Recommendation:** Optional: add one sentence in docs that “s_stress is identified with s_metabolic where used.”

---

## 4. Preprocessing and missing values

### 4.1 **Full panel — missing biomarkers default to 0**

- **Chapter 4:** Preprocessing: “imputation of missing values with the **median value that is specific to the category**”.
- **Current code:** When **Full panel** is selected, `get_biomarkers_for_calculation(..., core_markers=None)` uses `biomarkers.get(k, 0.0)` for any missing key. So missing biomarkers are set to **0**, not to a category median or reference value.
- **Impact:** If the user selects Full panel but leaves some inputs blank, formulas see 0 instead of imputed normals; scores (e.g. s_tumor, s_immune) can be skewed or undefined (e.g. division by zero if a denominator is 0).
- **Recommendation:** For Full panel, impute missing biomarkers to the same `REFERENCE_VALUES_FOR_IMPUTATION` (or category medians) instead of 0, and document that “missing = imputed to reference/normal”.

### 4.2 **Core panel imputation — “median” vs “reference value”**

- **Chapter 4:** “Imputation of missing values with the **median** value that is specific to the **category**.”
- **Current code:** Core panel imputes to **per-biomarker reference (normal) values** from `REFERENCE_VALUES_FOR_IMPUTATION`, not category medians.
- **Impact:** Conceptually close (both avoid zeros and stabilize formulas) but not literally “category median”.
- **Recommendation:** In docs (e.g. README/ISSUES), state: “Chapter 4 specifies category median; we use per-biomarker reference values for stability and interpretability.”

---

## 5. Organ function formulas

- **Chapter 4:** Gives explicit formulas for f_liver (ALT, AST, Bilirubin) and f_kidney (Creatinine, BUN) with the same structure (max/min, denominators).
- **Current code:** Matches that structure (e.g. 40/max(ALT,5), 45/max(AST,8), 1.2/max(Bilirubin,0.1); 1.2/max(Creat,0.5), 20/max(BUN,5)).
- **Status:** Aligned; no issue.

---

## 6. Biological constraints

### 6.1 **Effectiveness lower bound**

- **Chapter 4:** “Effectiveness: 0.1 ≤ η_i ≤ 0.95”.
- **Current code:** All η formulas use `max(0.1, min(0.9, …))`, so lower bound 0.1 is enforced. ✅

### 6.2 **Growth rate hierarchy**

- **Chapter 4:** “Hierarchy: λ₁ > λ₂ > λ_R1 > λ_R2”.
- **Current code:** Enforced by post-hoc adjustment (e.g. if λ₁ ≤ λ₂, set λ₂ = λ₁×0.99) and appended to `constraint_violations`. ✅

### 6.3 **β₁ and ω bounds**

- **Chapter 4:** “Immune: β₁ > 0.001”; “Resistance: ω_R1, ω_R2 < 0.01”.
- **Current code:** Formulas use `max(0.001, …)` for β₁ and `min(0.01, …)` / `min(0.008, …)` for ω_R1/ω_R2, so bounds are respected. ✅

---

## 7. File and naming

### 7.1 **Chapter source file name**

- **Observation:** The LaTeX file is named **chapter4.tex.tex** (double extension).
- **Impact:** Cosmetic; may cause confusion or broken references if a build expects `chapter4.tex`.
- **Recommendation:** Rename to `chapter4.tex` if that matches the rest of the thesis/build.

---

## 8. ODE / model details

### 8.1 **α_acid (pH factor)**

- **Chapter 4:** The N₁ (and N₂) ODE uses a term `(1 + 0.1 M) / (1 + α_acid M)`; α_acid is not given an explicit derivation in the parameter-derivation subsection.
- **Current code:** Comment in `calculations.py`: “alpha_acid is used in differential equations but NOT explicitly derived in Chapter 4”.
- **Impact:** If the ODE solver or reporting uses α_acid, it must be set elsewhere (constant or placeholder); no biomarker-derived formula.
- **Recommendation:** Document that α_acid is not among the 37 derived parameters and how it is set (e.g. constant or N/A).

---

## 9. Testing and validation

### 9.1 **Unit consistency**

- **Potential issue:** Some formulas assume specific units (e.g. ctDNA/1.0 possibly as fraction or %; Exosomes/100; Glucose in mg/dL). If inputs are entered in different units, results will be wrong.
- **Recommendation:** In `biomarkers_data` and UI, document units for each biomarker and, if possible, validate or convert (e.g. ctDNA % vs fraction).

### 9.2 **Test data — missing biomarkers set to 0**

- **Current code:** `test_calculations.py` sets any missing biomarker keys to 0.0 for the example dict.
- **Impact:** Same as 4.1: formulas see 0 instead of reference values; test is not representative of “Full panel with imputation”.
- **Recommendation:** For a “full panel” test, either supply all 47 values or use the same reference imputation as the Core panel for missing keys.

---

## 10. Summary table

| # | Category | Issue | Severity | Location |
|---|----------|--------|----------|----------|
| 1.1 | Formula | η_E: f_general hardcoded to 1.0 instead of Albumin+glucose | Medium | calculations.py |
| 1.2 | Formula | s_activation: IL-2 missing from 47-panel | Medium | calculations.py |
| 1.3 | Formula | f_CYP2D6 not defined in Chapter 4; code uses cyp2d6/2.0 | Low | calculations.py |
| 1.4 | Formula | η upper bound 0.9 in code vs 0.95 in validation text | Low | calculations.py / docs |
| 1.5 | Formula | f_immune_ctx: (1−IL-10/15) can be negative | Low | calculations.py |
| 2 | Parameters | ν, δ_G, κ_M, δ_M, κ_H, δ_H, ρ₁, ρ₂ — no explicit Ch4 formulas | Low | calculations.py / docs |
| 3.1 | Composite | s_quiescence undefined in Chapter 4 | Low | calculations.py / docs |
| 3.2 | Composite | s_stress = s_metabolic (documentation only) | Info | docs |
| 4.1 | Preprocessing | Full panel: missing → 0 instead of imputation | High | calculations.py |
| 4.2 | Preprocessing | Core: reference values vs “category median” | Low | docs |
| 7.1 | Naming | chapter4.tex.tex double extension | Low | repo |
| 8.1 | ODE | α_acid not derived in Chapter 4 | Info | calculations.py / differential_equations |
| 9.1 | Validation | Unit consistency (ctDNA, Exosomes, etc.) | Medium | biomarkers_data / UI |
| 9.2 | Testing | test_calculations uses 0 for missing biomarkers | Low | test_calculations.py |

---

**Severity:**

- **High:** Can materially affect results or stability (e.g. Full-panel missing → 0).
- **Medium:** Deviation from Chapter 4 or plausible user data (η_E f_general, s_activation, units).
- **Low:** Clarification, documentation, or minor consistency (bounds, naming, heuristics).
- **Info:** Documentation or design note only.

If you want, the next step can be concrete code/doc changes for any of these (e.g. 1.1, 4.1, 9.1).
