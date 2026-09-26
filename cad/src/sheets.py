"""GrowRider general arrangement sheet GRR-DWG-001, Rev P2 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/GRR-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from the model and
PARAMS, so they follow any parameter change. The concept sheet in media/ is GRR-DWG-010.
"""
import shutil
import sys
from math import cos, radians
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, SETTINGS, build, derived, grip_pt, saddle_pt  # noqa: E402

DATE = "2026-09-25"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text):
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    large, small = build(setting="large"), build(setting="small")
    views = project_views(large, work / "large")
    views["iso"] = project_views(small, work / "small")["iso"]
    bb = large.bounding_box()
    s = Sheet(project="GrowRider", title="General arrangement", dwg_no="GRR-DWG-001", rev="P2",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Chromoly 4130 main tubes, steerer, quill and sleeve; aluminium rack; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "GRR-DDR-002: chromoly tubes, 29.2 sleeve, aluminium rack", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    # front view (from -Y): X to the right, ground at the bottom of the view
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L += dim_h(X(bb.min.X), X(bb.max.X), y - 10, f"{bb.size.X:,.0f} overall")
    L += [ext(X(0), y - 6, X(0), Z(D["R"])), ext(X(P["wheelbase"]), y - 6, X(P["wheelbase"]), Z(D["R"]))]
    L += dim_h(X(0), X(P["wheelbase"]), y - 4, f"{P['wheelbase']:.0f} wheelbase")
    L += dim_v(x - 4, Z(bb.max.Z), zg, f"{bb.size.Z:,.0f}")
    L += [ext(x - 11, Z(P['bb_z']), X(D['bb_x']), Z(P['bb_z']))]
    L += dim_v(x - 10, Z(P["bb_z"]), zg, f"{P['bb_z']:.0f} BB")
    L += [ext(X(D['stand_x']), Z(D['standover']), X(bb.max.X) + 8, Z(D['standover']))]
    L += dim_v(X(bb.max.X) + 6, Z(D["standover"]), zg, f"{D['standover']:.0f} standover")
    # top view: overall width
    x, y, w, h = c["top"]
    L += dim_v(x - 4, y, y + h, f"{bb.size.Y:.0f}")
    # right view: handlebar width
    x, y, w, h = c["right"]
    L += dim_h(x, x + w, y - 4, f"{P['bar_width']:.0f} bar")
    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view, smallest rider setting", sublabel="Not to scale")
    sp_s, sp_l = saddle_pt(SETTINGS["small"]["saddle_h"]), saddle_pt(SETTINGS["large"]["saddle_h"])
    s.add_notes("Main dimensions and interfaces (mm)", [
        "Ortho views at the largest rider setting (1.65 m)",
        f"Wheels 20 in (ISO 406), tire OD {P['tire_od']:.0f}; trail {D['trail']:.0f}; axes {P['head_ang']:.0f} deg",
        f"Saddle {D['saddle_min']:.0f} to {D['saddle_max']:.0f} from BB; {sp_s[1]:.0f} to {sp_l[1]:.0f} above ground",
        f"Seat post: {P['sleeve_od']} sleeve in {P['st_od']} seat tube, {P['post_od']} post; 100 min. insertion",
        f"Quill {P['quill_d']} in 1 in steerer, {P['quill_travel']:.0f} travel; head {P['ht_len']:.0f}",
        f"Stem head 0 or 60 forward; bar {P['bar_width']:.0f} wide, {P['bar_sweep']:.0f} sweep",
        f"Cranks {P['crank']:.0f}, {P['ring_t']}/{P['cog_t']}; coaster hub plus front rim brake",
        f"Rack {P['rack_len']:.0f} x {P['rack_w']:.0f} at Z {P['rack_z']:.0f}, rated 10 kg",
        f"Rims alloy; rack aluminium 6061-T6, {P['rack_tube']:.0f} x {P['rack_wall']}",
        "Mass about 14.4 kg (GRR-CAL-001 v0.2); third-angle, front view from -Y",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "GRR-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
