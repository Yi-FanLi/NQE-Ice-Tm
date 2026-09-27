# SET3: final revPBE0-D3 BPNN training dataset

This is the frozen `iter04` dataset used for BPNN3 in
[Training Dataset Matters for Machine Learning Potential: Water Simulation as an Example](https://github.com/Yi-FanLi/MLIP-training-dataset-matters-water-ice).
It contains 2,556 periodic configurations, each with 64 H2O molecules
(128 H atoms and 64 O atoms), reference energies, and atomic forces.

## What SET2 means

SET2 is the 1,778-configuration dataset generated through DP active learning
and used to train the paper's DP model and BPNN2. It is available in
[`../alldata/`](../alldata/), in DeePMD format. The `init/` subset contributes
100 classical-water configurations and must be included in SET2.
SET3 retains all SET2 configurations and adds 778 BPNN active-learning
configurations. The inherited data were converted to n2p2 format; numerical
comparison with the existing SET2 files confirms matching cells, coordinates,
energies, and forces within text precision, allowing atom reordering.

| Category | SET2 | Added | SET3 |
| --- | ---: | ---: | ---: |
| Classical liquid water | 179 | 492 | 671 |
| Quantum liquid water | 826 | 197 | 1,023 |
| Classical ice | 3 | 0 | 3 |
| Quantum ice | 770 | 89 | 859 |
| **Total** | **1,778** | **778** | **2,556** |

The additions comprise 492 configurations from `iter01`, 236 from `iter02`,
30 from `iter03`, and 20 from `iter04`. Their local provenance identifies
revPBE0-TC-D3 labels at an 800 Ry cutoff. The final four-seed committee was
trained for 200 epochs, with random seeds 123456, 223456, 323456, and 423456.
The production [BPNN3 model](../../../models/revPBE0-D3/BPNN3/) uses seed 123456.

## Files and units

- `input.data`: unchanged frozen n2p2 dataset. Each `begin`/`end` block contains
  three `lattice` vectors, `atom` records, total `energy`, and `charge`.
  Lengths are in bohr, total energies in hartree, and forces in hartree/bohr.
  Atom records contain x, y, z, element, charge, atomic-energy placeholder,
  Fx, Fy, Fz. The atomic-energy field is not an atomic reference-energy label.
- `configuration_index.tsv`: one row per block, with category, source iteration,
  and available sampling provenance. `global_index_zero_based` starts at 0;
  `configuration_number_one_based` starts at 1. For the inherited SET2 frames,
  `set2_source_file` and `set2_source_index_zero_based` identify the corresponding
  DeePMD source directory and frame. Blank provenance fields were not recorded.
- `indices_zero_based/` and `indices_one_based/`: configuration indices grouped
  by phase and nuclear treatment.
- `SHA256SUMS`: checksums for the files in this directory tree.

SET2's DeePMD files instead use angstrom, eV, and eV/angstrom. The conversion
constants used for the comparison are 1 bohr = 0.529177210903 angstrom and
1 hartree = 27.211386245988 eV. `energy` is the total cell energy, not energy
per atom or per water molecule.

## Ordering and metadata correction

The first 1,778 blocks are SET2, in the following actual order:

| Zero-based indices (inclusive) | SET2 source under `../alldata/` |
| --- | --- |
| 0–99 | `init/deepmd_data/` |
| 100–178 | `classical_liq/deepmd_data/` |
| 179–1004 | `quantum_liq/deepmd_data/` |
| 1005–1774 | `quantum_ice/deepmd_data/` |
| 1775–1777 | `classical_ice/deepmd_data/` |

The local pre-publication category metadata incorrectly placed classical ice
at indices 1005–1007. This public index corrects the inherited ice labels using
configuration-level comparison with SET2. Configuration counts and the bytes
of `input.data` are unchanged. Five repeated geometry occurrences inherited
from the base corpus are retained, as in the dataset used for training.

The frozen `input.data` is 69,831,177 bytes with SHA-256:

```text
8a2af01e382851ce37bc987420c84e28b680d4fade1bd42ead3ee66d0bacb36c
```

From this directory, verify the download with `shasum -a 256 -c SHA256SUMS`
(or `sha256sum -c SHA256SUMS` on Linux).
