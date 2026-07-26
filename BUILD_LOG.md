# Build Log

This file will track the physical build of the Mk3 Reference Loudspeaker.

---

# Prototype 1

## Status

Drivers received and measured (DATS). Waveguide mockup printed and impedance-verified.
Cabinet not yet built.

## Goals

- Validate cabinet geometry
- Validate woofer fit
- Validate waveguide and 18W spacing
- Validate mid chamber volume
- Validate bracing layout
- Prepare for acoustic measurements

---

# Cabinet Build Notes

## External dimensions

- Width: 300 mm
- Depth: 420 mm
- Height: 1180 mm
- Material: 22 mm birch plywood
- Front vertical roundovers: R19

## Bass placement

- Woofer centers: approx. 520 mm from bottom (both sides, opposed at the same height)
- Configuration: side-mounted push-push, opposed + coupling block (see Chapter 8)

## Mid/tweeter layout

- ScanSpeak 18W/4424G00 midrange at TOP of baffle
- Waveguide/tweeter BELOW midrange
- Target c-c spacing: 165 mm (DD-016)

---

# Assembly Checklist

- [ ] Cut panels
- [ ] Cut braces
- [ ] Build mid chamber
- [ ] Test fit waveguide
- [ ] Test fit midrange
- [ ] Test fit woofers
- [ ] Install threaded inserts
- [ ] Glue cabinet
- [ ] Add internal damping
- [ ] Install drivers
- [ ] Wire drivers
- [ ] Install DSP/amplifier
- [ ] Run polarity test
- [ ] Run first measurements

---

# Measurement Log

Use this section for real measurement notes.

## Date

Jul 25-26, 2026

## Setup

Dayton Audio Test System (DATS), free air impedance measurements.
All 3 driver types measured before and after break-in.

## Results

### GRS 12SW-4HE (woofer #1)
- 0h: Fs=25.1, Qts=0.51
- 5h: Fs=23.5, Qts=0.44
- 10h: Fs=23.3, Qts=0.46 (break-in complete)
- Re elevated to 4.40 Ω (cold recheck needed)

### ScanSpeak 18W/4424G00 (midrange)
- 0h: Fs=69.4, Qts=0.60 (stiff new suspension)
- 5h: Fs=64.5, Qts=0.58 (break-in progressing, needs more)
- Still ~30% above spec on Fs. Continue to 15-20h.

### SB26STAC-C000-4 (tweeter)
- Free air: Fs=658, Qts=1.04 (excellent match to spec)
- In waveguide mockup: Fs=632, Qts=1.08 (mild loading, as expected)
- Waveguide acoustically transparent. Crossover margin 468 Hz.

### Physical dimensions (SB26STAC, caliper-verified Jul 25)
- Throat: 32 mm (was 28 mm in CAD — corrected)
- Recess: 43 mm (was 53 mm — corrected)
- All other dims within tolerance of datasheet

Full analysis: `docs/15_measurements.md`

---

# Issues Found

Document all mechanical/acoustic problems here.

---

# Fixes

Document all fixes and revisions here.
