import json
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORAGE_PATH = PROJECT_ROOT / "storage"
METRICS_PATH = STORAGE_PATH / "metrics.json"

MAX_LATENCY_SAMPLES = 500


def default_metrics() -> dict:
    return {
        "successful_queries": 0,
        "latency_ms_samples": [],
        "cache_hits": 0,
        "cache_misses": 0,
        "failures": {},
    }


def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return default_metrics()

    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default_metrics()


def save_metrics(metrics: dict) -> None:
    STORAGE_PATH.mkdir(exist_ok=True)

    METRICS_PATH.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )


def record_latency(latency_ms: float) -> None:
    metrics = load_metrics()

    metrics["successful_queries"] += 1
    metrics["latency_ms_samples"].append(round(latency_ms, 2))

    metrics["latency_ms_samples"] = metrics["latency_ms_samples"][
        -MAX_LATENCY_SAMPLES:
    ]

    save_metrics(metrics)


def record_cache_event(cache_hit: bool) -> None:
    metrics = load_metrics()

    if cache_hit:
        metrics["cache_hits"] += 1
    else:
        metrics["cache_misses"] += 1

    save_metrics(metrics)


def record_failure(error_type: str) -> None:
    metrics = load_metrics()

    failures = metrics["failures"]
    failures[error_type] = failures.get(error_type, 0) + 1

    save_metrics(metrics)


def calculate_percentile(values: list[float], percentile: int) -> float | None:
    if not values:
        return None

    sorted_values = sorted(values)
    position = math.ceil((percentile / 100) * len(sorted_values)) - 1

    return round(sorted_values[position], 2)


def get_metrics_summary() -> dict:
    metrics = load_metrics()

    samples = metrics["latency_ms_samples"]
    cache_hits = metrics["cache_hits"]
    cache_misses = metrics["cache_misses"]
    cache_total = cache_hits + cache_misses

    return {
        "successful_queries": metrics["successful_queries"],
        "latency": {
            "sample_count": len(samples),
            "median_ms": calculate_percentile(samples, 50),
            "p95_ms": calculate_percentile(samples, 95),
        },
        "embedding_cache": {
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "effectiveness_percent": (
                round((cache_hits / cache_total) * 100, 2)
                if cache_total > 0
                else None
            ),
        },
        "failures": metrics["failures"],
        "total_failures": sum(metrics["failures"].values()),
    }