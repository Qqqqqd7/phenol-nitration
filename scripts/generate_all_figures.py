"""
generate_all_figures.py
========================
Master script: generates all publication-ready figures for the
phenol nitration computational chemistry study.

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
    ("fig1_pes_diagram",           "Figure 1 — Dual-Pathway PES Diagram"),
    ("fig2_spin_density",          "Figure 2 — Spin Density Bar Chart"),
    ("fig3_reaction_thermodynamics", "Figure 3 — Reaction Thermodynamics"),
    ("fig4_selectivity_comparison","Figure 4 — Ortho vs Para Selectivity"),
]

GENERATED = []
FAILED    = []

print("=" * 60)
print("Generating all figures for phenol nitration study")
print("=" * 60)

for module_name, description in FIGURE_SCRIPTS:
    print(f"\n[{description}]")
    try:
        mod = importlib.import_module(module_name)
        # Re-run if already imported (e.g., interactive session)
        importlib.reload(mod)
        GENERATED.append(description)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        FAILED.append((description, str(exc)))

print("\n" + "=" * 60)
print(f"Summary: {len(GENERATED)} generated, {len(FAILED)} failed")
print("=" * 60)

if GENERATED:
    print("\nGenerated figures:")
    for desc in GENERATED:
        print(f"  ✓  {desc}")

if FAILED:
    print("\nFailed:")
    for desc, err in FAILED:
        print(f"  ✗  {desc}: {err}")
    sys.exit(1)

print(f"\nAll figures saved to: {figures_dir}")
