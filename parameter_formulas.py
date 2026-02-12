"""
Parameter Derivation Formulas Module
Displays all 37 parameter derivation formulas from Chapter 4
"""

import streamlit as st

def display_parameter_formulas():
    """
    Display all 37 parameter derivation formulas from Chapter 4
    """
    st.header("📊 Parameter Derivation Formulas")
    st.info("""
    All 37 model parameters are systematically derived from the 47-biomarker blood panel. Each parameter is calculated using direct scaling, composite scoring, piecewise functions, 
    and bounded transformations to ensure biologically realistic values.
    """)
    
    # Composite Scores Section
    st.subheader("🔢 Composite Scores (Used in Parameter Calculations)")
    
    with st.expander("📈 Composite Score Formulas"):
        st.write("**Tumor Burden Score:**")
        st.latex(r"""
        s_{\text{tumor}} = \frac{1}{5}\left(\frac{\text{CA 15-3}}{31.3} + \frac{\text{CA 27-29}}{38} 
        + \frac{\text{CEA}}{3.0} + \frac{\text{CTC}}{5} + \frac{\text{ctDNA}}{1.0}\right)
        """)
        
        st.write("**Proliferation Score:**")
        st.latex(r"""
        s_{\text{prolif}} = \frac{1}{4}\left(\frac{\text{TK1}}{2.0} + \frac{\text{Glucose}}{95} 
        + \frac{\text{Lactate}}{2.2} + \frac{\text{Survivin}}{0.5}\right)
        """)
        
        st.write("**Immune Strength Score:**")
        st.latex(r"""
        s_{\text{immune}} = 0.4\left(\frac{\text{CD8}}{700}\right) + 0.3\left(\frac{\text{CD4}}{1050}\right) 
        + 0.2\left(\frac{\text{NK}}{345}\right) + 0.1\left(\frac{\text{IFN-}\gamma}{2.0}\right)
        """)
        
        st.write("**Immunosuppression Score:**")
        st.latex(r"""
        s_{\text{suppress}} = \frac{1}{3}\left(\frac{\text{IL-10}}{5.0} + \frac{\text{TGF-}\beta}{2.5} 
        + \frac{\text{PD-L1}}{1.0}\right)
        """)
        
        st.write("**Genetic Stability (G):**")
        st.latex(r"""
        G = \max\left(0.1, \min\left(1.0, 1 - 0.3\left(\frac{\text{ctDNA}}{1.0}\right) 
        - 0.2\left(\frac{\text{PIK3CA}}{10}\right) - 0.2\left(\frac{\text{TP53}}{10}\right)\right)\right)
        """)
        
        st.write("**Genetic Score:**")
        st.latex(r"""
        s_{\text{genetic}} = \frac{1}{3}\left(\frac{\text{ctDNA}}{1.0} + \frac{\text{PIK3CA}}{10} 
        + \frac{\text{TP53}}{10}\right)
        """)
        
        st.write("**Metabolic Stress Score:**")
        st.latex(r"""
        s_{\text{metabolic}} = \frac{1}{3}\left(\frac{\text{Glucose}}{95} + \frac{\text{Lactate}}{2.2} 
        + \frac{\text{LDH}}{250}\right)
        """)
        
        st.write("**Activation Score:**")
        st.latex(r"""
        s_{\text{activation}} = \frac{1}{2}\left(\frac{\text{IFN-}\gamma}{5} + \frac{\text{CD4}}{1200}\right)
        """)
        
        st.write("**Resistance Factor 1:**")
        st.latex(r"""
        f_{\text{resist1}} = \max\left(0.1, \min\left(2.0, \frac{1}{4}\left(\frac{\text{ESR1\_mut}}{8} 
        + \frac{\text{PGR}}{20} + \frac{\text{PIK3CA}}{5} + \frac{\text{Survivin}}{6}\right)\right)\right)
        """)
        
        st.write("**Resistance Factor 2:**")
        st.latex(r"""
        f_{\text{resist2}} = \max\left(0.1, \min\left(2.0, \frac{1}{4}\left(\frac{\text{HER2\_mut}}{10} 
        + \frac{\text{MDR1}}{150} + \frac{\text{Survivin}}{6} + \frac{\text{HSP}}{10}\right)\right)\right)
        """)
        
        st.write("**Metastatic Factor:**")
        st.latex(r"""
        f_{\text{metastatic}} = \frac{1}{3}\left(\frac{\text{CTC}}{20} + f_{\text{EMT}} 
        + \frac{\text{Exosomes}}{100}\right)
        """)
        st.latex(r"""
        f_{\text{EMT}} = \max\left(0, \frac{5 - \text{miR-200}}{5}\right)
        """)
        st.write("**Stress Score (s_stress):** $s_{\\text{stress}} = s_{\\text{metabolic}}$")
        st.write("**Quiescence Score:**")
        st.latex(r"""
        s_{\text{quiescence}} = \frac{1}{2}\left(\max\left(0, \frac{100 - \text{Glucose}}{100}\right) 
        + \min\left(1, \frac{\text{Lactate}}{4}\right)\right)
        """)
        st.write("**Organ Function Factors:**")
        st.latex(r"""
        f_{\text{liver}} = \frac{1}{3}\left(\max\left(0.2, \min\left(1.2, \frac{40}{\max(\text{ALT}, 5)}\right)\right) 
        + \max\left(0.2, \min\left(1.2, \frac{45}{\max(\text{AST}, 8)}\right)\right) 
        + \max\left(0.5, \min\left(1.5, \frac{1.2}{\max(\text{Bili}, 0.1)}\right)\right)\right)
        """)
        st.latex(r"""
        f_{\text{kidney}} = \frac{1}{2}\left(\max\left(0.3, \min\left(1.3, \frac{1.2}{\max(\text{Creat}, 0.5)}\right)\right) 
        + \max\left(0.3, \min\left(1.3, \frac{20}{\max(\text{BUN}, 5)}\right)\right)\right)
        """)
        st.latex(r"""
        f_{\text{clearance}} = f_{\text{liver}} \times f_{\text{kidney}}
        """)
    
    st.divider()
    
    # Growth Parameters
    st.subheader("🌱 Growth and Proliferation Parameters (5)")
    
    st.write("**1. Sensitive Cell Growth Rate (λ₁):**")
    st.latex(r"""
    \lambda_1 = \max(0.01, \min(0.15, 0.04 \times (1 + 1.5 \times s_{\text{prolif}})))
    """)
    st.caption("Derived from: TK1, Glucose, Lactate, Survivin → s_prolif")
    
    st.write("**2. Partially Resistant Cell Growth Rate (λ₂):**")
    st.latex(r"""
    \lambda_2 = \max(0.005, \min(0.1, 0.6 \times \lambda_1 \times (1 + 0.5 \times f_{\text{resist1}})))
    """)
    st.caption("Derived from: λ₁, ESR1_mut, PGR, PIK3CA, Survivin → f_resist1")
    
    st.write("**3. Hormone-Resistant Cell Growth (λ_R1):**")
    st.latex(r"""
    \lambda_{R1} = \max(0.003, \min(0.05, 0.4 \times \lambda_1 \times f_{\text{resist1}}))
    """)
    st.caption("Derived from: λ₁, f_resist1")
    
    st.write("**4. Multi-Drug Resistant Cell Growth (λ_R2):**")
    st.latex(r"""
    \lambda_{R2} = \max(0.001, \min(0.03, 0.25 \times \lambda_1 \times (1 - 0.3 \times f_{\text{resist2}})))
    """)
    st.caption("Derived from: λ₁, HER2_mut, MDR1, Survivin, HSP → f_resist2")
    
    st.write("**5. Carrying Capacity (K):**")
    st.latex(r"""
    K = \max(100, \min(15000, s_{\text{tumor}} \times 2000))
    """)
    st.caption("Derived from: CA 15-3, CA 27-29, CEA, CTC, ctDNA → s_tumor")
    
    st.divider()
    
    # Immune Parameters
    st.subheader("🛡️ Immune System Parameters (6)")
    
    st.write("**6. Cytotoxic Immune Killing Rate (β₁):**")
    st.latex(r"""
    \beta_1 = \max(0.001, \min(0.1, 0.02 \times s_{\text{immune}} \times (1 - s_{\text{suppress}})))
    """)
    st.caption("Derived from: CD8, CD4, NK, IFN-γ → s_immune; IL-10, TGF-β, PD-L1 → s_suppress")
    
    st.write("**7. Regulatory Immune Suppression Rate (β₂):**")
    st.latex(r"""
    \beta_2 = \max(0.01, \min(0.5, 0.05 + 0.15 \times s_{\text{suppress}}))
    """)
    st.caption("Derived from: IL-10, TGF-β, PD-L1 → s_suppress")
    
    st.write("**8. Basal Cytotoxic Immune Production (φ₁):**")
    st.latex(r"""
    \phi_1 = \max(0.01, \min(0.2, 0.05 + 0.1 \times s_{\text{activation}}))
    """)
    st.caption("Derived from: IFN-γ, CD4 → s_activation")
    
    st.write("**9. Tumor-Induced Immune Recruitment (φ₂):**")
    st.latex(r"""
    \phi_2 = \max(0.005, \min(0.1, 0.01 + 0.03 \times \frac{s_{\text{tumor}}}{2}))
    """)
    st.caption("Derived from: s_tumor")
    
    st.write("**10. Regulatory Cell Recruitment (φ₃):**")
    st.latex(r"""
    \phi_3 = \max(0.005, \min(0.15, 0.02 + 0.08 \times \frac{\text{IL-10}}{15}))
    """)
    st.caption("Derived from: IL-10 directly")
    
    st.write("**11. Immune Cell Death Rate (δ_I):**")
    st.latex(r"""
    \delta_I = \max(0.02, \min(0.3, 0.05 + 0.1 \times s_{\text{stress}}))
    """)
    st.caption("Derived from: Glucose, Lactate, LDH → s_metabolic = s_stress")
    
    st.divider()
    
    # Resistance Evolution Parameters
    st.subheader("🔄 Resistance Evolution Parameters (3)")
    
    st.write("**12. Hormone Resistance Evolution Rate (ω_R1):**")
    st.latex(r"""
    \omega_{R1} = \max(0.0001, \min(0.01, 0.002 \times s_{\text{genetic}} \times s_{\text{stress}}))
    """)
    st.caption("Derived from: ctDNA, PIK3CA, TP53 → s_genetic; s_metabolic → s_stress")
    
    st.write("**13. Multi-Drug Resistance Evolution (ω_R2):**")
    st.latex(r"""
    \omega_{R2} = \max(0.0001, \min(0.008, 0.001 \times s_{\text{genetic}} \times s_{\text{stress}}))
    """)
    st.caption("Derived from: s_genetic, s_stress")
    
    st.write("**14. Genetic Instability Accumulation (μ):**")
    st.latex(r"""
    \mu = \max(0.001, \min(0.05, 0.01 \times (1 + 1.5 \times s_{\text{genetic}})))
    """)
    st.caption("Derived from: ctDNA, PIK3CA, TP53 → s_genetic")
    
    st.divider()
    
    # Treatment Effectiveness Parameters
    st.subheader("💊 Treatment Effectiveness Parameters (4)")
    
    st.write("**15. Hormone Therapy Effectiveness (η_E):**")
    st.latex(r"""
    \eta_E = \max(0.1, \min(0.95, f_{\text{receptor}} \times f_{\text{metabolism}} \times f_{\text{resist\_hormone}}))
    """)
    st.latex(r"""
    f_{\text{receptor}} = \min\left(1.0, \frac{\text{ESR1\_protein}}{6.0}\right)
    """)
    st.latex(r"""
    f_{\text{metabolism}} = \frac{1}{3}(f_{\text{liver}} + f_{\text{CYP2D6}} + f_{\text{general}})
    """)
    st.latex(r"""
    f_{\text{CYP2D6}} = \min(1.0, \text{CYP2D6}/2.0), \quad
    f_{\text{general}} = \frac{1}{2}\left(\frac{\text{Albumin}}{4.0} + \max\left(0.5, 1 - 0.3 \times \frac{|95 - \text{Glucose}|}{95}\right)\right)
    """)
    st.latex(r"""
    f_{\text{resist\_hormone}} = 1 - \min\left(0.9, 0.6 \times \frac{\text{ESR1\_mut}}{8} + 0.4 \times s_{\text{genetic}}\right)
    """)
    st.caption("Derived from: ESR1_protein, Liver (ALT/AST/Bilirubin), CYP2D6, Albumin, Glucose, ESR1_mut, s_genetic")
    
    st.write("**16. Chemotherapy Effectiveness (η_C):**")
    st.latex(r"""
    \eta_C = \max(0.1, \min(0.95, f_{\text{general}} \times f_{\text{organs}} \times (1 - 0.7 \times f_{\text{resist2}})))
    """)
    st.latex(r"""
    f_{\text{general}} = \frac{1}{2}\left(\frac{\text{Albumin}}{4.0} + \max\left(0.5, 1 - 0.3 \times \frac{|95 - \text{Glucose}|}{95}\right)\right)
    """)
    st.latex(r"""
    f_{\text{organs}} = \frac{1}{2}(f_{\text{liver}} + f_{\text{kidney}})
    """)
    st.caption("Derived from: Albumin, Glucose, Liver function, Kidney function (Creatinine/BUN), f_resist2")
    
    st.write("**17. HER2-Targeted Therapy Effectiveness (η_H):**")
    st.latex(r"""
    \eta_H = \max(0.1, \min(0.95, f_{\text{HER2}} \times f_{\text{organs}} \times (1 - 0.5 \times f_{\text{resist2}})))
    """)
    st.latex(r"""
    f_{\text{HER2}} = \min\left(1.0, \frac{\text{HER2\_circ}}{5.0}\right) \times \left(1 - 0.6 \times \frac{\text{HER2\_mut}}{10}\right)
    """)
    st.caption("Derived from: HER2_circ, HER2_mut, f_organs, f_resist2")
    
    st.write("**18. Immunotherapy Effectiveness (η_I):**")
    st.latex(r"""
    \eta_I = \max(0.1, \min(0.95, f_{\text{PDL1}} \times f_{\text{immune\_ctx}} \times f_{\text{general}}))
    """)
    st.latex(r"""
    f_{\text{PDL1}} = \min\left(1.0, \frac{\text{PD-L1\_CTC}}{3.0}\right)
    """)
    st.latex(r"""
    f_{\text{immune\_ctx}} = \frac{1}{4}\left(\frac{\text{CD8}}{700} + \frac{\text{CD4}}{1050} + \frac{\text{IFN-}\gamma}{2.0} 
    + \max\left(0, 1 - \frac{\text{IL-10}}{15}\right)\right)
    """)
    st.caption("Derived from: PD-L1_CTC, CD8, CD4, IFN-γ, IL-10, Albumin, Glucose")
    
    st.divider()
    
    # Pharmacokinetic Parameters
    st.subheader("⚡ Pharmacokinetic Parameters (3)")
    
    st.write("**19. Drug Elimination Rate (k_el):**")
    st.latex(r"""
    k_{\text{el}} = \max\left(0.05, \min\left(0.3, \frac{0.1}{f_{\text{clearance}}}\right)\right)
    """)
    st.latex(r"""
    f_{\text{clearance}} = f_{\text{liver}} \times f_{\text{kidney}}
    """)
    st.caption("Derived from: Liver function (ALT/AST/Bilirubin), Kidney function (Creatinine/BUN)")
    
    st.write("**20. Drug Metabolism Rate (k_metabolism):**")
    st.latex(r"""
    k_{\text{metabolism}} = \max(0.02, \min(0.2, 0.05 \times f_{\text{liver}}))
    """)
    st.caption("Derived from: Liver function (ALT/AST/Bilirubin)")
    
    st.write("**21. Metabolite Clearance (k_clearance):**")
    st.latex(r"""
    k_{\text{clearance}} = \max(0.1, \min(0.5, 0.2 \times f_{\text{clearance}}))
    """)
    st.caption("Derived from: f_clearance (Liver × Kidney)")
    
    st.divider()
    
    # Microenvironmental Parameters
    st.subheader("🌐 Microenvironmental Parameters (8)")
    
    st.write("**22. Angiogenesis Induction (α_A):**")
    st.latex(r"""
    \alpha_A = \max\left(0.001, \min\left(0.1, 0.02 \times \left(1 + \frac{\text{VEGF}}{400}\right) 
    \times \left(1 + \frac{\text{Ang-2}}{3000}\right)\right)\right)
    """)
    st.caption("Derived from: VEGF, Ang-2 directly")
    
    st.write("**23. Angiogenesis Degradation (δ_A):**")
    st.latex(r"""
    \delta_A = \max(0.05, \min(0.2, 0.1 \times f_{\text{clearance}}))
    """)
    st.caption("Derived from: f_clearance")
    
    st.write("**24. Quiescence Entry Rate (κ_Q):**")
    st.latex(r"""
    \kappa_Q = \max(0.001, \min(0.05, 0.005 + 0.02 \times s_{\text{quiescence}}))
    """)
    st.caption("Derived from: Nutrient stress, Metabolic stress → s_quiescence")
    
    st.write("**25. Quiescence Exit Rate (λ_Q):**")
    st.latex(r"""
    \lambda_Q = \max(0.0005, \min(0.02, 0.002 + 0.01 \times (1 - s_{\text{quiescence}})))
    """)
    st.caption("Derived from: s_quiescence")
    
    st.write("**26. Senescence Induction (κ_S):**")
    st.latex(r"""
    \kappa_S = \max(0.001, \min(0.04, 0.002 + 0.01 \times s_{\text{stress}}))
    """)
    st.caption("Derived from: s_metabolic = s_stress")
    
    st.write("**27. Senescent Cell Clearance (δ_S):**")
    st.latex(r"""
    \delta_S = \max(0.02, \min(0.1, 0.05 \times s_{\text{immune}}))
    """)
    st.caption("Derived from: CD8, CD4, NK, IFN-γ → s_immune")
    
    st.write("**28. Metastatic Seeding Rate (γ):**")
    st.latex(r"""
    \gamma = \max(0.0001, \min(0.01, 0.002 \times f_{\text{metastatic}}))
    """)
    st.caption("Derived from: CTC, miR-200, Exosomes → f_metastatic")
    
    st.write("**29. Metastatic Clearance (δ_P):**")
    st.latex(r"""
    \delta_P = \max(0.02, \min(0.1, 0.05 + 0.03 \times s_{\text{immune}}))
    """)
    st.caption("Derived from: s_immune")
    
    st.divider()
    
    # Genetic & Metabolic Parameters
    st.subheader("🧬 Genetic & Metabolic Parameters (7)")
    
    st.write("**30. Treatment-Induced Mutagenesis (ν):**")
    st.latex(r"""
    \nu = \max(0.0001, \min(0.01, 0.002 \times s_{\text{genetic}} \times s_{\text{stress}}))
    """)
    st.caption("Derived from: s_genetic, s_stress")
    
    st.write("**31. Genetic Stability Restoration (δ_G):**")
    st.latex(r"""
    \delta_G = \max(0.001, \min(0.05, 0.01 \times \text{BRCA\_factor} \times G))
    """)
    st.caption("Derived from: BRCA mutations, Genetic stability (G)")
    
    st.write("**32. Metabolic Reprogramming Rate (κ_M):**")
    st.latex(r"""
    \kappa_M = \max(0.001, \min(0.1, 0.02 \times s_{\text{metabolic}} \times \text{ketone\_factor}))
    """)
    st.caption("Derived from: Glucose, Lactate, LDH → s_metabolic; Beta-hydroxybutyrate")
    
    st.write("**33. Metabolic Normalization (δ_M):**")
    st.latex(r"""
    \delta_M = \max(0.001, \min(0.05, 0.01 \times (1 - 0.5 \times s_{\text{metabolic}})))
    """)
    st.caption("Derived from: s_metabolic")
    
    st.write("**34. Hypoxia Induction Rate (κ_H):**")
    st.latex(r"""
    \kappa_H = \max(0.001, \min(0.1, 0.02 \times \max(0, s_{\text{tumor}} - 0.5)))
    """)
    st.caption("Derived from: s_tumor (only when > 50% capacity)")
    
    st.write("**35. Hypoxia Clearance (δ_H):**")
    st.latex(r"""
    \delta_H = \max(0.01, \min(0.1, 0.05 \times (1 + f_{\text{clearance}})))
    """)
    st.caption("Derived from: f_clearance")
    
    st.write("**36. Hormone-Resistant Immune Sensitivity (ρ₁):**")
    st.latex(r"""
    \rho_1 = \max(0.6, \min(0.9, 0.75 + 0.15 \times s_{\text{immune}}))
    """)
    st.caption("Derived from: s_immune (range [0.6, 0.9] per Chapter 4)")
    
    st.write("**37. Multi-Drug Resistant Immune Sensitivity (ρ₂):**")
    st.latex(r"""
    \rho_2 = \max(0.3, \min(0.6, 0.45 - 0.15 \times f_{\text{resist2}}))
    """)
    st.caption("Derived from: f_resist2 (range [0.3, 0.6] per Chapter 4)")

    st.divider()
    # ODE-only parameter (not counted in the 37)
    st.subheader("📐 ODE Supplementary: α_acid")
    st.latex(r"""
    \alpha_{\text{acid}} = \max\left(0.01, \min\left(0.5, 2 \times (7.4 - \text{Blood pH})\right)\right)
    """)
    
    st.divider()
    
    # Summary
    st.subheader("📋 Parameter Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Parameters", "37")
        st.metric("Growth Parameters", "5")
        st.metric("Immune Parameters", "6")
    with col2:
        st.metric("Resistance Parameters", "3")
        st.metric("Treatment Parameters", "4")
        st.metric("Pharmacokinetic", "3")
    with col3:
        st.metric("Microenvironmental", "8")
        st.metric("Genetic/Metabolic", "6")
        st.metric("Immune Sensitivity", "2")
    
    st.info("""
    **All 37 parameters** are derived from the **47-biomarker blood panel**. 
    Each parameter is bounded to ensure biologically realistic values and validated against biological constraints.
    """)

