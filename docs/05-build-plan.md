---
doc_id: GRR-BLD-001
title: GrowRider prototype build plan
project: GrowRider
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (GRR-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: GRR-DDR-003 accepted by Amish; painted height scales on the sleeve and quill, a bright painted band above the quill's insertion mark, and the name screen printed on the chainguard
---

# GrowRider prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order, with the bike set for a 1.38 m rider.*

The prototype is one GrowRider: a step-through children's bicycle on 20 in wheels whose seat post and handlebar stem slide to fit riders from about 1.10 to 1.65 m tall. Figure 1 shows its 24 components in the order you make or fit them. Eight are made in a frame builder's workshop: the two rear dropouts, the brazed frame, the seat post sleeve, the two clamp collars with their stop screws, the slotted seat post, the quill stem with its welded head plate, the aluminium bar clamp block and the welded aluminium rack. Everything else is bought and fitted: fork, headset, bottom bracket, wheels with a coaster brake hub, solid tires, crankset, chain, front brake, saddle, handlebar, fenders, chainguard, kickstand, reflectors and bell. The work is cutting and mitring steel tube, cutting plate, brazing or TIG welding chromoly on a jig, reaming, drilling and filing slots, TIG welding aluminium, and ordinary bicycle assembly. The parts cost about USD 299 for the bike, from the bill of materials.

> **Safety:** This bicycle is for children, who will ride it on roads shared with motor traffic. Nobody may ride the prototype: the frame, fork, seat post, stem, rack and brakes must first pass the tests of ISO 4210-2, which is TRL 4 work. Brazing and welding chromoly and aluminium need training, fume extraction and fire precautions. Cut tube and plate edges are sharp; deburr everything. The sliding seat post and stem must never be set above their minimum insertion marks.

## 2. What changed to make it buildable

The concept showed what the bike does; some of its parts could not be made, fitted or fixed as drawn. Each change below keeps what the bike does (the same wheels, frame geometry, fit range, bar heights, reach, brakes and rack), and all of them are recorded in decision record GRR-DDR-003, accepted by Amish on 2026-10-01.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Rear dropouts | Plain blocks 105 mm apart, no slot | 6 mm plates with a slot open to the rear, 110 mm apart, with an eyelet (Figure 2) | The axle slides back to tension the chain of a single-speed coaster hub |
| Seat stays | Joined the seat tube where the clamp collar sits | Joined to a cross bar 25 mm lower, which holds them 80 mm apart (Figure 6) | The collar closes on plain tube, and the rear fender passes between the stays |
| Sliding seat post | "Positive stop bolts" with no way to fit them | A stop screw in each clamp collar riding in a slot in the part inside (Figures 10 and 12) | Each stage stops with 100 mm still inserted and cannot be pulled past it |
| Head tube | 31 mm bore | 30 mm bore (34 x 2.0 mm tube) | Standard 1 in headset cups press into it |
| Quill stem | 22.2 mm quill, which cannot slide in the 22.2 mm steerer bore; a head at 0 or 60 mm that no single part could be | 22.0 mm quill with a welded head plate; a bar clamp block bolted at one of two positions (Figures 13 and 16) | The quill slides; the two bar positions are one part; the grips sit where the concept had them |
| Handlebar | 160 mm sweep, 25 mm rise | 205 mm sweep, 15 mm rise | Keeps the grips in place with the clamp block ahead of the expander bolt |
| Rack | Struts and stays ending in the air; front end under the saddle | Tabs bolted to the dropout eyelets and to bosses on the seat stays; 30 mm lower (Figure 17) | Four bolted fixings; the saddle clears the rack at the lowest setting |
| Front fender and caliper | Fender passing under a crown it did not fit under; caliper with no reach given | A crown 16 mm deep, the front fender 12 mm off the tire, a long-reach caliper of about 84 mm (Figure 18) | Everything fits under the crown on one bolt |
| Coaster brake arm, kickstand, chainguard | No fixings | Arm clip on the chainstay; kickstand plate under the chainstays; chainguard clip and boss (Figures 7 and 19) | Each part is held to the frame |
| Chain line | 48 mm, which put the sprocket into the chainstay | 42 mm, chainstays placed to suit | The sprocket, chainring and chain clear the frame by 2 mm or more |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as the rider sits; the chain is on the right. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Rear dropouts (make 2: a left and a right)

![Figure 2. Making sketch of the rear dropout](../cad/drawings/GRR-DWG-101.png)

*Figure 2. Rear dropout making sketch (GRR-DWG-101).*

**What it is and what it is made from.** The flat plate at each end of the rear stays that holds the rear axle. Steel plate 6 mm thick (S235, or 4130 to match the frame), 82 x 54 mm blanks.

**How to make it.**

1. Mark the outline on the plate, measuring from the axle center: 30 behind it to 52 ahead, 16 below to 38 above, with the upper front corner cut down to the front edge as Figure 2 shows.
2. Saw and file to the line. Break every edge.
3. Drill 10 mm with its center 3 mm ahead of the axle center: this is the round end of the slot.
4. Saw the two sides of the slot from the rear edge to the hole, 10 apart, and file them straight and parallel.
5. Drill the eyelet 5.5 mm, 18 behind and 20 above the axle center.
6. Make the second plate as a mirror image (the eyelet is in the same place; only the sides are swapped).

**How it fits the parts next to it.**

![Figure 3. Joint 1: left rear dropout, seen from outside](05-build-plan/joint-01.png)

*Figure 3. The axle sits in the slot and slides back to tension the chain; one M5 bolt holds the fender stay and the rack strut tab on the eyelet.*

The chainstay end and the seat stay end are each slotted 6 mm and brazed over the plate: the chainstay 40 ahead of the axle and level with it, the seat stay 16 ahead and 20 above. The two plates' inner faces are 110 apart, which is the width of the coaster hub over its locknuts. The rear axle nuts bear on the outer faces.

**Check before moving on.** A 3/8 in axle slides the full length of the slot without binding.

### 3.2 Frame

![Figure 4. Making sketch of the frame](../cad/drawings/GRR-DWG-102.png)

*Figure 4. Frame making sketch (GRR-DWG-102).*

![Figure 5. Frame layout for the jig](05-build-plan/frame-layout.png)

*Figure 5. Tube center lines and key points from the bottom bracket center, for setting up the jig.*

**What it is and what it is made from.** The step-through frame: head tube, seat tube, down tube and a second, higher "loop" tube between them (the twin down tubes), the bottom bracket shell, two chainstays, two seat stays on a cross bar, and the dropouts. Chromoly 4130 tube for the main tubes: head tube 34 x 2.0, seat tube 31.8 x 1.2, down tube 31.8 x 0.9, loop tube 28.6 x 0.9. Steel tube for the stays (chainstays 19 x 1.2, seat stays and cross bar 16 x 1.2, fender bridge 12 x 1.0). A 68 mm threaded (BSA) bottom bracket shell, bought. Small fittings from 4 mm steel plate and M5 brazing bosses.

**How to make it.**

1. Set up a flat frame jig to Figure 5. Every position is in millimetres from the bottom bracket center: forward and up. The head and seat axes both lean back 70° from the ground.
2. Cut each tube 10 longer than its center-line length in Figure 5, then file the mitre at each end to fit the tube it meets, checking on the jig. Mitre the down tube and loop tube onto the head tube and the bottom bracket shell or seat tube, never into the bore.
3. The down tube meets the head tube with its edge at least 3 above the head tube's lower end, so the lower headset cup has a clean round end to press into.
4. Tack the front triangle (head tube, seat tube, down tube, loop tube, shell) on the jig, check it is flat, then braze or TIG weld it.
5. Chainstays: 21 each side of center at the shell, 58 each side at the dropouts; slot each rear end 6 wide and 20 deep for the dropout plate.
6. Seat stays: braze the cross bar across the back of the seat tube, its center 235 up the seat axis and 25 behind the seat tube's center line; the stays meet it 40 each side of center and run to the dropouts, 58 each side, each slotted 6 wide for the plate.
7. Hold the two dropouts on a 3/8 in dummy axle with their inner faces 110 apart and centered, and braze the stays to them.
8. Fittings: the 12 mm fender bridge between the seat stays where they are 292 from the axle; the kickstand plate (40 x 64 x 4) under both chainstays, 55 behind the bottom bracket center, with a 10.5 hole in its middle; an M5 boss on the outside of each seat stay at the rack's front end; an M5 boss on top of the right chainstay, 38 % of the way from the dropout to the bottom bracket, for the chainguard.
9. Seat tube top: saw a 2 wide, 26 long slit at the back so the collar can close it, and drill a 5.5 hole on the left side, 7 below the top, for the stop screw.
10. After brazing: ream the seat tube to 29.4 down to the bottom bracket shell, ream the head tube ends to 30.0 and face them square, chase and face the bottom bracket threads. Clean off flux, and powder coat.

**How it fits the parts next to it.**

![Figure 6. Joint 8: seat stay cross bar, fender bridge and rack stay](05-build-plan/joint-08.png)

*Figure 6. The cross bar holds the seat stays 80 apart so the 64 wide fender passes between them; the rack's front stays bolt to bosses on the seat stays.*

![Figure 7. Joint 9: kickstand on the kickstand plate](05-build-plan/joint-09.png)

*Figure 7. The kickstand plate is brazed under both chainstays; the kickstand clamps to it with one M10 bolt and clears the chain.*

The sleeve slides in the reamed seat tube with 0.2 clearance on the diameter. The headset cups press into the reamed head tube. The bottom bracket threads into the shell. The rack, fenders, chainguard and kickstand all bolt to the bosses, bridge, plate and eyelets named above.

**Check before moving on.** On the jig or a flat table: the dropouts are centered on the frame's center plane within 1, level, and 110 apart; the head and seat tubes lie in the frame's center plane within 1; the sleeve slides the full depth of the seat tube.

### 3.3 Seat post sleeve

![Figure 8. Making sketch of the seat post sleeve](../cad/drawings/GRR-DWG-103.png)

*Figure 8. Seat post sleeve making sketch (GRR-DWG-103), drawn lying down with its slot facing up.*

**What it is and what it is made from.** The first sliding stage: a tube that slides in the seat tube and that the seat post slides in. Chromoly 4130 tube 29.2 x 1.8, 250 long.

**How to make it.**

1. Cut 250 long; square and deburr both ends inside and out.
2. On the left side, scribe a line along the tube and mark a slot 6 wide from 90 to 226 up from the bottom end.
3. Chain drill 6 holes along the line and file the slot's sides straight. File its two ends square: they are the stops.
4. At the top end, saw a 2 wide, 26 long slit at the back, and drill a 5.5 hole on the right side, 7 below the top, for the post's stop screw.
5. Scribe the minimum insertion mark all the way round, 100 up from the bottom end.
6. Paint a height scale on the part that shows above the seat tube: a band every 20 mm and a longer band every 60 mm, so a setting can be noted and reset.

**How it fits the parts next to it.** It slides in the seat tube, slot to the left, and the seat tube collar's stop screw rides in the slot (Figure 10). The seat post slides inside it (Figure 12).

**Check before moving on.** The slot ends are square; no burr inside the bore; the post slides through the whole sleeve.

### 3.4 Clamp collars with stop screws (make 2)

![Figure 9. Making sketch of the clamp collars](../cad/drawings/GRR-DWG-104.png)

*Figure 9. Clamp collar making sketch (GRR-DWG-104); the seat tube collar is drawn, the sleeve collar is the same at its own size.*

**What it is and what it is made from.** The bolt-up collars that lock each sliding stage, each carrying the stop screw for the part inside. Two bought steel clamp collars with 13 mm (M8) bolts: 31.8 for the seat tube and 29.8 for the sleeve. Two M5 x 10 dog-point screws.

**How to make it.**

1. On each collar, mark a point half way up, a quarter turn from the clamp bolt.
2. Drill 4.2 square to the bore and tap M5.
3. Seat tube collar: the hole is on the left. Sleeve collar: the hole is on the right.
4. Grind the seat tube collar's screw so its tip enters the sleeve slot 1.5 and never reaches the post (the sleeve wall is 1.8 thick). Grind the sleeve collar's screw so its tip enters the post slot about 1.5.

**How it fits the parts next to it.**

![Figure 10. Joint 3: seat tube collar and the sleeve's stop screw](05-build-plan/joint-03.png)

*Figure 10. Cut open across the bike and seen from the front: the screw passes through the collar and the seat tube wall into the sleeve's slot, and its tip stops 0.6 short of the post.*

Each collar sits flush with the top of its tube, its slit over the tube's slit at the back, its hole lined up with the hole in the tube.

**Check before moving on.** With the screw in, the part inside slides from one slot end to the other and stops at each; the collar bolt closes the tube without the screw binding.

### 3.5 Seat post, slotted

![Figure 11. Making sketch of the seat post](../cad/drawings/GRR-DWG-105.png)

*Figure 11. Seat post making sketch (GRR-DWG-105), drawn lying down with its slot facing up.*

**What it is and what it is made from.** The second sliding stage, carrying the saddle. A bought plain 25.4 steel seat post with a top saddle clamp, 1.8 wall, cut to 280 long.

**How to make it.**

1. Cut to 280 if longer; deburr the bottom end.
2. On the right side, scribe a line along the post and mark a slot 6 wide from 90 to 236 up from the bottom end.
3. Chain drill and file as for the sleeve, ends square. The slot is on the side, where fore-and-aft bending stress is lowest; it lowers the post's stiffness by under 1 %.
4. Scribe the minimum insertion mark all the way round, 100 up from the bottom end.

**How it fits the parts next to it.**

![Figure 12. Joint 4: sleeve collar and the post's stop screw](05-build-plan/joint-04.png)

*Figure 12. The same arrangement one stage up, on the right: the sleeve collar's screw rides in the post's slot.*

The post slides in the sleeve, slot to the right, with 0.2 clearance on the diameter. The screw also keys the post so the saddle stays pointing forward.

**Check before moving on.** The slot is straight along the post; the post slides in the sleeve from stop to stop.

### 3.6 Quill stem with head plate

![Figure 13. Making sketch of the quill stem](../cad/drawings/GRR-DWG-106.png)

*Figure 13. Quill stem making sketch (GRR-DWG-106).*

**What it is and what it is made from.** The sliding stem that sets handlebar height: a tube in the fork's steerer, locked by an expander wedge, with a flat plate on top that carries the bar clamp. Chromoly 4130 tube 22.0 x 2.0, 240 long; 4130 plate 10 thick, 127 x 44; a 3 mm steel cap; a bought quill expander wedge and an M8 x 260 expander bolt with a 13 mm head.

**How to make it.**

1. Cut the quill 240 long. Cut the bottom end at the angle of your wedge (most are 45°).
2. Weld the cap into the top end and drill it 8.5 for the expander bolt.
3. Cut the plate to 127 x 44. File one end to the quill's 22 curve so it sits snug against the quill's front.
4. Drill 6.8 and tap M8, eight holes: at 27, 63, 87 and 123 ahead of the quill's center line, each 13 each side of the plate's center line. The first four are the back bar position, the last four the front.
5. Hold the quill leaning back 20° from upright (a 70° block on the welding table) and the plate level across its front, the plate's top flush with the quill's top. TIG weld both sides of the joint.
6. Fit the wedge and expander bolt. Scribe the minimum insertion mark all the way round, 100 up from the quill's bottom.
7. Paint a bright band all the way round just above the mark, so a quill set close to its limit is easy to see. Above the band, paint a height scale like the sleeve's: a band every 20 mm and a longer band every 60 mm.

**How it fits the parts next to it.**

![Figure 14. Joint 5: head tube, headset, steerer and quill](05-build-plan/joint-05.png)

*Figure 14. Cut open on the center plane: the quill slides in the steerer's 22.2 bore; the expander bolt pulls the wedge up to lock it.*

The quill slides in the steerer with 0.2 clearance on the diameter. At the lowest setting the quill top stands 20 above the headset locknut and the plate clears the locknut by 2. The quill has no stop screw: the minimum insertion mark is the only limit, so it must always be inside the steerer; the bright band above it catches the eye when the quill is near its limit (safety stop S4).

**Check before moving on.** The quill slides the full 120 of travel; the plate is level when the quill is in the steerer.

### 3.7 Bar clamp block

![Figure 15. Making sketch of the bar clamp block](../cad/drawings/GRR-DWG-107.png)

*Figure 15. Bar clamp block making sketch (GRR-DWG-107).*

**What it is and what it is made from.** The two-piece block that clamps the handlebar to the head plate. Aluminium 6061-T6 flat bar 45 x 30 (or 50 x 30); four M8 x 40 bolts with 13 mm heads.

**How to make it.**

1. Saw a 56 long piece and file or mill it square to 54 x 44 x 30.
2. Across the 44 width, at mid-length and 15 up from the bottom, drill a pilot, then 22, then ream 22.2 (or bore it on a lathe).
3. Drill four 8.5 holes straight through, 18 each side of the bar hole and 13 each side of the middle.
4. Saw the block in half through the bar hole's center line and file the sawn faces flat, so the closed halves leave about a 1 gap and grip the bar.
5. Break every edge, especially round the bar hole.

**How it fits the parts next to it.**

![Figure 16. Joint 6: bar clamp block on the head plate](05-build-plan/joint-06.png)

*Figure 16. The lower half sits on the head plate over one set of holes; the cap goes over the bar; four bolts pass through both halves into the tapped plate.*

In the back position the bar is 45 ahead of the steering axis, in the front position 105. Moving between them takes the four bolts and a 13 mm spanner. The expander bolt head stays clear for a socket in both positions.

**Check before moving on.** With the bolts tight the bar turns in the clamp only with a firm twist.

### 3.8 Rack

![Figure 17. Making sketch of the rack](../cad/drawings/GRR-DWG-108.png)

*Figure 17. Rack making sketch (GRR-DWG-108).*

**What it is and what it is made from.** The small rear platform for a school bag, rated 10 kg. Aluminium 6061-T6 tube 12 x 1.5; 3 mm aluminium tabs; a rating plate.

**How to make it.**

1. Platform: three rails 300 long (the middle one and one each side, 60 from the middle) and three cross bars 120 long at both ends and the middle. Weld in a flat jig.
2. Struts: one from each rear corner down to a dropout eyelet, about 300 long. Flatten 30 at the lower end and weld on a 3 mm tab drilled 5.5.
3. Stays: one from each front corner down to the boss on each seat stay, about 120 long, with a drilled 3 mm tab at the end.
4. Weld the struts and stays with the rack in a jig taken off the frame, so the tabs land on the eyelets and bosses unforced.
5. Fix the rating plate across the rear, marked "MAX 10 kg", with the rear reflector.

**How it fits the parts next to it.** The struts' tabs go on the outside of the dropout eyelets, over the fender stay eyes (Figure 3); the stays' tabs go on the seat stay bosses (Figure 6). Four M5 bolts. The platform sits level, 545 above the ground; it clears the fender by 20 and the saddle by 37 at the lowest saddle setting.

**Check before moving on.** All four tabs sit flat on their eyelets and bosses with the bolts in by hand.

### 3.9 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Fork (line 2).** 20 in (ISO 406), 30 mm offset, crown no deeper than 16, a 1 in threaded chromoly steerer 25.4 x 1.6 (22.2 bore) with 220 usable above the crown, slotted fork ends 100 apart with M5 eyelets, a hole through the crown for the caliper bolt. Cut and thread the steerer to suit the head tube if needed.
- **Headset and bottom bracket (line 18).** 1 in threaded headset with 30.0 press-in cups and a 32 mm locknut; cup-and-cone or cartridge bottom bracket for a 68 mm BSA shell.
- **Wheels (lines 7 and 8).** 20 in (ISO 406) alloy rims. Front: 28 spokes, 100 between locknuts, 3/8 in nutted axle. Rear: 36 spokes, single-speed coaster brake hub 110 between locknuts, 18T sprocket on a 42 chain line, with its brake arm.
- **Arm clip (line 19).** A coaster brake arm clip for a 19 mm chainstay, with an M6 bolt.

![Figure 18. Joint 2: coaster brake arm clipped to the left chainstay](05-build-plan/joint-02.png)

*Figure 18. The clip's band goes round the chainstay and its legs either side of the arm; one M6 bolt under the arm takes the braking force.*

- **Tires (line 9).** Two 20 x 1.95 in solid or airless tires, no wider than 50 on the rim.
- **Crankset and pedals (line 10).** 140 mm steel cranks, 32T chainring on a 42 chain line, 9/16 in pedal threads, reflective pedals.
- **Chain (line 11).** 1/2 x 1/8 in single-speed chain, 86 links.
- **Front brake (line 12).** A long-reach side-pull caliper whose reach covers 84, on a nutted bolt; a short-reach child's lever with reach adjustment; cable and housing with slack for 120 of stem travel.

![Figure 19. Joint 7: front caliper and fender bracket at the fork crown](05-build-plan/joint-07.png)

*Figure 19. One bolt through the crown carries the caliper in front and the front fender bracket behind; the fender clears the crown by 7.*

- **Saddle (line 4), handlebar and grips (line 6).** Child-size saddle with a standard rail clamp. 22.2 alloy roadster-style bar, 520 wide, about 205 sweep and 15 rise; rubber grips.
- **Fenders (line 14).** Plastic, 20 in, 64 wide, with wire stays and L brackets. Trim the rear fender's front end to start 10° above the axle line.
- **Chainguard (line 15).** Plate guard for the upper chain run, with a seat tube clip and a tab for the chainstay boss. The name "GrowRider" is screen printed on its outer face.
- **Kickstand (line 16).** Centre-mount kickstand with its clamp plate and an M10 bolt.
- **Reflectors and bell (line 17).** Front white, rear red, two spoke reflectors per wheel, bell.
- **Fixings (line 19).** M8 collar bolts; M5 bolts with nyloc nuts for the rack, fender stays and chainguard; grease; warning labels for the minimum insertion marks.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Grease every thread and every sliding surface.

### Step 1: bottom bracket into the frame

![Step 1](05-build-plan/step-01.png)

Right-hand (drive side) cup in first; it has a left-hand thread. Tighten it fully. Spindle in, then the left cup and lockring, set so the spindle turns freely with no play.

### Step 2: headset cups and fork

![Step 2](05-build-plan/step-02.png)

Press both cups into the head tube with a headset press or a threaded rod and washers. Fit the crown race on the fork. Fork up through the head tube; top bearing, top cup, keyed washer and locknut. Set so the fork turns freely with no play, then lock with the 32 mm spanner.

### Step 3: sleeve into the seat tube, collar and stop screw

![Step 3](05-build-plan/step-03.png)

Sleeve in with its slot to the left. Collar on, flush with the top of the seat tube, its hole over the hole in the tube. Stop screw in. Set the sleeve height and tighten the 13 mm collar bolt. **Hold point:** pull the sleeve up; it must stop with its minimum insertion mark still inside the seat tube.

### Step 4: seat post, sleeve collar and saddle

![Step 4](05-build-plan/step-04.png)

Post in with its slot to the right. Sleeve collar on, flush with the sleeve top, and its stop screw in. Saddle clamped level on the post. **Hold point:** pull the post up; it must stop with its mark inside the sleeve.

### Step 5: quill stem into the steerer

![Step 5](05-build-plan/step-05.png)

Quill in to the chosen height, head plate square to the front wheel; tighten the 13 mm expander bolt. **Hold point:** the minimum insertion mark is inside the steerer (safety stop S4).

### Step 6: bar clamp block and handlebar

![Step 6](05-build-plan/step-06.png)

Lower half of the block on the chosen set of holes; bar on it, centered, grips level; cap on; four M8 x 40 bolts tightened evenly in a cross pattern. Fit the grips and the brake lever on the right grip.

### Step 7: front fender and caliper on the crown

![Step 7](05-build-plan/step-07.png)

Front fender up between the fork blades, its bracket behind the crown; caliper in front; one bolt through all three, nut behind. Leave the fender stays loose until step 9.

### Step 8: tires onto the rims

![Step 8](05-build-plan/step-08.png)

Soak each solid tire in hot water for a few minutes to soften it. Seat one side on the rim, then work the other side on with tire levers, a little at a time round the rim. Same for the rear wheel.

### Step 9: front wheel into the fork

![Step 9](05-build-plan/step-09.png)

Axle up into the fork ends, wheel centered between the blades; axle nuts tight. Fender stays onto the fork-end eyelets with M5 bolts. Set the caliper pads on the rim's brake track.

### Step 10: crankset and pedals

![Step 10](05-build-plan/step-10.png)

Chainring on the right. Cranks onto the spindle and tight. Pedals in; the left pedal has a left-hand thread.

### Step 11: rear wheel into the track ends

![Step 11](05-build-plan/step-11.png)

Slide the axle forward into both slots, sprocket on the right, brake arm on the left under the chainstay. Nuts finger tight for now.

### Step 12: chain, tension and brake arm clip

![Step 12](05-build-plan/step-12.png)

Chain on and joined. Pull the axle back until the chain moves 10 to 15 up and down half way between the sprocket and chainring, wheel centered; tighten both axle nuts. Clip the brake arm to the chainstay and tighten the M6 bolt. **Hold point:** back-pedal hard by hand; the wheel locks and the arm does not move.

### Step 13: rear fender and stays

![Step 13](05-build-plan/step-13.png)

Fender up between the seat stays; its bracket bolted to the bridge; stays to the dropout eyelets, against the plates.

### Step 14: rack

![Step 14](05-build-plan/step-14.png)

Strut tabs on the dropout eyelets over the fender stay eyes, stay tabs on the seat stay bosses; four M5 bolts with nyloc nuts.

### Step 15: chainguard

![Step 15](05-build-plan/step-15.png)

Clip round the seat tube, tab on the chainstay boss. Turn the cranks: the guard clears the chain and the crank arm.

### Step 16: kickstand

![Step 16](05-build-plan/step-16.png)

Clamp plate under the kickstand plate, leg on the left, M10 bolt tight. Cut the leg so the bike leans a little to the left when parked.

### Step 17: reflectors, bell and brake cable

![Step 17](05-build-plan/step-17.png)

Front reflector on the front of the head plate, rear reflector on the rack plate, two spoke reflectors per wheel, bell on the bar. Run the brake cable with enough slack for the stem's full 120 of travel; set the lever reach for small hands.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of GRR-REQ-001. Nobody rides the bike for any of them.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Standover | R1 | Measure the loop tube's top 100 ahead of its joint with the seat tube | 470 or less above the ground (455 expected) |
| Saddle height range and stops | R2 | Set the saddle fully down, then pull each stage up to its stop; measure bottom bracket center to saddle top along the seat tube | 400 or less fully down; 670 or more at the top; every insertion mark still inside at the stops |
| Bar height and reach | R3 | Run the quill through its 120 of travel; fit the block in both positions; measure grip positions | Bar height changes by 100 or more; reach changes by 100 or more over the range |
| Wheel size | R4 | Inspect | 20 in (ISO 406) rims front and rear |
| Mass | R5 | Weigh the complete bike with rack, fenders and kickstand | Record against 13 kg (15.1 kg estimated) |
| Rack | R6 | Inspect the marking; hang 10 kg on the platform for 5 minutes, bike on its kickstand and held | Marked "MAX 10 kg"; platform 300 x 120 or less; no permanent bend |
| Brakes, on the stand | R7 | Spin each wheel by hand and brake; check the lever reach with a child's hand span | Each brake stops its wheel; pads on the brake track, clear of the tire; lever reachable at its shortest setting |
| Puncture-proof tires | R8 | Inspect | Solid or airless tires fitted, seated evenly |
| Fit change | R9 | Time a change from the smallest to the largest setting with a 13 mm spanner and a screwdriver | 10 minutes or less, no other tool |
| Stops and sliding parts | R2, R12 | Slide each stage stop to stop, ten times | No binding; each stop holds with the collar bolt loose |
| Frame alignment | R12 | String line from the dropouts to the head tube; check the rear wheel sits centered | Rear wheel centered within 2; dropouts parallel |
| Clearances | All | Turn the bar lock to lock and spin both wheels and the cranks | Nothing rubs: tire to frame 3 or more, fender to crown 5 or more, chain to frame and guard 2 or more |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before brazing or welding.** The person brazing chromoly or TIG welding aluminium is trained for it; fume extraction is on; no galvanised or plated parts are being heated; a fire extinguisher and a metal bin for hot offcuts are at hand.
- **S2. Before the frame comes off the jig.** The frame and dropout checks of section 3.2 pass. A frame that is out of line is corrected on the jig, never by bending a brazed joint cold.
- **S3. Before any sliding part is set for a rider.** Both stop screws are in, and each stage stops with its minimum insertion mark still inside the tube below. The warning labels for the marks are on.
- **S4. At every stem setting.** The quill has no stop screw: its minimum insertion mark must be inside the steerer, below the locknut, every time the stem is set (if the bright band shows in full above the locknut, check the mark), and the expander bolt is tight.
- **S5. Before any load on the rack or the saddle.** Every bolt is tight with its nyloc nut or collar; the rack is marked "MAX 10 kg"; nothing heavier goes on it, and never a passenger.
- **S6. Before anyone rides it.** Nobody rides the prototype. The frame, fork, seat post, stem, rack and brakes must first pass the tests of ISO 4210-2, which is TRL 4 work and outside this plan.
- **S7. When fitting solid tires.** Hot water can scald and a tire lever can spring back: wear gloves and eye protection.

## 7. Tools, skills and workspace

**Tools.** Tube cutter or hacksaw; mitre files or a tube notcher; flat frame jig; brazing torch (or TIG welder) for chromoly and a TIG welder for aluminium; bench vice with soft jaws; bench drill; drills 4.2 to 12 mm and a 22 mm drill; 22.2 and 29.4 mm reamers, a 30.0 mm head tube reamer and facer, a bottom bracket tap and facer (or a frame builder's shop that has them); M5 and M8 taps; files; scriber, square, steel rule and calipers; headset press; bottom bracket tools, a 32 mm headset spanner and a lockring spanner; 13 and 15 mm spanners, sockets and a screwdriver; tire levers; chain tool; spoke key; spring balance or scale to 30 kg; stopwatch.

**Skills.** Frame building: mitring, brazing or TIG welding chromoly on a jig, and TIG welding aluminium for the rack. Basic metalwork: cutting, drilling, tapping, filing a slot. Bicycle assembly: headset, bottom bracket, wheels, chain and brakes. A local frame builder can make sections 3.1 to 3.8; any bicycle mechanic can do section 4.

**Workspace.** A metalwork bench with the frame jig; a ventilated brazing and welding area away from anything that burns; a clean assembly bench with a bicycle repair stand.

**Personal protective equipment.** Welding helmet, gloves and leather apron for brazing and welding; safety glasses for cutting, drilling and filing; hearing protection when cutting tube; gloves when handling cut tube and plate; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 66 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/GRR-DWG-101` to `GRR-DWG-108`.
- General arrangement: `cad/drawings/GRR-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (GRR-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; fit [A], reach [B], crown clearance and caliper reach [C3], mass [D], rack [E], braking [F], fit change [H], cost [J], strength [K].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (GRR-DDR-003), with GRR-DDR-001 and GRR-DDR-002; open items in `docs/06-design-decisions.md` (GRR-DEC-001).
- Requirements: `docs/03-requirements.md` (GRR-REQ-001 v0.6).
