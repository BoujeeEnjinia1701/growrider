"""GrowRider product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a painted step-through frame with dropouts, bosses
and a head badge; the two-stage telescoping seat post and long quill stem with clamp collars,
13 mm bolts and painted height scales; a shaped saddle on rails; alloy rims with laced spokes and
treaded solid tires; hubs, axle nuts and the coaster brake arm; a toothed chainring and sprocket
with a linked chain; shaped cranks and platform pedals with reflectors; a side-pull front brake
with pads, lever and cable; the aluminium rack with its 10 kg marking; fenders with stays and
mud flaps; chainguard with the name; kickstand, reflectors and bell. A clay mannequin of a
1.30 m child rides it for scale. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail.
CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and the point helpers in model.py.
Axes as model.py: X along the bike (rear axle at x = 0, front toward +X), Z up with the ground at
z = 0, Y lateral, drive side (chain) at -Y.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import asin, atan2, cos, degrees, pi, radians, sin, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Location, Plane, Polyline, Pos,
                       RectangleRounded, RegularPolygon, Rot, SlotOverall, Solid, Sphere, Text,
                       Vector, extrude, fillet, make_face, revolve, Spline, sweep, Circle)
from model import PARAMS, derived, seat_pt, steer_pt, split_saddle

TITLE = "GrowRider: adjustable children's bicycle that grows from age 6 to 14"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation), drive side toward "
             "the viewer; a 1.30 m child (clay figure) rides the bike set for their height"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): frame, fork, "
             "telescoping seat post and quill stem, saddle, bar, wheels and solid tires, drivetrain, "
             "front brake, rack, fenders and chainguard"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -62,
     "note": "Bike alone from the front right, slightly above (about 14 deg elevation): the adjustable "
             "frame, with the two-stage seat post and quill stem and their painted height scales"},
]

# Rider setting shown in the renders: a 1.30 m child (about age 8). Saddle 505 mm from the BB
# (between fit rules A and B of GRR-CAL-001), stem raised 45 mm, short stem head position.
SETTING = {"saddle_h": 505.0, "stem_exp": 45.0, "ext": 0.0}
RIDER_H = 1300.0
CRANK_ANG = 20.0            # drive-side crank angle above horizontal, forward (as model.py)

# Colours (restrained product palette; kit accent for the frame)
C_FRAME = "#0F766E"
C_GRAPHITE = "#2F3640"      # sleeve, stem head (the sliding parts)
C_COLLAR = "#1F2328"
C_SCALE = "#F2F2EE"
C_CHROME = "#C7CCD2"
C_ALLOY = "#B8BEC6"
C_RACK = "#C5CAD0"
C_STEEL = "#8A9099"
C_DARK_STEEL = "#4A4F57"
C_TIRE = "#1E1F22"
C_RUBBER = "#26282C"
C_SADDLE = "#D9D2C3"
C_SADDLE_BASE = "#2A2D32"
C_FENDER = "#3A3F47"
C_GUARD = "#D5D9DE"
C_RED = "#C0262D"
C_AMBER = "#E08A1E"
C_WHITE_REFL = "#EEF0F2"
C_CLAY = "#9CA3AF"

FONT = str(Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")


# ------------------------------------------------------------------ helpers

def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _v(p):
    return Vector(*p)


def _tube(p1, p2, r):
    p1, p2 = _v(p1), _v(p2)
    v = p2 - p1
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v.normalized()))


def _rtube(p1, p2, r):
    """Tube with rounded (spherical) ends."""
    return _tube(p1, p2, r) + Pos(*p1) * Sphere(r) + Pos(*p2) * Sphere(r)


def _xz(p, y=0.0):
    return (p[0], y, p[1])


def _cyl_y(c, r, w, y=0.0):
    """Cylinder with its axis along Y, centred on (c[0], y, c[1])."""
    return Solid.make_cylinder(r, w, Plane(origin=(c[0], y - w / 2, c[1]), z_dir=(0, 1, 0)))


def _ring_y(c, ro, ri, w, y=0.0):
    return _cyl_y(c, ro, w, y) - _cyl_y(c, ri, w + 2, y)


def _loc(origin, z_dir, x_dir=None):
    """Location whose local Z is z_dir at origin (x_dir optional, projected)."""
    z = _v(z_dir).normalized()
    if x_dir is None:
        x_dir = (0, 1, 0) if abs(z.Y) < 0.9 else (1, 0, 0)
    x = _v(x_dir)
    x = (x - z * x.dot(z)).normalized()
    return Location(Plane(origin=_v(origin), x_dir=x, z_dir=z))


def _hex_nut(af, h):
    """Hex nut or bolt head, across flats af, height h, local Z from 0 to h, chamfered look."""
    n = extrude(RegularPolygon(af / sqrt(3), 6), amount=h)
    return _fillet_try(n, n.edges().filter_by(Axis.Z, reverse=True), [h * 0.18, h * 0.1])


def _hull_pts(circles, n=72):
    """Convex hull (x, z) of sampled circles [(cx, cz, r)], counter-clockwise."""
    from scipy.spatial import ConvexHull
    pts = [(cx + r * cos(2 * pi * k / n), cz + r * sin(2 * pi * k / n)) for cx, cz, r in circles for k in range(n)]
    h = ConvexHull(pts)
    return [pts[i] for i in h.vertices]


def _plate_xz(pts, y0, t):
    """Planar outline in XZ (list of (x, z)) extruded from y0 by t along +Y."""
    pl = Plane(origin=(0, y0, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))     # local y is world -Z
    face = make_face(Polyline(*[(x, -z) for x, z in pts], close=True))
    return pl.location * extrude(face, amount=t)


def _gear_y(c, r_pitch, teeth, w, y, bore):
    """Toothed sprocket in the XZ plane: disc with roller seats cut at the pitch circle."""
    g = _cyl_y(c, r_pitch + 3.6, w, y)
    cutters = [_cyl_y((c[0] + r_pitch * cos(2 * pi * k / teeth), c[1] + r_pitch * sin(2 * pi * k / teeth)), 4.1, w + 2, y)
               for k in range(teeth)]
    g -= Compound(children=cutters)
    g -= _cyl_y(c, bore, w + 2, y)
    return g


def _text_plate(txt, size, depth):
    """Raised text, lying in local XY, height along +Z, centred on the origin."""
    t = Text(txt, size, font_path=FONT)
    return extrude(t, amount=depth)


# ------------------------------------------------------------------ rider fit

def _rider(P, D, saddle_top, grips, pedals):
    """Clay mannequin (1.30 m, "ride") with its seat on the saddle, hands on the grips, feet on the pedals.

    The joint angles are fitted to the landmarks of context_parts.mannequin_landmarks; the figure faces
    -Y in its own frame and is turned 90 deg so it faces +X (forward) here.
    """
    from context_parts import mannequin, mannequin_landmarks
    PITCH = {"l": -18.0, "r": 0.0}      # foot pitch: rear (left) pedal toes down, front pedal level

    def joints(v):
        j = dict(torso_lean=v[0], shoulder_flex_l=v[1], shoulder_flex_r=v[1], elbow_flex_l=v[2],
                 elbow_flex_r=v[2], shoulder_abd_l=v[3], shoulder_abd_r=v[3], hip_flex_l=v[4],
                 knee_flex_l=v[5], hip_flex_r=v[6], knee_flex_r=v[7], head_tilt=-0.7 * v[0])
        for s in "lr":
            j[f"ankle_flex_{s}"] = PITCH[s] - (j[f"hip_flex_{s}"] - j[f"knee_flex_{s}"])
        return j

    def world(p, off):
        return (-p[1] + off[0], p[0] + off[1], p[2] + off[2])

    def offset(lm):
        s = lm["seat"]
        return (saddle_top[0] + s[1], -s[0], saddle_top[2] - s[2])

    def cost(v):
        lm = mannequin_landmarks(RIDER_H, "ride", **joints(v))
        off = offset(lm)
        e = 0.0
        for i, side in ((0, 1), (1, -1)):
            h, f = world(lm["hands"][i], off), world(lm["feet"][i], off)
            g, pd = grips[side], pedals[side]
            e += (h[0] - g[0]) ** 2 + (h[2] - g[2]) ** 2 + 0.3 * (h[1] - g[1]) ** 2
            e += (f[0] - pd[0]) ** 2 + (f[2] - pd[2]) ** 2
        return e

    v = [15.2, 1.2, 74.6, 15.1, 41.4, 83.2, 39.7, 44.3]      # fitted values for SETTING (fallback)
    try:
        from scipy.optimize import minimize
        r = minimize(cost, v, method="Powell", options=dict(maxiter=6000, xtol=1e-2, ftol=1e-3))
        if r.fun < cost(v):
            v = list(r.x)
    except Exception:
        pass
    j = joints(v)
    off = offset(mannequin_landmarks(RIDER_H, "ride", **j))
    return Pos(*off) * Rot(0, 0, 90) * mannequin(RIDER_H, "ride", **j)


# ------------------------------------------------------------------ parts

def product_parts(P=PARAMS):
    D = derived(P)
    S = SETTING
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    R = D["R"]
    WB = P["wheelbase"]
    rear, front = (0.0, R), (WB, R)
    bb = (D["bb_x"], P["bb_z"])
    st = lambda s: seat_pt(s, P)
    sr = lambda t: steer_pt(t, P)
    seat_dir = (D["seat_dir"][0], 0.0, D["seat_dir"][1])
    steer_dir = (D["steer_dir"][0], 0.0, D["steer_dir"][1])
    ax_seat = lambda s, y=0.0: _xz(st(s), y)
    ax_steer = lambda t, y=0.0: _xz(sr(t), y)
    ex_seat = lambda k: (seat_dir[0] * k, 0.0, seat_dir[2] * k)       # explode along the seat axis
    ex_steer = lambda k: (steer_dir[0] * k, 0.0, steer_dir[2] * k)

    # ================================================================ 1 frame
    ht = _tube(ax_steer(P["ht_bot"]), ax_steer(D["ht_top"]), P["ht_od"] / 2)
    seat_tube = _tube(_xz(bb), ax_seat(P["st_len"]), P["st_od"] / 2)
    down = _tube(ax_steer(P["down_t"]), _xz(bb), P["down"][0] / 2)
    loop = _tube(ax_steer(P["loop_t"]), ax_seat(P["loop_s"]), P["loop"][0] / 2)
    od, _, w = P["bb_shell"]
    shell = _cyl_y(bb, od / 2, w)
    cs = [_tube((bb[0], s * 25, bb[1]), (0, s * 55, R), P["chainstay_tube"][0] / 2) for s in (-1, 1)]
    sst = st(P["ss_s"])
    ss = [_tube((sst[0], s * 18, sst[1]), (0, s * 55, R), P["seatstay_tube"][0] / 2) for s in (-1, 1)]
    # seat stay caps where they meet the seat tube
    ss_caps = [Pos(sst[0], s * 18, sst[1]) * Sphere(P["seatstay_tube"][0] / 2) for s in (-1, 1)]
    # rear dropouts: rounded plates with a rear-facing axle slot
    drops = []
    for s in (-1, 1):
        prof = extrude(Plane.XZ * RectangleRounded(46, 40, 11), amount=2.5, both=True)
        slot = extrude(Plane.XZ * Pos(-14, 0) * SlotOverall(38, 10.5), amount=4, both=True)
        drops.append(Pos(-4, s * 55, R) * (prof - slot))
    # kickstand plate between the chainstays, rack bosses on the seat stays
    ks_z = 250.0 + (P["bb_z"] - 250.0) * 120.0 / bb[0]
    ks_plate = Pos(120, 0, ks_z) * Box(42, 96, 5)
    ks_plate = _fillet_try(ks_plate, ks_plate.edges().filter_by(Axis.Z), [8, 4])
    frame = ht + seat_tube + down + loop + shell
    for s in cs + ss + ss_caps + drops:
        frame += s
    frame += ks_plate
    add("Step-through chromoly frame", frame, C_FRAME, "painted", 1, "shell", (0, 0, 0))

    # head badge: a curved shield on the front of the head tube
    hb_c = sr(P["ht_bot"] + P["ht_len"] * 0.55)
    loc_ht = _loc(_xz(hb_c), steer_dir, x_dir=(1, 0, 0))
    r_ht = P["ht_od"] / 2
    badge = Cylinder(r_ht + 0.8, 62) - Cylinder(r_ht - 0.2, 64)
    badge &= Pos(r_ht, 0, 0) * Box(2 * r_ht, 26, 62)
    badge = _fillet_try(badge, badge.edges().filter_by(Axis.Z, reverse=True), [4.0, 2.0])
    add("Head badge", loc_ht * badge, C_ALLOY, "metal", 1, "shell", (60, 0, 0))

    # ================================================================ 18 bottom bracket and headset
    bbc = _ring_y(bb, 21.5, 9.5, 5, y=w / 2 + 2.5) + _ring_y(bb, 21.5, 9.5, 5, y=-w / 2 - 2.5)
    bbc = _fillet_try(bbc, bbc.edges(), [0.8, 0.4])
    add("Bottom bracket cups", bbc, C_STEEL, "metal", 18, "shell", (0, -150, -120))
    spindle = _cyl_y(bb, 8, 130)
    add("Bottom bracket spindle", spindle, C_STEEL, "metal", 18, "internal", (0, -150, -120))
    cup_lo = _tube(ax_steer(P["ht_bot"] - 11), ax_steer(P["ht_bot"]), 18.5)
    cup_hi = _tube(ax_steer(D["ht_top"]), ax_steer(D["ht_top"] + 11), 18.5)
    washer = _tube(ax_steer(D["ht_top"] + 11), ax_steer(D["ht_top"] + 16), 16.0)
    nut = _loc(ax_steer(D["ht_top"] + 16), steer_dir) * _hex_nut(32, D["steerer_top"] - D["ht_top"] - 16)
    headset = _fillet_try(cup_lo, cup_lo.edges(), [1.0, 0.5]) + _fillet_try(cup_hi, cup_hi.edges(), [1.0, 0.5])
    headset = headset + washer + nut
    add("Headset cups and 32 mm locknut", headset, C_STEEL, "metal", 18, "shell", (-40, 0, 110))

    # ================================================================ 2 fork
    c = sr(P["crown_t"] - 11)
    crown = Box(110, 40, 22)      # local: x lateral, y along the bike, z along the steering axis
    crown = _fillet_try(crown, crown.edges().filter_by(Axis.Z), [12, 8, 4])
    crown = _fillet_try(crown, crown.faces().sort_by(Axis.Z)[-1].edges(), [4, 2])
    crown = _loc(_xz(c), steer_dir, x_dir=(0, 1, 0)) * crown
    blades = [_rtube((c[0], s * 45, c[1]), (front[0], s * 50, R + 6), 10) for s in (-1, 1)]
    ftips = []
    for s in (-1, 1):
        tip = extrude(Plane.XZ * SlotOverall(34, 18), amount=2.5, both=True)
        ftips.append(Pos(front[0], s * 50, R + 6) * Rot(0, -70, 0) * tip)
    steerer = _tube(ax_steer(P["crown_t"]), ax_steer(D["steerer_top"]), 12.7)
    fork = crown + steerer
    for b in blades + ftips:
        fork += b
    add("Fork, 1 in steerer", fork, C_FRAME, "painted", 2, "shell", (230, 0, -40))

    # ================================================================ 3 telescoping seat post
    sl_exp, po_exp = split_saddle(S["saddle_h"], P)
    sleeve_top = P["st_len"] + sl_exp
    post_top = sleeve_top + po_exp
    sleeve = _tube(ax_seat(sleeve_top - P["sleeve_len"]), ax_seat(sleeve_top), P["sleeve_od"] / 2)
    add("Seat post sleeve, 29.2 mm chromoly", sleeve, C_GRAPHITE, "painted", 3, "shell", ex_seat(150))
    post = _tube(ax_seat(post_top - P["post_len"]), ax_seat(post_top), P["post_od"] / 2)
    add("Seat post, 25.4 mm", post, C_CHROME, "metal", 3, "shell", ex_seat(300))
    # painted height scale on the exposed sleeve (every 20 mm, a longer band every 60 mm)
    rings = []
    k = 0
    s_ = P["st_len"] + 20.0
    while s_ < sleeve_top - 18:
        wd = 2.2 if k % 3 == 2 else 1.1
        rings.append(_tube(ax_seat(s_ - wd / 2), ax_seat(s_ + wd / 2), P["sleeve_od"] / 2 + 0.25))
        s_ += 20.0
        k += 1
    if rings:
        add("Sleeve height scale (painted)", Compound(children=rings), C_SCALE, "painted", 3, "shell", ex_seat(150))

    def collar(s_top, r_in, r_out, h=13.0):
        """Split clamp collar on an axis tube: ring, rear lug and a 13 mm hex bolt (local Z = seat axis)."""
        ring = Pos(0, 0, -h / 2) * (Cylinder(r_out, h) - Cylinder(r_in, h + 2))
        lug = Pos(-(r_out + 4), 0, -h / 2) * Box(12, 16, h)
        body = ring + lug
        body -= Pos(-(r_out + 6), 0, -h / 2) * Box(20, 2.2, h + 2)      # clamp slot
        body -= Pos(-(r_out + 5), 0, -h / 2) * Rot(90, 0, 0) * Cylinder(4.2, 30)
        body = _fillet_try(body, body.edges().filter_by(Axis.Z), [1.2, 0.6])
        bolt = Pos(-(r_out + 5), -8.0, -h / 2) * Rot(90, 0, 0) * _hex_nut(13, 5.5)
        bolt += Pos(-(r_out + 5), 0, -h / 2) * Rot(90, 0, 0) * Cylinder(4.0, 22)
        nut = Pos(-(r_out + 5), 8.0, -h / 2) * Rot(-90, 0, 0) * _hex_nut(13, 6.5)
        return body, bolt + nut

    loc_st = _loc(ax_seat(P["st_len"]), seat_dir, x_dir=(1, 0, 0))
    b1, h1 = collar(0, P["sleeve_od"] / 2 + 0.2, P["st_od"] / 2 + 3.2)
    add("Seat tube clamp collar", loc_st * b1, C_COLLAR, "metal", 1, "shell", ex_seat(60))
    loc_sl = _loc(ax_seat(sleeve_top), seat_dir, x_dir=(1, 0, 0))
    b2, h2 = collar(0, P["post_od"] / 2 + 0.2, P["sleeve_od"] / 2 + 3.2)
    add("Sleeve clamp collar", loc_sl * b2, C_COLLAR, "metal", 3, "shell", ex_seat(210))
    add("Clamp bolts, 13 mm (seat)", Compound(children=[loc_st * h1, loc_sl * h2]), C_STEEL, "metal", 19, "shell",
        ex_seat(135))

    # ================================================================ 4 saddle
    sp = st(post_top + P["saddle_stack"])
    top_z = sp[1]
    scx = sp[0] + 15.0
    half = [(-110, 50), (-104, 60), (-92, 63), (-70, 62), (-40, 55), (-5, 38), (40, 26), (85, 22), (104, 20), (110, 14)]
    plan = [(x, y) for x, y in half] + [(110, 0)] + [(x, -y) for x, y in reversed(half)] + [(-112, 0)]
    try:
        wire = Spline(*[(scx + x, y, 0) for x, y in plan], periodic=True)
        cover = extrude(make_face(wire), amount=36)
    except Exception:
        cover = extrude(make_face(Polyline(*[(scx + x, y, 0) for x, y in plan], close=True)), amount=36)
    cover = Pos(0, 0, top_z - 36) * cover
    cover = _fillet_try(cover, cover.faces().sort_by(Axis.Z)[-1].edges(), [14, 10, 6, 3])
    add("Saddle cover (vinyl)", cover, C_SADDLE, "plastic", 4, "shell", (-200, 0, 560))
    base = Pos(0, 0, top_z - 41) * extrude(make_face(Polyline(*[(scx + x * 0.94, y * 0.9, 0) for x, y in plan], close=True)),
                                          amount=6)
    base = _fillet_try(base, base.faces().sort_by(Axis.Z)[0].edges(), [2.5, 1.2])
    add("Saddle base", base, C_SADDLE_BASE, "plastic", 4, "shell", (-200, 0, 560))
    pt = st(post_top)
    rz = top_z - 47.0
    rails = []
    for s in (-1, 1):
        a = (scx - 80, s * 30, top_z - 38)
        b = (scx - 62, s * 22, rz)
        c2 = (scx + 55, s * 22, rz)
        d2 = (scx + 80, s * 14, top_z - 38)
        rails += [_rtube(a, b, 3.5), _tube(b, c2, 3.5), _rtube(c2, d2, 3.5)]
    rail_s = rails[0]
    for r_ in rails[1:]:
        rail_s += r_
    add("Saddle rails", rail_s, C_STEEL, "metal", 4, "shell", (-200, 0, 560))
    clamp_s = Pos(pt[0], 0, rz) * Box(34, 56, 13)
    clamp_s = _fillet_try(clamp_s, clamp_s.edges(), [2.5, 1.5])
    clamp_s += _tube(ax_seat(post_top - 20), (pt[0], 0, rz), 13.2)
    clamp_s += Pos(pt[0], -31, rz) * Rot(90, 0, 0) * _hex_nut(13, 5)
    add("Saddle clamp, 13 mm", clamp_s, C_COLLAR, "metal", 4, "shell", (-200, 0, 480))

    # ================================================================ 5 telescoping quill stem
    t_clamp = D["steerer_top"] + S["stem_exp"]
    q_top = sr(t_clamp)
    quill = _tube(ax_steer(t_clamp - D["quill_len"]), ax_steer(t_clamp - 6), P["quill_d"] / 2)
    add("Quill, 22.2 mm chromoly", quill, C_CHROME, "metal", 5, "shell", ex_steer(170))
    wedge = _tube(ax_steer(t_clamp - D["quill_len"] - 22), ax_steer(t_clamp - D["quill_len"] + 2), P["quill_d"] / 2 - 0.4)
    add("Quill expander wedge", wedge, C_STEEL, "metal", 5, "internal", ex_steer(120))
    qrings = []
    tq = D["steerer_top"] + 10.0
    k = 0
    while tq < t_clamp - 14:
        wd = 2.2 if k % 3 == 2 else 1.1
        qrings.append(_tube(ax_steer(tq - wd / 2), ax_steer(tq + wd / 2), P["quill_d"] / 2 + 0.25))
        tq += 10.0
        k += 1
    if qrings:
        add("Quill height scale (painted)", Compound(children=qrings), C_GRAPHITE, "painted", 5, "shell", ex_steer(170))
    clamp = (q_top[0] + S["ext"], q_top[1] + P["stem_rise"])
    neck = _tube(ax_steer(t_clamp - 22), _xz(clamp), 14.0)
    barrel = _cyl_y(clamp, 16.5, 46)
    head = neck + barrel
    head -= _cyl_y(clamp, P["bar_d"] / 2 + 0.2, 60)
    head = _fillet_try(head, head.edges(), [1.2, 0.6])
    pinch = Pos(clamp[0] + 13, 0, clamp[1] - 14) * Box(14, 22, 10)
    pinch = _fillet_try(pinch, pinch.edges(), [2.0, 1.0])
    head += pinch
    add("Stem head", head, C_GRAPHITE, "painted", 5, "shell", ex_steer(200))
    exp_bolt = _loc(_xz((clamp[0] - 2 * 0, clamp[1] + 16.5 - 2)), steer_dir) * \
        (Cylinder(6.5, 6, align=None) - Pos(0, 0, 3) * extrude(RegularPolygon(3.6, 6), amount=4))
    pinch_bolt = Pos(clamp[0] + 13, -12, clamp[1] - 14) * Rot(90, 0, 0) * _hex_nut(13, 5)
    add("Stem bolts, 13 mm", exp_bolt + pinch_bolt, C_STEEL, "metal", 19, "shell", ex_steer(200))

    # ================================================================ 6 handlebar, grips, lever, bell
    gx, gz = clamp[0] - P["bar_sweep"], clamp[1] + P["bar_rise"]
    hw = P["bar_width"] / 2
    br = P["bar_d"] / 2
    bar = _tube((clamp[0], -110, clamp[1]), (clamp[0], 110, clamp[1]), br)
    grips_pt = {}
    grip_parts, plug_parts = [], []
    for s in (-1, 1):
        p0 = (clamp[0], s * 110, clamp[1])
        p1 = (gx + 40, s * (hw - 110), gz)
        p2 = (gx - 10, s * hw, gz)
        bar += _tube(p0, p1, br) + Pos(*p0) * Sphere(br) + Pos(*p1) * Sphere(br) + _tube(p1, p2, br)
        u = (_v(p2) - _v(p1))
        L = u.length
        u = u.normalized()
        g0 = _v(p1) + u * 8
        grip = Pos(0, 0, (L - 12) / 2) * Cylinder(14.5, L - 12)
        grip += Pos(0, 0, 2) * Cylinder(18, 4)                        # inner flange
        for kk in range(10):
            grip -= Pos(0, 0, 14 + kk * 9.5) * (Cylinder(16, 3.2) - Cylinder(13.2, 3.6))
        grip = _fillet_try(grip, grip.faces().sort_by(Axis.Z)[0].edges(), [1.5, 0.8])
        grip_parts.append(_loc(g0, u) * grip)
        plug = Pos(0, 0, L - 12 + 3) * Cylinder(15.5, 6)
        plug = _fillet_try(plug, plug.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
        plug_parts.append(_loc(g0, u) * plug)
        grips_pt[s] = tuple(g0 + u * ((L - 12) / 2))
    add("Handlebar, 22.2 mm alloy", bar, C_ALLOY, "metal", 6, "shell", (-60, 0, 330))
    add("Grips", Compound(children=grip_parts), C_RUBBER, "rubber", 6, "shell", (-60, 0, 330))
    add("Grip end plugs", Compound(children=plug_parts), C_COLLAR, "plastic", 6, "shell", (-60, 0, 330))

    # front brake lever on the right (-Y) grip
    p1 = _v((gx + 40, -(hw - 110), gz))
    p2 = _v((gx - 10, -hw, gz))
    u = (p2 - p1).normalized()
    nfw = Vector(-u.Y, u.X, 0) if (-u.Y) > 0 else Vector(u.Y, -u.X, 0)     # horizontal, toward +X
    lclamp = _loc(p1 + u * 2, u) * (Pos(0, 0, 0) * (Cylinder(17, 12) - Cylinder(br + 0.2, 14)))
    lbody = _loc(p1 + u * 2 + nfw * 20 + Vector(0, 0, -4), u) * Box(16, 22, 12)
    lbody = lbody + _loc(p1 + u * 2 + nfw * 11, u) * Box(10, 18, 10)
    lclamp += lbody
    blade = _rtube(tuple(p1 + u * 10 + nfw * 28 + Vector(0, 0, -6)), tuple(p1 + u * 92 + nfw * 32 + Vector(0, 0, -10)), 4.5)
    add("Front brake lever", lclamp + blade, C_ALLOY, "metal", 12, "shell", (-60, 0, 330))

    # bell on the left of the bar centre
    bc = (clamp[0], 88.0, clamp[1])
    bell = Pos(bc[0] - 6, bc[1], bc[2] + br + 4) * (Sphere(21) & Pos(0, 0, 21) * Box(50, 50, 42))
    bell += Pos(bc[0] - 6, bc[1], bc[2] + br + 2) * Cylinder(21, 4)
    bell_clamp = _cyl_y((bc[0], bc[2]), br + 3, 12, y=bc[1]) - _cyl_y((bc[0], bc[2]), br + 0.2, 14, y=bc[1])
    bell_clamp += Pos(bc[0] - 6, bc[1], bc[2] + br + 0.5) * Box(12, 12, 5)
    bell_lever = Pos(bc[0] - 6 - 24, bc[1], bc[2] + br + 6) * Box(18, 6, 3)
    add("Bell", bell, C_CHROME, "metal", 17, "shell", (-60, 60, 380))
    add("Bell clamp and striker", bell_clamp + bell_lever, C_COLLAR, "plastic", 17, "shell", (-60, 60, 380))

    # front reflector on the stem head (white)
    fr = Pos(clamp[0] + 30, 0, clamp[1] - 25) * Box(7, 58, 34)
    fr = _fillet_try(fr, fr.edges().filter_by(Axis.X), [8, 5, 2])
    fr = _fillet_try(fr, fr.faces().sort_by(Axis.X)[-1].edges(), [1.5, 0.8])
    fr_br = Pos(clamp[0] + 22, 0, clamp[1] - 18) * Box(12, 16, 3)
    add("Front reflector (white)", fr, C_WHITE_REFL, "plastic", 17, "shell", (80, 0, 300))
    add("Front reflector bracket", fr_br, C_COLLAR, "metal", 17, "shell", (80, 0, 300))

    # ================================================================ 7, 8 wheels, 9 tires
    def rim(cen):
        prof = [(189.5, -8.0), (193.0, -10.5), (199.0, -11.0), (207.0, -11.0), (208.8, -11.6), (209.6, -9.8),
                (206.5, -8.0), (204.5, -2.5), (204.5, 2.5), (206.5, 8.0), (209.6, 9.8), (208.8, 11.6),
                (207.0, 11.0), (199.0, 11.0), (193.0, 10.5), (189.5, 8.0)]
        wire = Polyline(*[(r, 0, z) for r, z in prof], close=True)
        ring = revolve(make_face(wire), Axis.Z, 360)
        return Pos(cen[0], 0, cen[1]) * Rot(90, 0, 0) * ring

    def brake_track(cen):
        rings = []
        for s in (-1, 1):
            rings.append(_ring_y(cen, 206.8, 199.5, 0.6, y=s * 11.2))
        return rings[0] + rings[1]

    def spokes(cen, n, flange_r, flange_y, cross_deg):
        items = []
        for i in range(n):
            a = 2 * pi * i / n
            side = 1 if i % 2 else -1
            dirn = 1 if (i // 2) % 2 else -1
            ph = (cen[0] + flange_r * cos(a), side * flange_y, cen[1] + flange_r * sin(a))
            ar = a + dirn * radians(cross_deg)
            pr = (cen[0] + 190.5 * cos(ar), side * 1.5, cen[1] + 190.5 * sin(ar))
            items.append(_tube(ph, pr, 1.0))
            items.append(_tube(pr, tuple(_v(pr) + (_v(ph) - _v(pr)).normalized() * 9.0), 1.7))   # nipple
        return Compound(children=items)

    def hub(cen, barrel_r, flange_r, flange_y, length):
        h = _cyl_y(cen, barrel_r, 2 * flange_y)
        for s in (-1, 1):
            f = _cyl_y(cen, flange_r, 3.2, y=s * flange_y)
            h += _fillet_try(f, f.edges(), [1.2, 0.6])
            h += _cyl_y(cen, barrel_r * 0.7, length / 2 - flange_y, y=s * (flange_y + (length / 2 - flange_y) / 2))
        return h

    def tire(cen, grooves=56):
        t = Solid.make_torus(R - P["tire_sec_r"], P["tire_sec_r"], Plane(origin=(cen[0], 0, cen[1]), z_dir=(0, 1, 0)))
        cuts = []
        for kk in range(grooves):
            a = 2 * pi * kk / grooves
            for s in (-1, 1):
                ang = a + (pi / grooves if s > 0 else 0)
                rr = R - 1.2
                loc = Location(Plane(origin=(cen[0] + rr * cos(ang), s * 8.0, cen[1] + rr * sin(ang)),
                                     x_dir=(-sin(ang), 0, cos(ang)), z_dir=(cos(ang), 0, sin(ang))))
                cuts.append(loc * Box(4.0, 12.0, 4.4))
        try:
            t2 = t - Compound(children=cuts)
            if t2.is_valid:
                return t2
        except Exception:
            pass
        return t

    for key, cen, n, fr_r, fr_y, blen, bom_w, dx in (("front", front, 28, 26.0, 30.0, 100.0, 7, 520.0),
                                                     ("rear", rear, 36, 33.0, 40.0, 120.0, 8, -540.0)):
        label = "Front" if key == "front" else "Rear"
        ex = (dx, 0, 0)
        add(f"{label} rim, alloy", rim(cen), C_ALLOY, "metal", bom_w, "shell", ex)
        add(f"{label} rim brake track", brake_track(cen), "#D5D9DE", "metal", bom_w, "shell", ex)
        add(f"{label} spokes", spokes(cen, n, fr_r - 4, fr_y, 38 if key == "front" else 44), C_CHROME, "metal", bom_w,
            "shell", ex)
        if key == "front":
            hb = hub(cen, 14, fr_r, fr_y, blen)
            add("Front hub", hb, C_ALLOY, "metal", 7, "shell", ex)
        else:
            hb = hub(cen, 22, fr_r, fr_y, blen)
            add("Rear coaster brake hub", hb, C_ALLOY, "metal", 8, "shell", ex)
        axle = _cyl_y(cen, 5.5, 150)
        nuts = []
        for s in (-1, 1):
            yd = (57.5 if key == "rear" else 52.5)
            nut = _hex_nut(15, 7)
            loc = Location(Plane(origin=(cen[0], s * yd, cen[1]), x_dir=(1, 0, 0), z_dir=(0, s, 0)))
            nuts.append(loc * nut)
            nuts.append(_cyl_y(cen, 9.0, 1.5, y=s * (yd - 0.75)))       # washer
        add(f"{label} axle and 15 mm nuts", axle + nuts[0] + nuts[1] + nuts[2] + nuts[3], C_STEEL, "metal", bom_w,
            "shell", ex)
        add(f"{label} solid tire, 20 x 1.95 in", tire(cen), C_TIRE, "rubber", 9, "shell", ex)
        # spoke reflector (amber), in the spoke plane
        sr_ = Pos(cen[0] + 120, 0, cen[1] + 60) * Box(50, 9, 20)
        sr_ = _fillet_try(sr_, sr_.edges().filter_by(Axis.Y), [7, 4])
        sr_ = _fillet_try(sr_, sr_.faces().sort_by(Axis.Y)[0].edges(), [1.2, 0.6])
        add(f"{label} spoke reflector", sr_, C_AMBER, "plastic", 17, "shell", ex)

    # coaster brake reaction arm and clip (non-drive side)
    arm = Pos(70, 50, R + 2.5) * Rot(0, -2, 0) * Box(140, 5, 16)
    arm = _fillet_try(arm, arm.edges().filter_by(Axis.Y), [6, 3])
    arm += _cyl_y((0, R), 16, 5, y=50)
    clip = _ring_y((140, R + 5), 12, 9.6, 14, y=50)
    add("Coaster brake arm and clip", arm + clip, C_DARK_STEEL, "metal", 8, "shell", (-540, 40, 0))

    # ================================================================ 10 crankset and pedals, 11 chain
    yc = P["chain_y"]
    ring_r = P["chain_pitch"] / (2 * sin(pi / P["ring_t"]))
    cog_r = P["chain_pitch"] / (2 * sin(pi / P["cog_t"]))
    ca = radians(CRANK_ANG)
    cv = (P["crank"] * cos(ca), P["crank"] * sin(ca))
    ring = _gear_y(bb, ring_r, P["ring_t"], 3.0, yc, 22)
    for kk in range(5):
        a = 2 * pi * kk / 5 + ca
        win = _cyl_y((bb[0] + 38 * cos(a + pi / 5), bb[1] + 38 * sin(a + pi / 5)), 12.5, 6, yc)
        ring -= win
    add("Chainring, 32T", ring, C_ALLOY, "metal", 10, "shell", (0, -260, -60))

    def crank_arm(p_end, y0):
        pts = _hull_pts([(bb[0], bb[1], 16.0), (p_end[0], p_end[1], 11.0)], n=48)
        a = _plate_xz(pts, y0 - 5, 10)
        return _fillet_try(a, a.edges(), [3.0, 2.0, 1.0])

    pe_r = (bb[0] + cv[0], bb[1] + cv[1])
    pe_l = (bb[0] - cv[0], bb[1] - cv[1])
    crank_r = crank_arm(pe_r, yc - 9)
    crank_l = crank_arm(pe_l, 58)
    caps = _cyl_y(bb, 10, 3, y=yc - 15) + _cyl_y(bb, 10, 3, y=64.5)
    spider = _cyl_y(bb, 26, 4, y=yc - 3)
    for kk in range(5):
        a = 2 * pi * kk / 5 + ca
        spider += _tube((bb[0], yc - 3, bb[1]), (bb[0] + 38 * cos(a), yc - 3, bb[1] + 38 * sin(a)), 5)
        spider += _cyl_y((bb[0] + 38 * cos(a), bb[1] + 38 * sin(a)), 5.5, 5, y=yc - 1)
    add("Crank arms, 140 mm", crank_r + crank_l + spider, C_ALLOY, "metal", 10, "shell", (0, -260, -60))
    add("Crank dust caps", caps, C_COLLAR, "plastic", 10, "shell", (0, -260, -60))

    def pedal(pe, yin, s):
        """Platform pedal: cage with a spindle barrel, reflectors front and back (s = +1 at +Y)."""
        L_, Wd, T = 76.0, 92.0, 20.0
        yc_ = yin + s * (8 + Wd / 2)
        body = Pos(pe[0], yc_, pe[1]) * Box(L_, Wd, T)
        body = _fillet_try(body, body.edges().filter_by(Axis.Z), [8, 5])
        body -= Pos(pe[0], yc_, pe[1]) * Box(L_ - 20, Wd - 16, T + 2)
        body += _cyl_y(pe, 10, Wd - 4, y=yc_)
        for dxp in (-L_ / 2 + 5, L_ / 2 - 5):       # grip teeth on the cage bars
            for kk in range(6):
                yy = yc_ - Wd / 2 + 12 + kk * (Wd - 24) / 5
                body += Pos(pe[0] + dxp, yy, pe[1] + T / 2 + 1) * Box(6, 4, 2)
                body += Pos(pe[0] + dxp, yy, pe[1] - T / 2 - 1) * Box(6, 4, 2)
        axle_p = _cyl_y(pe, 5.5, 10, y=yin + s * 4)
        refl = [Pos(pe[0] + sx * (L_ / 2 + 0.6), yc_, pe[1]) * Box(2.2, 46, 10) for sx in (-1, 1)]
        return body + axle_p, refl[0] + refl[1]

    pr_body, pr_refl = pedal(pe_r, yc - 14, -1)
    pl_body, pl_refl = pedal(pe_l, 63, 1)
    add("Pedal, drive side", pr_body, C_RUBBER, "plastic", 10, "shell", (0, -380, -60))
    add("Pedal, left", pl_body, C_RUBBER, "plastic", 10, "shell", (0, 260, -60))
    add("Pedal reflectors", pr_refl, C_AMBER, "plastic", 10, "shell", (0, -380, -60))
    add("Pedal reflectors, left", pl_refl, C_AMBER, "plastic", 10, "shell", (0, 260, -60))

    # 18T sprocket and the chain (86 links around the chainring and sprocket)
    cog = _gear_y(rear, cog_r, P["cog_t"], 3.0, yc, 16)
    add("Sprocket, 18T", cog, C_DARK_STEEL, "metal", 8, "shell", (-540, -120, 0))
    path = _hull_pts([(bb[0], bb[1], ring_r), (rear[0], rear[1], cog_r)], n=240)
    path.append(path[0])
    seg = [sqrt((path[i + 1][0] - path[i][0]) ** 2 + (path[i + 1][1] - path[i][1]) ** 2) for i in range(len(path) - 1)]
    per = sum(seg)
    n_links = max(int(round(per / P["chain_pitch"])), 10)
    step = per / n_links
    pins = []
    acc, i, tgt = 0.0, 0, 0.0
    for kk in range(n_links):
        tgt = kk * step
        while i < len(seg) - 1 and acc + seg[i] < tgt:
            acc += seg[i]
            i += 1
        f = (tgt - acc) / seg[i] if seg[i] else 0.0
        pins.append((path[i][0] + f * (path[i + 1][0] - path[i][0]), path[i][1] + f * (path[i + 1][1] - path[i][1])))
    links, rollers = [], []
    for kk in range(n_links):
        a_, b_ = pins[kk], pins[(kk + 1) % n_links]
        mx, mz = (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2
        ang = degrees(atan2(b_[1] - a_[1], b_[0] - a_[0]))
        wy = 3.9 if kk % 2 else 3.0          # outer and inner plates alternate
        for s in (-1, 1):
            pl = Pos(mx, yc + s * wy, mz) * Rot(0, -ang, 0) * extrude(Plane.XZ * SlotOverall(P["chain_pitch"] + 7.5, 7.8),
                                                                    amount=0.6, both=True)
            links.append(pl)
        rollers.append(_cyl_y(a_, 2.6, 2 * 3.9 + 1.2, y=yc))
    add("Chain, 1/2 x 1/8 in", Compound(children=links), C_DARK_STEEL, "metal", 11, "shell", (0, -170, 0))
    add("Chain rollers", Compound(children=rollers), C_STEEL, "metal", 11, "shell", (0, -170, 0))

    # ================================================================ 12 front rim brake (side-pull caliper)
    cx_b = c[0] + 8
    rb = 203.5
    zpad = front[1] + sqrt(rb ** 2 - (front[0] - cx_b) ** 2)
    cal_top = c[1] - 4
    arms = []
    for s in (-1, 1):
        a1 = _rtube((cx_b, 0, cal_top), (cx_b, s * 34, cal_top - 14), 4.2)
        a2 = _rtube((cx_b, s * 34, cal_top - 14), (cx_b, s * 30, zpad + 4), 4.2)
        arms += [a1, a2]
    cal = arms[0] + arms[1] + arms[2] + arms[3]
    cal += Pos(cx_b, 0, cal_top) * Rot(0, 90, 0) * Cylinder(7, 12)
    add("Side-pull caliper", cal, C_ALLOY, "metal", 12, "shell", (320, 0, 140))
    pads = []
    for s in (-1, 1):
        pad = Pos(cx_b, s * 16.5, zpad) * Box(34, 6, 9)
        pad = _fillet_try(pad, pad.edges().filter_by(Axis.Y), [3, 1.5])
        pads.append(pad + _tube((cx_b, s * 19, zpad), (cx_b, s * 30, zpad + 3), 3.0))
    add("Brake pads", pads[0] + pads[1], C_RUBBER, "rubber", 12, "shell", (320, 0, 140))
    add("Caliper mounting bolt", _tube((c[0] - 22, 0, cal_top + 2), (cx_b + 8, 0, cal_top), 3.0)
        + Pos(cx_b + 9, 0, cal_top) * Rot(0, 90, 0) * _hex_nut(10, 4), C_STEEL, "metal", 19, "shell", (320, 0, 140))
    try:
        lever_end = p1 + u * 12 + nfw * 24 + Vector(0, 0, -2)
        pts = [tuple(lever_end), (lever_end.X + 40, lever_end.Y + 40, lever_end.Z - 30),
               (clamp[0] + 70, -40, clamp[1] - 70), (cx_b + 30, -6, cal_top + 60), (cx_b + 2, -2, cal_top + 8)]
        path_c = Spline(*pts)
        prof = Plane(origin=path_c @ 0, z_dir=path_c % 0) * Circle(2.6)
        cable = sweep(prof, path=path_c)
        if cable.is_valid:
            add("Brake cable housing", cable, C_RUBBER, "plastic", 12, "shell", (-60, 0, 330))
    except Exception:
        pass

    # ================================================================ 13 rear rack
    rz_ = P["rack_z"]
    x0, x1 = P["rack_x0"], P["rack_x0"] + P["rack_len"]
    rw, rt = P["rack_w"] / 2, P["rack_tube"] / 2
    parts_r = [_rtube((x0, s * rw, rz_), (x1, s * rw, rz_), rt) for s in (-1, 1)]
    parts_r += [_tube((x0, 0, rz_), (x1, 0, rz_), rt)]
    parts_r += [_tube((x, -rw, rz_), (x, rw, rz_), rt - 1) for x in (x0, (x0 + x1) / 2, x1)]
    parts_r += [_rtube((x0 + 5, s * rw, rz_), (0, s * (rw + 2), R + 10), rt) for s in (-1, 1)]
    ssx = st(P["ss_s"] - 60)
    parts_r += [_rtube((x1 - 5, s * rw, rz_), (ssx[0] * 0.55, s * 30, R + (ssx[1] - R) * 0.55), rt - 2) for s in (-1, 1)]
    rack = parts_r[0]
    for p_ in parts_r[1:]:
        rack += p_
    add("Aluminium rear rack, 10 kg rated", rack, C_RACK, "metal", 13, "shell", (-80, 0, 380))
    tabs = []
    for s in (-1, 1):
        tabs.append(Pos(0, s * 60.5, R + 10) * Box(16, 3, 22))
        tabs.append(Location(Plane(origin=(0, s * 62, R + 10), x_dir=(1, 0, 0), z_dir=(0, s, 0))) * _hex_nut(10, 4))
        sx_ = (ssx[0] * 0.55, s * 30, R + (ssx[1] - R) * 0.55)
        tabs.append(Pos(sx_[0], s * 26, sx_[2]) * Rot(90, 0, 0) * Cylinder(6.5, 8))
    tb = tabs[0]
    for t_ in tabs[1:]:
        tb += t_
    add("Rack mounting bolts", tb, C_STEEL, "metal", 19, "shell", (-80, 0, 380))
    # rating plate on the drive-side rail, text raised
    plate_c = ((x0 + x1) / 2 + 30, -rw - 6.4, rz_ - 12)
    plate = Pos(*plate_c) * Box(84, 1.6, 22)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [3, 1.5])
    add("Rack rating plate", plate, C_GRAPHITE, "painted", 13, "shell", (-80, -40, 380))
    try:
        txt = _text_plate("MAX 10 kg", 11, 0.5)
        txt = Location(Plane(origin=(plate_c[0], plate_c[1] - 0.8, plate_c[2]), x_dir=(1, 0, 0), z_dir=(0, -1, 0))) * \
            Pos(0, -4.0, 0) * txt
        add("Rack rating marking", txt, C_SCALE, "painted", 13, "shell", (-80, -40, 380))
    except Exception:
        pass
    # rear reflector (red) under the rear of the platform
    rr_ = Pos(x0 - 14, 0, rz_ - 40) * Box(7, 72, 38)
    rr_ = _fillet_try(rr_, rr_.edges().filter_by(Axis.X), [8, 4])
    rr_ = _fillet_try(rr_, rr_.faces().sort_by(Axis.X)[0].edges(), [1.5, 0.8])
    rr_br = Pos(x0 - 6, 0, rz_ - 14) * Box(10, 20, 28)
    add("Rear reflector (red)", rr_, C_RED, "plastic", 17, "shell", (-140, 0, 380))
    add("Rear reflector bracket", rr_br, C_RACK, "metal", 17, "shell", (-140, 0, 380))

    # ================================================================ 14 fenders
    def fender(cen, keep, ends_deg):
        ro, ri = R + P["fender_gap"] + 4, R + P["fender_gap"]
        f = _ring_y(cen, ro, ri, 58)
        for s in (-1, 1):
            f += _ring_y(cen, ro, ri - 8, 3, y=s * 29.5)
        f = f & keep
        f = _fillet_try(f, f.edges(), [1.2, 0.6])
        return f

    fk = Pos(WB + 20, 0, R + 250) * Box(620, 200, 500)
    rk = Pos(-40, 0, R + 250) * Box(700, 200, 500)
    add("Front fender", fender(front, fk, None), C_FENDER, "plastic", 14, "shell", (520, 0, 240))
    add("Rear fender", fender(rear, rk, None), C_FENDER, "plastic", 14, "shell", (-540, 0, 230))
    stays = []
    rf = R + P["fender_gap"] + 2
    for cen, th, yax in ((front, 12.0, 52.5), (rear, 168.0, 57.5)):
        for s in (-1, 1):
            p_f = (cen[0] + rf * cos(radians(th)), s * 31.5, cen[1] + rf * sin(radians(th)))
            stays.append(_rtube(p_f, (cen[0], s * (yax + 8.5), cen[1] + 4), 2.2))
    add("Fender stays, front", stays[0] + stays[1], C_STEEL, "metal", 14, "shell", (520, 0, 240))
    add("Fender stays, rear", stays[2] + stays[3], C_STEEL, "metal", 14, "shell", (-540, 0, 230))
    flap = Pos(WB + 20 + 290 - 12, 0, R + 30) * Box(3, 56, 70)
    flap = _fillet_try(flap, flap.edges().filter_by(Axis.X), [8, 4])
    add("Mud flap", flap, C_RUBBER, "rubber", 14, "shell", (520, 0, 240))

    # ================================================================ 15 chainguard
    mid = (bb[0] / 2, (bb[1] + R) / 2)
    gcx, gcz = mid[0] + 30, mid[1] + 50
    gy = yc - 16
    guard = extrude(Plane.XZ * Pos(gcx, gcz) * RectangleRounded(440, 45, 18), amount=1.5, both=True)
    guard = Pos(0, gy, 0) * guard
    lip = _tube((gcx - 200, gy, gcz + 22.5), (gcx + 200, gy, gcz + 22.5), 2.4)
    guard = guard + lip
    add("Chainguard", guard, C_GUARD, "painted", 15, "shell", (0, -330, 80))
    try:
        name = _text_plate("GrowRider", 20, 0.6)
        name = Location(Plane(origin=(gcx - 60, gy - 1.5, gcz), x_dir=(1, 0, 0), z_dir=(0, -1, 0))) * Pos(0, -7, 0) * name
        add("Chainguard name", name, C_FRAME, "painted", 15, "shell", (0, -330, 80))
    except Exception:
        pass
    gb = [Location(Plane(origin=(x, gy - 1.5, gcz - 8), x_dir=(1, 0, 0), z_dir=(0, -1, 0))) *
          Pos(0, 0, 1.0) * Cylinder(4.5, 2.0)
          for x in (gcx - 180, gcx + 150)]
    add("Chainguard screws", gb[0] + gb[1], C_STEEL, "metal", 19, "shell", (0, -330, 80))

    # ================================================================ 16 kickstand
    ks_top = (120.0, 20.0, P["bb_z"] - 2)
    ks_bot = (190.0, 110.0, 12.0)
    leg = _rtube(ks_top, ks_bot, 7)
    foot = Pos(ks_bot[0] + 4, ks_bot[1] + 5, 6) * Box(34, 22, 12)
    foot = _fillet_try(foot, foot.edges(), [4, 2])
    ks_mount = Pos(120, 20, ks_z - 8) * Box(36, 44, 12)
    ks_mount = _fillet_try(ks_mount, ks_mount.edges().filter_by(Axis.Z), [5, 3])
    add("Kickstand", leg + ks_mount, C_DARK_STEEL, "metal", 16, "shell", (0, 220, -160))
    add("Kickstand foot", foot, C_RUBBER, "rubber", 16, "shell", (0, 220, -160))

    # ================================================================ context: 1.30 m child riding
    ped_top = 10.0 + 1.0
    grips_w = {1: grips_pt[1], -1: grips_pt[-1]}
    pedals_w = {-1: (pe_r[0], yc - 60, pe_r[1] + ped_top), 1: (pe_l[0], 110.0, pe_l[1] + ped_top)}
    saddle_top = (scx - 12.0, 0.0, top_z)
    try:
        rider = _rider(P, D, saddle_top, grips_w, pedals_w)
        add("Child rider, 1.30 m (scale)", rider, C_CLAY, "clay", None, "context", (0, 0, 0))
    except Exception as e:  # keep the bike renderable if the mannequin cannot be built
        print("rider not built:", e)
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
