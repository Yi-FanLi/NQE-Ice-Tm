# B97M-rV Deep Potential committee

This directory contains four independently seeded, compressed Deep Potential
models trained on the phase-resolved B97M-rV dataset in
`training_data/B97M-rV`.

| File | Seed label |
| --- | --- |
| `graph.000.pb` | 000 |
| `graph.001.pb` | 001 |
| `graph.002.pb` | 002 |
| `graph.003.pb` | 003 |

The models were compressed with DeePMD-kit 2.2.9 using the default tabulation
step (0.01). `dp test -n 0` was then run separately on the 825 quantum-liquid
and 456 quantum-ice configurations for every model. The phase-resolved logs are
under `dp_test`, and `validation/dp_test_metrics.csv` reports metrics calculated
from all predictions. The compact `validation/parity_data.npz` contains all
energy predictions and a deterministic sample of force components for plotting.

`summarize_dp_test.py` reproduces the metrics and parity-data archive from the
full `dp test` detail files. The detail files are not included because they are
large; the summary artifacts and original `dp-test.log` files are retained.

See `SHA256SUMS` for checksums of the four compressed model files.
