# B97M-rV CP2K input

This directory contains a CP2K static energy/force/stress input for generating
Deep Potential labels with B97M-rV.

## Published model chemistry

The electronic-structure choices follow Pestana *et al.*, *Chem. Sci.* **8**,
3554 (2017), DOI [10.1039/C6SC04711D](https://doi.org/10.1039/C6SC04711D):

- semilocal Libxc `MGGA_XC_B97M_V` plus nonlocal rVV10 (in CP2K 2025.1,
  each Libxc functional is enabled by its named `&XC_FUNCTIONAL` subsection);
- rVV10 parameters `b = 6.0` and `C = 0.01`;
- `TZV2P-MOLOPT-GTH` (called mTZV2P in the paper);
- PBE-optimized GTH pseudopotentials;
- five multigrid levels;
- 800 Ry cutoff, as used for their higher-accuracy and fluctuating-cell work;
- `EPS_DEFAULT = 1e-12` and benchmark SCF tolerance `EPS_SCF = 5e-7`.

The paper's Supporting Information reports that B97M-rV WATER20 binding-energy
RMSE improves from 2.80 kcal/mol at mTZV2P/400 Ry to 1.53 kcal/mol at
mTZV2P/800 Ry. This is why 800 Ry is used for the liquid/ice labeling baseline.

## Workflow-specific controls

The OT/outer-SCF setup, `EPS_PGF_ORB`, analytical stress output, and
`NN50_SMOOTH` derivative are explicit numerical controls retained from our
working CP2K labeling workflow. They were not fully specified by Pestana
*et al.* and should not be described as settings reported in that paper.

`structure.xyz` is only a lightweight syntax-test structure. For production
labeling, replace it with the target configuration and replace the `&CELL`
vectors in `input.inp` with that configuration's full cell matrix. Do not use
the example cubic cell for arbitrary ice configurations.

CP2K must be able to find `BASIS_MOLOPT`, `GTH_POTENTIALS`, and
`rVV10_kernel_table.dat` in its data directory.

## Validation

Before production use, validation requires all of the following in the CP2K
output:

- the requested Libxc `MGGA_XC_B97M_V` functional and rVV10 contribution;
- SCF convergence;
- total energy, atomic forces, and analytical stress tensor;
- `PROGRAM ENDED AT` and no `ABORT` or `ERROR` marker.
