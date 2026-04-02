# Phenol Nitration — Computational Chemistry

Computational study of OH•-initiated radical nitration of phenol,
focussing on the **comparison of *ortho* vs *para* OH• addition** to the phenol ring
as the primary mechanistic pathway producing *ortho*- and *para*-nitrophenol.

---

## Primary Focus

The study centres on the **OH• radical addition** to the phenol ring at the ortho and para
positions, followed by NO₂• capture to give the final nitrophenol products.  All thermodynamic
and kinetic metrics favour the *para* pathway (see Key Results below).

### Mechanistic pathways considered

**Ortho pathway (primary):**
PhOH + OH• → PhOH·OH RC(o) → TS(o) → *o*-OHCHD → [+NO₂•, −H₂O] → *o*-nitrophenol

**Para pathway (primary):**
PhOH + OH• → PhOH·OH RC(p) → TS(p) → *p*-OHCHD → [+NO₂•, −H₂O] → *p*-nitrophenol

**H-abstraction (secondary, briefly noted):**
PhOH + OH• → PhO• + H₂O (ΔG = −41.07 kcal/mol) — thermodynamically feasible but not the
primary pathway under study.

**Electrophilic aromatic substitution** also exists as a mechanistic possibility but is
beyond the scope of this radical-addition study.

---

## Level of Theory

- **Geometry optimizations and frequency calculations** performed at a lower DFT level.
- **Single-point (SP) energy corrections** computed at a higher DFT level on the
  optimised geometries.
- **G_combined** (Ha) = E_SP + G_corr(opt+freq) is the primary thermodynamic quantity
  used throughout.  1 Ha = 627.509 kcal/mol.

> ⚠ **Data quality notes**
> - Transition-state (TS) barriers for OH addition **lack SP corrections** and are
>   therefore approximate; they are flagged with † in all figures.
> - The `PhOH_cation` opt+freq entry has a formula mismatch (wrong input geometry);
>   only the vertical ionisation energy (from SP energies) is reported.

---

## Repository Structure

```
phenol-nitration/
├── data/
│   ├── thermochemistry.csv   # G_combined and SP energies for all species (37 rows)
│   │                         # G_combined = E_SP + G_corr; where G_corr is blank,
│   │                         # G_combined = E_SP alone (SP-only) or E+G_corr(opt+freq).
│   ├── spin_density.csv      # Mulliken spin densities at key atomic sites (14 rows)
│   └── reaction_dg.csv       # Balanced-reaction ΔG and ΔH values (7 rows)
├── scripts/
│   ├── fig1_pes_diagram.py              # PRIMARY: Dual-pathway PES diagram (ortho vs para)
│   ├── fig2_selectivity.py              # PRIMARY: Ortho vs para selectivity comparison
│   ├── fig3_reaction_thermodynamics.py  # SUPPORTING: Reaction ΔG / ΔH bar chart
│   ├── figS1_spin_density.py            # SUPPLEMENTARY: Spin density grouped bar chart
│   └── generate_all_figures.py          # Master script — runs all four in order
├── figures/                  # Generated PNG and PDF outputs (git-ignored)
├── requirements.txt
└── README.md
```

---

## Figures

| Figure | File | Role | Description |
|--------|------|------|-------------|
| Fig 1 | `fig1_pes_diagram` | **Primary** | Connected energy-level diagram for both ortho and para OH• addition pathways; ΔG relative to PhOH + OH• + NO₂• = 0; includes ΔΔG‡ and ΔΔG emphasis annotations |
| Fig 2 | `fig2_selectivity` | **Primary** | Side-by-side ortho vs para comparison for RC binding, TS barrier, adduct ΔG, NO₂• capture ΔG, and overall ΔG; summary box highlighting para advantage |
| Fig 3 | `fig3_reaction_thermo` | Supporting | Horizontal grouped bar chart of ΔG and ΔH for the four ring-addition and NO₂• capture steps |
| Fig S1 | `figS1_spin_density` | Supplementary | Grouped bar chart of Mulliken spin densities (O, Ipso-C, Ortho-C, Para-C) for PhO•, PhOH•⁺, *o*-OHCHD, *p*-OHCHD |

All figures are saved as both high-resolution PNG (300 DPI) and PDF in `figures/`.

---

## Quick Start

```bash
pip install -r requirements.txt
python scripts/generate_all_figures.py
```

Figures are written to the `figures/` directory.

---

## Key Results

| Metric | Ortho | Para | Favours |
|--------|-------|------|---------|
| RC binding energy (kcal/mol) | −2.26 | −7.14 | **Para** |
| TS barrier from reactants (kcal/mol)† | +21.27 | +17.95 | **Para** |
| Adduct ΔG (kcal/mol) | −19.14 | −22.96 | **Para** |
| NO₂• capture ΔG (kcal/mol) | −44.21 | −43.83 | Ortho (marginal) |
| Overall ΔG (kcal/mol) | −63.33 | −66.80 | **Para** |

† SP corrections missing for TS structures; barriers are approximate.

The *para* pathway is favoured by 4 of 5 thermodynamic and kinetic metrics,
consistent with the observed preference for *para*-nitrophenol formation.
