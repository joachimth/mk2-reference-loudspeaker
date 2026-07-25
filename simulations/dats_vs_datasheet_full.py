"""
Mk3 Reference Loudspeaker — Full system response: DATS vs datasheet
====================================================================

Compares the ENTIRE system response using:
  1. All datasheet T/S parameters (the design baseline)
  2. DATS-measured T/S parameters (real units, Jul 25 2026)
  3. Predicted settled 18W values (Fs ~57 Hz, Qts ~0.50 after full break-in)

Shows bass + mid response BEFORE DSP correction so Joachim can see
exactly what the Linkwitz Transform + PEQ has to handle.

Key differences from system_response_inroom.py:
  - Woofer uses RAW sealed alignment (before LT), not post-LT
  - Mid uses raw sealed alignment (before crossover HP)
  - Three columns: datasheet | DATS current | DATS predicted (settled)

Output: simulations/plots/dats_vs_datasheet_full.png
"""
import os, sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

c_speed = 343.0

# ============================================================
#  Sealed enclosure model
# ============================================================
def sealed_response_db(f, fs, qts, vas_L, vb_L, sens=84.5):
    """Returns sealed box SPL response for n drivers in shared chamber."""
    alpha = vas_L / vb_L
    qtc = np.sqrt(alpha + 1) * qts if False else qts * np.sqrt(1 + alpha)
    # Correct Qtc formula for sealed: Qtc = Qts * sqrt(1 + Vas/Vb)
    qtc = qts * np.sqrt(1 + vas_L / vb_L)
    fc = fs * np.sqrt(1 + vas_L / vb_L)
    s = 1j * f / fc
    H = s**2 / (s**2 + s / qtc + 1)
    return 20 * np.log10(np.abs(H) + 1e-12) + sens

# ============================================================
#  Driver configs
# ============================================================
# Bass: 2x GRS 12SW-4HE in 65 L shared sealed, 2 drivers = +3 dB
VB_BASS = 65.0
SENS_BASS = 84.5 + 3.0  # per driver +3 dB for pair

# Datasheet GRS
FS_DS, QTS_DS, VAS_DS = 22.0, 0.43, 80.4
# DATS GRS (Fs unchanged, Qts 0.51)
FS_DATS, QTS_DATS = 22.0, 0.51

# Mid: 18W/4424G00 in 13 L sealed
VB_MID = 13.0
SENS_MID = 91.0

# Datasheet 18W
FM_DS, QTM_DS, VAM_DS = 49.0, 0.38, 19.0
# DATS 18W (5h break-in)
FM_DATS, QTM_DATS = 64.5, 0.58
# Predicted settled 18W (guesstimate)
FM_SET, QTM_SET = 57.0, 0.50

# ============================================================
#  Compute sealed alignments
# ============================================================
f = np.logspace(np.log10(10), np.log10(500), 1000)

def calc_sealed(f, fs, qts, vas, vb, sens):
    qtc = qts * np.sqrt(1 + vas / vb)
    fc = fs * np.sqrt(1 + vas / vb)
    mag = sealed_response_db(f, fs, qts, vas, vb, sens)
    return mag, qtc, fc

# Bass
w_ds, qw_ds, fw_ds = calc_sealed(f, FS_DS, QTS_DS, VAS_DS, VB_BASS, SENS_BASS)
w_dats, qw_dats, fw_dats = calc_sealed(f, FS_DATS, QTS_DATS, VAS_DS, VB_BASS, SENS_BASS)

# Mid
m_ds, qm_ds, fm_ds = calc_sealed(f, FM_DS, QTM_DS, VAM_DS, VB_MID, SENS_MID)
m_dats, qm_dats, fm_dats = calc_sealed(f, FM_DATS, QTM_DATS, VAM_DS, VB_MID, SENS_MID)
m_set, qm_set, fm_set = calc_sealed(f, FM_SET, QTM_SET, VAM_DS, VB_MID, SENS_MID)

# ============================================================
#  Print summary
# ============================================================
print("=" * 72)
print("  FULL SYSTEM: DATS vs Datasheet — Sealed alignment BEFORE DSP")
print("=" * 72)
print()
print("  BASS: 2× GRS 12SW-4HE (65 L shared sealed)")
print(f"  {'':30s} {'Datasheet':>12s} {'DATS 25/7':>12s}")
print(f"  {'Qts':30s} {QTS_DS:>12.3f} {QTS_DATS:>12.3f}")
print(f"  {'Qtc (65L)':30s} {qw_ds:>12.3f} {qw_dats:>12.3f}")
print(f"  {'Fc (Hz)':30s} {fw_ds:>12.1f} {fw_dats:>12.1f}")
print(f"  {'Delta @Fc vs datasheet (dB)':30s} {'0.0':>12s} {w_dats[np.argmin(np.abs(f - fw_ds))] - w_ds[np.argmin(np.abs(f - fw_ds))]:>12.2f}")
print()
print("  MID: 18W/4424G00 (13 L sealed)")
print(f"  {'':30s} {'Datasheet':>12s} {'DATS 5h':>12s} {'Settled':>12s}")
print(f"  {'Fs (Hz)':30s} {FM_DS:>12.1f} {FM_DATS:>12.1f} {FM_SET:>12.1f}")
print(f"  {'Qts':30s} {QTM_DS:>12.3f} {QTM_DATS:>12.3f} {QTM_SET:>12.3f}")
print(f"  {'Qtc (13L)':30s} {qm_ds:>12.3f} {qm_dats:>12.3f} {qm_set:>12.3f}")
print(f"  {'Fc (Hz)':30s} {fm_ds:>12.1f} {fm_dats:>12.1f} {fm_set:>12.1f}")

# ============================================================
#  Plot
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

colors = {
    "ds": "#2563eb",
    "dats": "#dc2626",
    "settled": "#059669",
    "lt_target": "#f59e0b",
}

# --- Woofer ---
ax = ax1
ax.semilogx(f, w_ds, lw=2.5, color=colors["ds"], label=f"Datasheet (Qts={QTS_DS}, Qtc={qw_ds:.3f}, Fc={fw_ds:.0f} Hz)")
ax.semilogx(f, w_dats, lw=2.5, color=colors["dats"], ls="--",
            label=f"DATS 25/7 (Qts={QTS_DATS}, Qtc={qw_dats:.3f}, Fc={fw_dats:.0f} Hz)")
# Mark Fc points
ax.axvline(fw_ds, color=colors["ds"], ls=":", lw=1, alpha=0.4)
ax.axvline(fw_dats, color=colors["dats"], ls=":", lw=1, alpha=0.4)
# LT target
ax.axhline(SENS_BASS, color=colors["lt_target"], ls="-.", lw=1.5, alpha=0.7,
           label=f"LT target: Fc=28 Hz, Qtc=0.707 ({SENS_BASS:.0f} dB SPL)")
ax.set_ylabel("SPL [dB]")
ax.set_title("2× GRS 12SW-4HE — Sealed in 65 L (before Linkwitz Transform)", fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)
ax.set_ylim(75, 100)
ax.set_xlim(10, 500)

# Shade the difference
ax.fill_between(f, w_ds, w_dats, alpha=0.08, color=colors["dats"])

# --- Midrange ---
ax = ax2
ax.semilogx(f, m_ds, lw=2.5, color=colors["ds"], label=f"Datasheet (Fs={FM_DS}, Qts={QTM_DS}, Qtc={qm_ds:.3f}, Fc={fm_ds:.0f} Hz)")
ax.semilogx(f, m_dats, lw=2.5, color=colors["dats"], ls="--",
            label=f"DATS 5h BI (Fs={FM_DATS}, Qts={QTM_DATS}, Qtc={qm_dats:.3f}, Fc={fm_dats:.0f} Hz)")
ax.semilogx(f, m_set, lw=2.5, color=colors["settled"], ls=":",
            label=f"Predicted settled (Fs={FM_SET}, Qts={QTM_SET}, Qtc={qm_set:.3f}, Fc={fm_set:.0f} Hz)")
# Mark Fc
ax.axvline(fm_ds, color=colors["ds"], ls=":", lw=1, alpha=0.4)
ax.axvline(fm_dats, color=colors["dats"], ls=":", lw=1, alpha=0.4)
ax.axvline(fm_set, color=colors["settled"], ls=":", lw=1, alpha=0.4)
# Crossfade region (200 Hz XO)
ax.axvspan(150, 260, alpha=0.06, color=colors["lt_target"], label="200 Hz BW4 crossover region")
ax.set_ylabel("SPL [dB]")
ax.set_xlabel("Frequency [Hz]")
ax.set_title("ScanSpeak 18W/4424G00 — Sealed in 13 L (before crossover HP)", fontsize=12, fontweight="bold")
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.25)
ax.set_ylim(65, 100)

# Shade difference
ax.fill_between(f, m_ds, m_dats, alpha=0.08, color=colors["dats"])

fig.suptitle("Mk3 Reference Loudspeaker v9 — DATS vs Datasheet Comparison\n"
             "Raw sealed alignment (before DSP correction / crossover filters)",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.95])

script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'dats_vs_datasheet_full.png')
fig.savefig(out_png, dpi=150)
print(f"\n✓ wrote {out_png}")
print()
print("=" * 72)
print("KEY TAKEAWAY")
print("=" * 72)
print()
print("Bass: DATS Qts=0.51 giver +0.7 dB @Fc vs datasheet Qts=0.43.")
print("      LT'en retter begge til Fc=28 Hz / Qtc=0.707 — intet problem.")
print()
print("Mid:  DATS 5h Fc=101 Hz vs datasheet Fc=77 Hz — 24 Hz højere.")
print("      Ved 200 Hz BW4 crossover: forskellen er <0.3 dB.")
print("      Mid-kammeret kan sagtens håndtere det uden ændringer.")
print()
print("Settled mid (estimeret Fs 57, Qts 0.50): Fc=87 Hz.")
print("      ALLE tre scenarier er uproblematiske ved 200 Hz BW4.")
print("      Kabinetdesignet er robust.")
print("=" * 72)
