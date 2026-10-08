#!/usr/bin/env python

# ElectronScattering portal parser: metadata() reads the macro, parse() the
# ".root.ascii" fluence table written by Run::PrintFluence at the end of the run.
import os

from geantval import energy_mev, getJSON, one_command, single_run

NAMES = {
    "Titanium": "Ti",
    "Gold": "Au",
    "Graphite": "C",
    "Tantalum": "Ta",
    "Beryllium": "Be",
    "Aluminum": "Al",
    "Copper": "Cu",
}

PLISTS = {
    "penelope": "empenelope",
    "livermore": "emlivermore",
    "GoudsmitSaunderson": "emstandardGS",
    "emstandard_opt0": "emstandard_opt0",
    "emstandard_opt4": "emstandard_opt4",
}


def extract_fluence(filename):
    rad, fluence, norm_fluence = [], [], []
    with open(filename) as myfile:
        for line in myfile:
            fields = line.split()
            if len(fields) == 7:
                rad.append(float(fields[2]))
                fluence.append(float(fields[4]))
                norm_fluence.append(float(fields[5]))
    if not rad:
        raise ValueError("Empty fluence output: " + filename)
    return rad, fluence, norm_fluence


def parse(job):
    filename = job["MATERIAL"] + "_" + job["PHYSLIST"] + ".root.ascii"
    filepath = os.path.join(job["path"], filename)
    print("Parsing", filepath)
    rad, fluence, norm_fluence = extract_fluence(filepath)

    yield getJSON(job, "chart",
                 mctool_name="GEANT4",
                 mctool_model=PLISTS[job["PHYSLIST"]],
                 observableName="radial fluence",
                 targetName=NAMES[job["MATERIAL"]],
                 beamParticle=job["PARTICLE"],
                 beamEnergies=[job["ENERGY"]],
                 secondaryParticle="None",
                 title="radial fluence",
                 xAxisName="position (mm)",
                 yAxisName="",
                 xValues=rad,
                 yValues=fluence)

    yield getJSON(job, "chart",
                 mctool_name="GEANT4",
                 mctool_model=PLISTS[job["PHYSLIST"]],
                 observableName="radial fluence (normalized)",
                 targetName=NAMES[job["MATERIAL"]],
                 beamParticle=job["PARTICLE"],
                 beamEnergies=[job["ENERGY"]],
                 secondaryParticle="None",
                 title="radial fluence (normalized)",
                 xAxisName="position (mm)",
                 yAxisName="",
                 xValues=rad,
                 yValues=norm_fluence)


def metadata(commands):
    single_run(commands)
    physlist = one_command(commands, "/testem/phys/addPhysics")
    if physlist not in PLISTS:
        raise ValueError("Unsupported physics list for this validation: " + physlist)
    material = one_command(commands, "/testem/det/setScatteringFoilMaterial")
    if material not in NAMES:
        raise ValueError("Unsupported scattering material for this validation: " + material)
    expected_name = material + "_" + physlist
    if one_command(commands, "/analysis/setFileName") != expected_name:
        raise ValueError("Expected /analysis/setFileName " + expected_name)
    return {"TEST": "ElectronScattering",
            "PHYSLIST": physlist,
            "MATERIAL": material,
            "WINDOW_MATERIAL": one_command(commands, "/testem/det/setExitWindowMaterial"),
            "PARTICLE": one_command(commands, "/gun/particle"),
            "ENERGY": energy_mev(one_command(commands, "/gun/energy"))}
