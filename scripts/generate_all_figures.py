"""
generate_all_figures.py
========================
Master script: generates all publication-ready figures for the
phenol nitration computational chemistry study.

Figure hierarchy:
  Primary figures   — fig1 (PES), fig2 (selectivity comparison)
  Supporting figure — fig3 (reaction thermodynamics)
  Supplementary     — figS1 (spin density)

Usage
-----
    python scripts/generate_all_figures.py

or from the repo root:

    python -m scripts.generate_all_figures

All output goes to the figures/ directory (created automatically).
"""

import importlib
import os
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.dirname(SCRIPTS_DIR)

# Ensure figures/ exists relative to repo root
figures_dir = os.path.join(REPO_ROOT, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Change to repo root so relative paths in sub-scripts resolve correctly
os.chdir(REPO_ROOT)

# Add scripts/ to path so we can import sub-scripts as modules
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

FIGURE_SCRIPTS = [
    ("fig1_pes_diagram",           "primary",       "Figure 1 — PES Diagram (Ortho vs Para OH• Addition)"),
    ("fig2_selectivity",           "primary",       "Figure 2 — Ortho vs Para Selectivity Comparison"),
    ("fig3_reaction_thermodynamics", "supporting",  "Figure 3 — Reaction Thermodynamics"),
    ("figS1_spin_density",         "supplementary", "Figure S1 — Spin Density Distribution"),
]

GENERATED = []
FAILED    = []

print("=" * 60)
print("Generating all figures for phenol nitration study")
print("=" * 60)

for module_name, _category, description in FIGURE_SCRIPTS:
    print(f"\n[{description}]")
    try:
        mod = importlib.import_module(module_name)
        # Re-run if already imported (e.g., interactive session)
        importlib.reload(mod)
        GENERATED.append((_category, description))
    except Exception as exc:
        print(f"  ERROR: {exc}")
        FAILED.append((description, str(exc)))

print("\n" + "=" * 60)
print(f"Summary: {len(GENERATED)} generated, {len(FAILED)} failed")
print("=" * 60)

if GENERATED:
    primary = [d for c, d in GENERATED if c == "primary"]
    supporting = [d for c, d in GENERATED if c == "supporting"]
    supplementary = [d for c, d in GENERATED if c == "supplementary"]

    if primary:
        print("\nPrimary figures:")
        for desc in primary:
            print(f"  ✓  {desc}")
    if supporting:
        print("\nSupporting figures:")
        for desc in supporting:
            print(f"  ✓  {desc}")
    if supplementary:
        print("\nSupplementary figures:")
        for desc in supplementary:
            print(f"  ✓  {desc}")

if FAILED:
    print("\nFailed:")
    for desc, err in FAILED:
        print(f"  ✗  {desc}: {err}")
    sys.exit(1)

print(f"\nAll figures saved to: {figures_dir}")
