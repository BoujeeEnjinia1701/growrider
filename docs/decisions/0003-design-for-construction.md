---
doc_id: GRR-DDR-003
title: GrowRider design for construction
project: GrowRider
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Accepted by Amish, including the recommendations for A1 to A3
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-01: "i agree with your recommendations for both GrowRider and GravitySort". This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A3), which are now decided as recommended and recorded in the design decisions register (GRR-DEC-001).

## Context

On 2026-09-30 Amish approved the build plan format and asked for it on every repo, writing: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of GRR-DDR-002 showed what GrowRider does and carried its calculations, but it was a massing model: several parts could not be made, fitted or fixed as drawn. Checking the model with build123d found the seventeen problems below.

The changes keep what the bike does: the same wheels, frame geometry, fit range (saddle 400 to 670 mm, 100 mm insertion), bar heights and reach (the grips move less than 2 mm), standover, brakes, rack size and rating, fenders and parts list. Nothing here changes the pitch. Every change is in `cad/src/model.py`, which now builds each component separately (`build_components`) and runs 66 constructability checks (`python cad/src/model.py --check`): fits between sliding parts, the stop positions, parts that must touch, and clearances between parts that must not. All 66 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | Rear dropouts were plain 40 x 5 x 40 mm blocks 105 mm apart, with no slot. A single-speed coaster hub must slide back to tension its chain, and roadster coaster hubs are about 110 mm over the locknuts. | Track-end dropouts cut from 6 mm steel plate, slot 10 mm wide open to the rear, inner faces 110 mm apart, an M5 eyelet 18 mm behind and 20 mm above the axle. The chainstay ends 40 mm ahead of the axle and the seat stay 16 mm ahead and 20 mm above it, each slotted over the plate and brazed. | The usual single-speed arrangement on roadsters; one plate shape for both sides, mirrored. The eyelet carries the rack strut and fender stay. |
| P2 | Fork blades ended at the axle center with no fork ends. | The bought fork is specified with slotted fork ends 100 mm apart and M5 eyelets (BOM line 2). | Standard on 20 in forks; the eyelets carry the front fender stays. |
| P3 | The coaster brake arm ended in mid-air and ran into the left chainstay. | The arm runs forward under the left chainstay and is held 135 mm ahead of the axle by a bought arm clip: a band round the stay, two legs either side of the arm, one M6 bolt (BOM line 19). | The brake's reaction torque must go into the frame; a clip is how roadsters do it and needs no brazed fitting. |
| P4 | The 34 x 1.5 mm head tube had a 31.0 mm bore; 1 in press-in headset cups need 30.0 mm (JIS). | Head tube 34 x 2.0 mm chromoly, 30.0 mm bore, reamed and faced after brazing. | Fits the common 1 in roadster headset without shims. +0.06 kg. |
| P5 | A 22.2 mm quill cannot slide in a 25.4 x 1.6 mm steerer, whose bore is also 22.2 mm. | Quill 22.0 x 2.0 mm chromoly (a standard metric tube), 0.2 mm diametral clearance; stress at full extension 79 MPa against the 90 MPa screen (77 MPa before) [K2]. | Keeps the decided steerer (GRR-DDR-002, D10). 22.0 mm quills are the other common 1 in size. |
| P6 | The stem head was a block at 0 mm or a tube at 60 mm: no single part does both, and a bar clamp over the quill axis would cover the expander bolt. | A 10 mm chromoly head plate, 127 x 44 mm, welded across the front of the quill, its top flush with the quill top, with four tapped M8 holes at each of two positions. A two-piece aluminium bar clamp block (54 x 44 x 30 mm) bolts to it with four M8 x 40 bolts (13 mm heads) through both halves, putting the bar 45 or 105 mm ahead of the steering axis. The bar sweep becomes 205 mm (from 160) and its rise 15 mm (from 25), and the quill's lowest exposure 20 mm (from 15), so the plate clears the locknut by 2 mm and the grips sit within 2 mm of where the concept had them. Head plate stress 71 MPa against 90 [K6]. | The reach and bar heights of GRR-CAL-001, Section B are unchanged, and the bar position still changes with the 13 mm spanner of R9a. The expander bolt stays reachable from the top with a socket. Moving the block means four bolts; the 1.5 minutes allowed for it in the fit-change estimate [H1] is kept but is tight. |
| P7 | The seat stays met the seat tube 260 mm up, inside the 14 mm band where the clamp collar sits. | The stays end on a cross bar 235 mm up the seat axis (P10), 22 mm below the collar. | The collar must close on a plain tube. |
| P8 | The concept named "positive stop bolts" for the sliding parts but gave no way to fit one. | An M5 dog-point stop screw in each clamp collar, through a hole in the tube below, rides in a 6 mm slot on the side of the part inside: the seat tube collar's screw (left) in a 136 mm slot in the sleeve, the sleeve collar's screw (right) in a 146 mm slot in the post. The lower end of each slot stops its part with exactly 100 mm inserted. The seat tube screw's tip enters the sleeve slot 1.5 mm and stays 0.6 mm clear of the post. | A positive stop that a child or parent cannot pull past, made with a drill and a file. The screws also key the post so the saddle stays straight. The slots lie on the neutral axis of fore-and-aft bending and lower the stiffness by under 1 % [K7]. The quill cannot take a stop of this kind (A1). |
| P9 | The rack struts ended in the air near the axle and its stays in the air by the seat stays. | Struts end in 3 mm tabs bolted to the dropout eyelets; stays end in tabs bolted to M5 bosses brazed on the seat stays. | Four bolted points, all reachable with the wheel in place. |
| P10 | The 64 mm rear fender crossed the seat stays where they were about 50 mm apart, and its front end ran into the chainstays. | The seat stays meet a 16 mm cross bar behind the seat tube that holds them 80 mm apart at the top; the fender's front end starts 10 degrees above the axle line instead of at it; a 12 mm bridge between the stays carries the fender's top bracket; wire stays go to the dropout eyelets. | Full coverage over the top and back of the wheel is kept; 4.8 mm clearance to the frame. |
| P11 | At the smallest setting the saddle sat inside the front of the rack. | Rack platform lowered 30 mm, to 545 mm above the ground: the saddle clears it by 37 mm at the lowest setting and the rack clears the fender by 20 mm. | Same 300 x 120 mm platform and 10 kg rating; slightly lower load. Rail stress unchanged (26 MPa). |
| P12 | The kickstand floated beside the chainstay. | A 4 mm kickstand plate brazed under both chainstays 55 mm behind the BB; a bought centre-mount kickstand clamps to it with one M10 bolt, leg on the left. | The kickstand bosses named in BOM line 1, made concrete. |
| P13 | The calculation measured the fork crown from its top face (26 mm above the tire); the crown is about 22 mm deep, so its underside was 16 mm above the tire and the 16 mm fender gap plus a 3 mm fender would not fit under it. | Fork crown specified about 16 mm deep; front fender 12 mm off the tire (the rear stays at 16 mm). The crown underside is 22 mm above the tire and the fender clears it by 7 mm [C3]. | The only way to keep a front fender under a stock-height crown; the rainy-season mud gap is a little smaller at the front (still at least as large as the 6 mm the concept quoted at the crown). |
| P14 | The front caliper was a box with no reach given. | A long-reach side-pull caliper with about 84 mm reach, on a nutted bolt through the crown; the front fender bracket goes on the same bolt behind the crown. | The reach follows from the crown height and tire size. A caliper of this reach has to be found (register, to confirm). |
| P15 | The down tube met the head tube 1.7 mm below its lower end, where the headset cup presses in. | Down tube moved 5 mm up the head tube; it now ends 3.2 mm above the lower end. | The cup needs a clean, round end to press into. |
| P16 | With a 48 mm chain line the sprocket ran into the drive-side chainstay end and the chain rubbed the seat stay. | Chain line 42 mm; chainstays 21 mm each side of center at the BB. Clearances: sprocket 5.0 mm, chainring 2.4 mm, chain 2.2 mm to the frame; rear tire 4.0 mm to the stays. | A normal single-speed chain line. |
| P17 | The chainguard was a loose plate. | Mounted by a clip round the seat tube and a tab to an M5 boss brazed on the drive chainstay; it clears the chain by 3.9 mm and the crank by 2.0 mm. | As on roadster chainguards. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 14.4 to 15.1 kg (R5 production goal 13 kg, still not met) [D3]: dropouts 0.31 kg, kickstand plate and bosses 0.10 kg, heavier head tube 0.06 kg, stay cross bar and bridge 0.07 kg, collars 0.12 kg, the stem's head plate and clamp block 0.37 kg more than the concept's head; seat stays and chainstays are shorter. | Parts added for construction. |
| Cost | BOM lines 1, 5, 12 and 19 repriced: bike USD 281 to 299, with helmet USD 293 to 311. Value-engineering target USD 300 (`budget_usd` unchanged): the bike is USD 1 under it and the bike with the helmet USD 11 over it [J1]. | Parts added for construction. |
| Braking | Smallest rider, coaster 0.23 to 0.22 g; wet front 0.15 to 0.14 g; both brakes 0.47 to 0.46 g [F2] to [F4]. R7 stays at risk. | Heavier bike. |
| Drawing | GRR-DWG-001 Rev P4; making sketches GRR-DWG-101 to 108 added. | Follows the model. |
| Documents | GRR-CAL-001 v0.4, GRR-PRC-001 v0.6, GRR-REQ-001 v0.6: mass, cost, crown clearance, quill and stem figures updated. No requirement changed status. | Follows the model. |
| Media | Concept media regenerated from the model. The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept stem head, dropouts and fittings and need regenerating on Amish's Mac; `cad/src/product_model.py` reads the changed parameters but has not been re-run. | Blender is on the Mac. |

*Table 3. Items that change what the bike does or its safety case: proposed, then accepted by Amish as recommended on 2026-10-01.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The quill cannot take a positive stop like the seat post's: the whole of its inserted length is inside the threaded steerer, under the headset locknut. The concept's safety section says every sliding part has a positive stop. | (a) the minimum insertion mark only, as on every quill stem, checked at each fit change; (b) a steerer 15 mm longer, standing above the locknut, with a clamp-on stop collar whose screw rides in a slot in the quill (the bar sits 14 mm higher at every setting); (c) a stop cable inside the steerer from the crown to the wedge. | (a) for the prototype, with a bright painted band above the mark; decide (b) after the fit trials. |
| A2 | The parts added for construction make the bike 0.7 kg heavier (15.1 kg against the 13 kg production goal). | (a) accept for the prototype and weigh it at TRL 4; (b) look for savings now (for example a lighter head plate design). | (a). |
| A3 | Steerer strength (GRR-DDR-002, N2) now interacts with the quill: a 25.4 x 2.0 mm wall leaves a 21.4 mm bore that no quill fits, and at the lowest setting the quill reaches the crown, where the steerer is most stressed. | (a) keep the 1.6 mm wall and let the ISO 4210-2 fork test decide; (b) a butted steerer thick only inside the crown, with the quill's lowest position raised 20 mm (the bar cannot go as low by 19 mm); (c) a 1 1/8 in steerer with a 25.4 mm quill (less common headset). | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan GRR-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`), and the design decisions register GRR-DEC-001 carries the open items.
- With A1 accepted, the quill's limit for the prototype is its minimum insertion mark with a bright painted band above it (build plan GRR-BLD-001, section 3.6 and safety stop S4); the stop collar of option (b) is to be decided after the fit trials. With A2 and A3 accepted, the prototype is weighed at TRL 4 and the ISO 4210-2 fork test decides the steerer.
- Requirement status is unchanged: 1 not met (R5), 4 at risk (R7, R9, R11, R12), 2 not verifiable at TRL 3, 5 met (GRR-CAL-001 v0.4).
- Several bought parts set dimensions in the model and must be checked when bought: the coaster hub (110 mm over the locknuts, 42 mm chain line), the caliper reach, the fork's crown depth, steerer length and fork ends, the tire's real width and the 29.8 mm collar closing on the 29.2 mm sleeve. They are listed in the register.
- Nothing has been built or tested; TRL 4 remains on hold by Amish's instruction.
