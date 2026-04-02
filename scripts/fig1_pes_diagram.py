"""
fig1_pes_diagram.py
===================
Dual-Pathway Potential Energy Surface Diagram for phenol nitration via
OH• radical addition, showing ortho and para pathways on the same axes.

Both pathways reference PhOH + OH• + NO₂• = 0.00 kcal/mol.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
# X positions for each stage (0–4)
x_positions = [0, 1, 2, 3, 4]
x_labels = [
    "PhOH + OH•\n+ NO₂•",
    "RC\n+ NO₂•",
    "TS\n+ NO₂•",
    "OHCHD Adduct\n+ NO₂•",
    "NP + H₂O",
]

# ΔG (kcal/mol) relative to PhOH + OH• + NO₂• = 0.00
ortho_dG = [0.00, -2.26, +21.27, -19.14, -63.33]
para_dG  = [0.00, -7.14, +17.95, -22.96, -66.80]

# Flag which points lack SP corrections (index 2 = TS)
ts_index = 2

# Colors (colorblind-friendly)
ORTHO_COLOR = "#2166AC"  # blue
PARA_COLOR  = "#B2182B"  # red

# Half-width of each horizontal energy-level bar
BAR_HALF = 0.25

# ---------------------------------------------------------------------------
# Set up font
# ---------------------------------------------------------------------------
import matplotlib.font_manager as fm

def _get_serif_font():
    """Return the best available serif font name."""
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
# Draw
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

def draw_pathway(ax, x_pos, dG_values, color, label, ts_idx):
    """Draw horizontal bars connected by dashed lines for a single pathway."""
    n = len(x_pos)
    # Draw dashed connecting lines first (so bars sit on top)
    for i in range(n - 1):
        x_start = x_pos[i] + BAR_HALF
        x_end   = x_pos[i + 1] - BAR_HALF
        ax.plot(
            [x_start, x_end],
            [dG_values[i], dG_values[i + 1]],
            linestyle="--",
            color=color,
            linewidth=1.2,
            alpha=0.7,
        )
    # Draw horizontal bars and annotations
    for i, (x, dg) in enumerate(zip(x_pos, dG_values)):
        lw = 2.0
        ls = "-"
        if i == ts_idx:
            lw = 1.8
            ls = ":"  # dotted bar for approximate TS

        ax.plot(
            [x - BAR_HALF, x + BAR_HALF],
            [dg, dg],
            color=color,
            linewidth=lw,
            linestyle=ls,
            solid_capstyle="round",
            label=label if i == 0 else None,
        )

        # Annotation text
        sign = "+" if dg > 0 else ""
        annotation = f"{sign}{dg:.2f}"
        if i == ts_idx:
            annotation += "†"

        # Offset label above or below the bar to avoid overlap
        offset = 0.9 if dg >= 0 else -1.5
        # Fine-tune to avoid ortho/para labels colliding at same x
        if label == "Ortho" and i in (2, 3, 4):
            x_offset = -0.22
        elif label == "Para" and i in (2, 3, 4):
            x_offset = 0.22
        else:
            x_offset = 0.0

        ax.text(
            x + x_offset,
            dg + offset,
            annotation,
            ha="center",
            va="bottom" if offset > 0 else "top",
            fontsize=8.5,
            color=color,
            fontweight="bold",
        )


draw_pathway(ax, x_positions, ortho_dG, ORTHO_COLOR, "Ortho", ts_index)
draw_pathway(ax, x_positions, para_dG,  PARA_COLOR,  "Para",  ts_index)

# ---------------------------------------------------------------------------
# Axes decoration
# ---------------------------------------------------------------------------
ax.set_xticks(x_positions)
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_ylabel("ΔG (kcal mol⁻¹)", fontsize=12)
ax.set_title(
    "Potential Energy Surface: OH• Addition to Phenol — Ortho vs Para Pathways",
    fontsize=14,
    pad=12,
)
ax.axhline(0, color="gray", linewidth=0.6, linestyle="-", alpha=0.5)
ax.set_xlim(-0.6, 4.6)
ax.set_ylim(-78, 30)

# Legend
ortho_patch = mpatches.Patch(color=ORTHO_COLOR, label="Ortho pathway")
para_patch  = mpatches.Patch(color=PARA_COLOR,  label="Para pathway")
ax.legend(
    handles=[ortho_patch, para_patch],
    loc="lower left",
    fontsize=10,
    frameon=False,
)

# ---------------------------------------------------------------------------
# Emphasis: ΔΔG‡ between TS levels and ΔΔG between adduct levels
# ---------------------------------------------------------------------------
ts_x = x_positions[2]
ts_ortho = ortho_dG[2]
ts_para  = para_dG[2]
# Double-headed arrow between TS levels
ax.annotate(
    "",
    xy=(ts_x + BAR_HALF + 0.05, ts_para),
    xytext=(ts_x + BAR_HALF + 0.05, ts_ortho),
    arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2),
)
ax.text(
    ts_x + BAR_HALF + 0.18,
    (ts_ortho + ts_para) / 2,
    "ΔΔG‡ = 3.32",
    ha="left",
    va="center",
    fontsize=7.5,
    color="#555555",
    style="italic",
)

adduct_x = x_positions[3]
adduct_ortho = ortho_dG[3]
adduct_para  = para_dG[3]
# Double-headed arrow between adduct levels
ax.annotate(
    "",
    xy=(adduct_x + BAR_HALF + 0.05, adduct_ortho),
    xytext=(adduct_x + BAR_HALF + 0.05, adduct_para),
    arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2),
)
ax.text(
    adduct_x + BAR_HALF + 0.18,
    (adduct_ortho + adduct_para) / 2,
    "ΔΔG = 3.82",
    ha="left",
    va="center",
    fontsize=7.5,
    color="#555555",
    style="italic",
)

# H-abstraction note (subtle, bottom-left)
ax.text(
    -0.5, -73,
    "H-abstraction: ΔG = −41.07 kcal/mol (not shown)",
    ha="left",
    va="bottom",
    fontsize=8,
    color="gray",
    style="italic",
)

# Footnote
fig.text(
    0.12, 0.01,
    "† SP correction missing; barrier approximate (E+G_corr only)",
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
fig.savefig("figures/fig1_pes_diagram.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/fig1_pes_diagram.pdf", bbox_inches="tight")
plt.close(fig)
print("Saved: figures/fig1_pes_diagram.png  figures/fig1_pes_diagram.pdf")
