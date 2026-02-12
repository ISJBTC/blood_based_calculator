# Corrected 47 Biomarkers List - Per Chapter 4

## Based on Chapter 4 Explicit Lists + Formula Requirements

### Tumor Markers (6) ✓
1. CA 15-3
2. CA 27-29
3. CEA
4. TK1
5. ctDNA
6. ESR1 protein

### Immune Function Markers (12) ✓
1. CD8+ T cells
2. CD4+ T cells
3. NK cells
4. IFN-γ
5. IL-10
6. TNF-α (MISSING - need to add)
7. TGF-β (already added)
8. PD-L1 CTC
9. HLA-DR
10. CTC (Circulating tumor cells) - currently in Resistance tab, needs to move
11. Ang-2 (Angiopoietin-2) - currently in Resistance tab, needs to move
12. Total lymphocyte count - currently in Resistance tab, needs to move

**REMOVE from HTML:** B cells, Neutrophils, IL-2, Complement C3, Immunoglobulins

### Resistance Markers (16) - NEEDS MAJOR FIX
**Must Include (from formulas + Chapter 4):**
1. ESR1 mutations
2. PGR (already added)
3. PIK3CA mutations
4. TP53 mutations (already added)
5. HER2 mutations
6. HER2_circ (used in formula - line 468)
7. MDR1
8. CYP2D6 (used in formula - line 423)
9. Survivin
10. HSP (used in formula - line 322)
11. miR-200 (used in formula - line 554)
12. Exosomes (used in formula - line 550)
13. VEGF (used in formula - line 514, but may be counted elsewhere)

**Chapter 4 Also Lists (but may not all be in 16):**
- BRCA mutations
- MRP1, BCRP, LRP, ABCG2
- Ki-67
- Vimentin, N-cadherin, E-cadherin

**REMOVE from HTML:** miR-21 (not in Chapter 4)

**MOVE OUT:** CTC, Ang-2, Lymphocytes (to Immune), Folate, Vitamin D (to Metabolic)

### Metabolic Markers (8) ✓
1. Glucose
2. Lactate
3. LDH
4. Albumin
5. Beta-hydroxybutyrate (we have "Ketones" - verify if same)
6. Blood pH (we have Bicarbonate, CO2, Anion Gap - may represent pH)
7. Folate (currently in Resistance tab - needs to move)
8. Vitamin D (currently in Resistance tab - needs to move)

**KEEP:** Bicarbonate, CO2, Anion Gap (may be pH-related, or need to clarify)

### Organ Function Markers (5) ✓
1. Creatinine
2. BUN
3. ALT
4. AST
5. Bilirubin

## Action Plan

1. **Fix Immune Tab:** Remove B cells, Neutrophils, IL-2, Complement C3, Immunoglobulins. Add TNF-α. Move CTC, Ang-2, Lymphocytes from Resistance.

2. **Fix Resistance Tab:** Remove miR-21, HER2_circ (or verify if it's actually in the 16). Add missing markers if needed. Move Folate, Vitamin D to Metabolic. Keep CYP2D6, HSP, miR-200, Exosomes, VEGF (they're used in formulas).

3. **Fix Metabolic Tab:** Move Folate and Vitamin D from Resistance. Verify Beta-hydroxybutyrate vs Ketones. Verify Blood pH representation.

4. **Verify Total:** Must equal exactly 47 biomarkers.

## Key Question

Some biomarkers used in formulas (HER2_circ, CYP2D6, HSP, miR-200, Exosomes, VEGF) are not explicitly listed in the Chapter 4 category breakdowns. They MUST be part of the 47, but where are they counted?

**Hypothesis:** They may be counted within the 16 resistance markers, or some (like VEGF, Ang-2) may be counted in Immune section. Need to verify exact categorization.

