# Static UAV CFD Example

This example demonstrates the current UAV-Sim CFD pipeline.

## Input

- UAV boundary extracted from CAD geometry
- 2D closed boundary
- Reference characteristic length: 0.33 m
- Airspeed reference: 180 km/h
- Angle of attack: 0°

## Processing

```text
UAV boundary
     ↓
Geometry transformation
     ↓
CFD domain
     ↓
Solid body mask
     ↓
D2Q9 LBM
     ↓
Velocity field
     ↓
Vorticity
     ↓
Visualization