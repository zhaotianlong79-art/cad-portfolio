# FigNest R01 | Design and prototype review

**Independent portfolio concept based on the public job excerpt. Not released
for tool cutting, food contact or infant use.**

## What is modelled

- **FN-101:** One-piece hollow teat with an integrated natural rubber collar.
  The blank, slow study and medium study are separate STEP files. The two study
  parts use the same blank and differ only in the post-mould bore.
- **FN-102:** Flat closed storage cap with a rounded pull tab, rounded skirt
  edge and the same ring seal and neck interface as the teat.
- **FN-900:** Nominal glass neck gauge, not a supplier bottle model. The bore
  beneath both closures is smooth. The dashed lines in the section indicate
  the region reserved for the future thread.
- Both closures have a nominal 9 mm custom fig leaf in 0.25 mm low relief,
  on the front collar of the teat and on the top face of the cap.
- The assembly STEP shows the two alternatives side by side, each at the same
  local seat elevation. The concept board lifts the storage cap for clarity.

## Nominal model values

| Feature | R01 value | Status |
|---|---:|---|
| Glass lip datum | Z = 0 | Shared assembly datum |
| Maximum gauge OD through skirt | Ø41.10 mm | Assumed glass envelope |
| Smooth collar bore | Ø43.10 mm | Reference clearance of 1.00 mm per side along the straight skirt |
| Collar outside diameter | Ø50.80 mm | Excludes tab and relief |
| Teat blank height | 43.05 mm | Excludes the illustrated piercing operations |
| Cap body height | 16.30 mm | Excludes raised mark |
| Cap centre deck | 3.20 mm | Nominal undeformed section |
| Teat blank crown thickness | 2.22 mm | Axial measurement at centre |
| Seal bead | Ø38.00 mm crown centre | Tangent at Z = 0 in CAD, no squeeze applied |
| Trial straight bores | Ø0.55 / Ø0.80 mm | Geometry examples only, no flow rate inferred |
| Natural rubber hardness | 35 ± 5 Shore A | Brief target, grade and performance TBD |

The two closures share a geometry reference only. No screw engagement, clamping
torque, seal preload, pull-off capacity, fluid flow or leakage performance has
been established. A through-bore remains open at rest. If the teat itself must
be dry when inverted, define the pressure head, liquid, duration and leakage
limit before deciding whether a straight pierced hole fits that requirement.
Test the closed storage cap and teat assembly separately.

## Tooling decision for the moulder

Use the same teat cavity for both trial variants and qualify two piercing
operations. The cap requires a different cavity and core. A shared tool frame
with separate inserts is a candidate if the moulder confirms compatible
compound, cure cycle and loading, acceptable fill and venting for both shapes,
and a workable cavity ratio. Separate inserts or tools make iteration of the
teat easier while the cap remains stable. The proposed separation or trimming
zone is near the skirt rim, away from the lip seal and pierced outlet. The
moulder must set actual draft, parting and flash controls, cure and shrinkage
compensation, and confirm whether to strip or unscrew the future threaded core.
The part STEP files have no shrinkage compensation.

## Before a production release

1. Measure representative glass samples. Obtain the neck finish drawing, major
   and minor thread diameters, profile, lead, pitch, starts, usable engagement,
   entry and runout, lip flatness and supplier tolerances.
2. Obtain the moulder’s rules and the exact natural rubber compound. Review
   minimum wall, demoulding, edge radii, parting line, shrinkage and flash limits.
   Obtain material documentation for the intended markets and food contact.
3. Obtain shape feedback from the lactation consultant and the brief’s flow
   targets. Confirm piercing method, bore geometry and process variation.
4. Build the measured thread and define seal squeeze with a stack-up at the
   glass and rubber tolerance limits. Validate engagement and seal repeatability
   on actual moulded samples and representative glass.
5. Agree on the applicable edition and test scope with a lab. Verify teat
   retention and other applicable product requirements, plus inverted
   leakage, storage and flow under the brief’s conditions, before claiming
   performance or compliance. The cited standard describes the test scope.
   This CAD review is not a test report.

## Files and review checks

Run `uv run Build-FigNest.py` to edit and rebuild the parametric CadQuery source.
The STEP files contain B-rep solids. FN-001 DXF contains true-scale section
outlines as editable polylines, material hatching, centerlines, four AutoCAD
dimension entities and an A3 layout. The PNG is an English presentation view.

All exported STEP parts were reopened and checked as valid solids. Both rubber
parts clear the nominal glass gauge in the CAD model and contact it at the
seal datum. The concept bores cut through the crown. Section probes around the axis
confirmed both bore sizes and the CAD differences were confined to the crown.
The DXF reopened without audit errors. During the first fit check the pull tab root penetrated the
glass envelope. The root is now trimmed before fusion and the revised solids
pass the same zero-volume overlap check.

- [BSI, BS EN 14350:2020+A1:2023 drinking equipment requirements and test methods](https://landingpage.bsigroup.com/LandingPage/Standard?UPI=000000000030478650)
- [Minnesota Rubber & Plastics elastomer engineering design guide](https://www.mnrubber.com/tools-resources/design-guide/)
- [Panova rubber moulding design guidance](https://www.panova.com/designing-for-rubber-molding-engineering-best-practices-for-tolerances-shrinkage-parting-lines-and-draft-angles/)
