# Mk3 Prototype — Status før ferie (uge 31-33)

**Dato:** 25. juli 2026 (lørdag aften)
**Næste handling:** Første værkstedsdag efter ferie

## ✅ Hvad er klart

| Område | Status | Detaljer |
|--------|--------|----------|
| **Cabinet design** | LÅST (v9) | W300 D420 H1180, 22mm birkekrydsfiner. CAD, STL, cut-SVG, BOM alle genereret. |
| **Push-push woofers** | LÅST | 2× GRS 12SW-4HE, side-mounted, 65 L shared sealed chamber. |
| **Waveguide** | VERIFICERET | Throat 32mm ✅, recess ØD 43mm ✅ (caliper 25/7). Waveguide.scad opdateret. Mockup printet og impedans-målt. |
| **Crossover frekvenser** | LÅST | 200 Hz BW4 + 1100 Hz LR4. Bekræftet optimal (175 Hz testet og afvist). |
| **DSP config** | KLAR | `mk3-sb26stac-200hz-bw4.xml`. Gains W0/M-4/T-9. Subsonic 18 Hz LR4. |
| **BOM v9** | KLAR | ~EUR 800/pair aktivt. Alle driverpartnumre, tilbehør, dæmpematerialer. |
| **Bench cheat sheet** | KLAR | `docs/BENCH_CHEAT_SHEET.md` med byggeprocedure og mål. |
| **CI/CD** | GRØN | cad-r32 udgivet. 12 sims → STL → 34 renders → cut SVGs → deploy. Auto-release aktiveret. |

## 🔬 Driver-målinger (DATS, 25. juli)

### GRS 12SW-4HE (woofer, 2 stk.)

| Parameter | Datasheet | Målt 0h | Målt 5h | Målt 10h | Forskel (10h) |
|---|---|---|---|---|---|
| Fs | 22 Hz | 25.1 Hz | 23.5 Hz | 23.3 Hz | +5.7% ✅ |
| Qts | 0.43 | 0.51 | 0.44 | 0.46 | +7.3% ✅ |
| Re | 3.7 Ω | 4.20 Ω | 4.23 Ω | 4.40 Ω | +18.9% ⚠ (kold recheck) |
| Vas | 80.4 L | 80.4 L (antaget) | — | — | — |

**Konsekvens:** Qtc = 0.88 i 65 L (vs 0.80 datasheet). Linkwitz Transform kan stadig rette til 28 Hz / Q 0.707. **Kabinet uændret.** Break-in færdig efter 10h.

Anden 12SW er ikke målt endnu — bør matches til push-push.

### ScanSpeak 18W/4424G00 (midrange)

| Parameter | Datasheet | Målt 0h | Målt 5h | Proj. 10h | Proj. 15h | Proj. 20h |
|---|---|---|---|---|---|---|
| Fs | 49 Hz | 69.4 Hz | 64.5 Hz | 61.6 Hz | 59.8 Hz | 58.7 Hz |
| Qts | 0.38 | 0.598 | 0.576 | 0.559 | 0.546 | 0.535 |
| Qtc (13 L) | 0.60 | 0.94 | 0.91 | 0.88 | 0.86 | 0.84 |
| Fc (13 L) | 76.9 Hz | 109.0 Hz | 101.2 Hz | 96.7 Hz | 93.9 Hz | 92.0 Hz |

**Estimater baseret på eksponentiel decay-model** (se `simulations/plots/breakin_projection.png`):
- **Optimistisk scenarie** (Fs→57, Qts→0.50): τ_Fs=10h, τ_Qts=20h. 90% efter ~23h (Fs) og ~45h (Qts).
- **Konservativt scenarie** (Fs→60, Qts→0.55): τ_Fs=6.8h, τ_Qts=8.2h. 90% efter ~16h (Fs) og ~19h (Qts).
- **Reelt estimat:** Forvent Fs ~55-60 Hz, Qts ~0.50-0.55 efter 20-25h break-in.

**Break-in plan:**
| Milestone | Handling |
|---|---|
| 10h (1. session efter ferie) | Re-mål DATS |
| 15h (2. session) | Re-mål DATS — forvent 70-80% af total ændring |
| 20h (3. session) | Re-mål DATS — forvent ~90% settled. Herefter kan DSP biquads regnes. |

Næste 5h break-in blok giver ~3 Hz Fs-forbedring (5→10h). Derefter aftager udbyttet: 10→15h giver ~2 Hz, 15→20h giver ~1 Hz.

**Design note:** Selv med Fc=101 Hz (5h) er mid-kammeret fint da krydset er 200 Hz BW4. Ingen kabinetændring nødvendig.

### SB26STAC-C000-4 (tweeter)

| Parameter | Datasheet | Målt fri luft | I waveguide | Forskel |
|---|---|---|---|---|
| Fs | 750 Hz | 658 Hz | 632 Hz | −12% / −16% ✅ |
| Re | 3.2 Ω | 3.22 Ω | 3.27 Ω | <1% ✅ |
| Qts | 1.12 | 1.04 | 1.08 | −7% / −4% ✅ |

**Konklusion:** Fremragende match. Waveguide loading mild (Fs −4%, Qts +3.8%). Crossover margin 468 Hz (632 vs 1100 Hz LR4). Ingen justering nødvendig.

### Fysiske mål (SB26STAC, caliper 25/7)
- Throat: 32 mm (var 28 mm i CAD — rettet)
- Recess: 43 mm (var 53 mm — rettet)
- Alle øvrige mål inden for tolerance
- Waveguide.scad opdateret og pushed

## 📋 Mangler efter ferien (uge 34 →)

### 🔴 Skal gøres før prototype

| # | Opgave | Estimeret tid | Note |
|---|---|---|---|
| 1 | **18W break-in færdiggør** (15h + 20h måling) | 1 døgn | Start når du er hjemme. Re-mål DATS efter hver session. |
| 2 | **Mål anden GRS 12SW** | 15 min | Skal matche første (Qts indenfor ±0.03 for push-push). |
| 3 | **Opdater DSP biquads** med endelige DATS-værdier | 1 time | Script: `generate_minidsp_xml.py`. |
| 4 | **SB26STAC distortion test** ved 1100 Hz | 30 min | Bekræft at krydset er sikkert. |

### 🟡 Prototype-byg

| # | Opgave | Note |
|---|---|---|
| 5 | Indkøb materialer (BOM v9) | ~EUR 800. 22mm birkekrydsfiner + dæmpematerialer + skruer/lim. |
| 6 | Skær cabinet-paneler | Cut SVGs i `cad/cut/`. CNC eller håndværktøj. |
| 7 | Montér kabinet | Lim/skru, dæmpematerialer, divider-plade, waveguide. |
| 8 | Montér drivere | Push-push 12SW, 18W, SB26STAC. |
| 9 | Indmåling og DSP-tuning | REW-måling i stuen. Justér PEQ. |

### 🔵 Når prototypen spiller

| # | Opgave |
|---|---|
| 10 | Distortion + max SPL test |
| 11 | Kabinet-resonans test (accelerometer) |
| 12 | Endelig DSP config færdiggør |
| 13 | Byg nummer to |

## 📈 Hvad pipeline gør i ferien

- **Outlook pipeline** — kører hver 3. time hverdage: invoices → info@, spam filtreres, drafts forberedes. **Config issue:** nogle invoices går stadig til lb@ — kan ikke rettes uden Make-adgang.
- **Defender incident 23** — stadig ulæst (dag 15). Skal tjekkes.
- **CodeTwo SIU** — afventer din handling.
- **Milair-history-proxy** — kører stabilt (3,174 rows / 447 aircraft).
- **Stock monitoring** — næste automatiske check mandag morgen.

## 🔗 Nøgle-filer

| Fil | Formål |
|---|---|
| `docs/BOM_v9.md` | Indkøbsliste |
| `cad/cabinet.scad` | Cabinet source of truth |
| `assets/datasheets/` | Datasheets + STEP |
| `simulations/DATS_FINDINGS.md` | DATS resultater |
| `dsp/mk3-sb26stac-200hz-bw4.xml` | DSP config |
| `docs/BENCH_CHEAT_SHEET.md` | Værkstedsprocedure |
