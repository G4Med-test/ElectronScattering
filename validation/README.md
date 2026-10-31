# Portal JSON parser

Adapted from `geant-config-generator/tests/geant4/ElectronScattering/parser.py` at
commit `0bf42953c9c98ac6ecccf077e7c7fe2c4ceb7307`, with queue discovery replaced by
the shared ci-workflows exporter.

`config.json` selects the GoudsmitSaunderson run of the five materials with
experimental data in `EGS_13MeV/` (Aluminum, Beryllium, Titanium, Gold, Graphite);
the other 30 material/physics-list combinations in `macro/` are kept for manual or
Padova runs but are not run automatically. The macros are the original ones from
`geant-validation-tests/src/ElectronScattering`, unchanged apart from dropping the
`results/` output directory from `/analysis/setFileName` (the pipeline runs each
macro in a fresh, already-existing directory and never creates subdirectories).

The parser reads `<MATERIAL>_<PHYSLIST>.root.ascii`: the ascii fluence table that
`Run::PrintFluence` writes next to the (default ROOT-format) histogram file at the
end of every run, independently of any `/analysis/h1/setAscii` command. Geant4's
built-in ROOT writer (`g4tools`) needs no ROOT installation. Columns are `ibin`,
`angle`, `radius (mm)`, `Nb`, `fluence`, `norm fluence`, `rms/nfl (%)`; the parser
keeps radius, fluence and normalized fluence, exactly as the original parser did.
Physics list and material names are mapped to the portal's historical
`mctool_model` and `targetName` values (`emstandardGS`, `empenelope`,
`emlivermore`, and the element symbols). Energy, particle and exit-window material
come from the macro; `metadata()` rejects a macro whose `/analysis/setFileName`
does not match `<material>_<physlist>`, or that beams to more than one run.

The pipeline uploads `validation-json/results.json` (an array of plot objects)
and `plots/*.json` (the original one-object-per-file format), plus raw artifacts.
See [ci-workflows](https://github.com/G4Med-test/ci-workflows) for local CLI usage.
