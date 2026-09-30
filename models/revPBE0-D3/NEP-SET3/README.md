# SET3-trained NEP used in the water/ice paper

This directory releases the **single NEP used for the paper's SET3 validation
and density calculations** (SI Section S6, Figures S8 and S9). No other NEP
training runs or committee models are included.

The production potential is `nep.txt`, SHA-256
`d2e95382e117e9657a60cddf748d87cd3e765177214cfaaf77e8ff0197085f7a`.
It was trained from scratch for 400,000 generations on all 2,556 configurations
of [SET3](../../../training_data/revPBE0-D3/SET3/), with batch size 25,
population 52, and four A100 GPUs in one NEP process. The exact input is
`training/nep.in`; the archived learning curve is `training/loss.out`.
`training/nep.restart` is the final optimizer checkpoint, not a fresh-training
input. The native training executable uses a wall-clock random seed that was
not recorded; a fresh fit reproduces the protocol, not the exact model bytes.
Use the released potential to reproduce the reported predictions and MD.

## Contents and units

- `training/`: exact NEP input, compressed training/monitoring XYZ files,
  final checkpoint, learning curve, training log and completion marker.
- `evaluation/{training,liq,ice}/`: full-dataset prediction inputs and archived
  energy/force predictions. The liquid and ice sets have 50 configurations
  each, with independent **800 Ry** DFT labels. These configurations were
  not added to SET3. The training-time `test.xyz` contains these same 100
  configurations, monitored during fitting; they are held out from the
  training loss, not an unseen final audit set.
- `md/{water,ice}/`: exact `run.in`, 64-H2O starting structure, complete
  compressed thermodynamic output and completion marker. The ice coordinate
  trajectory is also included for the reported crystalline-order diagnostics.
- `scripts/`, `data/nep_set3/`, `figures/`: reproducible analysis and figure
  notebooks, derived data, and the paper's PDF/PNG figures.
- `GPUMD_COMMIT`, `provenance.json`, `energy_reference.json`, `SHA256SUMS`:
  code version, model identity, energy convention, and integrity checks.

XYZ positions/cells are in angstrom, energies in eV per configuration, and
forces in eV/angstrom. NEP prediction energy columns are prediction/reference
in eV/atom; force columns are predicted x/y/z then reference x/y/z in
 eV/angstrom. The fixed offset is **e0 = -156.39267947333917 eV/atom**:
`E_training = E_DFT - N_atoms * e0`. Add `e0` to both prediction and reference
energy-per-atom columns to restore absolute DFT energies. Forces are unchanged.
No fitted energy alignment is used. Unshifted independent test data are in
[`test_data/revPBE0-D3`](../../../test_data/revPBE0-D3/).

## Software

Use GPUMD source commit `fd63d2c61e773e59803e76d57a0edcea0fca874d`
(also in `GPUMD_COMMIT`). The original build used CUDA 12.9. For example,
clone https://github.com/brucefan1983/GPUMD.git, check out this commit, and
build `nep` and `gpumd` in `src` using `make` with a compatible CUDA toolkit.
Analysis requires Python 3.10+, NumPy and Matplotlib. The supplied notebook
runner requires no Jupyter installation. Times New Roman is used for the
paper figures; without that font Matplotlib substitutes an available font.

## Recompute the reported results without running MD

From this directory:

```sh
shasum -a 256 -c SHA256SUMS
python scripts/prepare_results.py
python scripts/render_figures.py
gunzip -k md/ice/dump.xyz.gz
python scripts/analyze_structure.py . --phase ice
```

The archived full-training RMSEs are **0.454724 meV/atom** (energy) and
**51.522420 meV/angstrom** (force components). Independent-test RMSEs are
**0.571209 / 37.336248** for water and **0.260811 / 28.837420** for ice,
in the same respective units. Figures show only the independent test sets.
All force components have equal weight in the reported RMSE.

## Run predictions, fresh training, or density MD

Prepare a new destination (it must not already exist):

```sh
python scripts/prepare_runs.py /path/to/new-nep-runs
```

On an allocated GPU node, run the compiled `nep` executable in each
`/path/to/new-nep-runs/evaluation/{training,liq,ice}` directory to evaluate
the released potential (`prediction 1`). Run `nep` in
`/path/to/new-nep-runs/training/fresh` to train from scratch. The original
training allocation exposed four A100 GPUs to one process; do not launch
four independent NEP processes. The generated fresh-training directory
intentionally contains no potential or optimizer restart.

Run the compiled `gpumd` executable separately in
`/path/to/new-nep-runs/md/water` and `.../md/ice`, using one GPU per MD run.
The input specifies the released potential and the original velocity seeds.
These commands run substantial calculations; request appropriate GPU time
on your cluster. Trajectories can differ across hardware/builds, and averages
should be compared statistically rather than expecting identical coordinates.

Both phases use classical nuclei, 64 H2O molecules, 300 K, 1 bar and a
0.5 fs timestep. Water uses isotropic MTTK pressure coupling for 4,000,000
steps (2 ns); ice uses anisotropic coupling of three cell lengths for
1,000,000 steps (500 ps). Pressure in `run.in` is in GPa (`0.0001` = 1 bar).
Thermostat/barostat periods are 200/1000 steps (0.1/0.5 ps). Thermodynamic
output intervals are 100 steps for water and 200 steps for ice. Density
uses physical masses H=1.00794 and O=15.9994 u and the determinant of the
full cell matrix in the last nine thermodynamic columns.

The reported means discard 200 ps of water and 50 ps of ice. Uncertainties
are standard errors of nonoverlapping 50 ps block means (36 and 9 blocks):
**water 0.9014 ± 0.0006 g/cm³; ice 0.8886 ± 0.0004 g/cm³**.
`prepare_results.py` derives these statistics and the figure data directly
from the archived compressed outputs. To analyze a rerun with this script,
use a separate copy of the release and replace its phase-specific compressed
`thermo.out.gz` files and evaluation outputs with the new completed results.
The structure-analysis script expects the original 1 ps ice coordinate
sampling, as specified in the released ice input.
