# Description
This repo stores the models, job scripts, and data for our manuscripts:

[Training Dataset Matters for Machine Learning Potential: Water Simulation as an Example](https://github.com/Yi-FanLi/MLIP-training-dataset-matters-water-ice)

Assessment of First-Principles Methods in Modeling the Melting Properties of Water, Yifan Li, Bingjia Yang, Chunyi Zhang, Pinchen Xie, Yixiao Chen, Pablo M. Piaggi, and Roberto Car

Ab Initio Melting Properties of Water and Ice from Machine Learning Potentials, Yifan Li, Bingjia Yang, Chunyi Zhang, Pinchen Xie, Yixiao Chen, Pablo M. Piaggi, and Roberto Car

## Table of Contents
### `dft_inputs`
This folder contains versioned CP2K labeling inputs organized by density functional.

### `models`
This folder contains Deep Potential models based on the revPBE-D3,
revPBE0-D3, SCAN, SCAN0, and B97M-rV density functionals. The B97M-rV
directory contains a four-seed model committee. The production BPNN3 model
trained on SET3 is in [`models/revPBE0-D3/BPNN3/`](models/revPBE0-D3/BPNN3/).

### `training_data`
This folder contains the corresponding DFT-labeled training data.

## SET2 and SET3 for the water/ice training-dataset paper

**SET2** is the 1,778-configuration revPBE0-D3 dataset obtained through Deep
Potential (DP) active learning. It is the training set for the paper's DP model
and BPNN2, and the starting dataset for the BPNN active-learning extension.
SET2 is already stored in
[`training_data/revPBE0-D3/alldata/`](training_data/revPBE0-D3/alldata/);
there is no separate `SET2/` directory.

**SET3** is SET2 plus 778 configurations added through BPNN active learning,
for a total of 2,556 configurations. The frozen final iteration (`iter04`)
is in [`training_data/revPBE0-D3/SET3/`](training_data/revPBE0-D3/SET3/)
and is the training set for BPNN3.

| Configurations | SET2 | SET3 | Existing SET2 location under `alldata/` |
| --- | ---: | ---: | --- |
| Classical liquid water | 179 | 671 | `init/deepmd_data/` (100) + `classical_liq/deepmd_data/` (79) |
| Quantum liquid water | 826 | 1,023 | `quantum_liq/deepmd_data/` |
| Classical ice | 3 | 3 | `classical_ice/deepmd_data/` |
| Quantum ice | 770 | 859 | `quantum_ice/deepmd_data/` |
| **Total** | **1,778** | **2,556** | |

Here "quantum" denotes configurations sampled using path-integral molecular
dynamics. Both sets contain DFT reference energies and forces. SET2 uses the
existing DeePMD format (angstrom, eV, eV/angstrom); SET3 is supplied as an n2p2
`input.data` file (bohr, hartree, hartree/bohr). See the
[SET3 README](training_data/revPBE0-D3/SET3/README.md) for indexing, provenance,
and checksums. The existing SET2 data and DP model remain at their original paths.

## Independent AIMD test data

[`test_data/revPBE0-D3/`](test_data/revPBE0-D3/) provides the independent
300 K, 1 bar AIMD test sets: 50 liquid-water and 50 ice-Ih configurations
(64 H2O each), with separate 400 Ry and 800 Ry reference labels. Both the
original DeePMD raw files and extended XYZ files are included. These are
held-out evaluation data, distinct from SET2 and SET3. Use the 800 Ry
references for SET3-trained models; the original BPNN1/NEP comparisons use
400 Ry references.
