# Chapter 15 — Measurements

> **DATS impedance measurements (Jul 25, 2026):** All three mk3 drivers
> measured in free air with Dayton Audio Test System (DATS). Raw data
> in `assets/measurements/dats/`. Plot: `assets/measurements/dats_impedance_plot.svg`.

---

## Summary

| Driver | Fs (DATS) | Fs (datasheet) | Δ | Qts (DATS) | Qts (datasheet) | Δ | Status |
|---|---|---|---|---|---|---|---|
| GRS 12SW-4HE | 25.1 Hz | 22.0 Hz | +14% | 0.512 | 0.43 | +19% | ⚠ Qms high |
| ScanSpeak 18W/4424G00 | 69.4 Hz | 49.0 Hz | +42% | 0.598 | 0.38 | +57% | ⚠ Significant |
| SB26STAC-C000-4 | 658 Hz | 750 Hz | −12% | 1.042 | 1.12 | −7% | ✓ Good match |

---

## GRS 12SW-4HE (woofer, push-push pair)

| Parameter | DATS | Datasheet | Δ | Status |
|---|---|---|---|---|
| Fs | 25.07 Hz | 22.0 Hz | +14.0% | ✓ within tolerance |
| Re | 4.20 Ω | 3.7 Ω | +13.5% | ✓ |
| Qms | 3.929 | 2.0 | +96.4% | ⚠ high |
| Qes | 0.589 | 0.54 | +9.0% | ✓ |
| Qts | 0.512 | 0.43 | +19.0% | ⚠ high |
| Le | 2.86 mH | 2.5 mH | +14.2% | ✓ |
| Zmax | 32.24 Ω | — | — | — |

**Computed (using datasheet Vas = 80.4 L):**
- Cms = 228.0 µm/N
- Mms = 176.8 g
- Bl = 0.30 T·m (seems low — Vas from datasheet may not match this unit)

**Assessment:** Fs and Re are within 15% of spec — normal unit-to-unit variation
for GRS. The Qms is nearly double the datasheet value (3.93 vs 2.0), which drives
Qts up to 0.51. This suggests the suspension is softer than the datasheet sample.
For sealed push-push this is workable but will raise Qtc slightly. The cabinet
simulation should be re-run with DATS values.

**Break-in update (5 hours, Jul 26):**

| Parameter | 0h | 5h | Δ | Datasheet | 5h vs spec |
|---|---|---|---|---|---|
| Fs | 25.07 Hz | 23.52 Hz | −6.2% | 22 Hz | +6.9% ✓ |
| Qts | 0.512 | 0.442 | −13.7% | 0.43 | +2.7% ✓ |
| Qms | 3.929 | 2.995 | −23.8% | 2.0 | +49.8% ⚠ |
| Qes | 0.589 | 0.518 | −12.0% | 0.54 | −4.1% ✓ |
| Zmax | 32.24 Ω | 28.70 Ω | −11.0% | — | — |
| Le | 2.86 mH | 2.91 mH | +1.8% | 2.5 mH | +16.2% |

Excellent response to break-in. After just 5 hours, Qts is within 2.7% of spec
(0.442 vs 0.43) and Fs is within 7% (23.5 vs 22 Hz). Qes is within 4% of spec.
The driver is essentially at datasheet values now. Qms is still 50% high (3.0 vs
2.0) but Qms has less impact on sealed box response than Qts.

The 12SW responded much faster to break-in than the 18W (Qts −13.7% vs −3.7%
in the same 5 hours). GRS uses a softer surround formulation that loosens
quickly.

**Action:** Measure the second 12SW unit (also break in if needed). With Qts =
0.44 and Fs = 23.5 Hz, the sealed push-push cabinet simulation can proceed with
confidence. Match the two units within ~1 Hz on Fs for optimal push-push
cancellation.

**Break-in update (10 hours, Jul 26):**

| Parameter | 0h | 5h | 10h | Datablad | 10h vs spec |
|---|---|---|---|---|---|
| Fs | 25.07 Hz | 23.52 Hz | 23.25 Hz | 22 Hz | +5.7% ✓ |
| Qts | 0.512 | 0.442 | 0.462 | 0.43 | +7.3% ✓ |
| Qes | 0.589 | 0.518 | 0.542 | 0.54 | +0.4% ✓ |
| Qms | 3.929 | 2.995 | 3.097 | 2.0 | +54.9% ⚠ |
| Re | 4.20 Ω | 4.23 Ω | 4.40 Ω | 3.7 Ω | +18.9% ⚠ |
| Zmax | 32.24 Ω | 28.70 Ω | 29.53 Ω | — | — |

Break-in is essentially complete. Fs stabilized at 23.25 Hz (only 1.2% change
from 5h to 10h, vs 6.2% from 0h to 5h). Qts at 0.46 is within 7% of spec —
good enough for cabinet design. Qes is within 0.4% of spec. Qms remains high
(+55%) but has minimal impact on sealed box response. Re creeping up to 4.40 Ω
(+19%) is likely voice coil warming from the break-in session — should settle
back when measured cold.

**Final 12SW design values:** Fs = 23.3 Hz, Qts = 0.46, Re = 4.4 Ω (cold recheck
recommended).

---

## ScanSpeak 18W/4424G00 (midrange)

| Parameter | DATS | Datasheet | Δ | Status |
|---|---|---|---|---|
| Fs | 69.41 Hz | 49.0 Hz | +41.7% | ⚠ significant |
| Re | 3.117 Ω | 3.2 Ω | −2.6% | ✓ |
| Qms | 5.518 | 1.82 | +203% | ⚠ very high |
| Qes | 0.671 | 0.47 | +42.7% | ⚠ high |
| Qts | 0.598 | 0.38 | +57.4% | ⚠ high |
| Le | 0.299 mH | 0.36 mH | −17.0% | ⚠ |
| Zmax | 28.75 Ω | — | — | — |

**Computed (using datasheet Vas = 24.1 L):**
- Cms = 924.9 µm/N (matches datasheet 920 closely!)
- Mms = 5.68 g (datasheet says 11.4 g — significant mismatch)
- Bl = 0.92 T·m (datasheet says 5.2 — way off, Vas assumption may be wrong)

**Assessment:** This is the most concerning result. Fs is 42% higher than spec
(69 vs 49 Hz), and Qts is 57% higher (0.60 vs 0.38). The Qms of 5.5 is 3× the
datasheet value. Two possible explanations:

1. **Suspension break-in:** New driver, stiff surround. ScanSpeak Discovery
   series units often need 10-20 hours of break-in before Fs drops and Q values
   settle. This is the most likely explanation — a stiff suspension raises Fs
   and Qms simultaneously, which is exactly what we see.

2. **Unit variation:** Less likely for ScanSpeak (tighter QC than GRS), but
   possible.

**Crossover impact:** The midrange operates 200-1100 Hz with 200 Hz BW4 high-pass.
Fs at 69 Hz is still well below 200 Hz, so the crossover design is not threatened.
But the higher Qts means the sealed mid chamber (5.7 L) will have a higher Qtc
and Fc than simulated. Re-run the mid chamber simulation with DATS values.

**Break-in update (5 hours, Jul 25):**

| Parameter | 0h | 5h | Δ | Datasheet | Trend |
|---|---|---|---|---|---|
| Fs | 69.41 Hz | 64.53 Hz | −7.0% | 49 Hz | ✓ dropping |
| Qts | 0.598 | 0.576 | −3.7% | 0.38 | ✓ dropping |
| Qms | 5.518 | 5.409 | −2.0% | 1.82 | ✓ dropping (slow) |
| Qes | 0.671 | 0.644 | −4.0% | 0.47 | ✓ dropping |
| Zmax | 28.75 Ω | 29.78 Ω | +3.6% | — | resonance sharpening |

The suspension is loosening — Fs dropped ~5 Hz and all Q values are falling.
Break-in is working but 5 hours is not enough. The Qms in particular is still
3× the datasheet value. Linear extrapolation suggests 15-20 more hours may
bring Fs close to spec, but break-in is non-linear and will flatten out.
Realistic expectation: Fs will settle around 55-60 Hz, Qts around 0.50-0.55.

**Action:** Continue break-in. Re-measure at 15h and 20h. If Fs has not dropped
below 60 Hz by 20h, the driver may simply have a stiffer suspension than the
datasheet sample — not necessarily a defect, but the mid chamber simulation
should use the settled DATS values, not the datasheet.

---

## SB Acoustics SB26STAC-C000-4 (tweeter)

| Parameter | DATS | Datasheet | Δ | Status |
|---|---|---|---|---|
| Fs | 658.1 Hz | 750 Hz | −12.3% | ✓ |
| Re | 3.223 Ω | 3.2 Ω | +0.7% | ✓ |
| Qms | 2.608 | 3.0 | −13.1% | ✓ |
| Qes | 1.735 | 1.78 | −2.5% | ✓ |
| Qts | 1.042 | 1.12 | −7.0% | ✓ |
| Le | 0.0 mH | 0.04 mH | — | ✓ (effectively 0) |
| Zmax | 8.07 Ω | — | — | — |

**Assessment:** Excellent match to datasheet. All parameters within 13% of spec.
Fs at 658 Hz (vs 750 spec) gives even more crossover margin at 1100 Hz LR4 —
442 Hz margin instead of 350 Hz. This is a healthy, well-built driver.

No action needed.

**Waveguide loading measurement (Jul 26):**

| Parameter | Free air | In waveguide mockup | Δ | Datasheet |
|---|---|---|---|---|
| Fs | 658.1 Hz | 631.9 Hz | −4.0% | 750 Hz |
| Qts | 1.042 | 1.082 | +3.8% | 1.12 |
| Qes | 1.735 | 1.808 | +4.2% | 1.78 |
| Qms | 2.608 | 2.692 | +3.2% | 3.0 |
| Zmax | 8.07 Ω | 8.15 Ω | +1.0% | — |
| Re | 3.22 Ω | 3.27 Ω | +1.6% | 3.2 Ω |

First impedance measurement with the tweeter mounted in the 3D-printed waveguide
mockup. Fs dropped 4% (658→632 Hz) — the waveguide adds acoustic mass loading on
the dome, lowering resonance. Qts rose 3.8% — also expected from waveguide
loading. These are small, predictable changes.

The waveguide-loaded Qts (1.08) is now within 3.4% of the datasheet free-air
value (1.12). Crossover margin: Fs = 632 Hz vs 1100 Hz LR4 = 468 Hz. Plenty.

**Conclusion:** The waveguide is acoustically transparent enough that it does not
significantly alter the tweeter's behavior. The loading is mild and predictable.
No crossover adjustment needed.

---

## Recommendations

1. **Re-run cabinet simulation** with DATS-measured T/S parameters for all three
   drivers. The 12SW's higher Qts (0.51 vs 0.43) and the 18W's much higher Fs/Qts
   will change the sealed box response.

2. **Break in the 18W/4424G00** for 10-20 hours and re-measure. The 42% Fs
   deviation is most likely new-suspension stiffness. If it doesn't settle,
   investigate further.

3. **Measure the second 12SW-4HE** to check pair matching for push-push. Match
   Fs within ~1 Hz for optimal cancellation.

4. **Crossover safe:** The 200 Hz BW4 high-pass on the midrange is well above
   Fs=69 Hz. The 1100 Hz LR4 on the tweeter is well above Fs=658 Hz. No
   crossover redesign needed based on these measurements.

5. **DATS could not compute Vas, Mms, Bl, Cms, sensitivity** because piston
   diameter was not entered (set to 0). For future measurements, enter Sd so
   DATS can compute the full parameter set. The values computed above used
   datasheet Vas as a proxy, which may not be accurate for these specific units.

---

## Files

- `assets/measurements/dats/12SW-4HE_dats.txt` — raw DATS export (344 pts, 1-20643 Hz)
- `assets/measurements/dats/18W-4424G00_dats.txt` — raw DATS export
- `assets/measurements/dats/SB26STAC-C000-4_dats.txt` — raw DATS export
- `assets/measurements/dats_impedance_plot.svg` — overlay impedance plot, all 3 drivers
