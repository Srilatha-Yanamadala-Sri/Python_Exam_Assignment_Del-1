"""Reusable analysis tools for the health study dataset."""

from pathlib import Path
from typing import Dict, Union

import numpy as np
import pandas as pd


def load_dataset(path: Union[str, Path]) -> pd.DataFrame:
    """Load the health study CSV from the given path."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    return pd.read_csv(csv_path)


class HealthAnalyzer:
    """Run simple statistical analyses on health study participants."""

    required_columns = {"age", "systolic_bp", "sex", "disease"}

    def __init__(self, data: pd.DataFrame) -> None:
        """Validate and store a copy of the participant data."""
        missing_columns = self.required_columns.difference(data.columns)
        if missing_columns:
            raise ValueError(
                f"Dataset is missing required columns: {sorted(missing_columns)}"
            )
        if data.empty:
            raise ValueError("Dataset must contain at least one participant.")
        if data[list(self.required_columns)].isna().any().any():
            raise ValueError("Required analysis columns cannot contain missing values.")
        if not data["disease"].isin([0, 1]).all():
            raise ValueError("The disease column must contain only 0 and 1.")

        self.data = data.copy()

    def fit_linear_regression(self, predictor: str, target: str) -> Dict[str, float]:
        """Fit a one-predictor least-squares model and return its results."""
        if predictor not in self.data.columns or target not in self.data.columns:
            raise ValueError("Predictor and target must be columns in the dataset.")

        x = pd.to_numeric(self.data[predictor], errors="raise").to_numpy(dtype=float)
        y = pd.to_numeric(self.data[target], errors="raise").to_numpy(dtype=float)
        if not np.isfinite(x).all() or not np.isfinite(y).all():
            raise ValueError("Predictor and target must contain finite values.")
        if len(x) < 2:
            raise ValueError("At least two participants are required for regression.")

        design_matrix = np.column_stack((np.ones(len(x)), x))
        coefficients, _, _, _ = np.linalg.lstsq(design_matrix, y, rcond=None)
        predictions = design_matrix @ coefficients
        residual_sum = np.sum((y - predictions) ** 2)
        total_sum = np.sum((y - y.mean()) ** 2)
        r_squared = 1 - residual_sum / total_sum if total_sum > 0 else 0.0

        return {
            "intercept": float(coefficients[0]),
            "slope": float(coefficients[1]),
            "r_squared": float(r_squared),
        }

    def disease_rate_by(self, group_column: str) -> pd.Series:
        """Return disease prevalence as a percentage for each group."""
        if group_column not in self.data.columns:
            raise ValueError(f"Group column is not in the dataset: {group_column}")
        return (
            self.data.groupby(group_column)["disease"]
            .mean()
            .mul(100)
            .rename("disease_rate_percent")
        )
