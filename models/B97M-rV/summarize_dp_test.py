#!/usr/bin/env python3
"""Summarize full B97M-rV dp-test outputs and prepare parity-plot data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


MODELS = ("000", "001", "002", "003")
PHASES = ("quantum_liq", "quantum_ice")
FORCE_SAMPLE_SIZE = 50_000
FORCE_SAMPLE_SEED = 20_260_824


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("dp_test_root", type=Path)
    parser.add_argument("output_root", type=Path)
    return parser.parse_args()


def metrics(reference: np.ndarray, prediction: np.ndarray) -> tuple[float, float]:
    error = prediction - reference
    return float(np.mean(np.abs(error))), float(np.sqrt(np.mean(error**2)))


def main() -> None:
    args = parse_args()
    dp_test_root = args.dp_test_root.resolve(strict=True)
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    energy_reference: dict[str, np.ndarray] = {}
    energy_predictions: dict[str, list[np.ndarray]] = {phase: [] for phase in PHASES}
    force_reference: dict[str, np.ndarray] = {}
    force_predictions: dict[str, list[np.ndarray]] = {phase: [] for phase in PHASES}

    for model in MODELS:
        for phase in PHASES:
            detail_root = dp_test_root / f"model.{model}" / phase
            energy = np.loadtxt(detail_root / "detail.e_peratom.out")
            force = np.loadtxt(detail_root / "detail.f.out")
            e_ref, e_pred = energy[:, 0], energy[:, 1]
            f_ref, f_pred = force[:, :3].reshape(-1), force[:, 3:].reshape(-1)

            if phase not in energy_reference:
                energy_reference[phase] = e_ref
                force_reference[phase] = f_ref
            else:
                if not np.array_equal(energy_reference[phase], e_ref):
                    raise ValueError(f"Energy references differ for {model} {phase}")
                if not np.array_equal(force_reference[phase], f_ref):
                    raise ValueError(f"Force references differ for {model} {phase}")
            energy_predictions[phase].append(e_pred)
            force_predictions[phase].append(f_pred)

    rows = []
    for model_index, model in enumerate(MODELS):
        for phase in (*PHASES, "all"):
            if phase == "all":
                e_ref = np.concatenate([energy_reference[p] for p in PHASES])
                e_pred = np.concatenate(
                    [energy_predictions[p][model_index] for p in PHASES]
                )
                f_ref = np.concatenate([force_reference[p] for p in PHASES])
                f_pred = np.concatenate(
                    [force_predictions[p][model_index] for p in PHASES]
                )
            else:
                e_ref = energy_reference[phase]
                e_pred = energy_predictions[phase][model_index]
                f_ref = force_reference[phase]
                f_pred = force_predictions[phase][model_index]
            e_mae, e_rmse = metrics(e_ref, e_pred)
            f_mae, f_rmse = metrics(f_ref, f_pred)
            rows.append(
                {
                    "model": model,
                    "phase": phase,
                    "nframes": len(e_ref),
                    "nforce_components": len(f_ref),
                    "energy_mae_meV_per_atom": 1000 * e_mae,
                    "energy_rmse_meV_per_atom": 1000 * e_rmse,
                    "force_mae_meV_per_A": 1000 * f_mae,
                    "force_rmse_meV_per_A": 1000 * f_rmse,
                }
            )

    e_ref_all = np.concatenate([energy_reference[p] for p in PHASES])
    e_pred_all = np.stack(
        [
            np.concatenate([energy_predictions[p][i] for p in PHASES])
            for i in range(len(MODELS))
        ]
    )
    f_ref_all = np.concatenate([force_reference[p] for p in PHASES])
    f_pred_all = np.stack(
        [
            np.concatenate([force_predictions[p][i] for p in PHASES])
            for i in range(len(MODELS))
        ]
    )
    e_mae, e_rmse = metrics(e_ref_all, np.mean(e_pred_all, axis=0))
    f_mae, f_rmse = metrics(f_ref_all, np.mean(f_pred_all, axis=0))
    rows.append(
        {
            "model": "committee_mean",
            "phase": "all",
            "nframes": len(e_ref_all),
            "nforce_components": len(f_ref_all),
            "energy_mae_meV_per_atom": 1000 * e_mae,
            "energy_rmse_meV_per_atom": 1000 * e_rmse,
            "force_mae_meV_per_A": 1000 * f_mae,
            "force_rmse_meV_per_A": 1000 * f_rmse,
        }
    )

    with (output_root / "dp_test_metrics.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=rows[0].keys(), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    rng = np.random.default_rng(FORCE_SAMPLE_SEED)
    force_indices = np.sort(
        rng.choice(
            len(f_ref_all),
            size=min(FORCE_SAMPLE_SIZE, len(f_ref_all)),
            replace=False,
        )
    )
    np.savez_compressed(
        output_root / "parity_data.npz",
        model_ids=np.array(MODELS),
        energy_reference=e_ref_all,
        energy_prediction=e_pred_all,
        force_reference=f_ref_all[force_indices],
        force_prediction=f_pred_all[:, force_indices],
        force_sample_indices=force_indices,
        force_sample_seed=FORCE_SAMPLE_SEED,
        force_total_components=len(f_ref_all),
    )


if __name__ == "__main__":
    main()
