---
doc_id: GRR-PRC-001
title: GrowRider design precis
project: GrowRider
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, design choices, safety, media)
---

# GrowRider design precis

GrowRider is a step-through steel children's bicycle on 20 in wheels whose seat post and stem telescope, so one bike fits riders from about 1.10 to 1.65 m (ages about 6 to 14) and can be handed down between siblings. It uses a coaster brake plus a front rim brake, puncture-proof tires, a single-speed chain drive and a small rack rated 10 kg, with wear parts shared with the region's adult roadsters. First-order numbers show the fit range, brakes and cost are achievable; mass (about 15.5 kg against a 13 kg target) is the main problem to solve.

![Hero render](../media/hero.png)

*Figure 1. GrowRider massing model with the seat post and stem extended toward the top of their range, beside a 1.35 m child (about 10 years old) for scale.*

## How it works

1. **Fit the rider.** A parent, teacher or mechanic sets saddle height with a two-stage telescoping seat post (an inner sleeve inside the seat tube, then a standard seat post inside the sleeve) and sets handlebar height with a long quill stem that slides in the fork steerer. Minimum insertion marks on each sliding part show the limit. Both clamps use 13 mm bolts.
2. **Ride to school.** The rider pedals a single-speed chain drive (32T chainring, 18T sprocket, 140 mm cranks) at about 65 rpm for 11 km/h. Solid or airless tires cannot go flat on thorns.
3. **Stop.** Pedaling backward engages the coaster brake in the rear hub. A front rim brake with a short-reach lever gives a second, independent brake that still works if the chain comes off.
4. **Carry a school bag.** A small rear rack, rated and marked 10 kg, carries a bag or books. It is sized for a bag, not a passenger or a water container.
5. **Grow and hand down.** As the child grows, the post and stem are raised. When the child moves to an adult roadster, both are lowered and the bike passes to a younger sibling. Worn parts are replaced from the roadster parts already sold in the local market.

![Growth and hand-down cycle](../media/flow.png)

*Figure 2. Growth and hand-down cycle. Saddle heights are estimates from the fit rules in the first-order numbers; the 10-year life is a target.*

## Main components

Item numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Frame | Step-through steel frame with twin down tubes; 31.8 mm outer seat tube | Low stepping point for small riders and for school skirts; sleeves for the telescoping parts. Proposed, awaiting Amish |
| 2 | Fork | 20 in steel fork, 1 in threaded steerer | Standard 1 in headset as on roadsters |
| 3 | Telescoping seat post | 28.6 mm inner sleeve plus 25.4 mm seat post | 218 mm of travel in two stages of about 110 mm |
| 4 | Saddle | Child size, light color cover | Light color stays cooler in sun |
| 5 | Telescoping stem | Long 22.2 mm quill, 120 mm travel, two-position head (0 or 60 mm forward) | Adjusts bar height and reach |
| 6 | Handlebar and grips | 22.2 mm swept-back bar, 520 mm wide | Upright position for visibility |
| 7 | Front wheel | 20 in (ISO 406), 28 spokes, nutted axle | 15 mm axle nuts as on roadsters |
| 8 | Rear wheel | 20 in (ISO 406) with coaster brake hub | Hub type widely used on regional roadsters (to confirm) |
| 9 | Tires (2) | 20 x 1.95 in solid or airless | Proposed, awaiting Amish |
| 10 | Crankset | 140 mm cranks, 32T ring, 9/16 in pedal threads | Adult pedals fit |
| 11 | Chain and sprocket | 1/2 x 1/8 in chain, 18T sprocket | Same chain as roadsters |
| 12 | Front brake | Side-pull caliper, short-reach adjustable lever | Second, independent brake |
| 13 | Rear rack | Steel, about 300 x 120 mm, 10 kg marked | No footrests or passenger seat |
| 14 | Fenders | Pair, full coverage | Rainy-season mud and school uniforms |
| 15 | Chainguard | Full plate over the upper chain run | Keeps clothing out of the chain |
| 16 | Kickstand | Rear-mounted | Parking at school |
| 17 | Reflectors and bell | Front white, rear red, spoke and pedal reflectors, bell | Road visibility |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with item numbers matching the BOM. The bottom bracket, headset, hardware and helmet (BOM lines 18 to 20) are not modeled.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

**Fit.** Assumptions: inseam is about 0.45 times standing height; saddle height (bottom bracket center to saddle top) is about 0.88 times inseam; seat tube angle 70°.

| Rider height | Inseam (0.45 x height) | Saddle height (0.88 x inseam) |
| --- | --- | --- |
| 1.10 m (about age 6) | 495 mm | 436 mm |
| 1.38 m (about age 10) | 621 mm | 546 mm |
| 1.65 m (about age 14) | 743 mm | 654 mm |

Table 1. Saddle height across the fit range (estimates).

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Saddle height range | 436 to 654 mm (218 mm) | Table 1 | R2, met by two stages of about 110 mm with 100 mm insertion each |
| Saddle rise and setback over the range | 205 mm up, 75 mm back | 218 mm along a 70° seat tube | |
| Handlebar height range | about 113 mm | 120 mm of quill travel along a 70° steering axis | R3 met |
| Reach adjustment | about 124 mm | Saddle setback 75 mm, less 41 mm as the bar rises back along the steering axis, plus 60 mm stem head and 30 mm saddle rail | R3 met; needs about 110 mm if reach is 0.2 x height (assumption) |
| Standover at the stepping point | about 460 mm | Low loop tube, 20 in wheels, 260 mm bottom bracket height | R1 met, thin margin; about 510 mm with 24 in wheels (not met) |
| Minimum saddle top above ground | about 670 mm | 260 mm bottom bracket plus 436 mm at 70° | Small riders stand over the frame to stop, as on any bicycle |
| Pedal clearance | about 110 mm | 260 mm bottom bracket, 140 mm cranks | Adequate for ruts; check on field roads |
| Gear development | 2.8 m per crank turn | 32/18 on a 1.57 m rolling circumference | 66 rpm at 11 km/h |
| Power on the level at 11 km/h | about 35 W | 45 kg rider and bike, rolling coefficient 0.02 (solid tire on gravel), small air drag | Sustainable for a child |
| Power on a 5 % climb at 7 km/h | about 60 W | Same, plus gravity | Short climbs only; steep hills walked |
| Mass | about 15.5 kg | Frame 3.5, wheels 2.6, solid tires 2.0, drive 1.7, rack 0.8, other parts 4.9 kg | **R5 (13 kg) not met** |
| Rear coaster brake alone, dry | about 0.27 g | Rear-wheel skid limit: μ (L - x) / (L + μh), μ = 0.7, wheelbase L = 0.86 m, center of mass x = 0.33 m ahead of rear axle and h = 0.70 m high | R7 met |
| Rear coaster brake alone, loose gravel | about 0.19 g | Same with μ = 0.4; 4.7 m stop from 15 km/h | R7 marginal; the case for a front brake |
| Front brake pitch-over limit | about 0.76 g | (L - x) / h | Grip limits both brakes to about μ, so 0.4 g on gravel and above 0.35 g on dry ground if a child can squeeze hard enough |
| Rack | 10 kg | Rating chosen for child safety; school bag 3 to 5 kg | R6 |
| Prototype parts cost | about $243 for the bike, $255 with helmet | Indicative prices, see `bom/bom.csv` | R11 met for the bike; $5 over with the helmet |

**Commute time.** Assumptions: a 5 km trip each way; walking at 4 to 5 km/h; cycling at 10 to 12 km/h on dirt roads.

| Mode | Speed | One way | Round trip |
| --- | --- | --- | --- |
| Walking | 4 to 5 km/h | 60 to 75 min | 2.0 to 2.5 h |
| GrowRider | 10 to 12 km/h | 25 to 30 min | 50 to 60 min |
| Time returned to the child | | 30 to 50 min | 60 to 100 min per day, about 250 h per 190-day school year at the midpoint |

Table 2. School trip time, walking and cycling (estimates).

## Key design choices

- **Wheel size: 20 in (ISO 406) or 24 in (ISO 507).** 20 in keeps standover at about 460 mm so a 1.10 m child can stand over the frame, and gives lower mass. 24 in rolls better on ruts and suits riders above about 1.35 m, but raises standover to about 510 mm and fails R1 for the smallest riders. Neither is a regional roadster size, so tires and rims are the one commonality gap either way. Recommendation: 20 in. Proposed, awaiting Amish.
- **Brakes: coaster brake plus front rim brake.** A coaster brake is simple, weather-proof, needs no hand strength, and uses hub internals common on regional roadsters. On its own it fails completely if the chain comes off and is marginal on loose gravel (about 0.19 g). Adding a front rim brake gives two independent brakes. Alternatives: coaster only (cheaper, one failure mode away from no brake) or two hand brakes without a coaster (needs hand strength small children may lack). Recommendation: coaster plus front rim brake. Proposed, awaiting Amish.
- **Step-through frame.** Lower standover than a diamond frame, and practical for school uniforms and skirts. It needs twin down tubes to keep the frame stiff. Proposed, awaiting Amish.
- **Puncture-proof tires.** Solid or airless tires remove thorn punctures entirely but add about 0.8 kg, ride harsher and roll less freely. Thorn-resistant tubes with tire liners keep standard parts and a softer ride, but still puncture occasionally. Recommendation: solid or airless for the prototype, and ask users. Proposed, awaiting Amish.
- **Parts commonality.** Chain, coaster hub internals, 1 in headset, 25.4 mm seat post, 22.2 mm handlebar and 9/16 in pedal threads are chosen to match adult roadster parts. Children's bikes often use 1/2 in pedal threads; GrowRider does not.
- **Bolted clamps, not quick releases.** 13 mm bolts discourage casual changes and theft of the seat post, and every mechanic already has the spanner.

## Safety

> **Safety:** GrowRider is ridden by children on roads shared with trucks and motorbikes. It is a concept. No part of it has been built or tested, and it must not be ridden until the frame, fork, sliding joints, rack and brakes have passed the tests of the applicable standard (ISO 8098 or ISO 4210) at a later TRL.

- **Brakes.** Two independent brakes are required (R7). The coaster brake stops working if the chain comes off, so the front brake is not optional. Small hands need a short-reach lever. Riders need to be shown that a hard front brake on loose gravel can skid the front wheel.
- **Telescoping parts.** A seat post or stem raised past its minimum insertion can break or pull out. Every sliding part carries a permanent minimum insertion mark, and a positive stop is proposed at TRL 3. Clamp slots are pinch points for fingers.
- **Rack limit.** The rack is rated 10 kg and marked. It must not carry passengers, water containers or goods above the rating: a heavy load high over the rear wheel makes a light bike hard for a child to steer and can lift the front wheel. The rack is sized for a school bag, with no footrests.
- **Road visibility.** School trips often start and end near dawn or dusk. Front white, rear red, spoke and pedal reflectors are fitted, and a bright frame color is proposed. A light (for example a hub dynamo) is suggested for a later version.
- **Helmet.** An adjustable, ventilated child helmet is proposed with each bike (BOM line 20). Hot-climate comfort will decide whether it is worn, so it needs to be discussed in co-design. Proposed, awaiting Amish.
- **Clothing and hot surfaces.** The chainguard keeps skirts and trousers out of the chain. A light saddle cover limits heating in the sun.
- **Mass.** At about 15.5 kg, the bike is about three quarters of the weight of a 20 kg six-year-old. This makes pushing, lifting and controlling a fall harder for the smallest riders, and is the reason R5 matters.

## Open questions for TRL 3

- Reduce mass toward 13 kg: chromoly tubes, pneumatic tires with liners, lighter rack and fenders. Which are acceptable to users and mechanics?
- Sliding joints in dust and rain: will greased steel sleeves seize over years of use? Would a split collar with a wiper seal or a plastic bushing help?
- Crank length: 140 mm is long for a 1.10 m rider and short for a 1.65 m rider. Keep one length, or offer a 127 mm swap for the smallest riders? Proposed: one length for the prototype, awaiting Amish.
- Which standard applies across the fit range, ISO 8098, ISO 4210 or both?
- Confirm with a partner which roadster parts are actually stocked in the target region, including coaster hubs and 20 in tires.
- Test the anthropometric assumptions (inseam ratio, reach) with measurements of children in the target region, where average heights may be below global references.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
