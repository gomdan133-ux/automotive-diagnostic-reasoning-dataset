# Automotive Diagnostic Reasoning Dataset

A hand-written dataset of real-world automotive diagnostic cases, structured for training and evaluating AI models on **step-by-step technical reasoning**.

Each case goes from the customer complaint to the confirmed root cause, the way a working technician actually diagnoses a vehicle. Each one also records the **common wrong answers**: the parts-swapping guesses an AI model (or an inexperienced tech) is likely to make, and why they are wrong.

Written by an ASE-certified (Brakes) mobile mechanic based in Miami, FL.

## Why this exists

Large language models often "diagnose" cars by pattern-matching a trouble code to the most common part replacement (P0420 → "replace the catalytic converter"). Real diagnosis means testing, ruling things out, and finding the root cause. This dataset is built to teach and test that reasoning.

## What's in each case

| Field | Description |
|---|---|
| `id` | Unique case ID |
| `system` | Vehicle system (brakes, cooling, ignition, ...) |
| `vehicle` | Year, make, model, engine |
| `complaint` | What the customer reports |
| `dtcs` | Diagnostic trouble codes (may be empty) |
| `observations` | Measurements and findings from inspection and live data |
| `diagnostic_steps` | Ordered reasoning steps from complaint to root cause |
| `root_cause` | The confirmed cause |
| `fix` | The correct repair |
| `common_wrong_answers` | Likely wrong conclusions and why each is wrong |
| `safety_notes` | Safety items for the technician or customer |
| `difficulty` | easy / medium / hard |

## Example (shortened)

```json
{
  "id": "DIAG-002",
  "dtcs": ["P0420"],
  "root_cause": "Exhaust leak (cracked flex pipe) upstream of the downstream O2 sensor making the cat appear inefficient.",
  "common_wrong_answers": [
    {"answer": "Replace the catalytic converter immediately.",
     "why_wrong": "An exhaust leak ahead of the rear sensor can mimic a failed cat; leaks must be ruled out first."}
  ]
}
```

## Coverage

12 cases across ignition, fuel/air, exhaust/emissions, cooling, brakes, ABS, starting/charging, and engine management.

## Usage

```bash
python scripts/validate_and_export.py
```

This checks every case against the schema and writes `data/cases.jsonl` (one case per line), the standard format for fine-tuning and evaluation pipelines.

## Possible uses

- Supervised fine-tuning data for technical reasoning
- An evaluation set: give a model the complaint, DTCs and observations, then compare its answer to `root_cause` and check whether it falls into a `common_wrong_answers` trap
- Rubric source for grading model explanations

## Notes

Values such as specs and tolerances are typical figures for illustration. Always use the manufacturer's service information for a specific vehicle.

## License

MIT
