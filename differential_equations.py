"""
Differential Equations Module
Displays all 15 differential equations from Chapter 4
"""

import streamlit as st

def display_differential_equations():
    """
    Display all 15 differential equations from Chapter 4
    """
    st.header("📐 15-Dimensional Differential Equation System")
    st.info("""
    The complete mathematical framework consists of 15 coupled ordinary differential equations 
    describing cancer progression, immune response, treatment effects, and resistance evolution.
    """)
    
    # State variables explanation
    with st.expander("📊 State Variables (15 dimensions)"):
        st.write("""
        The state vector **Y(t)** = [N₁, N₂, I₁, I₂, P, A, Q, R₁, R₂, S, D, Dₘ, G, M, H]ᵀ where:
        
        - **N₁(t)**: Treatment-sensitive cancer cells
        - **N₂(t)**: Partially resistant cancer cells  
        - **I₁(t)**: Cytotoxic immune cells (CD8+ T cells, NK cells)
        - **I₂(t)**: Regulatory immune cells (Tregs, MDSCs)
        - **P(t)**: Metastatic potential and invasion capacity
        - **A(t)**: Angiogenesis factors and vascular density
        - **Q(t)**: Quiescent (dormant) cancer cells
        - **R₁(t)**: Hormone receptor-based resistant cells
        - **R₂(t)**: Multi-drug resistant cells
        - **S(t)**: Senescent cells
        - **D(t)**: Active drug concentration
        - **Dₘ(t)**: Metabolized drug concentration
        - **G(t)**: Genetic stability
        - **M(t)**: Metabolic state
        - **H(t)**: Hypoxia level
        """)
    
    st.divider()
    
    # Equation 1: Sensitive Cancer Cells (N₁)
    st.subheader("1️⃣ Sensitive Cancer Cell Dynamics (N₁)")
    st.write("""
    **What it models:** Treatment-sensitive cancer cells that respond to therapy. Tracks growth, immune interactions, 
    treatment effects, and transitions to other cell states (quiescent, resistant, senescent).
    """)
    st.latex(r"""
    \frac{dN_1}{dt} = \lambda_1 N_1 \left(1 - \frac{N_{\text{total}}}{K}\right) \frac{(1 + 0.1M)}{(1 + \alpha_{\text{acid}} M)} 
    - \frac{\beta_1 N_1 I_1}{1 + 0.01N_{\text{total}}} - \eta_{\text{treat}} N_1
    """)
    st.latex(r"""
    \quad - \kappa_Q N_1(1 + 0.5H) - \omega_{R1} \eta_{\text{treat}} N_1(2 - G) 
    - \omega_{R2} \eta_{\text{treat}} N_1(2 - G) - \kappa_S \eta_{\text{treat}} N_1(1.3 - 0.3G)
    """)
    st.caption("""
    **Contains:** Logistic growth (λ₁, K) → Metabolic/pH modulation → Immune killing (β₁) → Treatment (η) → 
    Quiescence (κ_Q) → Resistance evolution (ω_R1, ω_R2) → Senescence (κ_S)
    """)
    
    # Equation 2: Partially Resistant Cells (N₂)
    st.subheader("2️⃣ Partially Resistant Cell Dynamics (N₂)")
    st.write("""
    **What it models:** Intermediate resistance phenotype with reduced sensitivity to treatment (70%) and immune killing (50%). 
    Acts as transitional state between sensitive and fully resistant cells.
    """)
    st.latex(r"""
    \frac{dN_2}{dt} = \lambda_2 N_2 \left(1 - \frac{N_{\text{total}}}{K}\right) \frac{(1 + 0.1M)}{(1 + \alpha_{\text{acid}} M)} 
    - \frac{0.5\beta_1 N_2 I_1}{1 + 0.01N_{\text{total}}} - 0.7\eta_{\text{treat}} N_2 
    - \kappa_Q N_2(1 + 0.5H)
    """)
    st.caption("""
    **Contains:** Reduced growth (λ₂) → Reduced immune killing (0.5×β₁) → Reduced treatment (0.7×η) → Quiescence entry
    """)
    
    # Equation 3: Cytotoxic Immune Cells (I₁)
    st.subheader("3️⃣ Cytotoxic Immune Cell Dynamics (I₁)")
    st.write("""
    **What it models:** CD8+ T cells and NK cells that kill cancer cells. Includes production, tumor-induced recruitment, 
    regulatory suppression, hypoxia-enhanced death, and immunotherapy enhancement.
    """)
    st.latex(r"""
    \frac{dI_1}{dt} = \phi_1 + \frac{\phi_2 N_{\text{total}}}{1 + 0.01N_{\text{total}}} 
    - \frac{\beta_2 I_1 I_2}{1 + I_1} - \delta_I I_1(1 + 0.2H) + 0.1\eta_I u_I I_1
    """)
    st.caption("""
    **Contains:** Basal production (φ₁) → Tumor recruitment (φ₂) → Regulatory suppression (β₂) → 
    Hypoxia-enhanced death (δ_I) → Immunotherapy boost (η_I)
    """)
    
    # Equation 4: Regulatory Immune Cells (I₂)
    st.subheader("4️⃣ Regulatory Immune Cell Dynamics (I₂)")
    st.write("""
    **What it models:** Tregs and MDSCs that suppress immune responses. Recruited by tumors, die under hypoxia, 
    and are depleted by immunotherapy.
    """)
    st.latex(r"""
    \frac{dI_2}{dt} = \frac{\phi_3 N_{\text{total}}}{1 + 0.01N_{\text{total}}} 
    - \delta_I I_2(1 + 0.1H) - 0.1\eta_I u_I I_2
    """)
    st.caption("""
    **Contains:** Tumor recruitment (φ₃) → Hypoxia-enhanced death (δ_I) → Immunotherapy depletion
    """)
    
    # Equation 5: Metastatic Potential (P)
    st.subheader("5️⃣ Metastatic Potential Dynamics (P)")
    st.write("""
    **What it models:** Invasion capacity and circulating tumor cell seeding. Enhanced by hypoxia and metabolic 
    reprogramming, cleared by immune surveillance.
    """)
    st.latex(r"""
    \frac{dP}{dt} = \gamma N_{\text{total}}(1 + 0.5H)(1 + 0.3M) - \delta_P P
    """)
    st.caption("""
    **Contains:** Seeding rate (γ) → Hypoxia enhancement → Metabolic enhancement → Clearance (δ_P)
    """)
    
    # Equation 6: Angiogenesis (A)
    st.subheader("6️⃣ Angiogenesis Factor Dynamics (A)")
    st.write("""
    **What it models:** Vascular density and angiogenic factors (VEGF, Ang-2). Induced by tumor burden and hypoxia, 
    degraded naturally. Critical for tumor growth and oxygen supply.
    """)
    st.latex(r"""
    \frac{dA}{dt} = \frac{\alpha_A N_{\text{total}}(1 + H)}{1 + 0.01N_{\text{total}}} - \delta_A A
    """)
    st.caption("""
    **Contains:** Induction (α_A) → Hypoxia enhancement → Saturation kinetics → Degradation (δ_A)
    """)
    
    # Equation 7: Quiescent Cells (Q)
    st.subheader("7️⃣ Quiescent Cell Dynamics (Q)")
    st.write("""
    **What it models:** Dormant cancer cells that stop dividing. Enter quiescence under stress/hypoxia, 
    exit when conditions improve (angiogenesis). Treatment-resistant due to low metabolic activity.
    """)
    st.latex(r"""
    \frac{dQ}{dt} = \kappa_Q(N_1 + N_2)(1 + 0.5H) - \frac{\lambda_Q Q(1 + 0.2A)}{1 + 0.5H}
    """)
    st.caption("""
    **Contains:** Entry rate (κ_Q) → Hypoxia enhancement → Exit rate (λ_Q) → Angiogenesis promotion → Hypoxia inhibition
    """)
    
    # Equation 8: Hormone-Resistant Cells (R₁)
    st.subheader("8️⃣ Hormone-Resistant Cell Dynamics (R₁)")
    st.write("""
    **What it models:** Cells resistant to hormone therapy (ESR1 mutations). Evolve from sensitive cells under 
    treatment pressure, have reduced immune sensitivity (60-90%), and grow independently of estrogen.
    """)
    st.latex(r"""
    \frac{dR_1}{dt} = \omega_{R1} \eta_E u_E N_1(2 - G) + \lambda_{R1} R_1 \left(1 - \frac{N_{\text{total}}}{K}\right) 
    - \frac{\rho_1 \beta_1 R_1 I_1}{1 + 0.01N_{\text{total}}}
    """)
    st.caption("""
    **Contains:** Evolution rate (ω_R1) → Treatment pressure → Genetic instability → Growth (λ_R1) → Reduced immune killing (ρ₁)
    """)
    
    # Equation 9: Multi-Drug Resistant Cells (R₂)
    st.subheader("9️⃣ Multi-Drug Resistant Cell Dynamics (R₂)")
    st.write("""
    **What it models:** Cells with broad resistance (MDR1, efflux pumps). Evolve under chemotherapy pressure, 
    have severely reduced immune sensitivity (30-60%), and slow growth due to fitness costs.
    """)
    st.latex(r"""
    \frac{dR_2}{dt} = \omega_{R2} \eta_C u_C N_1(2 - G) + \lambda_{R2} R_2 \left(1 - \frac{N_{\text{total}}}{K}\right) 
    - \frac{\rho_2 \beta_1 R_2 I_1}{1 + 0.01N_{\text{total}}}
    """)
    st.caption("""
    **Contains:** Evolution rate (ω_R2) → Chemotherapy pressure → Genetic instability → Growth (λ_R2) → Highly reduced immune killing (ρ₂)
    """)
    
    # Equation 10: Senescent Cells (S)
    st.subheader("🔟 Senescent Cell Dynamics (S)")
    st.write("""
    **What it models:** Permanently growth-arrested cells from treatment-induced DNA damage. More common with 
    genetic instability. Cleared by immune cells (NK, macrophages).
    """)
    st.latex(r"""
    \frac{dS}{dt} = \kappa_S \eta_{\text{treat}} N_1(1.3 - 0.3G) - \delta_S S
    """)
    st.caption("""
    **Contains:** Senescence induction (κ_S) → Treatment pressure → Genetic instability enhancement → Clearance (δ_S)
    """)
    
    # Equation 11: Active Drug (D)
    st.subheader("1️⃣1️⃣ Active Drug Concentration (D)")
    st.write("""
    **What it models:** Pharmacokinetics of active drug in plasma. Includes administration, renal elimination, 
    and hepatic metabolism. Derived from organ function biomarkers.
    """)
    st.latex(r"""
    \frac{dD}{dt} = \text{dose\_rate}(t) - k_{\text{el}} D - k_{\text{metabolism}} D
    """)
    st.caption("""
    **Contains:** Drug administration → Renal elimination (k_el) → Hepatic metabolism (k_metabolism)
    """)
    
    # Equation 12: Metabolized Drug (Dₘ)
    st.subheader("1️⃣2️⃣ Metabolized Drug Concentration (Dₘ)")
    st.write("""
    **What it models:** Metabolized drug products. Some metabolites retain activity or cause toxicity. 
    Cleared by renal and biliary excretion.
    """)
    st.latex(r"""
    \frac{dD_m}{dt} = k_{\text{metabolism}} D - k_{\text{clearance}} D_m
    """)
    st.caption("""
    **Contains:** Input from metabolism → Renal/biliary clearance (k_clearance)
    """)
    
    # Equation 13: Genetic Stability (G)
    st.subheader("1️⃣3️⃣ Genetic Stability Dynamics (G)")
    st.write("""
    **What it models:** Genomic integrity (0-1 scale). Decreases with tumor burden and treatment-induced mutations, 
    partially restored by DNA repair. Lower stability accelerates resistance evolution.
    """)
    st.latex(r"""
    \frac{dG}{dt} = -\mu N_{\text{total}} - \nu \eta_{\text{treat}}(2 - G) + \delta_G(1 - G)
    """)
    st.caption("""
    **Contains:** Mutation accumulation (μ) → Treatment mutagenesis (ν) → DNA repair restoration (δ_G)
    """)
    
    # Equation 14: Metabolic State (M)
    st.subheader("1️⃣4️⃣ Metabolic State Dynamics (M)")
    st.write("""
    **What it models:** Warburg effect and metabolic reprogramming. Enhanced by hypoxia (HIF-1α), 
    derived from glucose, lactate, LDH. Supports rapid growth and metastasis.
    """)
    st.latex(r"""
    \frac{dM}{dt} = \kappa_M N_{\text{total}}(1 + 0.5H) - \delta_M M
    """)
    st.caption("""
    **Contains:** Metabolic reprogramming (κ_M) → Hypoxia enhancement → Normalization (δ_M)
    """)
    
    # Equation 15: Hypoxia (H)
    st.subheader("1️⃣5️⃣ Hypoxia Level Dynamics (H)")
    st.write("""
    **What it models:** Oxygen deprivation in tumors. Develops when tumor burden exceeds vascular supply (>50% capacity). 
    Reduced by angiogenesis, cleared by natural oxygenation. Enhances metastasis and metabolic reprogramming.
    """)
    st.latex(r"""
    \frac{dH}{dt} = \kappa_H \max\left(0, \frac{N_{\text{total}}}{K} - 0.5\right) - \alpha_A A H - \delta_H H
    """)
    st.caption("""
    **Contains:** Hypoxia induction (κ_H) → Threshold (50% capacity) → Angiogenesis reduction → Natural clearance (δ_H)
    """)
    
    st.divider()
    
    # Summary
    st.subheader("📋 System Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Dimensions", "15")
        st.metric("Total Parameters", "37")
        st.metric("Biomarkers Used", "47")
    with col2:
        st.metric("Cancer Compartments", "6")
        st.metric("Immune Compartments", "2")
        st.metric("Microenvironment", "4")
        st.metric("Pharmacokinetics", "2")
        st.metric("Genetic/Metabolic", "2")
    
    st.info("""
    **Note:** All 37 parameters are derived from the 47-biomarker blood biomarkers. The system captures tumor growth, immune interactions, treatment effects, 
    resistance evolution, and microenvironmental factors in a personalized, patient-specific model.
    """)

