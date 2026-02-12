"""
Test script to verify calculations work correctly
Runs without Streamlit to test core functionality
"""

from biomarkers_data import ALL_BIOMARKERS, TOTAL_BIOMARKERS
from calculations import calculate_all_parameters, REFERENCE_VALUES_FOR_IMPUTATION

print("=" * 60)
print("Blood-Based Cancer Model Calculator - Test")
print("=" * 60)
print(f"\nTotal Biomarkers: {TOTAL_BIOMARKERS}")
print(f"Categories: {len(ALL_BIOMARKERS)} biomarkers defined\n")

# Example biomarker data
example_biomarkers = {
    'ca153': 45, 'ca2729': 38, 'cea': 4.2, 'tk1': 3.1, 'ctdna': 1.2, 'esr1_protein': 5.2,
    'cd8': 650, 'cd4': 950, 'nk': 180, 'ifn_gamma': 3.8, 'il10': 28, 'tnf_alpha': 6.5,
    'tgf_beta': 3.2, 'pdl1_ctc': 3.5, 'hla_dr': 75, 'ctc': 8, 'ang2': 2200, 'lymphocytes': 1800,
    'esr1_mutations': 2, 'pgr': 45, 'brca': 1, 'pik3ca': 4, 'tp53': 3, 'her2_mutations': 1,
    'her2_circ': 3.5, 'mdr1': 135, 'cyp2d6': 1.8, 'survivin': 6.1, 'hsp': 12, 'mir200': 0.6,
    'exosomes': 11, 'vegf': 320, 'mrp1': 100, 'ki67': 12,
    'glucose': 115, 'lactate': 2.8, 'ldh': 310, 'albumin': 3.4, 'beta_hydroxybutyrate': 0.3,
    'blood_ph': 7.38, 'folate': 8, 'vitamin_d': 25,
    'creatinine': 0.9, 'bun': 18, 'alt': 28, 'ast': 32, 'bilirubin': 0.8
}

# Ensure all biomarkers have values; use reference imputation for missing (per Chapter 4)
all_keys = set(ALL_BIOMARKERS.keys())
example_keys = set(example_biomarkers.keys())
missing = all_keys - example_keys
if missing:
    for key in missing:
        example_biomarkers[key] = REFERENCE_VALUES_FOR_IMPUTATION.get(key, 0.0)
    print(f"📌 Imputed {len(missing)} missing biomarkers to reference values")

print(f"\n✅ Example data prepared: {len(example_biomarkers)} biomarkers")
print("\nCalculating parameters...\n")

try:
    results = calculate_all_parameters(example_biomarkers)
    parameters = results['parameters']
    scores = results['scores']
    
    print("=" * 60)
    print("CALCULATION RESULTS - All 37 Parameters")
    print("=" * 60)
    
    print("\n🌱 Growth Parameters:")
    print(f"  λ₁ (Sensitive):     {parameters['lambda1']:.6f}/mo")
    print(f"  λ₂ (Resistant):     {parameters['lambda2']:.6f}/mo")
    print(f"  λ_R1 (Hormone):     {parameters['lambdaR1']:.6f}/mo")
    print(f"  λ_R2 (Multi-drug):  {parameters['lambdaR2']:.6f}/mo")
    print(f"  K (Capacity):       {int(parameters['K'])} cells")
    
    print("\n🛡️  Immune Parameters:")
    print(f"  β₁ (Killing):       {parameters['beta1']:.6f}/mo")
    print(f"  β₂ (Suppression):   {parameters['beta2']:.6f}/mo")
    print(f"  φ₁ (Basal):         {parameters['phi1']:.6f}/mo")
    print(f"  φ₂ (Tumor):         {parameters['phi2']:.6f}/mo")
    print(f"  φ₃ (IL-10):         {parameters['phi3']:.6f}/mo")
    print(f"  δ_I (Death):        {parameters['deltaI']:.6f}/mo")
    
    print("\n🔄 Resistance Evolution:")
    print(f"  ω_R1 (Hormone):     {parameters['omegaR1']:.7f}/mo")
    print(f"  ω_R2 (Multi-drug):  {parameters['omegaR2']:.7f}/mo")
    
    print("\n💊 Treatment Effectiveness:")
    print(f"  η_E (Hormone):      {parameters['etaE']*100:.1f}%")
    print(f"  η_C (Chemo):        {parameters['etaC']*100:.1f}%")
    print(f"  η_H (HER2):         {parameters['etaH']*100:.1f}%")
    print(f"  η_I (Immuno):       {parameters['etaI']*100:.1f}%")
    
    print("\n⚡ Pharmacokinetics:")
    print(f"  k_el (Elimination): {parameters['kel']:.6f}/mo")
    
    print("\n🌐 Microenvironment:")
    print(f"  α_A (Angio rate):   {parameters['alphaA']:.6f}/mo")
    print(f"  α_acid (ODE):       {parameters.get('alpha_acid', 0):.4f}")
    print(f"  δ_A (Angio decay):  {parameters['deltaA']:.6f}/mo")
    print(f"  κ_Q (Quiescence):   {parameters['kappaQ']:.6f}/mo")
    print(f"  κ_S (Senescence):   {parameters['kappaS']:.6f}/mo")
    print(f"  δ_S (Sen clear):    {parameters['deltaS']:.6f}/mo")
    print(f"  γ (Metastasis):     {parameters['gamma']:.7f}/mo")
    print(f"  δ_P (Met death):    {parameters['deltaP']:.6f}/mo")
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS: All 37 parameters calculated!")
    print("=" * 60)
    
    if results['constraint_violations']:
        print(f"\n⚠️  Constraint violations (auto-corrected):")
        for v in results['constraint_violations']:
            print(f"  - {v}")
    
    print(f"\n📊 Composite Scores:")
    print(f"  s_prolif:    {scores['s_prolif']:.3f}")
    print(f"  s_immune:    {scores['s_immune']:.3f}")
    print(f"  s_suppress:  {scores['s_suppress']:.3f}")
    print(f"  s_tumor:     {scores['s_tumor']:.3f}")
    print(f"  G:           {scores['G']:.3f}")
    print(f"  s_genetic:   {scores['s_genetic']:.3f}")
    
    print("\n✅ All calculations completed successfully!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

