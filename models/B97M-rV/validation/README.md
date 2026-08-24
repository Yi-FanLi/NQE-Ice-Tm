# Validation artifacts

`dp_test_metrics.csv` contains energy and force MAE/RMSE values calculated from
the complete B97M-rV training set for each compressed model. Energy errors are
reported per atom. The `committee_mean` row evaluates the arithmetic mean of
the four model predictions, rather than the mean of the four model RMSE values.

`parity_data.npz` contains all 1,281 reference energies and their four model
predictions. To keep plotting responsive, it contains a deterministic sample of
50,000 out of 737,856 force components (NumPy seed 20260824); the metrics in the
CSV always use all force components.
