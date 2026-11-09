# /// script
# dependencies = ["cadquery>=2.5,<2.8"]
# ///
"""FigNest R01 parametric concept geometry in millimetres."""
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent
FLOW_BORES = {"Slow-Study": 0.55, "Medium-Study": 0.80}
SEAL_RADIUS = 19.0
COLLAR_RADIUS = 25.4
PLACEHOLDER_BORE_RADIUS = 21.55
SKIRT_BOTTOM = -12.05
RELIEF = 0.25
GLASS_OUTER_RADIUS = 20.55
GLASS_INNER_RADIUS = 15.35


def fig_leaf():
    """Closed 9 mm fig leaf, built from cubic Bezier segments in local XY."""
    curves = [
        [(0, 4.5), (0.7, 3.7), (1.7, 2.9), (1.45, 1.85)],
        [(1.45, 1.85), (2.2, 2.08), (2.94, 2.73), (3.68, 2.25)],
        [(3.68, 2.25), (3.82, 1.44), (3.48, 0.62), (2.72, 0.25)],
        [(2.72, 0.25), (3.49, 0.34), (4.02, 0.1), (4.22, -0.54)],
        [(4.22, -0.54), (3.8, -2.13), (1.9, -2.9), (0.62, -2.89)],
        [(0.62, -2.89), (0.43, -3.29), (0.6, -3.87), (0.37, -4.3)],
        [(0.37, -4.3), (0.19, -4.59), (-0.3, -4.55), (-0.43, -4.23)],
        [(-0.43, -4.23), (-0.58, -3.91), (-0.45, -3.22), (-0.65, -2.9)],
        [(-0.65, -2.9), (-2.2, -2.94), (-3.83, -2.02), (-4.14, -0.65)],
        [(-4.14, -0.65), (-4.11, -0.07), (-3.48, 0.37), (-2.72, 0.25)],
        [(-2.72, 0.25), (-3.34, 0.73), (-3.85, 1.48), (-3.65, 2.3)],
        [(-3.65, 2.3), (-2.96, 2.81), (-2.23, 2.26), (-1.47, 1.89)],
        [(-1.47, 1.89), (-1.58, 2.98), (-0.67, 3.65), (0, 4.5)],
    ]
    edges = [
        cq.Edge.makeBezier([cq.Vector(x, y, 0) for x, y in points])
        for points in curves
    ]
    return cq.Wire.assembleEdges(edges)


def leaf_prism(height):
    return cq.Solid.extrudeLinear(fig_leaf(), [], cq.Vector(0, 0, height))


def collar_return(profile):
    """Finish the rounded skirt, placeholder bore and common annular bead."""
    return (
        profile.lineTo(COLLAR_RADIUS, -10.9)
        .threePointArc((25.063, -11.713), (24.25, SKIRT_BOTTOM))
        .lineTo(22.5, SKIRT_BOTTOM)
        .threePointArc((21.828, -11.772), (PLACEHOLDER_BORE_RADIUS, -11.1))
        .lineTo(PLACEHOLDER_BORE_RADIUS, -0.15)
        .threePointArc((21.21, 0.75), (20.40, 1.05))
        .lineTo(SEAL_RADIUS + 1.05, 1.05)
        .threePointArc((SEAL_RADIUS, 0), (SEAL_RADIUS - 1.05, 1.05))
    )


def pull_tab():
    tab = (
        cq.Workplane("XY", origin=(26, 0, -8.5))
        .ellipse(8.5, 7)
        .extrude(4.2)
    )
    rounded = tab.edges().fillet(1.25).val()
    # Trim the hidden root before fusing so the tab cannot obstruct the bore.
    root_limit = cq.Solid.makeBox(17, 20, 12, cq.Vector(23, -10, -12))
    return rounded.intersect(root_limit)


def teat_blank():
    outer = [
        (0, 31), (2.45, 30.56), (4.58, 29.3), (5.62, 26.55),
        (5.92, 23.1), (6.84, 19), (9.67, 14.65), (13.98, 9.12),
        (18.30, 5.68), (22.50, 4.2), (24.1, 4.1),
    ]
    inner = [
        (15.15, 1.92), (14.78, 4.45), (12.20, 7.69), (8.05, 12.9),
        (4.84, 17.65), (4.02, 22.40), (3.82, 25.5), (3.23, 27.4),
        (1.95, 28.43), (0, 28.78),
    ]
    profile = (
        cq.Workplane("XZ").spline(outer, tangents=[(1, 0), (1, -0.06)])
        .threePointArc((25.02, 3.67), (COLLAR_RADIUS, 2.55))
    )
    profile = (
        collar_return(profile).lineTo(16.4, 1.05)
        .threePointArc((15.52, 1.28), inner[0])
        .spline(inner[1:], includeCurrent=True, tangents=[(0, 1), (-1, 0)])
        .close()
    )
    body = profile.revolve().val()
    leaf = leaf_prism(3).rotate((0, 0, 0), (1, 0, 0), 90).translate((0, -23.5, -6.1))
    relief_envelope = cq.Solid.makeCylinder(COLLAR_RADIUS + RELIEF, 12, cq.Vector(0, 0, -12))
    return body.fuse(pull_tab(), leaf.intersect(relief_envelope)).clean()


def teat_variant(blank, hole_diameter):
    bore = cq.Solid.makeCylinder(hole_diameter / 2, 8, cq.Vector(0, 0, 26))
    return blank.cut(bore).clean()


def storage_cap():
    profile = (
        cq.Workplane("XZ").moveTo(0, 4.25).lineTo(24.15, 4.25)
        .threePointArc((25.03, 3.88), (COLLAR_RADIUS, 3))
    )
    profile = collar_return(profile).lineTo(0, 1.05).close()
    lid = profile.revolve().val()
    mark = leaf_prism(0.35).translate((0, 0, 4.15))
    return lid.fuse(pull_tab(), mark).clean()


def glass_gauge():
    profile = [
        (GLASS_INNER_RADIUS, 0), (19.95, 0),
        (GLASS_OUTER_RADIUS, -0.65), (GLASS_OUTER_RADIUS, -14.7),
        (23.4, -17.7), (23.4, -29), (20.5, -29),
        (20.5, -20), (GLASS_INNER_RADIUS, -14.7),
    ]
    return cq.Workplane("XZ").polyline(profile).close().revolve().val()


def components():
    blank = teat_blank()
    return {
        "FN-101-Teat-Blank": blank,
        **{
            f"FN-101-Teat-{name}": teat_variant(blank, diameter)
            for name, diameter in FLOW_BORES.items()
        },
        "FN-102-Storage-Cap": storage_cap(),
        "FN-900-Glass-Neck-Gauge": glass_gauge(),
    }


def validate(parts):
    glass = parts["FN-900-Glass-Neck-Gauge"]
    blank = parts["FN-101-Teat-Blank"]
    cap = parts["FN-102-Storage-Cap"]
    for name, part in parts.items():
        assert part.isValid() and len(part.Solids()) == 1, name
        if part is not glass:
            assert part.intersect(glass).Volume() < 1e-5, f"{name}: gauge interference"
            bead = cq.Vector(SEAL_RADIUS, 0, 0)
            assert cq.Vertex.makeVertex(*bead.toTuple()).distance(part) < 1e-6
    for name, diameter in FLOW_BORES.items():
        part = parts[f"FN-101-Teat-{name}"]
        bore = cq.Solid.makeCylinder(diameter / 2, 8, cq.Vector(0, 0, 26))
        removed = blank.intersect(bore).Volume()
        assert 2.1 < removed / (3.141592653589793 * (diameter / 2) ** 2) < 2.4
        assert not part.isInside(cq.Vector(0, 0, 30))
    assert cap.isInside(cq.Vector(0, 0, 2.7))


def export():
    target = ROOT / "STEP"
    target.mkdir(exist_ok=True)
    parts = components()
    validate(parts)
    for name, shape in parts.items():
        filename = target / f"{name}.step"
        cq.exporters.export(shape, str(filename))
        reopened = cq.importers.importStep(str(filename)).solids().vals()
        assert len(reopened) == 1 and reopened[0].isValid(), name
        assert abs(reopened[0].Volume() / shape.Volume() - 1) < 0.0001
        print(name, "valid solid", round(shape.Volume(), 2), "mm³", flush=True)

    assembly = cq.Assembly(name="FN-001 | FigNest R01 | nominal interfaces only")
    for station, key in [
        (-44, "FN-101-Teat-Slow-Study"),
        (44, "FN-102-Storage-Cap"),
    ]:
        shift = cq.Location(cq.Vector(station, 0, 0))
        assembly.add(parts[key], name=key, loc=shift, color=cq.Color(0.82, 0.56, 0.33))
        assembly.add(
            parts["FN-900-Glass-Neck-Gauge"],
            name=f"Reference gauge {station:+}",
            loc=shift,
            color=cq.Color(0.45, 0.66, 0.62, 0.35),
        )
    filename = target / "FN-001-FigNest-Assembly.step"
    assembly.export(str(filename))
    reopened = cq.importers.importStep(str(filename)).solids().vals()
    assert len(reopened) == 4 and all(s.isValid() for s in reopened)
    print("Assembly: four valid solids. Reference clearance and open bores checked.")


if __name__ == "__main__":
    export()
