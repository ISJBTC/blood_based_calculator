"""
Biomarker Data Module
Exact 47 biomarkers as specified in Chapter 4
"""

# Tumor Markers (6)
TUMOR_MARKERS = {
    'ca153': {
        'name': 'CA 15-3 (Cancer Antigen 15-3)',
        'unit': 'U/mL',
        'normal': '< 25 U/mL',
        'category': 'tumor'
    },
    'ca2729': {
        'name': 'CA 27-29 (Cancer Antigen 27-29)',
        'unit': 'U/mL',
        'normal': '< 38 U/mL',
        'category': 'tumor'
    },
    'cea': {
        'name': 'CEA (Carcinoembryonic Antigen)',
        'unit': 'ng/mL',
        'normal': '< 3.0 ng/mL',
        'category': 'tumor'
    },
    'tk1': {
        'name': 'TK1 (Thymidine Kinase 1)',
        'unit': 'U/L',
        'normal': '< 2.0 U/L',
        'category': 'tumor'
    },
    'ctdna': {
        'name': 'ctDNA Fraction (Circulating Tumor DNA)',
        'unit': '%',
        'normal': '< 0.5%',
        'category': 'tumor'
    },
    'esr1_protein': {
        'name': 'ESR1 Protein (Estrogen Receptor Alpha)',
        'unit': 'ng/mL',
        'normal': '< 6.0 ng/mL',
        'category': 'tumor'
    }
}

# Immune Function Markers (12)
IMMUNE_MARKERS = {
    'cd8': {
        'name': 'CD8+ T cells (Cytotoxic T Lymphocytes)',
        'unit': 'cells/μL',
        'normal': '600-1200 cells/μL',
        'category': 'immune'
    },
    'cd4': {
        'name': 'CD4+ T cells (Helper T Lymphocytes)',
        'unit': 'cells/μL',
        'normal': '800-1600 cells/μL',
        'category': 'immune'
    },
    'nk': {
        'name': 'NK cells (Natural Killer cells)',
        'unit': 'cells/μL',
        'normal': '200-400 cells/μL',
        'category': 'immune'
    },
    'ifn_gamma': {
        'name': 'IFN-γ (Interferon-gamma)',
        'unit': 'pg/mL',
        'normal': '2.0-8.0 pg/mL',
        'category': 'immune'
    },
    'il10': {
        'name': 'IL-10 (Interleukin-10)',
        'unit': 'pg/mL',
        'normal': '< 10 pg/mL',
        'category': 'immune'
    },
    'tnf_alpha': {
        'name': 'TNF-α (Tumor Necrosis Factor-alpha)',
        'unit': 'pg/mL',
        'normal': '< 8.1 pg/mL',
        'category': 'immune'
    },
    'tgf_beta': {
        'name': 'TGF-β (Transforming Growth Factor-beta)',
        'unit': 'ng/mL',
        'normal': '< 2.5 ng/mL',
        'category': 'immune'
    },
    'pdl1_ctc': {
        'name': 'PD-L1 CTC (Programmed Death-Ligand 1 on CTC)',
        'unit': '% positive',
        'normal': '< 1%',
        'category': 'immune'
    },
    'hla_dr': {
        'name': 'HLA-DR (Human Leukocyte Antigen-DR)',
        'unit': '% positive',
        'normal': '70-90%',
        'category': 'immune'
    },
    'ctc': {
        'name': 'CTC (Circulating Tumor Cells)',
        'unit': 'cells/7.5mL',
        'normal': '< 5 cells/7.5mL',
        'category': 'immune'
    },
    'ang2': {
        'name': 'Ang-2 (Angiopoietin-2)',
        'unit': 'pg/mL',
        'normal': '1000-3000 pg/mL',
        'category': 'immune'
    },
    'lymphocytes': {
        'name': 'Total Lymphocyte Count',
        'unit': 'cells/μL',
        'normal': '1200-4000 cells/μL',
        'category': 'immune'
    }
}

# Resistance Markers (16)
RESISTANCE_MARKERS = {
    'esr1_mutations': {
        'name': 'ESR1 Mutations (Estrogen Receptor Alpha)',
        'unit': 'score',
        'normal': '0 (wild-type)',
        'category': 'resistance'
    },
    'pgr': {
        'name': 'PGR Protein (Progesterone Receptor)',
        'unit': 'ng/mL',
        'normal': '< 20 ng/mL',
        'category': 'resistance'
    },
    'brca': {
        'name': 'BRCA Mutations (BRCA1/BRCA2)',
        'unit': 'score',
        'normal': '0 (wild-type)',
        'category': 'resistance'
    },
    'pik3ca': {
        'name': 'PIK3CA Mutations (Phosphatidylinositol-4,5-bisphosphate 3-kinase)',
        'unit': 'score',
        'normal': '0 (wild-type)',
        'category': 'resistance'
    },
    'tp53': {
        'name': 'TP53 Mutations (Tumor Protein p53)',
        'unit': 'score',
        'normal': '0 (wild-type)',
        'category': 'resistance'
    },
    'her2_mutations': {
        'name': 'HER2 Mutations (Human Epidermal Growth Factor Receptor 2)',
        'unit': 'score',
        'normal': '0 (wild-type)',
        'category': 'resistance'
    },
    'her2_circ': {
        'name': 'HER2 Circular (HER2 Circular RNA)',
        'unit': 'score',
        'normal': '< 5.0',
        'category': 'resistance'
    },
    'mdr1': {
        'name': 'MDR1 Expression (Multidrug Resistance Protein 1 / ABCB1)',
        'unit': 'units',
        'normal': '100-200 units',
        'category': 'resistance'
    },
    'cyp2d6': {
        'name': 'CYP2D6 Activity (Cytochrome P450 2D6)',
        'unit': '0-3',
        'normal': '1.5-2.5',
        'category': 'resistance'
    },
    'survivin': {
        'name': 'Survivin (BIRC5)',
        'unit': 'ng/mL',
        'normal': '< 0.5 ng/mL',
        'category': 'resistance'
    },
    'hsp': {
        'name': 'Heat Shock Proteins (HSP70/HSP90)',
        'unit': 'ng/mL',
        'normal': '5-15 ng/mL',
        'category': 'resistance'
    },
    'mir200': {
        'name': 'miR-200 (microRNA-200)',
        'unit': 'fold',
        'normal': '0.5-1.5 fold',
        'category': 'resistance'
    },
    'exosomes': {
        'name': 'Exosomes (Tumor-Derived Exosomes)',
        'unit': 'particles/mL',
        'normal': '5-15 × 10⁹ particles/mL',
        'category': 'resistance'
    },
    'vegf': {
        'name': 'VEGF (Vascular Endothelial Growth Factor)',
        'unit': 'pg/mL',
        'normal': '100-400 pg/mL',
        'category': 'resistance'
    },
    'mrp1': {
        'name': 'MRP1 (Multidrug Resistance-Associated Protein 1 / ABCC1)',
        'unit': 'units',
        'normal': 'Normal range',
        'category': 'resistance'
    },
    'ki67': {
        'name': 'Ki-67 (Proliferation Marker)',
        'unit': '%',
        'normal': '< 15%',
        'category': 'resistance'
    }
}

# Metabolic Markers (8)
METABOLIC_MARKERS = {
    'glucose': {
        'name': 'Glucose (Blood Glucose)',
        'unit': 'mg/dL',
        'normal': '70-140 mg/dL',
        'category': 'metabolic'
    },
    'lactate': {
        'name': 'Lactate (Lactic Acid)',
        'unit': 'mmol/L',
        'normal': '< 2.2 mmol/L',
        'category': 'metabolic'
    },
    'ldh': {
        'name': 'LDH (Lactate Dehydrogenase)',
        'unit': 'U/L',
        'normal': '< 250 U/L',
        'category': 'metabolic'
    },
    'albumin': {
        'name': 'Albumin (Serum Albumin)',
        'unit': 'g/dL',
        'normal': '3.5-5.0 g/dL',
        'category': 'metabolic'
    },
    'beta_hydroxybutyrate': {
        'name': 'Beta-hydroxybutyrate (β-HB)',
        'unit': 'mmol/L',
        'normal': '< 0.5 mmol/L',
        'category': 'metabolic'
    },
    'blood_ph': {
        'name': 'Blood pH (Arterial pH)',
        'unit': 'pH',
        'normal': '7.35-7.45',
        'category': 'metabolic'
    },
    'folate': {
        'name': 'Folate (Folic Acid)',
        'unit': 'ng/mL',
        'normal': '5-15 ng/mL',
        'category': 'metabolic'
    },
    'vitamin_d': {
        'name': 'Vitamin D (25-Hydroxyvitamin D)',
        'unit': 'ng/mL',
        'normal': '> 30 ng/mL',
        'category': 'metabolic'
    }
}

# Organ Function Markers (5)
ORGAN_MARKERS = {
    'creatinine': {
        'name': 'Creatinine (Serum Creatinine)',
        'unit': 'mg/dL',
        'normal': '0.6-1.3 mg/dL',
        'category': 'organ'
    },
    'bun': {
        'name': 'BUN (Blood Urea Nitrogen)',
        'unit': 'mg/dL',
        'normal': '6-24 mg/dL',
        'category': 'organ'
    },
    'alt': {
        'name': 'ALT (Alanine Aminotransferase)',
        'unit': 'U/L',
        'normal': '5-40 U/L',
        'category': 'organ'
    },
    'ast': {
        'name': 'AST (Aspartate Aminotransferase)',
        'unit': 'U/L',
        'normal': '8-45 U/L',
        'category': 'organ'
    },
    'bilirubin': {
        'name': 'Bilirubin (Total Bilirubin)',
        'unit': 'mg/dL',
        'normal': '0.2-1.5 mg/dL',
        'category': 'organ'
    }
}

# Combine all biomarkers
ALL_BIOMARKERS = {
    **TUMOR_MARKERS,
    **IMMUNE_MARKERS,
    **RESISTANCE_MARKERS,
    **METABOLIC_MARKERS,
    **ORGAN_MARKERS
}

# Verify count
TOTAL_BIOMARKERS = len(ALL_BIOMARKERS)
assert TOTAL_BIOMARKERS == 47, f"Expected 47 biomarkers, found {TOTAL_BIOMARKERS}"

# Category counts
CATEGORY_COUNTS = {
    'tumor': len(TUMOR_MARKERS),
    'immune': len(IMMUNE_MARKERS),
    'resistance': len(RESISTANCE_MARKERS),
    'metabolic': len(METABOLIC_MARKERS),
    'organ': len(ORGAN_MARKERS)
}

