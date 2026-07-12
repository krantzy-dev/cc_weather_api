# scripts/simulate_forecast_history.py
"""Simulate several past days of daily forecast ingestion runs.

DEMO/TEST TOOL ONLY. Open-Meteo only ever returns today's actual forecast,
so the *values* produced here are today's real forecast, just filed under
artificially backdated ts_created/forecast_horizon combinations. This is
useful to quickly populate multi-horizon test data without waiting for
several real days to pass, but must not be mistaken for accurate historical
forecast data.
"""

import argparse
from datetime import UTC, datetime, timedelta

from src.load_data.daily_forecast_ingest import run_daily_forecast_ingest


def main(days_back: int) -> None:
    now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
    for offset in range(days_back, 0, -1):
        simulated_now = now - timedelta(days=offset)
        print(f"Simulating daily forecast ingest as if run on {simulated_now}")
        run_daily_forecast_ingest(reference_time=simulated_now)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days-back", type=int, default=5, help="Number of past days to simulate")
    args = parser.parse_args()
    main(args.days_back)
