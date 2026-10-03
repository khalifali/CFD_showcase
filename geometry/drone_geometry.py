"""Parametric, full fixed-wing UAV exterior for the CFD showcase.

Run with CadQuery 2.7: python drone_geometry.py [output_directory]
Geometry is in metres. Propeller and thrust are excluded. This is a geometric
concept for unpowered aerodynamic comparison, not a flight-certified design.
"""

from pathlib import Path
import math
import sys
import cadquery as cq

SPAN = 1.8
FUSELAGE_LENGTH = 1.35
ROOT_CHORD = 0.32
TIP_CHORD = 0.19
WING_LE_X = 0.48
WING_SWEEP = 0.11
WING_Z = 0.075


def naca4(m, p, t, count=50):
    """Clockwise perimeter from trailing edge over upper to lower surface."""
    beta = [math.pi * i / count for i in range(count + 1)]
    xs = [(1 - math.cos(a)) / 2 for a in beta]
    upper, lower = [], []
    for x in xs:
        yt = 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x
                      - 0.3516 * x*x + 0.2843 * x**3 - 0.1036 * x**4)
        if x < p:
            yc = m / (p*p) * (2*p*x - x*x)
            dy = 2*m / (p*p) * (p - x)
        else:
            yc = m / ((1-p)**2) * ((1-2*p) + 2*p*x - x*x)
            dy = 2*m / ((1-p)**2) * (p - x)
        a = math.atan(dy)
        upper.append((x - yt*math.sin(a), yc + yt*math.cos(a)))
        lower.append((x + yt*math.sin(a), yc - yt*math.cos(a)))
    return list(reversed(upper)) + lower[1:-1]


def section(chord, x_le, y, z, points, vertical=False):
    if vertical:
        vertices = [cq.Vector(x_le + chord*x, y + chord*h, z) for x, h in points]
    else:
        vertices = [cq.Vector(x_le + chord*x, y, z + chord*h) for x, h in points]
    return cq.Wire.makePolygon(vertices + [vertices[0]])


def wing_pair():
    profile = naca4(0.02, 0.4, 0.12)
    solids = []
    for side in (-1, 1):
        root = section(ROOT_CHORD, WING_LE_X, 0, WING_Z, profile)
        tip = section(TIP_CHORD, WING_LE_X + WING_SWEEP,
                      side*SPAN/2, WING_Z + 0.045, profile)
        solids.append(cq.Solid.makeLoft([root, tip], ruled=True))
    return solids


def fuselage():
    # x, lateral radius, vertical radius, centre height
    stations = [
        (0.00, 0.005, 0.005, 0.02),
        (0.11, 0.052, 0.055, 0.025),
        (0.28, 0.073, 0.073, 0.020),
        (0.55, 0.078, 0.080, 0.015),
        (0.82, 0.062, 0.063, 0.010),
        (1.10, 0.041, 0.043, 0.005),
        (1.35, 0.018, 0.020, 0.000),
    ]
    wires = []
    for x, ry, rz, zc in stations:
        plane = cq.Plane(origin=(x, 0, zc), xDir=(0, 1, 0), normal=(1, 0, 0))
        wires.append(cq.Workplane(plane).ellipse(ry, rz).val())
    return cq.Solid.makeLoft(wires, ruled=False)


def tail():
    symmetric = naca4(0, 0.4, 0.10)
    parts = []
    for side in (-1, 1):
        root = section(0.19, 1.04, 0, 0.025, symmetric)
        tip = section(0.125, 1.11, side*0.38, 0.045, symmetric)
        parts.append(cq.Solid.makeLoft([root, tip], ruled=True))
    # Swept vertical stabiliser intersects the fuselage.
    root = section(0.26, 1.02, 0, 0.00, symmetric, vertical=True)
    tip = section(0.10, 1.18, 0, 0.29, symmetric, vertical=True)
    parts.append(cq.Solid.makeLoft([root, tip], ruled=True))
    return parts


def build():
    body = fuselage()
    for part in wing_pair() + tail():
        body = body.fuse(part)
    body = body.clean()
    if not body.isValid() or len(body.Solids()) != 1:
        raise RuntimeError("Aircraft union is not a single valid solid")
    return body


def main():
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else "build")
    destination.mkdir(parents=True, exist_ok=True)
    aircraft = build()
    cq.exporters.export(aircraft, str(destination / "drone.step"))
    cq.exporters.export(aircraft, str(destination / "drone.stl"),
                        tolerance=0.0005, angularTolerance=0.1)
    box = aircraft.BoundingBox()
    print(f"Valid solid: {aircraft.isValid()}, solids: {len(aircraft.Solids())}")
    print(f"Bounds [m]: x={box.xmin:.3f}..{box.xmax:.3f}, "
          f"y={box.ymin:.3f}..{box.ymax:.3f}, z={box.zmin:.3f}..{box.zmax:.3f}")
    print(f"Solid volume: {aircraft.Volume():.6f} m^3")
    print(f"Wrote {destination / 'drone.step'} and {destination / 'drone.stl'}")


if __name__ == "__main__":
    main()
