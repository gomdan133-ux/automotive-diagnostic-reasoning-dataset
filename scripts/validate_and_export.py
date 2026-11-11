"""Validate the diagnostic cases and export them to JSONL.

Usage:
    python scripts/validate_and_export.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "cases.json"
OUT = ROOT / "data" / "cases.jsonl"

REQUIRED = {
    "id": str,
    "system": str,
    "vehicle": dict,
    "complaint": str,
    "dtcs": list,
    "observations": list,
    "diagnostic_steps": list,
    "root_cause": str,
    "fix": str,
    "common_wrong_answers": list,
    "safety_notes": list,
    "difficulty": str,
}
DIFFICULTIES = {"easy", "medium", "hard"}


def validate(cases):
    errors = []
    seen = set()
    for i, case in enumerate(cases):
        cid = case.get("id", f"index {i}")
        for field, ftype in REQUIRED.items():
            if field not in case:
                errors.append(f"{cid}: missing '{field}'")
            elif not isinstance(case[field], ftype):
                errors.append(f"{cid}: '{field}' should be {ftype.__name__}")
        if cid in seen:
            errors.append(f"{cid}: duplicate id")
        seen.add(cid)
        if case.get("difficulty") not in DIFFICULTIES:
            errors.append(f"{cid}: difficulty must be one of {sorted(DIFFICULTIES)}")
        if len(case.get("diagnostic_steps", [])) < 3:
            errors.append(f"{cid}: needs at least 3 diagnostic steps")
        for w in case.get("common_wrong_answers", []):
            if not {"answer", "why_wrong"} <= set(w):
                errors.append(f"{cid}: wrong answers need 'answer' and 'why_wrong'")
    return errors


def main():
    cases = json.loads(SRC.read_text(encoding="utf-8"))
    errors = validate(cases)
    if errors:
        print("Validation failed:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    with OUT.open("w", encoding="utf-8") as f:
        for case in cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    systems = sorted({c["system"] for c in cases})
    print(f"OK: {len(cases)} cases valid -> {OUT.relative_to(ROOT)}")
    print("Systems covered:", ", ".join(systems))


if __name__ == "__main__":
    main()
