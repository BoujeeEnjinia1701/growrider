# GrowRider

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $250 USD · **Difficulty:** 2 of 5

Rugged, repairable children's bicycle with an adjustable frame that fits ages 6 to 14, puncture-proof tires, a coaster brake and a small rated rack, built from parts common to regional adult bicycles.

![GrowRider concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Rural children often walk more than an hour each way to school, and adult bicycles do not fit them while imported children's bikes break quickly and cannot be repaired locally. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Rugged, repairable children's bicycle with an adjustable frame that fits ages 6 to 14, puncture-proof tires, a coaster brake and a small rated rack, built from parts common to regional adult bicycles.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Steel frame with telescoping seat and head tubes
- Puncture-proof 20 to 24 in wheels
- Coaster brake hub
- Single-speed chain drive
- Rated rear rack (10 kg)
- Reflectors and bell

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Rack load is limited to 10 kg for child safety. Frames must pass drop and fatigue tests before field use.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (GRR-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `GRR-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
