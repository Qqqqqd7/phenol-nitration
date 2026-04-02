"""
figS1_spin_density.py
======================
Grouped bar chart of Mulliken spin densities at key atomic sites
for four key radical intermediates in the phenol nitration mechanism.

Supplementary figure — supporting data for regioselectivity of NO₂• attack.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
sites = ["O", "Ipso-C", "Ortho-C (max)", "Para-C"]

spin_data = {
    "PhO•":      [0.377, -0.061,  0.274,  0.396],
    "PhOH•⁺":   [0.160,  0.250,  0.133,  0.455],
    "o-OHCHD":  [0.048,  0.347,  0.181, -0.158],
    "p-OHCHD":  [0.367, -0.026,  0.273,  0.396],
}

species_names = list(spin_data.keys())
n_species = len(species_names)
n_sites   = len(sites)

# Colorblind-friendly palette
COLORS = ["#2166AC", "#B2182B", "#4DAC26", "#E08214"]  # blue, red, green, orange

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
fig, ax = plt.subplots(figsize=(7, 4.5))

x = np.arange(n_sites)
total_width = 0.72
bar_width = total_width / n_species
offsets = np.linspace(
    -(total_width / 2) + bar_width / 2,
     (total_width / 2) - bar_width / 2,
    n_species,
)

for i, (species, values) in enumerate(spin_data.items()):
    bars = ax.bar(
        x + offsets[i],
        values,
        width=bar_width,
        color=COLORS[i],
        label=species,
        edgecolor="white",
        linewidth=0.5,
        alpha=0.88,
    )

# Zero line
ax.axhline(0, color="black", linewidth=0.8, linestyle="-")

# Axes
ax.set_xticks(x)
ax.set_xticklabels(sites, fontsize=10)
ax.set_ylabel("Mulliken Spin Density", fontsize=12)
ax.set_xlabel("Atomic Site", fontsize=12)
ax.set_title(
    "Fig. S1 — Spin Density Distribution in Key Radical Intermediates\n"
    "Supplementary data supporting regioselectivity of NO₂• attack",
    fontsize=12,
    pad=10,
)
ax.tick_params(axis="both", labelsize=10)

# Legend
ax.legend(
    fontsize=9,
    frameon=False,
    loc="upper right",
    ncol=2,
)

# Value annotations on bars (skip very small bars for clarity)
for i, (species, values) in enumerate(spin_data.items()):
    for j, v in enumerate(values):
        if abs(v) >= 0.06:
            y_pos = v + 0.012 if v >= 0 else v - 0.022
            va = "bottom" if v >= 0 else "top"
            ax.text(
                x[j] + offsets[i],
                y_pos,
                f"{v:+.3f}",
                ha="center",
                va=va,
                fontsize=7,
                color="black",
            )

fig.patch.set_facecolor("white")
ax.set_facecolor("white")
plt.tight_layout()

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/figS1_spin_density.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/figS1_spin_density.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved: figures/figS1_spin_density.png  figures/figS1_spin_density.pdf")
