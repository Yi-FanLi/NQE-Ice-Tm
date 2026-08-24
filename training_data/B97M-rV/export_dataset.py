#!/usr/bin/env python3
"""Export the B97M-rV training set with phase and quantum provenance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import dpdata


PHASE_SOURCES = {
    "quantum_liq": (
        "init_data/liquid/O64H128",
        "dpgen-workdir/iter.000000/02.fp/data.000/O64H128",
    ),
    "quantum_ice": (
        "init_data/ice/O64H128",
        "dpgen-workdir/iter.000000/02.fp/data.001/O64H128",
        "dpgen-workdir/iter.000004/02.fp/data.001/O64H128",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_root",
        type=Path,
        help="B97M-rV dpgen-active-learning directory containing init_data and dpgen-workdir",
    )
    parser.add_argument(
        "output_root",
        type=Path,
        help="New directory in which alldata/<phase>/deepmd_data will be created",
    )
    return parser.parse_args()


def load_system(path: Path) -> dpdata.LabeledSystem:
    system = dpdata.LabeledSystem(
        str(path), fmt="deepmd/npy", type_map=["O", "H"]
    )
    # The initial quantum datasets did not contain virials.  The published
    # phase-resolved datasets therefore use the common energy/force label set.
    system.data.pop("virials", None)
    if system.data["atom_names"] != ["O", "H"]:
        raise ValueError(f"Unexpected type map in {path}: {system.data['atom_names']}")
    if system.data["atom_numbs"] != [64, 128]:
        raise ValueError(f"Unexpected composition in {path}: {system.data['atom_numbs']}")
    return system


def main() -> None:
    args = parse_args()
    source_root = args.source_root.resolve(strict=True)
    output_root = args.output_root.resolve()
    if output_root.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {output_root}")

    summary: dict[str, object] = {
        "functional": "B97M-rV",
        "sampling": "quantum",
        "type_map": ["O", "H"],
        "atom_numbs": [64, 128],
        "phases": {},
    }

    for phase, relative_sources in PHASE_SOURCES.items():
        systems = []
        source_counts = []
        for relative_source in relative_sources:
            source = source_root / relative_source
            system = load_system(source)
            systems.append(system)
            source_counts.append(
                {"source": relative_source, "configurations": len(system)}
            )

        merged = systems[0]
        for system in systems[1:]:
            merged.append(system)

        destination = output_root / "alldata" / phase / "deepmd_data"
        destination.mkdir(parents=True)
        merged.to_deepmd_raw(str(destination))
        merged.to_deepmd_npy(str(destination), set_size=len(merged))
        phase_summary = {
            "configurations": len(merged),
            "sources": source_counts,
        }
        summary["phases"][phase] = phase_summary

    summary["total_configurations"] = sum(
        phase["configurations"] for phase in summary["phases"].values()
    )
    with (output_root / "dataset_manifest.json").open("w") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
