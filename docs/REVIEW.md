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

1. Wheel size: 20 in (ISO 406), recommended, or 24 in (ISO 507), which fails standover for 1.10 m riders.
2. Brakes: coaster brake plus front rim brake, recommended; alternatives are coaster only or two hand brakes.
3. Frame: step-through with twin down tubes, recommended, or a small diamond frame.
4. Tires: solid or airless, recommended for the prototype, or thorn-resistant tubes with liners (about 1 kg lighter and $10 cheaper).
5. Helmet: supply one with each bike (BOM line 20). Either fund it from the $250 budget ($5 over), fund it separately, or raise the budget to about $275. The budget in `project.yaml` is unchanged at $250.
6. Crank length: one 140 mm length for the prototype, with a possible 127 mm swap for the smallest riders later.
7. Production cost target of $120 or less at volume (R11), and first partner and region (a distribution NGO or school network, in Zambia, Kenya or Malawi).

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
