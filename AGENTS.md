# AGENTS.md

This repo is a single-file Python simulation (`prime-society.py`). Keep changes small and localized.

## Quick orientation
- Main entrypoint: `prime-society.py`
- Logs: `prime_society.log`
- Optional docs: `README.md`, `complete-rules_italian.md`

## Preferred workflow
1. Read `prime-society.py` first; most behavior is defined there.
2. Keep edits minimal and avoid sweeping refactors.
3. If adding new logic, favor small helper methods or constants at the top.

## Running
- Basic run: `python prime-society.py --days 200 --no-graphs`
- Graphs are optional and can slow runs; prefer `--no-graphs` for quick checks.

## Notes
- The simulation is stochastic; use `--seed` when debugging for repeatability.
