# Mk3 Prototype — Status før ferie (uge 31-33)

**Dato:** 25. juli 2026 (lørdag aften)
**Næste handling:** Første værkstedsdag efter ferie

## ✅ Hvad er klart

| Område | Status | Detaljer |
|--------|--------|----------|
| **Cabinet design** | LÅST (v9) | W300 D420 H1180, 22mm birkekrydsfiner. CAD, STL, cut-SVG, BOM alle genereret. |
| **Push-push woofers** | LÅST | 2× GRS 12SW-4HE, side-mounted, 65 L shared sealed chamber. |
| **Waveguide** | VERIFICERET | Throat 32mm ✅, recess ØD 43mm ✅ (caliper 25/7). Waveguide.scad opdateret. |
| **Crossover frekvenser** | LÅST | 200 Hz BW4 + 1100 Hz LR4. Bekræftet optimal (175 Hz testet og afvist). |
| **DSP config** | KLAR | `mk3-sb26stac-200hz-bw4.xml`. Gains W0/M-4/T-9. Subsonic 18 Hz LR4. |
| **BOM v9** | KLAR | ~EUR 800/pair aktivt. Alle driverpartnumre, tilbehør, dæmpematerialer. |
| **Bench cheat sheet** | KLAR | `docs/BENCH_CHEAT_SHEET.md` med byggeprocedure og mål. |
| **CI/CD** | GRØN | cad-r30 udgivet. 12 sims → STL → 34 renders → cut SVGs → deploy. |

## 🔬 Driver-målinger (DATS, 25. juli)

### GRS 12SW-4HE (woofer, 2 stk.)

| Parameter | Datasheet | Målt 25/7 | Forskel |
|---|---|---|---|
| Fs | 22 Hz | 22 Hz | 0% ✅ |
| Qts | 0.43 | **0.51** | +19% |
| Vas | 80.4 L | 80.4 L (antaget) | — |

**Konsekvens:** Qtc = 0.95 i 65 L (vs 0.80). Linkwitz Transform kan stadig rette til 28 Hz / Q 0.707. Kræver ~1-2 dB mere EQ-boost. **Kabinet uændret.**

Anden 12SW er ikke målt endnu — bør matches til push-push.

### ScanSpeak 18W/4424G00 (midrange)

| Parameter | Datasheet | Målt 5h BI | Målt ~15h | Målt ~20h |
|---|---|---|---|---|
| Fs | 49 Hz | 64.5 Hz | **mangler** | **mangler** |
| Qts | 0.38 | 0.58 | **mangler** | **mangler** |
| Qtc (13 L) | 0.60 | 0.91 | — | — |
| Fc (13 L) | 76.9 Hz | 101.2 Hz | — | — |

**Status:** Break-in virker (Fs faldt 69.4→64.5 på 5 timer). Skal måles ved 15h og 20h. Forventet stabilisering: Fs ~55-60 Hz, Qts ~0.50-0.55.

**Design note:** Selv med Fc=101 Hz er mid-kammeret fint da krydset er 200 Hz BW4. Ingen kabinetændring nødvendig.

### SB26STAC-C000-4 (tweeter)

| Parameter | Datasheet | Målt 25/7 | Forskel |
|---|---|---|---|
| Fs | 750 Hz | ~740 Hz | ~1% ✅ |
| Re | 3.7 Ω | 3.68 Ω | <1% ✅ |
| Qms | 3.5 | 3.1 | Acceptabelt |
| Qes | 0.63 | 0.60 | Acceptabelt |
| Qts | 0.53 | 0.50 | Acceptabelt |

**Konklusion:** Fremragende match. Ingen overraskelser.

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
