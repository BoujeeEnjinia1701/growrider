---
doc_id: GRR-REQ-001
title: GrowRider requirements
project: GrowRider
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record decisions of GRR-DDR-001 (20 in wheels, brakes, $120 production target); add TRL 3 status from GRR-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status figures from GRR-CAL-001 v0.4 (constructable design, GRR-DDR-003); R11 stated against the value-engineering target
---

# GrowRider requirements

These are the requirements for the concept. They were checked by calculation at TRL 3 in GRR-CAL-001 v0.4, on the constructable design of GRR-DDR-003: 5 are met on paper, 1 is not met (R5, mass), 4 are at risk and 2 cannot be verified at TRL 3. Amish's acceptance of the TRL 3 recommendations on 2026-09-25 (GRR-DDR-002) widened R2 to the crank-corrected fit range, split R9 into parent and mechanic tool lists, restated R5 as the production goal and named the alloy front rim in R7. All targets must still be revised from co-design findings before the design is frozen (see GRR-PRB-001).

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 3 status (GRR-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fit the intended riders | Rider height 1.10 to 1.65 m (ages about 6 to 14); standover height 470 mm or less at the stepping point | Fit calculation from anthropometric data; later fit trials with children | Met: standover 455 mm |
| R2 | Adjustable saddle height | 400 to 670 mm from bottom bracket center to saddle top (270 mm range), with at least 100 mm insertion at every sliding joint across the range (widened from 436 to 654 mm, GRR-DDR-002, D11) | Geometry calculation; massing model | Met: 400 to 670 mm, 100 mm insertion |
| R3 | Adjustable reach and handlebar height | Handlebar height adjustable by 100 mm or more; horizontal saddle-to-grip reach adjustable by 100 mm or more | Geometry calculation | Met: bar 113 mm, reach 141 mm |
| R4 | One wheel size across the whole fit range | Single wheel size for all riders: 20 in (ISO 406), decided 2026-09-25 (GRR-DDR-001, D1) | Design review; fit calculation | Met: 20 in |
| R5 | Light enough for the smallest rider to handle | Production goal: complete bike with rack, fenders and kickstand 13 kg or less; the prototype estimate is tracked against it (GRR-DDR-002, D7) | Mass estimate, then weighing | **Not met: 15.1 kg** (14.4 kg before the parts added for construction, GRR-DDR-003; 15.3 kg before D7) |
| R6 | Small, clearly rated rear rack | Rated 10 kg, rating marked on the rack; platform no larger than a school bag (about 300 x 140 mm); no passenger footrests | Design review; later static load test | Met by design: 300 x 120 mm |
| R7 | Two independent brakes a child can operate | Rear coaster brake plus front rim brake (decided 2026-09-25, GRR-DDR-001, D2), with an alloy front rim for wet braking (GRR-DDR-002, D8); each brake alone 0.2 g or more and both together 0.35 g or more on a dry, level surface; hand lever reach adjustable for small hands | First-order braking calculation; later tests to ISO 8098 or ISO 4210 as applicable | At risk: small margins for the smallest rider; wet steel rim poor |
| R8 | Puncture resistance | No loss of use from thorn punctures; tire life 2,000 km or more (about one school year of 10 km per day) | Supplier data; later field trial | Not verifiable at TRL 3 (tire life) |
| R9 | Serviceable with basic tools (split by GRR-DDR-002, D12) | R9a, parent or teacher: every fit adjustment with a 13 mm spanner and a screwdriver, and a fit change in 10 minutes or less. R9b, mechanic: all routine service, including headset and bottom bracket, with 13, 15 and 32 mm spanners, a bottom bracket lockring spanner and a screwdriver | Design review; later timed trial | At risk: both tool lists met; fit change 10 min, at the limit |
| R10 | Parts commonality with regional adult roadsters | Every wear part except tires and rims interchangeable with regional roadster parts (chain, sprocket, coaster hub internals, bottom bracket, headset, pedals, seat post, handlebar, brake blocks) | BOM review against a regional parts list from the partner | Not verifiable at TRL 3 (no regional parts list) |
| R11 | Low cost | Prototype parts cost reported against the USD 300 value-engineering target in `project.yaml` (a hypothetical control target, not a limit; Amish, 2026-10-01; raised from USD 250 on 2026-09-26, GRR-DDR-002, N1); production cost target USD 120 or less per bike at volume (decided 2026-09-25, GRR-DDR-001, D6) | Priced BOM; production estimate with a regional assembler | At risk: USD 299 for the bike (USD 1 under the target), USD 311 with helmet (USD 11 over); USD 120 production cost not yet estimated |
| R12 | Lasts across siblings | 10-year service life for at least three successive riders; frame and fork sized for a 60 kg rider plus a 10 kg rack load; sliding joints that do not seize in dust and rain | Fatigue calculation at TRL 3; later frame fatigue tests | At risk: 1 of 7 sections above the fatigue screen (steerer; 3 of 6 before GRR-DDR-002) |

## Assumptions

- Inseam is about 0.45 times standing height, and a comfortable saddle height (bottom bracket center to saddle top) is about 0.88 times inseam. Both are common bicycle fitting rules of thumb for adults and older children and must be checked against measurements of the intended users.
- Horizontal saddle-to-grip reach for an upright riding position scales with torso and arm length, estimated at about 0.2 times height (220 mm at 1.10 m, 330 mm at 1.65 m). This is a placeholder until fit measurements are taken.
- A typical school trip is 5 km each way on dirt or gravel, ridden at 10 to 12 km/h.
- A 1.65 m rider is assumed to weigh up to 60 kg, including a margin for older teenagers.
- Saddle height (R2) is measured from the BB center to the saddle top along the seat axis. GRR-CAL-001 also checks a second fitting rule that accounts for the 140 mm crank (saddle top to pedal at 1.09 times inseam), which asks for 400 to 669 mm. R2 now takes the wider range, which covers both rules.
- Applicable standard: classified by its maximum saddle height above the ground (about 890 mm), GrowRider falls under ISO 4210-2 as a city and trekking bicycle; ISO 8098 covers maximum saddle heights below 635 mm (GRR-CAL-001, section M).
