# ElectronScattering

**Electron multiple-scattering benchmark against the NRC Canada EGS measurements**
(T. O'Shea and B. Faddegon), with the updated physics list and foil-geometry fixes
from J. Ramos-Mendez.

---

## 📚 Reference

- Geometry: see `NRCC_electron_scat.pdf` (the `electronScattering` Geant4 example
  this test is built from).
- Included in G4-Med: P. Arce et al., *Med. Phys.*, vol. 48, iss. 1, pp. 19–56,
  Jan. 2021. [https://doi.org/10.1002/mp.14226](https://doi.org/10.1002/mp.14226)

## 🔬 What this test does

A mono-energetic 13 MeV electron pencil beam hits a thin scattering foil (one of
Aluminum, Beryllium, Copper, Gold, Graphite, Tantalum or Titanium) followed by an
exit window, inside the frame geometry of the original NRCC benchmark. The radial
fluence distribution of charged particles at the scoring plane downstream of the
foil is recorded and compared with EGSnrc measurements at 13 MeV
(`validation/EGS_13MeV` — not present in this adaptation, see the original
`geant-validation-tests/src/ElectronScattering/EGS_13MeV` for the reference data).

Physics lists compared: `GoudsmitSaunderson` (the model this benchmark was built
for), `penelope`, `livermore`, `emstandard_opt0` and `emstandard_opt4` (from
`geant4/source/physics_lists/builders`); `emstandard_opt3` is also supported by
`PhysicsList` but has no macro here. Foil material, thickness, exit-window
material and physics list are set via the UI commands in each macro (see
`macro/run_option.mac` for the parameterized template they come from).

Four 1D histograms are filled per run (angle, dN/dS, d(N/cosθ)/dS and its
normalized form); `Run::PrintFluence` always writes the normalized radial fluence
table as `<name>.root.ascii` next to the histogram file, independently of the
`/analysis/h1/setAscii` command. This ascii table is what `validation/parser.py`
reads.

## 🚀 How to run the container

```bash
apptainer build --build-arg PROJECT_NAME=ElectronScattering ElectronScattering.sif Apptainer.def
apptainer run -B /path/to/geant4_data:/g4data:ro ElectronScattering.sif macro/Aluminum_GoudsmitSaunderson.mac
```

See the top-level [template README](https://github.com/G4Med-test/template#readme)
for the full local workflow (pulling the CI-built container, mounting Geant4
datasets, and running `ci-workflows/validation/export.py`).

## 📦 Container on GHCR

[![Container on GHCR](https://img.shields.io/badge/Container-GHCR-blue?logo=github)](https://github.com/orgs/G4Med-test/packages?repo_name=ElectronScattering)

```bash
apptainer pull oras://ghcr.io/g4med-test/electronscattering:<tag>
```
> Replace `<tag>` with the desired release tag or commit hash.

## ✅ GitHub Actions workflow

Defined in the shared [`ci-workflows`](https://github.com/G4Med-test/ci-workflows)
repository and invoked from [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
