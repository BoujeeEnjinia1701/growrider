"""GrowRider parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    growrider-small.step / .stl    whole bike set for the smallest rider (1.10 m)
    growrider-large.step / .stl    whole bike set for the largest rider (1.65 m)
    frame.step, fork.step, seat-post-assembly.step, stem-and-bar.step, rack.step (and .stl)

Axes: X along the bike (rear axle at x = 0, front toward +X), Z up with the ground
at z = 0, Y lateral. The drive side (chain) is at -Y.

Main dimensions and interfaces only: wheel size and wheelbase, bottom bracket
position, seat and steering axes, the two-stage telescoping seat post (outer
seat tube, sleeve, post), the long quill stem in the 1 in steerer, the rack
platform and the brake mounts. Not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (GRR-CAL-001).
"""
from math import atan2, cos, degrees, radians, sin, sqrt
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
    "ht_bot": 285.0, "ht_len": 180.0,
    "headset_top_stack": 30.0,   # upper cup, washer and locknut above the head tube
    "ht_od": 34.0, "ht_wall": 1.5,
    # seat tube and two-stage telescoping seat post
    "seat_ang": 70.0,
    "st_len": 280.0,             # bottom bracket center to top of seat tube, along the seat axis
    "st_od": 31.8, "st_wall": 1.5,
    "st_blocked": 40.0,          # bottom of the seat tube bore lost to the BB shell
    "sleeve_od": 28.6, "sleeve_wall": 1.5, "sleeve_len": 250.0,
    "sleeve_exp_min": 20.0, "sleeve_exp_max": 150.0,
    "post_od": 25.4, "post_wall": 1.8, "post_len": 280.0,
    "post_exp_min": 40.0, "post_exp_max": 180.0,
    "saddle_stack": 60.0,        # top of post to top of saddle
    "saddle_rail": 15.0,         # fore-aft rail adjustment, each way
    "min_insert": 100.0,         # minimum insertion at every sliding joint (R2)
    # long quill stem in the 1 in threaded steerer, two-position head
    "quill_d": 22.2, "quill_wall": 2.0, "quill_travel": 120.0, "quill_exp_min": 15.0,
    "stem_ext": (0.0, 60.0), "stem_rise": 10.0,
    # swept-back handlebar
    "bar_d": 22.2, "bar_width": 520.0, "bar_sweep": 160.0, "bar_rise": 25.0,
    # other frame tubes (OD, wall)
    "down": (31.8, 1.4), "loop": (28.6, 1.4), "chainstay_tube": (19.0, 1.2), "seatstay_tube": (16.0, 1.2),
    "loop_t": 380.0, "loop_s": 120.0,    # loop tube ends: on the steering axis and on the seat axis
    "down_t": 300.0,                     # down tube top end on the steering axis
    "ss_s": 260.0,                       # seat stay top on the seat axis
    "bb_shell": (40.0, 3.0, 68.0),       # OD, wall, width
    "stand_ahead": 100.0,                # stepping point: this far ahead of the loop tube's seat-tube joint
    # drive
    "crank": 140.0, "ring_t": 32, "cog_t": 18, "chain_pitch": 12.7, "chain_y": -48.0,
    # rack: platform over the rear wheel, rated 10 kg
    "rack_len": 300.0, "rack_w": 120.0, "rack_z": 575.0, "rack_x0": -85.0, "rack_tube": 12.0,
    # fenders
    "fender_gap": 16.0,
}

# Rider settings used for the exported assemblies (saddle height from BB center to
# saddle top along the seat axis; stem exposure above the steerer; stem head extension).
SETTINGS = {
    "small": {"saddle_h": 400.0, "stem_exp": 15.0, "ext": 0.0},
    "large": {"saddle_h": 670.0, "stem_exp": 135.0, "ext": 60.0},
}


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
    d["quill_len"] = d["steerer_usable"] + P["quill_exp_min"]          # quill below the clamp axis
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
    # stepping point on the loop tube (top surface)
    a = seat_pt(P["loop_s"], P, d)
    b = steer_pt(P["loop_t"], P, d)
    xs = a[0] + P["stand_ahead"]
    zs = a[1] + (b[1] - a[1]) * (xs - a[0]) / (b[0] - a[0])
    ang = atan2(b[1] - a[1], b[0] - a[0])
    d["standover"] = zs + P["loop"][0] / 2 / cos(ang)
    d["stand_x"] = xs
    # fork crown to tire clearance (radial from the front axle)
    c = steer_pt(P["crown_t"], P, d)
    d["crown_pt"] = c
    d["crown_clear"] = sqrt((c[0] - P["wheelbase"]) ** 2 + (c[1] - R) ** 2) - R - 11.0
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
    """Grip center (x, z) for a stem exposure above the steerer and a stem head extension."""
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


# ---------------------------------------------------------------- geometry

def _tube(p1, p2, r):
    from build123d import Plane, Solid, Vector
    p1, p2 = Vector(*p1), Vector(*p2)
    v = p2 - p1
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v.normalized()))


def _xz(p, y=0.0):
    return (p[0], y, p[1])


def _ring_y(c, r_out, r_in, width, y=0.0):
    from build123d import Plane, Solid
    pl = Plane(origin=(c[0], y - width / 2, c[1]), z_dir=(0, 1, 0))
    return Solid.make_cylinder(r_out, width, pl) - Solid.make_cylinder(r_in, width, pl)


def _disc_y(c, r, width, y=0.0):
    from build123d import Plane, Solid
    return Solid.make_cylinder(r, width, Plane(origin=(c[0], y - width / 2, c[1]), z_dir=(0, 1, 0)))


def _comp(*shapes):
    from build123d import Compound
    return Compound(children=list(shapes))


def build_parts(P=PARAMS, setting="large"):
    """Return [(key, name, shape, bom_no)] for the assembly at a rider setting."""
    from math import pi
    from build123d import Box, Cylinder, Plane, Pos, Solid
    S = SETTINGS[setting] if isinstance(setting, str) else setting
    d = derived(P)
    R = d["R"]
    rear, front = (0.0, R), (P["wheelbase"], R)
    bb = (d["bb_x"], P["bb_z"])
    st = lambda s: seat_pt(s, P)
    sr = lambda t: steer_pt(t, P)

    # 1 Frame: head tube, seat tube, down tube, loop tube (the twin down tubes), BB shell, stays
    ht = _tube(_xz(sr(P["ht_bot"])), _xz(sr(d["ht_top"])), P["ht_od"] / 2)
    seat_tube = _tube(_xz(bb), _xz(st(P["st_len"])), P["st_od"] / 2)
    down = _tube(_xz(sr(P["down_t"])), _xz(bb), P["down"][0] / 2)
    loop = _tube(_xz(sr(P["loop_t"])), _xz(st(P["loop_s"])), P["loop"][0] / 2)
    od, _, w = P["bb_shell"]
    shell = _disc_y(bb, od / 2, w)
    cs = [_tube((bb[0], s * 25, bb[1]), (0, s * 55, R), P["chainstay_tube"][0] / 2) for s in (-1, 1)]
    ss = [_tube((st(P["ss_s"])[0], s * 18, st(P["ss_s"])[1]), (0, s * 55, R), P["seatstay_tube"][0] / 2)
          for s in (-1, 1)]
    drop = [Pos(0, s * 55, R) * Box(40, 5, 40) for s in (-1, 1)]
    frame = _comp(ht, seat_tube, down, loop, shell, *cs, *ss, *drop)

    # 2 Fork: crown, blades to the front axle, 1 in steerer up to the locknut
    c = sr(P["crown_t"] - 11)
    crown = Pos(c[0], 0, c[1]) * Box(40, 110, 22)
    blades = [_tube((c[0], s * 45, c[1]), (front[0], s * 50, R), 10) for s in (-1, 1)]
    steerer = _tube(_xz(sr(P["crown_t"])), _xz(sr(d["steerer_top"])), 12.7)
    cups = [_tube(_xz(sr(P["ht_bot"] - 10)), _xz(sr(P["ht_bot"])), 18),
            _tube(_xz(sr(d["ht_top"])), _xz(sr(d["steerer_top"])), 16)]
    fork = _comp(crown, *blades, steerer, *cups)

    # 3 Telescoping seat post: sleeve in the seat tube, post in the sleeve (shown at the setting)
    sl_exp, po_exp = split_saddle(S["saddle_h"], P)
    sleeve_top = P["st_len"] + sl_exp
    post_top = sleeve_top + po_exp
    sleeve = _tube(_xz(st(sleeve_top - P["sleeve_len"])), _xz(st(sleeve_top)), P["sleeve_od"] / 2)
    collar = [_tube(_xz(st(P["st_len"] - 12)), _xz(st(P["st_len"])), P["st_od"] / 2 + 3),
              _tube(_xz(st(sleeve_top - 12)), _xz(st(sleeve_top)), P["sleeve_od"] / 2 + 3)]
    post = _tube(_xz(st(post_top - P["post_len"])), _xz(st(post_top)), P["post_od"] / 2)
    seatpost = _comp(sleeve, *collar, post)

    # 4 Saddle
    sp = st(post_top + P["saddle_stack"])
    saddle = Pos(sp[0] + 15, 0, sp[1] - P["saddle_stack"] / 2) * Box(220, 125, P["saddle_stack"])

    # 5 Telescoping stem (quill plus head) and 6 handlebar
    t_clamp = d["steerer_top"] + S["stem_exp"]
    q_top = sr(t_clamp)
    quill = _tube(_xz(sr(t_clamp - d["quill_len"])), _xz(q_top), P["quill_d"] / 2)
    clamp = (q_top[0] + S["ext"], q_top[1] + P["stem_rise"])
    head = _tube(_xz(q_top), _xz(clamp), 14) if S["ext"] > 0 else Pos(clamp[0], 0, clamp[1]) * Box(40, 45, 30)
    stem = _comp(quill, head)
    gx, gz = clamp[0] - P["bar_sweep"], clamp[1] + P["bar_rise"]
    hw = P["bar_width"] / 2
    br = P["bar_d"] / 2
    bar = [_tube((clamp[0], -110, clamp[1]), (clamp[0], 110, clamp[1]), br)]
    for s in (-1, 1):
        bar.append(_tube((clamp[0], s * 110, clamp[1]), (gx + 40, s * (hw - 110), gz), br))
        bar.append(_tube((gx + 40, s * (hw - 110), gz), (gx - 10, s * hw, gz), 15))  # grip
    handlebar = _comp(*bar)

    # 7, 8 Wheels (rim, hub, spokes); rear has the coaster brake hub and reaction arm
    def wheel(cen, hub_r, hub_w):
        rim = _ring_y(cen, P["rim_r"] + 6, P["rim_r"] - 14, 26)
        hub = _disc_y(cen, hub_r, hub_w)
        axle = _disc_y(cen, 6, 140)
        spokes = []
        for i in range(18):
            a = 2 * pi * i / 18
            side = 1 if i % 2 else -1
            ph = (cen[0] + hub_r * cos(a), side * hub_w * 0.4, cen[1] + hub_r * sin(a))
            pr = (cen[0] + (P["rim_r"] - 14) * cos(a + 0.35), 0, cen[1] + (P["rim_r"] - 14) * sin(a + 0.35))
            spokes.append(_tube(ph, pr, 1.6))
        return _comp(rim, hub, axle, *spokes)

    front_wheel = wheel(front, 22, 80)
    rear_wheel = _comp(wheel(rear, 32, 110), _tube((0, 50, R), (140, 50, R + 5), 6))

    # 9 Tires, 20 x 1.95 in solid or airless
    tires = _comp(*[Solid.make_torus(R - P["tire_sec_r"], P["tire_sec_r"], Plane(origin=(cx, 0, cz), z_dir=(0, 1, 0)))
                    for cx, cz in (rear, front)])

    # 10 Crankset and pedals, 11 chain and sprocket
    yc = P["chain_y"]
    ring_r = P["chain_pitch"] / (2 * sin(pi / P["ring_t"]))
    cog_r = P["chain_pitch"] / (2 * sin(pi / P["cog_t"]))
    ca = radians(20)
    cv = (P["crank"] * cos(ca), P["crank"] * sin(ca))
    ring = _ring_y(bb, ring_r + 4, ring_r - 18, 4, y=yc)
    crank_r = _tube((bb[0], yc - 8, bb[1]), (bb[0] + cv[0], yc - 8, bb[1] + cv[1]), 8)
    crank_l = _tube((bb[0], 58, bb[1]), (bb[0] - cv[0], 58, bb[1] - cv[1]), 8)
    spindle = _disc_y(bb, 8, 130)
    pedals = [Pos(bb[0] + cv[0], yc - 60, bb[1] + cv[1]) * Box(80, 90, 22),
              Pos(bb[0] - cv[0], 110, bb[1] - cv[1]) * Box(80, 90, 22)]
    crankset = _comp(ring, crank_r, crank_l, spindle, *pedals)
    cog = _ring_y(rear, cog_r + 3, 18, 4, y=yc)
    runs = [_tube((bb[0], yc, bb[1] + s * ring_r), (0, yc, R + s * cog_r), 4) for s in (-1, 1)]
    chain = _comp(cog, *runs)

    # 12 Front rim brake (caliper below the crown) and lever on the right grip
    caliper = _comp(Pos(c[0] + 8, 0, c[1] - 4) * Box(30, 90, 10),
                    *[Pos(c[0] + 8, s * 38, c[1] - 40) * Box(22, 8, 64) for s in (-1, 1)])
    lever = _tube((gx + 20, -(hw - 20), gz), (gx - 25, -(hw - 90), gz - 10), 5)
    front_brake = _comp(caliper, lever)

    # 13 Rear rack: 300 x 120 mm platform, three rails, struts to the dropouts and stays to the seat stays
    rz, x0, x1 = P["rack_z"], P["rack_x0"], P["rack_x0"] + P["rack_len"]
    rw, rt = P["rack_w"] / 2, P["rack_tube"] / 2
    rails = [_tube((x0, s * rw, rz), (x1, s * rw, rz), rt) for s in (-1, 0, 1)]
    cross = [_tube((x, -rw, rz), (x, rw, rz), rt - 1) for x in (x0, (x0 + x1) / 2, x1)]
    struts = [_tube((x0 + 5, s * rw, rz), (0, s * (rw + 2), R + 10), rt) for s in (-1, 1)]
    ssx = st(P["ss_s"] - 60)
    stays = [_tube((x1 - 5, s * rw, rz), (ssx[0] * 0.55, s * 30, R + (ssx[1] - R) * 0.55), rt - 2) for s in (-1, 1)]
    rack = _comp(*rails, *cross, *struts, *stays)

    # 14 Fenders
    def fender(cen, keep):
        return _ring_y(cen, R + P["fender_gap"] + 4, R + P["fender_gap"], 64) & keep
    fenders = _comp(fender(rear, Pos(-40, 0, R + 250) * Box(700, 200, 500)),
                    fender(front, Pos(P["wheelbase"] + 20, 0, R + 250) * Box(620, 200, 500)))

    # 15 Chainguard over the upper chain run
    mid = ((bb[0]) / 2, (bb[1] + R) / 2)
    chainguard = Pos(mid[0] + 30, yc - 16, mid[1] + 50) * Box(440, 3, 45)

    # 16 Kickstand, rear-mounted, shown down
    kickstand = _tube((120, 20, P["bb_z"] - 2), (190, 110, 8), 7)

    # 17 Reflectors and bell
    refl = [Pos(x0 - 12, 0, rz - 40) * Box(8, 70, 40),
            Pos(clamp[0] + 25, 0, clamp[1] - 25) * Box(8, 60, 35),
            Pos(clamp[0] - 20, 100, clamp[1] + 20) * Cylinder(22, 16)]
    refl += [Pos(cx + 120, 0, cz + 60) * Box(50, 10, 20) for cx, cz in (rear, front)]
    reflectors = _comp(*refl)

    return [
        ("frame", "Step-through steel frame", frame, 1),
        ("fork", "Fork, 1 in steerer", fork, 2),
        ("seatpost", "Telescoping seat post (sleeve and post)", seatpost, 3),
        ("saddle", "Saddle", saddle, 4),
        ("stem", "Telescoping quill stem", stem, 5),
        ("handlebar", "Handlebar and grips", handlebar, 6),
        ("front_wheel", "Front wheel, 20 in", front_wheel, 7),
        ("rear_wheel", "Rear wheel, coaster brake hub", rear_wheel, 8),
        ("tires", "Solid tires, 20 x 1.95 in (2)", tires, 9),
        ("crankset", "Crankset, 32T, 140 mm", crankset, 10),
        ("chain", "Chain and 18T sprocket", chain, 11),
        ("front_brake", "Front rim brake and lever", front_brake, 12),
        ("rack", "Rear rack, 10 kg rated", rack, 13),
        ("fenders", "Fenders", fenders, 14),
        ("chainguard", "Chainguard", chainguard, 15),
        ("kickstand", "Kickstand", kickstand, 16),
        ("reflectors", "Reflectors and bell", reflectors, 17),
    ]


def build(P=PARAMS, setting="large"):
    return _comp(*[s for _, _, s, _ in build_parts(P, setting)])


def tube_lengths(P=PARAMS):
    """Center-line lengths (mm) of the frame tubes, for the mass estimate in GRR-CAL-001."""
    d = derived(P)
    bb = (d["bb_x"], P["bb_z"])
    dist = lambda a, b: sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    R = d["R"]
    ss_top = seat_pt(P["ss_s"], P)
    return {
        "head": P["ht_len"],
        "seat": P["st_len"],
        "down": dist(steer_pt(P["down_t"], P), bb),
        "loop": dist(steer_pt(P["loop_t"], P), seat_pt(P["loop_s"], P)),
        "chainstay": 2 * sqrt(P["chainstay"] ** 2 + 30 ** 2),
        "seatstay": 2 * sqrt(dist(ss_top, (0, R)) ** 2 + 37 ** 2),
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    for setting in ("small", "large"):
        asm = build(setting=setting)
        export_step(asm, str(out / "step" / f"growrider-{setting}.step"))
        export_stl(asm, str(out / "stl" / f"growrider-{setting}.stl"))
    parts = {k: s for k, _, s, _ in build_parts(setting="large")}
    for key, fname in [("frame", "frame"), ("fork", "fork"), ("seatpost", "seat-post-assembly"),
                       ("rack", "rack")]:
        export_step(parts[key], str(out / "step" / f"{fname}.step"))
        export_stl(parts[key], str(out / "stl" / f"{fname}.stl"))
    sb = _comp(parts["stem"], parts["handlebar"])
    export_step(sb, str(out / "step" / "stem-and-bar.step"))
    export_stl(sb, str(out / "stl" / "stem-and-bar.stl"))
    d = derived()
    print(f"saddle height range {d['saddle_min']:.0f} to {d['saddle_max']:.0f} mm; "
          f"standover {d['standover']:.0f} mm; trail {d['trail']:.0f} mm")
    print("exported STEP and STL to cad/step and cad/stl")
