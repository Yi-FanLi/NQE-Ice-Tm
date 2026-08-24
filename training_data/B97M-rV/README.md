# B97M-rV training data

The B97M-rV Deep Potential committee was trained on 1,281 configurations of
64 water molecules. All configurations were sampled from quantum simulations
and are separated by phase:

| Directory | Configurations | Provenance |
| --- | ---: | --- |
| `alldata/quantum_liq/deepmd_data` | 825 | 590 initial configurations and 235 DP-GEN configurations |
| `alldata/quantum_ice/deepmd_data` | 456 | 347 initial configurations and 109 DP-GEN configurations |

The two initial datasets were generated from quantum simulations. The 109
DP-GEN ice configurations comprise 83 configurations selected in iteration 0
and 26 configurations carried from later quantum-ice exploration.

Each phase directory contains the same labels in both `deepmd/raw` and
`deepmd/npy` formats. The type map is `O H`, and every configuration has 64 O
and 128 H atoms. Energy and force labels are provided. Virials are omitted
because they were not available for the initial quantum datasets.

`dataset_manifest.json` records the source systems and configuration counts.
`export_dataset.py` reproduces the phase-resolved export from the completed
DP-GEN work directory using dpdata.
