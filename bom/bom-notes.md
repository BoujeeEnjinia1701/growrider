# BOM notes

Prices are indicative estimates by supplier type for a single prototype (TRL 3), not quotes. Every line is priced. Item numbers match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`; lines 18 to 20 are not modeled in detail. `docs/04-calcs/sizing.py` reads this file and prints the totals quoted in GRR-CAL-001 [J1].

- The bike itself (lines 1 to 19) comes to $281, $31 over the $250 budget in `project.yaml` (it was $243 before GRR-DDR-002).
- Adding the child helmet (line 20, $12) brings the total to $293 (was $255). The helmet's funding is still proposed, awaiting Amish (GRR-DDR-001, O1), and a budget change to $300 is proposed, awaiting Amish (GRR-DDR-002, N1). The budget is unchanged.
- GRR-DDR-002 changes (decided by Amish, 2026-09-25): chromoly 4130 main tubes (line 1, $40 to $58); chromoly steerer (line 2, $14 to $18); 29.2 x 1.8 mm chromoly sleeve (line 3, $9 to $13); chromoly quill (line 5, $10 to $14); alloy bar (line 6, $8 to $10); alloy front rim confirmed at the same price (line 7); alloy rear rim (line 8, $28 to $30); aluminium 6061-T6 rack (line 13, $10 to $14). Together they add $38 and save 0.9 kg (GRR-CAL-001 v0.2).
- The line 1 frame price covers tube and consumables only; a frame builder's labor is not included and would push the bike over budget if paid.
- The largest cost lines are the chromoly frame ($58), the solid tires ($32 for the pair, decided 2026-09-25) and the rear wheel with coaster brake hub ($30).
- Earlier TRL 3 changes: the fork needs a steerer with 220 mm usable length (longer than a stock 20 in fork), the stem is a long quill with 235 mm below the clamp, an alloy front rim was preferred for wet braking (now decided), plastic fenders are preferred for mass, the chain is 86 links, and line 19 now includes the positive stop bolts for the sliding parts. None changed a price.
- Parts commonality: lines 3 (post), 6, 10 (pedals), 11, 12, 16, 17, 18 and the hub internals in line 8 are intended to match parts sold for regional adult roadsters. Lines 7, 8 (rims), 9 and 14 are specific to the 20 in wheel size, and lines 2, 3 (sleeve) and 5 are made or modified parts. This must be checked against a real parts list from a partner.
- Production cost at volume is not estimated. The $120 target (decided 2026-09-25) needs an estimate from a regional assembler.
