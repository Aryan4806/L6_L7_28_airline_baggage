# Coverage execution commands

Run from the `lab6` directory after installing pytest and coverage.

## Code coverage

```bash
coverage erase
coverage run --source=airline_baggage -m pytest -q test_code_coverage_airline_baggage.py
coverage report -m
```

## Branch coverage

```bash
coverage erase
coverage run --branch --source=airline_baggage -m pytest -q test_branch_coverage_airline_baggage.py
coverage report -m
```

Record the actual terminal percentages from your own execution. The application source is unchanged.
