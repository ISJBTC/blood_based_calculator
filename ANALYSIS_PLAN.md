# Model Calculator Analysis & Fix Plan
## Based on Chapter 4 Requirements

### Executive Summary
After thorough analysis of `chapter4.tex.tex`, I've identified **multiple critical discrepancies** between the current HTML calculator implementation and the exact formulas specified in Chapter 4. The calculator needs comprehensive fixes to match the thesis specifications exactly.

---

## 🔴 CRITICAL ISSUES FOUND

### 1. **Composite Score Calculations - MAJOR DISCREPANCIES**

#### Tumor Burden Score
- **Chapter 4 Formula:**
  ```
  s_tumor = (1/5) × (CA15-3/31.3 + CA27-29/38 + CEA/3.0 + CTC/5 + ctDNA/1.0)
  ```
- **Current HTML:** Uses different denominators and missing normalization
- **Fix Required:** ✅ Implement exact formula

#### Proliferation Score
- **Chapter 4 Formula:**
  ```
  s_prolif = (1/4) × (TK1/2.0 + Glucose/95 + Lactate/2.2 + Survivin/0.5)
  ```
- **Current HTML:** Uses different denominators (e.g., Survivin/6 instead of /0.5)
- **Fix Required:** ✅ Implement exact formula

#### Immune Strength Score
- **Chapter 4 Formula:**
  ```
  s_immune = 0.4×(CD8/700) + 0.3×(CD4/1050) + 0.2×(NK/345) + 0.1×(IFN-γ/2.0)
  ```
- **Current HTML:** Uses different denominators (e.g., CD8/900, CD4/1200, NK/250)
- **Fix Required:** ✅ Implement exact formula with correct weights

#### Immunosuppression Score
- **Chapter 4 Formula:**
  ```
  s_suppress = (1/3) × (IL-10/5.0 + TGF-β/2.5 + PD-L1/1.0)
  ```
- **Current HTML:** Missing TGF-β biomarker input
- **Fix Required:** ✅ Add TGF-β input OR handle missing biomarker

#### Genetic Stability Score
- **Chapter 4 Formula:**
  ```
  G = max(0.1, min(1.0, 1 - 0.3×(ctDNA/1.0) - 0.2×(PIK3CA/10) - 0.2×(TP53/10)))
  ```
- **Current HTML:** Missing TP53 biomarker
- **Fix Required:** ✅ Add TP53 input OR handle missing biomarker

#### Metabolic Stress Score
- **Chapter 4 Formula:**
  ```
  s_metabolic = (1/3) × (Glucose/95 + Lactate/2.2 + LDH/250)
  ```
- **Current HTML:** Uses different formula (lactate/4.0, albumin stress, ldh/400)
- **Fix Required:** ✅ Implement exact formula

#### Resistance Scores
- **Chapter 4 Formula Type 1:**
  ```
  f_resist1 = max(0.1, min(2.0, (1/4)×(ESR1_mut/8 + PGR/20 + PIK3CA/5 + Survivin/6)))
  ```
- **Current HTML:** Missing PGR biomarker
- **Fix Required:** ✅ Add PGR input OR handle missing biomarker

- **Chapter 4 Formula Type 2:**
  ```
  f_resist2 = max(0.1, min(2.0, (1/4)×(HER2_mut/10 + MDR1/150 + Survivin/6 + HSP/10)))
  ```
- **Current HTML:** ✅ Mostly correct, but verify denominators

---

### 2. **Growth Parameters - FORMULA ERRORS**

#### λ₁ (Sensitive Cell Growth Rate)
- **Chapter 4 Formula:**
  ```
  λ₁ = max(0.01, min(0.15, 0.04 × (1 + 1.5 × s_prolif)))
  ```
- **Current HTML:** Uses `0.05 × proliferationScore × pHFactor`
- **Fix Required:** ✅ Use exact formula (no pH factor in λ₁ calculation)

#### λ₂ (Partially Resistant Growth Rate)
- **Chapter 4 Formula:**
  ```
  λ₂ = max(0.005, min(0.1, 0.6 × λ₁ × (1 + 0.5 × f_resist1)))
  ```
- **Current HTML:** Uses `λ₁ × 0.6 × (1 + pik3ca/5)` - WRONG
- **Fix Required:** ✅ Use exact formula with f_resist1

#### λ_R1 (Hormone-Resistant Growth)
- **Chapter 4 Formula:**
  ```
  λ_R1 = max(0.003, min(0.05, 0.4 × λ₁ × f_resist1))
  ```
- **Current HTML:** Uses `λ₁ × 0.3 × resistFactor1` - WRONG coefficient
- **Fix Required:** ✅ Use exact formula

#### λ_R2 (Multi-Drug Resistant Growth)
- **Chapter 4 Formula:**
  ```
  λ_R2 = max(0.001, min(0.03, 0.25 × λ₁ × (1 - 0.3 × f_resist2)))
  ```
- **Current HTML:** Uses `λ₁ × 0.2 × resistFactor2` - WRONG formula
- **Fix Required:** ✅ Use exact formula

#### K (Carrying Capacity)
- **Chapter 4 Formula:**
  ```
  K = max(100, min(15000, s_tumor × 2000))
  ```
- **Current HTML:** Uses `tumorBurden × 2000` - might be using wrong score
- **Fix Required:** ✅ Verify uses s_tumor score

---

### 3. **Immune Parameters - FORMULA ERRORS**

#### β₁ (Cytotoxic Immune Killing)
- **Chapter 4 Formula:**
  ```
  β₁ = max(0.001, min(0.1, 0.02 × s_immune × (1 - s_suppress)))
  ```
- **Current HTML:** ✅ Formula looks correct but verify scores

#### β₂ (Regulatory Suppression)
- **Chapter 4 Formula:**
  ```
  β₂ = max(0.01, min(0.5, 0.05 + 0.15 × s_suppress))
  ```
- **Current HTML:** ✅ Formula looks correct

#### φ₁ (Basal Immune Production)
- **Chapter 4 Formula:**
  ```
  φ₁ = max(0.01, min(0.2, 0.05 + 0.1 × s_activation))
  ```
  where `s_activation = (1/3) × (IFN-γ/5 + IL-2/2.5 + CD4/1200)`
- **Current HTML:** ✅ Formula looks correct

#### φ₂ (Tumor-Induced Recruitment)
- **Chapter 4 Formula:**
  ```
  φ₂ = max(0.005, min(0.1, 0.01 + 0.03 × (s_tumor/2)))
  ```
- **Current HTML:** Uses `0.01 + 0.03 × (tumorBurden/2)` - verify score

#### φ₃ (Regulatory Recruitment)
- **Chapter 4 Formula:**
  ```
  φ₃ = max(0.005, min(0.15, 0.02 + 0.08 × (IL-10/15)))
  ```
- **Current HTML:** ✅ Formula looks correct

#### δ_I (Immune Cell Death)
- **Chapter 4 Formula:**
  ```
  δ_I = max(0.02, min(0.3, 0.05 + 0.1 × s_stress))
  ```
- **Current HTML:** Uses `stressFactor` - need to verify if s_stress = s_metabolic

---

### 4. **Resistance Evolution Parameters**

#### ω_R1 (Hormone Resistance Evolution)
- **Chapter 4 Formula:**
  ```
  ω_R1 = max(0.0001, min(0.01, 0.002 × s_genetic × s_stress))
  ```
  where `s_genetic = (1/3) × (ctDNA/1.0 + PIK3CA/10 + TP53/10)`
- **Current HTML:** Uses `geneticInstability × stressFactor` - need to verify formulas
- **Fix Required:** ✅ Use exact s_genetic formula (includes TP53)

#### ω_R2 (Multi-Drug Resistance Evolution)
- **Chapter 4 Formula:**
  ```
  ω_R2 = max(0.0001, min(0.008, 0.001 × s_genetic × s_stress))
  ```
- **Current HTML:** ✅ Formula structure correct, verify scores

---

### 5. **Treatment Effectiveness Parameters**

#### η_E (Hormone Therapy)
- **Chapter 4 Formula:**
  ```
  η_E = max(0.1, min(0.9, f_receptor × f_metabolism × f_resist_hormone))
  ```
  where:
  - `f_receptor = min(1.0, ESR1_protein/6.0)`
  - `f_metabolism = (1/3) × (f_liver + f_CYP2D6 + f_general)`
  - `f_resist_hormone = 1 - min(0.9, 0.6×(ESR1_mut/8) + 0.4×s_genetic)`
- **Current HTML:** ✅ Structure correct, verify all components

#### η_C (Chemotherapy)
- **Chapter 4 Formula:**
  ```
  η_C = max(0.1, min(0.9, f_general × f_organs × (1 - 0.7 × f_resist2)))
  ```
  where:
  - `f_general = (1/2) × (Albumin/4.0 + max(0.5, 1 - 0.3×|95-Glucose|/95))`
  - `f_organs = (1/2) × (f_liver + f_kidney)`
- **Current HTML:** ✅ Structure correct, verify formulas

#### η_H (HER2 Therapy)
- **Chapter 4 Formula:**
  ```
  η_H = max(0.1, min(0.9, f_HER2 × f_organs × (1 - 0.5 × f_resist2)))
  ```
  where:
  - `f_HER2 = min(1.0, HER2_circ/5.0) × (1 - 0.6 × HER2_mut/10)`
- **Current HTML:** Missing HER2_circ biomarker
- **Fix Required:** ✅ Add HER2_circ input OR handle missing biomarker

#### η_I (Immunotherapy)
- **Chapter 4 Formula:**
  ```
  η_I = max(0.1, min(0.9, f_PDL1 × f_immune_ctx × f_general))
  ```
  where:
  - `f_PDL1 = min(1.0, PD-L1_CTC/3.0)`
  - `f_immune_ctx = (1/4) × (CD8/700 + CD4/1050 + IFN-γ/2.0 + (1 - IL-10/15))`
- **Current HTML:** ✅ Structure correct, verify denominators

---

### 6. **Pharmacokinetic Parameters**

#### k_el (Drug Elimination)
- **Chapter 4 Formula:**
  ```
  k_el = max(0.05, min(0.3, 0.1 / f_clearance))
  ```
  where `f_clearance = f_liver × f_kidney`
- **Current HTML:** ✅ Formula correct

---

### 7. **Microenvironmental Parameters**

#### α_A (Angiogenesis Induction)
- **Chapter 4 Formula:**
  ```
  α_A = max(0.001, min(0.1, 0.02 × (1 + VEGF/400) × (1 + Ang-2/3000)))
  ```
- **Current HTML:** ✅ Formula correct

#### δ_A (Angiogenesis Degradation)
- **Chapter 4 Formula:**
  ```
  δ_A = max(0.05, min(0.2, 0.1 × f_clearance))
  ```
- **Current HTML:** ✅ Formula correct

#### κ_Q (Quiescence Entry)
- **Chapter 4 Formula:**
  ```
  κ_Q = max(0.001, min(0.05, 0.005 + 0.02 × s_quiescence))
  ```
- **Current HTML:** Uses custom quiescence score - need to verify formula
- **Fix Required:** ✅ Find or define s_quiescence formula

#### κ_S (Senescence Induction)
- **Chapter 4 Formula:**
  ```
  κ_S = max(0.001, min(0.04, 0.002 + 0.01 × s_stress))
  ```
- **Current HTML:** Uses `stressFactor` - need to verify if s_stress = s_metabolic

#### δ_S (Senescent Clearance)
- **Chapter 4 Formula:**
  ```
  δ_S = max(0.02, min(0.1, 0.05 × s_immune))
  ```
- **Current HTML:** ✅ Formula correct

#### γ (Metastatic Seeding)
- **Chapter 4 Formula:**
  ```
  γ = max(0.0001, min(0.01, 0.002 × f_metastatic))
  ```
  where:
  - `f_metastatic = (1/3) × (CTC/20 + f_EMT + Exosomes/100)`
  - `f_EMT = max(0, (5 - miR-200)/5)`
- **Current HTML:** ✅ Formula correct

#### δ_P (Metastatic Clearance)
- **Chapter 4 Formula:**
  ```
  δ_P = max(0.02, min(0.1, 0.05 + 0.03 × s_immune))
  ```
- **Current HTML:** ✅ Formula correct

---

### 8. **Missing Biomarkers**

The following biomarkers are referenced in Chapter 4 but may be missing from the HTML calculator:
1. **TGF-β** - Used in immunosuppression score
2. **TP53** - Used in genetic stability and genetic score
3. **PGR** (Progesterone Receptor) - Used in resistance score type 1
4. **HER2_circ** - Used in HER2 therapy effectiveness

**Options:**
- Add these as input fields
- Use default/median values if not available
- Modify formulas to handle missing biomarkers gracefully

---

### 9. **Biological Constraints**

Chapter 4 specifies:
```
Hierarchy: λ₁ > λ₂ > λ_R1 > λ_R2
Effectiveness: 0.1 ≤ η_i ≤ 0.95
Immune: β₁ > 0.001
Resistance: ω_R1, ω_R2 < 0.01
```

**Current HTML:** Has some constraints but may not enforce hierarchy properly
**Fix Required:** ✅ Implement all constraint validations

---

### 10. **pH Factor Issue**

- **Chapter 4:** Mentions pH effects in differential equations but **no explicit pH factor formula** in parameter derivation section
- **Current HTML:** Has `calculatePHFactor()` function
- **Fix Required:** ✅ Verify if pH factor should be removed or if formula exists elsewhere

---

### 11. **Stress Score vs Metabolic Stress Score**

- **Chapter 4:** Defines `s_metabolic` explicitly
- **Chapter 4:** Uses `s_stress` in formulas but doesn't explicitly define it
- **Current HTML:** Has custom `calculateStressFactor()` 
- **Fix Required:** ✅ Verify if `s_stress = s_metabolic` or find actual definition

---

### 12. **Quiescence Score**

- **Chapter 4:** Uses `s_quiescence` but doesn't explicitly define it
- **Current HTML:** Has custom `calculateQuiescenceScore()`
- **Fix Required:** ✅ Find definition or verify current implementation is acceptable

---

## 📋 IMPLEMENTATION PLAN

### Phase 1: Fix Composite Scores
1. Fix tumor burden score formula
2. Fix proliferation score formula (Survivin denominator)
3. Fix immune strength score (denominators and weights)
4. Fix immunosuppression score (add TGF-β handling)
5. Fix genetic stability score (add TP53 handling)
6. Fix metabolic stress score formula
7. Fix resistance scores (add PGR handling)

### Phase 2: Fix Growth Parameters
1. Fix λ₁ formula (remove pH factor, use exact formula)
2. Fix λ₂ formula (use f_resist1)
3. Fix λ_R1 formula (correct coefficient)
4. Fix λ_R2 formula (correct formula)
5. Verify K calculation

### Phase 3: Fix Immune & Resistance Parameters
1. Verify all immune parameter formulas
2. Fix resistance evolution formulas (add TP53 to s_genetic)
3. Verify stress score usage

### Phase 4: Fix Treatment Effectiveness
1. Verify all treatment effectiveness formulas
2. Add HER2_circ handling
3. Verify all sub-factors

### Phase 5: Handle Missing Biomarkers
1. Decide on approach (add inputs vs defaults)
2. Implement missing biomarker handling
3. Update formulas to be robust

### Phase 6: Implement Constraints
1. Add hierarchy validation (λ₁ > λ₂ > λ_R1 > λ_R2)
2. Add all bound validations
3. Add constraint warnings/errors

### Phase 7: Testing & Validation
1. Test with example data
2. Verify all 37 parameters calculated
3. Verify constraints are met
4. Compare outputs with expected values

---

## 🎯 RECOMMENDATION

**Continue with HTML** - The current HTML implementation is well-structured and can be fixed. The issues are primarily formula discrepancies that can be corrected systematically. No need to switch to a different technology unless there are specific requirements for interactivity or deployment that HTML cannot meet.

---

## ⚠️ NOTES

- Some formulas reference biomarkers that may not be in the 47-biomarker panel (e.g., TP53, PGR, TGF-β, HER2_circ). Need to clarify if these should be:
  1. Added to the panel (making it >47 biomarkers)
  2. Estimated from other biomarkers
  3. Set to default values
  4. Formulas modified to exclude them

- The chapter mentions 37 parameters but the calculator may need to calculate additional intermediate scores (composite scores) that are not part of the 37 final parameters.

