"""
fig2_selectivity.py
====================
Grouped horizontal bar chart comparing ortho vs para pathway metrics
for regioselectivity analysis of phenol OH• addition.

Primary figure — demonstrates para pathway superiority across all key metrics.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
metrics = [
    "RC binding energy\n(kcal mol⁻¹)",
    "TS barrier†\n(kcal mol⁻¹)",
    "Adduct ΔG\n(kcal mol⁻¹)",
    "NO₂• capture ΔG\n(kcal mol⁻¹)",
    "Overall ΔG\n(kcal mol⁻¹)",
]

ortho_values = [-2.26, +21.27, -19.14, -44.21, -63.33]
para_values  = [-7.14, +17.95, -22.96, -43.83, -66.80]

# Which metrics favour para (for annotation)
diff = [o - p for o, p in zip(ortho_values, para_values)]
# positive diff means ortho > para; for negative quantities, ortho > para = ortho less stable
favoured = []
for i, (o, p) in enumerate(zip(ortho_values, para_values)):
    if i == 1:  # TS barrier: lower is better
        favoured.append("Para" if p < o else "Ortho")
    elif i == 3:  # NO2 capture: ortho slightly more negative
        favoured.append("Ortho (marginal)")
    else:
        favoured.append("Para" if p < o else "Ortho")

# Colors
ORTHO_COLOR = "#2166AC"
PARA_COLOR  = "#B2182B"

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
n = len(metrics)
y = np.arange(n)
bar_height = 0.32
gap = 0.06

fig, ax = plt.subplots(figsize=(10, 6))

bars_ortho = ax.barh(
    y + bar_height / 2 + gap / 2,
    ortho_values,
    height=bar_height,
    color=ORTHO_COLOR,
    label="Ortho",
    alpha=0.88,
    edgecolor="white",
    linewidth=0.4,
)

bars_para = ax.barh(
    y - bar_height / 2 - gap / 2,
    para_values,
    height=bar_height,
    color=PARA_COLOR,
    label="Para",
    alpha=0.88,
    edgecolor="white",
    linewidth=0.4,
)

# Value labels
for bar, val in zip(bars_ortho, ortho_values):
    sign = "+" if val > 0 else ""
    x_text = val + 0.4 if val > 0 else val - 0.4
    ha = "left" if val > 0 else "right"
    ax.text(
        x_text,
        bar.get_y() + bar.get_height() / 2,
        f"{sign}{val:.2f}",
        ha=ha,
        va="center",
        fontsize=8.5,
        color=ORTHO_COLOR,
        fontweight="bold",
    )

for bar, val in zip(bars_para, para_values):
    sign = "+" if val > 0 else ""
    x_text = val + 0.4 if val > 0 else val - 0.4
    ha = "left" if val > 0 else "right"
    ax.text(
        x_text,
        bar.get_y() + bar.get_height() / 2,
        f"{sign}{val:.2f}",
        ha=ha,
        va="center",
        fontsize=8.5,
        color=PARA_COLOR,
        fontweight="bold",
    )

# Difference annotations on the right
x_annotation = max(max(ortho_values), max(para_values)) + 3.5
for i, (fav, d) in enumerate(zip(favoured, diff)):
    d_abs = abs(d)
    ax.text(
        x_annotation,
        y[i],
        f"Δ={d_abs:.2f}\n→ {fav}",
        ha="left",
        va="center",
        fontsize=7.5,
        color="gray",
    )

# Zero line
ax.axvline(0, color="black", linewidth=0.8)

# Axes
ax.set_yticks(y)
ax.set_yticklabels(metrics, fontsize=10)
ax.set_xlabel("Energy (kcal mol⁻¹)", fontsize=12)
ax.set_title(
    "Ortho vs Para Selectivity: OH• Addition to Phenol",
    fontsize=14,
    pad=10,
)
ax.tick_params(axis="x", labelsize=10)
ax.invert_yaxis()

# Extend x-axis to make room for annotations
current_xlim = ax.get_xlim()
ax.set_xlim(current_xlim[0] - 2, current_xlim[1] + 18)

# Legend
ax.legend(fontsize=10, frameon=False, loc="lower left")

# Summary annotation box
ax.text(
    current_xlim[1] + 14,
    n - 1,
    "Para pathway\nfavoured in\n4 of 5 metrics",
    ha="center",
    va="bottom",
    fontsize=9,
    color="#B2182B",
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF0F0", edgecolor="#B2182B", alpha=0.8),
)

# Footnote
fig.text(
    0.12, 0.01,
    "† TS barriers lack SP corrections; values are approximate (E+G_corr only)",
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
fig.savefig("figures/fig2_selectivity.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/fig2_selectivity.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved: figures/fig2_selectivity.png  figures/fig2_selectivity.pdf")
