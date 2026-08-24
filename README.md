# Description
This repo stores the models, job scripts, and data for our manuscripts:

Assessment of First-Principles Methods in Modeling the Melting Properties of Water, Yifan Li, Bingjia Yang, Chunyi Zhang, Pinchen Xie, Yixiao Chen, Pablo M. Piaggi, and Roberto Car

Ab Initio Melting Properties of Water and Ice from Machine Learning Potentials, Yifan Li, Bingjia Yang, Chunyi Zhang, Pinchen Xie, Yixiao Chen, Pablo M. Piaggi, and Roberto Car

## Table of Contents
### `dft_inputs`
This folder contains versioned CP2K labeling inputs organized by density functional.

### `models`
This folder contains Deep Potential models based on the revPBE-D3,
revPBE0-D3, SCAN, SCAN0, and B97M-rV density functionals. The B97M-rV
directory contains a four-seed model committee.

### `training_data`
This folder contains the corresponding DFT-labeled training data.
