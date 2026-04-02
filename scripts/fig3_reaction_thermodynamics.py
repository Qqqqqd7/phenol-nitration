"""
fig3_reaction_thermodynamics.py
================================
Horizontal grouped bar chart of ΔG and ΔH (kcal/mol) for all
relevant reactions in the phenol nitration mechanism.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Data  (NaN = not available)
# ---------------------------------------------------------------------------
reactions = [
    "H-abstraction\n(PhOH + OH• → PhO• + H₂O)",
    "Ring addition ortho\n(PhOH + OH• → o-OHCHD)",
    "Ring addition para\n(PhOH + OH• → p-OHCHD)",
    "NO₂• capture ortho\n(o-OHCHD + NO₂• → oNP + H₂O)",
    "NO₂• capture para\n(p-OHCHD + NO₂• → pNP + H₂O)",
    "Overall ortho\n(PhOH + OH• + NO₂• → oNP + H₂O)",
    "Overall para\n(PhOH + OH• + NO₂• → pNP + H₂O)",
]

dG_values = [-41.07, -19.14, -22.96, -44.21, -43.83, -63.33, -66.80]
dH_values = [-39.53, -28.48, -28.66,    None,   None,   None,   None]

# Colors
DG_COLOR = "#1A6FAB"   # darker blue
DH_COLOR = "#7BBBE8"   # lighter blue

# ---------------------------------------------------------------------------
# Font
# ---------------------------------------------------------------------------
import matplotlib.font_manager as fm

def _get_serif_font():
    for name in ("Times New Roman", "DejaVu Serif"):
        try:
            path = fm.findfont(fm.FontProperties(family=name), fallback_to_default=False)
            if path:
                return name
        except Exception:
            pass
    return "serif"

FONT = _get_serif_font()
plt.rcParams.update({
    "font.family": FONT,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
n = len(reactions)
y = np.arange(n)
bar_height = 0.35
gap = 0.04

fig, ax = plt.subplots(figsize=(10, 7))

# Draw ΔG bars
bars_dg = ax.barh(
    y + bar_height / 2 + gap / 2,
    dG_values,
    height=bar_height,
    color=DG_COLOR,
    label="ΔG (kcal mol⁻¹)",
    edgecolor="white",
    linewidth=0.4,
)

# Draw ΔH bars where available
dH_plot = [v if v is not None else 0 for v in dH_values]
bars_dh = ax.barh(
    y - bar_height / 2 - gap / 2,
    dH_plot,
    height=bar_height,
    color=DH_COLOR,
    label="ΔH (kcal mol⁻¹)",
    edgecolor="white",
    linewidth=0.4,
)

# Hatch bars where ΔH is unavailable to indicate N/A
for i, dh in enumerate(dH_values):
    if dh is None:
        bars_dh[i].set_visible(False)

# Value labels at bar ends
for i, (bar, val) in enumerate(zip(bars_dg, dG_values)):
    ax.text(
        val - 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.2f}",
        ha="right",
        va="center",
        fontsize=8.5,
        color="white",
        fontweight="bold",
    )

for i, (bar, val) in enumerate(zip(bars_dh, dH_values)):
    if val is not None:
        ax.text(
            val - 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}",
            ha="right",
            va="center",
            fontsize=8.5,
            color="white",
            fontweight="bold",
        )

# Zero line
ax.axvline(0, color="black", linewidth=0.8)

# Axes
ax.set_yticks(y)
ax.set_yticklabels(reactions, fontsize=9.5)
ax.set_xlabel("Energy (kcal mol⁻¹)", fontsize=12)
ax.set_title(
    "Reaction Thermodynamics: Phenol Nitration Pathway",
    fontsize=14,
    pad=10,
)
ax.tick_params(axis="x", labelsize=10)
ax.invert_yaxis()  # top reaction first

# Legend
ax.legend(fontsize=10, frameon=False, loc="lower right")

# Note for N/A
fig.text(
    0.12, 0.01,
    "ΔH not available for NO₂• capture and overall reactions",
    fontsize=8,
    color="gray",
    style="italic",
)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")
plt.tight_layout(rect=[0, 0.04, 1, 1])

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/fig3_reaction_thermo.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/fig3_reaction_thermo.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved: figures/fig3_reaction_thermo.png  figures/fig3_reaction_thermo.pdf")
