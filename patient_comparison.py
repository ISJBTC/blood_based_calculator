"""
Patient Comparison Module
Scientific longitudinal comparison of biomarker readings with clinical interpretation.
"""

from typing import Dict, List, Tuple, Optional
from biomarkers_data import ALL_BIOMARKERS

# Clinical interpretation: direction of change that indicates improvement
# "lower_better": decrease = improvement (e.g. tumor markers, lactate)
# "higher_better": increase = improvement (e.g. CD8, albumin)
# "near_normal": optimal near reference (e.g. glucose 95)
DIRECTION = {
    "lower_better": [
        "ca153", "ca2729", "cea", "tk1", "ctdna", "ctc", "exosomes",
        "il10", "tgf_beta", "pdl1_ctc",
        "esr1_mutations", "pgr", "brca", "pik3ca", "tp53", "her2_mutations",
        "mdr1", "mrp1", "survivin", "hsp", "mir200", "vegf", "ki67",
        "lactate", "ldh", "beta_hydroxybutyrate",
        "creatinine", "bun", "alt", "ast", "bilirubin",
    ],
    "higher_better": [
        "cd8", "cd4", "nk", "ifn_gamma", "hla_dr", "lymphocytes",
        "esr1_protein",  # receptor presence for hormone therapy
        "albumin", "vitamin_d", "folate",
    ],
    "near_normal": ["glucose", "blood_ph", "tnf_alpha", "ang2", "her2_circ", "cyp2d6"],
}


def _get_direction(key: str) -> str:
    for d, keys in DIRECTION.items():
        if key in keys:
            return d
    return "lower_better"


def compute_comparison(
    current: Dict[str, float],
    previous: Dict[str, float],
    biomarkers_to_show: Optional[List[str]] = None,
) -> List[Dict]:
    """
    Compare current vs previous biomarker readings.
    Returns list of dicts with: key, name, current, previous, delta, pct_change, trend, interpretation.
    """
    from biomarkers_data import ALL_BIOMARKERS

    keys = biomarkers_to_show or list(ALL_BIOMARKERS.keys())
    rows = []

    for key in keys:
        if key not in ALL_BIOMARKERS:
            continue
        cur = float(current.get(key, 0) or 0)
        prev = float(previous.get(key, 0) or 0)

        delta = cur - prev
        if prev != 0:
            pct = 100 * (delta / prev)
        else:
            pct = 100.0 if cur != 0 else 0.0

        direction = _get_direction(key)
        info = ALL_BIOMARKERS[key]

        # Clinical interpretation
        if abs(delta) < 1e-6:
            trend = "unchanged"
            interpretation = "No significant change"
        else:
            if direction == "lower_better":
                if delta < 0:
                    trend = "improved"
                    interpretation = "Decrease (favorable)"
                else:
                    trend = "worsened"
                    interpretation = "Increase (unfavorable)"
            elif direction == "higher_better":
                if delta > 0:
                    trend = "improved"
                    interpretation = "Increase (favorable)"
                else:
                    trend = "worsened"
                    interpretation = "Decrease (unfavorable)"
            else:  # near_normal
                # For glucose, 95 is target; for blood_ph, 7.4
                if key == "glucose":
                    cur_dist = abs(cur - 95)
                    prev_dist = abs(prev - 95)
                    if cur_dist < prev_dist:
                        trend = "improved"
                        interpretation = "Closer to target (95 mg/dL)"
                    else:
                        trend = "worsened"
                        interpretation = "Further from target"
                elif key == "blood_ph":
                    cur_dist = abs(cur - 7.4)
                    prev_dist = abs(prev - 7.4)
                    if cur_dist < prev_dist:
                        trend = "improved"
                        interpretation = "Closer to normal (7.35–7.45)"
                    else:
                        trend = "worsened"
                        interpretation = "Further from normal"
                else:
                    trend = "changed"
                    interpretation = f"Δ = {delta:+.2f}"

        rows.append({
            "key": key,
            "name": info["name"],
            "unit": info["unit"],
            "current": cur,
            "previous": prev,
            "delta": delta,
            "pct_change": pct,
            "trend": trend,
            "interpretation": interpretation,
        })

    return rows


def get_summary_stats(rows: List[Dict]) -> Dict[str, int]:
    """Count improved, worsened, unchanged."""
    counts = {"improved": 0, "worsened": 0, "unchanged": 0, "changed": 0}
    for r in rows:
        t = r.get("trend", "changed")
        if t in counts:
            counts[t] += 1
        else:
            counts["changed"] += 1
    return counts
