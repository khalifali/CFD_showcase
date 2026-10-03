# CFD Showcase — OpenFOAM 13

## Purpose

Develop a portfolio of reproducible CFD simulations relevant to engineering applications in the Middle East, with clear, visually compelling movies for professional presentations and self-marketing.

The portfolio will demonstrate geometry creation, meshing, physical modelling, numerical verification, interpretation of results, and scientific visualization.

**Status: planning only.** No simulation cases have been prepared or run.

**Platform:** OpenFOAM Foundation version 13. Solver modules, models, dictionary syntax, and tutorial starting points must be checked against this exact release before implementation. This is an independent project.

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
- Do not assume that VOF, species transport, reaction, and interphase transfer are available together in one standard OpenFOAM 13 configuration. Audit the available modules and identify any required extension first.
- A fine dispersed-bubble reactor may call for an Eulerian multiphase approach; that would be a proposed scope change requiring discussion.

### Development stages

1. Establish geometry and nonreacting interface dynamics.
2. Add conservative species transport in the intended phase.
3. Add interphase transfer or reaction only after defining a physical model and verification target.
4. Compare one meaningful design or operating choice.

### Evidence to show

Phase-volume conservation, bounded phase fractions and concentrations, species mass balance, and sensitivity of a chosen output to mesh and timestep. Report mixing time, uptake, or conversion only when the corresponding physics is included.

**Relative effort:** high, particularly if coupled VOF and interphase species transfer require development.

## 2. Drone aerodynamics

### Intended showcase

A civil drone in flight conditions, showing surface pressure and its wake. Possible application: inspection of solar farms or industrial infrastructure.

### Choice still open

- **Fixed-wing drone:** lift, drag, separation, and wake over a small range of incidence angles.
- **Multirotor drone:** rotor-generated flow, thrust, and interactions with the body or ground.

### Development stages

1. Select a geometry with a clear source and reuse licence, or generate an original parametric geometry.
2. Establish a baseline mesh and aerodynamic calculation.
3. For multirotors, choose the rotor representation explicitly: actuator approximation, rotating reference frame, or resolved moving blades.
4. Use a transient calculation if the movie is intended to show time-dependent wake physics.

Animating particles through a steady velocity field is a visualization of that field; it must not be described as a resolved unsteady wake.

### Evidence to show

Force convergence or statistical stability, appropriate near-wall treatment, domain and mesh sensitivity, and comparison with suitable reference data where available.

**Relative effort:** medium for a fixed-wing baseline; high for resolved transient multirotor flow.

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
- Treat dust settling, deposition, and chemical reactions as possible later extensions, each requiring additional models.

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
2. **OpenFOAM 13 audit:** exact solver/module, supported models, tutorial reference, and any missing functionality.
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
- [ ] Select fixed-wing or multirotor drone.
- [ ] Define the fire-source and smoke modelling scope.
- [ ] Select an idealized district and pollutant source.
- [ ] Select the first case.
- [ ] Identify available compute resources and acceptable runtime/storage.
- [ ] Check exact OpenFOAM Foundation 13 capabilities for the selected case.

## Progress

- [x] Record the initial portfolio plan.
- [ ] Agree on the first case and modelling scope.
- [ ] Complete the release-specific feasibility audit.
- [ ] Prepare and verify the first simulation case.
- [ ] Produce the first presentation movie.

Planning baseline: 3 October 2026.
