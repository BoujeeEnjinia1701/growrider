"""GrowRider prototype build plan pictures (GRR-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layout|joints|steps ...]
With no argument it draws everything; a step or joint number after its group draws only that one
(for example: steps 3). Every picture is drawn from cad/src/model.py (build_components), so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/GRR-DWG-101 to 108        making sketches for the made components
    docs/05-build-plan/frame-layout.png    frame jig layout: tube center lines and key points
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from math import cos, radians, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, build_components, derived, seat_pt, steer_pt, seatstay_pt, chainstay_pt,  # noqa: E402
                   split_saddle, _bridge_f, _rack_boss_f, _axis_plane, _comp)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
R = D["R"]
MID = {"saddle_h": 537.0, "stem_exp": 75.0, "ext": 45.0}      # a 1.38 m rider, as in the concept media
C = build_components(P, MID)
S = lambda *ks: _comp(*[C[k].shape for k in ks])  # noqa: E731

COL = {"frame": "#0F766E", "bb": "#57534E", "headset": "#374151", "fork": "#115E59", "sleeve": "#6B7280",
       "collars": "#1D4ED8", "post": "#9CA3AF", "saddle": "#A16207", "quill": "#475569", "block": "#7C3AED",
       "bar": "#4B5563", "ffender": "#334155", "caliper": "#D4A017", "tires": "#262626", "fwheel": "#94A3B8",
       "crank": "#57534E", "rwheel": "#94A3B8", "chain": "#C2410C", "clip": "#1D4ED8", "rfender": "#334155",
       "rack": "#B45309", "guard": "#64748B", "kick": "#57534E", "refl": "#DC2626", "bolt": "#111827"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def along(axis_ang, k):
    """Offset of k mm along an axis tilted back axis_ang degrees from horizontal (seat or steering axis)."""
    a = radians(axis_ang)
    return (-k * cos(a), 0, k * sin(a))


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "frame": part("Frame, with its dropouts and fittings", C["frame"].shape, COL["frame"]),
        "bb": part("Bottom bracket", C["bb"].shape, COL["bb"]),
        "headset": part("Headset", C["headset"].shape, COL["headset"]),
        "fork": part("Fork", C["fork"].shape, COL["fork"]),
        "sleeve": part("Seat post sleeve", C["sleeve"].shape, COL["sleeve"]),
        "collars": part("Collars and stop screws (2)", S("st_collar", "st_screws", "sl_collar", "sl_screws"), COL["collars"]),
        "post": part("Seat post, slotted", C["post"].shape, COL["post"]),
        "saddle": part("Saddle", C["saddle"].shape, COL["saddle"]),
        "quill": part("Quill stem with head plate", S("quill", "exp_bolt", "head_plate"), COL["quill"]),
        "block": part("Bar clamp block and bolts", S("clamp_lo", "clamp_hi", "clamp_bolts"), COL["block"]),
        "bar": part("Handlebar, grips, brake lever", S("handlebar", "grips", "lever"), COL["bar"]),
        "ffender": part("Front fender and stays", _comp(C["ffender"].shape, _ffstays()), COL["ffender"]),
        "caliper": part("Front brake caliper", S("caliper", "brake_bolt"), COL["caliper"]),
        "tires": part("Solid tires (2)", C["tires"].shape, COL["tires"]),
        "fwheel": part("Front wheel", C["front_wheel"].shape, COL["fwheel"]),
        "crank": part("Crankset and pedals", S("crankset", "pedals"), COL["crank"]),
        "rwheel": part("Rear wheel, sprocket, brake arm", S("rear_wheel", "cog", "arm"), COL["rwheel"]),
        "chain": part("Chain", C["chain"].shape, COL["chain"]),
        "clip": part("Brake arm clip", C["arm_clip"].shape, COL["clip"]),
        "rfender": part("Rear fender and stays", _comp(C["rfender"].shape, _rfstays()), COL["rfender"]),
        "rack": part("Rack", S("rack", "rack_plate"), COL["rack"]),
        "guard": part("Chainguard and mounts", S("chainguard", "guard_mounts"), COL["guard"]),
        "kick": part("Kickstand", S("kickstand", "kick_bolt"), COL["kick"]),
        "refl": part("Reflectors and bell", C["reflectors"].shape, COL["refl"]),
    }


def _split_stays():
    """The fender stays and brackets part holds both fenders' pieces; split them by x."""
    rear, front = [], []
    for s in C["fender_stays"].shape.solids():
        (front if s.center().X > P["wheelbase"] / 2 else rear).append(s)
    return _comp(*rear), _comp(*front)


def _rfstays():
    return _split_stays()[0]


def _ffstays():
    return _split_stays()[1]


ORDER = ["frame", "bb", "headset", "fork", "sleeve", "collars", "post", "saddle", "quill", "block", "bar",
         "ffender", "caliper", "tires", "fwheel", "crank", "rwheel", "chain", "clip", "rfender", "rack",
         "guard", "kick", "refl"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    sa, ha = P["seat_ang"], P["head_ang"]
    off = {"frame": (0, 0, 0), "bb": (130, 0, -440), "headset": (90, 0, 260), "fork": (380, 0, -200),
           "sleeve": along(sa, 300), "collars": along(sa, 470), "post": along(sa, 640), "saddle": along(sa, 900),
           "quill": tuple(a + b for a, b in zip(along(ha, 420), (160, 0, 0))),
           "block": tuple(a + b for a, b in zip(along(ha, 560), (260, 0, 0))),
           "bar": tuple(a + b for a, b in zip(along(ha, 680), (330, 0, 0))),
           "ffender": (640, 0, 420), "caliper": (560, 0, 180), "tires": (0, 0, -820), "fwheel": (760, 0, -60),
           "crank": (380, 0, -330), "rwheel": (-640, 0, -120), "chain": (-40, 0, -300), "clip": (0, 330, -260),
           "rfender": (-360, 0, 560), "rack": (-180, 0, 330), "guard": (40, 0, -150), "kick": (-200, 0, -380),
           "refl": (-260, 0, 1020)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "GrowRider prototype: every component, pulled apart",
                       subtitle="Numbered in build order; the bike is set for a 1.38 m rider. Seen from the front right (drive side) and above",
                       elev=14, azim=-62, size=(13, 9), dpi=140, key=True)


# ----------------------------------------------------------------- making sketches
def _flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="GrowRider", date=DATE)
    out = []
    sa = radians(P["seat_ang"])
    axis = (-cos(sa), 0, sin(sa))
    bbp = (D["bb_x"], P["bb_z"])

    def want(n):
        return only is None or n in only

    # 101 rear track-end dropout (the left one, seen from outside)
    if want(101):
        dl = _drop_left()
        out.append(bv.component_sheet(
            Part("Rear dropout", dl, COL["frame"]), [M["rwheel"], part("", _rear_end(), COL["frame"])],
            dwg_no="GRR-DWG-101", title="GrowRider rear track-end dropout (make 2, a left and a right): making sketch",
            material="Steel plate 6 mm (S235 or 4130)", view_shape=b.Pos(0, -D["drop_y"], -R) * dl, inset_view=(15, 65),
            notes=["Make two, mirror images. Mark out on 6 mm steel plate; positions are",
                   "  from the axle center (the middle of the slot's round end is 3 mm ahead).",
                   "Outline: 82 long, from 30 behind to 52 ahead of the axle; 54 tall,",
                   "  from 16 below to 38 above it. Saw and file; break every edge.",
                   "Axle slot 10 wide, open to the rear, round end 3 mm ahead of the axle:",
                   "  drill 10 mm at the round end, saw the two sides, file parallel.",
                   "Eyelet: 5.5 mm hole 18 behind and 20 above the axle (rack and fender).",
                   "Fit: the chainstay end (40 ahead, 1 above the axle) and the seat stay",
                   "  end (16 ahead, 20 above) are slotted 6 mm and brazed over the plate.",
                   "The inner faces sit 110 apart for the coaster hub. The axle slides",
                   "  back in the slot to tension the chain.",
                   "Check: a 3/8 in axle slides the length of the slot without binding."],
            **base))

    # 102 frame
    if want(102):
        out.append(bv.component_sheet(
            Part("Frame", C["frame"].shape, COL["frame"]), [M["fork"], M["sleeve"], M["rwheel"], M["fwheel"]],
            dwg_no="GRR-DWG-102", title="GrowRider frame: making sketch", material="Chromoly 4130 main tubes; steel stays and fittings",
            view_shape=b.Pos(-D["bb_x"], 0, -P["bb_z"]) * C["frame"].shape, inset_view=(14, -62),
            notes=["Built on a flat jig to the frame layout (build plan Figure 5).",
                   "Head tube 34 x 2.0, 180 long (30.0 bore). Seat tube 31.8 x 1.2,",
                   "  280 long. Down tube 31.8 x 0.9. Loop tube 28.6 x 0.9. Both axes 70 deg.",
                   "Chainstays 19 x 1.2 steel, 21 each side of center at the BB.",
                   "Seat stays 16 x 1.2 steel onto a 16 mm cross bar 25 behind the seat",
                   "  tube, 235 up the seat axis; stays 40 each side of center there.",
                   "Mitre every tube to the tube it meets; braze or TIG. Then ream the seat",
                   "  tube to 29.4 and the head tube to 30.0, face the BB shell and cups.",
                   "Seat tube top: 2 x 26 slit at the back; M5 stop hole on the left,",
                   "  7 below the top. Fittings: 12 mm bridge for the rear fender, 4 mm",
                   "  kickstand plate 55 behind the BB, M5 bosses (rack, chainguard).",
                   "Check: dropouts 110 apart and level; frame flat on the jig within 1 mm."],
            **base))

    # 103 seat post sleeve, laid flat with the slot toward the viewer
    pl_bot = seat_pt(P["st_len"] + split_saddle(MID["saddle_h"])[0] - P["sleeve_len"])
    if want(103):
        sl = _flat(C["sleeve"].shape, (pl_bot[0], 0, pl_bot[1]), axis, (0, 1, 0))
        out.append(bv.component_sheet(
            Part("Seat post sleeve", C["sleeve"].shape, COL["sleeve"]), [M["frame"], M["post"], M["collars"]],
            dwg_no="GRR-DWG-103", title="GrowRider seat post sleeve: making sketch", material="Chromoly 4130 tube 29.2 x 1.8 mm",
            view_shape=sl, inset_view=(14, 55),
            notes=["Cut 250 long from 29.2 x 1.8 chromoly tube; square and deburr both ends.",
                   "Check it slides in the reamed seat tube (29.4) and the post slides in it.",
                   "Stop slot, left side: 6 wide, from 90 to 226 up from the bottom end.",
                   "  Chain drill 6 mm along a scribed line and file the sides straight;",
                   "  its two ends are the stops, so file them square.",
                   "Top end: a 2 mm slit 26 long at the back, so the sleeve collar closes it;",
                   "  an M5 clearance hole (5.5) on the right side, 7 below the top, for the",
                   "  post's stop screw.",
                   "Scribe the minimum insertion mark all round, 100 up from the bottom.",
                   "Fit: goes into the seat tube slot-side left; the seat tube collar's",
                   "  stop screw rides in the slot. 100 stays inside at the top stop.",
                   "Check: slot ends square; no burr inside the bore."],
            **base))

    # 104 collars: the seat tube collar (and the sleeve collar, the same at 29.8)
    if want(104):
        pst = _axis_plane(seat_pt(P["st_len"] - P["collar_h"]), P["seat_ang"])
        col = pst.to_local_coords(_comp(C["st_collar"].shape, C["st_screws"].shape))
        out.append(bv.component_sheet(
            Part("Collar with stop screw", _comp(C["st_collar"].shape, C["st_screws"].shape), COL["collars"]),
            [M["frame"], M["sleeve"], M["post"]],
            dwg_no="GRR-DWG-104", title="GrowRider clamp collars with stop screws (make 2): making sketch",
            material="Bought steel clamp collars, 31.8 and 29.8 mm, with M8 bolts", view_shape=col, inset_view=(14, 55),
            notes=["Two bought bolt-up clamp collars: 31.8 mm for the seat tube and",
                   "  29.8 mm for the sleeve (it closes onto the 29.2 sleeve).",
                   "Drill and tap one radial M5 hole in each, square to the bore, half way",
                   "  up (7 below the top), a quarter turn from the clamp bolt.",
                   "Seat tube collar: hole on the LEFT. Sleeve collar: hole on the RIGHT.",
                   "Stop screws: M5 x 10 with a dog point. Seat tube one: grind its tip so",
                   "  it enters the sleeve slot 1.5 mm and never touches the post.",
                   "Sleeve one: tip enters the post slot about 1.5 mm.",
                   "Fit: each collar sits flush with the top of its tube, slit at the back,",
                   "  its stop hole lined up with the hole in the tube under it.",
                   "Check: with the screw in, the part inside slides to both slot ends",
                   "  and stops; the collar bolt closes the tube without the screw binding."],
            **base))

    # 105 seat post, slotted (bought post)
    if want(105):
        post_bot = seat_pt(P["st_len"] + sum(split_saddle(MID["saddle_h"])) - P["post_len"])
        po = _flat(C["post"].shape, (post_bot[0], 0, post_bot[1]), axis, (0, -1, 0))
        out.append(bv.component_sheet(
            Part("Seat post", C["post"].shape, COL["post"]), [M["sleeve"], M["saddle"], M["collars"]],
            dwg_no="GRR-DWG-105", title="GrowRider seat post, slotted: making sketch", material="Bought steel seat post 25.4 x 1.8 mm, 280 mm",
            view_shape=po, inset_view=(14, 55),
            notes=["Bought plain 25.4 mm steel post with a top saddle clamp, cut to 280.",
                   "Stop slot on the right (chain) side: 6 wide, from 90 to 236 up from",
                   "  the bottom end.",
                   "Chain drill 6 mm along a scribed line, file straight, ends square.",
                   "The slot lies on the side of the post, where fore-and-aft bending",
                   "  stress is lowest; it lowers the post's stiffness by under 1 %.",
                   "Scribe the minimum insertion mark all round, 100 up from the bottom.",
                   "Fit: slides in the sleeve, slot to the right; the sleeve collar's stop",
                   "  screw rides in it. 100 stays inside the sleeve at the top stop.",
                   "Check: the slot is straight along the post (the saddle stays",
                   "  pointing forward because the screw keys it)."],
            **base))

    # 106 quill with its head plate (welded assembly)
    if want(106):
        q = S("quill", "head_plate")
        qt = steer_pt(D["steerer_top"] + MID["stem_exp"])
        out.append(bv.component_sheet(
            Part("Quill stem", q, COL["quill"]), [M["frame"], M["fork"], M["block"], M["bar"], M["headset"]],
            dwg_no="GRR-DWG-106", title="GrowRider quill stem with head plate: making sketch",
            material="Chromoly 4130 tube 22.0 x 2.0 mm; 4130 plate 10 mm", view_shape=b.Pos(-qt[0], 0, -qt[1]) * q, inset_view=(18, -40),
            notes=["Quill: cut 240 from 22.0 x 2.0 chromoly tube. Weld a 3 mm steel cap",
                   "  in the top with an 8.5 hole; fit the bought expander wedge at the",
                   "  bottom with the M8 x 260 expander bolt (13 mm head on the cap).",
                   "Head plate: 127 x 44 x 10, 4130. Cope one end to the quill's 22 curve.",
                   "  Drill 6.8 and tap M8, eight holes: at 27, 63, 87 and 123 ahead of",
                   "  the quill's center line, 13 each side of the plate's center line.",
                   "Weld the plate square across the quill's front, its top flush with",
                   "  the quill top and level when the quill leans back 20 deg (use a",
                   "  70 deg jig block). TIG both sides.",
                   "Scribe the minimum insertion mark 100 up from the quill's bottom.",
                   "Check: the quill slides in the 22.2 bore of the steerer; the plate",
                   "  clears the headset locknut by 2 mm at the lowest setting."],
            **base))

    # 107 bar clamp block
    if want(107):
        blk = S("clamp_lo", "clamp_hi")
        bc = C["clamp_lo"].shape.bounding_box().center()
        out.append(bv.component_sheet(
            Part("Bar clamp block", blk, COL["block"]), [M["quill"], M["bar"], M["fork"]],
            dwg_no="GRR-DWG-107", title="GrowRider bar clamp block (two halves): making sketch",
            material="Aluminium 6061-T6 flat bar 45 x 30 mm (or 50 x 30)", view_shape=b.Pos(-bc.X, -bc.Y, -bc.Z - 7.5) * blk, inset_view=(22, -40),
            notes=["Saw 56 long from 45 x 30 flat bar; file or mill to 54 x 44 x 30.",
                   "Drill the bar hole across the 44 width at mid-length, 15 up from",
                   "  the bottom: pilot, then 22 mm, then ream 22.2 (or bore it).",
                   "Drill four 8.5 holes straight through, 18 each side of the bar hole",
                   "  and 13 each side of the middle.",
                   "Saw the block in half along the bar hole's center line; file the",
                   "  two sawn faces flat so the halves clamp the bar with a 1 mm gap.",
                   "Break every edge, especially round the bar hole.",
                   "Fit: the lower half sits on the head plate over one of the two hole",
                   "  sets; the cap goes on over the bar; four M8 x 40 bolts (13 mm",
                   "  heads) go through both halves into the tapped plate.",
                   "Check: the bar turns in the closed clamp only with a firm twist."],
            **base))

    # 108 rack
    if want(108):
        rk = C["rack"].shape
        out.append(bv.component_sheet(
            Part("Rack", rk, COL["rack"]), [M["frame"], M["rwheel"], M["rfender"], M["sleeve"], M["post"], M["saddle"]],
            dwg_no="GRR-DWG-108", title="GrowRider rear rack (rated 10 kg): making sketch",
            material="Aluminium 6061-T6 tube 12 x 1.5 mm; 3 mm 6061 tabs", view_shape=b.Pos(-P["rack_x0"], 0, -P["rack_z"]) * rk,
            inset_view=(20, -125),
            notes=["Platform 300 x 120: three rails 300 long (center and both sides) and",
                   "  three cross bars 120 long, at both ends and the middle.",
                   "Struts: one from each rear corner down to the dropout eyelet",
                   "  (about 300 long); flatten 30 at the end and weld on a 3 mm tab.",
                   "Stays: one from each front corner down to the boss on the seat stay",
                   "  (about 120 long), with a 3 mm tab at the end.",
                   "Drill each tab 5.5 for an M5 bolt. Weld with the rack in a jig",
                   "  taken off the frame so the tabs land on the eyelets and bosses.",
                   "Rating plate across the rear: 'MAX 10 kg', with the rear reflector.",
                   "Platform 545 above the ground, level; it clears the fender by 20,",
                   "  and the saddle by at least 20 at the lowest setting.",
                   "Check: all four tabs sit flat on their eyelets and bosses unforced."],
            **base))
    return out


def _drop_left():
    """The left rear dropout plate on its own, built from the same outline as the model's."""
    import build123d as b
    from model import _plate_xz, _disc_y
    pts = [(-30, R - 14), (-30, R + 30), (-2, R + 30), (24, R + 38), (52, R + 14), (52, R - 12), (36, R - 16)]
    y = D["drop_y"] + P["drop_t"] / 2
    pl = _plate_xz(pts, D["drop_y"], P["drop_t"])
    slot = b.Pos(-14, y, R) * b.Box(34, 20, P["axle_d"] + 0.5) + _disc_y((3, R), (P["axle_d"] + 0.5) / 2, 20, y=y)
    return pl - slot - _disc_y(D["eyelet"], 2.75, 20, y=y)


def _rear_end():
    """The frame's rear end only, for the dropout sketch's inset."""
    return _win(C["frame"].shape, -60, 260, -90, 90, 150, 520)


# ----------------------------------------------------------------- frame jig layout (matplotlib)
def layout():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    bx, bz = D["bb_x"], P["bb_z"]
    rel = lambda p: (p[0] - bx, p[1] - bz)  # noqa: E731
    fig = plt.figure(figsize=(13, 8.6), dpi=140)
    ax = fig.add_axes([0.03, 0.08, 0.66, 0.80]); ax.set_aspect("equal"); ax.set_axis_off()
    tubes = [("Head tube", steer_pt(P["ht_bot"]), steer_pt(D["ht_top"]), P["ht_od"]),
             ("Seat tube", (bx, bz), seat_pt(P["st_len"]), P["st_od"]),
             ("Down tube", steer_pt(P["down_t"]), (bx, bz), P["down"][0]),
             ("Loop tube", steer_pt(P["loop_t"]), seat_pt(P["loop_s"]), P["loop"][0]),
             ("Chainstay", chainstay_pt(1, 1)[::2], chainstay_pt(0, 1)[::2], P["chainstay_tube"][0]),
             ("Seat stay", seatstay_pt(0, 1)[::2], seatstay_pt(1, 1)[::2], P["seatstay_tube"][0])]
    for name, a, b_, od in tubes:
        a, b_ = rel(a), rel(b_)
        ax.plot([a[0], b_[0]], [a[1], b_[1]], color="#99D5CF", lw=od * 0.62, solid_capstyle="butt", zorder=1)
        ax.plot([a[0], b_[0]], [a[1], b_[1]], color=AC, lw=0.8, ls=(0, (8, 3, 2, 3)), zorder=2)
    # BB shell, cross bar, dropout
    ax.add_patch(plt.Circle((0, 0), 20, fc="#99D5CF", ec=AC, lw=0.8, zorder=2))
    xb = rel(D["xbar"])
    ax.add_patch(plt.Circle(xb, 8, fc="#99D5CF", ec=AC, lw=0.8, zorder=2))
    pts = [(-30, -14), (-30, 30), (-2, 30), (24, 38), (52, 14), (52, -12), (36, -16)]
    ax.add_patch(plt.Polygon([(x - bx, z + R - bz) for x, z in pts], closed=True, fc="#CBD5E1", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(plt.Circle((-bx, R - bz), 4.75, fc="white", ec=INK, lw=0.6, zorder=4))
    # key points with coordinates (x forward, z up, from the BB center)
    keys = [("Rear axle", (0.0, R), (-60, -60)),
            ("Head tube bottom", steer_pt(P["ht_bot"]), (70, -70)),
            ("Head tube top", steer_pt(D["ht_top"]), (45, 25)),
            ("Seat tube top", seat_pt(P["st_len"]), (-150, 45)),
            ("Down tube on head axis", steer_pt(P["down_t"]), (-150, -60)),
            ("Loop tube on head axis", steer_pt(P["loop_t"]), (-150, 45)),
            ("Loop tube on seat axis", seat_pt(P["loop_s"]), (130, -30)),
            ("Seat stay cross bar", D["xbar"], (-200, 20)),
            ("Chainstay end", D["cs_end"], (40, -70)),
            ("Seat stay end", D["ss_end"], (-150, 60))]
    for name, p, (dx, dz) in keys:
        x, z = rel(p)
        ax.plot([x], [z], "o", ms=3.5, color="#B45309", zorder=5)
        ax.annotate(f"{name}\n({x:+.0f}, {z:+.0f})", xy=(x, z), xytext=(x + dx, z + dz), fontsize=7.6, color=INK,
                    ha="center", va="center", zorder=6, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5),
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#9CA3AF", lw=0.5))
    ax.plot([0], [0], "+", ms=12, color=INK, zorder=6)
    ax.annotate("BB center (0, 0)", xy=(0, 0), xytext=(60, -95), fontsize=7.6, ha="center", color=INK,
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#9CA3AF", lw=0.5))
    ax.axhline(-bz, color=MUT, lw=0.6)
    ax.text(-bx - 40, -bz + 6, "ground", fontsize=7.5, color=MUT)
    ax.text(rel(steer_pt(D["ht_top"]))[0] - 70, rel(steer_pt(D["ht_top"]))[1] + 70, "head and seat axes 70 deg",
            fontsize=7.5, color=AC)
    ax.set_xlim(-bx - 120, 420); ax.set_ylim(-bz - 20, 520)
    fig.text(0.02, 0.97, "Frame layout for the jig (seen from the drive side)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.935, "Tube center lines (dashed) and key points in mm from the BB center: x forward, z up. "
             "The frame is symmetric about its center plane except the chainguard boss on the drive chainstay.", fontsize=8.5, color=MUT, va="top")
    rows = [("Tube", "Size (mm)", "Center line"),
            ("Head tube", "34 x 2.0 chromoly", f"{P['ht_len']:.0f}"),
            ("Seat tube", "31.8 x 1.2 chromoly", f"{P['st_len']:.0f}"),
            ("Down tube", "31.8 x 0.9 chromoly", f"{_len(steer_pt(P['down_t']), (bx, bz)):.0f}"),
            ("Loop tube", "28.6 x 0.9 chromoly", f"{_len(steer_pt(P['loop_t']), seat_pt(P['loop_s'])):.0f}"),
            ("Chainstays (2)", "19 x 1.2 steel", f"{_len3(chainstay_pt(0, 1), chainstay_pt(1, 1)):.0f}"),
            ("Seat stays (2)", "16 x 1.2 steel", f"{_len3(seatstay_pt(0, 1), seatstay_pt(1, 1)):.0f}"),
            ("Stay cross bar", "16 x 1.2 steel", f"{2 * P['ss_y_top'] + 16:.0f}"),
            ("Fender bridge", "12 x 1.0 steel", f"{2 * abs(seatstay_pt(_bridge_f(), 1)[1]):.0f}"),
            ("BB shell", "68 wide, BSA", "68"),
            ("Dropouts (2)", "6 mm plate", "GRR-DWG-101")]
    y0 = 0.86
    fig.text(0.715, y0 + 0.02, "Tubes (cut 10 long, then mitre to fit the jig)", fontsize=9, fontweight="bold", color=INK)
    for i, (a, b_, c) in enumerate(rows):
        w = "bold" if i == 0 else "normal"
        fig.text(0.715, y0 - i * 0.03, a, fontsize=8, color=INK, fontweight=w)
        fig.text(0.825, y0 - i * 0.03, b_, fontsize=8, color=INK, fontweight=w)
        fig.text(0.955, y0 - i * 0.03, c, fontsize=8, color=INK, fontweight=w, ha="right")
    notes = ["Lateral positions (from the center plane):",
             "  chainstays 21 at the BB, 58 at the dropouts;",
             "  seat stays 40 at the cross bar, 58 at the dropouts;",
             "  dropout inner faces 55 (110 apart).",
             "Kickstand plate 55 behind the BB, under the stays.",
             "Fender bridge where the stays are 292 from the axle.",
             "Rack stay bosses on the seat stays at the rack's front.",
             "Chainguard boss on the drive chainstay, 38 % of the",
             "  way from the dropout to the BB."]
    for i, t in enumerate(notes):
        fig.text(0.715, 0.50 - i * 0.027, t, fontsize=8, color=INK)
    fig.text(0.02, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.98, 0.015, "github.com/BoujeeEnjinia1701/growrider", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "frame-layout.png", facecolor="white"); plt.close(fig)
    return OUT / "frame-layout.png"


def _len(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _len3(a, b):
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5


# ----------------------------------------------------------------- joints
def _win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def joints(only=None):
    out = []
    W = _win
    fr = C["frame"].shape

    def want(n):
        return only is None or n in only

    # 1 left rear dropout from outside: axle, nut, brake arm, rack tab, fender stay
    if want(1):
        bx_ = (-45, 70, 40, 80, R - 30, R + 50)
        out.append(bv.joint([
            part("Dropout (6 mm plate)", W(fr, *bx_), COL["frame"]),
            part("Axle nut on the axle in the slot", W(C["rear_wheel"].shape, *bx_), COL["rwheel"]),
            part("Rack strut tab, outside", W(C["rack"].shape, *bx_), COL["rack"]),
            part("Fender stay eye, under the tab", W(C["fender_stays"].shape, *bx_), "#475569")],
            OUT / "joint-01.png", "Joint 1: left rear dropout, seen from outside",
            subtitle="The axle slides back in the slot to tension the chain. One M5 bolt holds the fender stay and the rack tab on the eyelet",
            elev=8, azim=80, size=(8, 6)))
    # 2 coaster brake arm clip, from below the left chainstay
    if want(2):
        pa = chainstay_pt((135 - D["cs_end"][0]) / (D["bb_x"] - D["cs_end"][0]), 1)
        bx_ = (pa[0] - 45, pa[0] + 45, pa[1] - 25, pa[1] + 25, pa[2] - 45, pa[2] + 20)
        out.append(bv.joint([
            part("Left chainstay", W(fr, *bx_), COL["frame"]),
            part("Coaster brake arm", W(C["arm"].shape, *bx_), COL["rwheel"]),
            part("Arm clip and M6 bolt", W(C["arm_clip"].shape, *bx_), COL["clip"])],
            OUT / "joint-02.png", "Joint 2: coaster brake arm clipped to the left chainstay",
            subtitle="The clip's band goes round the stay, its legs either side of the arm; one M6 bolt under the arm. Seen from outside and below",
            elev=-20, azim=70, size=(8, 6)))
    # 3 seat tube top, cut through the axis across the bike (rear half kept), seen from the front
    def axis_cut(sh, s_mid, half=36):
        import build123d as b
        pl = _axis_plane(seat_pt(s_mid), P["seat_ang"])
        return sh & (pl * b.Pos(-30, 0, 0) * b.Box(60, 90, 2 * half))
    if want(3):
        sm = P["st_len"] - 8
        out.append(bv.joint([
            part("Seat tube, cut open", axis_cut(fr, sm), COL["frame"]),
            part("Sleeve; the screw is in its slot", axis_cut(C["sleeve"].shape, sm), COL["sleeve"]),
            part("Post inside the sleeve", axis_cut(C["post"].shape, sm), COL["post"]),
            part("Seat tube collar", axis_cut(C["st_collar"].shape, sm), COL["collars"]),
            part("Stop screw (M5, dog point)", axis_cut(C["st_screws"].shape, sm), COL["bolt"])],
            OUT / "joint-03.png", "Joint 3: seat tube collar and the sleeve's stop screw (cut open, seen from the front)",
            subtitle="The screw passes through the collar and the seat tube wall into the sleeve's slot; its tip stops short of the post",
            elev=20, azim=0, size=(8, 6)))
    # 4 sleeve top, the same cut one stage up
    if want(4):
        sm = P["st_len"] + split_saddle(MID["saddle_h"])[0] - 8
        out.append(bv.joint([
            part("Sleeve, cut open", axis_cut(C["sleeve"].shape, sm), COL["sleeve"]),
            part("Post; the screw is in its slot", axis_cut(C["post"].shape, sm), COL["post"]),
            part("Sleeve collar", axis_cut(C["sl_collar"].shape, sm), COL["collars"]),
            part("Stop screw (M5, dog point)", axis_cut(C["sl_screws"].shape, sm), COL["bolt"])],
            OUT / "joint-04.png", "Joint 4: sleeve collar and the post's stop screw (cut open, seen from the front)",
            subtitle="The same arrangement one stage up, on the right. Each slot's lower end leaves 100 mm inserted",
            elev=20, azim=0, size=(8, 6)))
    # 5 head tube cut open: cups, steerer, quill
    if want(5):
        a, b_ = steer_pt(P["crown_t"] - 30), steer_pt(D["steerer_top"] + MID["stem_exp"] + 20)
        bx_ = (min(a[0], b_[0]) - 45, max(a[0], b_[0]) + 60, 0, 50, a[1], b_[1])
        out.append(bv.joint([
            part("Head tube (cut open)", W(fr, *bx_), COL["frame"]),
            part("Headset cups and locknut", W(C["headset"].shape, *bx_), COL["headset"]),
            part("Fork crown and steerer", W(C["fork"].shape, *bx_), "#D4A017"),
            part("Quill in the steerer", W(C["quill"].shape, *bx_), "#CBD5E1"),
            part("Expander bolt", W(C["exp_bolt"].shape, *bx_), COL["bolt"]),
            part("Head plate", W(C["head_plate"].shape, *bx_), "#475569")],
            OUT / "joint-05.png", "Joint 5: head tube, headset, steerer and quill (cut open on the center plane)",
            subtitle="The quill slides in the steerer's 22.2 mm bore; the expander bolt pulls the wedge up to lock it",
            elev=6, azim=-90, size=(8, 7)))
    # 6 quill head: plate, block, bar, expander bolt
    if want(6):
        qt = steer_pt(D["steerer_top"] + MID["stem_exp"])
        bx_ = (qt[0] - 30, qt[0] + 145, -60, 60, qt[1] - 30, qt[1] + 40)
        out.append(bv.joint([
            part("Head plate (welded to the quill)", W(C["head_plate"].shape, *bx_), "#94A3B8"),
            part("Quill", W(C["quill"].shape, *bx_), "#E2E8F0"),
            part("Expander bolt head", W(C["exp_bolt"].shape, *bx_), COL["bolt"]),
            part("Bar clamp block, back position", W(S("clamp_lo", "clamp_hi"), *bx_), COL["block"]),
            part("Four M8 bolts into the plate", W(C["clamp_bolts"].shape, *bx_), "#111827"),
            part("Handlebar", W(C["handlebar"].shape, *bx_), COL["bar"])],
            OUT / "joint-06.png", "Joint 6: bar clamp block on the head plate",
            subtitle="Seen from behind and above. Back position shown (bar 45 mm ahead of the steering axis); the front holes put it 105 mm ahead",
            elev=32, azim=145, size=(8, 6)))
    # 7 crown: caliper, bolt, front fender bracket
    if want(7):
        cm = D["crown_mid"]
        bx_ = (cm[0] - 70, cm[0] + 60, -70, 70, cm[1] - 120, cm[1] + 30)
        fst = _ffstays()
        out.append(bv.joint([
            part("Fork crown and blades", W(C["fork"].shape, *bx_), COL["fork"]),
            part("Caliper", W(C["caliper"].shape, *bx_), COL["caliper"]),
            part("Caliper bolt through the crown", W(C["brake_bolt"].shape, *bx_), COL["bolt"]),
            part("Front fender", W(C["ffender"].shape, *bx_), COL["ffender"]),
            part("Fender bracket under the crown", W(fst, *bx_), "#475569"),
            part("Tire", W(C["tires"].shape, *bx_), COL["tires"]),
            part("Rim; the pads close on its brake track", W(C["front_wheel"].shape, *bx_), "#CBD5E1")],
            OUT / "joint-07.png", "Joint 7: front caliper and fender bracket at the fork crown",
            subtitle="One bolt through the crown carries the caliper in front and the fender bracket behind. The fender clears the crown by 7 mm",
            elev=15, azim=-35, size=(8, 6)))
    # 8 seat stays: cross bar, fender bridge, rack stay on its boss
    if want(8):
        xb = D["xbar"]
        bx_ = (130, xb[0] + 40, -85, 85, 330, xb[1] + 25)
        out.append(bv.joint([
            part("Seat tube, stays and cross bar", W(fr, *bx_), COL["frame"]),
            part("Rack stays, tabs on the bosses", W(C["rack"].shape, *bx_), COL["rack"]),
            part("Rear fender", W(C["rfender"].shape, *bx_), "#94A3B8"),
            part("Fender bracket on the bridge", W(_rfstays(), *bx_), "#475569")],
            OUT / "joint-08.png", "Joint 8: seat stay cross bar, fender bridge and rack stays, seen from behind",
            subtitle="The cross bar holds the stays 80 mm apart so the 64 mm fender passes between them",
            elev=32, azim=160, size=(8, 6)))
    # 9 kickstand plate, from below
    if want(9):
        kx = D["bb_x"] - P["kick_x"]
        bx_ = (kx - 70, D["bb_x"] + 25, -60, 70, 180, 290)
        out.append(bv.joint([
            part("Chainstays and BB shell", W(fr, *bx_), COL["frame"]),
            part("Kickstand clamp and leg", W(C["kickstand"].shape, *bx_), COL["kick"]),
            part("M10 bolt through the plate", W(C["kick_bolt"].shape, *bx_), COL["bolt"])],
            OUT / "joint-09.png", "Joint 9: kickstand on the kickstand plate, seen from below",
            subtitle="The 4 mm plate is brazed under both chainstays; the kickstand clamps to it with one M10 bolt, 36 mm clear of the chain",
            elev=-45, azim=-120, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only is None or n in only:
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    sa, ha = P["seat_ang"], P["head_ang"]
    fr = M["frame"]
    st(1, [fr], [mv(part("Drive-side cup", _bb_half(-1), COL["bb"]), (0, -140, 0)),
                 mv(part("Spindle and left cup", _bb_half(1), "#78716C"), (0, 160, 0))],
       "bottom bracket into the frame",
       "Grease the threads; drive-side cup (left-hand thread) tight, spindle in, left cup and lockring set for no play",
       elev=12, azim=-35, label_done=False)
    st(2, [fr, M["bb"]], [mv(M["headset"], (0, 0, 0)), mv(M["fork"], along(ha, -260))],
       "headset cups and fork",
       "Press both cups into the head tube, crown race on the fork; fork up through the head tube; top race, washer, locknut",
       elev=12, azim=-40, label_done=False)
    base = [fr, M["bb"], M["headset"], M["fork"]]
    stc = part("Seat tube collar and stop screw", S("st_collar", "st_screws"), COL["collars"])
    st(3, base, [mv(M["sleeve"], along(sa, 260)), mv(stc, along(sa, 110))],
       "sleeve into the seat tube, collar and stop screw",
       "Grease the sleeve; slot to the left. Collar on, hole lined up; stop screw in; set the height and tighten the 13 mm bolt",
       elev=14, azim=40, label_done=False)
    slc = part("Sleeve collar and stop screw", S("sl_collar", "sl_screws"), COL["collars"])
    base3 = base + [M["sleeve"], stc]
    st(4, base3, [mv(slc, along(sa, 90)), mv(M["post"], along(sa, 360)), mv(M["saddle"], along(sa, 600))],
       "seat post, sleeve collar and saddle",
       "Post greased, slot to the right; collar and stop screw; saddle clamped level on the post top",
       elev=14, azim=-40, label_done=False)
    base4 = base3 + [slc, M["post"], M["saddle"]]
    st(5, base4, [mv(M["quill"], along(ha, 300))], "quill stem into the steerer",
       "Grease the quill; slide it in to the setting; tighten the 13 mm expander bolt with the plate square to the wheel",
       elev=14, azim=-40, label_done=False)
    base5 = base4 + [M["quill"]]
    st(6, base5, [mv(part("Lower half of the clamp block", C["clamp_lo"].shape, COL["block"]), (0, 0, 90)),
                  mv(M["bar"], (0, 0, 190)),
                  mv(part("Clamp block cap and bolts", S("clamp_hi", "clamp_bolts"), "#A78BFA"), (0, 0, 300))],
       "bar clamp block and handlebar",
       "Lower half over the chosen hole set; bar on it, centered; cap and four M8 x 40 bolts, tightened evenly",
       elev=22, azim=-50, label_done=False)
    base6 = base5 + [M["block"], M["bar"]]
    st(7, base6, [mv(M["ffender"], (0, 0, -150)), mv(M["caliper"], (160, 0, 40))],
       "front fender and caliper on the crown",
       "Fender bracket behind the crown, caliper in front, on the one bolt; fender stays to the fork-end eyelets later (step 9)",
       elev=12, azim=-40, label_done=False)
    st(8, [part("Front wheel", C["front_wheel"].shape, COL["fwheel"])],
       [mv(part("Solid tire", _tire(1), COL["tires"]), (0, -160, 0))],
       "tires onto the rims",
       "Soak the solid tire in hot water to soften it; seat one side, then lever the other on, working round. Same for the rear",
       elev=10, azim=-60, label_done=False)
    base7 = base6 + [M["ffender"], M["caliper"]]
    st(9, base7, [mv(part("Front wheel with tire", _comp(C["front_wheel"].shape, _tire(1)), COL["fwheel"]), (0, 0, -170))],
       "front wheel into the fork",
       "Axle up into the fork ends, wheel centered; 15 mm axle nuts tight; fender stays onto the fork-end eyelets",
       elev=10, azim=-45, label_done=False)
    fwt = part("Front wheel and tire", _comp(C["front_wheel"].shape, _tire(1)), "#9CA3AF")
    base8 = base7 + [fwt]
    st(10, base8, [mv(M["crank"], (0, -220, 0))], "crankset and pedals",
       "Chainring on the drive side; cranks onto the spindle and tight; pedals in (left pedal has a left-hand thread)",
       elev=12, azim=-45, label_done=False)
    rwt = part("Rear wheel with tire, sprocket and arm", _comp(C["rear_wheel"].shape, C["cog"].shape, C["arm"].shape, _tire(0)), COL["rwheel"])
    base9 = base8 + [M["crank"]]
    st(11, base9, [mv(rwt, (-150, 0, 0))], "rear wheel into the track ends",
       "Axle slides forward into both slots; brake arm on the left, under the chainstay; nuts finger tight for now",
       elev=12, azim=-45, label_done=False)
    base10 = base9 + [rwt]
    st(12, base10, [mv(M["chain"], (0, -160, 0)), mv(M["clip"], (0, 40, -210))],
       "chain, tension and brake arm clip",
       "Chain on; pull the axle back until the chain moves 10 to 15 mm up and down mid-span; nuts tight; clip the arm to the stay",
       elev=10, azim=-60, label_done=False)
    base11 = base10 + [M["chain"], M["clip"]]
    st(13, base11, [mv(M["rfender"], (-60, 0, 160))], "rear fender and stays",
       "Fender up between the seat stays; bracket to the bridge; stays to the dropout eyelets (inside the rack tabs)",
       elev=16, azim=-55, label_done=False)
    base12 = base11 + [M["rfender"]]
    st(14, base12, [mv(M["rack"], (0, 0, 200))], "rack",
       "Struts to the dropout eyelets over the fender stay eyes, stays to the seat stay bosses; four M5 bolts",
       elev=18, azim=-55, label_done=False)
    base13 = base12 + [M["rack"]]
    st(15, base13, [mv(M["guard"], (0, -160, 30))], "chainguard",
       "Clip round the seat tube; tab to the boss on the drive chainstay; check it clears the chain and the crank",
       elev=10, azim=-70, label_done=False)
    base14 = base13 + [M["guard"]]
    st(16, base14, [mv(M["kick"], (0, 60, -160))], "kickstand",
       "Clamp under the kickstand plate with the M10 bolt; leg on the left; set its length so the bike leans a little",
       elev=6, azim=35, label_done=False)
    base15 = base14 + [M["kick"]]
    st(17, base15, [mv(M["refl"], (0, 0, 150))], "reflectors, bell and brake cable",
       "Front reflector on the head plate, rear on the rack plate, spoke reflectors, bell; front brake cable with slack for the full stem travel",
       elev=14, azim=-50, label_done=False)
    return out


def _bb_half(side):
    """side -1: the drive-side cup; side +1: the spindle and the left cup."""
    import build123d as b
    bb = C["bb"].shape
    if side < 0:
        return bb & b.Pos(D["bb_x"], -55, P["bb_z"]) * b.Box(60, 30, 60)
    return bb & b.Pos(D["bb_x"], 25, P["bb_z"]) * b.Box(60, 140, 60)


def _tire(front):
    import build123d as b
    t = C["tires"].shape
    x = P["wheelbase"] if front else 0.0
    return t & (b.Pos(x, 0, R) * b.Box(520, 60, 520))


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layout", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "layout": layout, "joints": joints, "steps": steps}
    i = 0
    while i < len(args):
        w = args[i]
        nums = []
        while i + 1 < len(args) and args[i + 1].isdigit():
            nums.append(int(args[i + 1])); i += 1
        r = fns[w](set(nums)) if nums and w in ("sheets", "joints", "steps") else fns[w]()
        print(w, "->", r)
        i += 1
