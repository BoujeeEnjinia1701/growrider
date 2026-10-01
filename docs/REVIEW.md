# Review note: GrowRider

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (GRR-PRB-001 v0.2): problem, users and context (child riders, parents, schools, NGOs and distribution programs, local mechanics), constraints, out of scope, prior work, open questions. The co-design checklist is kept unchanged.
- `docs/03-requirements.md` (GRR-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, planned verification and stated assumptions.
- `docs/02-concept.md` (GRR-PRC-001 v0.2): how it works, 17 numbered components, fit and commute-time numbers with assumptions, braking and power estimates, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of a step-through child's bicycle built from tubes (frame, fork, wheels, tires, telescoping seat post shown extended, telescoping stem, handlebar, saddle, crankset, chain line, front brake, rack, fenders, chainguard, kickstand, reflectors). Scale reference: a 1.35 m child (`human_figure(height=1350)`) passed as a context part with `scale_figure=False`, chosen because it shows the fit better than the 1.75 m adult. No cutaway (`cut=False`), since the inside of a bicycle does not add information.
- `media/`: hero, blueprint sheet (PNG and PDF), exploded view with BOM callouts, growth and hand-down flow diagram, `model.glb` and `viewer.html`.
- `bom/bom.csv`: 20 lines with indicative prices; lines 1 to 17 match the exploded view callouts, 18 to 20 are not modeled. `bom/bom-notes.md` explains totals and commonality.
- `README.md`: hero image and links to the viewer, blueprint and this note.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Fit range | 1.10 to 1.65 m riders; saddle height 436 to 654 mm | R1, R2 met |
| Standover | about 460 mm with 20 in wheels | R1 met, thin margin (about 510 mm with 24 in, not met) |
| Reach and bar height adjustment | about 124 mm and 113 mm | R3 met; reach need rests on an assumed 0.2 x height |
| Mass | about 15.5 kg | **R5 (13 kg) not met** |
| Coaster brake alone | about 0.27 g dry, 0.19 g on loose gravel | R7 met dry, marginal on gravel; front brake needed |
| School trip, 5 km | 25 to 30 min cycling vs 60 to 75 min walking; 60 to 100 min saved per day | Motivation |
| Prototype parts cost | about $243 for the bike, $255 with helmet | R11 met for the bike; $5 over with the helmet |

Requirements not met or at risk:

- **R5 mass:** about 15.5 kg against 13 kg. Solid tires, twin down tubes, rack and fenders all add weight.
- **R10 parts commonality:** met in intent for wear parts, but tires and rims are not a roadster size with either 20 in or 24 in wheels. Commonality is unverified until a partner supplies a regional parts list.
- **R11 cost:** within budget without the helmet, $5 over with it.
- **R12 lifespan:** unverified. Seizing of the sliding joints in dust is the main risk.

### Proposed, awaiting Amish

1. Wheel size: 20 in (ISO 406), recommended, or 24 in (ISO 507), which fails standover for 1.10 m riders. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-001)
2. Brakes: coaster brake plus front rim brake, recommended; alternatives are coaster only or two hand brakes. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-001)
3. Frame: step-through with twin down tubes, recommended, or a small diamond frame. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-001)
4. Tires: solid or airless, recommended for the prototype, or thorn-resistant tubes with liners (about 1 kg lighter and $10 cheaper). **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-001)
5. Helmet (still proposed, awaiting Amish; no recommendation): supply one with each bike (BOM line 20). Either fund it from the $250 budget ($5 over), fund it separately, or raise the budget to about $275. The budget in `project.yaml` is unchanged at $250.
6. Crank length: one 140 mm length for the prototype, with a possible 127 mm swap for the smallest riders later. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-001)
7. Production cost target of $120 or less at volume (R11): **decided by Amish, 2026-09-25: go with recommendation** (GRR-DDR-001, D6). First partner and region (a distribution NGO or school network, in Zambia, Kenya or Malawi): still proposed, awaiting Amish.

### Safety concerns

- Child riders on shared roads: two independent brakes, reflectors and a bright frame are required, and a light is suggested for dawn and dusk trips.
- Telescoping seat post and stem must never be raised past minimum insertion; marks plus a positive stop are proposed.
- The 10 kg rack rating protects the child. The design must discourage carrying passengers and water, and the documents must not describe it as a cargo or water bike.
- Bike mass is about three quarters of a six-year-old's body weight.
- Nothing has been built or tested. Frame, fork, rack and brakes need tests to ISO 8098 or ISO 4210 before anyone rides it.

### Suggestions (not added to the repo)

- A hub dynamo light as an option for dark commutes.
- A school fit-check card: a simple chart that maps a child's height to seat post and stem marks.

### Recommended next step

Review this note and the media, and decide the proposed items above, especially wheel size and brakes. If approved, run `/advance-trl3` to check the fit geometry, braking, frame loads and mass by calculation, and to produce the parametric model and drawing sheet. In parallel, find a partner for co-design so the anthropometric and parts-commonality assumptions can be tested.

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." GrowRider now claims TRL 3 (proof of concept on paper). TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (GRR-DDR-001 v0.1): six TRL 2 review items with a recommendation recorded as decided by Amish, 2026-09-25, and four items that stay open.
- `docs/04-calcs/01-sizing.md` (GRR-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: fit under two saddle-height rules, seat post and quill insertion and bore depth, standover, reach and bar height, trail, crown and fender clearance, toe overlap, pedal clearance, mass from the model's tubes, rider-plus-bike mass center, rack, braking (grip limits, coaster back-pedal force, rim brake lever force dry and wet), service task analysis, BOM total, a strength screen of six sections, drive, power, trip time and the applicable ISO standard. The script imports the model's `PARAMS` and prints every number the note quotes, tagged [A1] to [M1].
- `cad/src/model.py`: parametric build123d model (frame, fork with long steerer, two-stage seat post, saddle, quill stem with two-position head, handlebar, wheels, solid tires, crankset, chain, front brake, rack, fenders, chainguard, kickstand, reflectors) with rider settings. Exports `cad/step/growrider-small.step`, `growrider-large.step`, `frame.step`, `fork.step`, `seat-post-assembly.step`, `stem-and-bar.step`, `rack.step` and matching STL files in `cad/stl/`.
- `cad/src/sheets.py` and `cad/drawings/GRR-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:10, ortho views at the largest setting with overall length and height, wheelbase, BB height, standover, width and bar width drawn from the model; isometric at the smallest setting; a main-dimensions box. The sheet carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet remains GRR-DWG-010, so DWG-001 was free for the general arrangement.
- `bom/bom.csv` and `bom/bom-notes.md`: all 20 lines priced with a supplier type; specs updated to the model.
- `cad/src/concept_media.py` now builds the media from `model.py` (bike set for a 1.38 m rider beside a 1.35 m child), with key figures from GRR-CAL-001. All media in `media/` were regenerated and checked by eye; the temporary `media/_views*` folders were deleted.
- GRR-PRB-001, GRR-PRC-001 and GRR-REQ-001 revised to v0.3 (decisions recorded, numbers replaced by GRR-CAL-001, requirement status column); `README.md` updated to TRL 3 with links; `project.yaml` set to `trl: 3`, `trl_target: 3`, with the evidence files listed. PDFs are in `docs/pdf/`.

### Requirements (GRR-CAL-001, Table 6)

5 met, 1 not met, 4 at risk, 2 not verifiable at TRL 3.

| ID | Status | Value against target |
| --- | --- | --- |
| R5 | **Not met** | 15.3 kg against 13 kg; 81 % of a 19 kg six-year-old. All five saving options together reach about 13.1 kg |
| R7 | At risk | Smallest rider, dry: coaster 0.22 g (85 N back-pedal force needed, about 93 N available), front 0.24 g, both 0.46 g. Wet steel rim about 0.05 g |
| R9 | At risk | Fit change about 10 min with a 13 mm spanner and a screwdriver; headset needs a 32 mm spanner and the BB a lockring spanner |
| R11 | At risk | $243 for the bike, $255 with the helmet (helmet funding open); production cost not estimated |
| R12 | At risk | 3 of 6 sections above the 60 MPa fatigue screen at 1 g: sleeve at the seat tube top 74 MPa, quill at full extension 77 MPa, steerer in hard braking 117 MPa; none above yield. Seizing of sliding joints not assessable |
| R8 | Not verifiable at TRL 3 | Solid tires cannot puncture; tire life needs supplier data |
| R10 | Not verifiable at TRL 3 | Parts chosen to match roadsters; needs a regional parts list |
| R1 | Met | 1.10 to 1.65 m; standover 455 mm against 470 mm (40 mm below the smallest inseam) |
| R2 | Met | Saddle 400 to 670 mm; 100 mm insertion at every sliding joint |
| R3 | Met | Bar height 113 mm; reach 141 mm |
| R4 | Met | 20 in (ISO 406) |
| R6 | Met | 300 x 120 mm platform; 35 MPa at 10 kg and 2.5 g |

Other key numbers: trail 59 mm; fork crown to fender 6 mm; toe overlap up to 19 mm for the largest rider; grips 128 mm above the saddle at the smallest setting; gear 2.79 m per turn (66 rpm at 11 km/h); 34 W on the level and 65 W on a 5 % climb for a 1.38 m rider; about 79 min a day returned on a 5 km trip. The adult fitting rule used at TRL 2 put the smallest saddle 36 mm too high for 140 mm cranks; the design now covers the crank-corrected rule too. Every TRL 2 number in the docs was checked against the script and corrected where it differed (GRR-CAL-001, "Checks against earlier figures").

### Decisions recorded (GRR-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 20 in (ISO 406) wheels; D2 coaster brake plus front rim brake; D3 step-through frame with twin down tubes; D4 solid or airless tires for the prototype; D5 one 140 mm crank length for the prototype; D6 production cost target $120 or less at volume. No requirement target was relaxed or redefined; `budget_usd` stays at $250 and the pitch and problem lines are unchanged (no rewording was recommended). The SwapCell decisions do not apply to GrowRider.

D6 was read as carrying a recommendation because the TRL 2 note proposed the $120 figure itself; if Amish did not mean to fix it, it reverts to proposed.

### Proposed, awaiting Amish (items 3 to 9 decided on 2026-09-25, see GRR-DDR-002)

Still open from TRL 2 (no recommendation was made):

1. Helmet funding (O1): from the $250 budget ($5 over), funded separately, or a budget of about $275.
2. First partner (O2) and first region (O3). Per Amish's portfolio instruction, co-design partners are picked per area later (O4).

New from TRL 3:

3. **Mass (R5).** Options: (a) relax R5 to 15.5 kg for the prototype and keep the decided solid tires; (b) adopt chromoly main tubes, an aluminium rack, alloy rims and bar (about 13.6 kg, some added cost), keeping solid tires; (c) all of (b) plus pneumatic tires with liners (about 13.1 kg), which reverses D4. Recommendation: (b), and keep R5 at 13 kg as the production goal. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)
4. **Alloy front rim (R7).** Specify an alloy front rim, since a wet steel rim gives a child about 0.05 g. Recommendation: adopt; BOM line 7 already prefers alloy at the same price. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)
5. **Coaster hub data (R7).** Get the brake ratio of a regional coaster hub; the smallest rider's margin rests on an assumed ratio of 2.5. Recommendation: do this before any further brake work. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)
6. **Strength (R12).** Specify chromoly or thicker-walled sleeve, quill and steerer, or limit the maximum extension. Recommendation: chromoly steerer and quill, and a 1.8 mm wall sleeve; recheck in GRR-CAL-001. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)
7. **R2 target.** Widen R2 to 400 to 670 mm to match the crank-corrected fit rule the design already meets. Recommendation: adopt. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)
8. **R9 tools.** Either add a 32 mm headset spanner and a BB lockring spanner to R9 for mechanics, or keep R9 for parents' fit changes only. Recommendation: split R9 into a parent tool list (13 mm spanner, screwdriver) and a mechanic tool list. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)
9. **Low bar option.** Offer a flat bar for the smallest riders, since the grips sit 128 mm above the saddle at the smallest setting. Recommendation: note as a co-design question. **Decided by Amish, 2026-09-25: go with recommendation.** (GRR-DDR-002)

### Safety concerns

- Child riders on shared roads; nothing built or tested. The applicable standard by saddle height is ISO 4210-2 (city and trekking), whose tests assume adult riders.
- Braking margins for a 1.10 m rider are small on paper, the coaster brake is lost if the chain comes off, and a wet steel rim barely brakes.
- Sliding joints at full extension carry the highest stresses; minimum insertion marks and positive stops are required, and clamp slots are pinch points.
- The bike is about 81 % of a six-year-old's weight; 10 kg on the rack cuts the front wheel load from 40 % to 33 % for the smallest rider.
- Toe overlap for the largest riders; 6 mm fender-to-crown clearance can pack with mud and lock the front wheel.

### Other notes

- No existing TRL 4 material was found (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created. STANDARDS section 9 asks for a TRL change to be recorded in the build log; no build-log entry was written, since the brief did not name one.
- Citations: no unchecked citations were listed at TRL 2. The ISO 8098 and ISO 4210-2 saddle height scopes quoted in GRR-CAL-001 and GRR-PRB-001 were checked on the ISO catalog pages; the standards' test loads were not read. BOM prices are indicative estimates by supplier type, not quotes. Rider masses, lever and back-pedal forces, the coaster brake ratio and catalog part masses are assumptions stated in GRR-CAL-001, Table 1.

### Recommended next step

Stay at TRL 3. TRL 4 is on hold by Amish's instruction. Decide items 3 to 8 above, starting with mass and the alloy rim, get coaster hub brake data and catalog masses for the tires, rims and hub, then revise GRR-CAL-001, the model and the BOM on paper. In parallel, a co-design partner is needed to test the fit assumptions and supply a regional parts list.

For reference only, TRL 4 would need: a lab test report (TST, `environment: lab`) on a built frame, fork and seat post (ISO 4210-2 frame and fork fatigue and impact, seat post and stem tests, brake performance with child-level forces, rack static load), weighing, a timed fit change, build-log entries, and the purchasing and build work that goes with them. None of this has been started.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item above with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (GRR-DDR-002 v0.1). Items without a recommendation stay proposed. `trl` and `trl_target` stay at 3.

### Decisions applied and what changed

| # | Decision | Change in the repo | Before | After |
| --- | --- | --- | --- | --- |
| D1 to D6 | Wheel, brakes, frame, tires, crank, $120 production target (GRR-DDR-001) | Confirmed; no further change | | |
| D7 | Mass option (b): chromoly main tubes, aluminium rack, alloy rims and bar; solid tires kept; R5 kept at 13 kg as the production goal | `model.py` walls and rack; BOM lines 1, 6, 8, 13; R5 restated | 15.3 kg | 14.4 kg (the TRL 3 note had estimated 13.6 kg) |
| D8 | Alloy front rim | BOM line 7; R7 text | Wet front braking, smallest rider, 0.05 g (steel) | 0.15 g (alloy) |
| D9 | Get the coaster hub brake ratio first | Open action; needs hub maker or partner data. Any purchase or bench test is TRL 4, on hold | Assumed ratio 2.5 | Unchanged until data arrives |
| D10 | Chromoly steerer and quill, 1.8 mm sleeve wall | Sleeve 28.6 x 1.5 to 29.2 x 1.8 mm chromoly; seat tube 1.5 to 1.2 mm wall for a 29.4 mm bore; chromoly screen 90 MPa added to GRR-CAL-001 | 3 of 6 sections above screen (sleeve 74, quill 77, steerer 117 MPa) | 1 of 6 (steerer 117 MPa against 90 MPa); sleeve 61, quill 77, seat tube 72 MPa pass |
| D11 | Widen R2 | GRR-REQ-001 | 436 to 654 mm | 400 to 670 mm (met) |
| D12 | Split R9 | GRR-REQ-001 (R9a parent, R9b mechanic) | Tools at risk | Both tool lists met; 10 min fit change at the limit |
| D13 | Low bar as a co-design question | GRR-PRB-001 and GRR-PRC-001 open questions | | |

Cost: the BOM rose from $243 to $281 for the bike and from $255 to $293 with the helmet (+$38: frame +$18, steerer, sleeve and quill +$12, bar and rear rim +$4, rack +$4). `budget_usd` stays at $250, since no budget recommendation existed; a change is proposed below.

Files changed: `cad/src/model.py` (and STEP and STL re-exported), `cad/src/sheets.py` and GRR-DWG-001 at Rev P2, `cad/src/concept_media.py` and all of `media/`, `docs/04-calcs/sizing.py`, GRR-CAL-001 v0.2, GRR-REQ-001 v0.4, GRR-PRC-001 v0.4, GRR-PRB-001 v0.4, `bom/bom.csv`, `bom/bom-notes.md`, `project.yaml` (evidence list), `README.md`, and GRR-DDR-002 v0.1 (new). The README gained the sections Concept rationale, Burning platform, Where it could be used and What sparked the idea; the inspiration point is the Bihar Chief Minister's Bicycle program (2006) and its evaluation by Muralidharan and Prakash (2017). All PDFs, drawings and media were regenerated so none shows the old domain.

### Requirement status (GRR-CAL-001 v0.2)

5 met, 2 not met, 3 at risk, 2 not verifiable at TRL 3 (was 5, 1, 4, 2).

| ID | Status | Value against target |
| --- | --- | --- |
| R5 | **Not met** | 14.4 kg against the 13 kg production goal (was 15.3 kg); pneumatic tires would reach about 13.9 kg but reverse D4 |
| R11 | **Not met** | $281 bike, $293 with helmet, against $250 (was $243 and $255, at risk) |
| R7 | At risk | Smallest rider, dry: coaster 0.23 g, front 0.24 g, both 0.47 g; hub ratio still assumed |
| R9 | At risk | Tool lists met; fit change 10 min, at the limit |
| R12 | At risk | Steerer 117 MPa against the 90 MPa chromoly screen; seizing not assessable |
| R8 | Not verifiable at TRL 3 | Tire life needs supplier data |
| R10 | Not verifiable at TRL 3 | Needs a regional parts list |
| R1, R2, R3, R4, R6 | Met | Standover 455 mm; saddle 400 to 670 mm; bar 113 mm and reach 141 mm; 20 in; rack 26 MPa in aluminium |

### Still awaiting Amish

1. O1 Helmet funding (no recommendation).
2. O2 First partner and O4 co-design partner (picked per area later).
3. O3 First region (no recommendation).
4. ~~N1 (new) Prototype budget~~ **Decided by Amish, 2026-09-26: budget top-up to $300** (see the session below).
5. N2 (new) Steerer: specify a 25.4 x 2.0 mm butted chromoly steerer (98 MPa, still above the screen) and confirm by the ISO 4210-2 fork tests. Recommendation: adopt, and accept that the fork test decides.

### Cross-repo actions

None. No decision for GrowRider needs another repo to change.

### Safety

- The aluminium rack is new: welded aluminium has low fatigue strength, so the rack needs static and fatigue tests before any use.
- The thinner chromoly tubes depend on competent brazing or TIG welding; a local builder used to hi-tensile steel may not have it.
- Wet braking with the alloy rim (about 0.15 g for the smallest rider) is still well below dry braking.
- Nothing has been built or tested; nothing may be ridden.

### TRL 4

TRL 4 remains on hold by Amish's instruction. D9 (hub data) and the tests named above are recorded but not started; no build, test, purchasing or build-log work was done.

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to fix the weaker sources and approved the budget top-up ("I am ok with the budget top ups").

### Sources

Three rows of "By country or region" in `README.md` had no citation. Each was rewritten to state only what a verified source supports:

| Row | Old source | New source |
| --- | --- | --- |
| Andean and rural Latin America (Peru, Bolivia) | None | Replaced by Latin America (Bogotá, Colombia): [Alcaldía de Bogotá](https://bogota.gov.co/mi-ciudad/educacion/movilidad-en-bogota-al-colegio-en-bici-beneficios-para-estudiantes), Al Colegio en Bici and the city's other guided school-travel programs, more than 9,000 students from 147 public schools (2024) |
| Southeast Asia (Cambodia, Myanmar) | None | Narrowed to Cambodia: [Agence Kampuchea Presse](https://www.akp.gov.kh/post/detail/374647), 200 donated bicycles for pupils of five schools in Banteay Meanchey province who had walked several kilometres a day (July 2026) |
| Netherlands and other high-income cycling countries | None | [Veldman, Westerbroek and Singh, *Transportation Research Interdisciplinary Perspectives*, 2026](https://doi.org/10.1016/j.trip.2026.101998): 64 % of Dutch primary school children in the study cycled to school at least once a week. The claim "children ride to school daily" was dropped |

The other sources (UNESCO, WHO, Muralidharan and Prakash in the *American Economic Journal: Applied Economics*, NBER) are primary and were kept. The inspiration (Bihar Chief Minister's Bicycle program and its peer-reviewed evaluation) already rests on primary sources and is unchanged.

### Budget

- `project.yaml`: `budget_usd` 250 to 300.
- `docs/04-calcs/sizing.py` now reads the budget from `project.yaml` and was re-run: [J1] $281 bike, $293 with helmet, against $300; R11 moves from not met to at risk (prototype within budget; the $120 production target is not yet estimated). Totals: 5 met, 1 not met, 4 at risk, 2 not verifiable.
- GRR-CAL-001 v0.3, GRR-REQ-001 v0.5, GRR-PRC-001 v0.5 and GRR-PRB-001 v0.5 record the new budget and R11 status; GRR-DDR-002 v0.2 records "Budget top-up to $300: decided by Amish, 2026-09-26" against N1 and notes that the $293 total with the helmet now fits (O1's funding question).
- `README.md`: budget badge line and cost sentences updated to $300.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo on 2026-09-26 for the first batch of product renders. This session adds an appearance model for photoreal renders; it does not change the design, the calculations or the BOM.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 75 parts (74 bike parts in the "shell" and "internal" groups and one "context" part), with `TITLE` and three `RENDER_VIEWS`: "hero" (front right, about 22 deg elevation, with the rider), "exploded" (front right, about 28 deg) and "detail" (bike alone, front right, about 14 deg, framing the adjustable frame). Every main dimension and interface comes from `PARAMS`, `derived()` and the point helpers in `cad/src/model.py`, which is unchanged.
- The appearance model adds:
  - a painted frame (kit accent #0F766E) with rear dropouts, a kickstand plate and a head badge;
  - the two-stage seat post (graphite sleeve, chrome post) and the chrome quill with split clamp collars, 13 mm bolts and painted height scales on the exposed sleeve and quill;
  - a shaped vinyl saddle with base, rails and clamp;
  - alloy rims with brake tracks, laced spokes (28 front, 36 rear, as in the BOM) with nipples, hubs, axle nuts and the coaster brake arm; solid tires with a cut tread;
  - a toothed 32T chainring and 18T sprocket, an 86-link chain, shaped cranks, platform pedals with reflectors;
  - a side-pull caliper with pads, the short-reach lever and a cable housing;
  - the aluminium rack with a raised "MAX 10 kg" rating plate, fenders with side lips, stays and a mud flap, the chainguard with the name raised on it, kickstand, reflectors and bell;
  - a clay mannequin of a 1.30 m child (about age 8), group "context", riding the bike set for that height (saddle 505 mm from the BB, stem raised 45 mm), fitted so the seat meets the saddle, the hands meet the grips and the feet meet the pedals.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced later by the orchestrator.
- Self-check previews (matplotlib, not committed): `/tmp/growrider-prod/prev-hero.png`, `prev-exploded.png`, `prev-detail.png`.

### Differences from model.py (appearance only)

1. Spoke count: the massing model draws 18 spokes per wheel; the appearance model uses the BOM counts (28 front, 36 rear). No decision needed.
2. Rider setting shown: the renders show the bike set for a 1.30 m rider; the concept media show 1.38 m. Proposed, awaiting Amish. Recommendation: keep 1.30 m for the product renders (the child mannequin reads as a younger rider) and 1.38 m for the concept sheet.
3. Frame colour: kit accent teal (#0F766E) instead of the blue (#2E5E8C) of the concept media. The precis proposes a bright frame for road visibility. Proposed, awaiting Amish. Recommendation: use teal for the portfolio renders and settle the production colour in co-design, with a high-visibility option.
4. Painted height scales on the exposed sleeve and quill (a band every 20 mm, a longer band every 60 mm): not in the model or the BOM. Proposed, awaiting Amish. Recommendation: adopt; a teacher or mechanic can note a child's setting and reset it quickly, which helps the at-risk fit-change time.
5. Rear dropouts drawn as rear-facing track ends for chain tension on the single-speed coaster hub; the massing model has plain blocks. Proposed, awaiting Amish. Recommendation: adopt, as on regional roadsters.
6. Markings: the name "GrowRider" on the chainguard and a head badge are not in the BOM. Proposed, awaiting Amish (naming and branding are his decision). Recommendation: keep the chainguard name, which costs nothing if screen printed.
7. Small placements: the brake lever sits in front of the right grip (the massing model's lever line runs back from the grip), the pedal bodies sit about 8 mm further out, and the chainguard gains a rolled top edge. No decision needed.
8. The mannequin's feet sit at hip width, so they rest on the inner half of the pedals. A render limitation only.

### TRL

This is an appearance model only: no tolerances, no fabrication detail and nothing past TRL 3. `trl` stays 3 in `project.yaml`, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: constructable design and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it on every repo, with the instruction "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations", and with open decisions kept out of the build plan. On 2026-10-01 he set `budget_usd` as a value-engineering target, not a limit. This session brings GrowRider to that standard. trl stays 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rebuilt as a constructable design: `build_components()` returns 41 made and bought components; `build_parts()` still groups them into the 17 modelled BOM lines for the concept media; `check()` runs 66 constructability checks with build123d (fits, stop positions, contacts, clearances); all pass (`python cad/src/model.py --check`). STEP and STL regenerated.
- `docs/decisions/0003-design-for-construction.md` (GRR-DDR-003 v0.1, Draft): 17 changes, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review; three items proposed, awaiting Amish.
- `docs/05-build-plan.md` (GRR-BLD-001 v0.1) with `cad/src/build_plan_media.py`: overview, frame jig layout, 8 making sketches (GRR-DWG-101 to 108), 9 joint close-ups and 17 assembly step pictures in `docs/05-build-plan/`.
- `docs/06-design-decisions.md` (GRR-DEC-001 v0.1): 11 open decisions, 12 items to confirm when parts are bought, a Value engineering section and the decisions made.
- `bom/bom.csv` lines 1, 2, 3, 5, 6, 12, 14, 16 and 19 respecified; `bom/bom-notes.md` updated.
- `docs/04-calcs/sizing.py` re-run with the new model; GRR-CAL-001 v0.4, GRR-PRC-001 v0.6 and GRR-REQ-001 v0.6 updated; cost stated against the value-engineering target throughout.
- GRR-DWG-001 at Rev P4; concept media (`media/hero.png`, `exploded.png`, `flow.png`, `concept-blueprint.*`, `model.glb`, `viewer.html`) regenerated from the model.
- `project.yaml`: `design_state: constructable`; GRR-DDR-003, the build plan and the register added to `trl_evidence`; `budget_usd` unchanged at 300. README: build plan and register links, "Building the prototype" section with the overview picture.

### Design changes made for construction (GRR-DDR-003)

| # | Change |
| --- | --- |
| P1 | Rear dropouts: 6 mm track-end plates, slot open to the rear, 110 mm apart, M5 eyelets (were plain blocks 105 mm apart) |
| P2 | Fork specified with slotted fork ends 100 mm apart and eyelets (blades ended at the axle) |
| P3 | Coaster brake arm held under the left chainstay by an arm clip and M6 bolt (it floated) |
| P4 | Head tube 34 x 2.0 mm, 30.0 mm bore for 1 in press-in cups (was 31.0 mm) |
| P5 | Quill 22.0 x 2.0 mm so it slides in the 22.2 mm steerer bore (22.2 mm could not) |
| P6 | Stem head: welded 10 mm chromoly head plate and a bolt-on two-piece aluminium bar clamp block at 45 or 105 mm ahead of the axis; bar sweep 205 mm, rise 15 mm; quill lowest exposure 20 mm; grips within 2 mm of the concept |
| P7 | Seat stays join a cross bar 235 mm up, clear of the seat tube collar (were at 260 mm, inside it) |
| P8 | Positive stops: M5 stop screws in both clamp collars riding in side slots in the sleeve and post; 100 mm insertion at the stops |
| P9 | Rack fixed by tabs to the dropout eyelets and to brazed bosses on the seat stays (ends floated) |
| P10 | Seat stays 80 mm apart at the cross bar so the 64 mm rear fender passes; rear fender starts 10 deg above the axle line; fender bridge and wire stays |
| P11 | Rack lowered from 575 to 545 mm so the saddle clears it at the lowest setting |
| P12 | Kickstand plate under the chainstays with a centre-mount kickstand |
| P13 | Fork crown 16 mm deep and front fender 12 mm off the tire; the crown clearance in GRR-CAL-001 was corrected from 26 to 22 mm |
| P14 | Long-reach side-pull caliper (about 84 mm), fender bracket on the same crown bolt |
| P15 | Down tube 5 mm higher on the head tube, clear of the lower cup |
| P16 | Chain line 42 mm (was 48) and chainstays 21 mm each side at the BB; sprocket, chainring and chain clear the frame |
| P17 | Chainguard mounted by a seat tube clip and a chainstay boss |

### Key results

- Mass 15.1 kg (was 14.4 kg); **R5 (13 kg production goal) not met**.
- Value-engineering target: USD 300. Estimated cost of the constructable design: USD 299 for the bike (USD 1 under the target) and USD 311 with the helmet (USD 11 over).
- Smallest rider's coaster braking 0.22 g (was 0.23 g), back-pedal margin 9 %; R7 still at risk.
- Requirement statuses unchanged: 1 not met, 4 at risk, 2 not verifiable at TRL 3, 5 met.

### Proposed, awaiting Amish

All in GRR-DEC-001: accept GRR-DDR-003 (item 1); quill positive stop (item 2, recommendation: insertion mark only for the prototype); 0.7 kg mass increase (item 3, accept); steerer strength now interacting with the quill bore (item 4, let the fork test decide); and the earlier open items (helmet, partner, region, render setting, frame color, height scales, markings).

### Safety

- The quill has no positive stop; its minimum insertion mark is its only limit (safety stop S4 in the build plan). This departs from the concept's safety section and is item 2 in the register.
- Brazed chromoly and welded aluminium need a trained builder; the build plan's safety stops S1 to S7 apply. Nobody may ride the prototype before the ISO 4210-2 tests.

### Stale media

The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` show the concept stem head, dropouts and fittings and need regenerating on Amish's Mac; `cad/src/product_model.py` has not been re-run.

### Recommended next step

Amish reviews GRR-DDR-003 and the register. TRL 4 (building and testing to GRR-BLD-001) remains on hold by his instruction.
