# BPNN3 production model

The production BPNN3 used in the water/ice training-dataset paper is the
`iter04`, epoch-200 model trained with random seed 123456 on
[SET3](../../../training_data/revPBE0-D3/SET3/), containing 2,556 configurations.
This directory contains the production member of the four-seed committee.

- `input.nn`: original n2p2 settings and symmetry functions.
- `scaling.data`: symmetry-function scaling statistics from SET3.
- `weights.001.data` and `weights.008.data`: accepted epoch-200 weights for H
  and O, respectively, renamed from the archived `weights.*.accepted.out`
  files to the n2p2 inference filenames; their contents are unchanged.
- `TRAINING_COMPLETION.tsv`: accepted epoch, completion status, original
  checkpoint names, and weight hashes.
- `learning-curve.out`: recorded training and internal-test learning curves.
- `SHA256SUMS`: checksums for this directory.

The model uses bohr and hartree units, including forces in hartree/bohr.
Its two hidden layers have 25 neurons each and its symmetry-function cutoff
is 12 bohr. Training used a 20% internal test fraction. The independent AIMD
tests reported in the paper are separate from that internal split.

SET2 is the original 1,778-configuration DP active-learning dataset at
[`training_data/revPBE0-D3/alldata/`](../../../training_data/revPBE0-D3/alldata/).
BPNN2 was trained on SET2; BPNN3 was trained on the extended SET3.

Verify this directory with `shasum -a 256 -c SHA256SUMS`
(or `sha256sum -c SHA256SUMS` on Linux).
