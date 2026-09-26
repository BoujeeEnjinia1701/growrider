---
doc_id: GRR-CAL-001
title: GrowRider sizing calculations
project: GrowRider
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (fit, reach, steering, mass, rack, braking, service, cost, strength screen, drive and trip time)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# GrowRider sizing calculations

On paper, GrowRider meets five of its twelve requirements, misses two and has three at risk; two cannot be verified at TRL 3. This issue applies the decisions of GRR-DDR-002 (chromoly main tubes, steerer, quill and a thicker sleeve; aluminium rack; alloy rims and bar; R2 widened; R9 split). The fit works: the two-stage seat post gives 400 to 670 mm of saddle height with 100 mm of insertion at every sliding joint, which covers the 1.10 to 1.65 m range under both fitting rules used here, and standover is 455 mm against 470 mm. The misses are mass, about 14.4 kg against the 13 kg production goal (R5; 15.3 kg in v0.1), and prototype cost, $281 for the bike against the $250 budget (R11; $243 in v0.1). Braking (R7), the fit-change time (R9) and frame life (R12, now one section above its screen instead of three) are at risk. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A2], is the line of that script's output that carries it.

> **Safety:** These calculations concern a bicycle ridden by children on roads shared with motor traffic. They are first-principles estimates for a paper proof of concept and are not a substitute for the brake, frame, fork, handlebar and seat post tests of ISO 8098 or ISO 4210. Nothing may be ridden on the strength of this note. See GRR-PRC-001, Safety.

## Scope and method

The note checks every requirement in GRR-REQ-001 v0.4 against the design in GRR-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, so the frame, wheel, seat post, stem and rack dimensions used here are the ones in the STEP files and in drawing GRR-DWG-001. Run it from the repo root with `python docs/04-calcs/sizing.py`.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Riders | 1.10 m and 19 kg (about age 6); 1.38 m and 32 kg (about age 10); 1.65 m and 60 kg (about age 14, with a margin) | Global growth references; 60 kg from GRR-REQ-001. To check against children in the target region |
| Fit | Inseam 0.45 x height. Rule A: BB to saddle top 0.88 x inseam (adult rule used at TRL 2). Rule B: saddle top to pedal at the bottom of the stroke 1.09 x inseam, so BB to saddle = 1.09 x inseam minus the 140 mm crank | Common fitting rules of thumb; rule B accounts for the crank length, which matters for small riders |
| Reach | Horizontal saddle-to-grip reach about 0.2 x height | Placeholder from GRR-REQ-001 |
| Mass center | Rider 0.18 x height above the saddle top and a quarter of the way from saddle to grips; bike at 45 % of the wheelbase ahead of the rear axle and 0.40 m high | Upright seated posture; engineering judgment |
| Grip | Tire to ground friction 0.7 dry, 0.4 loose gravel | Handbook ranges |
| Coaster brake | Hub brake torque 2.5 x the sprocket torque (2 to 3 typical, to confirm from hub data); a seated rider back-pedals with 0.5 x body weight | Assumed; no hub datasheet yet |
| Rim brake | Total pad force 5 x lever force; pad friction 0.5 dry, 0.3 on a wet alloy rim, 0.1 on a wet steel rim; braking radius 200 mm; lever force 40, 70 and 150 N for the three riders | Typical side-pull and short-reach lever; wet steel rims are known to brake poorly |
| Steel | Hi-tensile tube (seat post, stays, fork blades), yield 250 MPa (conservative), 60 MPa at 1 g as a fatigue screen for brazed, welded or clamped joints. Chromoly 4130 (main tubes, sleeve, quill, steerer), yield 435 MPa, 90 MPa at 1 g as a screen, scaled from tensile strength (about 670 against 430 MPa). 2.5 g peak bump factor; 70 % of rider weight on the saddle | Screening values, not a fatigue analysis; the chromoly screen is an assumption |
| Masses | Tubes from the model's lengths and wall sizes at 7,850 kg/m³ (steel) and 2,700 kg/m³ (aluminium rack); bought parts from typical catalog values (Table 3) | To confirm by weighing parts |
| Aluminium | Rack in 6061-T6, 110 MPa yield in the heat-affected zone of a weld | Typical design value |
| Riding | Rolling coefficient 0.02 (solid tire on gravel), CdA 0.35 m², air 1.2 kg/m³ | Handbook ranges |

## A. Fit (R1, R2)

*Table 2. Saddle height needed across the fit range [A1].*

| Rider | Inseam | Rule A (0.88 x inseam) | Rule B (1.09 x inseam minus crank) |
| --- | --- | --- | --- |
| 1.10 m | 495 mm | 436 mm | 400 mm |
| 1.38 m | 621 mm | 546 mm | 537 mm |
| 1.65 m | 742 mm | 653 mm | 669 mm |

- **Range.** The two stages give 400 to 670 mm from BB center to saddle top, a 270 mm range [A2]. The 29.2 x 1.8 mm chromoly sleeve slides 130 mm in the 31.8 x 1.2 mm seat tube (29.4 mm bore) and the 25.4 mm post slides 140 mm in the sleeve (25.6 mm bore). This covers 400 to 669 mm, the widest need under either rule, and meets the R2 target of 400 to 670 mm.
- **Insertion.** At full extension the sleeve, the post and the quill stem each keep 100 mm inside the part below [A3]. Fully lowered, the sleeve reaches 230 mm and the post 220 mm below the seat tube top, inside the 240 mm of clear bore above the BB shell [A4].
- **Standover.** The loop tube top is 455 mm above the ground 100 mm ahead of its joint with the seat tube, where a rider stands to mount [A5]. A 1.10 m rider's 495 mm inseam clears it by 40 mm. R1 is met, with a thin margin.
- **Saddle above ground.** 636 mm at the smallest setting to 890 mm at the largest [A6]. The smallest rider cannot reach the ground from the saddle and stops by sliding forward, as on any bicycle.
- **Crank length.** The 140 mm crank is 0.28 of the smallest rider's inseam and 0.19 of the largest [A7]. Small riders will pedal with a large knee bend at the top of the stroke; this is the reason for the later 127 mm option (GRR-DDR-001, D5).

Rule A, used at TRL 2, sets the smallest saddle 36 mm too high for a 1.10 m rider on 140 mm cranks. The design covers both rules, and R2 was widened from 436 to 654 mm to 400 to 670 mm to match (GRR-DDR-002, D11).

## B. Reach and handlebar height (R3)

- **Bar height.** 120 mm of quill travel along the 70° steering axis raises the bar 113 mm; the grips also move back 41 mm as they rise [B1].
- **Reach.** At the smallest setting the saddle-to-grip reach is 241 to 331 mm across the two stem head positions (0 or 60 mm) and the ±15 mm saddle rail; the placeholder need is 220 mm. At the largest setting it is 292 to 382 mm against 330 mm [B2]. Over the fit range the reach adjusts by 141 mm [B3]. R3 is met.
- **Bar above the saddle.** At the smallest setting the grips are 128 mm above the saddle top; at the largest they are 13 mm below it [B4]. The small rider sits very upright. The cause is the 180 mm head tube needed to give the quill 100 mm of insertion with 120 mm of travel; a flat bar instead of the 25 mm rise would lower it slightly, and is now a co-design question (GRR-DDR-002, D13).

## C. Wheel size and steering (R4)

- One wheel size, 20 in (ISO 406), for every rider; tire outside diameter 500 mm and rolling circumference 1.57 m [C1]. R4 is met.
- Trail is 59 mm with a 70° head angle and 30 mm fork offset [C2], in the usual range for small wheels.
- The fork crown clears the tire by 26 mm; with a 16 mm tire-to-fender gap, the fender clears the crown by 6 mm [C3]. Mud clearance is tight in the rainy season.
- Toe overlap: none for the smallest rider; about 19 mm for the largest when the bar is turned [C4]. This is normal on small-wheeled bikes but should be shown to riders.
- Pedal clearance is 109 mm; a pedal strikes at about 32° of lean [C5].

## D. Mass (R5)

The frame, from the model's tube lengths and walls, is about 2.41 kg with chromoly head, seat, down and loop tubes (seat tube 31.8 x 1.2 mm, down tube 31.8 x 0.9 mm, loop tube 28.6 x 0.9 mm) and steel stays [D1].

*Table 3. Mass estimate [D2].*

| # | Part | kg | # | Part | kg |
| --- | --- | --- | --- | --- | --- |
| 1 | Frame, chromoly main tubes | 2.41 | 11 | Chain | 0.30 |
| 2 | Fork, chromoly long steerer | 0.95 | 12 | Front brake, lever, cable | 0.35 |
| 3 | Sleeve (29.2 x 1.8 mm) and seat post | 0.68 | 13 | Rack (aluminium) | 0.44 |
| 4 | Saddle | 0.45 | 14 | Fenders (plastic) | 0.40 |
| 5 | Quill stem and head | 0.53 | 15 | Chainguard | 0.25 |
| 6 | Handlebar (alloy) and grips | 0.45 | 16 | Kickstand | 0.30 |
| 7 | Front wheel (alloy rim) | 0.95 | 17 | Reflectors and bell | 0.15 |
| 8 | Rear wheel (alloy rim), coaster hub | 1.80 | 18 | Bottom bracket and headset | 0.45 |
| 9 | Solid tires (2) | 2.20 | 19 | Hardware | 0.15 |
| 10 | Crankset and pedals | 1.15 | | **Total** | **14.4** |

The complete bike is about 14.4 kg, 1.4 kg over the 13 kg production goal and 76 % of a 19 kg six-year-old's weight [D3]. **R5 is not met.** The GRR-DDR-002 changes save 0.9 kg against v0.1 (15.3 kg) [D5]. The TRL 3 review estimated about 13.6 kg for the same changes using a flat 45 % saving on all frame tubes; the model gives less because the head tube keeps its 1.5 mm wall for the headset cups, the seat tube keeps 1.2 mm to take the thicker sleeve, the stays stay in steel, and the 1.8 mm sleeve adds 0.06 kg. The one remaining option, pneumatic tires with thorn-resistant tubes and liners, saves 0.50 kg [D4] and would reach about 13.9 kg, but reverses decision D4.

## E. Mass center and rack (R6)

- With rider, the combined mass center is 341 mm ahead of the rear axle and 647 mm high for the 1.10 m rider, 304 and 823 mm for the 1.38 m rider, and 269 and 1,035 mm for the 1.65 m rider. The front wheel carries 40, 35 and 31 % of the weight [E1].
- With 10 kg on the rack, the front wheel share falls to 32 % for the smallest rider and 29 % for the largest [E2]. A heavier load would make steering light and unsafe for a small child; this supports the 10 kg rating.
- The 300 x 120 mm platform meets the size limit. The rack is now 12 x 1.5 mm aluminium 6061-T6 tube (GRR-DDR-002, D7), 0.44 kg. Rail bending at 10 kg and 2.5 g is 26 MPa against 110 MPa for welded 6061-T6 [E3]. Welded aluminium has a low fatigue strength, so the rack joints need the static and fatigue tests of ISO 4210-2 at TRL 4. R6 is met by design; the static load test is later work.

## F. Braking (R7)

*Table 4. Braking on a dry, level road [F1] to [F4].*

| Rider | Rear (coaster) grip limit | Back-pedal force for 0.2 g, available | Coaster, achieved | Front lever force for 0.2 g, assumed | Front, achieved | Both |
| --- | --- | --- | --- | --- | --- | --- |
| 1.10 m | 0.28 g | 83 N, 93 N | 0.23 g | 33 N, 40 N | 0.24 g | 0.47 g |
| 1.38 m | 0.27 g | 115 N, 157 N | 0.27 g | 45 N, 70 N | 0.31 g | 0.58 g |
| 1.65 m | 0.26 g | 185 N, 294 N | 0.26 g | 73 N, 150 N | 0.41 g | 0.57 g |

- On paper each brake alone reaches 0.2 g and both together at least 0.47 g, so the R7 targets are met. For the smallest rider the margins are small: 12 % on back-pedal force and 21 % on lever force (slightly better than v0.1 because the bike is lighter). **R7 is at risk** until the coaster hub's brake ratio (GRR-DDR-002, D9) and children's lever and back-pedal forces are known.
- On loose gravel the coaster alone is limited to 0.19 g by rear-wheel grip for every rider [F1], so the front brake is needed.
- Pitch-over limits the largest rider to 0.57 g with the front brake [F1].
- **Wet rims.** A wet steel rim would need 164 N at the lever for 0.2 g with the smallest rider, giving a child about 0.05 g. The decided alloy front rim (GRR-DDR-002, D8) needs 55 N and gives about 0.15 g [F3]. Wet braking stays well below the dry figures, which riders need to be taught.
- Stopping from 15 km/h takes 4.4 m at 0.2 g and 2.5 m at 0.35 g, plus 4.2 m in a 1 s reaction [F5].

## G. Puncture resistance (R8)

Solid or airless tires (decision D4) cannot puncture, so the first half of R8 is met by selection. Tire life of 2,000 km depends on the compound and needs supplier data. R8 is not verifiable at TRL 3.

## H. Service and fit change (R9)

- A fit change by task analysis takes about 10 minutes: two seat post collars, the stem expander, the stem head position, a brake cable and lever check, and an insertion-mark check with a test ride [H1]. This is at the 10 minute limit.
- Fit adjustments need only a 13 mm spanner and a screwdriver; wheels and pedals need 15 mm. The 1 in threaded headset needs a 32 mm spanner and a cup-and-cone bottom bracket needs a lockring spanner [H2]. With R9 split (GRR-DDR-002, D12), the parent tool list (R9a) and the mechanic tool list (R9b) are both met [H3]. The 10 minute fit change sits at its limit and rests on a task analysis, so **R9 stays at risk.**
- The front brake housing must carry slack for 120 mm of stem travel, or every fit change also needs a cable adjustment.

## I. Parts commonality (R10)

Chain, coaster hub internals, 1 in headset, 25.4 mm seat post, 22.2 mm handlebar and 9/16 in pedal threads were chosen to match adult roadster parts. The fork needs a longer steerer than a stock 20 in fork, and the sleeve and long quill are made parts. Whether the rest are stocked in the target region needs a partner's parts list. R10 is not verifiable at TRL 3.

## J. Cost (R11)

The 20-line BOM totals $281 for the bike (lines 1 to 19) and $293 with the $12 helmet, against the $250 budget [J1]; v0.1 had $243 and $255. The chromoly frame tubes (+$18), chromoly steerer, sleeve and quill (+$12), alloy bar and rear rim (+$4) and aluminium rack (+$4) add $38. **R11 is not met** for the prototype. A budget change is proposed, awaiting Amish (GRR-DDR-002, N1); the helmet's funding is still open (O1). The $120 production target at volume (D6) needs an estimate from a regional assembler.

## K. Strength screen (R12)

A screen, not a fatigue analysis, for the largest rider (60 kg) at the largest setting.

*Table 5. Section stresses [K1] to [K4].*

| Section | Load case | Stress | Screen |
| --- | --- | --- | --- |
| Seat post at the sleeve top, 25.4 x 1.8 mm steel | 1 g saddle load, 97 mm lever | 54 MPa (136 MPa at 2.5 g) | Passes (60 MPa) |
| Sleeve at the seat tube top, 29.2 x 1.8 mm chromoly | 1 g, 148 mm lever | 61 MPa (153 MPa at 2.5 g) | Passes (90 MPa); 74 MPa in v0.1 |
| Seat tube at its clamp, 31.8 x 1.2 mm chromoly | 1 g, 148 mm lever | 72 MPa (180 MPa at 2.5 g) | Passes (90 MPa); 59 MPa at 1.5 mm in v0.1 |
| Quill at the steerer top, 22.2 x 2.0 mm chromoly | 300 N vertical and 200 N pull at the grips, full extension | 45 N m, 77 MPa | Passes (90 MPa) |
| Steerer at the crown, 25.4 x 1.6 mm chromoly | 0.41 g front braking, 589 N normal and 300 N brake force | 78 N m, 117 MPa | **Above 90 MPa** |
| Fork blades at the crown | 2.5 g bump | 53 MPa (21 MPa at 1 g) | Passes (60 MPa) |

With the decided chromoly sleeve, quill and steerer and the 1.8 mm sleeve wall (GRR-DDR-002, D10), one of six sections is above its screen, against three in v0.1; none reaches yield at the peak load [K5]. The remaining one is the standard 1 in steerer under an adult-scale rider braking hard: 117 MPa, and 98 MPa even with a 2.0 mm wall [K3]. It is proposed, awaiting Amish, to specify a 25.4 x 2.0 mm butted steerer and confirm it by the ISO 4210-2 fork tests (GRR-DDR-002, N2). The thinner chromoly seat tube raises its clamp stress from 59 to 72 MPa, inside the chromoly screen but with less margin. The chromoly screen is an assumption scaled from tensile strength; the brazed crown joint may deserve a lower value. Whether greased steel sleeves seize in dust and rain over ten years cannot be assessed by calculation. **R12 is at risk.**

## L. Drive, power and trip time

- 32/18 gives 2.79 m per crank turn, so 11 km/h is 66 rpm [L1]. The chain is 86 links [L2].
- Power on the level at 11 km/h is 26, 34 and 51 W for the three riders; a 5 % climb at 7 km/h takes 46, 63 and 101 W. On that climb the smallest rider pushes a mean pedal force of 40 % of body weight [L3], so steep hills will be walked.
- A 5 km trip takes 60 to 75 min walking and 25 to 30 min cycling [L4]. At the midpoints this returns about 79 min per day, about 249 h per 190-day school year [L5].

## M. Applicable standard

The maximum saddle height is 890 mm above the ground [M1]. ISO 8098:2023 covers bicycles for young children with a maximum saddle height of more than 435 mm and less than 635 mm; ISO 4210-2:2023 covers young adult bicycles from 635 mm to less than 750 mm and city and trekking bicycles from 635 mm up. Classified by its maximum saddle height, GrowRider falls under ISO 4210-2 as a city and trekking bicycle, even though its smallest setting (636 mm) serves riders of ISO 8098 size. The scope limits were checked on the ISO catalog pages for [ISO 8098:2023](https://www.iso.org/standard/78085.html) and [ISO 4210-2:2023](https://www.iso.org/standard/78077.html); the test loads have not been read, as the standards were not purchased.

## Results against requirements

*Table 6. Requirement status (GRR-REQ-001 v0.4), not met and at risk first.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Mass | 14.4 kg | 13 kg or less (production goal) | **Not met** |
| R11 | Cost | $281 bike, $293 with helmet; production not estimated | $250 prototype; $120 at volume | **Not met** |
| R7 | Two independent brakes | Coaster 0.23 g, front 0.24 g, both 0.47 g (smallest rider, dry); wet alloy rim about 0.15 g | 0.2 g each, 0.35 g together, dry | At risk |
| R9 | Basic tools, 10 min fit change | Parent and mechanic tool lists met; fit change 10 min | R9a: 13 mm, screwdriver, 10 min; R9b: 13, 15, 32 mm, lockring spanner, screwdriver | At risk |
| R12 | Lasts across siblings | 1 of 6 sections above its screen (steerer); seizing not assessable | 10 years, 3 riders, 60 kg plus 10 kg | At risk |
| R8 | Puncture resistance | Solid tires, no punctures; life unknown | No punctures; 2,000 km | Not verifiable at TRL 3 |
| R10 | Parts commonality | Chosen to match; no regional list | All wear parts but tires and rims | Not verifiable at TRL 3 |
| R1 | Fit the riders | 1.10 to 1.65 m; standover 455 mm | 1.10 to 1.65 m; 470 mm or less | Met |
| R2 | Saddle height | 400 to 670 mm; 100 mm insertion | 400 to 670 mm; 100 mm insertion | Met |
| R3 | Reach and bar height | Bar 113 mm; reach 141 mm | 100 mm or more each | Met |
| R4 | One wheel size | 20 in (ISO 406) | One size | Met |
| R6 | Rack | 300 x 120 mm; 26 MPa at 2.5 g (aluminium) | 10 kg, marked; 300 x 140 mm or less | Met |

Totals: 5 met, 2 not met, 3 at risk, 2 not verifiable at TRL 3 (v0.1: 5 met, 1 not met, 4 at risk, 2 not verifiable).

## Changes in v0.2

Applied from GRR-DDR-002: mass 15.3 to 14.4 kg; prototype bike cost $243 to $281 ($255 to $293 with helmet), so R11 moves from at risk to not met; sections above the strength screen 3 to 1; wet front braking for the smallest rider 0.05 to 0.15 g with the alloy rim; rack rail stress 35 MPa in steel to 26 MPa in aluminium; R2 target 436 to 654 mm to 400 to 670 mm; R9 split into R9a and R9b. Fit, reach, steering and standover are unchanged.

## Checks against earlier figures

The TRL 2 figures in GRR-PRC-001 v0.2 were checked against the script and the documents were corrected where they differed:

- Saddle range: 436 to 654 mm (rule A only) became 400 to 670 mm; the rise and setback over the range are now 254 mm and 92 mm.
- Reach adjustment: about 124 mm became 141 mm.
- Standover: about 460 mm became 455 mm.
- Mass: about 15.5 kg became 15.3 kg; the saving from pneumatic tires is about 0.5 kg, not 1 kg.
- Front brake pitch-over: 0.76 g became 0.57 to 0.81 g depending on the rider; rear coaster limits (0.27 g dry, 0.19 g gravel) are confirmed.
- Power on a 5 % climb: about 60 W became 65 W for the 1.38 m rider; the level figure (about 35 W) is confirmed at 34 W.
- Commute time and gear figures are confirmed.
