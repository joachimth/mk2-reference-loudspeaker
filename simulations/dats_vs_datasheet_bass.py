"""
Mk3 Reference Loudspeaker - DATS-measured vs datasheet bass alignment comparison
================================================================================

Compares sealed cabinet behavior using:
  1. Datasheet T/S parameters (design nominal)
  2. DATS-measured T/S parameters (real unit, Jul 25 2026)

Also computes the combined effect of both the GRS 12SW-4HE woofer AND
the ScanSpeak 18W/4424G00 midrange measured differences (mid Fs shift
is 64.5 Hz vs spec 49 Hz — still breaking in).

This helps Joachim see whether the cabinet design needs revision based
on real driver measurements.

ASSUMPTIONS
- 2 x GRS 12SW-4HE per loudspeaker, shared sealed ~65 L net chamber (v9)
- N-driver sealed relation applied
- GRS 12SW DATS (Jul 25): Qts=0.51 (vs 0.43). Fs assumed same (22 Hz) since
  DAYTONAUDIO measurement didn't show a significant Fs shift.
- 18W/4424G00 mid chamber: ~13 L sealed (datasheet closed-box rec)
- 18W DATS (Jul 25, after 5h break-in): Fs=64.5 Hz, Qts=0.58, Vas~19L
  (break-in trending toward spec Fs 49 Hz, Qts 0.38 — re-measure needed)

Output: simulations/plots/dats_vs_datasheet_bass.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rho = 1.18

# --- Driver parameters ---

# GRS 12SW-4HE — datasheet (design nominal)
GRS12_DS = dict(name="GRS 12SW-4HE (datasheet)", Fs=22.0, Qts=0.43, Vas=80.4,
                Sd=504e-4, Xmax=12.5e-3, sens=84.5, Pmax=250, imp=4)

# GRS 12SW-4HE — DATS measured (Jul 25)
GRS12_DATS = dict(name="GRS 12SW-4HE (DATS, Jul 25)", Fs=22.0, Qts=0.51, Vas=80.4,
                  Sd=504e-4, Xmax=12.5e-3, sens=84.5, Pmax=250, imp=4)

# ScanSpeak 18W/4424G00 — datasheet
SS18_DS = dict(name="18W/4424G00 (datasheet)", Fs=49.0, Qts=0.38, Vas=19.0,
               Sd=150e-4, Xmax=6.5e-3, sens=90.0, Pmax=100, imp=4)

# ScanSpeak 18W/4424G00 — DATS measured (Jul 25, 5h break-in)
SS18_DATS = dict(name="18W/4424G00 (DATS, 5h BI)", Fs=64.5, Qts=0.58, Vas=19.0,
                 Sd=150e-4, Xmax=6.5e-3, sens=90.0, Pmax=100, imp=4)

def sealed_sealed(d, Vb):
    """N drivers in same sealed chamber (shared volume)"""
    a = 2 * d["Vas"] / Vb
    root = np.sqrt(1 + a)
    return d["Qts"] * root, d["Fs"] * root

def sealed_single(d, Vb):
    """Single driver in its own sealed chamber (midrange)"""
    a = d["Vas"] / Vb
    root = np.sqrt(1 + a)
    return d["Qts"] * root, d["Fs"] * root

def hp2(f, Fc, Q):
    s2 = (f / Fc) ** 2
    return s2 / np.sqrt((1 - s2) ** 2 + (f / (Fc * Q)) ** 2)

# === BASS SECTION — GRS 12SW-4HE ===
Vb_bass = 65  # v9 net bass volume (L)

print("=" * 65)
print("  BASS: 2× GRS 12SW-4HE in shared sealed chamber")
print("=" * 65)

results_bass = {}
for label, d in [("Datasheet", GRS12_DS), ("DATS Jul 25", GRS12_DATS)]:
    Qtc, Fc = sealed_sealed(d, Vb_bass)
    results_bass[label] = (Qtc, Fc)
    print(f"\n  {label}:")
    print(f"    Fs={d['Fs']} Hz, Qts={d['Qts']}, Vas={d['Vas']} L")
    print(f"    Vb={Vb_bass} L  ->  Qtc={Qtc:.3f},  Fc={Fc:.1f} Hz")

# === MID SECTION — 18W/4424G00 ===
Vb_mid = 13  # v9 mid chamber (L)
print("\n" + "=" * 65)
print("  MID: 18W/4424G00 in sealed chamber")
print("=" * 65)

results_mid = {}
for label, d in [("Datasheet", SS18_DS), ("DATS 5h BI", SS18_DATS)]:
    Qtc, Fc = sealed_single(d, Vb_mid)
    results_mid[label] = (Qtc, Fc)
    print(f"\n  {label}:")
    print(f"    Fs={d['Fs']} Hz, Qts={d['Qts']}, Vas={d['Vas']} L")
    print(f"    Vb={Vb_mid} L  ->  Qtc={Qtc:.3f},  Fc={Fc:.1f} Hz")

# === LT COMPARISON ===
Fc_target = 28.0
Qt_target = 0.707
print("\n" + "=" * 65)
print("  LINKWITZ TRANSFORM: bass alignment")
print("=" * 65)
for label, (Qtc, Fc) in results_bass.items():
    print(f"\n  {label}: raw Fc={Fc:.1f} Hz, Qtc={Qtc:.3f}")
    print(f"    LT boost required: Fc {Fc:.1f} -> {Fc_target:.1f} Hz  "
          f"Q {Qtc:.3f} -> {Qt_target:.3f}")

# === PLOT ===
f = np.logspace(np.log10(10), np.log10(500), 500)
sens_bass = 84.5 + 3  # +3 dB push-push

fig, axes = plt.subplots(3, 1, figsize=(12, 13), sharex=True)

# Top: Bass response
ax = axes[0]
ax.set_title("Bass alignment: 2× GRS 12SW-4HE sealed 65 L — Datasheet vs DATS (Jul 25)",
             fontsize=12, fontweight="bold")

for label, (Qtc, Fc), col, ls in [
    ("Datasheet (Qts=0.43)", results_bass["Datasheet"], "tab:blue", "-"),
    ("DATS (Qts=0.51)", results_bass["DATS Jul 25"], "tab:red", "--")]:
    H = hp2(f, Fc, Qtc)
    ax.plot(f, 20*np.log10(H) + sens_bass, col, ls=ls, lw=2.5,
            label=f'{label}: Qtc={Qtc:.2f}, Fc={Fc:.1f} Hz')
    # With Linkwitz Transform
    H_lt = hp2(f, Fc_target, Qt_target)
    ax.plot(f, 20*np.log10(H_lt) + sens_bass, col, ls=":", lw=1.5, alpha=0.6,
            label=f'{label} + LT (Fc={Fc_target} Hz)')

ax.set_ylabel("SPL (dB @ 2.83V/1m)")
ax.set_ylim(50, 100)
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.3)
ax.axhline(sens_bass, color="0.5", ls=":", lw=0.5)

# Middle: Fold change in SPL
ax = axes[1]
ax.set_title("Change in predicted response: DATS - Datasheet",
             fontsize=12, fontweight="bold")
_, Q_DS, Fc_DS, _, Q_DATS, Fc_DATS = None, *results_bass["Datasheet"], None, *results_bass["DATS Jul 25"]
H_DS = hp2(f, results_bass["Datasheet"][1], results_bass["Datasheet"][0])
H_DATS = hp2(f, results_bass["DATS Jul 25"][1], results_bass["DATS Jul 25"][0])
diff = 20 * np.log10(H_DATS / H_DS)
ax.plot(f, diff, "tab:purple", lw=2.5)
ax.axhline(0, color="gray", ls="--", lw=0.8)
ax.fill_between(f, diff, 0, where=(diff < 0), color="tab:red", alpha=0.2, label="Loss")
ax.fill_between(f, diff, 0, where=(diff > 0), color="tab:green", alpha=0.2, label="Gain")
ax.set_ylabel("SPL difference (dB)")
ax.set_ylim(-6, 3)
ax.set_xlim(10, 500)
ax.set_xscale("log")
ax.legend(fontsize=9)
ax.grid(True, which="both", alpha=0.3)

# Bottom: midrange chamber alignment
ax = axes[2]
ax.set_title("Midrange chamber: 18W/4424G00 sealed 13 L — Datasheet vs DATS (5h break-in)",
             fontsize=12, fontweight="bold")

for label, (Qtc, Fc), col, ls in [
    ("Datasheet (Fs=49, Qts=0.38)", results_mid["Datasheet"], "tab:blue", "-"),
    ("DATS 5h BI (Fs=64.5, Qts=0.58)", results_mid["DATS 5h BI"], "tab:orange", "--")]:
    H = hp2(f, Fc, Qtc)
    ax.plot(f, 20*np.log10(H) + 90, col, ls=ls, lw=2.5,
            label=f'{label}: Qtc={Qtc:.2f}, Fc={Fc:.1f} Hz')

ax.set_ylabel("SPL (dB @ 2.83V/1m)")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylim(55, 100)
ax.legend(fontsize=9, loc="lower left")
ax.grid(True, which="both", alpha=0.3)

# Add annotation about break-in status
ax.text(0.98, 0.02,
        "Note: 18W break-in at 5h — Fs trending from 64.5→49 Hz.\n"
        "Expected settled Fs ~55-60 Hz. Re-measure at 15h and 20h.",
        transform=ax.transAxes, fontsize=8, ha="right", va="bottom",
        bbox=dict(facecolor="lightyellow", alpha=0.8, boxstyle="round,pad=0.3"))

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), "plots", "dats_vs_datasheet_bass.png")
fig.savefig(out, dpi=150)
print(f"\n✓ wrote {out}")

# === SUMMARY TABLE ===
print("\n" + "=" * 65)
print("  SUMMARY")
print("=" * 65)
print(f"\n  Bass (2× GRS 12SW, 65 L shared sealed):")
print(f"    {'Parameter':<25} {'Datasheet':<15} {'DATS Jul 25':<15}")
print(f"    {'-'*25} {'-'*15} {'-'*15}")
print(f"    {'Fs (Hz)':<25} {GRS12_DS['Fs']:<15} {GRS12_DATS['Fs']:<15}")
print(f"    {'Qts':<25} {GRS12_DS['Qts']:<15} {GRS12_DATS['Qts']:<15}")
print(f"    {'Qtc':<25} {results_bass['Datasheet'][0]:<15.3f} {results_bass['DATS Jul 25'][0]:<15.3f}")
print(f"    {'Fc (Hz)':<25} {results_bass['Datasheet'][1]:<15.1f} {results_bass['DATS Jul 25'][1]:<15.1f}")
print(f"    {'LT boost range (Hz)':<25} {results_bass['Datasheet'][1]:.1f}->{Fc_target:<9.0f} {results_bass['DATS Jul 25'][1]:.1f}->{Fc_target:<9.0f}")

print(f"\n  Mid (18W/4424G00, 13 L sealed):")
print(f"    {'Parameter':<25} {'Datasheet':<15} {'DATS 5h BI':<15}")
print(f"    {'-'*25} {'-'*15} {'-'*15}")
print(f"    {'Fs (Hz)':<25} {SS18_DS['Fs']:<15} {SS18_DATS['Fs']:<15}")
print(f"    {'Qts':<25} {SS18_DS['Qts']:<15} {SS18_DATS['Qts']:<15}")
print(f"    {'Qtc':<25} {results_mid['Datasheet'][0]:<15.3f} {results_mid['DATS 5h BI'][0]:<15.3f}")
print(f"    {'Fc (Hz)':<25} {results_mid['Datasheet'][1]:<15.1f} {results_mid['DATS 5h BI'][1]:<15.1f}")
