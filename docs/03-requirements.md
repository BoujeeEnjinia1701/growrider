---
doc_id: GRR-REQ-001
title: GrowRider requirements
project: GrowRider
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
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
---

# GrowRider requirements

These are first-pass requirements for the concept. Targets are proposals for review, will be checked by calculation at TRL 3, and must be revised from co-design findings before the design is frozen (see GRR-PRB-001).

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Fit the intended riders | Rider height 1.10 to 1.65 m (ages about 6 to 14); standover height 470 mm or less at the stepping point | Fit calculation from anthropometric data; later fit trials with children |
| R2 | Adjustable saddle height | 436 to 654 mm from bottom bracket center to saddle top (218 mm range), with at least 100 mm insertion at every sliding joint across the range | Geometry calculation; massing model |
| R3 | Adjustable reach and handlebar height | Handlebar height adjustable by 100 mm or more; horizontal saddle-to-grip reach adjustable by 100 mm or more | Geometry calculation |
| R4 | One wheel size across the whole fit range | Single wheel size for all riders; 20 in (ISO 406) proposed, 24 in (ISO 507) alternative | Design review; fit calculation |
| R5 | Light enough for the smallest rider to handle | Complete bike with rack, fenders and kickstand 13 kg or less | Mass estimate, then weighing |
| R6 | Small, clearly rated rear rack | Rated 10 kg, rating marked on the rack; platform no larger than a school bag (about 300 x 140 mm); no passenger footrests | Design review; later static load test |
| R7 | Two independent brakes a child can operate | Rear coaster brake plus front hand brake; each brake alone 0.2 g or more and both together 0.35 g or more on a dry, level surface; hand lever reach adjustable for small hands | First-order braking calculation; later tests to ISO 8098 or ISO 4210 as applicable |
| R8 | Puncture resistance | No loss of use from thorn punctures; tire life 2,000 km or more (about one school year of 10 km per day) | Supplier data; later field trial |
| R9 | Serviceable with basic tools | All fit adjustments and routine service with 13 mm and 15 mm spanners and a screwdriver; a fit change takes 10 minutes or less for a parent or teacher | Design review; later timed trial |
| R10 | Parts commonality with regional adult roadsters | Every wear part except tires and rims interchangeable with regional roadster parts (chain, sprocket, coaster hub internals, bottom bracket, headset, pedals, seat post, handlebar, brake blocks) | BOM review against a regional parts list from the partner |
| R11 | Low cost | Prototype parts $250 or less (project budget); production cost target $120 or less per bike at volume (proposed, awaiting Amish) | Priced BOM; production estimate with a regional assembler |
| R12 | Lasts across siblings | 10-year service life for at least three successive riders; frame and fork sized for a 60 kg rider plus a 10 kg rack load; sliding joints that do not seize in dust and rain | Fatigue calculation at TRL 3; later frame fatigue tests |

## Assumptions

- Inseam is about 0.45 times standing height, and a comfortable saddle height (bottom bracket center to saddle top) is about 0.88 times inseam. Both are common bicycle fitting rules of thumb for adults and older children and must be checked against measurements of the intended users.
- Horizontal saddle-to-grip reach for an upright riding position scales with torso and arm length, estimated at about 0.2 times height (220 mm at 1.10 m, 330 mm at 1.65 m). This is a placeholder until fit measurements are taken.
- A typical school trip is 5 km each way on dirt or gravel, ridden at 10 to 12 km/h.
- A 1.65 m rider is assumed to weigh up to 60 kg, including a margin for older teenagers.
- The standard that applies (ISO 8098 for young children's bicycles or ISO 4210 for larger bicycles) depends on the saddle height range and is to be confirmed at TRL 3.
