# DATS vs Datasheet — Simulation Results

**Dato:** Lørdag 25. juli 2026
**Script:** `simulations/dats_vs_datasheet_bass.py`
**Output plot:** `simulations/plots/dats_vs_datasheet_bass.png`

## Resultater

### Bass: 2× GRS 12SW-4HE (65 L sealed)

| Parameter | Datasheet | DATS Jul 25 | Forskel |
|---|---|---|---|
| Qts | 0.43 | **0.51** | +19% |
| Qtc (i 65 L) | 0.80 | **0.95** | Højere |
| Fc | 41.0 Hz | 41.0 Hz | Ingen |
| LT boost | 41→28 Hz, Q 0.80→0.71 | 41→28 Hz, Q 0.95→0.71 | Kraftigere EQ |

**Konklusion:** Den højere Qts (0.51 vs 0.43) giver en Qtc på 0.95 i stedet for 0.80. Det betyder en smallere, mere peaker respons før EQ — ca. 1-2 dB mere udstråling omkring Fc. Linkwitz Transform kan stadig rette det til 28 Hz/Q 0.707, men kræver lidt mere EQ-boost. **Acceptabelt — kabinettet behøver ikke ændres.**

### Mid: 18W/4424G00 (13 L sealed)

| Parameter | Datasheet | DATS 5h BI | Forskel |
|---|---|---|---|
| Fs | 49.0 Hz | **64.5 Hz** | +32% |
| Qts | 0.38 | **0.58** | +53% |
| Qtc | 0.60 | **0.91** | Kraftig |
| Fc | 76.9 Hz | **101.2 Hz** | +24 Hz |

**Konklusion:** Mid'en er stadig i break-in. Fc på 101 Hz vs forventet 77 Hz betyder mindre low-end headroom i mid chamber — men da krydset er 200 Hz BW4, er det **stadig fint**. ScanSpeak-spec (Fs=49, Qts=0.38) forventes at nærme sig efter 15-20h break-in. Følg op med re-måling ved 15h og 20h.

## Anbefaling

1. **Cabinet uændret** — begge driveres afvigelser er indenfor justeringsområdet for DSP
2. **18W break-in fortsætter** — re-mål ved 15h og 20h
3. **DSP config opdateres** når 18W er stabiliseret
