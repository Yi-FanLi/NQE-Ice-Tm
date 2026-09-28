# Independent revPBE0-D3 AIMD test sets

These are the independent liquid-water and ice-Ih reference configurations
used to test the models in [the water/ice training-dataset paper](https://github.com/Yi-FanLi/MLIP-training-dataset-matters-water-ice),
Supporting Information section "Independent AIMD Test Sets".
They are evaluation data, separate from SET2 and SET3 training data.

| Reference-label cutoff | Liquid water | Ice Ih | Models compared in the paper |
| --- | ---: | ---: | --- |
| [400 Ry](400Ry/) | 50 | 50 | Original BPNN1 and NEP |
| [800 Ry](800Ry/) | 50 | 50 | DP and SET3-trained BPNN3 |

Each configuration contains 64 H2O molecules (192 atoms). Configurations
were sampled from NpT AIMD at 300 K and 1 bar. The two cutoff directories
provide their respective reference labels; use 800 Ry when testing a model
trained on SET3. Do not mix the 400 Ry labels with the 800 Ry labels when
reporting errors.

## Layout and units

Each cutoff contains `liq/` and `ice/`, each with:

- `deepmd_data_raw/`: original DeePMD raw files, copied without modification.
  `coord.raw` and `force.raw` have one configuration per row, with 3 components
  per atom. `box.raw` has nine cell-vector components per row. `energy.raw`
  is the total cell energy. `type.raw` contains zero-based atom-type indices;
  `type_map.raw` maps them to O and H.
- `reference.xyz`: equivalent extended XYZ, with lattice, species, positions,
  forces, total energy, and periodic boundary conditions. Configuration and
  atom order are preserved. No energy shift is applied.

Units are angstrom for coordinates and cells, eV for total cell energies,
and eV/angstrom for force components. Full cell matrices are retained,
including the variable-cell ice configurations. Energies per atom for parity
plots are obtained by dividing the total energies by 192.

## Reference method and provenance

The paper specifies CP2K 2022.1, revPBE0-D3 with zero-damping D3, ADMM exact
exchange, GTH pseudopotentials, TZV2P-GTH orbital and cpFIT3 auxiliary basis
sets, and an SCF threshold of 5e-7 hartree. The cutoff is identified by the
400Ry/800Ry parent directory.

The source files are the reference datasets retained with the 26 August 2026
BPNN3 AIMD evaluation: `reference/test-data/` (800 Ry) and
`reference/test-data-400Ry/` (400 Ry). The 800 Ry energy and force labels were
also checked against the reference columns in the archived DP evaluation
outputs. These data reproduce the energy/force tests; original AIMD
trajectories and CP2K outputs are not included here.

`SHA256SUMS` covers the released data files and this README. From this
directory run `shasum -a 256 -c SHA256SUMS` or `sha256sum -c SHA256SUMS`.
