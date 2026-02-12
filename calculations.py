"""
Calculation Module for all 37 parameters.

Core panel: when only 15 biomarkers are provided, missing biomarkers are imputed
to reference (normal) values.
"""

import numpy as np
from biomarkers_data import ALL_BIOMARKERS

# Core panel (15 biomarkers): ca153, cd8, pik3ca, albumin, cea, cd4, esr1_protein, il10,
# glucose, her2_mutations, tk1, nk, lactate, mdr1, ifn_gamma.
# Mapping of each parameter to Core-panel relevance (formula inputs from Core vs imputed):
# - "core_driven": main formula inputs come from Core biomarkers.
# - "partly_core": some inputs from Core, some imputed.
# - "imputed_only": all formula inputs are from imputed biomarkers (e.g. organs, VEGF, f_metastatic).
CORE_PANEL_PARAMETER_COVERAGE = {
    'lambda1': 'core_driven',   # s_prolif: tk1, glucose, lactate (3/4 Core)
    'lambda2': 'partly_core',   # lambda1 + f_resist1 (pik3ca Core)
    'lambdaR1': 'partly_core',  # lambda1 + f_resist1
    'lambdaR2': 'partly_core',  # lambda1 + f_resist2 (her2_mutations, mdr1 Core)
    'K': 'partly_core',         # s_tumor (ca153, cea Core)
    'beta1': 'core_driven',    # s_immune (all 4 Core), s_suppress (il10 Core)
    'beta2': 'partly_core',    # s_suppress (il10 Core)
    'phi1': 'core_driven',     # s_activation (ifn_gamma, cd4 Core)
    'phi2': 'partly_core',     # s_tumor (ca153, cea Core)
    'phi3': 'core_driven',     # il10 (Core)
    'deltaI': 'core_driven',   # s_stress (glucose, lactate Core)
    'omegaR1': 'partly_core',  # s_genetic (pik3ca), s_stress (glucose, lactate)
    'omegaR2': 'partly_core',
    'etaE': 'partly_core',     # esr1_protein (Core); esr1_mutations, organs imputed
    'etaC': 'partly_core',     # albumin, glucose (Core); organs imputed
    'etaH': 'partly_core',     # her2_mutations (Core); her2_circ, organs imputed
    'etaI': 'core_driven',     # cd8, cd4, ifn_gamma, il10, albumin, glucose (Core); pdl1 imputed
    'kel': 'imputed_only',     # organs only (creatinine, bun, alt, ast, bilirubin)
    'k_metabolism': 'imputed_only',
    'k_clearance': 'imputed_only',
    'alphaA': 'imputed_only',  # VEGF, Ang-2
    'deltaA': 'imputed_only',  # organs
    'kappaQ': 'core_driven',   # s_quiescence (glucose, lactate Core)
    'lambdaQ': 'core_driven',
    'kappaS': 'core_driven',   # s_stress (glucose, lactate Core)
    'deltaS': 'core_driven',   # s_immune (all Core)
    'gamma': 'imputed_only',   # f_metastatic (CTC, miR-200, exosomes)
    'deltaP': 'core_driven',   # s_immune (Core)
    'mu': 'partly_core',       # s_genetic (pik3ca), s_stress
    'nu': 'partly_core',
    'deltaG': 'partly_core',   # G (pik3ca), BRCA imputed
    'kappaM': 'partly_core',   # s_metabolic (glucose, lactate Core)
    'deltaM': 'partly_core',
    'kappaH': 'partly_core',   # s_tumor (ca153, cea Core)
    'deltaH': 'imputed_only',  # organs
    'rho1': 'core_driven',     # s_immune (Core)
    'rho2': 'partly_core',     # f_resist2 (her2_mutations, mdr1 Core)
    'G': 'partly_core',        # pik3ca (Core); ctDNA, TP53 imputed
}

# Reference values for imputation when using Core (or Optimized) panel.
# Missing biomarkers are set to these mid-normal / formula-safe values so that
# composite scores and organ functions are defined and stable (no division by zero,
# no degenerate extremes). Values align with Chapter 4 formula denominators and
# clinical normal ranges from biomarkers_data.
REFERENCE_VALUES_FOR_IMPUTATION = {
    'ca153': 15.65, 'ca2729': 19.0, 'cea': 1.5, 'tk1': 1.0, 'ctdna': 0.25, 'esr1_protein': 3.0,
    'cd8': 700.0, 'cd4': 1050.0, 'nk': 345.0, 'ifn_gamma': 2.0, 'il10': 2.5, 'tnf_alpha': 4.0,
    'tgf_beta': 2.5, 'pdl1_ctc': 0.5, 'hla_dr': 80.0, 'ctc': 2.5, 'ang2': 2000.0, 'lymphocytes': 2000.0,
    'esr1_mutations': 0.0, 'pgr': 10.0, 'brca': 0.0, 'pik3ca': 0.0, 'tp53': 0.0, 'her2_mutations': 0.0,
    'her2_circ': 2.5, 'mdr1': 75.0, 'cyp2d6': 1.5, 'survivin': 0.25, 'hsp': 7.5, 'mir200': 2.5,
    'exosomes': 50.0, 'vegf': 200.0, 'mrp1': 50.0, 'ki67': 15.0,
    'glucose': 95.0, 'lactate': 1.1, 'ldh': 125.0, 'albumin': 4.0, 'beta_hydroxybutyrate': 0.25,
    'blood_ph': 7.4, 'folate': 10.0, 'vitamin_d': 40.0,
    'creatinine': 1.0, 'bun': 15.0, 'alt': 25.0, 'ast': 25.0, 'bilirubin': 1.0,
}


def get_biomarkers_for_calculation(biomarkers, core_markers=None):
    """
    Return the biomarker dict to use for parameter calculation.

    When core_markers is provided (e.g. Core Panel 15), only those keys are taken
    from the user input; all other biomarkers are set to reference values.
    When core_markers is None (Full panel), user-provided values are used where
    present; any missing key is imputed to reference (normal) values 
    ("imputation of missing values with the median value that is specific to the
    category"). This avoids zeros that would distort composite scores and formulae.
    """
    if core_markers is None or len(core_markers) == 0:
        # Full panel: impute missing biomarkers to reference values (no zeros)
        return {
            k: biomarkers.get(k, REFERENCE_VALUES_FOR_IMPUTATION.get(k, 0.0))
            for k in ALL_BIOMARKERS
        }
    # Core (or Optimized) panel: only core keys from user; rest to reference
    return {
        k: biomarkers.get(k, REFERENCE_VALUES_FOR_IMPUTATION.get(k, 0.0))
        for k in ALL_BIOMARKERS
    }


def calculate_composite_scores(biomarkers):
    """
    Calculate all composite scores 
    Returns dictionary of all composite scores
    """
    scores = {}
    
    # Tumor burden score: s_tumor = (1/5) × (CA15-3/31.3 + CA27-29/38 + CEA/3.0 + CTC/5 + ctDNA/1.0)
    scores['s_tumor'] = (1/5) * (
        biomarkers['ca153'] / 31.3 +
        biomarkers['ca2729'] / 38 +
        biomarkers['cea'] / 3.0 +
        biomarkers['ctc'] / 5 +
        biomarkers['ctdna'] / 1.0
    )
    
    # Proliferation score: s_prolif = (1/4) × (TK1/2.0 + Glucose/95 + Lactate/2.2 + Survivin/0.5)
    scores['s_prolif'] = (1/4) * (
        biomarkers['tk1'] / 2.0 +
        biomarkers['glucose'] / 95 +
        biomarkers['lactate'] / 2.2 +
        biomarkers['survivin'] / 0.5
    )
    
    # Immune strength score: s_immune = 0.4×(CD8/700) + 0.3×(CD4/1050) + 0.2×(NK/345) + 0.1×(IFN-γ/2.0)
    scores['s_immune'] = (
        0.4 * (biomarkers['cd8'] / 700) +
        0.3 * (biomarkers['cd4'] / 1050) +
        0.2 * (biomarkers['nk'] / 345) +
        0.1 * (biomarkers['ifn_gamma'] / 2.0)
    )
    
    # Immunosuppression score: s_suppress = (1/3) × (IL-10/5.0 + TGF-β/2.5 + PD-L1/1.0)
    scores['s_suppress'] = (1/3) * (
        biomarkers['il10'] / 5.0 +
        biomarkers['tgf_beta'] / 2.5 +
        biomarkers['pdl1_ctc'] / 1.0
    )
    
    # Genetic stability score: G = max(0.1, min(1.0, 1 - 0.3×(ctDNA/1.0) - 0.2×(PIK3CA/10) - 0.2×(TP53/10)))
    scores['G'] = max(0.1, min(1.0, 
        1 - 0.3 * (biomarkers['ctdna'] / 1.0) - 
        0.2 * (biomarkers['pik3ca'] / 10) - 
        0.2 * (biomarkers['tp53'] / 10)
    ))
    
    # Genetic score: s_genetic = (1/3) × (ctDNA/1.0 + PIK3CA/10 + TP53/10)
    scores['s_genetic'] = (1/3) * (
        biomarkers['ctdna'] / 1.0 +
        biomarkers['pik3ca'] / 10 +
        biomarkers['tp53'] / 10
    )
    
    # Metabolic stress score: s_metabolic = (1/3) × (Glucose/95 + Lactate/2.2 + LDH/250)
    scores['s_metabolic'] = (1/3) * (
        biomarkers['glucose'] / 95 +
        biomarkers['lactate'] / 2.2 +
        biomarkers['ldh'] / 250
    )
    
    # Stress score (Chapter 4 uses s_stress but doesn't define separately - using s_metabolic)
    scores['s_stress'] = scores['s_metabolic']
    
    # Activation score: s_activation = (1/2)×(IFN-γ/5 + CD4/1200) per Chapter 4.
    # 47-panel does not include IL-2; uses IFN-γ and CD4 with equal weighting.
    scores['s_activation'] = (1/2) * (
        biomarkers['ifn_gamma'] / 5 +
        biomarkers['cd4'] / 1200
    )
    
    # Resistance factor 1: f_resist1 = max(0.1, min(2.0, (1/4)×(ESR1_mut/8 + PGR/20 + PIK3CA/5 + Survivin/6)))
    scores['f_resist1'] = max(0.1, min(2.0, (1/4) * (
        biomarkers['esr1_mutations'] / 8 +
        biomarkers['pgr'] / 20 +
        biomarkers['pik3ca'] / 5 +
        biomarkers['survivin'] / 6
    )))
    
    # Resistance factor 2: f_resist2 = max(0.1, min(2.0, (1/4)×(HER2_mut/10 + MDR1/150 + Survivin/6 + HSP/10)))
    scores['f_resist2'] = max(0.1, min(2.0, (1/4) * (
        biomarkers['her2_mutations'] / 10 +
        biomarkers['mdr1'] / 150 +
        biomarkers['survivin'] / 6 +
        biomarkers['hsp'] / 10
    )))
    
    # Quiescence score: s_quiescence = (1/2)×(max(0,(100-Glucose)/100) + min(1, Lactate/4)) per Chapter 4
    nutrient_stress = max(0, (100 - biomarkers['glucose']) / 100)
    metabolic_stress = min(1.0, biomarkers['lactate'] / 4.0)
    scores['s_quiescence'] = (nutrient_stress + metabolic_stress) / 2
    
    # Metastatic factor: f_metastatic = (1/3) × (CTC/20 + f_EMT + Exosomes/100)
    # where f_EMT = max(0, (5 - miR-200)/5)
    f_emt = max(0, (5 - biomarkers['mir200']) / 5)
    scores['f_metastatic'] = (1/3) * (
        biomarkers['ctc'] / 20 +
        f_emt +
        biomarkers['exosomes'] / 100
    )
    
    return scores

def calculate_organ_functions(biomarkers):
    """
    Calculate liver and kidney function factors
    """
    # Liver function: f_liver = (1/3) × (ALT_factor + AST_factor + Bilirubin_factor)
    alt_factor = max(0.2, min(1.2, 40 / max(biomarkers['alt'], 5)))
    ast_factor = max(0.2, min(1.2, 45 / max(biomarkers['ast'], 8)))
    bilirubin_factor = max(0.5, min(1.5, 1.2 / max(biomarkers['bilirubin'], 0.1)))
    f_liver = (alt_factor + ast_factor + bilirubin_factor) / 3
    
    # Kidney function: f_kidney = (1/2) × (Creatinine_factor + BUN_factor)
    creatinine_factor = max(0.3, min(1.3, 1.2 / max(biomarkers['creatinine'], 0.5)))
    bun_factor = max(0.3, min(1.3, 20 / max(biomarkers['bun'], 5)))
    f_kidney = (creatinine_factor + bun_factor) / 2
    
    return {
        'f_liver': f_liver,
        'f_kidney': f_kidney,
        'f_clearance': f_liver * f_kidney
    }

def calculate_all_parameters(biomarkers, core_markers=None):
    """
    Calculate all 37 parameters formulas.

    When core_markers is provided (Core Panel), only those biomarkers are taken
    from the user; all others are imputed to reference values so formulas remain
    well-defined and stable (see get_biomarkers_for_calculation).

    Returns:
        dict with 'parameters', 'scores', 'organs', 'constraint_violations',
        and optionally 'imputed_core_panel': True when Core panel imputation was used.
    """
    biomarkers_use = get_biomarkers_for_calculation(biomarkers, core_markers)
    imputed = core_markers is not None and len(core_markers) > 0

    # Get composite scores (from full 47, with imputed values when Core panel)
    scores = calculate_composite_scores(biomarkers_use)

    # Get organ functions
    organs = calculate_organ_functions(biomarkers_use)
    
    parameters = {}
    # Expose selected composite scores (e.g., G) alongside parameters for downstream interpretation
    parameters['G'] = scores['G']
    
    # Growth Parameters
    # λ₁ = max(0.01, min(0.15, 0.04 × (1 + 1.5 × s_prolif)))
    parameters['lambda1'] = max(0.01, min(0.15, 0.04 * (1 + 1.5 * scores['s_prolif'])))
    
    # λ₂ = max(0.005, min(0.1, 0.6 × λ₁ × (1 + 0.5 × f_resist1)))
    parameters['lambda2'] = max(0.005, min(0.1, 0.6 * parameters['lambda1'] * (1 + 0.5 * scores['f_resist1'])))
    
    # λ_R1 = max(0.003, min(0.05, 0.4 × λ₁ × f_resist1))
    parameters['lambdaR1'] = max(0.003, min(0.05, 0.4 * parameters['lambda1'] * scores['f_resist1']))
    
    # λ_R2 = max(0.001, min(0.03, 0.25 × λ₁ × (1 - 0.3 × f_resist2)))
    parameters['lambdaR2'] = max(0.001, min(0.03, 0.25 * parameters['lambda1'] * (1 - 0.3 * scores['f_resist2'])))
    
    # K = max(100, min(15000, s_tumor × 2000))
    parameters['K'] = max(100, min(15000, scores['s_tumor'] * 2000))
    
    # Immune Parameters
    # β₁ = max(0.001, min(0.1, 0.02 × s_immune × (1 - s_suppress)))
    parameters['beta1'] = max(0.001, min(0.1, 0.02 * scores['s_immune'] * (1 - scores['s_suppress'])))
    
    # β₂ = max(0.01, min(0.5, 0.05 + 0.15 × s_suppress))
    parameters['beta2'] = max(0.01, min(0.5, 0.05 + 0.15 * scores['s_suppress']))
    
    # φ₁ = max(0.01, min(0.2, 0.05 + 0.1 × s_activation))
    parameters['phi1'] = max(0.01, min(0.2, 0.05 + 0.1 * scores['s_activation']))
    
    # φ₂ = max(0.005, min(0.1, 0.01 + 0.03 × (s_tumor/2)))
    parameters['phi2'] = max(0.005, min(0.1, 0.01 + 0.03 * (scores['s_tumor'] / 2)))
    
    # φ₃ = max(0.005, min(0.15, 0.02 + 0.08 × (IL-10/15)))
    parameters['phi3'] = max(0.005, min(0.15, 0.02 + 0.08 * (biomarkers_use['il10'] / 15)))
    
    # δ_I = max(0.02, min(0.3, 0.05 + 0.1 × s_stress))
    parameters['deltaI'] = max(0.02, min(0.3, 0.05 + 0.1 * scores['s_stress']))
    
    # Resistance Evolution Parameters
    # ω_R1 = max(0.0001, min(0.01, 0.002 × s_genetic × s_stress))
    parameters['omegaR1'] = max(0.0001, min(0.01, 0.002 * scores['s_genetic'] * scores['s_stress']))
    
    # ω_R2 = max(0.0001, min(0.008, 0.001 × s_genetic × s_stress))
    parameters['omegaR2'] = max(0.0001, min(0.008, 0.001 * scores['s_genetic'] * scores['s_stress']))
    
    # Treatment Effectiveness Parameters (use biomarkers_use for consistency with imputation)
    # Chapter 4 validation: 0.1 ≤ η_i ≤ 0.95 (we use 0.95 as upper bound in formulas).
    eta_lo, eta_hi = 0.1, 0.95

    # f_general = (1/2)×(Albumin/4.0 + max(0.5, 1 - 0.3×|95-Glucose|/95)) per Chapter 4 (η_C, η_I; also used in η_E f_metabolism)
    albumin_component = biomarkers_use['albumin'] / 4.0
    glucose_component = max(0.5, 1 - 0.3 * abs(95 - biomarkers_use['glucose']) / 95)
    f_general = (albumin_component + glucose_component) / 2
    f_organs = (organs['f_liver'] + organs['f_kidney']) / 2

    # η_E = max(0.1, min(0.95, f_receptor × f_metabolism × f_resist_hormone))
    # f_metabolism = (1/3)(f_liver + f_CYP2D6 + f_general). Chapter 4 does not define f_CYP2D6; we use min(1, CYP2D6/2) (activity 0–2 scale, normal ~1–2).
    f_receptor = min(1.0, biomarkers_use['esr1_protein'] / 6.0)
    f_CYP2D6 = min(1.0, biomarkers_use['cyp2d6'] / 2.0)
    f_metabolism = (organs['f_liver'] + f_CYP2D6 + f_general) / 3
    resistance_component = 0.6 * (biomarkers_use['esr1_mutations'] / 8) + 0.4 * scores['s_genetic']
    f_resist_hormone = 1 - min(0.9, resistance_component)
    parameters['etaE'] = max(eta_lo, min(eta_hi, f_receptor * f_metabolism * f_resist_hormone))

    # η_C = max(0.1, min(0.95, f_general × f_organs × (1 - 0.7 × f_resist2)))
    parameters['etaC'] = max(eta_lo, min(eta_hi, f_general * f_organs * (1 - 0.7 * scores['f_resist2'])))

    # η_H = max(0.1, min(0.95, f_HER2 × f_organs × (1 - 0.5 × f_resist2)))
    her2_circ_component = min(1.0, biomarkers_use['her2_circ'] / 5.0)
    her2_mut_penalty = 1 - 0.6 * (biomarkers_use['her2_mutations'] / 10)
    f_HER2 = her2_circ_component * her2_mut_penalty
    parameters['etaH'] = max(eta_lo, min(eta_hi, f_HER2 * f_organs * (1 - 0.5 * scores['f_resist2'])))

    # η_I = max(0.1, min(0.95, f_PDL1 × f_immune_ctx × f_general))
    # f_immune_ctx = (1/4)(CD8/700 + CD4/1050 + IFN-γ/2.0 + (1 − IL-10/15)); clamp (1 − IL-10/15) ≥ 0 to avoid negative contribution
    f_PDL1 = min(1.0, biomarkers_use['pdl1_ctc'] / 3.0)
    cd8_component = biomarkers_use['cd8'] / 700
    cd4_component = biomarkers_use['cd4'] / 1050
    ifn_component = biomarkers_use['ifn_gamma'] / 2.0
    il10_component = max(0.0, 1.0 - biomarkers_use['il10'] / 15)
    f_immune_ctx = (cd8_component + cd4_component + ifn_component + il10_component) / 4
    parameters['etaI'] = max(eta_lo, min(eta_hi, f_PDL1 * f_immune_ctx * f_general))
    
    # Pharmacokinetic Parameters
    # k_el = max(0.05, min(0.3, 0.1 / f_clearance))
    parameters['kel'] = max(0.05, min(0.3, 0.1 / organs['f_clearance']))
    
    # k_metabolism = max(0.02, min(0.2, 0.05 × f_liver))
    parameters['k_metabolism'] = max(0.02, min(0.2, 0.05 * organs['f_liver']))
    
    # k_clearance = max(0.1, min(0.5, 0.2 × f_clearance))
    parameters['k_clearance'] = max(0.1, min(0.5, 0.2 * organs['f_clearance']))
    
    # Microenvironmental Parameters
    # α_A = max(0.001, min(0.1, 0.02 × (1 + VEGF/400) × (1 + Ang-2/3000)))
    parameters['alphaA'] = max(0.001, min(0.1, 0.02 * (1 + biomarkers_use['vegf'] / 400) * (1 + biomarkers_use['ang2'] / 3000)))
    
    # δ_A = max(0.05, min(0.2, 0.1 × f_clearance))
    parameters['deltaA'] = max(0.05, min(0.2, 0.1 * organs['f_clearance']))
    
    # κ_Q = max(0.001, min(0.05, 0.005 + 0.02 × s_quiescence))
    parameters['kappaQ'] = max(0.001, min(0.05, 0.005 + 0.02 * scores['s_quiescence']))
    
    # λ_Q = max(0.0005, min(0.02, 0.002 + 0.01 × (1 - s_quiescence)))
    parameters['lambdaQ'] = max(0.0005, min(0.02, 0.002 + 0.01 * (1 - scores['s_quiescence'])))
    
    # κ_S = max(0.001, min(0.04, 0.002 + 0.01 × s_stress))
    parameters['kappaS'] = max(0.001, min(0.04, 0.002 + 0.01 * scores['s_stress']))
    
    # δ_S = max(0.02, min(0.1, 0.05 × s_immune))
    parameters['deltaS'] = max(0.02, min(0.1, 0.05 * scores['s_immune']))
    
    # γ = max(0.0001, min(0.01, 0.002 × f_metastatic))
    parameters['gamma'] = max(0.0001, min(0.01, 0.002 * scores['f_metastatic']))
    
    # δ_P = max(0.02, min(0.1, 0.05 + 0.03 × s_immune))
    parameters['deltaP'] = max(0.02, min(0.1, 0.05 + 0.03 * scores['s_immune']))
    
    # Genetic Instability Parameters
    # μ = max(0.001, min(0.05, 0.01 × (1 + 1.5 × s_genetic)))
    parameters['mu'] = max(0.001, min(0.05, 0.01 * (1 + 1.5 * scores['s_genetic'])))
    
    # ν (treatment-induced mutagenesis) - derived from treatment pressure and genetic instability
    # Based on Chapter 4: "Rate ν captures treatment-induced mutagenesis"
    parameters['nu'] = max(0.0001, min(0.01, 0.002 * scores['s_genetic'] * (1 + scores['s_stress'])))
    
    # δ_G (genetic stability restoration) - DNA repair capacity
    # Based on Chapter 4: "Natural DNA repair restores baseline restoration ability"
    brca_factor = 1.0 - min(0.5, biomarkers_use.get('brca', 0) / 2.0)  # BRCA mutations reduce repair
    parameters['deltaG'] = max(0.001, min(0.05, 0.01 * brca_factor * scores['G']))
    
    # Metabolic State Parameters
    # κ_M (metabolic reprogramming rate) - derived from glucose, lactate, LDH
    # Based on Chapter 4: "derived from glucose, lactate, and LDH levels"
    beta_hydroxybutyrate_factor = max(0.5, 1 - biomarkers_use.get('beta_hydroxybutyrate', 0) / 2.0)
    parameters['kappaM'] = max(0.001, min(0.1, 0.02 * scores['s_metabolic'] * beta_hydroxybutyrate_factor))
    
    # δ_M (metabolic normalization) - homeostatic clearance
    # Based on Chapter 4: "natural metabolic normalization occurs at rate δ_M"
    parameters['deltaM'] = max(0.001, min(0.05, 0.01 * (1 - 0.5 * scores['s_metabolic'])))
    
    # Hypoxia Parameters
    # κ_H (hypoxia induction rate) - occurs when tumor burden exceeds capacity
    # Based on Chapter 4: "Hypoxia develops when tumor burden exceeds vascular oxygen supply"
    parameters['kappaH'] = max(0.001, min(0.1, 0.02 * max(0, scores['s_tumor'] - 0.5)))
    
    # δ_H (hypoxia clearance) - natural oxygenation
    # Based on Chapter 4: "Natural oxygenation provides clearance process"
    parameters['deltaH'] = max(0.01, min(0.1, 0.05 * (1 + organs['f_clearance'])))
    
    # Immune Sensitivity Factors (for resistant cells)
    # ρ₁ (hormone-resistant immune sensitivity) - range [0.6, 0.9] per Chapter 4
    # Based on Chapter 4: "partial immune sensitivity with factor ρ₁ ∈ [0.6, 0.9]"
    parameters['rho1'] = max(0.6, min(0.9, 0.75 + 0.15 * scores['s_immune']))
    
    # ρ₂ (multi-drug resistant immune sensitivity) - range [0.3, 0.6] per Chapter 4
    # Based on Chapter 4: "highest resistance to immune killing with factor ρ₂ ∈ [0.3, 0.6]"
    parameters['rho2'] = max(0.3, min(0.6, 0.45 - 0.15 * scores['f_resist2']))

    # α_acid (acidosis modulation in N₁, N₂ ODEs): Chapter 4 uses (1+0.1M)/(1+α_acid M); "pH effects (α_acid) modulate logistic growth";
    # "acidotic states partially counteract". Not one of the 37 parameters; derived from blood pH for ODE completeness.
    # Normal pH 7.35–7.45; acidosis < 7.35. α_acid increases as pH drops so growth is reduced in acidotic microenvironment.
    ph_deviation = max(0.0, 7.4 - biomarkers_use['blood_ph'])
    parameters['alpha_acid'] = max(0.01, min(0.5, 2.0 * ph_deviation))

    # Validate biological constraints
    constraint_violations = []
    if parameters['lambda1'] <= parameters['lambda2']:
        constraint_violations.append("λ₁ must be > λ₂")
        parameters['lambda2'] = parameters['lambda1'] * 0.99
    if parameters['lambda2'] <= parameters['lambdaR1']:
        constraint_violations.append("λ₂ must be > λ_R1")
        parameters['lambdaR1'] = parameters['lambda2'] * 0.99
    if parameters['lambdaR1'] <= parameters['lambdaR2']:
        constraint_violations.append("λ_R1 must be > λ_R2")
        parameters['lambdaR2'] = parameters['lambdaR1'] * 0.99
    
    out = {
        'parameters': parameters,
        'scores': scores,
        'organs': organs,
        'constraint_violations': constraint_violations
    }
    if imputed:
        out['imputed_core_panel'] = True
        out['parameter_coverage'] = dict(CORE_PANEL_PARAMETER_COVERAGE)  # core_driven / partly_core / imputed_only
    return out


def assess_mathematical_stability(parameters):
    """
    Assess approximate mathematical stability of the model for a given parameter set.

    This is a heuristic summary based on growth, immune, and carrying capacity relationships,
    inspired by the 15-dimensional ODE stability analysis (46.7% stability in synthetic cohort).

    Returns:
        (stability_status, message)
        stability_status: 'STABLE', 'MARGINAL', or 'UNSTABLE'
        message: human-readable summary
    """
    lambda1 = parameters['lambda1']
    lambda2 = parameters['lambda2']
    beta1 = parameters['beta1']
    phi1 = parameters['phi1']
    K = parameters['K']

    # Simple heuristic checks
    growth_stability = lambda1 > lambda2  # sensitive growth > partially resistant growth
    immune_stability = beta1 * 1000 > lambda1  # effective immune killing vs growth
    capacity_stability = K > 1000  # carrying capacity above minimal threshold

    stability_score = sum([growth_stability, immune_stability, capacity_stability]) / 3

    if stability_score >= 0.67:
        return "STABLE", "✅ Mathematical stability confirmed - reliable predictions expected"
    elif stability_score >= 0.33:
        return "MARGINAL", "⚠️ Marginal stability - monitor predictions carefully"
    else:
        return "UNSTABLE", "❌ Mathematical instability - recommend frequent monitoring"

