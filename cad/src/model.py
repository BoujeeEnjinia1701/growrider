"""GrowRider parametric model (build123d), TRL 3, constructable design (GRR-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks only
Exports:
    growrider-small.step / .stl    whole bike set for the smallest rider (1.10 m)
    growrider-large.step / .stl    whole bike set for the largest rider (1.65 m)
    frame.step, fork.step, seat-post-assembly.step, stem-and-bar.step, rack.step (and .stl)

Axes: X along the bike (rear axle at x = 0, front toward +X), Z up with the ground
at z = 0, Y lateral. The drive side (chain) is at -Y, the rider's right.

Every part can be made by its stated process and fits and fastens to the parts next
to it (STANDARDS section 18). build_components() returns each made or bought
component by name; build_parts() groups them into the 17 BOM lines used by the
concept media. check() measures contacts and clearances with build123d.
The same PARAMS feed docs/04-calcs/sizing.py (GRR-CAL-001).
"""
import sys
from collections import namedtuple
from math import atan2, cos, degrees, pi, radians, sin, sqrt
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # wheels: 20 in, ISO 406, solid or airless 20 x 1.95 in tires (decided 2026-09-25)
    "tire_od": 500.0, "tire_sec_r": 24.0, "rim_r": 203.0,
    "wheelbase": 860.0, "chainstay": 380.0, "bb_z": 260.0,
    # steering: 70 deg head angle, 30 mm fork offset
    "head_ang": 70.0, "fork_offset": 30.0,
    # head tube and steerer, positions along the steering axis from its point at axle height
    "crown_t": 275.0,            # top of fork crown (bottom of the lower headset cup)
    "crown_h": 16.0,             # fork crown depth along the steering axis (DDR-003, P13)
    "ht_bot": 285.0, "ht_len": 180.0,
    "headset_top_stack": 30.0,   # upper cup, washer and locknut above the head tube
    "ht_od": 34.0, "ht_wall": 2.0,            # 30.0 mm bore for 1 in (JIS) press-in headset cups (DDR-003, P4)
    "steerer": (25.4, 1.6),                   # 1 in threaded chromoly steerer, 22.2 mm bore
    # main tubes (head, seat, down, loop), steerer, quill and sleeve in chromoly 4130 (GRR-DDR-002, D7 and D10)
    # seat tube and two-stage telescoping seat post
    "seat_ang": 70.0,
    "st_len": 280.0,             # bottom bracket center to top of seat tube, along the seat axis
    "st_od": 31.8, "st_wall": 1.2,            # 29.4 mm bore for the 29.2 mm sleeve
    "st_blocked": 40.0,          # bottom of the seat tube bore lost to the BB shell
    "sleeve_od": 29.2, "sleeve_wall": 1.8, "sleeve_len": 250.0,   # 25.6 mm bore for the 25.4 mm post
    "sleeve_exp_min": 20.0, "sleeve_exp_max": 150.0,
    "post_od": 25.4, "post_wall": 1.8, "post_len": 280.0,
    "post_exp_min": 40.0, "post_exp_max": 180.0,
    "saddle_stack": 60.0,        # top of post to top of saddle
    "saddle_rail": 15.0,         # fore-aft rail adjustment, each way
    "min_insert": 100.0,         # minimum insertion at every sliding joint (R2)
    # clamp collars with stop screws (DDR-003, P8): collar height, wall, stop screw depth below the top
    "collar_h": 14.0, "collar_wall": 4.0, "stop_depth": 7.0, "stop_d": 5.0, "slot_w": 6.0,
    # long quill stem in the 1 in threaded steerer; 22.0 mm quill (DDR-003, P5)
    "quill_d": 22.0, "quill_wall": 2.0, "quill_travel": 120.0, "quill_exp_min": 20.0,
    # head plate welded to the quill, bar clamp block bolted at one of two positions (DDR-003, P6):
    # bar center ahead of the steering axis, and bar center above the quill top
    "stem_ext": (45.0, 105.0), "stem_rise": 15.0,
    "head_plate": (127.0, 44.0, 10.0),        # length, width, thickness (chromoly 4130 plate)
    "clamp_block": (54.0, 44.0, 30.0),        # along X, along Y (bar axis), height (aluminium, two halves)
    # swept-back roadster-style handlebar: 205 mm sweep and 15 mm rise keep the grips where the concept had them
    "bar_d": 22.2, "bar_width": 520.0, "bar_sweep": 205.0, "bar_rise": 15.0,
    # other frame tubes (OD, wall)
    "down": (31.8, 0.9), "loop": (28.6, 0.9), "chainstay_tube": (19.0, 1.2), "seatstay_tube": (16.0, 1.2),
    "loop_t": 380.0, "loop_s": 120.0,    # loop tube ends: on the steering axis and on the seat axis
    "down_t": 305.0,                     # down tube top end on the steering axis (DDR-003, P15)
    "ss_s": 235.0,                       # seat stay cross bar on the seat axis, below the collar (DDR-003, P7)
    "ss_y_top": 40.0,                    # seat stay centers at the cross bar, each side (DDR-003, P10)
    "cs_y_bb": 21.0,                     # chainstay centers at the BB shell, each side
    "bb_shell": (40.0, 3.0, 68.0),       # OD, wall, width
    "stand_ahead": 100.0,                # stepping point: this far ahead of the loop tube's seat-tube joint
    # rear track-end dropouts and fork ends (DDR-003, P1 and P2)
    "drop_t": 6.0, "rear_old": 110.0, "front_old": 100.0, "fork_end_t": 5.0, "axle_d": 9.5,
    # drive
    "crank": 140.0, "ring_t": 32, "cog_t": 18, "chain_pitch": 12.7, "chain_y": -42.0, "crank_y": 59.0,
    # rack: aluminium (6061-T6) platform over the rear wheel, rated 10 kg (GRR-DDR-002, D7); lowered to clear the saddle (P11)
    "rack_len": 300.0, "rack_w": 120.0, "rack_z": 545.0, "rack_x0": -85.0, "rack_tube": 12.0, "rack_wall": 1.5,
    # fenders: 16 mm gap to the tire, 64 mm wide; rear fender starts 10 deg above the axle line at the front
    "fender_gap": 16.0, "ffender_gap": 12.0, "fender_w": 64.0, "rfender_front_deg": 10.0,
    # kickstand plate between the chainstays, this far behind the BB center
    "kick_x": 55.0,
}

# Rider settings used for the exported assemblies (saddle height from BB center to
# saddle top along the seat axis; stem exposure above the steerer; bar clamp position).
SETTINGS = {
    "small": {"saddle_h": 400.0, "stem_exp": 20.0, "ext": 45.0},
    "large": {"saddle_h": 670.0, "stem_exp": 140.0, "ext": 105.0},
}

Comp = namedtuple("Comp", "name shape bom make")


def derived(P=PARAMS):
    """Positions and ranges that other parts and the calc note depend on."""
    d = {}
    R = P["tire_od"] / 2
    d["R"] = R
    d["bb_x"] = sqrt(P["chainstay"] ** 2 - (R - P["bb_z"]) ** 2)
    ha, sa = radians(P["head_ang"]), radians(P["seat_ang"])
    d["steer_dir"] = (-cos(ha), sin(ha))
    d["seat_dir"] = (-cos(sa), sin(sa))
    d["steer0_x"] = P["wheelbase"] - P["fork_offset"] / sin(ha)
    d["trail"] = (R * cos(ha) - P["fork_offset"]) / sin(ha)
    d["ht_top"] = P["ht_bot"] + P["ht_len"]
    d["steerer_top"] = d["ht_top"] + P["headset_top_stack"]
    d["steerer_usable"] = d["steerer_top"] - P["crown_t"]
    d["quill_len"] = d["steerer_usable"] + P["quill_exp_min"]          # quill below its top end
    d["quill_exp_max"] = P["quill_exp_min"] + P["quill_travel"]
    d["quill_insert_min"] = d["quill_len"] - d["quill_exp_max"]
    # seat post stages
    d["saddle_min"] = P["st_len"] + P["sleeve_exp_min"] + P["post_exp_min"] + P["saddle_stack"]
    d["saddle_max"] = P["st_len"] + P["sleeve_exp_max"] + P["post_exp_max"] + P["saddle_stack"]
    d["sleeve_insert_min"] = P["sleeve_len"] - P["sleeve_exp_max"]
    d["post_insert_min"] = P["post_len"] - P["post_exp_max"]
    d["st_depth"] = P["st_len"] - P["st_blocked"]
    d["sleeve_depth_max"] = P["sleeve_len"] - P["sleeve_exp_min"]      # deepest sleeve bottom below seat tube top
    d["post_depth_max"] = P["post_len"] - P["post_exp_min"] - P["sleeve_exp_min"]
    # stop slots: the stop screw sits stop_depth below the top of the outer part (in its collar);
    # slot ends, measured up from the bottom of the inner part, are where the screw stops it
    c = P["stop_d"] / 2 + 0.5
    d["sleeve_slot"] = (P["sleeve_len"] - P["stop_depth"] - P["sleeve_exp_max"] - c,
                        P["sleeve_len"] - P["stop_depth"] - P["sleeve_exp_min"] + c)
    d["post_slot"] = (P["post_len"] - P["stop_depth"] - P["post_exp_max"] - c,
                      P["post_len"] - P["stop_depth"] - P["post_exp_min"] + c)
    # stepping point on the loop tube (top surface)
    a = seat_pt(P["loop_s"], P, d)
    b = steer_pt(P["loop_t"], P, d)
    xs = a[0] + P["stand_ahead"]
    zs = a[1] + (b[1] - a[1]) * (xs - a[0]) / (b[0] - a[0])
    ang = atan2(b[1] - a[1], b[0] - a[0])
    d["standover"] = zs + P["loop"][0] / 2 / cos(ang)
    d["stand_x"] = xs
    # fork crown: its underside on the steering axis, and its clearance to the front tire
    c = steer_pt(P["crown_t"], P, d)
    d["crown_pt"] = c
    u = steer_pt(P["crown_t"] - P["crown_h"], P, d)
    d["crown_under"] = u
    d["crown_clear"] = sqrt((u[0] - P["wheelbase"]) ** 2 + (u[1] - R) ** 2) - R
    cc = steer_pt(P["crown_t"] - P["crown_h"] / 2, P, d)
    d["crown_mid"] = cc
    # dropout and stay end points
    d["cs_end"] = (40.0, R + 1.2)                 # chainstay end on the dropout plate (x, z)
    d["ss_end"] = (16.0, R + 20.0)                # seat stay end on the dropout plate
    d["eyelet"] = (-18.0, R + 20.0)               # M5 eyelet on each dropout (rack strut and fender stay)
    d["drop_y"] = P["rear_old"] / 2               # inner face of each rear dropout
    sx, sz = seat_pt(P["ss_s"], P)
    off = (P["st_od"] / 2 + P["seatstay_tube"][0] / 2) / cos(radians(90 - P["seat_ang"]))
    d["xbar"] = (sx - off, sz)                    # seat stay cross bar center (x, z)
    # front brake reach: crown bolt to the middle of the rim's brake track
    d["brake_reach"] = sqrt((cc[0] - P["wheelbase"]) ** 2 + (cc[1] - R) ** 2) - (P["rim_r"] - 7.0)
    return d


def seat_pt(s, P=PARAMS, d=None):
    """Point on the seat axis, s mm from the BB center. Returns (x, z)."""
    R = P["tire_od"] / 2
    bx = sqrt(P["chainstay"] ** 2 - (R - P["bb_z"]) ** 2)
    sa = radians(P["seat_ang"])
    return (bx - s * cos(sa), P["bb_z"] + s * sin(sa))


def steer_pt(t, P=PARAMS, d=None):
    """Point on the steering axis, t mm above its point at axle height. Returns (x, z)."""
    ha = radians(P["head_ang"])
    x0 = P["wheelbase"] - P["fork_offset"] / sin(ha)
    return (x0 - t * cos(ha), P["tire_od"] / 2 + t * sin(ha))


def grip_pt(stem_exp, ext, P=PARAMS):
    """Grip center (x, z) for a stem exposure above the steerer and a bar clamp position."""
    d = derived(P)
    cx, cz = steer_pt(d["steerer_top"] + stem_exp, P)
    return (cx + ext - P["bar_sweep"], cz + P["stem_rise"] + P["bar_rise"])


def saddle_pt(saddle_h, P=PARAMS):
    """Saddle reference point (seat axis at saddle top height), (x, z)."""
    return seat_pt(saddle_h, P)


def split_saddle(saddle_h, P=PARAMS):
    """Share a saddle height between the two stages: sleeve first, then post."""
    need = saddle_h - P["st_len"] - P["saddle_stack"]
    sl = min(max(need - P["post_exp_min"], P["sleeve_exp_min"]), P["sleeve_exp_max"])
    po = min(max(need - sl, P["post_exp_min"]), P["post_exp_max"])
    return sl, po


def seatstay_pt(f, side, P=PARAMS):
    """Point on a seat stay axis, f = 0 at the dropout end, 1 at the cross bar. Returns (x, y, z)."""
    d = derived(P)
    (x0, z0), (x1, z1) = d["ss_end"], d["xbar"]
    y0, y1 = d["drop_y"] + P["drop_t"] / 2, P["ss_y_top"]
    return (x0 + f * (x1 - x0), side * (y0 + f * (y1 - y0)), z0 + f * (z1 - z0))


def chainstay_pt(f, side, P=PARAMS):
    """Point on a chainstay axis, f = 0 at the dropout end, 1 at the BB center. Returns (x, y, z)."""
    d = derived(P)
    (x0, z0), (x1, z1) = d["cs_end"], (d["bb_x"], P["bb_z"])
    y0, y1 = d["drop_y"] + P["drop_t"] / 2, P["cs_y_bb"]
    return (x0 + f * (x1 - x0), side * (y0 + f * (y1 - y0)), z0 + f * (z1 - z0))


# ---------------------------------------------------------------- geometry helpers

def _tube(p1, p2, r):
    from build123d import Plane, Solid, Vector
    p1, p2 = Vector(*p1), Vector(*p2)
    v = p2 - p1
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v.normalized()))


def _hollow(p1, p2, ro, ri):
    return _tube(p1, p2, ro) - _tube(p1, p2, ri)


def _xz(p, y=0.0):
    return (p[0], y, p[1])


def _ring_y(c, r_out, r_in, width, y=0.0):
    from build123d import Plane, Solid
    pl = Plane(origin=(c[0], y - width / 2, c[1]), z_dir=(0, 1, 0))
    return Solid.make_cylinder(r_out, width, pl) - Solid.make_cylinder(r_in, width, pl)


def _disc_y(c, r, width, y=0.0):
    from build123d import Plane, Solid
    return Solid.make_cylinder(r, width, Plane(origin=(c[0], y - width / 2, c[1]), z_dir=(0, 1, 0)))


def _plate_xz(pts, y_lo, t):
    """Flat plate with outline pts (x, z) in the XZ plane, from y_lo to y_lo + t."""
    from build123d import Plane, Polygon, extrude
    pl = Plane(origin=(0, y_lo, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return extrude(pl * Polygon(*pts, align=None), amount=t)


def _axis_plane(p, ang):
    """Plane at point p (x, z) with z along an axis tilted back ang degrees from horizontal (seat or
    steering axis), x pointing forward and up square to it, and y toward +Y (the rider's left)."""
    from build123d import Plane
    a = radians(ang)
    return Plane(origin=(p[0], 0, p[1]), x_dir=(sin(a), 0, cos(a)), z_dir=(-cos(a), 0, sin(a)))


def _comp(*shapes):
    from build123d import Compound
    return Compound(children=[s for s in shapes if s is not None])


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out.fuse(s)
    return out.clean() if hasattr(out, "clean") else out


def _ltube(pl, a, b, r):
    """Tube between two points given in a plane's local coordinates."""
    va, vb = pl.from_local_coords(a), pl.from_local_coords(b)
    return _tube((va.X, va.Y, va.Z), (vb.X, vb.Y, vb.Z), r)


def _collar(pl, z0, bore, tip_r, P, side):
    """Clamp collar on an axis plane, from z0 to z0 + collar_h: a ring with clamp lugs and an M8
    (13 mm) bolt at the back, and an M5 stop screw on side (+1 left, -1 right), stop_depth below the
    top, whose dog point reaches in to radius tip_r (into the slot of the part inside)."""
    from build123d import Box, Pos, Solid
    h, w = P["collar_h"], P["collar_wall"]
    ro = bore / 2 + w
    ring = pl * Pos(0, 0, z0) * (Solid.make_cylinder(ro, h) - Solid.make_cylinder(bore / 2, h))
    lugs = pl * Pos(-(ro + 4), 0, z0 + h / 2) * Box(10, 14, h)
    slit = pl * Pos(-(ro + 3), 0, z0 + h / 2) * Box(14, 2.0, h + 2)
    zs = z0 + h - P["stop_depth"]
    hole = _ltube(pl, (0, side * (bore / 2 - 1), zs), (0, side * (ro + 1), zs), P["stop_d"] / 2)
    collar = (ring + lugs) - slit - hole
    bolt = _ltube(pl, (-(ro + 4), -12, z0 + h / 2), (-(ro + 4), 12, z0 + h / 2), 4)
    screw = _ltube(pl, (0, side * tip_r, zs), (0, side * (ro + 0.5), zs), P["stop_d"] / 2)
    head = _ltube(pl, (0, side * (ro + 0.5), zs), (0, side * (ro + 5), zs), 4.2)
    return collar, _comp(bolt, screw + head)


# ---------------------------------------------------------------- components

def build_components(P=PARAMS, setting="large"):
    """Every made and bought component, by name: {key: Comp(name, shape, bom line, make)}."""
    from build123d import Box, Cylinder, Plane, Pos, Rot, Solid
    S = SETTINGS[setting] if isinstance(setting, str) else setting
    d = derived(P)
    R = d["R"]
    rear, front = (0.0, R), (P["wheelbase"], R)
    bb = (d["bb_x"], P["bb_z"])
    st = lambda s: seat_pt(s, P)
    sr = lambda t: steer_pt(t, P)
    C = {}

    def add(key, name, shape, bom, make):
        C[key] = Comp(name, shape, bom, make)

    # ---------------------------------------------------------- 1 frame (one brazed or TIG-welded assembly)
    hb, sb = P["ht_od"] / 2 - P["ht_wall"], P["st_od"] / 2 - P["st_wall"]
    ht = _tube(_xz(sr(P["ht_bot"])), _xz(sr(d["ht_top"])), P["ht_od"] / 2)
    seat_tube = _tube(_xz(bb), _xz(st(P["st_len"])), P["st_od"] / 2)
    down = _tube(_xz(sr(P["down_t"])), _xz(bb), P["down"][0] / 2)
    loop = _tube(_xz(sr(P["loop_t"])), _xz(st(P["loop_s"])), P["loop"][0] / 2)
    od, _, w = P["bb_shell"]
    shell = _disc_y(bb, od / 2, w)
    xb = d["xbar"]
    yt = P["ss_y_top"]
    xbar = _tube((xb[0], -(yt + 8), xb[1]), (xb[0], yt + 8, xb[1]), P["seatstay_tube"][0] / 2)
    cs = [_tube(chainstay_pt(0, s, P), chainstay_pt(1, s, P), P["chainstay_tube"][0] / 2) for s in (-1, 1)]
    ss = [_tube(seatstay_pt(0, s, P), seatstay_pt(1, s, P), P["seatstay_tube"][0] / 2) for s in (-1, 1)]
    # rear track-end dropouts: 6 mm steel plate, slot open to the rear for the 3/8 in axle
    drop_pts = [(-30, R - 14), (-30, R + 30), (-2, R + 30), (24, R + 38), (52, R + 14), (52, R - 12), (36, R - 16)]
    drops = []
    for s in (-1, 1):
        y_lo = d["drop_y"] if s > 0 else -d["drop_y"] - P["drop_t"]
        pl = _plate_xz(drop_pts, y_lo, P["drop_t"])
        slot = Pos(-14, s * (d["drop_y"] + P["drop_t"] / 2), R) * Box(34, 20, P["axle_d"] + 0.5) + \
            _disc_y((3, R), (P["axle_d"] + 0.5) / 2, 20, y=s * (d["drop_y"] + P["drop_t"] / 2))
        eye = _disc_y(d["eyelet"], 2.75, 20, y=s * (d["drop_y"] + P["drop_t"] / 2))
        drops.append(pl - slot - eye)
    # seat stay bridge for the rear fender, where the stays are 292 mm from the axle
    fb = _bridge_f(P)
    pa, pb = seatstay_pt(fb, -1, P), seatstay_pt(fb, 1, P)
    bridge = _tube(pa, pb, 6.0)
    # kickstand plate under the chainstays, behind the BB
    kx = d["bb_x"] - P["kick_x"]
    fk = (kx - d["cs_end"][0]) / (d["bb_x"] - d["cs_end"][0])
    czk = chainstay_pt(fk, 1, P)[2] - P["chainstay_tube"][0] / 2
    kick_plate = Pos(kx, 0, czk - 2.0 + 0.4) * Box(40, 64, 4) - Pos(kx, 0, czk - 2) * Cylinder(5.25, 8)
    # brazed-on bosses: rack stay boss on each seat stay, chainguard boss on the drive chainstay
    fr = _rack_boss_f(P)
    bosses = []
    for s in (-1, 1):
        p = seatstay_pt(fr, s, P)
        bosses.append(_tube((p[0], s * (abs(p[1]) + 4), p[2]), (p[0], s * (abs(p[1]) + P["seatstay_tube"][0] / 2 + 8), p[2]), 5.0))
    pcg = chainstay_pt(0.38, -1, P)
    bosses.append(_tube((pcg[0], pcg[1], pcg[2] + 4), (pcg[0], pcg[1], pcg[2] + P["chainstay_tube"][0] / 2 + 8), 5.0))
    frame = _fuse([ht, seat_tube, down, loop, shell, xbar, bridge, kick_plate, *cs, *ss, *drops, *bosses])
    # mitres: every tube stops at the outside of the tube it meets, so the bores stay clear
    frame = frame - _tube(_xz(st(P["st_blocked"])), _xz(st(P["st_len"] + 5)), sb) \
        - _tube(_xz(sr(P["ht_bot"] - 5)), _xz(sr(d["ht_top"] + 5)), hb) - _disc_y(bb, od / 2 - 3, w + 2)
    # seat tube clamp slit (rear) and stop screw hole (left)
    pst = _axis_plane(st(0), P["seat_ang"])
    frame = frame - pst * Pos(-P["st_od"] / 2, 0, P["st_len"] - 12) * Box(6, 2.0, 26) \
        - pst * Pos(0, P["st_od"] / 2, P["st_len"] - P["stop_depth"]) * Rot(90, 0, 0) * Cylinder(P["stop_d"] / 2 + 0.25, 8)
    add("frame", "Frame", frame, 1, True)

    # ---------------------------------------------------------- 18 bottom bracket and headset (bought)
    bbset = _comp(_ring_y(bb, 21.5, 8, 4, y=w / 2 + 2), _ring_y(bb, 21.5, 8, 4, y=-w / 2 - 2),
                  _disc_y(bb, 8, 124))
    lower_cup = _hollow(_xz(sr(P["crown_t"])), _xz(sr(P["ht_bot"])), 18.5, 12.8)
    top_stack = _hollow(_xz(sr(d["ht_top"])), _xz(sr(d["steerer_top"])), 18.5, 12.8)
    add("bb", "Bottom bracket (cups and spindle)", bbset, 18, False)
    add("headset", "Headset (cups, locknut)", _comp(lower_cup, top_stack), 18, False)

    # ---------------------------------------------------------- 2 fork (bought to specification)
    c = d["crown_mid"]
    crown = Pos(c[0], 0, c[1]) * Rot(0, -(90 - P["head_ang"]), 0) * Box(40, 110, P["crown_h"])
    crown = crown - _tube((c[0] - 40 * sin(radians(P["head_ang"])), 0, c[1] - 40 * cos(radians(P["head_ang"]))),
                          (c[0] + 40 * sin(radians(P["head_ang"])), 0, c[1] + 40 * cos(radians(P["head_ang"]))), 3.5)
    fy = P["front_old"] / 2 + P["fork_end_t"] / 2
    fe_top = (front[0] - 6, R + 30)
    blades = [_tube((c[0], s * 45, c[1]), (fe_top[0], s * fy, fe_top[1] + 4), 10) for s in (-1, 1)]
    fe_pts = [(front[0] - 18, R - 12), (front[0] - 18, R + 40), (front[0] + 8, R + 40), (front[0] + 14, R + 20),
              (front[0] + 14, R - 12)]
    fork_ends = []
    for s in (-1, 1):
        y_lo = P["front_old"] / 2 if s > 0 else -P["front_old"] / 2 - P["fork_end_t"]
        pl = _plate_xz(fe_pts, y_lo, P["fork_end_t"])
        slot = Pos(front[0], s * fy, R - 8) * Box(P["axle_d"] + 0.5, 20, 16) + _disc_y(front, (P["axle_d"] + 0.5) / 2, 20, y=s * fy)
        eye = _disc_y((front[0] + 6, R + 24), 2.75, 20, y=s * fy)
        fork_ends.append(pl - slot - eye)
    steerer = _hollow(_xz(sr(P["crown_t"] - P["crown_h"] + 0.5)), _xz(sr(d["steerer_top"])), P["steerer"][0] / 2,
                      P["steerer"][0] / 2 - P["steerer"][1])
    add("fork", "Fork with long 1 in steerer", _fuse([crown, *blades, *fork_ends]) + steerer, 2, False)

    # ---------------------------------------------------------- 3 telescoping seat post: sleeve, post, collars
    sl_exp, po_exp = split_saddle(S["saddle_h"], P)
    sleeve_top = P["st_len"] + sl_exp
    post_top = sleeve_top + po_exp
    sleeve_bot = sleeve_top - P["sleeve_len"]
    post_bot = post_top - P["post_len"]
    pl_s = _axis_plane(st(sleeve_bot), P["seat_ang"])
    sleeve = _hollow(_xz(st(sleeve_bot)), _xz(st(sleeve_top)), P["sleeve_od"] / 2, P["sleeve_od"] / 2 - P["sleeve_wall"])
    a0, a1 = d["sleeve_slot"]
    sleeve = sleeve - pl_s * Pos(0, P["sleeve_od"] / 2, (a0 + a1) / 2) * Box(P["slot_w"], 8, a1 - a0) \
        - pl_s * Pos(-P["sleeve_od"] / 2, 0, P["sleeve_len"] - 12) * Box(6, 2.0, 26) \
        - pl_s * Pos(0, -P["sleeve_od"] / 2, P["sleeve_len"] - P["stop_depth"]) * Rot(90, 0, 0) * Cylinder(P["stop_d"] / 2 + 0.25, 8)
    pl_p = _axis_plane(st(post_bot), P["seat_ang"])
    post = _hollow(_xz(st(post_bot)), _xz(st(post_top)), P["post_od"] / 2, P["post_od"] / 2 - P["post_wall"])
    b0, b1 = d["post_slot"]
    post = post - pl_p * Pos(0, -P["post_od"] / 2, (b0 + b1) / 2) * Box(P["slot_w"], 8, b1 - b0)
    st_collar, st_bolts = _collar(pst, P["st_len"] - P["collar_h"], P["st_od"], P["sleeve_od"] / 2 - P["sleeve_wall"] / 2 - 0.4, P, +1)
    sl_collar, sl_bolts = _collar(pst, sleeve_top - P["collar_h"], P["sleeve_od"], P["post_od"] / 2 - P["post_wall"] - 0.5, P, -1)
    add("sleeve", "Seat post sleeve", sleeve, 3, True)
    add("post", "Seat post, slotted", post, 3, True)
    add("st_collar", "Seat tube collar and stop screw", st_collar, 19, True)
    add("st_screws", "Seat tube collar bolt and stop screw", st_bolts, 19, False)
    add("sl_collar", "Sleeve collar and stop screw", sl_collar, 19, True)
    add("sl_screws", "Sleeve collar bolt and stop screw", sl_bolts, 19, False)

    # ---------------------------------------------------------- 4 saddle
    sp = st(post_top + P["saddle_stack"])
    shell_ = Pos(sp[0] + 15, 0, sp[1] - 12) * Box(220, 125, 24)
    rails = Pos(sp[0] + 10, 0, sp[1] - 36) * Box(120, 44, 24)
    clamp_ = Pos(st(post_top)[0], 0, st(post_top)[1] + 12) * Box(40, 44, 24)
    add("saddle", "Saddle and clamp", _comp(shell_, rails, clamp_), 4, False)

    # ---------------------------------------------------------- 5 quill stem: quill, head plate, clamp block
    t_top = d["steerer_top"] + S["stem_exp"]
    q_top = sr(t_top)
    quill = _hollow(_xz(sr(t_top - d["quill_len"])), _xz(q_top), P["quill_d"] / 2, P["quill_d"] / 2 - P["quill_wall"])
    cap = _tube(_xz(sr(t_top - 3)), _xz(q_top), P["quill_d"] / 2)
    wedge = _tube(_xz(sr(t_top - d["quill_len"] - 24)), _xz(sr(t_top - d["quill_len"] - 2)), P["quill_d"] / 2 - 0.5)
    exp_bolt = _comp(_tube(_xz(q_top), _xz(sr(t_top + 5.5)), 7.5), _tube(_xz(sr(t_top - d["quill_len"] - 12)), _xz(q_top), 4))
    L, Wp, T = P["head_plate"]
    hp_x0 = q_top[0] + 10
    plate = Pos(hp_x0 + L / 2, 0, q_top[1] - T / 2) * Box(L, Wp, T)          # top flush with the quill top
    holes = []
    for e in P["stem_ext"]:
        for dx in (-18, 18):
            for dy in (-13, 13):
                holes.append(Pos(q_top[0] + e + dx, dy, q_top[1] - T / 2) * Cylinder(3.4, T + 2))   # tapped M8 (6.8 drill)
    for h in holes:
        plate = plate - h
    plate = plate - _tube(_xz(sr(t_top - 60)), _xz(sr(t_top + 20)), P["quill_d"] / 2)   # coped to the quill's curve
    add("quill", "Quill with its cap and wedge", _comp(quill, cap, wedge), 5, True)
    add("exp_bolt", "Expander bolt (M8, 13 mm head)", exp_bolt, 5, False)
    add("head_plate", "Head plate", plate, 5, True)
    bx, bz = q_top[0] + S["ext"], q_top[1] + P["stem_rise"]
    Lb, Wb, Hb = P["clamp_block"]
    bore = lambda: _tube((bx, -Wb, bz), (bx, Wb, bz), P["bar_d"] / 2 + 0.05)
    blk_lo = Pos(bx, 0, bz - 7.5) * Box(Lb, Wb, 15) - bore()
    blk_hi = Pos(bx, 0, bz + 7.5) * Box(Lb, Wb, 15) - bore()
    bolts = []
    for dx in (-18, 18):
        for dy in (-13, 13):
            blk_lo = blk_lo - Pos(bx + dx, dy, bz - 7.5) * Cylinder(4.25, 16)
            blk_hi = blk_hi - Pos(bx + dx, dy, bz + 7.5) * Cylinder(4.25, 16)
            bolts.append(Pos(bx + dx, dy, bz + 15 + 2.75) * Cylinder(6.5, 5.5, ))
            bolts.append(Pos(bx + dx, dy, bz - 10) * Cylinder(4, 40))
    add("clamp_lo", "Bar clamp block, lower half", blk_lo, 5, True)
    add("clamp_hi", "Bar clamp block, cap", blk_hi, 5, True)
    add("clamp_bolts", "Clamp bolts (4 x M8, 13 mm heads)", _comp(*bolts), 5, False)

    # ---------------------------------------------------------- 6 handlebar and grips
    gx, gz = bx - P["bar_sweep"], bz + P["bar_rise"]
    hw = P["bar_width"] / 2
    br = P["bar_d"] / 2
    bar = [_tube((bx, -110, bz), (bx, 110, bz), br)]
    grips = []
    on_bar = lambda t, s: (gx + 40 - 50 * t, s * (hw - 110 + 110 * t), gz)   # noqa: E731
    for s in (-1, 1):
        bar.append(_tube((bx, s * 110, bz), (gx + 40, s * (hw - 110), gz), br))
        bar.append(_tube((gx + 40, s * (hw - 110), gz), (gx - 10, s * hw, gz), br))
        grips.append(_tube(on_bar(0.3, s), on_bar(1.0, s), 15))
    add("handlebar", "Handlebar", _comp(*bar), 6, False)
    add("grips", "Grips", _comp(*grips), 6, False)

    # ---------------------------------------------------------- 7, 8 wheels; 9 tires
    def wheel(cen, hub_r, shell_w, old, n=18):
        rim = _ring_y(cen, P["rim_r"] + 6, P["rim_r"] - 14, 26)
        hub = _disc_y(cen, hub_r, shell_w)
        cones = _disc_y(cen, 12, old)
        axle = _disc_y(cen, P["axle_d"] / 2, old + 24)
        nuts = [_disc_y(cen, 8.5, 7, y=s * (old / 2 + P["drop_t"] + 3.5)) for s in (-1, 1)]
        spokes = []
        for i in range(n):
            a = 2 * pi * i / n
            side = 1 if i % 2 else -1
            ph = (cen[0] + hub_r * cos(a), side * shell_w * 0.4, cen[1] + hub_r * sin(a))
            pr = (cen[0] + (P["rim_r"] - 14) * cos(a + 0.35), 0, cen[1] + (P["rim_r"] - 14) * sin(a + 0.35))
            spokes.append(_tube(ph, pr, 1.6))
        return _comp(rim, hub, cones, axle, *nuts, *spokes)

    add("front_wheel", "Front wheel", wheel(front, 22, 70, P["front_old"]), 7, False)
    yc = P["chain_y"]
    cog_r = P["chain_pitch"] / (2 * sin(pi / P["cog_t"]))
    driver = _disc_y(rear, 16, 10, y=yc)
    cog = _ring_y(rear, cog_r + 3, 16, 3, y=yc)
    # coaster brake arm on the left, forward along the underside of the left chainstay
    fa = (135 - d["cs_end"][0]) / (d["bb_x"] - d["cs_end"][0])
    pa = chainstay_pt(fa, 1, P)
    arm_z = pa[2] - P["chainstay_tube"][0] / 2 - 8.0
    arm_y = d["drop_y"] - 3
    arm = _comp(_ring_y(rear, 16, P["axle_d"] / 2, 4, y=arm_y),
                Pos((135 + 10) / 2, arm_y, (R + arm_z) / 2) *
                Rot(0, -degrees(atan2(arm_z - R, 135)), 0) * Box(sqrt(135 ** 2 + (arm_z - R) ** 2) + 10, 4, 16))
    add("rear_wheel", "Rear wheel with coaster hub", _comp(wheel(rear, 32, 80, P["rear_old"]), driver), 8, False)
    add("cog", "18T sprocket", cog, 8, False)
    add("arm", "Coaster brake arm", arm, 8, False)
    # arm clip: a band round the chainstay and the arm, one M6 bolt below
    clip = _fuse([_tube((pa[0] - 6, pa[1], pa[2]), (pa[0] + 6, pa[1], pa[2]), P["chainstay_tube"][0] / 2 + 1.5)
                  - _tube((pa[0] - 7, pa[1], pa[2]), (pa[0] + 7, pa[1], pa[2]), P["chainstay_tube"][0] / 2),
                  Pos(pa[0], arm_y - 2.75, (pa[2] + arm_z) / 2 - 8) * Box(12, 1.5, abs(pa[2] - arm_z) + 18),
                  Pos(pa[0], arm_y + 2.75, (pa[2] + arm_z) / 2 - 8) * Box(12, 1.5, abs(pa[2] - arm_z) + 18)])
    clip_bolt = _tube((pa[0], arm_y - 8, arm_z - 12), (pa[0], arm_y + 8, arm_z - 12), 3)
    add("arm_clip", "Arm clip and M6 bolt", _comp(clip, clip_bolt), 19, False)
    tires = _comp(*[Solid.make_torus(R - P["tire_sec_r"], P["tire_sec_r"], Plane(origin=(cx, 0, cz), z_dir=(0, 1, 0)))
                    for cx, cz in (rear, front)])
    add("tires", "Solid tires (2)", tires, 9, False)

    # ---------------------------------------------------------- 10 crankset, 11 chain
    ring_r = P["chain_pitch"] / (2 * sin(pi / P["ring_t"]))
    ca = radians(20)
    cv = (P["crank"] * cos(ca), P["crank"] * sin(ca))
    ring = _ring_y(bb, ring_r + 4, ring_r - 18, 3, y=yc)
    spider = _ring_y(bb, ring_r - 16, 10, 3, y=yc - 6)
    cy = P["crank_y"]
    crank_r = Pos(bb[0] + cv[0] / 2, -cy, bb[1] + cv[1] / 2) * Rot(0, -20, 0) * Box(P["crank"] + 24, 12, 22)
    crank_l = Pos(bb[0] - cv[0] / 2, cy, bb[1] - cv[1] / 2) * Rot(0, -20, 0) * Box(P["crank"] + 24, 12, 22)
    pedals = [Pos(bb[0] + cv[0], -(cy + 58), bb[1] + cv[1]) * Box(80, 90, 22),
              Pos(bb[0] - cv[0], cy + 58, bb[1] - cv[1]) * Box(80, 90, 22)]
    pedal_axles = [_tube((bb[0] + cv[0], -cy, bb[1] + cv[1]), (bb[0] + cv[0], -(cy + 104), bb[1] + cv[1]), 5),
                   _tube((bb[0] - cv[0], cy, bb[1] - cv[1]), (bb[0] - cv[0], cy + 104, bb[1] - cv[1]), 5)]
    add("crankset", "Crankset and chainring", _comp(ring, spider, crank_r, crank_l), 10, False)
    add("pedals", "Pedals", _comp(*pedals, *pedal_axles), 10, False)
    runs = [_tube((bb[0], yc, bb[1] + s * ring_r), (0, yc, R + s * cog_r), 4) for s in (-1, 1)]
    add("chain", "Chain", _comp(*runs), 11, False)

    # ---------------------------------------------------------- 12 front rim brake
    ha = radians(P["head_ang"])
    nrm = (sin(ha), cos(ha))                         # forward, square to the steering axis
    bolt_c = (c[0] + 12 * nrm[0], c[1] + 12 * nrm[1])
    brake_bolt = _tube((c[0] - 20 * nrm[0], 0, c[1] - 20 * nrm[1]), (c[0] + 30 * nrm[0], 0, c[1] + 30 * nrm[1]), 3)
    # pads on the rim's brake track, on the line from the bolt to the front axle
    ux, uz = front[0] - bolt_c[0], front[1] - bolt_c[1]
    ul = sqrt(ux * ux + uz * uz)
    ux, uz = ux / ul, uz / ul
    rp = P["rim_r"] - 7.0
    pad_c = (front[0] - ux * rp, front[1] - uz * rp)
    body = Pos(bolt_c[0] + 6 * nrm[0], 0, bolt_c[1] + 6 * nrm[1]) * Box(14, 92, 14)
    arms = []
    for s in (-1, 1):
        arms.append(_tube((bolt_c[0] + 6 * nrm[0], s * 42, bolt_c[1] + 6 * nrm[1]), (pad_c[0] + 8 * nrm[0], s * 40, pad_c[1] + 8 * nrm[1]), 4))
        arms.append(_tube((pad_c[0] + 8 * nrm[0], s * 40, pad_c[1] + 8 * nrm[1]), (pad_c[0], s * 22, pad_c[1]), 4))
        arms.append(Pos(pad_c[0], s * 17.5, pad_c[1]) * Rot(0, -degrees(atan2(uz, ux)), 0) * Box(10, 6, 34))
    lm0, lm1 = on_bar(0.12, -1), on_bar(0.24, -1)
    lever_mount = _tube(lm0, lm1, 13)
    lever = _tube((lm1[0] + 12, lm1[1], lm1[2] - 4), (on_bar(0.75, -1)[0] + 22, on_bar(0.75, -1)[1], gz - 8), 5)
    add("caliper", "Front caliper", _comp(body, *arms), 12, False)
    add("brake_bolt", "Caliper bolt through the crown", brake_bolt, 12, False)
    add("lever", "Brake lever", _comp(lever, lever_mount), 12, False)

    # ---------------------------------------------------------- 13 rear rack (aluminium, welded)
    rz, x0, x1 = P["rack_z"], P["rack_x0"], P["rack_x0"] + P["rack_len"]
    rw, rt = P["rack_w"] / 2, P["rack_tube"] / 2
    rails = [_tube((x0, s * rw, rz), (x1, s * rw, rz), rt) for s in (-1, 0, 1)]
    cross = [_tube((x, -rw, rz), (x, rw, rz), rt - 1) for x in (x0, (x0 + x1) / 2, x1)]
    ey = d["drop_y"] + P["drop_t"]          # outer face of each dropout
    struts, tabs = [], []
    for s in (-1, 1):
        tab_y = s * (ey + 1.6 + 1.5)        # outside the fender stay eye
        struts.append(_tube((x0 + 5, s * rw, rz - rt + 1), (d["eyelet"][0], s * (ey + 1.6 + 6), d["eyelet"][1] + 22), rt))
        tabs.append(Pos(d["eyelet"][0], tab_y, d["eyelet"][1] + 8) * Box(16, 3, 34) -
                    _disc_y(d["eyelet"], 2.75, 6, y=tab_y))
    stays = []
    for s in (-1, 1):
        p = seatstay_pt(fr, s, P)
        yb = s * (abs(p[1]) + P["seatstay_tube"][0] / 2 + 8)
        stays.append(_tube((x1 - 5, s * rw, rz - rt + 1), (p[0], yb + s * 1.5, p[2] + 14), rt - 2))
        tabs.append(Pos(p[0], yb + s * 1.5, p[2] + 4) * Box(14, 3, 26) - _tube((p[0], yb - 3, p[2]), (p[0], yb + 6, p[2]), 2.75))
    plate_ = Pos(x0 - 2, 0, rz - 32) * Box(3, 70, 50)
    add("rack", "Rear rack", _fuse([*rails, *cross, *struts, *stays, *tabs]), 13, True)
    add("rack_plate", "Rating plate and rear reflector bracket", plate_, 13, True)

    # ---------------------------------------------------------- 14 fenders and stays
    fw = P["fender_w"]
    r_in, r_out = R + P["fender_gap"], R + P["fender_gap"] + 3
    f_in, f_out = R + P["ffender_gap"], R + P["ffender_gap"] + 3
    a_front = radians(P["rfender_front_deg"])
    big = 400.0
    keep_r = _plate_xz([(0, R), (-big, R), (-big, R + big), (big, R + big), (big, R + big * sin(a_front) / cos(a_front))], -100, 200)
    rfender = _ring_y(rear, r_out, r_in, fw) & keep_r
    keep_f = _plate_xz([(front[0], R), (front[0] - big, R), (front[0] - big, R + big), (front[0] + big, R + big),
                        (front[0] + big, R + big * 0.364)], -100, 200)
    ffender = _ring_y(front, f_out, f_in, fw) & keep_f
    fst = []
    for s in (-1, 1):
        a = radians(150)
        fst.append(_tube((d["eyelet"][0], s * (ey + 0.8), d["eyelet"][1]), (rear[0] + (r_out + 1) * cos(a), s * (fw / 2 + 2), R + (r_out + 1) * sin(a)), 2))
        a = radians(35)
        fst.append(_tube((front[0] + 6, s * (P["front_old"] / 2 + P["fork_end_t"] + 0.8), R + 24),
                         (front[0] + (f_out + 1) * cos(a), s * (fw / 2 + 2), R + (f_out + 1) * sin(a)), 2))
    # brackets: rear fender to the seat stay bridge, front fender under the crown on the caliper bolt
    pb_ = seatstay_pt(fb, 1, P)
    rb_len = sqrt(pb_[0] ** 2 + (pb_[2] - R) ** 2) - 6 - r_out
    ab = atan2(pb_[2] - R, pb_[0])
    rbr = Pos((r_out + rb_len / 2) * cos(ab), 0, R + (r_out + rb_len / 2) * sin(ab)) * Rot(0, -degrees(ab), 0) * Box(rb_len + 1, 20, 2)
    cu = d["crown_under"]
    cb = sqrt((cu[0] - front[0]) ** 2 + (cu[1] - R) ** 2)
    ac = atan2(cu[1] - R, cu[0] - front[0])
    fbr = Pos(front[0] + (f_out + (cb - f_out) / 2) * cos(ac), 0, R + (f_out + (cb - f_out) / 2) * sin(ac)) * \
        Rot(0, -degrees(ac), 0) * Box(cb - f_out + 0.4, 20, 2)
    add("rfender", "Rear fender", rfender, 14, False)
    add("ffender", "Front fender", ffender, 14, False)
    add("fender_stays", "Fender stays and brackets", _comp(*fst, rbr, fbr), 14, False)

    # ---------------------------------------------------------- 15 chainguard
    top_a = (bb[0], bb[1] + ring_r + 4)
    top_b = (40.0, R + cog_r)
    ang = atan2(top_a[1] - top_b[1], top_a[0] - top_b[0])
    mid = ((top_a[0] + top_b[0]) / 2 + 20, (top_a[1] + top_b[1]) / 2)
    gy = yc - 8.5
    guard = Pos(mid[0], gy, mid[1] + 8) * Rot(0, -degrees(ang), 0) * Box(400, 1.2, 46)
    lip = Pos(mid[0], gy + 6, mid[1] + 31) * Rot(0, -degrees(ang), 0) * Box(400, 12, 1.2)
    # two mounts: a tab to the boss on the drive chainstay, and a band clip round the seat tube
    btop = pcg[2] + P["chainstay_tube"][0] / 2 + 8
    zrun = top_b[1] + (top_a[1] - top_b[1]) * (pcg[0] - top_b[0]) / (top_a[0] - top_b[0])
    gbot = zrun + 8 - 23 * cos(ang) + 4
    gtab = _comp(Pos(pcg[0], (pcg[1] + gy) / 2 - 0.6, btop + 0.6) * Box(16, abs(gy - pcg[1]) + 1.2, 1.2),
                 Pos(pcg[0], gy - 1.2, (btop + gbot) / 2 + 0.6) * Box(16, 1.2, gbot - btop + 1.2))
    sp_ = st(95)
    band = _tube((sp_[0], 0, sp_[1] - 6), (sp_[0], 0, sp_[1] + 6), P["st_od"] / 2 + 1.5) - _tube((sp_[0], 0, sp_[1] - 7), (sp_[0], 0, sp_[1] + 7), P["st_od"] / 2)
    arm_g = Pos(sp_[0], (gy - 1.2 - P["st_od"] / 2 - 1.5) / 2, sp_[1]) * Box(12, abs(gy) + 1.2 - P["st_od"] / 2 - 1.5, 1.5)
    add("chainguard", "Chainguard", _comp(guard, lip), 15, False)
    add("guard_mounts", "Chainguard tab and seat tube clip", _comp(gtab, band, arm_g), 15, False)

    # ---------------------------------------------------------- 16 kickstand (centre mount, leg on the left)
    kz = czk - 4
    kclamp = Pos(kx, 0, kz - 5) * Box(36, 50, 10)
    kbolt = Pos(kx, 0, czk - 2) * Cylinder(5, 36)
    leg = _tube((kx, 22, kz - 8), (kx - 120, 150, 10), 7)
    foot = Pos(kx - 120, 150, 5) * Box(30, 22, 10)
    add("kickstand", "Kickstand", _comp(kclamp, leg, foot), 16, False)
    add("kick_bolt", "Kickstand bolt (M10)", kbolt, 16, False)

    # ---------------------------------------------------------- 17 reflectors and bell
    refl = [Pos(x0 - 6, 0, rz - 40) * Box(6, 60, 30),
            Pos(q_top[0] + 10 + L + 4, 0, q_top[1] - 10) * Box(6, 44, 30),
            Pos(bx, 80, bz + P["bar_d"] / 2 + 8) * Cylinder(22, 16)]
    refl += [Pos(cx + 120, 0, cz + 60) * Box(50, 8, 20) for cx, cz in (rear, front)]
    add("reflectors", "Reflectors and bell", _comp(*refl), 17, False)
    return C


def _angle_between(a, b, u):
    """Angle (deg) between the line a to b (x, z) and the direction u."""
    vx, vz = b[0] - a[0], b[1] - a[1]
    n = sqrt(vx * vx + vz * vz)
    from math import acos
    return degrees(acos(abs((vx * u[0] + vz * u[1]) / n)))


def _bridge_f(P=PARAMS):
    """Fraction along the seat stays where they are 292 mm from the rear axle (fender bridge)."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        x, _, z = seatstay_pt(m, 1, P)
        if sqrt(x * x + (z - P["tire_od"] / 2) ** 2) < 292.0:
            lo = m
        else:
            hi = m
    return lo


def _rack_boss_f(P=PARAMS):
    """Fraction along the seat stays at the x of the rack's front end, less 10 mm."""
    d = derived(P)
    x_t = P["rack_x0"] + P["rack_len"] - 10
    (x0, _), (x1, _) = d["ss_end"], d["xbar"]
    return (x_t - x0) / (x1 - x0)


# Components grouped into the 17 modelled BOM lines (the exploded view and concept media)
GROUPS = [
    ("frame", "Step-through chromoly frame", ["frame"], 1),
    ("fork", "Fork, 1 in steerer", ["fork", "headset"], 2),
    ("seatpost", "Telescoping seat post (sleeve and post)", ["sleeve", "post", "st_collar", "st_screws", "sl_collar", "sl_screws"], 3),
    ("saddle", "Saddle", ["saddle"], 4),
    ("stem", "Telescoping quill stem", ["quill", "exp_bolt", "head_plate", "clamp_lo", "clamp_hi", "clamp_bolts"], 5),
    ("handlebar", "Handlebar and grips", ["handlebar", "grips"], 6),
    ("front_wheel", "Front wheel, 20 in, alloy rim", ["front_wheel"], 7),
    ("rear_wheel", "Rear wheel, alloy rim, coaster hub", ["rear_wheel", "cog", "arm", "arm_clip"], 8),
    ("tires", "Solid tires, 20 x 1.95 in (2)", ["tires"], 9),
    ("crankset", "Crankset, 32T, 140 mm", ["crankset", "pedals", "bb"], 10),
    ("chain", "Chain and 18T sprocket", ["chain"], 11),
    ("front_brake", "Front rim brake and lever", ["caliper", "brake_bolt", "lever"], 12),
    ("rack", "Aluminium rear rack, 10 kg rated", ["rack", "rack_plate"], 13),
    ("fenders", "Fenders", ["rfender", "ffender", "fender_stays"], 14),
    ("chainguard", "Chainguard", ["chainguard", "guard_mounts"], 15),
    ("kickstand", "Kickstand", ["kickstand", "kick_bolt"], 16),
    ("reflectors", "Reflectors and bell", ["reflectors"], 17),
]


def build_parts(P=PARAMS, setting="large", C=None):
    """Return [(key, name, shape, bom_no)] for the assembly at a rider setting (17 BOM lines)."""
    C = C or build_components(P, setting)
    return [(k, n, _comp(*[C[c].shape for c in keys]), b) for k, n, keys, b in GROUPS]


def build(P=PARAMS, setting="large", C=None):
    return _comp(*[s for _, _, s, _ in build_parts(P, setting, C)])


def tube_lengths(P=PARAMS):
    """Center-line lengths (mm) of the frame tubes, for the mass estimate in GRR-CAL-001."""
    d = derived(P)
    bb = (d["bb_x"], P["bb_z"])
    dist = lambda a, b: sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))
    return {
        "head": P["ht_len"],
        "seat": P["st_len"],
        "down": dist(steer_pt(P["down_t"], P), bb),
        "loop": dist(steer_pt(P["loop_t"], P), seat_pt(P["loop_s"], P)),
        "chainstay": 2 * dist(chainstay_pt(0, 1, P), chainstay_pt(1, 1, P)),
        "seatstay": 2 * dist(seatstay_pt(0, 1, P), seatstay_pt(1, 1, P)),
        "cross bar": 2 * P["ss_y_top"] + 16,
        "bridge": 2 * abs(seatstay_pt(_bridge_f(P), 1, P)[1]),
    }


def fitting_masses(P=PARAMS):
    """Masses (kg) of the small made fittings, from the model's volumes."""
    C = build_components(P, "large")
    steel, alu = 7.85e-6, 2.70e-6
    d = derived(P)
    drop = 2 * 0.0  # computed below from the frame's plate outline
    from build123d import Polygon  # noqa: F401
    plate_area = 0.0
    pts = [(-30, -14), (-30, 30), (-2, 30), (24, 38), (52, 14), (52, -12), (36, -16)]
    for i in range(len(pts)):
        x1, z1 = pts[i]
        x2, z2 = pts[(i + 1) % len(pts)]
        plate_area += x1 * z2 - x2 * z1
    plate_area = abs(plate_area) / 2 - 34 * 10 - pi * 25
    drop = 2 * plate_area * P["drop_t"] * steel
    kick = 40 * 64 * 4 * steel
    bosses = 3 * pi * 25 * 12 * steel
    return {
        "track-end dropouts (2)": drop,
        "kickstand plate and bosses": kick + bosses,
        "head plate": C["head_plate"].shape.volume * steel,
        "bar clamp block (aluminium)": (C["clamp_lo"].shape.volume + C["clamp_hi"].shape.volume) * alu,
        "clamp collars (2)": (C["st_collar"].shape.volume + C["sl_collar"].shape.volume) * steel,
    }


# ---------------------------------------------------------------- constructability checks

def check(verbose=True):
    """Contacts, clearances and fits that make the design buildable. Returns (passed, failed)."""
    P = PARAMS
    d = derived(P)
    res = []

    def rec(name, ok, value):
        res.append((name, ok, value))

    # fits measured on sizes (diametral clearance, mm)
    st_bore = P["st_od"] - 2 * P["st_wall"]
    sl_bore = P["sleeve_od"] - 2 * P["sleeve_wall"]
    str_bore = P["steerer"][0] - 2 * P["steerer"][1]
    ht_bore = P["ht_od"] - 2 * P["ht_wall"]
    for name, gap, lo, hi in (("sleeve in seat tube", st_bore - P["sleeve_od"], 0.1, 0.4),
                              ("post in sleeve", sl_bore - P["post_od"], 0.1, 0.4),
                              ("quill in steerer", str_bore - P["quill_d"], 0.1, 0.4)):
        rec(f"fit: {name}, diametral clearance {gap:.2f} mm (0.1 to 0.4)", lo - 1e-9 <= gap <= hi + 1e-9, gap)
    rec(f"fit: head tube bore {ht_bore:.1f} mm takes 1 in JIS press-in cups (30.0 mm bore)", abs(ht_bore - 30.0) < 0.05, ht_bore)
    rec(f"fit: insertion at full height, sleeve {d['sleeve_insert_min']:.0f}, post {d['post_insert_min']:.0f}, "
        f"quill {d['quill_insert_min']:.0f} mm (100 or more)",
        min(d["sleeve_insert_min"], d["post_insert_min"], d["quill_insert_min"]) >= P["min_insert"], 0)
    rec(f"fit: sleeve fully down {d['sleeve_depth_max']:.0f} mm and post {d['post_depth_max']:.0f} mm below the "
        f"seat tube top, inside its {d['st_depth']:.0f} mm clear bore", max(d["sleeve_depth_max"], d["post_depth_max"]) <= d["st_depth"], 0)
    # stop slots: the screw meets the slot end exactly at the minimum insertion
    for nm, (a0, a1), ln, emax in (("sleeve", d["sleeve_slot"], P["sleeve_len"], P["sleeve_exp_max"]),
                                   ("post", d["post_slot"], P["post_len"], P["post_exp_max"])):
        ins = ln - emax
        screw = ln - P["stop_depth"] - emax
        rec(f"stop: {nm} slot {a0:.1f} to {a1:.1f} mm up from its bottom; at the top stop the screw is "
            f"{screw:.0f} mm up and {ins:.0f} mm stays inserted", abs(screw - (a0 + P['stop_d'] / 2 + 0.5)) < 0.01 and ins >= 100, ins)
    over = P["down"][0] / 2 / sin(radians(_angle_between(steer_pt(P["down_t"], P), (d["bb_x"], P["bb_z"]), d["steer_dir"])))
    rec(f"frame: down tube meets the head tube {P['down_t'] - over - P['ht_bot']:.1f} mm above its lower end (the cup needs a clear end)",
        P["down_t"] - over - P["ht_bot"] >= 2.0, 0)
    xs_top = P["ss_s"] + P["seatstay_tube"][0] / 2 / cos(radians(90 - P["seat_ang"]))
    rec(f"frame: seat stay cross bar ends {P['st_len'] - P['collar_h'] - xs_top:.0f} mm below the seat tube collar",
        P["st_len"] - P["collar_h"] - xs_top >= 5.0, 0)
    rec(f"fit: brake reach {d['brake_reach']:.0f} mm from the crown bolt to the rim's brake track",
        80 <= d["brake_reach"] <= 95, d["brake_reach"])

    for setting in ("small", "large"):
        C = build_components(P, setting)
        g = lambda k: C[k].shape  # noqa: E731

        def dist(a, b):
            return g(a).distance_to(g(b)) if isinstance(a, str) else a.distance_to(b)

        def touch(a, b, tol=0.15):
            v = dist(a, b)
            rec(f"[{setting}] touch: {a} and {b}, gap {v:.2f} mm", v <= tol, v)

        def clear(a, b, mn, label=None):
            v = dist(a, b)
            rec(f"[{setting}] clear: {label or (a + ' and ' + b)} {v:.1f} mm (at least {mn})", v >= mn - 1e-6, v)

        touch("st_collar", "frame")
        touch("sl_collar", "sleeve")
        touch("st_screws", "sleeve", 0.6)   # dog point sits in the sleeve slot, 0.5 mm each side
        touch("sl_screws", "post", 0.6)
        clear("st_screws", "post", 0.3, "seat tube stop screw tip to the post inside the sleeve")
        touch("quill", "head_plate")
        touch("head_plate", "clamp_lo")
        touch("clamp_lo", "handlebar", 0.1)
        touch("clamp_hi", "handlebar", 0.1)
        clear("head_plate", "headset", 2.0, "head plate to headset locknut")
        touch("headset", "frame")
        clear("clamp_lo", "quill", 2.0, "bar clamp block to quill")
        clear("clamp_lo", "exp_bolt", 4.0, "bar clamp block to expander bolt head")
        clear("saddle", "rack", 20.0, "saddle to rack")
        clear("post", "frame", 0.04, "seat post to frame (inside the sleeve)")
        if setting == "large":
            touch("frame", "rear_wheel")              # hub locknuts on the dropout inner faces
            touch("fork", "front_wheel")
            touch("arm", "arm_clip", 0.3)
            touch("arm_clip", "frame")
            touch("kickstand", "frame", 0.5)
            touch("rack", "fender_stays", 0.2)
            touch("rack", "frame", 0.2)
            touch("fender_stays", "frame", 0.5)
            touch("fender_stays", "rfender", 2.5)
            touch("guard_mounts", "frame", 0.5)
            touch("caliper", "brake_bolt", 0.5)
            clear("tires", "frame", 3.0, "rear tire to chainstays, seat stays and bridge")
            clear("tires", "fork", 5.0, "front tire to fork")
            clear("rfender", "frame", 3.0, "rear fender to frame")
            clear("ffender", "fork", 2.0, "front fender to fork")
            clear("cog", "frame", 2.0, "sprocket to chainstay and dropout")
            clear("crankset", "frame", 2.0, "chainring and cranks to frame")
            clear("chain", "frame", 2.0, "chain to frame")
            clear("chain", "chainguard", 1.5)
            clear("crankset", "chainguard", 1.5)
            clear("rack", "rfender", 15.0, "rack to rear fender")
            clear("rack", "tires", 30.0, "rack to tire")
            clear("caliper", "tires", 3.0, "caliper arms to tire")
            clear("caliper", "ffender", 2.0, "caliper arms to front fender")
            clear("kickstand", "chain", 3.0)
    passed = [r for r in res if r[1]]
    failed = [r for r in res if not r[1]]
    if verbose:
        for n, ok, _ in res:
            print(("PASS " if ok else "FAIL ") + n)
        print(f"{len(passed)} of {len(res)} constructability checks pass")
    return passed, failed


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, f = check()
        sys.exit(1 if f else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    for setting in ("small", "large"):
        C = build_components(setting=setting)
        asm = build(setting=setting, C=C)
        export_step(asm, str(out / "step" / f"growrider-{setting}.step"))
        export_stl(asm, str(out / "stl" / f"growrider-{setting}.stl"), tolerance=0.5, angular_tolerance=0.3)
        print("exported", setting)
    parts = {k: s for k, _, s, _ in build_parts(setting="large", C=C)}
    for key, fname in [("frame", "frame"), ("fork", "fork"), ("seatpost", "seat-post-assembly"), ("rack", "rack")]:
        export_step(parts[key], str(out / "step" / f"{fname}.step"))
        export_stl(parts[key], str(out / "stl" / f"{fname}.stl"), tolerance=0.3, angular_tolerance=0.3)
    sb = _comp(parts["stem"], parts["handlebar"])
    export_step(sb, str(out / "step" / "stem-and-bar.step"))
    export_stl(sb, str(out / "stl" / "stem-and-bar.stl"), tolerance=0.3, angular_tolerance=0.3)
    d = derived()
    print(f"saddle height range {d['saddle_min']:.0f} to {d['saddle_max']:.0f} mm; "
          f"standover {d['standover']:.0f} mm; trail {d['trail']:.0f} mm")
    print("exported STEP and STL to cad/step and cad/stl")
