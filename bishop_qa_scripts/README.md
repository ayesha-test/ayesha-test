# Project Bishop — Automated QA Checks

Proof-of-concept scripts for the fully automated checks identified in the
error catalog and automation split table (catalog IDs: S2, S3, S4, C1, C2,
C10, C12). Plain Python, no dependencies.

## Files

- `qa_checks.py` — one function per rule, each returns a list of failures
- `sample_data.py` — 9 mock segments (Encord-shaped), mixing clean and
  deliberately broken entries
- `run_qa.py` — runs every check against the sample data and prints a report

## Run it

```
python3 run_qa.py
```

## Sample output

Run against the mock data in `sample_data.py`, the script catches every
planted error and raises zero false positives on the clean segments:

```
8 issue(s) found:

  segment  1 [S2]  gap/overlap between segment 1 (ends 1.35) and 2 (starts 1.5)
  segment  1 [S3]  segment length 0.150s is below 0.2s minimum
  segment  2 [C1]  caption does not start with a capital letter
  segment  4 [C2]  label 'idle' has wrong case/whitespace
  segment  5 [S4]  IDLE segment is only 0.30s, below the 1.0s threshold
  segment  6 [C10]  caption uses banned word 'cloth' (use towel or blanket instead)
  segment  7 [C12]  caption uses a non-approved vague noun; approved fallbacks are ['container', 'garment', 'linen', 'utensil']
  segment  8 [C1]  caption ends with a period
```

| Segment | Rule | Issue |
|---|---|---|
| 1 | S3 | Segment 0.15s long, below the 0.2s minimum |
| 1→2 | S2 | Gap between segments (1.35s → 1.5s) |
| 2 | C1 | Caption starts lowercase |
| 4 | C2 | Label written as `idle`, not exact literal `IDLE` |
| 5 | S4 | Labeled IDLE but only 0.3s, below the 1s threshold |
| 6 | C10 | Banned word "cloth" used instead of towel/blanket |
| 7 | C12 | Vague noun "item" used instead of an approved fallback |
| 8 | C1 | Caption ends with a trailing period |

Segments that were actually correct (e.g. segment 0, segment 3) produced no
output, confirming the checks don't false-positive on valid data.

## Not covered here

These are the "fully automated" checks only. Hybrid checks (script flags,
human decides — e.g. C15 rubber-stamped suggestions, C7 landmark vs target
confusion) and manual-only checks are listed separately in the automation
split table.
