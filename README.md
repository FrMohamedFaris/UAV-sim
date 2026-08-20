# UAV-Sim ✈️

A modular UAV flight simulation and visualization platform that combines:

- 3D CAD/STEP models
- UAV flight dynamics
- Launch-angle simulation
- Wind and gust modelling
- Aerodynamic force modelling
- 3D UAV visualization
- Real-time simulation HUD
- MP4 flight rendering
- Planned LBM/CFD integration inspired by the rendering concepts used in Spectrometry

---

## 🚧 Project Status

**Current stage: Stage 5 — Flight + Wind Visualization**

The current version can:

- Load a UAV from a STEP CAD file
- Convert the CAD model into a visualization mesh
- Display the UAV in a 3D environment
- Simulate UAV position and velocity
- Simulate launch angle
- Simulate pitch changes through a flight profile
- Apply gravity
- Apply thrust
- Calculate simplified aerodynamic lift and drag
- Calculate relative air velocity
- Generate a configurable wind field
- Add wind gusts
- Visualize airflow around the UAV
- Display simulation information through a HUD
- Render the simulation to MP4

### Current pipeline

STEP CAD
   ↓
OpenCascade / CadQuery
   ↓
3D Mesh
   ↓
UAV Flight Physics
   ↓
Wind Field
   ↓
Relative Airflow
   ↓
Lift + Drag
   ↓
3D Visualization
   ↓
HUD
   ↓
MP4
