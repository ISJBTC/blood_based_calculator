"""
Patient Data Module
Scientific storage and retrieval of biomarker records for longitudinal comparison.
File-based JSON storage for persistence, portability, and reproducibility.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Storage directory (relative to project root)
PATIENT_DATA_DIR = Path(__file__).parent / "patient_data"
PATIENT_DATA_DIR.mkdir(exist_ok=True)


def _sanitize_id(patient_id: str) -> str:
    """Create filesystem-safe identifier."""
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in patient_id.strip())[:64]


def save_patient(
    biomarkers: Dict[str, float],
    patient_id: str = "",
    patient_name: str = "",
    notes: str = "",
    panel_type: str = "full",
) -> str:
    """
    Save patient biomarker data with metadata.
    Returns the stored record ID.
    """
    if not patient_id and not patient_name:
        patient_id = datetime.now().strftime("patient_%Y%m%d_%H%M%S")
    elif not patient_id:
        patient_id = _sanitize_id(patient_name) + "_" + datetime.now().strftime("%Y%m%d_%H%M")
    else:
        patient_id = _sanitize_id(patient_id)

    record = {
        "patient_id": patient_id,
        "patient_name": patient_name or patient_id,
        "date": datetime.now().isoformat(),
        "notes": notes,
        "panel_type": panel_type,
        "biomarkers": biomarkers,
    }

    filepath = PATIENT_DATA_DIR / f"{patient_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return patient_id


def load_patient(patient_id: str) -> Optional[Dict[str, Any]]:
    """Load a patient record by ID. Returns None if not found."""
    filepath = PATIENT_DATA_DIR / f"{_sanitize_id(patient_id)}.json"
    if not filepath.exists():
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_patients() -> List[Dict[str, Any]]:
    """List all saved patients (id, name, date) sorted by date descending."""
    records = []
    for f in PATIENT_DATA_DIR.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                r = json.load(fp)
                records.append({
                    "patient_id": r.get("patient_id", f.stem),
                    "patient_name": r.get("patient_name", f.stem),
                    "date": r.get("date", ""),
                    "notes": r.get("notes", "")[:50],
                })
        except (json.JSONDecodeError, IOError):
            continue
    records.sort(key=lambda x: x.get("date", ""), reverse=True)
    return records


def delete_patient(patient_id: str) -> bool:
    """Delete a patient record. Returns True if deleted."""
    filepath = PATIENT_DATA_DIR / f"{_sanitize_id(patient_id)}.json"
    if filepath.exists():
        filepath.unlink()
        return True
    return False


def export_to_json(record: Dict[str, Any]) -> str:
    """Serialize a patient record to JSON string for download."""
    return json.dumps(record, indent=2, ensure_ascii=False)


def import_from_json(json_str: str) -> Optional[Dict[str, Any]]:
    """Parse JSON string into a patient record. Returns None if invalid."""
    try:
        r = json.loads(json_str)
        if "biomarkers" in r:
            return r
        return None
    except json.JSONDecodeError:
        return None


def load_record_for_import(record: Dict[str, Any]) -> Dict[str, float]:
    """Extract biomarkers dict from a loaded/imported record."""
    return record.get("biomarkers", {})
