---
doc_id: GRR-DDR-002
title: GrowRider recommendations accepted
project: GrowRider
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up to $300 decided by Amish (N1)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items D7 to D13; D1 to D6 confirmed; items O1 to O4 and N1 to N2 remain proposed

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25: TRL 3) listed seven new items as "Proposed, awaiting Amish", each with a recommendation, and kept four TRL 2 items open because no recommendation had been made. GRR-DDR-001 had recorded D1 to D6 as "Adopted as recommended" under Amish's instruction of the same day. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided in favor of that recommendation; where several options were offered, the recommended option is the decision. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, so any decided item that needs building, testing or purchasing is recorded as decided but on hold.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25: TRL 3) and in GRR-CAL-001 v0.1.

## Decision

*Table 1. Items decided by this record.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 to D6 | Wheel size, brakes, frame, tires, crank length, $120 production target (GRR-DDR-001) | Decided by Amish, 2026-09-25: go with recommendation (confirmed) | Wording in GRR-DDR-001 and REVIEW unchanged in substance |
| D7 | Mass (R5) | Decided by Amish, 2026-09-25: go with recommendation. Option (b): chromoly main tubes, an aluminium rack, alloy rims and an alloy bar, keeping solid tires (D4); R5 stays at 13 kg as the production goal | `cad/src/model.py`: seat tube 31.8 x 1.2 mm, down tube 31.8 x 0.9 mm and loop tube 28.6 x 0.9 mm in chromoly 4130; rack 12 x 1.5 mm aluminium 6061-T6. BOM lines 1, 6, 8 and 13 respecified and repriced. GRR-CAL-001 v0.2: mass 15.3 kg to 14.4 kg (the TRL 3 note estimated 13.6 kg; the model-based figure is higher because the seat tube keeps a 1.2 mm wall for the sleeve and the head tube keeps 1.5 mm). R5 restated as the production goal; still not met |
| D8 | Alloy front rim (R7) | Decided by Amish, 2026-09-25: go with recommendation. Alloy front rim specified | BOM line 7 now alloy only; R7 target names the alloy rim; wet front braking for the smallest rider about 0.15 g instead of 0.05 g with steel |
| D9 | Coaster hub brake data (R7) | Decided by Amish, 2026-09-25: go with recommendation. Obtain the brake ratio of a regional coaster hub before further brake work | Recorded as an open action; the data must come from a hub maker or the co-design partner. Any hub purchase or bench test is TRL 4 work, on hold |
| D10 | Strength (R12) | Decided by Amish, 2026-09-25: go with recommendation. Chromoly steerer and quill, and a 1.8 mm wall sleeve; recheck in GRR-CAL-001 | Sleeve 28.6 x 1.5 mm became 29.2 x 1.8 mm chromoly (25.6 mm bore for the 25.4 mm post), which needs the 29.4 mm bore of a 1.2 mm seat tube. Steerer and quill chromoly at the same size. GRR-CAL-001 v0.2 adds a 90 MPa screen for chromoly sections: 3 of 6 sections above the screen became 1 of 6 (steerer at the crown, 117 MPa). Drawing GRR-DWG-001 to Rev P2 |
| D11 | R2 target | Decided by Amish, 2026-09-25: go with recommendation. R2 widened from 436 to 654 mm to 400 to 670 mm | GRR-REQ-001 v0.4; the design already meets it |
| D12 | R9 tools | Decided by Amish, 2026-09-25: go with recommendation. R9 split into a parent tool list (13 mm spanner, screwdriver) and a mechanic tool list (13, 15 and 32 mm spanners, BB lockring spanner, screwdriver) | GRR-REQ-001 v0.4 (R9a, R9b); both tool lists met on paper; the 10 min fit change sits at the limit, so R9 stays at risk |
| D13 | Low bar option | Decided by Amish, 2026-09-25: go with recommendation. A flat bar for the smallest riders is a co-design question | Added to the open questions of GRR-PRB-001 v0.4 and GRR-PRC-001 v0.4; no design change |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Helmet funding (BOM line 20, $12) | Proposed, awaiting Amish (no recommendation was made). Since the 2026-09-26 top-up (N1), the $293 total with the helmet fits the $300 budget |
| O2 | First partner | Proposed, awaiting Amish; community designs pick co-design partners per area later |
| O3 | First region (Zambia, Kenya or Malawi suggested) | Proposed, awaiting Amish (no recommendation was made) |
| O4 | Co-design partner for fit measurements and the regional parts list | Open; picked per area later |
| N1 | Prototype budget: D7 and D10 raise the bike to $281 ($293 with the helmet) against the $250 in `project.yaml` | New, proposed, awaiting Amish. Options: raise the budget to $300; keep $250 and build the first prototype in hi-tensile steel with the chromoly parts later; or keep $250 and treat R11 as not met. Recommendation: raise to $300, which also settles O1. Budget top-up to $300: decided by Amish, 2026-09-26. `budget_usd` is now $300; GRR-REQ-001 v0.5 and GRR-CAL-001 v0.3 record R11 as at risk (prototype $281, $293 with the helmet, within budget; production cost not estimated) |
| N2 | Steerer at the crown still above its screen (117 MPa against 90 MPa; 98 MPa with a 25.4 x 2.0 mm steerer) | New, proposed, awaiting Amish. Recommendation: specify a 25.4 x 2.0 mm butted chromoly steerer and confirm against the ISO 4210-2 fork tests at TRL 4 |

## Consequences

- GRR-REQ-001, GRR-PRC-001 and GRR-PRB-001 go to v0.4 and GRR-CAL-001 to v0.2; drawing GRR-DWG-001 goes to Rev P2; the STEP, STL and media files are regenerated from the model.
- Requirement status after this record (GRR-CAL-001 v0.2): 5 met, 2 not met (R5 mass 14.4 kg; R11 prototype cost $281), 3 at risk (R7, R9, R12), 2 not verifiable at TRL 3. See GRR-CAL-001, Table 6.
- `trl` and `trl_target` stay at 3. TRL 4 is on hold by Amish's instruction; nothing in this record authorizes building, testing or purchasing.
