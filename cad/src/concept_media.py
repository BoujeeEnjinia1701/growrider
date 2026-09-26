"""GrowRider concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Main dimensions and interfaces only; not for fabrication.

Axes: X along the bike (rear axle at x = 0, front toward +X), Z up, Y lateral.
The drive side (chain) is at -Y, facing the camera in the hero view.
Seat post and stem are set for a 1.38 m rider (about age 10). Figures come from GRR-CAL-001.
"""
import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[2] / ".kit"), str(Path(__file__).resolve().parent)]
from concept import Part, render_all, human_figure

from model import PARAMS, build_parts, derived  # noqa: E402

# Media show the bike set for a 1.38 m rider (about age 10), beside a 1.35 m child.
MID = {"saddle_h": 537.0, "stem_exp": 75.0, "ext": 0.0}
D = derived(PARAMS)
WHEELBASE, R_WHEEL = PARAMS["wheelbase"], D["R"]

COLORS = {"frame": "#2E5E8C", "fork": "#2E5E8C", "seatpost": "#9CA3AF", "saddle": "#D6C7A1",
          "stem": "#9CA3AF", "handlebar": "#4B5563", "front_wheel": "#B8BEC6", "rear_wheel": "#B8BEC6",
          "tires": "#262626", "crankset": "#6B7280", "chain": "#C2410C", "front_brake": "#D4A017",
          "rack": "#0F766E", "fenders": "#374151", "chainguard": "#94A3B8", "kickstand": "#6B7280",
          "reflectors": "#DC2626"}
EXPLODE = {"fork": (260, 0, 0), "seatpost": (-80, -220, 240), "saddle": (-40, 0, 640), "stem": (150, 0, 260),
           "handlebar": (250, 0, 450), "front_wheel": (560, 0, 0), "rear_wheel": (-560, 0, -520),
           "tires": (0, 0, -420), "crankset": (0, -260, -300), "chain": (0, -420, -150),
           "front_brake": (400, 0, 180), "rack": (160, 0, 400), "fenders": (320, 0, 800),
           "chainguard": (0, -300, 120), "kickstand": (0, 220, -220), "reflectors": (260, 0, 980)}
parts = [Part(name, shape, COLORS[key], bom, EXPLODE.get(key, (0, 0, 0)))
         for key, name, shape, bom in build_parts(PARAMS, MID)]

# Child for scale: 1.35 m (about a 10 year old), standing beside the front wheel
child = human_figure(height=1350, x=WHEELBASE + R_WHEEL + 450, y=0, z=0)
child.name = "Child, 1.35 m"
context = [child]

if __name__ == "__main__":
    render_all(
        parts, project="GrowRider", title="Adjustable child bicycle concept", dwg_no="GRR-DWG-010", date="2026-09-25",
        key_figures=["Rider height 1.10 to 1.65 m (ages about 6 to 14)",
                     "Saddle 400 to 670 mm from BB; 100 mm min. insertion",
                     "20 in wheels, 860 mm wheelbase, 455 mm standover",
                     "Coaster brake plus front rim brake",
                     "Rack rated 10 kg; bike about 14.4 kg (target 13 kg)",
                     "5 km school trip: 25 to 30 min vs 60 to 75 min walking"],
        scale_figure=False, context=context, cut=False,
        flow={"title": "growth and hand-down cycle (estimates)", "unit": "",
              "stages": [("Age 6, 1.10 m", "saddle 400 mm"), ("Age 10, 1.38 m", "saddle 537 mm"),
                         ("Age 14, 1.65 m", "saddle 669 mm"), ("Reset for sibling", "13 mm spanner, 10 min"),
                         ("Next sibling", "10 year life (target)")]},
    )
