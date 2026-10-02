---
doc_id: GRR-DDR-001
title: GrowRider TRL 2 review decisions
project: GrowRider
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Items O1 to O4 decided by Amish on 2026-10-02 as recommended (helmet supplied with every bike; World Bicycle Relief as first candidate partner and co-design partner; Zambia as first candidate region)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D6; items O1 to O4 decided on 2026-10-02 as recommended (Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions.")

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-24) listed seven groups of items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open. The same instruction approved portfolio-wide decisions on the SwapCell interface, which do not apply to GrowRider (it has no battery), and confirmed that community designs pick co-design partners per area later.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-24) and in GRR-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Wheel size | 20 in (ISO 406) for the whole fit range, rather than 24 in (ISO 507), which fails standover for 1.10 m riders. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Brakes | Coaster brake plus a front rim brake with a short-reach, reach-adjustable lever, rather than coaster only or two hand brakes. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Frame | Step-through steel frame with twin down tubes, rather than a small diamond frame. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Tires | Solid or airless puncture-proof tires for the prototype, rather than thorn-resistant tubes with liners; users to be asked in co-design. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Crank length | One 140 mm crank length for the prototype, with a possible 127 mm swap for the smallest riders later. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Production cost target | $120 or less per bike at volume (R11), as proposed. Decided by Amish, 2026-09-25: go with recommendation. The prototype budget stays at $250 in `project.yaml`. |

*Table 2. Items that were left open (no recommendation was made); decided by Amish on 2026-10-02 as recommended.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Helmet funding (BOM line 20, $12): fund it from the $250 prototype budget ($5 over), fund it separately, or raise the budget to about $275 | Decided by Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." An adjustable, ventilated child helmet is supplied with every bike through the partner program and fitted at handover; its USD 12 stays in the bike's cost (GRR-DEC-001 v0.3) |
| O2 | First partner: a bicycle distribution NGO, a rural school network or a regional bicycle assembler | Decided by Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." World Bicycle Relief, through its school bicycle programs and field mechanics, is the first candidate to approach (GRR-DEC-001 v0.3) |
| O3 | First region: Zambia, Kenya or Malawi were suggested by the Buffalo parts ecosystem, with no single recommendation | Decided by Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." Zambia is the first candidate region (GRR-DEC-001 v0.3) |
| O4 | Co-design partner for fit measurements and the regional parts list | Decided by Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." World Bicycle Relief is also the first candidate co-design partner (GRR-DEC-001 v0.3) |

## Consequences

- GRR-PRC-001 and GRR-REQ-001 are revised to v0.3: the four design choices are no longer "proposed", R4 names the 20 in wheel, and R11 carries the $120 production target as decided. No requirement target was relaxed or redefined by these decisions, and `budget_usd` stays at $250.
- The parametric model (`cad/src/model.py`), drawing GRR-DWG-001 and calculation note GRR-CAL-001 use the decided configuration.
- With the helmet still open, the prototype total is $243 for the bike and $255 with the helmet; the helmet line stays in the BOM, flagged.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
