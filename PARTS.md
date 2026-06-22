# Parts — Mk2 Reference Loudspeaker

All quantities and prices are **per pair** unless noted otherwise.
Prices are indicative (sourced June 2026); verify before ordering.

---

## Drivers

| Part | Qty/pair | Unit price | Supplier | Notes |
|---|---|---|---|---|
| GRS 8SW-4HE-8 (8" woofer) | 4 | ~€45 | Parts-Express | 2 per enclosure, push-push |
| ScanSpeak 15W/4434G00 (midrange) | 2 | ~€120 | Scan-Speak / Hifi-Skabet | — |
| ScanSpeak H2606/920000 (tweeter) | 2 | ~€90 | Scan-Speak / Hifi-Skabet | Mounted in WG212 waveguide |

## Waveguide

| Part | Qty/pair | Notes |
|---|---|---|
| WG212 oblate-spheroid waveguide | 2 | 3D print from `cad/mk2_waveguide_os.scad`. **throat_d = 28 mm is placeholder** — verify against physical H2606 dome before printing final version. Use SLA/MSLA for surface finish. |

## Cabinet

| Part | Notes |
|---|---|
| 22 mm birch plywood | ~3 sheets per cabinet (verify cut list from `assets/mk2_stykliste.csv`). Standard 1220 × 2440 mm sheet. |
| PVA woodworking glue | Titebond III or equivalent |
| Wood screws + threaded inserts | For driver mounting |
| Gasket tape (closed-cell foam, 5 mm) | All driver openings |
| Damping felt/foam | Mid chamber: fully lined. Bass chamber: 50 mm rear/top/sides. |
| Terminal cup or amplifier plate cutout | Depends on DSP/amp selection |

Approximate external dimensions (v6b): **300 × 370 × 1080 mm**, 22 mm walls, R50 front roundovers.

## Electronics / DSP

Platform **not yet selected**. Three leading candidates:

| Option | Notes |
|---|---|
| **MiniDSP 4×10 HD** | Easiest integration path. USB/optical in, 10 outputs. Well-documented with REW export. |
| **Hypex FusionAmp FA123 / FA253** | Integrated DSP + plate amp. Clean install, higher cost. |
| **ADAU1452-based custom board** | Full flexibility, lowest cost at scale, requires firmware work. |

Select after prototype measurements. MiniDSP 4×10 HD is recommended for initial prototyping.

## DSP Filter Plan (v6b target)

From `assets/mk2_dsp.csv` (SB23 study reference — filter frequencies differ from v6b; use for structure only):

| Driver path | Filters |
|---|---|
| Woofer (×2) | Subsonic HP ~18 Hz LR4, Linkwitz Transform (Fc ~28 Hz, Q 0.71), LP 150 Hz LR4, polarity/delay |
| Midrange | HP 150 Hz LR4, LP 1250 Hz LR4, delay |
| Tweeter | HP 1250 Hz LR4, level trim ~-5 to -7 dB (sensitivity mismatch), delay |

**Note:** 1250 Hz crossover frequency is **unconfirmed** — depends on H2606 distortion measurement in the WG212. Fallback options: 1350 / 1450 / 1600 Hz (see `simulations/vertical_polar_map.py`).

## Open Items

- [ ] Confirm throat_d against physical H2606 → update `cad/mk2_waveguide_os.scad`
- [ ] Print WG212 prototype → fit-check against H2606 and 15W/4434G00
- [ ] Measure H2606 distortion at 1250 Hz → confirm or adjust crossover
- [ ] Confirm actual c-c spacing (nominal 140 mm; expect ~150–155 mm from physical parts)
- [ ] Select and order DSP/amplifier platform
- [ ] Finalize cut list from CAD model before ordering sheet material
