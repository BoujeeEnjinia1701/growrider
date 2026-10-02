---
doc_id: GRR-DEC-001
title: GrowRider design decisions register
project: GrowRider
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from REVIEW.md, GRR-DDR-001 to 003 and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Amish accepted the recommendations of open items 1 to 4 and 8 to 11 (GRR-DDR-003 accepted); moved to decisions made; open items renumbered 1 to 3
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for open items 1 to 3 on 2026-10-02 (helmet supplied with every bike, World Bicycle Relief as first candidate partner, Zambia as first candidate region); moved to decisions made; USD 311 with the helmet reported as the prototype figure
---

# GrowRider design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, GRR-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The coaster brake hub is 110 mm over the locknuts with its sprocket on a 42 mm chain line, and its brake ratio (hub torque to sprocket torque) | The dropouts are 110 mm apart and the chainstays are placed for a 42 mm chain line; braking for the smallest rider rests on an assumed ratio of 2.5 | GRR-DDR-003, P1 and P16; GRR-DDR-002, D9 |
| 2 | A long-reach side-pull caliper whose reach covers about 84 mm is stocked. If none is, the fallback is a fork with brake bosses and a short-pull V-brake for children's levers, which is a design decision | The crown height and tire size set the reach | GRR-DDR-003, P14 |
| 3 | The fork: crown no deeper than 16 mm, 1 in threaded steerer 25.4 x 1.6 mm with 220 mm usable above the crown, slotted fork ends 100 mm apart with eyelets, crown hole for the caliper bolt | The front fender passes 7 mm under the crown; the quill needs the full steerer length | GRR-DDR-003, P2 and P13 |
| 4 | The solid tire's real width is 50 mm or less on the rim | The rear tire clears the chainstays by 4 mm at a 48 mm width | GRR-DDR-003, P16 |
| 5 | A 29.8 mm clamp collar closes firmly on the 29.2 mm sleeve, or one is turned to 29.2 mm | Sleeve collars are not a stock size | GRR-DDR-003, P8 |
| 6 | The 22.0 x 2.0 mm chromoly tube slides in the steerer bore with about 0.2 mm clearance | Steerer bores vary by maker | GRR-DDR-003, P5 |
| 7 | The 29.2 mm sleeve slides in the seat tube after reaming to 29.4 mm, and the 25.4 mm post in the sleeve | Drawn tube bores vary by about 0.1 mm | GRR-CAL-001, A |
| 8 | A 22.2 mm roadster-style bar of about 205 mm sweep and 15 mm rise is stocked | The grips sit where the fit calculation puts them only with this sweep and rise | GRR-DDR-003, P6 |
| 9 | 1 in JIS press-in headset (30.0 mm cups) and a 68 mm BSA bottom bracket are the regional standard | The head tube bore and BB shell are made to them | GRR-DDR-003, P4 |
| 10 | A builder who can TIG weld 6061 aluminium for the rack, or a bought rack of the same size and rating | Welded aluminium needs skill and has low fatigue strength | GRR-DDR-002, D7 |
| 11 | Masses of the tires, rims, hub and bought fittings | The mass estimate uses catalog values | GRR-CAL-001, D |
| 12 | Which parts are actually stocked in the first region (Zambia, the first candidate), including coaster hubs and 20 in solid tires | Parts commonality (R10) | GRR-REQ-001, R10 |

## Value engineering

Value-engineering target: USD 300 (a hypothetical control target, not a limit; Amish, 2026-10-01: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens"). Estimated cost of the constructable design: USD 311 for the bike with the helmet that is now supplied with every bike (decided 2026-10-02), BOM lines 1 to 20, USD 11 over the target; USD 299 for the bike alone, lines 1 to 19 (USD 1 under the target). The concept was USD 281 and 293; the parts added for construction account for the USD 18 difference. Frame builder labor is not included.

Main cost drivers:

- Frame tube, plate and consumables, USD 64 (line 1).
- Solid tires, USD 32 for the pair (line 9).
- Rear wheel with coaster hub, USD 30 (line 8).
- Quill stem with its head plate and clamp block, USD 20 (line 5).
- Fork with a long steerer, USD 18 (line 2).

Savings worth trying:

- Thorn-resistant tubes with liners instead of solid tires: about USD 10 and 0.5 kg less, but it reverses D4 (GRR-DDR-001), so it needs Amish's decision.
- A bought steel rack of the right size and rating instead of the welded aluminium one: no aluminium welding skill needed; check mass and price.
- One collar size: a 30.0 mm sleeve would take a stock collar, but the sleeve size was decided (GRR-DDR-002, D10), so only worth revisiting with the strength screen.
- A bought long quill stem cut and fitted with the head plate, if a 22.0 mm chromoly quill of 240 mm is stocked.
- Price the frame kit (tubes, dropouts, BB shell) as one order from a frame-building supplier.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D6: 20 in (ISO 406) wheels; coaster brake plus front rim brake; step-through frame with twin down tubes; solid or airless tires for the prototype; one 140 mm crank length; USD 120 production cost target at volume | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | GRR-DDR-001 |
| 2026-09-25 | D7 to D13: chromoly main tubes, aluminium rack, alloy rims and bar (R5 kept as the production goal); alloy front rim; obtain the coaster hub brake ratio; chromoly steerer and quill, 1.8 mm sleeve; R2 widened to 400 to 670 mm; R9 split into parent and mechanic tool lists; low bar as a co-design question | Amish: "i accept all your recommendations, go with them across all repos." | GRR-DDR-002 |
| 2026-09-26 | N1: prototype budget raised from USD 250 to USD 300 | Amish: "I am ok with the budget top ups" | GRR-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan and in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes themselves were accepted on 2026-10-01 (below) | GRR-DDR-003 |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit; cost is reported over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
| 2026-10-01 | Design for construction accepted: the changes P1 to P17 and their knock-on changes, as made | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GRR-DDR-003, Tables 1 and 2 |
| 2026-10-01 | Quill stem: no positive stop for the prototype; the minimum insertion mark, checked at every fit change, with a bright painted band above it. Follow-up: decide on the stop collar of option (b) after the fit trials | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GRR-DDR-003, A1 |
| 2026-10-01 | Mass of 15.1 kg accepted for the prototype (R5 production goal of 13 kg still not met); the prototype is weighed at TRL 4 | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GRR-DDR-003, A2 |
| 2026-10-01 | Steerer: keep the 25.4 x 1.6 mm steerer and let the ISO 4210-2 fork test decide | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GRR-DDR-002, N2; GRR-DDR-003, A3 |
| 2026-10-01 | Renders: 1.30 m rider setting in the product renders, 1.38 m in the concept sheet | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-01 | Frame color: kit teal for the portfolio renders; the production color is settled in co-design, with a high-visibility option | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-01 | Painted height scales on the exposed sleeve and quill: a band every 20 mm, a longer band every 60 mm | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 2026-10-01 | Markings: the name "GrowRider" screen printed on the chainguard; no head badge | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | `docs/REVIEW.md`, 2026-09-26, item 6 |
| 2026-10-02 | Helmet (BOM line 20): an adjustable, ventilated child helmet is supplied with every bike through the partner program and fitted at handover; its USD 12 stays in the bike's cost, so USD 311 is the prototype figure | Amish: "i approve your recommendations for all 555 open decisions." | GRR-DDR-001, O1 |
| 2026-10-02 | First partner and co-design partner: World Bicycle Relief, through its school bicycle programs and field mechanics, is the first candidate to approach for fit measurements and the regional parts list | Amish: "i approve your recommendations for all 555 open decisions." | GRR-DDR-001, O2 and O4 |
| 2026-10-02 | First region: Zambia is the first candidate region, for checking the regional parts list (items 1 to 12 below) | Amish: "i approve your recommendations for all 555 open decisions." | GRR-DDR-001, O3 |
