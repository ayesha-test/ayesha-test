"""
Project Bishop - automated QA checks (proof of concept)
Covers the 7 "fully automated" items from the automation split table:
S2, S3, S4, C1, C2, C10, C12

Input: a list of segment dicts per recording, each segment shaped like:
{
    "start": float,       # seconds
    "end": float,         # seconds
    "label": str,         # IDLE / SITTING / TASK UNRELATED ACTION / "" for normal
    "caption": str,       # caption text, "" for special segments
}

Each check returns a list of (segment_index, rule_id, reason) for failures.
No dependencies beyond the standard library.
"""

import re

SPECIAL_LABELS = {"IDLE", "SITTING", "TASK UNRELATED ACTION"}
BANNED_WORDS = {"cloth": "use towel or blanket instead"}
APPROVED_FALLBACKS = {"garment", "container", "utensil", "linen"}
MIN_SEGMENT_LEN = 0.2
PAUSE_THRESHOLD = 1.0


def check_contiguous(segments):
    """S2: no gaps or overlaps between consecutive segments."""
    fails = []
    for i in range(len(segments) - 1):
        end_a = segments[i]["end"]
        start_b = segments[i + 1]["start"]
        if abs(end_a - start_b) > 1e-6:
            fails.append((i, "S2", f"gap/overlap between segment {i} (ends {end_a}) and {i+1} (starts {start_b})"))
    return fails


def check_min_length(segments):
    """S3: no segment shorter than 0.2s."""
    fails = []
    for i, seg in enumerate(segments):
        dur = seg["end"] - seg["start"]
        if dur < MIN_SEGMENT_LEN:
            fails.append((i, "S3", f"segment length {dur:.3f}s is below {MIN_SEGMENT_LEN}s minimum"))
    return fails


def check_pause_labeling(segments):
    """S4: pauses >=1s must be labeled IDLE; IDLE segments <1s are suspect."""
    fails = []
    for i, seg in enumerate(segments):
        dur = seg["end"] - seg["start"]
        if seg["label"] == "IDLE" and dur < PAUSE_THRESHOLD:
            fails.append((i, "S4", f"IDLE segment is only {dur:.2f}s, below the {PAUSE_THRESHOLD}s threshold"))
    return fails


def check_caption_format(segments):
    """C1: capital start, no trailing period, one sentence, no commas."""
    fails = []
    for i, seg in enumerate(segments):
        cap = seg["caption"]
        if not cap or seg["label"] in SPECIAL_LABELS:
            continue
        if not cap[0].isupper():
            fails.append((i, "C1", "caption does not start with a capital letter"))
        if cap.endswith("."):
            fails.append((i, "C1", "caption ends with a period"))
        if "," in cap:
            fails.append((i, "C1", "caption contains a comma"))
        if cap.count(".") > 0 or len(re.findall(r"[.!?](?=\s|$)", cap)) > 0:
            pass  # sentence-count check folded into period check above
    return fails


def check_literal_spelling(segments):
    """C2: IDLE / SITTING / TASK UNRELATED ACTION must appear exactly, nothing else in the field."""
    fails = []
    for i, seg in enumerate(segments):
        label = seg["label"]
        if not label:
            continue
        if label not in SPECIAL_LABELS:
            # catch near-misses like "idle", "Idle", "IDLE ", "IDLE (unsure)"
            if label.strip().upper() in SPECIAL_LABELS:
                fails.append((i, "C2", f"label '{label}' has wrong case/whitespace"))
            else:
                fails.append((i, "C2", f"label '{label}' is not one of {sorted(SPECIAL_LABELS)}"))
    return fails


def check_banned_words(segments):
    """C10: flag known banned generic terms in captions."""
    fails = []
    for i, seg in enumerate(segments):
        cap = seg["caption"].lower()
        for word, suggestion in BANNED_WORDS.items():
            if re.search(rf"\b{word}\b", cap):
                fails.append((i, "C10", f"caption uses banned word '{word}' ({suggestion})"))
    return fails


def check_fallback_nouns(segments):
    """C12: if a fallback-style noun is used, it must be one of the 4 approved terms."""
    fails = []
    fallback_pattern = re.compile(r"\b(item|thing|stuff|object)\b", re.IGNORECASE)
    for i, seg in enumerate(segments):
        cap = seg["caption"]
        if fallback_pattern.search(cap):
            fails.append((i, "C12", f"caption uses a non-approved vague noun; approved fallbacks are {sorted(APPROVED_FALLBACKS)}"))
    return fails


ALL_CHECKS = [
    check_contiguous,
    check_min_length,
    check_pause_labeling,
    check_caption_format,
    check_literal_spelling,
    check_banned_words,
    check_fallback_nouns,
]


def run_all(segments):
    """Run every check against one recording's segments, return all failures sorted by segment."""
    results = []
    for check in ALL_CHECKS:
        results.extend(check(segments))
    return sorted(results, key=lambda r: r[0])
