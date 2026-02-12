"""
Results Display Module
Handles display of calculated parameters and results
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from calculations import assess_mathematical_stability
from calculations import calculate_composite_scores

def display_results(calc_results, biomarkers, progress):
    """
    Display all calculated parameters and results
    """
    parameters = calc_results['parameters']
    scores = calc_results['scores']
    organs = calc_results['organs']
    violations = calc_results['constraint_violations']
    imputed_core = calc_results.get('imputed_core_panel', False)
    parameter_coverage = calc_results.get('parameter_coverage') or {}

    def _core_badge(key):
        """When Core panel is used, show Core-informed / Partly Core / Reference only per parameter."""
        if not imputed_core or not parameter_coverage:
            return ""
        c = parameter_coverage.get(key, "")
        if c == "core_driven":
            return " — 📗 Core-informed"
        if c == "partly_core":
            return " — 📙 Partly Core"
        if c == "imputed_only":
            return " — 📕 Reference only"
        return ""

    st.header("📊 Calculation Results")
    st.subheader("Personalized Model Parameters Derived from Blood Biomarkers")
    if imputed_core:
        st.info(
            "**Core Panel used:** Parameters were calculated from your 15 entered biomarkers. "
            "The other 32 biomarkers were imputed to reference values (per Chapter 4 preprocessing: "
            "imputation of missing values). Same Chapter 4 formulas; validation R² ≈ 0.87 for this panel (Chapter 4)."
        )
        st.caption(
            "**Parameter labels (Core panel):** 📗 Core-informed = main inputs from your 15 biomarkers. "
            "📙 Partly Core = some inputs from Core, some imputed. 📕 Reference only = all inputs imputed (consider Full panel for these)."
        )
    # Progress summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Biomarkers Entered", f"{progress['total_filled']}/{progress['total']}")
    with col2:
        st.metric("Completion", f"{progress['percentage']:.1f}%")
    with col3:
        st.metric("Model Confidence", f"{calculate_confidence(biomarkers):.1f}%")
    
    # Constraint violations warning
    if violations:
        st.warning(f"⚠️ Constraint Violations (auto-corrected): {', '.join(violations)}")
    
    # Growth Parameters
    st.subheader("🌱 Growth Parameters")
    st.caption("Click on any parameter to see its derivation formula")
    
    # Parameter formulas dictionary
    param_formulas = {
        'lambda1': {
            'name': 'λ₁ (Sensitive Cell Growth Rate)',
            'formula': r'\lambda_1 = \max(0.01, \min(0.15, 0.04 \times (1 + 1.5 \times s_{\text{prolif}})))',
            'source': 'From: TK1, Glucose, Lactate, Survivin → s_prolif',
            'value': f"{parameters['lambda1']:.6f}/mo"
        },
        'lambda2': {
            'name': 'λ₂ (Partially Resistant Growth Rate)',
            'formula': r'\lambda_2 = \max(0.005, \min(0.1, 0.6 \times \lambda_1 \times (1 + 0.5 \times f_{\text{resist1}})))',
            'source': 'From: λ₁, ESR1_mut, PGR, PIK3CA, Survivin → f_resist1',
            'value': f"{parameters['lambda2']:.6f}/mo"
        },
        'lambdaR1': {
            'name': 'λ_R1 (Hormone-Resistant Growth)',
            'formula': r'\lambda_{R1} = \max(0.003, \min(0.05, 0.4 \times \lambda_1 \times f_{\text{resist1}}))',
            'source': 'From: λ₁, f_resist1',
            'value': f"{parameters['lambdaR1']:.6f}/mo"
        },
        'lambdaR2': {
            'name': 'λ_R2 (Multi-Drug Resistant Growth)',
            'formula': r'\lambda_{R2} = \max(0.001, \min(0.03, 0.25 \times \lambda_1 \times (1 - 0.3 \times f_{\text{resist2}})))',
            'source': 'From: λ₁, HER2_mut, MDR1, Survivin, HSP → f_resist2',
            'value': f"{parameters['lambdaR2']:.6f}/mo"
        },
        'K': {
            'name': 'K (Carrying Capacity)',
            'formula': r'K = \max(100, \min(15000, s_{\text{tumor}} \times 2000))',
            'source': 'From: CA 15-3, CA 27-29, CEA, CTC, ctDNA → s_tumor',
            'value': f"{int(parameters['K'])} cells"
        }
    }
    
    for key, info in param_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])
    
    # Immune Parameters
    st.subheader("🛡️ Immune Parameters")
    st.caption("Click on any parameter to see its derivation formula")
    
    immune_formulas = {
        'beta1': {
            'name': 'β₁ (Cytotoxic Immune Killing Rate)',
            'formula': r'\beta_1 = \max(0.001, \min(0.1, 0.02 \times s_{\text{immune}} \times (1 - s_{\text{suppress}})))',
            'source': 'From: CD8, CD4, NK, IFN-γ → s_immune; IL-10, TGF-β, PD-L1 → s_suppress',
            'value': f"{parameters['beta1']:.6f}/mo"
        },
        'beta2': {
            'name': 'β₂ (Regulatory Suppression Rate)',
            'formula': r'\beta_2 = \max(0.01, \min(0.5, 0.05 + 0.15 \times s_{\text{suppress}}))',
            'source': 'From: IL-10, TGF-β, PD-L1 → s_suppress',
            'value': f"{parameters['beta2']:.6f}/mo"
        },
        'phi1': {
            'name': 'φ₁ (Basal Cytotoxic Production)',
            'formula': r'\phi_1 = \max(0.01, \min(0.2, 0.05 + 0.1 \times s_{\text{activation}}))',
            'source': 'From: IFN-γ, CD4 → s_activation (Chapter 4)',
            'value': f"{parameters['phi1']:.6f}/mo"
        },
        'phi2': {
            'name': 'φ₂ (Tumor-Induced Recruitment)',
            'formula': r'\phi_2 = \max(0.005, \min(0.1, 0.01 + 0.03 \times \frac{s_{\text{tumor}}}{2}))',
            'source': 'From: s_tumor',
            'value': f"{parameters['phi2']:.6f}/mo"
        },
        'phi3': {
            'name': 'φ₃ (Regulatory Cell Recruitment)',
            'formula': r'\phi_3 = \max(0.005, \min(0.15, 0.02 + 0.08 \times \frac{\text{IL-10}}{15}))',
            'source': 'From: IL-10 directly',
            'value': f"{parameters['phi3']:.6f}/mo"
        },
        'deltaI': {
            'name': 'δ_I (Immune Cell Death Rate)',
            'formula': r'\delta_I = \max(0.02, \min(0.3, 0.05 + 0.1 \times s_{\text{stress}}))',
            'source': 'From: Glucose, Lactate, LDH → s_metabolic = s_stress',
            'value': f"{parameters['deltaI']:.6f}/mo"
        }
    }
    
    for key, info in immune_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])
    
    # Resistance Parameters
    st.subheader("🔄 Resistance Evolution")
    st.caption("Click on any parameter to see its derivation formula")
    
    resistance_formulas = {
        'omegaR1': {
            'name': 'ω_R1 (Hormone Resistance Evolution)',
            'formula': r'\omega_{R1} = \max(0.0001, \min(0.01, 0.002 \times s_{\text{genetic}} \times s_{\text{stress}}))',
            'source': 'From: ctDNA, PIK3CA, TP53 → s_genetic; s_metabolic → s_stress',
            'value': f"{parameters['omegaR1']:.7f}/mo"
        },
        'omegaR2': {
            'name': 'ω_R2 (Multi-Drug Resistance Evolution)',
            'formula': r'\omega_{R2} = \max(0.0001, \min(0.008, 0.001 \times s_{\text{genetic}} \times s_{\text{stress}}))',
            'source': 'From: s_genetic, s_stress',
            'value': f"{parameters['omegaR2']:.7f}/mo"
        },
        'mu': {
            'name': 'μ (Mutation Accumulation)',
            'formula': r'\mu = \max(0.001, \min(0.05, 0.01 \times (1 + 1.5 \times s_{\text{genetic}})))',
            'source': 'From: ctDNA, PIK3CA, TP53 → s_genetic',
            'value': f"{parameters['mu']:.6f}/mo"
        }
    }
    
    for key, info in resistance_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])
    
    # Treatment Effectiveness
    st.subheader("💊 Treatment Effectiveness")
    st.caption("Click on any parameter to see its derivation formula")
    
    treatment_formulas = {
        'etaE': {
            'name': 'η_E (Hormone Therapy Effectiveness)',
            'formula': r'\eta_E = \max(0.1, \min(0.95, f_{\text{receptor}} \times f_{\text{metabolism}} \times f_{\text{resist\_hormone}}))',
            'sub_formulas': [
                r'f_{\text{receptor}} = \min\left(1.0, \frac{\text{ESR1\_protein}}{6.0}\right)',
                r'f_{\text{metabolism}} = \frac{1}{3}(f_{\text{liver}} + f_{\text{CYP2D6}} + f_{\text{general}})',
                r'f_{\text{CYP2D6}} = \min(1.0, \text{CYP2D6}/2.0)',
                r'f_{\text{general}} = \frac{1}{2}\left(\frac{\text{Albumin}}{4.0} + \max\left(0.5, 1 - 0.3 \times \frac{|95 - \text{Glucose}|}{95}\right)\right)',
                r'f_{\text{resist\_hormone}} = 1 - \min\left(0.9, 0.6 \times \frac{\text{ESR1\_mut}}{8} + 0.4 \times s_{\text{genetic}}\right)'
            ],
            'source': 'From: ESR1_protein, Liver (ALT/AST/Bilirubin), CYP2D6, Albumin, Glucose, ESR1_mut, s_genetic',
            'value': f"{parameters['etaE']*100:.1f}%"
        },
        'etaC': {
            'name': 'η_C (Chemotherapy Effectiveness)',
            'formula': r'\eta_C = \max(0.1, \min(0.95, f_{\text{general}} \times f_{\text{organs}} \times (1 - 0.7 \times f_{\text{resist2}})))',
            'sub_formulas': [
                r'f_{\text{general}} = \frac{1}{2}\left(\frac{\text{Albumin}}{4.0} + \max\left(0.5, 1 - 0.3 \times \frac{|95 - \text{Glucose}|}{95}\right)\right)',
                r'f_{\text{organs}} = \frac{1}{2}(f_{\text{liver}} + f_{\text{kidney}})'
            ],
            'source': 'From: Albumin, Glucose, Liver function, Kidney function (Creatinine/BUN), f_resist2',
            'value': f"{parameters['etaC']*100:.1f}%"
        },
        'etaH': {
            'name': 'η_H (HER2-Targeted Therapy Effectiveness)',
            'formula': r'\eta_H = \max(0.1, \min(0.95, f_{\text{HER2}} \times f_{\text{organs}} \times (1 - 0.5 \times f_{\text{resist2}})))',
            'sub_formulas': [
                r'f_{\text{HER2}} = \min\left(1.0, \frac{\text{HER2\_circ}}{5.0}\right) \times \left(1 - 0.6 \times \frac{\text{HER2\_mut}}{10}\right)'
            ],
            'source': 'From: HER2_circ, HER2_mut, f_organs, f_resist2',
            'value': f"{parameters['etaH']*100:.1f}%"
        },
        'etaI': {
            'name': 'η_I (Immunotherapy Effectiveness)',
            'formula': r'\eta_I = \max(0.1, \min(0.95, f_{\text{PDL1}} \times f_{\text{immune\_ctx}} \times f_{\text{general}}))',
            'sub_formulas': [
                r'f_{\text{PDL1}} = \min\left(1.0, \frac{\text{PD-L1\_CTC}}{3.0}\right)',
                r'f_{\text{immune\_ctx}} = \frac{1}{4}\left(\frac{\text{CD8}}{700} + \frac{\text{CD4}}{1050} + \frac{\text{IFN-}\gamma}{2.0} + \max\left(0, 1 - \frac{\text{IL-10}}{15}\right)\right)'
            ],
            'source': 'From: PD-L1_CTC, CD8, CD4, IFN-γ, IL-10, Albumin, Glucose',
            'value': f"{parameters['etaI']*100:.1f}%"
        }
    }
    
    for key, info in treatment_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            if 'sub_formulas' in info:
                st.write("**Where:**")
                for sub_formula in info['sub_formulas']:
                    st.latex(sub_formula)
            st.caption(info['source'])
    
    # Pharmacokinetic Parameters
    st.subheader("⚡ Pharmacokinetics")
    st.caption("Click on any parameter to see its derivation formula")
    
    pk_formulas = {
        'kel': {
            'name': 'k_el (Drug Elimination Rate)',
            'formula': r'k_{\text{el}} = \max\left(0.05, \min\left(0.3, \frac{0.1}{f_{\text{clearance}}}\right)\right)',
            'source': 'From: f_clearance = f_liver × f_kidney (ALT, AST, Bilirubin, Creatinine, BUN)',
            'value': f"{parameters['kel']:.6f}/mo"
        },
        'k_metabolism': {
            'name': 'k_metabolism (Drug Metabolism Rate)',
            'formula': r'k_{\text{metabolism}} = \max(0.02, \min(0.2, 0.05 \times f_{\text{liver}}))',
            'source': 'From: Liver function (ALT, AST, Bilirubin)',
            'value': f"{parameters['k_metabolism']:.6f}/mo"
        },
        'k_clearance': {
            'name': 'k_clearance (Metabolite Clearance)',
            'formula': r'k_{\text{clearance}} = \max(0.1, \min(0.5, 0.2 \times f_{\text{clearance}}))',
            'source': 'From: f_clearance (Liver × Kidney function)',
            'value': f"{parameters['k_clearance']:.6f}/mo"
        }
    }
    
    for key, info in pk_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])
    
    # Microenvironmental Parameters
    st.subheader("🌐 Microenvironment")
    st.caption("Click on any parameter to see its derivation formula")
    
    micro_formulas = {
        'alphaA': {
            'name': 'α_A (Angiogenesis Induction)',
            'formula': r'\alpha_A = \max\left(0.001, \min\left(0.1, 0.02 \times \left(1 + \frac{\text{VEGF}}{400}\right) \times \left(1 + \frac{\text{Ang-2}}{3000}\right)\right)\right)',
            'source': 'From: VEGF, Ang-2 directly',
            'value': f"{parameters['alphaA']:.6f}/mo"
        },
        'deltaA': {
            'name': 'δ_A (Angiogenesis Degradation)',
            'formula': r'\delta_A = \max(0.05, \min(0.2, 0.1 \times f_{\text{clearance}}))',
            'source': 'From: f_clearance',
            'value': f"{parameters['deltaA']:.6f}/mo"
        },
        'kappaQ': {
            'name': 'κ_Q (Quiescence Entry Rate)',
            'formula': r'\kappa_Q = \max(0.001, \min(0.05, 0.005 + 0.02 \times s_{\text{quiescence}}))',
            'source': 'From: Nutrient stress, Metabolic stress → s_quiescence',
            'value': f"{parameters['kappaQ']:.6f}/mo"
        },
        'lambdaQ': {
            'name': 'λ_Q (Quiescence Exit Rate)',
            'formula': r'\lambda_Q = \max(0.0005, \min(0.02, 0.002 + 0.01 \times (1 - s_{\text{quiescence}})))',
            'source': 'From: s_quiescence',
            'value': f"{parameters['lambdaQ']:.6f}/mo"
        },
        'kappaS': {
            'name': 'κ_S (Senescence Induction)',
            'formula': r'\kappa_S = \max(0.001, \min(0.04, 0.002 + 0.01 \times s_{\text{stress}}))',
            'source': 'From: s_metabolic = s_stress',
            'value': f"{parameters['kappaS']:.6f}/mo"
        },
        'deltaS': {
            'name': 'δ_S (Senescent Cell Clearance)',
            'formula': r'\delta_S = \max(0.02, \min(0.1, 0.05 \times s_{\text{immune}}))',
            'source': 'From: CD8, CD4, NK, IFN-γ → s_immune',
            'value': f"{parameters['deltaS']:.6f}/mo"
        },
        'gamma': {
            'name': 'γ (Metastatic Seeding Rate)',
            'formula': r'\gamma = \max(0.0001, \min(0.01, 0.002 \times f_{\text{metastatic}}))',
            'source': 'From: CTC, miR-200, Exosomes → f_metastatic',
            'value': f"{parameters['gamma']:.7f}/mo"
        },
        'deltaP': {
            'name': 'δ_P (Metastatic Clearance)',
            'formula': r'\delta_P = \max(0.02, \min(0.1, 0.05 + 0.03 \times s_{\text{immune}}))',
            'source': 'From: s_immune',
            'value': f"{parameters['deltaP']:.6f}/mo"
        }
    }
    
    for key, info in micro_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])
    
    # Genetic & Metabolic Parameters
    st.subheader("🧬 Genetic & Metabolic")
    st.caption("Click on any parameter to see its derivation formula")
    
    genetic_formulas = {
        'nu': {
            'name': 'ν (Treatment-Induced Mutagenesis)',
            'formula': r'\nu = \max(0.0001, \min(0.01, 0.002 \times s_{\text{genetic}} \times s_{\text{stress}}))',
            'source': 'From: s_genetic, s_stress',
            'value': f"{parameters['nu']:.7f}/mo"
        },
        'deltaG': {
            'name': 'δ_G (Genetic Stability Restoration)',
            'formula': r'\delta_G = \max(0.001, \min(0.05, 0.01 \times \text{BRCA\_factor} \times G))',
            'source': 'From: BRCA mutations, Genetic stability (G)',
            'value': f"{parameters['deltaG']:.6f}/mo"
        },
        'kappaM': {
            'name': 'κ_M (Metabolic Reprogramming Rate)',
            'formula': r'\kappa_M = \max(0.001, \min(0.1, 0.02 \times s_{\text{metabolic}} \times \text{ketone\_factor}))',
            'source': 'From: Glucose, Lactate, LDH → s_metabolic; Beta-hydroxybutyrate',
            'value': f"{parameters['kappaM']:.6f}/mo"
        },
        'deltaM': {
            'name': 'δ_M (Metabolic Normalization)',
            'formula': r'\delta_M = \max(0.001, \min(0.05, 0.01 \times (1 - 0.5 \times s_{\text{metabolic}})))',
            'source': 'From: s_metabolic',
            'value': f"{parameters['deltaM']:.6f}/mo"
        },
        'kappaH': {
            'name': 'κ_H (Hypoxia Induction Rate)',
            'formula': r'\kappa_H = \max(0.001, \min(0.1, 0.02 \times \max(0, s_{\text{tumor}} - 0.5)))',
            'source': 'From: s_tumor (only when > 50% capacity)',
            'value': f"{parameters['kappaH']:.6f}/mo"
        },
        'deltaH': {
            'name': 'δ_H (Hypoxia Clearance)',
            'formula': r'\delta_H = \max(0.01, \min(0.1, 0.05 \times (1 + f_{\text{clearance}})))',
            'source': 'From: f_clearance',
            'value': f"{parameters['deltaH']:.6f}/mo"
        }
    }
    
    for key, info in genetic_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])
    
    # Immune Sensitivity Factors
    st.subheader("🛡️ Resistance Immune Sensitivity")
    st.caption("Click on any parameter to see its derivation formula")
    
    immune_sens_formulas = {
        'rho1': {
            'name': 'ρ₁ (Hormone-Resistant Immune Sensitivity)',
            'formula': r'\rho_1 = \max(0.6, \min(0.9, 0.75 + 0.15 \times s_{\text{immune}}))',
            'source': 'Range [0.6, 0.9] per Chapter 4. From: s_immune',
            'value': f"{parameters['rho1']:.3f}"
        },
        'rho2': {
            'name': 'ρ₂ (Multi-Drug Resistant Immune Sensitivity)',
            'formula': r'\rho_2 = \max(0.3, \min(0.6, 0.45 - 0.15 \times f_{\text{resist2}}))',
            'source': 'Range [0.3, 0.6] per Chapter 4. From: f_resist2',
            'value': f"{parameters['rho2']:.3f}"
        }
    }
    
    for key, info in immune_sens_formulas.items():
        with st.expander(f"**{info['name']}** = {info['value']}{_core_badge(key)}", expanded=False):
            st.latex(info['formula'])
            st.caption(info['source'])

    # Supplementary parameter for ODEs (not one of the 37; used in N₁, N₂ growth term)
    if 'alpha_acid' in parameters:
        st.subheader("📐 Supplementary (ODE)")
        st.caption("Used in differential equations; derived from biomarkers for completeness.")
        with st.expander(f"**α_acid (Acidosis modulation)** = {parameters['alpha_acid']:.4f}", expanded=False):
            st.latex(r"""
            \alpha_{\text{acid}} = \max\left(0.01, \min\left(0.5, 2 \times (7.4 - \text{Blood pH})\right)\right)
            """)
            st.caption("From: Blood pH. Modulates growth in N₁, N₂ via (1+0.1M)/(1+α_acid M). Normal pH 7.35–7.45.")
    
    # Composite Scores (Expandable)
    with st.expander("📈 Composite Scores (Chapter 4)"):
        scores_data = {
            'Score': ['s_prolif', 's_immune', 's_suppress', 's_tumor', 'G (Genetic Stability)', 
                     's_genetic', 's_metabolic', 's_stress', 's_activation', 's_quiescence',
                     'f_resist1', 'f_resist2', 'f_metastatic'],
            'Value': [
                f"{scores['s_prolif']:.3f}",
                f"{scores['s_immune']:.3f}",
                f"{scores['s_suppress']:.3f}",
                f"{scores['s_tumor']:.3f}",
                f"{scores['G']:.3f}",
                f"{scores['s_genetic']:.3f}",
                f"{scores['s_metabolic']:.3f}",
                f"{scores['s_stress']:.3f}",
                f"{scores['s_activation']:.3f}",
                f"{scores['s_quiescence']:.3f}",
                f"{scores['f_resist1']:.3f}",
                f"{scores['f_resist2']:.3f}",
                f"{scores['f_metastatic']:.3f}"
            ]
        }
        st.dataframe(pd.DataFrame(scores_data), use_container_width=True, hide_index=True)
        
        st.write("**Organ Function:**")
        st.write(f"f_liver: {organs['f_liver']:.3f}, f_kidney: {organs['f_kidney']:.3f}, f_clearance: {organs['f_clearance']:.3f}")
        with st.expander("Organ function formulas"):
            st.latex(r"f_{\text{liver}} = \frac{1}{3}\left(\max\left(0.2, \min\left(1.2, \frac{40}{\max(\text{ALT}, 5)}\right)\right) + \max\left(0.2, \min\left(1.2, \frac{45}{\max(\text{AST}, 8)}\right)\right) + \max\left(0.5, \min\left(1.5, \frac{1.2}{\max(\text{Bili}, 0.1)}\right)\right)\right)")
            st.latex(r"f_{\text{kidney}} = \frac{1}{2}\left(\max\left(0.3, \min\left(1.3, \frac{1.2}{\max(\text{Creat}, 0.5)}\right)\right) + \max\left(0.3, \min\left(1.3, \frac{20}{\max(\text{BUN}, 5)}\right)\right)\right)")
            st.latex(r"f_{\text{clearance}} = f_{\text{liver}} \times f_{\text{kidney}}")
    
    # Clinical Recommendations (interpretation layer – heuristic, not part of Chapter 4 equations)
    st.subheader("🏥 Clinical Recommendations (Heuristic Interpretation Layer)")
    st.caption(
        "All parameters above are computed exactly from Chapter 4. "
        "The statements below are heuristic interpretations based on those parameters "
        "and synthetic validation data; they are not part of the original thesis text."
    )
    recommendations = generate_recommendations(parameters, biomarkers)
    for rec in recommendations:
        st.write(rec)

    # Additional clinically-oriented views
    display_stability_assessment(parameters)
    display_resistance_monitoring(parameters, biomarkers)
    display_clinical_interpretation(parameters, biomarkers)
    display_export_options(biomarkers, parameters)

def calculate_confidence(biomarkers):
    """
    Calculate model confidence based on biomarker completeness
    """
    total = len(biomarkers)
    filled = sum(1 for v in biomarkers.values() if v > 0)
    completeness = filled / total if total > 0 else 0
    
    # Key markers check
    key_markers = ['ca153', 'cea', 'cd8', 'cd4', 'albumin', 'glucose', 'lactate', 'creatinine', 'alt', 'pik3ca']
    key_filled = sum(1 for k in key_markers if k in biomarkers and biomarkers[k] > 0)
    consistency = key_filled / len(key_markers) if key_markers else 0
    
    confidence = (completeness * 0.4 + consistency * 0.6) * 100
    return min(95, max(30, confidence))

def generate_recommendations(parameters, biomarkers):
    """
    Generate clinical recommendations based on parameters
    """
    recommendations = []

    # --- Hormone therapy (η_E) ---
    if parameters['etaE'] >= 0.7:
        recommendations.append("✅ **Hormone therapy highly effective** - Consider first-line")
    elif parameters['etaE'] >= 0.4:
        recommendations.append("✅ **Hormone therapy reasonably effective**")
    else:
        recommendations.append("⚠️ **Hormone therapy low effectiveness**")

    # --- Chemotherapy (η_C) ---
    if parameters['etaC'] >= 0.65:
        recommendations.append("✅ **Good chemotherapy response predicted**")
    elif parameters['etaC'] >= 0.4:
        recommendations.append("⚖️ **Intermediate chemotherapy sensitivity**")
    else:
        recommendations.append("⚠️ **Poor chemotherapy sensitivity**")

    # --- HER2-targeted therapy (η_H) ---
    if parameters['etaH'] >= 0.7:
        recommendations.append("✅ **HER2 therapy potential favorable**")
    elif parameters['etaH'] >= 0.4:
        recommendations.append("⚖️ **Moderate HER2 therapy benefit** (depends on clinical context)")

    # --- Immunotherapy (η_I and immune strength via β₁) ---
    etaI = parameters['etaI']
    beta1 = parameters['beta1']  # cytotoxic immune killing rate ∝ s_immune × (1 - s_suppress)

    if etaI >= 0.6 and beta1 >= 0.02:
        recommendations.append("✅ **Immunotherapy highly favorable** - Strong immune context and PD-L1 signal")
    elif etaI >= 0.45 and beta1 >= 0.01:
        recommendations.append("✅ **Immunotherapy shows promise**")
    elif etaI >= 0.45 and beta1 < 0.01:
        recommendations.append("⚖️ **Immunotherapy signal present but limited by weak immune function**")
    # If η_I is low, no positive immunotherapy recommendation is added.

    # --- Resistance risks ---
    if parameters['omegaR1'] > 0.005:
        recommendations.append("🚨 **High hormone resistance risk**")
    if parameters['omegaR2'] > 0.004:
        recommendations.append("🚨 **Elevated multi-drug resistance risk**")

    # --- Immune function summary (from β₁) ---
    if beta1 < 0.01:
        recommendations.append("⚠️ **Weak immune function**")
    elif beta1 > 0.05:
        recommendations.append("✅ **Strong immune function**")

    # --- Tumor growth and monitoring frequency ---
    if parameters['lambda1'] > 0.1:
        recommendations.append("🚨 **High tumor growth rate**")

    if parameters['omegaR1'] > 0.003 or parameters['omegaR2'] > 0.003 or parameters['lambda1'] > 0.08:
        recommendations.append("📅 **Enhanced monitoring** - Monthly panels")
    else:
        recommendations.append("📅 **Standard monitoring** - Quarterly panels")

    # --- Organ function safety flags ---
    if biomarkers.get('creatinine', 0) > 1.5 or biomarkers.get('alt', 0) > 60:
        recommendations.append("⚠️ **Organ function attention** - Adjust dosing")

    if not recommendations:
        recommendations.append("Standard treatment approach recommended.")

    return recommendations


def display_clinical_interpretation(parameters, biomarkers):
    """
    High-level, clinically-oriented interpretation of treatment effectiveness parameters.
    This is an adjunct decision-support layer, not part of Chapter 4 equations.
    """
    st.subheader("🏥 Clinical Decision Support")
    st.write("### Treatment Selection Guidance")

    # Immunotherapy
    eta_I = parameters['etaI']
    cd8_count = biomarkers['cd8']

    if eta_I > 0.5 and cd8_count > 500:
        st.success(f"✅ **Strong Immunotherapy Candidate** (ηI = {eta_I:.3f})")
        st.write("- High immune effectiveness predicted")
        st.write("- CD8+ T cell count supports immune response")
        st.write("- Recommend: PD-1/PD-L1 inhibitors")
    elif eta_I > 0.3:
        st.info(f"⚡ **Moderate Immunotherapy Candidate** (ηI = {eta_I:.3f})")
        st.write("- Consider combination with other therapies")
    else:
        st.warning(f"⚠️ **Limited Immunotherapy Response Expected** (ηI = {eta_I:.3f})")
        st.write("- Consider alternative treatment approaches")

    st.write("---")

    # Chemotherapy
    eta_C = parameters['etaC']
    organ_function = parameters['kel']  # Kidney/liver function indicator (lower kel → better clearance)

    st.write("### Chemotherapy Guidance")
    if eta_C > 0.4 and organ_function < 0.2:
        st.success(f"✅ **Strong Chemotherapy Candidate** (ηC = {eta_C:.3f})")
        st.write("- Good organ function for drug metabolism")
        st.write("- High treatment effectiveness predicted")
    elif eta_C > 0.2:
        st.info(f"⚡ **Moderate Chemotherapy Candidate** (ηC = {eta_C:.3f})")
        st.write("- Monitor organ function closely")
    else:
        st.warning(f"⚠️ **Limited Chemotherapy Effectiveness** (ηC = {eta_C:.3f})")

    st.write("---")

    # Hormone Therapy
    eta_E = parameters['etaE']
    esr1_mutations = biomarkers['esr1_mutations']

    st.write("### Hormone Therapy Guidance")
    if eta_E > 0.4 and esr1_mutations < 2:
        st.success(f"✅ **Strong Hormone Therapy Candidate** (ηE = {eta_E:.3f})")
        st.write("- Low ESR1 mutation burden")
        st.write("- Good receptor sensitivity predicted")
    else:
        st.info(f"⚡ **Monitor for Hormone Resistance** (ηE = {eta_E:.3f})")
        st.write(f"- ESR1 mutation score: {esr1_mutations}")


def display_resistance_monitoring(parameters, biomarkers):
    """
    Early resistance detection and monitoring recommendations based on ω_R1, ω_R2 and genetic stability.
    """
    st.subheader("🚨 Early Resistance Detection")

    omega_R1 = parameters['omegaR1']
    omega_R2 = parameters['omegaR2']
    # Genetic stability (from composite scores, stored in parameters for convenience)
    genetic_stability = parameters.get('G', 0.8)

    resistance_risk = (omega_R1 + omega_R2) * (2 - genetic_stability)

    if resistance_risk > 0.01:
        st.error("🔴 HIGH RESISTANCE RISK")
        st.write("Recommended Action: Monitor every 2–3 weeks vs standard 6–8 weeks")
        st.write("Clinical Benefit: Potentially avoid 1–2 ineffective treatment cycles")
    elif resistance_risk > 0.005:
        st.warning("🟡 MODERATE RESISTANCE RISK")
        st.write("Recommended Action: Enhanced monitoring every 4 weeks")
    else:
        st.success("🟢 LOW RESISTANCE RISK")
        st.write("Recommended Action: Standard monitoring schedule")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Hormone Resistance Rate (ω_R1)", f"{omega_R1:.6f}")
        st.caption("Reference (synthetic cohort): < 0.003")
    with col2:
        st.metric("MDR Resistance Rate (ω_R2)", f"{omega_R2:.6f}")
        st.caption("Reference (synthetic cohort): < 0.002")


def display_stability_assessment(parameters):
    """
    Display mathematical stability assessment based on Chapter 4 parameters.
    """
    st.subheader("🧮 Mathematical Stability Analysis")
    stability_status, message = assess_mathematical_stability(parameters)

    if stability_status == "STABLE":
        st.success(message)
        st.write("Clinical Implication: Model predictions highly reliable for treatment planning")
    elif stability_status == "MARGINAL":
        st.warning(message)
        st.write("Clinical Implication: Use predictions with caution, consider additional data")
    else:
        st.error(message)
        st.write("Clinical Implication: Aggressive disease likely, require frequent reassessment")

    st.caption("Based on 46.7% stability rate from 5,000 synthetic patient analysis.")


def generate_clinical_report(biomarkers, parameters, patient_id: str = ""):
    """
    Generate a text-based clinical-style report summarizing biomarkers and key parameters.
    """
    # Recompute genetic stability G from biomarkers to ensure correctness
    try:
        scores = calculate_composite_scores(biomarkers)
        genetic_stability = scores.get('G', 'N/A')
    except Exception:
        genetic_stability = 'N/A'

    report = (
        "# BLOOD-BASED CANCER MATHEMATICAL MODEL REPORT\n"
        f"Patient ID: {patient_id or 'N/A'}\n"
        f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        "Model Version: Chapter 4 Implementation v1.0\n\n"
        "## BIOMARKER SUMMARY\n"
        f"Total Biomarkers Analyzed: {sum(1 for v in biomarkers.values() if v > 0)}/47\n"
        "### Critical Values:\n"
        f"- CA 15-3: {biomarkers.get('ca153', 0):.1f} U/mL (Normal: <25)\n"
        f"- CD8+ T cells: {biomarkers.get('cd8', 0):.0f} cells/μL (Normal: 600-1200)\n"
        f"- Genetic Stability (G): {genetic_stability}\n\n"
        "## TREATMENT RECOMMENDATIONS\n"
        "### Immunotherapy Assessment:\n"
        f"- Effectiveness Parameter (η_I): {parameters['etaI']:.3f}\n"
        "- Recommendation: "
        f"{'STRONG CANDIDATE' if parameters['etaI'] > 0.5 else 'MODERATE' if parameters['etaI'] > 0.3 else 'LIMITED BENEFIT'}\n\n"
        "### Resistance Monitoring:\n"
        f"- Hormone Resistance Rate: {parameters['omegaR1']:.6f}\n"
        f"- MDR Resistance Rate: {parameters['omegaR2']:.6f}\n"
        "- Monitoring Frequency: "
        f"{'Every 2-3 weeks' if (parameters['omegaR1'] + parameters['omegaR2']) > 0.01 else 'Standard 6-8 weeks'}\n\n"
        "## MATHEMATICAL VALIDATION\n"
        "- Model Stability: Based on 46.7% stability rate from synthetic validation\n"
        "- R² = 0.996 on synthetic cohort (Chapter 4)\n\n"
        "## IMPORTANT DISCLAIMERS\n"
        "- This analysis is based on synthetic patient validation data\n"
        "- Clinical validation with real patients is required for clinical use\n"
        "- Results should supplement, not replace, clinical judgment\n"
        "- Immediate clinical correlation recommended for critical values\n"
    )
    return report


def display_export_options(biomarkers, parameters):
    """
    Export options for clinical-style report and raw parameter CSV.
    """
    st.subheader("📋 Export & Reporting")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Generate Clinical Report"):
            report = generate_clinical_report(biomarkers, parameters)
            st.download_button(
                label="Download Report (TXT)",
                data=report,
                file_name=f"cancer_model_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
            )

    with col2:
        if st.button("📊 Export Parameters (CSV)"):
            df = pd.DataFrame([parameters]).T
            df.columns = ['Value']
            csv = df.to_csv()
            st.download_button(
                label="Download Parameters (CSV)",
                data=csv,
                file_name=f"model_parameters_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )

