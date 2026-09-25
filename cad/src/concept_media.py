"""GrowRider concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the bike (rear axle at x = 0, front toward +X), Z up, Y lateral.
The drive side (chain) is at -Y, facing the camera in the hero view.
Seat post and stem are shown extended toward the upper end of their range.
"""
import sys
from math import cos, sin, radians, pi
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Plane, Solid, Vector
from concept import Part, render_all, human_figure

# Main parameters (mm), proposed baseline: 20 in wheels (ISO 406), step-through frame
TIRE_OD = 500.0            # 20 x 1.95 in tire outside diameter, about 500 mm
R_WHEEL = TIRE_OD / 2      # axle height above ground
TIRE_R = 24.0              # tire section radius
RIM_R = 203.0              # ISO 406 bead seat radius
WHEELBASE = 860.0
CHAINSTAY = 380.0
BB_Z = 260.0               # bottom bracket height
SEAT_ANG = HEAD_ANG = 70.0
CRANK = 140.0
SADDLE_H_SHOWN = 600.0     # BB center to saddle top along the seat axis (range 436 to 654)

REAR = Vector(0, 0, R_WHEEL)
FRONT = Vector(WHEELBASE, 0, R_WHEEL)
BB = Vector(CHAINSTAY, 0, BB_Z)
seat_dir = Vector(-cos(radians(SEAT_ANG)), 0, sin(radians(SEAT_ANG)))
steer_dir = Vector(-cos(radians(HEAD_ANG)), 0, sin(radians(HEAD_ANG)))
steer0 = Vector(WHEELBASE - 32.0, 0, R_WHEEL)   # steering axis at axle height (30 mm rake)


def steer(t):
    return steer0 + steer_dir * t


def seat(t):
    return BB + seat_dir * t


def tube(p1, p2, r):
    """Round tube between two points."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    return Solid.make_cylinder(r, d.length, Plane(origin=p1, z_dir=d.normalized()))


def ring_y(center, r_out, r_in, width, y=0.0):
    """Annulus in the XZ plane (axis along Y) centered at center."""
    pl = Plane(origin=(center.X, y - width / 2, center.Z), z_dir=(0, 1, 0))
    return Solid.make_cylinder(r_out, width, pl) - Solid.make_cylinder(r_in, width, pl)


def disc_y(center, r, width, y=0.0):
    return Solid.make_cylinder(r, width, Plane(origin=(center.X, y - width / 2, center.Z), z_dir=(0, 1, 0)))


def union(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out + s
    return out


# 1 Frame: step-through with twin down tubes, outer seat tube and head tube sleeves for telescoping parts
HT_LO, HT_HI = 285.0, 405.0
head_tube = tube(steer(HT_LO), steer(HT_HI), 19)
seat_tube = tube(BB, seat(300), 17)
down_tube = tube(steer(HT_LO + 15), BB, 17)
loop_tube = tube(steer(HT_HI - 25), seat(120), 14)
bb_shell = disc_y(BB, 20, 70)
chainstays = union([tube(BB + Vector(0, s * 25, 0), REAR + Vector(0, s * 55, 0), 9) for s in (-1, 1)])
seatstays = union([tube(seat(280) + Vector(0, s * 18, 0), REAR + Vector(0, s * 55, 0), 8) for s in (-1, 1)])
frame = union([head_tube, seat_tube, down_tube, loop_tube, bb_shell, chainstays, seatstays])

# 2 Fork: crown, two blades to the front axle
crown_pt = steer(HT_LO - 10)
crown = Pos(crown_pt.X, 0, crown_pt.Z) * Box(40, 110, 22)
blades = union([tube(crown_pt + Vector(0, s * 45, 0), FRONT + Vector(0, s * 50, 0), 10) for s in (-1, 1)])
steerer = tube(steer(HT_LO - 10), steer(HT_HI + 10), 12)
fork = crown + blades + steerer

# 3 Telescoping seat post (inner tube plus post), shown extended
saddle_pt = seat(SADDLE_H_SHOWN)
seat_post = tube(seat(260), seat(SADDLE_H_SHOWN - 35), 13.5)

# 4 Saddle
saddle = Pos(saddle_pt.X + 15, 0, saddle_pt.Z - 12) * Box(220, 125, 40)

# 5 Telescoping stem: quill rises inside the head tube, then a short forward extension
stem_top = steer(HT_HI + 115)
stem_quill = tube(steer(HT_HI - 60), stem_top, 11)
stem_ext = tube(stem_top, stem_top + Vector(55, 0, 10), 11)
stem = stem_quill + stem_ext
clamp = stem_top + Vector(55, 0, 10)

# 6 Handlebar with grips: swept-back roadster-style bar, 520 mm wide
bar_c = tube(clamp + Vector(0, -120, 0), clamp + Vector(0, 120, 0), 11)
bar_l = tube(clamp + Vector(0, 120, 0), clamp + Vector(-70, 260, 25), 11)
bar_r = tube(clamp + Vector(0, -120, 0), clamp + Vector(-70, -260, 25), 11)
grips = union([tube(clamp + Vector(-70, s * 260, 25), clamp + Vector(-85, s * 380, 30), 16) for s in (-1, 1)])
handlebar = union([bar_c, bar_l, bar_r, grips])


def wheel(center, hub_r, hub_w):
    rim = ring_y(center, RIM_R + 6, RIM_R - 14, 26)
    hub = disc_y(center, hub_r, hub_w)
    axle = disc_y(center, 6, 140)
    spokes = []
    for i in range(18):
        a = 2 * pi * i / 18
        side = 1 if i % 2 else -1
        p_hub = center + Vector(hub_r * cos(a), side * hub_w / 2 * 0.8, hub_r * sin(a))
        p_rim = center + Vector((RIM_R - 14) * cos(a + 0.35), 0, (RIM_R - 14) * sin(a + 0.35))
        spokes.append(tube(p_hub, p_rim, 1.6))
    return union([rim, hub, axle] + spokes)


# 7 Front wheel, 8 rear wheel with coaster brake hub and reaction arm
front_wheel = wheel(FRONT, 22, 80)
coaster_arm = tube(REAR + Vector(0, 50, 0), REAR + Vector(140, 50, 5), 6)
rear_wheel = wheel(REAR, 32, 110) + coaster_arm

# 9 Puncture-proof tires (solid or airless), 20 x 1.95 in
tires = union([Solid.make_torus(R_WHEEL - TIRE_R, TIRE_R, Plane(origin=(c.X, 0, c.Z), z_dir=(0, 1, 0)))
               for c in (REAR, FRONT)])

# 10 Crankset: 32T chainring on the drive side (-Y), 140 mm cranks, pedals
Y_CHAIN = -48.0
RING_R, COG_R = 65.0, 36.5          # 32T and 18T pitch radii, 1/2 in pitch
chainring = ring_y(BB, RING_R + 4, RING_R - 18, 4, y=Y_CHAIN)
crank_a = 20.0                      # crank angle shown
ca = Vector(CRANK * cos(radians(crank_a)), 0, CRANK * sin(radians(crank_a)))
crank_r = tube(BB + Vector(0, Y_CHAIN - 8, 0), BB + ca + Vector(0, Y_CHAIN - 8, 0), 8)
crank_l = tube(BB + Vector(0, 58, 0), BB - ca + Vector(0, 58, 0), 8)
spindle = disc_y(BB, 8, 130)
pedals = union([Pos(p.X, p.Y, p.Z) * Box(80, 90, 22) for p in
                (BB + ca + Vector(0, Y_CHAIN - 60, 0), BB - ca + Vector(0, 110, 0))])
crankset = union([chainring, crank_r, crank_l, spindle, pedals])

# 11 Chain: upper and lower runs from chainring to the coaster hub sprocket, plus the sprocket
cog = ring_y(REAR, COG_R + 3, 18, 4, y=Y_CHAIN)
chain = union([tube(BB + Vector(0, Y_CHAIN, s * RING_R), REAR + Vector(0, Y_CHAIN, s * COG_R), 4) for s in (-1, 1)]) + cog

# 12 Front rim brake: caliper at the fork crown, lever on the right grip
caliper = Pos(crown_pt.X + 8, 0, crown_pt.Z - 30) * Box(30, 90, 50)
lever = tube(clamp + Vector(-40, -250, 20), clamp + Vector(10, -330, 5), 5)
front_brake = caliper + lever

# 13 Rear rack, rated 10 kg: platform over the rear wheel, struts to the axle and seat stays
RACK_Z = 575.0
rails = union([tube((-90, s * 60, RACK_Z), (220, s * 60, RACK_Z), 6) for s in (-1, 0, 1)])
cross = union([tube((x, -60, RACK_Z), (x, 60, RACK_Z), 5) for x in (-90, 60, 220)])
struts = union([tube((-85, s * 60, RACK_Z), (0, s * 62, R_WHEEL + 10), 6) for s in (-1, 1)])
stays = union([tube((215, s * 60, RACK_Z), (220, s * 20, 462), 5) for s in (-1, 1)])
rack = union([rails, cross, struts, stays])

# 14 Fenders: arcs over both wheels
def fender(center, keep_box):
    arc = ring_y(center, R_WHEEL + 20, R_WHEEL + 16, 64)
    return arc & keep_box

rear_fender = fender(REAR, Pos(-40, 0, R_WHEEL + 250) * Box(700, 200, 500))
front_fender = fender(FRONT, Pos(WHEELBASE + 20, 0, R_WHEEL + 250) * Box(620, 200, 500))
fenders = rear_fender + front_fender

# 15 Chainguard: flat plate over the upper chain run on the drive side
cg_mid = (BB + REAR) * 0.5
chainguard = Pos(cg_mid.X + 30, Y_CHAIN - 16, cg_mid.Z + 50) * Box(440, 3, 45)

# 16 Kickstand: rear-mounted, shown down
kick_top = Vector(120, 20, 258)
kickstand = tube(kick_top, Vector(190, 110, 8), 7)

# 17 Reflectors and bell: rear reflector on the rack, front reflector on the bar, spoke and pedal reflectors
rear_ref = Pos(-100, 0, RACK_Z - 40) * Box(8, 70, 40)
front_ref = Pos(clamp.X + 22, 0, clamp.Z - 20) * Box(8, 60, 35)
bell = Pos(clamp.X - 20, 100, clamp.Z + 18) * Cylinder(22, 16)
spoke_refl = union([Pos(c.X + 120, 0, c.Z + 60) * Box(50, 10, 20) for c in (REAR, FRONT)])
reflectors = union([rear_ref, front_ref, bell, spoke_refl])

STEEL = "#2E5E8C"
parts = [
    Part("Step-through steel frame", frame, STEEL, 1),
    Part("Fork", fork, STEEL, 2, (260, 0, 0)),
    Part("Telescoping seat post (extended)", seat_post, "#9CA3AF", 3, (-80, -220, 240)),
    Part("Saddle", saddle, "#1F2937", 4, (-40, 0, 640)),
    Part("Telescoping stem", stem, "#9CA3AF", 5, (150, 0, 260)),
    Part("Handlebar and grips", handlebar, "#4B5563", 6, (250, 0, 450)),
    Part("Front wheel, 20 in", front_wheel, "#B8BEC6", 7, (560, 0, 0)),
    Part("Rear wheel, coaster brake hub", rear_wheel, "#B8BEC6", 8, (-560, 0, -520)),
    Part("Puncture-proof tires (2)", tires, "#262626", 9, (0, 0, -420)),
    Part("Crankset, 32T, 140 mm", crankset, "#6B7280", 10, (0, -260, -300)),
    Part("Chain and 18T sprocket", chain, "#C2410C", 11, (0, -420, -150)),
    Part("Front rim brake and lever", front_brake, "#D4A017", 12, (400, 0, 180)),
    Part("Rear rack, 10 kg rated", rack, "#0F766E", 13, (160, 0, 400)),
    Part("Fenders", fenders, "#374151", 14, (320, 0, 800)),
    Part("Chainguard", chainguard, "#94A3B8", 15, (0, -300, 120)),
    Part("Kickstand", kickstand, "#6B7280", 16, (0, 220, -220)),
    Part("Reflectors and bell", reflectors, "#DC2626", 17, (260, 0, 980)),
]

# Child for scale: 1.35 m (about a 10 year old), standing beside the front wheel
child = human_figure(height=1350, x=WHEELBASE + R_WHEEL + 450, y=0, z=0)
child.name = "Child, 1.35 m"
context = [child]

if __name__ == "__main__":
    render_all(
        parts, project="GrowRider", title="Adjustable child bicycle concept", dwg_no="GRR-DWG-010",
        key_figures=["Rider height 1.10 to 1.65 m (ages about 6 to 14)",
                     "Saddle height 436 to 654 mm from BB (estimate)",
                     "20 in wheels, 860 mm wheelbase (proposed)",
                     "Coaster brake plus front rim brake (proposed)",
                     "Rack rated 10 kg; about 15 kg bike (estimate)",
                     "5 km school trip: about 27 min vs 67 min walking"],
        scale_figure=False, context=context, cut=False,
        flow={"title": "growth and hand-down cycle (estimates)", "unit": "",
              "stages": [("Age 6, 1.10 m", "saddle 436 mm"), ("Age 10, 1.38 m", "saddle 546 mm"),
                         ("Age 14, 1.65 m", "saddle 654 mm"), ("Reset for sibling", "2 spanners, 10 min"),
                         ("Next sibling", "10 year life (target)")]},
    )
