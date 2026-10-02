---
doc_id: GRR-PRB-001
title: GrowRider problem statement
project: GrowRider
doc_type: Problem statement
version: "0.7"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update (standard classification checked; open partner and region questions kept open per GRR-DDR-001)
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
  change: Budget stated as a value-engineering target (Amish, 2026-10-01)
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: First candidate partner (World Bicycle Relief) and first candidate region (Zambia), as decided by Amish on 2026-10-02
---

# GrowRider problem statement

Many rural children in sub-Saharan Africa and other low-income regions walk an hour or more each way to school, and the bicycles that could cut that time do not fit them: adult roadsters are too big, and imported children's bikes are light-duty, outgrown in two or three years and built from parts that local mechanics do not stock.

## The problem

A 5 km walk to school takes 60 to 75 minutes each way at 4 to 5 km/h. That is two to two and a half hours a day spent walking, often in heat, before and after a full school day. Distance is a known reason for late arrival, fatigue and dropout, especially for secondary-school girls, whose schools tend to be farther away.

Bicycles already help. Adult roadster bicycles are the working vehicle of rural East and Southern Africa, and programs such as World Bicycle Relief distribute rugged roadsters (the Buffalo bicycle) to students, health workers and farmers. But a roadster with 28 in wheels is sized for teenagers and adults. Younger and smaller children either walk, ride a bike that is far too big (unable to reach the ground or the brakes safely), or ride a cheap imported children's bike that breaks on rough roads and cannot be repaired with the parts sold in the local market.

A family that does buy a children's bike also faces growth: a child outgrows a fixed-size frame within two or three years, so the bike is either too small for the child who owns it or too big for the younger sibling who inherits it.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Child rider, ages about 6 to 14 (1.10 to 1.65 m) | A bike that fits now and keeps fitting; easy to stop; comfortable for 5 to 10 km a day; can carry a school bag | Dirt and gravel roads, sand, ruts, mud in the rainy season, shared roads with trucks and motorbikes |
| Parent or guardian | A durable, affordable bike that serves several children in turn; simple adjustment at home | Low and irregular cash income; siblings of different ages share one bike |
| School | Safe arrival of riders; secure parking; a teacher who can check fit and brakes | Rural primary and secondary schools, often 3 to 10 km from home |
| NGO or bicycle distribution program | A children's model that fits its existing supply chain, mechanic training and spare-parts network | Programs that already distribute adult roadsters to students and workers |
| Local mechanic | Parts that are already on the shelf; repairs with the tools already in the kit | Roadside and market stalls with spanners, pliers, a pump and roadster spares |

Context that shapes the design:

- **Rough roads.** Corrugated dirt, loose gravel, sand patches and ruts. Wheels, rims and the frame take repeated impacts, and braking grip is poor on loose surfaces.
- **Heat and dust.** Air temperatures of 35 °C or more, strong sun on black saddles and grips, and fine dust that works into bearings and sliding joints.
- **Thorns.** Acacia and similar thorns cause frequent punctures, and a flat tire far from a pump ends the day's riding.
- **Sharing and growth.** One bike may serve a 6-year-old and a 12-year-old in the same year, and pass down the family over ten years. Fit must change quickly, many times, without special tools.
- **Load pressure.** Children are often asked to carry siblings, water or goods. The rack must be rated low and marked clearly so the bike is not used as a cargo vehicle by or for children.

## Constraints

- Garage-buildable prototype, using a steel frame and bought-in bicycle components. Value-engineering target: USD 300 (`budget_usd` in `project.yaml`, raised from USD 250 on 2026-09-26; a hypothetical control target, not a limit, Amish, 2026-10-01). Estimated cost of the constructable design: USD 299 for the bike (USD 1 under the target), USD 311 with a helmet (USD 11 over).
- Wear parts should be the same as those used on the region's adult roadsters, so local mechanics can repair it with parts already on sale.
- Adjustment and routine service with basic hand tools (open-ended spanners and a screwdriver).
- Child safety comes before carrying capacity: two independent brakes, reflectors, a chainguard and a low rack rating.
- Designed primarily for the school commute. It is not a cargo or water-hauling bike.

## Out of scope

- Carrying passengers, water containers or loads above the rack rating.
- Electric assist, gears or suspension.
- Riders under about 1.10 m (balance bikes serve that group) or adults.
- Manufacturing, distribution financing and the school programs that would use the bike. These belong to partners.

## Prior work

- **Buffalo bicycle (World Bicycle Relief).** A rugged adult roadster designed for rural Africa, with a strong steel frame and a regional spare-parts and mechanic network. It is the reference for durability and parts commonality, but it is too large for young children.
- **Bicycle-for-school programs.** Programs in several African countries give bicycles to students, and a large state program in Bihar, India, that gave girls bicycles for secondary school was found to raise girls' enrollment (Muralidharan and Prakash, "Cycling to School," *American Economic Journal: Applied Economics*, 2017).
- **Adjustable children's bicycles.** Several commercial children's bikes in high-income markets offer extendable seat posts, stems or frames. They are mostly aluminum, use lightweight components not sold in rural markets, and are priced well above a roadster.
- **Standards.** ISO 8098 covers safety requirements for bicycles for young children, and ISO 4210 covers city and trekking bicycles for larger riders. The scopes are set by maximum saddle height: ISO 8098 covers bicycles with a maximum saddle height above 435 mm and below 635 mm, and ISO 4210-2 covers larger ones, with young adult bicycles from 635 to 750 mm ([ISO 8098:2023](https://www.iso.org/standard/78085.html), [ISO 4210-2:2023](https://www.iso.org/standard/78077.html)). GrowRider's maximum saddle height is about 890 mm, so it falls under ISO 4210-2 (GRR-CAL-001, section M).

## Open questions

- Which partner to work with first (a bicycle distribution NGO, a rural school network, or a regional bicycle assembler)? Decided by Amish on 2026-10-02: World Bicycle Relief, through its school bicycle programs and field mechanics, is the first candidate to approach, as partner and co-design partner (GRR-DEC-001).
- Which region to design for first? The Buffalo parts ecosystem suggests Zambia, Kenya or Malawi. Decided by Amish on 2026-10-02: Zambia is the first candidate region (GRR-DEC-001).
- How common is carrying a sibling on the rack, and what design cues (rack size, marking, no footrests) discourage it best? To learn in co-design.
- Would the smallest riders prefer a flat, low handlebar to the swept-back bar, whose grips sit 128 mm above the saddle at the smallest setting? A co-design question, decided by Amish on 2026-09-25 (GRR-DDR-002, D13).
- Can local frame builders work chromoly tube and weld aluminium, as the decided materials require (GRR-DDR-002, D7)? To learn with the partner.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
