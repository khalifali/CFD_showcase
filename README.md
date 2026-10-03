# CFD Showcase — OpenFOAM 13

## Purpose

Develop a portfolio of reproducible CFD simulations relevant to engineering applications in the Middle East, with clear, visually compelling movies for professional presentations and self-marketing.

The portfolio will demonstrate geometry creation, meshing, physical modelling, numerical verification, interpretation of results, and scientific visualization.

**Status: planning only.** No simulation cases have been prepared or run.

**Platform:** OpenFOAM Foundation version 13. Solver modules, models, dictionary syntax, and tutorial starting points must be checked against this exact release before implementation. This is an independent project.

## Mandatory software constraint

All CFD cases must use unmodified solvers, solver modules, models, boundary conditions, and runtime functionality shipped with **OpenFOAM Foundation 13**.

- No custom solvers, source modifications, third-party CFD extensions, or custom compiled physics/boundary-condition libraries.
- Geometry-generation, case-setup, execution, and visualization scripts are allowed; they do not add CFD physics.
- Confirm each combination of physics in the version-13 source and tutorials before committing to it.
- If a desired combination is unavailable, propose a supported alternative or simpler case for discussion. Do not implement missing physics.
- In particular, combined VOF and species/interphase transfer remains unverified. Possible alternatives for discussion are a supported multiphase species-transport reactor or separate VOF and species-transport demonstrations.

## Planned portfolio

| Case | Engineering theme | Intended physics | Main movie | Quantitative companion |
| --- | --- | --- | --- | --- |
| Reactor | Water treatment or chemical processing | Multiphase flow, species transport, and potentially reaction or interphase mass transfer | Liquid interface and concentration evolution | Species balance, mixing time, and transfer or conversion where modelled |
| Drone aerodynamics | Civil inspection and environmental monitoring | External turbulent flow; rotor effects if a multirotor is selected | Wake structures, surface pressure, and flow around the aircraft | Lift/drag or thrust/torque, depending on the selected aircraft |
| Room fire | Building ventilation and fire engineering | Buoyant hot gases, heat transfer, combustion or a prescribed fire source, and smoke transport | Plume development, ceiling layer, and exchange through door/windows | Temperature histories, opening fluxes, and smoke-layer development |
| Urban pollutant dispersion | Urban air quality and ventilation | Atmospheric flow around buildings with pollutant transport | Plume transport, recirculation, and concentration at pedestrian level | Concentration at receptors and pollutant mass balance |

Regional relevance will come from the application, geometry, operating conditions, and comparison being studied. Specific climate data or real locations must be sourced when selected.

## 1. Reactor with species transport and Volume of Fluid

### Intended showcase

A transparent cutaway of a reactor showing the evolving liquid–gas interface and species concentration. Candidate applications include a partially filled mixing/contact vessel for water treatment or chemical processing.

**Working interpretation:** “colune of fluid” means **Volume of Fluid (VOF)**. Confirm this before selecting the reactor.

### Modelling decisions

- Select the reactor purpose, geometry, fluids, and species.
- Decide whether the target is liquid-phase mixing, gas–liquid transfer, or reactive conversion.
- Preserve the requested VOF objective while assessing whether the important interfaces can be resolved at an affordable mesh size.
- Species mixing within one phase and species transfer across an interface are separate modelling requirements.
- Do not assume that VOF, species transport, reaction, and interphase transfer are available together in one standard OpenFOAM 13 configuration. Audit the shipped modules and select only a supported combination; revise the proposed scope if needed.
- A fine dispersed-bubble reactor may call for an Eulerian multiphase approach; that would be a proposed scope change requiring discussion.

### Development stages

1. Establish geometry and nonreacting interface dynamics.
2. Add conservative species transport in the intended phase.
3. Add interphase transfer or reaction only if supported by the selected stock OpenFOAM 13 configuration, with a defined verification target.
4. Compare one meaningful design or operating choice.

### Evidence to show

Phase-volume conservation, bounded phase fractions and concentrations, species mass balance, and sensitivity of a chosen output to mesh and timestep. Report mixing time, uptake, or conversion only when the corresponding physics is included.

**Relative effort:** provisional medium to high, depending on the supported configuration selected. Custom development is excluded.

## 2. Drone aerodynamics

### Intended showcase

A civil drone in flight conditions, showing surface pressure and its wake. Possible application: inspection of solar farms or industrial infrastructure.

### Selected first concept

A **complete fixed-wing UAV**, spanning 1.8 m, with fuselage, main wing, horizontal tail, and vertical stabiliser. The original parametric CAD source is [geometry/drone_geometry.py](geometry/drone_geometry.py); it uses CadQuery 2.7 to export STEP and STL in metres. These geometry tools do not change the OpenFOAM solver.

The initial aerodynamic question is how angle of attack changes whole-aircraft lift, drag, and wake at a defined flight speed. The provisional sweep is 0°, 5°, and 10°, subject to pilot-run results. The geometry omits propeller and thrust, so forces describe an **unpowered airframe in prescribed oncoming flow**. No wing-only precursor case is planned.

Use steady RANS first, with the stock OpenFOAM 13 `incompressibleFluid` module and built-in force/force-coefficient reporting after a release-specific dictionary check. Select turbulence model, wall treatment, flight speed, reference area, and angle-of-attack convention before case preparation. A transient RANS run can be added for physical wake evolution. LES is outside the first case scope because its wall and wake resolution would be substantially more expensive.

**Geometry status:** the CAD source was executed locally; the union is one valid solid. Its STL has 47,014 triangles, one connected region, and zero boundary or nonmanifold edges in a VTK check. This verifies surface closure, not mesh suitability or aerodynamic accuracy. Inspect trailing edges and local refinement before meshing. Generated STEP/STL are rebuilt from the source and are not committed to Git.

```bash
python3 geometry/drone_geometry.py build/drone
```

### Development stages

1. Use and inspect the original parametric full-aircraft geometry.
2. Establish a baseline mesh and aerodynamic calculation.
3. Define reference area, centre of moments, and whole-aircraft force decomposition.
4. Use a transient calculation if the movie is intended to show time-dependent wake physics.

Animating particles through a steady velocity field is a visualization of that field; it must not be described as a resolved unsteady wake.

### Evidence to show

Force convergence or statistical stability, appropriate near-wall treatment, domain and mesh sensitivity, and comparison with suitable reference data where available.

**Relative effort:** medium for the proposed full-aircraft RANS sweep.

## 3. Fire in a room with windows and a door

### Intended showcase

A furnished or simplified room with a defined fire location, door, and windows. Show plume rise, accumulation beneath the ceiling, and exchange with the outside.

### Modelling decisions

- Start with a prescribed fire source of defined heat-release history, or select a combustion model with prescribed fuel supply.
- Distinguish a hot-gas/tracer demonstration from a model that explicitly predicts combustion and soot.
- Select wall thermal treatment, radiation, and smoke representation.
- Include enough exterior space to represent exchange through the openings.
- Use an established compartment-fire benchmark to guide verification before adding presentation details.

### Development stages

1. Verify buoyant flow and opening boundary conditions.
2. Add the selected fire and heat-transfer models.
3. Compare two defined ventilation configurations, such as different window openings.
4. Produce synchronized smoke/tracer and temperature views.

### Evidence to show

Energy and mass balances, temperature histories, opening flow direction and flux, and sensitivity to mesh and timestep. Label prescribed versus predicted quantities clearly. The initial scope is an engineering demonstration; safety or tenability conclusions need additional validation and modelling.

**Relative effort:** medium to high, depending on combustion, radiation, and soot scope.

## 4. Pollutant dispersion in a small city model

### Intended showcase

A compact district inspired by Middle Eastern urban layouts, with a defined pollutant source and wind direction. Show how streets, courtyards, and building heights influence ventilation and concentration.

### Initial scope

- Use an idealized district whose geometry can be regenerated.
- Establish atmospheric inflow, ground roughness, and consistent turbulence boundary conditions.
- Begin with a dilute passive gaseous pollutant.
- Select a traffic-like line source or a defined point source.
- Consider dust settling, deposition, and chemical reactions later only where the selected stock OpenFOAM 13 configuration supports them.

### Development stages

1. Verify the atmospheric inlet in an empty domain.
2. Add buildings and establish the flow.
3. Add pollutant transport and monitor receptors.
4. Compare two wind directions or two urban layouts.
5. Use transient output if showing physical plume fluctuations.

### Evidence to show

Source strength, pollutant mass balance, receptor histories or averages, domain and mesh sensitivity, and the averaging interval where relevant.

**Relative effort:** medium for an idealized district; higher for detailed real-city geometry or resolved transient turbulence.

## Proposed development order

This order is a proposal, not an approved execution schedule:

1. **Urban dispersion:** establish the shared geometry, meshing, scalar-transport, and rendering workflow.
2. **Drone aerodynamics:** add external-flow geometry and aerodynamic outputs.
3. **Reactor:** develop the coupled interface/species workflow after the OpenFOAM 13 feasibility audit.
4. **Room fire:** add combustion or prescribed fire modelling, radiation, and thermal boundaries.

Before implementation, select the first case and agree on its minimum credible scope. Runtime and cell-count estimates will follow a pilot mesh and short test on the chosen hardware.

## Common workflow for every case

1. **Case brief:** physical question, geometry, operating conditions, assumptions, and comparison.
2. **OpenFOAM 13 audit:** exact shipped solver/module, compatible built-in models, and version-13 tutorial reference. Resolve missing functionality by revising the scope.
3. **Geometry and mesh:** reproducible source, named boundaries, refinement strategy, and mesh-quality report.
4. **Pilot run:** confirm stability, conservation, outputs, and compute cost.
5. **Verification:** check the quantities that support the intended claim; perform targeted mesh/timestep checks.
6. **Production run:** use documented settings and retain sufficient data for the planned movie.
7. **Rendering:** reproducible ParaView camera, colour maps, annotations, and export settings.
8. **Case summary:** explain the physical result, simplifications, and evidence in one presentation slide.

## Presentation deliverables

For each completed case:

- A short presentation movie, provisionally 20–40 seconds, at 1080p.
- A geometry/mesh view and a clearly labelled physical-results view.
- A physical time label for transient results; explicitly label steady-flow visualizations.
- Fixed colour limits and matched camera views for comparisons.
- One compact plot or numerical result supporting the visual story.
- A short README with the engineering question, model, commands, result, and limitations.
- Reproducible rendering scripts or saved ParaView state.

A final combined reel can introduce all four applications with a consistent visual style.

## Proposed repository organization

To be created during implementation:

- `docs/`: modelling decisions, references, and portfolio storyboard.
- `cases/reactor/`
- `cases/drone/`
- `cases/room_fire/`
- `cases/urban_dispersion/`
- `geometry/`: reusable geometry-generation sources.
- `scripts/`: shared utilities where genuinely useful.
- `visualization/`: rendering scripts and ParaView states.
- `media/`: selected compact preview images and links to final movies.

Keep large meshes, transient fields, and rendered frame sequences out of ordinary Git history. Choose a suitable storage/release strategy when results exist.

## Decisions before case preparation

- [ ] Confirm that VOF is intended for the reactor.
- [ ] Select the reactor application and whether interphase transfer/reaction is required.
- [x] Select a full fixed-wing drone for the first airframe study.
- [ ] Define the fire-source and smoke modelling scope.
- [ ] Select an idealized district and pollutant source.
- [ ] Select the first case.
- [ ] Identify available compute resources and acceptable runtime/storage.
- [ ] Check exact OpenFOAM Foundation 13 capabilities for the selected case.

## Progress

- [x] Record the initial portfolio plan.
- [x] Select the drone as the first case and steady RANS as the starting approach.
- [ ] Complete the release-specific feasibility audit.
- [x] Create and check the parametric full-drone surface geometry.
- [ ] Prepare and verify the first simulation case.
- [ ] Produce the first presentation movie.

Planning baseline: 3 October 2026.
