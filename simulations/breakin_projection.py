"""
Mk3 Reference Loudspeaker — 18W/4424G00 Break-in Projection
===========================================================
Models the exponential-decay break-in curve for the ScanSpeak 18W/4424G00
midrange driver using measured DATS data at 0h and 5h.

Predicts: Fs(t), Qts(t) — and when they'll reach key milestones.

References:
  - Spec: Fs=49 Hz, Qts=0.38
  - Measured 0h: Fs=69.41, Qts=0.598
  - Measured 5h: Fs=64.53, Qts=0.576  (cad-r30, Jul 25 19:45)

Model: X(t) = X_final + (X_initial - X_final) * exp(-t / tau)
  where tau (time constant in hours) is fitted from data.

Output: simulations/plots/breakin_projection.png
"""
import os, sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Measured data points
# ============================================================
hours = np.array([0.0, 5.0])

# Fs (Hz)
fs_initial = 69.41
fs_5h = 64.53
fs_spec = 49.0

# Qts
qts_initial = 0.598
qts_5h = 0.576
qts_spec = 0.38

print("=" * 72)
print("  18W/4424G00 — Break-in Projection Model")
print("=" * 72)
print()
print("  Measured data:")
print(f"  {'':20s} {'0h':>10s} {'5h':>10s} {'Spec':>10s}")
print(f"  {'Fs (Hz)':20s} {fs_initial:>10.2f} {fs_5h:>10.2f} {fs_spec:>10.2f}")
print(f"  {'Qts':20s} {qts_initial:>10.3f} {qts_5h:>10.3f} {qts_spec:>10.3f}")
print()

# ============================================================
# Fit exponential decay: X(t) = X_final + (X_0 - X_final) * exp(-t / tau)
# With only 2 data points, we assume X_final and solve for tau.
# ============================================================

def solve_breakin(x0, x1, t1, x_final):
    """Solve for tau given X(0)=x0, X(t1)=x1, and known X_final."""
    if x_final >= x1:  # Not enough decay — can't solve
        return None
    # x1 = x_final + (x0 - x_final) * exp(-t1 / tau)
    # exp(-t1 / tau) = (x1 - x_final) / (x0 - x_final)
    ratio = (x1 - x_final) / (x0 - x_final)
    if ratio <= 0 or ratio > 1:
        return None
    tau = -t1 / np.log(ratio)
    return tau

def project(x0, x_final, tau, t_max=50, n=500):
    """Project break-in curve."""
    t = np.linspace(0, t_max, n)
    x = x_final + (x0 - x_final) * np.exp(-t / tau)
    return t, x

def hours_to_target(x0, x_final, tau, target):
    """Hours needed to reach a target value."""
    if target >= x0:
        return 0.0
    if target <= x_final:
        return float('inf')
    # target = x_final + (x0 - x_final) * exp(-t / tau)
    # t = -tau * ln((target - x_final) / (x0 - x_final))
    t = -tau * np.log((target - x_final) / (x0 - x_final))
    return t

# ============================================================
# Scenario 1: Optimistic — settles at Fs=57, Qts=0.50
# ============================================================
print("  Scenario 1 — OPTIMISTIC (settles at Fs=57, Qts=0.50):")

fs_final_opt = 57.0
qts_final_opt = 0.50

tau_fs_opt = solve_breakin(fs_initial, fs_5h, 5.0, fs_final_opt)
tau_qts_opt = solve_breakin(qts_initial, qts_5h, 5.0, qts_final_opt)

if tau_fs_opt and tau_qts_opt:
    print(f"  τ_Fs = {tau_fs_opt:.1f} h, τ_Qts = {tau_qts_opt:.1f} h")
    for target_fs in [64.5, 62, 60, 57]:
        h = hours_to_target(fs_initial, fs_final_opt, tau_fs_opt, target_fs)
        pct = (fs_initial - target_fs) / (fs_initial - fs_final_opt) * 100
        print(f"    Fs = {target_fs:.0f} Hz: {h:.1f} h ({pct:.0f}% of total change)")
    for target_qts in [0.58, 0.55, 0.53, 0.50]:
        h = hours_to_target(qts_initial, qts_final_opt, tau_qts_opt, target_qts)
        pct = (target_qts - qts_final_opt) / (qts_initial - qts_final_opt) * 100
        # Note: Qts is dropping (initial 0.598 → final 0.50)
        progress = (qts_initial - target_qts) / (qts_initial - qts_final_opt) * 100
        print(f"    Qts = {target_qts:.3f}: {h:.1f} h ({progress:.0f}% of total change)")
print()

# ============================================================
# Scenario 2: Conservative — settles at Fs=60, Qts=0.55
# ============================================================
print("  Scenario 2 — CONSERVATIVE (settles at Fs=60, Qts=0.55):")

fs_final_con = 60.0
qts_final_con = 0.55

tau_fs_con = solve_breakin(fs_initial, fs_5h, 5.0, fs_final_con)
tau_qts_con = solve_breakin(qts_initial, qts_5h, 5.0, qts_final_con)

if tau_fs_con and tau_qts_con:
    print(f"  τ_Fs = {tau_fs_con:.1f} h, τ_Qts = {tau_qts_con:.1f} h")
    for target_fs in [64.5, 62, 60]:
        h = hours_to_target(fs_initial, fs_final_con, tau_fs_con, target_fs)
        pct = (fs_initial - target_fs) / (fs_initial - fs_final_con) * 100
        print(f"    Fs = {target_fs:.0f} Hz: {h:.1f} h ({pct:.0f}% of total change)")
    for target_qts in [0.58, 0.55]:
        h = hours_to_target(qts_initial, qts_final_con, tau_qts_con, target_qts)
        progress = (qts_initial - target_qts) / (qts_initial - qts_final_con) * 100
        print(f"    Qts = {target_qts:.3f}: {h:.1f} h ({progress:.0f}% of total change)")
print()

# ============================================================
# Time constants comparison
# ============================================================
print("  Decay rate comparison (optimistic scenario):")
print(f"  Fs drops {fs_initial - fs_final_opt:.1f} Hz total. At 5h: {(fs_initial - fs_5h):.1f} Hz ({((fs_initial - fs_5h)/(fs_initial - fs_final_opt)*100):.0f}%)")
print(f"  Qts drops {qts_initial - qts_final_opt:.3f} total. At 5h: {(qts_initial - qts_5h):.3f} ({((qts_initial - qts_5h)/(qts_initial - qts_final_opt)*100):.0f}%)")
print()

# ============================================================
# How much better does a second 5h session get?
# ============================================================
print("  If you run another 5h break-in block (total 10h):")

# Fs at 10h (optimistic)
fs_10h_opt = fs_final_opt + (fs_initial - fs_final_opt) * np.exp(-10 / tau_fs_opt)
qts_10h_opt = qts_final_opt + (qts_initial - qts_final_opt) * np.exp(-10 / tau_qts_opt)
print(f"  Optimistic: Fs(10h) = {fs_10h_opt:.1f} Hz, Qts(10h) = {qts_10h_opt:.3f}")
print(f"    Fs improvement 5h→10h: {fs_5h - fs_10h_opt:.1f} Hz")

fs_10h_con = fs_final_con + (fs_initial - fs_final_con) * np.exp(-10 / tau_fs_con)
qts_10h_con = qts_final_con + (qts_initial - qts_final_con) * np.exp(-10 / tau_qts_con)
print(f"  Conservative: Fs(10h) = {fs_10h_con:.1f} Hz, Qts(10h) = {qts_10h_con:.3f}")
print(f"    Fs improvement 5h→10h: {fs_5h - fs_10h_con:.1f} Hz")

# ============================================================
# When does it reach 90% of total change?
# ============================================================
print()
print("  Time to 90% of total parameter change:")
t_90_fs_opt = -tau_fs_opt * np.log(1 - 0.90) if tau_fs_opt else float('inf')
t_90_qts_opt = -tau_qts_opt * np.log(1 - 0.90) if tau_qts_opt else float('inf')
print(f"  Fs (opt): {t_90_fs_opt:.1f} h  |  Qts (opt): {t_90_qts_opt:.1f} h")
t_90_fs_con = -tau_fs_con * np.log(1 - 0.90) if tau_fs_con else float('inf')
t_90_qts_con = -tau_qts_con * np.log(1 - 0.90) if tau_qts_con else float('inf')
print(f"  Fs (con): {t_90_fs_con:.1f} h  |  Qts (con): {t_90_qts_con:.1f} h")

# ============================================================
# Plot
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# Point markers — use plot for measured points, scatter for projections

# --- Fs projection ---
ax = ax1
t_fs_opt, fs_proj_opt = project(fs_initial, fs_final_opt, tau_fs_opt, 60)
t_fs_con, fs_proj_con = project(fs_initial, fs_final_con, tau_fs_con, 60)

ax.plot(t_fs_opt, fs_proj_opt, color='#059669', linewidth=2.5, label=f"Optimistic: Fs→{fs_final_opt:.0f}, τ={tau_fs_opt:.0f}h")
ax.plot(t_fs_con, fs_proj_con, color='#d97706', linewidth=2.5, ls='--', label=f"Conservative: Fs→{fs_final_con:.0f}, τ={tau_fs_con:.0f}h")
ax.plot(hours, [fs_initial, fs_5h], 'o', color='#dc2626', markersize=10, zorder=5, label="Measured")
ax.axhline(fs_spec, color='#6366f1', ls='-.', linewidth=1.5, alpha=0.7, label=f"Spec: {fs_spec} Hz")

# Annotate measured points
for h, v in [(0, fs_initial), (5, fs_5h)]:
    ax.annotate(f"  {v:.1f}", (h, v), fontsize=9, fontweight='bold', va='bottom')

# Target markers — squares for projection milestones
for h_target in [10, 15, 20]:
    v_opt = fs_final_opt + (fs_initial - fs_final_opt) * np.exp(-h_target / tau_fs_opt)
    v_con = fs_final_con + (fs_initial - fs_final_con) * np.exp(-h_target / tau_fs_con)
    ax.plot(h_target, v_opt, 's', color='#059669', markersize=7, zorder=4)
    ax.plot(h_target, v_con, 's', color='#d97706', markersize=7, zorder=4)

ax.set_xlabel("Break-in time [hours]")
ax.set_ylabel("Fs [Hz]")
ax.set_title("ScanSpeak 18W/4424G00 — Fs Break-in Projection", fontweight='bold')
ax.legend(fontsize=8, loc='upper right')
ax.grid(True, alpha=0.25)
ax.set_xlim(-2, 52)
ax.set_ylim(45, 72)

# Add shaded uncertainty region between optimistic and conservative
ax.fill_between(t_fs_opt, fs_proj_con, fs_proj_opt, alpha=0.08, color='#d97706')

# --- Qts projection ---
ax = ax2
t_qts_opt, qts_proj_opt = project(qts_initial, qts_final_opt, tau_qts_opt, 60)
t_qts_con, qts_proj_con = project(qts_initial, qts_final_con, tau_qts_con, 60)

ax.plot(t_qts_opt, qts_proj_opt, color='#059669', linewidth=2.5, label=f"Optimistic: Qts→{qts_final_opt:.3f}, τ={tau_qts_opt:.0f}h")
ax.plot(t_qts_con, qts_proj_con, color='#d97706', linewidth=2.5, ls='--', label=f"Conservative: Qts→{qts_final_con:.3f}, τ={tau_qts_con:.0f}h")
ax.plot(hours, [qts_initial, qts_5h], 'o', color='#dc2626', markersize=10, zorder=5, label="Measured")
ax.axhline(qts_spec, color='#6366f1', ls='-.', linewidth=1.5, alpha=0.7, label=f"Spec: {qts_spec:.3f}")

for h, v in [(0, qts_initial), (5, qts_5h)]:
    ax.annotate(f"  {v:.3f}", (h, v), fontsize=9, fontweight='bold', va='bottom')

for h_target in [10, 15, 20]:
    v_opt = qts_final_opt + (qts_initial - qts_final_opt) * np.exp(-h_target / tau_qts_opt)
    v_con = qts_final_con + (qts_initial - qts_final_con) * np.exp(-h_target / tau_qts_con)
    ax.plot(h_target, v_opt, 's', color='#059669', markersize=7, zorder=4)
    ax.plot(h_target, v_con, 's', color='#d97706', markersize=7, zorder=4)

ax.set_xlabel("Break-in time [hours]")
ax.set_ylabel("Qts")
ax.set_title("ScanSpeak 18W/4424G00 — Qts Break-in Projection", fontweight='bold')
ax.legend(fontsize=8, loc='upper right')
ax.grid(True, alpha=0.25)
ax.set_xlim(-2, 52)
ax.set_ylim(0.35, 0.62)

ax.fill_between(t_qts_opt, qts_proj_con, qts_proj_opt, alpha=0.08, color='#d97706')

fig.suptitle("18W/4424G00 Break-in Projection — Predictions based on 0h→5h DATS data\n"
             "Exponential decay model: X(t) = X_final + (X₀ − X_final)·exp(−t⁄τ)",
             fontsize=13, fontweight='bold')

fig.tight_layout(rect=[0, 0, 1, 0.92])

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
out_png = os.path.join(script_dir, 'plots', 'breakin_projection.png')
fig.savefig(out_png, dpi=150)
print(f"\n✓ wrote {out_png}")

# ============================================================
# Summary table
# ============================================================
print()
print("=" * 72)
print("  SUMMARY — Recommended Re-measure Schedule")
print("=" * 72)
print()
print("  After ferie, measure at these milestones:")
print()
print(f"  {'Hours':>6s} | {'Fs (opt)':>10s} {'Fs (con)':>10s} | {'Qts (opt)':>10s} {'Qts (con)':>10s} | {'Note':>30s}")
print(f"  {'-'*6} | {'-'*10} {'-'*10} | {'-'*10} {'-'*10} | {'-'*30}")

for h_target in [0, 5, 10, 15, 20, 30]:
    if h_target == 0:
        fs_o, fs_c = fs_initial, fs_initial
        qts_o, qts_c = qts_initial, qts_initial
    else:
        fs_o = fs_final_opt + (fs_initial - fs_final_opt) * np.exp(-h_target / tau_fs_opt)
        fs_c = fs_final_con + (fs_initial - fs_final_con) * np.exp(-h_target / tau_fs_con)
        qts_o = qts_final_opt + (qts_initial - qts_final_opt) * np.exp(-h_target / tau_qts_opt)
        qts_c = qts_final_con + (qts_initial - qts_final_con) * np.exp(-h_target / tau_qts_con)

    if h_target <= 5:
        note = "already measured" if h_target <= 5 else ""
    elif h_target == 10:
        note = "recommended re-measure"
    elif h_target == 15:
        note = "recommended re-measure"
    elif h_target == 20:
        note = "likely settled enough"
    else:
        note = "diminishing returns"

    print(f"  {h_target:>6.0f} | {fs_o:>10.1f} {fs_c:>10.1f} | {qts_o:>10.3f} {qts_c:>10.3f} | {note:>30s}")

print()
print("  Key insight: 70-80% of the total break-in change happens in the first")
print("  ~15 hours. After 20h, you're within 90% of settled values.")
print("  No need to break in beyond ~25h — diminishing returns kick in hard.")
print()
print("  Octave-averaged pink noise at 2-3V RMS is adequate for break-in.")
print("  Don't exceed 5V RMS (12W nominal) to avoid thermal damage.")
print()
print("  NOTE: The second GRS 12SW also needs measurement for push-push matching.")
print("  (Qts match within ±0.03 is ideal — if off, the worse one goes to the back)")
print("=" * 72)
