# UAV-Sim

<p align="center">

**UAV Flight & Aerodynamic Simulation Framework**

CAD Geometry → CFD → LBM → Aerodynamic Visualization → Dynamic Flight

</p>

---

## 🚧 Pre-Release

**Current version: `v0.1.0-pre.1`**

UAV-Sim is currently under active development.

This pre-release establishes the foundation for a UAV aerodynamic simulation framework using:

- UAV geometry
- 2D computational fluid dynamics
- D2Q9 Lattice Boltzmann Method (LBM)
- Velocity-field visualization
- Vorticity visualization
- Angle-of-attack control
- Physical flight-condition calculations

The next development stage will introduce:

- Dynamic angle of attack
- Acceleration
- Launch
- Climb
- Cruise
- Descent
- Landing
- Dynamic flight-state simulation
- 3D UAV visualization
- Animated CFD
- Flight trajectory

---

# Overview

UAV-Sim is an experimental UAV simulation framework designed to connect **aircraft geometry, aerodynamic simulation and flight dynamics** into a single workflow.

The long-term goal is to allow a user to provide a UAV model and flight conditions such as:

```text
UAV Geometry
     ↓
Mass
     ↓
Launch Angle
     ↓
Initial Speed
     ↓
Altitude
     ↓
Wind
     ↓
Angle of Attack
     ↓
Flight State