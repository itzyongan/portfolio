#!/usr/bin/env python3
"""Apply alignment fixes to index.html. Run in repo root: python3 apply_fixes.py"""
import sys

PATH = "index.html"
src = open(PATH, encoding="utf-8").read()

# (old, new, expected count)
EDITS = [
    # 1. Nav overflow at 561-615px: raise mobile breakpoint 560 -> 640
    ("@media (max-width: 560px)", "@media (max-width: 640px)", 2),
    ("@media (min-width: 561px)", "@media (min-width: 641px)", 2),
    ("matchMedia('(min-width: 561px)')", "matchMedia('(min-width: 641px)')", 1),
    ("innerWidth > 560", "innerWidth > 640", 1),
    # 2. Logo 52.4px tall vs 52px toggle/links: fix to 52px
    (
        "justify-self: start; padding: 13px 20px; will-change: transform;",
        "justify-self: start; padding: 0 20px; line-height: 52px; will-change: transform;",
        1,
    ),
    # 3. h1 nowrap overflow on 320px phones
    ("clamp(2rem, 5.2vw, 3rem)", "clamp(1.7rem, 5.2vw, 3rem)", 1),
    (
        "    .eyebrow { font-size: .8rem;",
        "    .hero > div { min-width: 0; }\n    .eyebrow { font-size: .8rem;",
        1,
    ),
]

for old, new, n in EDITS:
    found = src.count(old)
    if found != n:
        sys.exit(f"ABORT: expected {n}x, found {found}x: {old!r}")
    src = src.replace(old, new)

open(PATH, "w", encoding="utf-8").write(src)
print("done:", len(EDITS), "edits applied")
