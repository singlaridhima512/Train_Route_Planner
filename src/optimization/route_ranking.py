
"""Rank candidate routes using configurable weighted metrics.

Lower travel time, distance, and transfer count are considered better.
Scores are normalized across candidate routes.
A lower final score indicates a better route.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional

from .route_metrics import route_metrics

import math
DEFAULT_WEIGHTS = {
    "travel_time": 0.60,
    "transfers": 0.30,
    "distance": 0.10,
}


def _normalize_weights(
    weights: Optional[Mapping[str, float]]
) -> Dict[str, float]:

    chosen = dict(DEFAULT_WEIGHTS if weights is None else weights)

    if set(chosen) != set(DEFAULT_WEIGHTS):
        raise ValueError(
            f"Weights must contain exactly: {sorted(DEFAULT_WEIGHTS)}"
        )

    values = [float(value) for value in chosen.values()]

    if any(not math.isfinite(value) or value < 0 for value in values):
        raise ValueError(
        "Weights must be finite and non-negative."
    )

    total = sum(values)

    if total <= 0:
        raise ValueError("At least one weight must be greater than zero.")

    return {
        key: float(value) / total
        for key, value in chosen.items()
    }


def rank_routes(
    routes: Iterable[Mapping[str, Any]],
    weights: Optional[Mapping[str, float]] = None
) -> list[Dict[str, Any]]:
    """Return candidate routes sorted from best to worst."""

    routes = list(routes)

    if not routes:
        return []

    normalized_weights = _normalize_weights(weights)

    metric_rows = [route_metrics(route) for route in routes]

    # Match ranking criteria to the actual keys in route_metrics.py.
    metric_keys = {
        "travel_time": "total_travel_time",
        "distance": "total_distance",
        "transfers": "count_transfers",
    }

    mins = {
        key: min(row[value] for row in metric_rows)
        for key, value in metric_keys.items()
    }

    maxs = {
        key: max(row[value] for row in metric_rows)
        for key, value in metric_keys.items()
    }

    scored = []

    for index, (route, metrics) in enumerate(zip(routes, metric_rows)):

        score = 0.0

        for metric_key, weight in normalized_weights.items():

            actual_key = metric_keys[metric_key]

            low = mins[metric_key]
            high = maxs[metric_key]

            if high == low:
                normalized = 0.0
            else:
                normalized = (
                    metrics[actual_key] - low
                ) / (high - low)

            score += weight * normalized

        scored.append({
            "route": route,
            "metrics": metrics,
            "score": round(score, 6),
            "_input_order": index,
        })

    # Lower score means better route.
    scored.sort(
        key=lambda item: (item["score"], item["_input_order"])
    )

    for item in scored:
        item.pop("_input_order")

    return scored
