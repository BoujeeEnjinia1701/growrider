"""GrowRider sizing calculations for GRR-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Every number quoted in docs/04-calcs/01-sizing.md is printed here with a tag
such as [A1]. Geometry comes from cad/src/model.py (PARAMS), so the calc note,
the STEP files and drawing GRR-DWG-001 use the same dimensions.
First-principles estimates for a paper proof of concept; not a substitute for
the tests of ISO 8098 or ISO 4210.
"""
import csv
import sys
from math import atan, cos, degrees, pi, radians, sin, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, SETTINGS, derived, grip_pt, saddle_pt, split_saddle, tube_lengths  # noqa: E402

g = 9.81
D = derived(P)
R_TIRE = D["R"] / 1000          # m
L = P["wheelbase"] / 1000       # m
STATUS = {}
# Prototype budget, read from project.yaml (raised from $250 to $300 by Amish, 2026-09-26)
BUDGET = float(next(l.split(":", 1)[1] for l in (ROOT / "project.yaml").read_text().splitlines()
                    if l.startswith("budget_usd:")).strip())


def out(tag, text):
    print(f"[{tag}] {text}")


def status(req, value, target, state):
    STATUS[req] = (value, target, state)


# ------------------------------------------------------------------ assumptions
RIDERS = {  # height m, mass kg (1.65 m at 60 kg per GRR-REQ-001 assumptions)
    "small": (1.10, 19.0),
    "mid": (1.38, 32.0),
    "large": (1.65, 60.0),
}
INSEAM_K = 0.45          # inseam / height
SADDLE_K_A = 0.88        # rule A: BB to saddle top = 0.88 x inseam (adult rule, used at TRL 2)
SADDLE_K_B = 1.09        # rule B: saddle top to pedal at the bottom of the stroke = 1.09 x inseam
REACH_K = 0.20           # saddle-to-grip horizontal reach = 0.2 x height (placeholder, REQ assumption)
RIDER_CG_UP = 0.18       # rider center of mass above the saddle top, x height (upright, seated)
RIDER_CG_FWD = 0.25      # rider center of mass forward of the saddle, fraction of saddle-to-grip distance
BIKE_CG = (0.45, 0.40)   # bike center of mass: fraction of wheelbase ahead of the rear axle, height m
MU = {"dry": 0.7, "gravel": 0.4}       # tire-ground friction
COASTER_K = 2.5          # coaster brake: hub brake torque / sprocket drive torque (2 to 3 typical, to confirm)
BACKPEDAL_K = 0.5        # back-pedal force a seated rider can apply, x body weight
LEVER_MA = 5.0           # front brake: total pad normal force / hand force at the lever
PAD_MU = {"dry": 0.5, "wet alloy": 0.3, "wet steel": 0.1}
R_BRAKE = 0.200          # rim braking radius, m
HAND_F = {"small": 40.0, "mid": 70.0, "large": 150.0}   # sustained lever force, N (assumed)
STEEL_RHO = 7850.0
ALU_RHO = 2700.0
YIELD = 250.0            # MPa, hi-tensile bicycle tube (conservative)
FATIGUE_ALLOW = 60.0     # MPa at 1 g for a brazed, welded or clamped joint in hi-tensile steel (screening value)
CRMO_YIELD = 435.0       # MPa, chromoly 4130, normalized (typical)
CRMO_FATIGUE = 90.0      # MPa at 1 g, chromoly sections (screen scaled by tensile strength, about 670 vs 430 MPa; assumed)
ALU_WELD_YIELD = 110.0   # MPa, 6061-T6 in the heat-affected zone of a weld (typical design value)
PEAK_G = 2.5             # bump factor for the static strength check

# ------------------------------------------------------------------ A. fit (R1, R2)
print("A. Fit")
need = {}
for k, (h, m) in RIDERS.items():
    ins = INSEAM_K * h * 1000
    a = SADDLE_K_A * ins
    b = SADDLE_K_B * ins - P["crank"]
    need[k] = (ins, a, b)
    out("A1", f"{k}: height {h:.2f} m, inseam {ins:.0f} mm, saddle height rule A {a:.0f} mm, rule B {b:.0f} mm")
lo_req = min(need["small"][1], need["small"][2])
hi_req = max(need["large"][1], need["large"][2])
out("A2", f"design saddle range {D['saddle_min']:.0f} to {D['saddle_max']:.0f} mm "
          f"({D['saddle_max'] - D['saddle_min']:.0f} mm); needed {lo_req:.0f} to {hi_req:.0f} mm under either rule")
out("A3", f"minimum insertion: sleeve {D['sleeve_insert_min']:.0f} mm, post {D['post_insert_min']:.0f} mm, "
          f"quill {D['quill_insert_min']:.0f} mm (target 100 mm)")
out("A4", f"bore depth: sleeve bottom at most {D['sleeve_depth_max']:.0f} mm and post bottom at most "
          f"{D['post_depth_max']:.0f} mm below the seat tube top; clear bore {D['st_depth']:.0f} mm")
r2_ok = (D["saddle_min"] <= 400 and D["saddle_max"] >= 670 and min(D["sleeve_insert_min"], D["post_insert_min"]) >= 100
         and D["sleeve_depth_max"] <= D["st_depth"] and D["post_depth_max"] <= D["st_depth"])
status("R2", f"{D['saddle_min']:.0f} to {D['saddle_max']:.0f} mm; 100 mm insertion at both stages",
       "400 to 670 mm; 100 mm insertion", "Met" if r2_ok else "Not met")
so = D["standover"]
out("A5", f"standover at the stepping point ({P['stand_ahead']:.0f} mm ahead of the loop tube joint): {so:.0f} mm; "
          f"smallest rider inseam {need['small'][0]:.0f} mm, clearance {need['small'][0] - so:.0f} mm")
sad_gnd = {k: saddle_pt(SETTINGS[k]["saddle_h"])[1] for k in ("small", "large")}
out("A6", f"saddle top above ground: {sad_gnd['small']:.0f} mm (smallest setting) to {sad_gnd['large']:.0f} mm (largest)")
out("A7", f"crank / inseam: {P['crank'] / need['small'][0]:.2f} (1.10 m) to {P['crank'] / need['large'][0]:.2f} (1.65 m)")
status("R1", f"1.10 to 1.65 m fitted; standover {so:.0f} mm", "1.10 to 1.65 m; 470 mm or less",
       "Met" if so <= 470 and r2_ok else "Not met")

# ------------------------------------------------------------------ B. reach and bar height (R3)
print("B. Reach and handlebar height")
bar_rise = P["quill_travel"] * sin(radians(P["head_ang"]))
out("B1", f"handlebar height adjustment {bar_rise:.0f} mm ({P['quill_travel']:.0f} mm of quill travel on a "
          f"{P['head_ang']:.0f} deg axis); the grips move back {P['quill_travel'] * cos(radians(P['head_ang'])):.0f} mm as they rise")
reach = {}
for k, sh, se in (("small", need["small"][2], 0.0), ("large", need["large"][2], P["quill_travel"])):
    sx = saddle_pt(sh)[0]
    vals = []
    for ext in P["stem_ext"]:
        gx = grip_pt(se, ext)[0]
        for rail in (-P["saddle_rail"], P["saddle_rail"]):
            vals.append(gx - (sx + rail))
    reach[k] = (min(vals), max(vals))
    out("B2", f"{k} rider setting: reach {min(vals):.0f} to {max(vals):.0f} mm; placeholder need "
              f"{REACH_K * RIDERS[k][0] * 1000:.0f} mm")
span = reach["large"][1] - reach["small"][0]
out("B3", f"reach adjustment over the fit range {span:.0f} mm (smallest to largest setting)")
gz = {k: grip_pt(SETTINGS[k]["stem_exp"], SETTINGS[k]["ext"])[1] for k in ("small", "large")}
out("B4", f"grips {gz['small'] - sad_gnd['small']:+.0f} mm relative to the saddle top at the smallest setting, "
          f"{gz['large'] - sad_gnd['large']:+.0f} mm at the largest")
small_short = reach["small"][0] - REACH_K * 1100
r3_state = "Met" if bar_rise >= 100 and span >= 100 else "Not met"
status("R3", f"bar height {bar_rise:.0f} mm; reach {span:.0f} mm (shortest {reach['small'][0]:.0f} mm)",
       "100 mm or more each", r3_state)

# ------------------------------------------------------------------ C. wheel and steering (R4)
print("C. Wheel size and steering")
circ = pi * P["tire_od"] / 1000
out("C1", f"one wheel size, 20 in (ISO 406); tire outside diameter {P['tire_od']:.0f} mm; rolling circumference {circ:.2f} m")
out("C2", f"trail {D['trail']:.0f} mm with {P['head_ang']:.0f} deg head angle and {P['fork_offset']:.0f} mm offset")
out("C3", f"fork crown to tire {D['crown_clear']:.0f} mm; tire to fender {P['fender_gap']:.0f} mm; "
          f"fender to crown {D['crown_clear'] - P['fender_gap'] - 4:.0f} mm")
fc = P["wheelbase"] - D["bb_x"]
tire_back = fc - (D["R"] + P["fender_gap"] + 4)
for k, (h, _) in RIDERS.items():
    if k == "mid":
        continue
    toe = P["crank"] + 0.35 * 0.155 * h * 1000   # toe beyond the pedal spindle: 35 % of a foot of 0.155 x height
    out("C4", f"{k}: toe reaches {toe:.0f} mm ahead of the BB; fender back edge {tire_back:.0f} mm ahead; "
              f"overlap {max(0.0, toe - tire_back):.0f} mm when the bar is turned")
clear = P["bb_z"] - P["crank"] - 11
lean = degrees(atan(clear / 175))
out("C5", f"pedal clearance {clear:.0f} mm; pedal strike at about {lean:.0f} deg of lean (pedal end 175 mm off center)")
status("R4", "20 in (ISO 406) for all riders", "one size", "Met")

# ------------------------------------------------------------------ D. mass (R5)
print("D. Mass")
tl = tube_lengths()


def tube_kg(od, wall, length_mm):
    a = pi / 4 * (od ** 2 - (od - 2 * wall) ** 2) * 1e-6
    return a * length_mm / 1000 * STEEL_RHO


frame_tubes = {
    "head": tube_kg(P["ht_od"], P["ht_wall"], tl["head"]),
    "seat": tube_kg(P["st_od"], P["st_wall"], tl["seat"]),
    "down": tube_kg(*P["down"], tl["down"]),
    "loop": tube_kg(*P["loop"], tl["loop"]),
    "chainstays": tube_kg(*P["chainstay_tube"], tl["chainstay"]),
    "seat stays": tube_kg(*P["seatstay_tube"], tl["seatstay"]),
    "BB shell": tube_kg(P["bb_shell"][0], P["bb_shell"][1], P["bb_shell"][2]),
}
frame_kg = sum(frame_tubes.values()) + 0.45   # dropouts, collar, bosses, bridges, filler, paint
out("D1", "frame tubes (chromoly head, seat, down and loop tubes; steel stays) " + ", ".join(f"{k} {v:.2f}" for k, v in frame_tubes.items())
    + f" kg; plus 0.45 kg of dropouts, collar, bosses, bridges, filler and paint = {frame_kg:.2f} kg")
sleeve_kg = tube_kg(P["sleeve_od"], P["sleeve_wall"], P["sleeve_len"])
rt_ = P["rack_tube"]
rack_len_tube = 3 * P["rack_len"] + 3 * P["rack_w"] + 2 * 330 + 2 * 300   # rails, cross bars, struts, stays (mm)
rack_kg = tube_kg(rt_, P["rack_wall"], rack_len_tube) * ALU_RHO / STEEL_RHO + 0.10   # plus plates and fixings
post_kg = tube_kg(P["post_od"], P["post_wall"], P["post_len"]) + 0.08
quill_kg = tube_kg(P["quill_d"], P["quill_wall"], D["quill_len"]) + 0.30
MASS = {  # kg; tubes computed, bought parts estimated from typical catalog values
    "1 frame": frame_kg,
    "2 fork (chromoly 1 in steerer, long)": 0.95,
    "3 sleeve and seat post": sleeve_kg + post_kg,
    "4 saddle": 0.45,
    "5 quill stem and head": quill_kg,
    "6 handlebar and grips (alloy bar)": 0.45,
    "7 front wheel (alloy rim)": 0.95,
    "8 rear wheel with coaster hub (alloy rim)": 1.80,
    "9 solid tires (2)": 2.20,
    "10 crankset and pedals": 1.15,
    "11 chain": 0.30,
    "12 front brake, lever, cable": 0.35,
    "13 rack (aluminium)": rack_kg,
    "14 fenders (plastic)": 0.40,
    "15 chainguard": 0.25,
    "16 kickstand": 0.30,
    "17 reflectors and bell": 0.15,
    "18 bottom bracket and headset": 0.45,
    "19 hardware": 0.15,
}
m_bike = sum(MASS.values())
for k, v in MASS.items():
    out("D2", f"{k}: {v:.2f} kg")
out("D3", f"complete bike {m_bike:.1f} kg against 13 kg (R5), over by {m_bike - 13:.1f} kg; "
          f"{m_bike / RIDERS['small'][1] * 100:.0f} % of a 19 kg six-year-old")
# TRL 3 values before GRR-DDR-002 (hi-tensile main tubes, steel rack, steel rear rim and bar), for the before and after table
TRL3_V01 = {"mass": 15.3, "bike_usd": 243, "total_usd": 255}
SAVE = {"pneumatic tires with thorn-resistant tubes and liners (0.85 kg each); reverses D4": 2.20 - 1.70}
for k, v in SAVE.items():
    out("D4", f"saving option: {k}: {v:.2f} kg")
out("D5", f"with the remaining option: {m_bike - sum(SAVE.values()):.1f} kg; before GRR-DDR-002 the bike was "
          f"{TRL3_V01['mass']:.1f} kg, so the adopted changes save {TRL3_V01['mass'] - m_bike:.1f} kg")
status("R5", f"{m_bike:.1f} kg", "13 kg or less", "Not met")

# ------------------------------------------------------------------ E. rider plus bike mass center, rack (R6)
print("E. Mass center and rack")


def mass_center(k, rack_kg=0.0):
    h, m = RIDERS[k]
    set_ = {"small": SETTINGS["small"], "large": SETTINGS["large"]}.get(k)
    if set_ is None:
        set_ = {"saddle_h": need["mid"][2], "stem_exp": 60.0, "ext": 0.0}
    sx, sz = saddle_pt(set_["saddle_h"])
    gx, _ = grip_pt(set_["stem_exp"], set_["ext"])
    rx = (sx + RIDER_CG_FWD * (gx - sx)) / 1000
    rz = sz / 1000 + RIDER_CG_UP * h
    bx, bz = BIKE_CG[0] * L, BIKE_CG[1]
    kx = (P["rack_x0"] + P["rack_len"] / 2) / 1000
    kz = P["rack_z"] / 1000 + 0.10
    mt = m + m_bike + rack_kg
    x = (m * rx + m_bike * bx + rack_kg * kx) / mt
    z = (m * rz + m_bike * bz + rack_kg * kz) / mt
    return mt, x, z


CG = {}
for k in RIDERS:
    CG[k] = mass_center(k)
    mt, x, z = CG[k]
    out("E1", f"{k}: total {mt:.1f} kg, mass center {x * 1000:.0f} mm ahead of the rear axle, {z * 1000:.0f} mm high; "
              f"front wheel carries {x / L * 100:.0f} %")
for k in ("small", "large"):
    mt, x, z = mass_center(k, 10.0)
    out("E2", f"{k} with 10 kg on the rack: front wheel carries {x / L * 100:.0f} %, mass center {z * 1000:.0f} mm high")
rack_w = 10 * g * PEAK_G
rt = P["rack_tube"]
z_rail = pi * (rt ** 4 - (rt - 2 * P["rack_wall"]) ** 4) / (32 * rt)
m_rail = rack_w / 3 * P["rack_len"] / 1000 / 8 * 1000   # N mm, three rails, uniform load, simply supported
out("E3", f"rack platform {P['rack_len']:.0f} x {P['rack_w']:.0f} mm; rail bending at 10 kg x {PEAK_G} g: "
          f"{m_rail / z_rail:.0f} MPa in {rt:.0f} x {P['rack_wall']} mm aluminium tube (welded 6061-T6 {ALU_WELD_YIELD:.0f} MPa); "
          f"rack {rack_kg:.2f} kg")
status("R6", f"{P['rack_len']:.0f} x {P['rack_w']:.0f} mm platform, rail stress {m_rail / z_rail:.0f} MPa at {PEAK_G} g",
       "10 kg rated, marked; 300 x 140 mm or less", "Met")

# ------------------------------------------------------------------ F. braking (R7)
print("F. Braking")
ring_r = P["chain_pitch"] / (2 * sin(pi / P["ring_t"])) / 1000
cog_r = P["chain_pitch"] / (2 * sin(pi / P["cog_t"])) / 1000
crank = P["crank"] / 1000
brake = {}
for k in RIDERS:
    mt, x, z = CG[k]
    h_r, m_r = RIDERS[k]
    res = {}
    for s, mu in MU.items():
        rear = mu * (L - x) / (L + mu * z)
        front = min(mu * x / (L - mu * z) if L > mu * z else 9, (L - x) / z)
        res[s] = (rear, front, min(mu, (L - x) / z))
    pitch = (L - x) / z
    # coaster: back-pedal force for 0.2 g, and decel from the available force
    f_need = mt * 0.2 * g * R_TIRE * ring_r / (COASTER_K * crank * cog_r)
    f_av = BACKPEDAL_K * m_r * g
    a_coast = min(0.2 * f_av / f_need, res["dry"][0])
    # front rim brake: hand force for 0.2 g, and decel from the assumed hand force
    hand = {c: mt * 0.2 * g * R_TIRE / (mu_p * LEVER_MA * R_BRAKE) for c, mu_p in PAD_MU.items()}
    a_front = {c: min(0.2 * HAND_F[k] / hand[c], res["dry"][1]) for c in PAD_MU}
    brake[k] = dict(res=res, pitch=pitch, f_need=f_need, f_av=f_av, a_coast=a_coast, hand=hand, a_front=a_front)
    out("F1", f"{k}: grip limits, dry: rear alone {res['dry'][0]:.2f} g, front alone {res['dry'][1]:.2f} g; "
              f"gravel: rear {res['gravel'][0]:.2f} g, front {res['gravel'][1]:.2f} g; pitch-over at {pitch:.2f} g")
    out("F2", f"{k}: coaster needs {f_need:.0f} N back-pedal force for 0.2 g; rider can give about {f_av:.0f} N "
              f"({BACKPEDAL_K:g} x body weight), so {a_coast:.2f} g")
    out("F3", f"{k}: front lever force for 0.2 g: dry {hand['dry']:.0f} N, wet alloy rim {hand['wet alloy']:.0f} N, "
              f"wet steel rim {hand['wet steel']:.0f} N; with {HAND_F[k]:.0f} N: dry {a_front['dry']:.2f} g, "
              f"wet alloy {a_front['wet alloy']:.2f} g, wet steel {a_front['wet steel']:.2f} g")
    both = min(a_coast + a_front["dry"], MU["dry"], pitch)
    brake[k]["both"] = both
    out("F4", f"{k}: both brakes, dry: {both:.2f} g")
v = 15 / 3.6
for a in (0.2, 0.35):
    out("F5", f"stop from 15 km/h at {a} g: {v ** 2 / (2 * a * g):.1f} m, plus {v * 1.0:.1f} m in 1 s of reaction")
worst_rear = min(b["a_coast"] for b in brake.values())
worst_front = min(b["a_front"]["dry"] for b in brake.values())
worst_both = min(b["both"] for b in brake.values())
r7_state = "Met" if worst_rear >= 0.2 and worst_front >= 0.2 and worst_both >= 0.35 else "Not met"
if r7_state == "Met" and (worst_rear < 0.25 or worst_front < 0.25):
    r7_state = "At risk"
status("R7", f"rear {worst_rear:.2f} g, front {worst_front:.2f} g, both {worst_both:.2f} g (worst rider, dry)",
       "0.2 g each, 0.35 g both, dry", r7_state)

# ------------------------------------------------------------------ G. puncture resistance (R8)
status("R8", "solid or airless tires cannot puncture; life not known", "no punctures; 2,000 km life",
       "Not verifiable at TRL 3")

# ------------------------------------------------------------------ H. service (R9)
print("H. Service and fit change")
tasks = {"loosen seat tube collar, set sleeve, tighten (13 mm)": 1.5,
         "loosen sleeve collar, set post, level saddle, tighten (13 mm)": 2.0,
         "loosen stem expander, set height, align bar, tighten (13 mm)": 2.0,
         "set stem head position (0 or 60 mm) if needed (13 mm)": 1.5,
         "check brake cable slack and lever reach (screwdriver)": 1.5,
         "check insertion marks and positive stops, test ride": 1.5}
t_fit = sum(tasks.values())
out("H1", f"fit change by task analysis: {t_fit:.0f} min (target 10 min or less)")
out("H2", "fit adjustments use 13 mm and a screwdriver; wheels 15 mm; pedals 15 mm; "
          "headset locknut needs a 32 mm spanner and the bottom bracket a lockring spanner")
out("H3", "parent tool list (R9a): 13 mm spanner and screwdriver, met; mechanic tool list (R9b): 13, 15 and 32 mm "
          "spanners, BB lockring spanner, screwdriver, met")
status("R9", f"fit change {t_fit:.0f} min (at the limit); parent and mechanic tool lists met",
       "parent: 13 mm, screwdriver, 10 min; mechanic: 13, 15, 32 mm, lockring", "At risk")

# ------------------------------------------------------------------ I. parts commonality (R10)
status("R10", "chain, hub internals, 1 in headset, 25.4 mm post, 22.2 mm bar, 9/16 in pedals chosen to match",
       "every wear part except tires and rims", "Not verifiable at TRL 3")

# ------------------------------------------------------------------ J. cost (R11)
print("J. Cost")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
helmet = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if "helmet" in r["item"].lower())
bike = tot - helmet
out("J1", f"BOM lines {len(rows)}; bike (lines 1 to 19) ${bike:.0f}; helmet ${helmet:.0f}; total ${tot:.0f} "
          f"against the ${BUDGET:.0f} budget (before GRR-DDR-002: ${TRL3_V01['bike_usd']} and ${TRL3_V01['total_usd']})")
status("R11", f"${bike:.0f} bike, ${tot:.0f} with helmet; production cost not estimated",
       f"${BUDGET:.0f} prototype; $120 at volume", "Not met" if bike > BUDGET else "At risk")

# ------------------------------------------------------------------ K. strength screen (R12)
print("K. Strength screen, largest rider")


def zmod(od, wall):
    di = od - 2 * wall
    return pi * (od ** 4 - di ** 4) / (32 * od)


h_l, m_l = RIDERS["large"]
w_saddle = 0.7 * m_l * g                 # share of rider weight on the saddle, N
sin_s = cos(radians(P["seat_ang"]))       # lever per unit of length along a 70 deg seat axis
sl_e, po_e = split_saddle(SETTINGS["large"]["saddle_h"])
arm_post = (po_e + P["saddle_stack"]) * sin_s + P["saddle_rail"]
arm_st = (sl_e + po_e + P["saddle_stack"]) * sin_s + P["saddle_rail"]
checks = []   # (name, stress at 1 g or at the load case, fatigue screen, yield, peak factor)
for name, arm, od, wall, crmo in (("seat post at the sleeve top", arm_post, P["post_od"], P["post_wall"], False),
                                  ("sleeve at the seat tube top", arm_st, P["sleeve_od"], P["sleeve_wall"], True),
                                  ("seat tube at its clamp", arm_st, P["st_od"], P["st_wall"], True)):
    s1 = w_saddle * arm / zmod(od, wall)
    scr, yl = (CRMO_FATIGUE, CRMO_YIELD) if crmo else (FATIGUE_ALLOW, YIELD)
    checks.append((name, s1, scr, yl, PEAK_G))
    out("K1", f"{name} ({od} x {wall} mm, {'chromoly' if crmo else 'hi-tensile'}): lever {arm:.0f} mm, {s1:.0f} MPa at 1 g, "
              f"{s1 * PEAK_G:.0f} MPa at {PEAK_G} g; screen {scr:.0f} MPa")
# quill at full extension: 300 N up or down at the grips plus 200 N fore-aft pull
qe = SETTINGS["large"]["stem_exp"] + P["stem_rise"] + P["bar_rise"]
m_q = sqrt((300 * abs(P["stem_ext"][1] - P["bar_sweep"])) ** 2 + (200 * qe) ** 2)
s_q = m_q / zmod(P["quill_d"], P["quill_wall"])
checks.append(("quill at the steerer top", s_q, CRMO_FATIGUE, CRMO_YIELD, 1.0))
out("K2", f"quill at the steerer top, full extension (chromoly): {m_q / 1000:.0f} N m, {s_q:.0f} MPa "
          f"(300 N vertical, 200 N pull at the grips); screen {CRMO_FATIGUE:.0f} MPa")
# steerer at the crown under hard front braking, largest rider
mt, x, z = CG["large"]
a = brake["large"]["a_front"]["dry"]
n_f = mt * g * (x / L + a * z / L)
f_b = mt * a * g
cx, cz = D["crown_pt"]
m_st = abs((P["wheelbase"] - cx) / 1000 * n_f - cz / 1000 * f_b) * 1000
s_st = m_st / zmod(25.4, 1.6)
checks.append(("steerer at the crown, braking", s_st, CRMO_FATIGUE, CRMO_YIELD, 1.0))
out("K3", f"steerer at the crown, {a:.2f} g front braking: N {n_f:.0f} N, brake force {f_b:.0f} N, "
          f"{m_st / 1000:.0f} N m, {s_st:.0f} MPa in 25.4 x 1.6 mm chromoly; screen {CRMO_FATIGUE:.0f} MPa; "
          f"a 25.4 x 2.0 mm steerer would give {m_st / zmod(25.4, 2.0):.0f} MPa")
# fork blades at the crown, bump
f_bump = mt * g * x / L * PEAK_G
blade_l = sqrt((P["wheelbase"] - cx) ** 2 + (cz - D["R"]) ** 2)
m_bl = f_bump * cos(radians(P["head_ang"])) * blade_l / 2
s_bl = m_bl / zmod(25.4, 1.2)
out("K4", f"fork blades at the crown, {PEAK_G} g bump: {m_bl / 1000:.0f} N m per blade, {s_bl:.0f} MPa in 25.4 x 1.2 mm "
          f"({s_bl / PEAK_G:.0f} MPa at 1 g)")
checks.append(("fork blade at the crown, 1 g", s_bl / PEAK_G, FATIGUE_ALLOW, YIELD, PEAK_G))
over_f = [n for n, s, scr, yl, pk in checks if s > scr]
over_y = [n for n, s, scr, yl, pk in checks if s * pk > yl]
out("K5", f"above the fatigue screen for their material: {', '.join(over_f) or 'none'}; "
          f"above yield at peak: {', '.join(over_y) or 'none'}")
status("R12", f"{len(over_f)} of {len(checks)} sections above the fatigue screen ({', '.join(over_f) or 'none'}); "
       f"joint seizing not assessable",
       "10 years, 3 riders, 60 kg + 10 kg", "At risk")

# ------------------------------------------------------------------ L. drive, power and trip time
print("L. Drive, power and trip time")
dev = circ * P["ring_t"] / P["cog_t"]
out("L1", f"gear {P['ring_t']}/{P['cog_t']}: {dev:.2f} m per crank turn; 11 km/h at {11000 / 60 / dev:.0f} rpm")
chain_links = 2 * P["chainstay"] / P["chain_pitch"] + (P["ring_t"] + P["cog_t"]) / 2 + \
    ((P["ring_t"] - P["cog_t"]) / (2 * pi)) ** 2 * P["chain_pitch"] / P["chainstay"]
out("L2", f"chain length {chain_links:.1f} pitches, so {2 * int(chain_links / 2 + 1)} links")
CRR, CDA, RHO = 0.02, 0.35, 1.2
for k in ("small", "mid", "large"):
    mt = CG[k][0]
    v1, v2 = 11 / 3.6, 7 / 3.6
    p1 = (CRR * mt * g + 0.5 * RHO * CDA * v1 ** 2) * v1
    p2 = ((CRR + 0.05) * mt * g + 0.5 * RHO * CDA * v2 ** 2) * v2
    rpm2 = 7000 / 60 / dev
    f_ped = p2 / (rpm2 * 2 * pi / 60 * crank)
    out("L3", f"{k}: {p1:.0f} W at 11 km/h on the level; {p2:.0f} W on a 5 % climb at 7 km/h "
              f"({rpm2:.0f} rpm, mean pedal force {f_ped:.0f} N, {f_ped / (RIDERS[k][1] * g) * 100:.0f} % of body weight)")
for mode, v_lo, v_hi in (("walking", 4, 5), ("cycling", 10, 12)):
    out("L4", f"{mode} 5 km: {5 / v_hi * 60:.0f} to {5 / v_lo * 60:.0f} min one way")
saved = (5 / 4.5 - 5 / 11) * 2 * 60
out("L5", f"time returned at the midpoints (4.5 and 11 km/h): {saved:.0f} min per day, {saved * 190 / 60:.0f} h per 190-day year")

# ------------------------------------------------------------------ M. standards classification
print("M. Standard")
out("M1", f"maximum saddle height above ground {sad_gnd['large']:.0f} mm: ISO 8098 covers under 635 mm, "
          f"ISO 4210-2 young adult 635 to 750 mm, city and trekking 635 mm or more; smallest setting {sad_gnd['small']:.0f} mm")

# ------------------------------------------------------------------ results
print("RESULTS")
order = {"Not met": 0, "At risk": 1, "Not verifiable at TRL 3": 2, "Met": 3}
for req in sorted(STATUS, key=lambda r: (order[STATUS[r][2]], int(r[1:]))):
    v_, t_, s_ = STATUS[req]
    print(f"[R] {req} | {s_} | {v_} | target {t_}")
counts = {s: sum(1 for v in STATUS.values() if v[2] == s) for s in order}
print("[R] counts " + ", ".join(f"{k}: {v}" for k, v in counts.items()))
