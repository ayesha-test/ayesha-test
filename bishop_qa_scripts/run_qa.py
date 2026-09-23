from qa_checks import run_all
from sample_data import SEGMENTS

failures = run_all(SEGMENTS)

if not failures:
    print("All checks passed.")
else:
    print(f"{len(failures)} issue(s) found:\n")
    for idx, rule, reason in failures:
        print(f"  segment {idx:>2} [{rule}]  {reason}")
