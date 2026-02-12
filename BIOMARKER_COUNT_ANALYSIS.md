# Biomarker Count Analysis - Chapter 4 vs Current HTML

## Chapter 4 Specification: 47 Biomarkers

### Tumor Markers (6) - ✓ CORRECT
1. CA 15-3 ✓
2. CA 27-29 ✓
3. CEA ✓
4. TK1 ✓
5. ctDNA ✓
6. ESR1 protein ✓

### Immune Function Markers (12) - ❌ ISSUES FOUND
**Chapter 4 Lists:**
1. CD8+ T cells ✓
2. CD4+ T cells ✓
3. NK cells ✓
4. IFN-γ ✓
5. IL-10 ✓
6. TNF-α ❌ MISSING in HTML
7. TGF-β ✓ (I added this correctly)
8. PD-L1 CTC ✓
9. HLA-DR ✓
10. CTC (Circulating tumor cells) ✓
11. Ang-2 ✓
12. Total lymphocyte count ✓

**Current HTML Has (13):**
1. CD8+ ✓
2. CD4+ ✓
3. NK ✓
4. B cells ❌ NOT in Chapter 4
5. Neutrophils ❌ NOT in Chapter 4
6. IFN-γ ✓
7. IL-2 ❌ NOT in Chapter 4 (mentioned but not in 12-count)
8. IL-10 ✓
9. TGF-β ✓
10. PD-L1 CTC ✓
11. HLA-DR ✓
12. Complement C3 ❌ NOT in Chapter 4
13. Immunoglobulins ❌ NOT in Chapter 4

**FIX NEEDED:** Remove B cells, Neutrophils, IL-2, Complement C3, Immunoglobulins. Add TNF-α.

### Resistance Markers (16) - ❌ ISSUES FOUND
**Chapter 4 Lists:**
1. ESR1 mutations ✓
2. PGR ✓ (I added this correctly)
3. BRCA mutations ❌ MISSING in HTML
4. PIK3CA mutations ✓
5. TP53 mutations ✓ (I added this correctly)
6. HER2 mutations ✓
7. MDR1 ✓
8. MRP1 ❌ MISSING in HTML
9. BCRP ❌ MISSING in HTML
10. LRP ❌ MISSING in HTML
11. ABCG2 ❌ MISSING in HTML
12. Ki-67 ❌ MISSING in HTML
13. Survivin ✓
14. Vimentin ❌ MISSING in HTML
15. N-cadherin ❌ MISSING in HTML
16. E-cadherin ❌ MISSING in HTML

**Current HTML Has (19):**
1. PIK3CA ✓
2. TP53 ✓
3. ESR1 mutations ✓
4. PGR ✓
5. HER2 mutations ✓
6. HER2_circ ❌ NOT in Chapter 4 (mentioned but not in 16-count)
7. CYP2D6 ✓ (used in formulas)
8. MDR1 ✓
9. Survivin ✓
10. HSP ✓ (used in formulas)
11. miR-21 ❌ NOT in Chapter 4
12. miR-200 ✓ (used in formulas)
13. Exosomes ✓ (used in formulas)
14. VEGF ✓ (used in formulas)
15. CTC ✓ (but this is in Immune section!)
16. Ang-2 ✓ (but this is in Immune section!)
17. Lymphocytes ✓ (but this is in Immune section!)
18. Folate ✓ (but this is in Metabolic section!)
19. Vitamin D ✓ (but this is in Metabolic section!)

**FIX NEEDED:** 
- Remove: HER2_circ, miR-21
- Add: BRCA, MRP1, BCRP, LRP, ABCG2, Ki-67, Vimentin, N-cadherin, E-cadherin
- Move CTC, Ang-2, Lymphocytes to Immune (they're counted there)
- Move Folate, Vitamin D to Metabolic (they're counted there)
- Keep CYP2D6, HSP, miR-200, Exosomes, VEGF (used in formulas but may need to verify)

### Metabolic Markers (8) - ❌ ISSUES FOUND
**Chapter 4 Lists:**
1. Glucose ✓
2. Lactate ✓
3. LDH ✓
4. Albumin ✓
5. Beta-hydroxybutyrate ❌ MISSING (we have "ketones" - need to verify)
6. Blood pH ❌ MISSING (we have bicarbonate, CO2, anion_gap - need to verify)
7. Folate ✓ (currently in Resistance tab - WRONG!)
8. Vitamin D ✓ (currently in Resistance tab - WRONG!)

**Current HTML Has (8):**
1. Albumin ✓
2. Glucose ✓
3. Lactate ✓
4. Bicarbonate ✓ (may be pH-related)
5. LDH ✓
6. Ketones ✓ (may be Beta-hydroxybutyrate)
7. CO2 ✓ (may be pH-related)
8. Anion Gap ✓ (may be pH-related)

**FIX NEEDED:** 
- Move Folate and Vitamin D from Resistance to Metabolic
- Verify if Ketones = Beta-hydroxybutyrate
- Verify if Blood pH is represented by Bicarbonate/CO2/Anion Gap or needs separate input

### Organ Function Markers (5) - ✓ CORRECT
1. Creatinine ✓
2. BUN ✓
3. ALT ✓
4. AST ✓
5. Bilirubin ✓

## Summary

**Current Count:** 51 biomarkers
**Target Count:** 47 biomarkers

**Issues:**
1. Immune: Has extra markers (B cells, Neutrophils, IL-2, Complement C3, Immunoglobulins), missing TNF-α
2. Resistance: Has wrong markers (HER2_circ, miR-21), missing many (BRCA, MRP1, BCRP, LRP, ABCG2, Ki-67, Vimentin, N-cadherin, E-cadherin), has markers that belong elsewhere (CTC, Ang-2, Lymphocytes, Folate, Vitamin D)
3. Metabolic: Missing Folate and Vitamin D (they're in Resistance tab), may need Blood pH clarification

**Action Required:**
1. Remove extra markers that aren't in Chapter 4
2. Add missing markers from Chapter 4
3. Move markers to correct categories
4. Verify which markers are actually used in formulas vs just mentioned

