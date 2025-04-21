# Project Architecture: Distributed Validation, Observability & Conflict Resolution

## Parallel Test Strategy
- All legacy test suites preserved in `tests/legacy/`
- Property-based and chaos-driven tests in `tests/property_based/`
- Both tracks run in CI for regression and edge-case coverage

## Merge Conflict Resolution
- `.gitattributes` uses semantic merge driver for schema files
- `scripts/merge_schema` performs JSONPath-aware merges
- ML pipeline (`ml_conflict_prediction.py`) predicts likely conflicts before merge

## Observability & Feature Flags
- Prometheus alerting controlled via `config/feature_flags.yml`
- Tiered alerting for circuit breaker, trace completeness
- All new metrics/alerts rolled out behind feature flags for safe adoption

## Chaos Engineering
- CI/CD workflows inject Redis latency, Postgres failover, network partitions
- Advanced chaos: Byzantine fault injection via `chaos_byzantine.yml`
- Trace completeness validated post-chaos with Jaeger/OTel integration

## Documentation & Governance
- All architecture, test, and chaos patterns documented here and in `session_log.md`
- Update this file with every major integration or workflow change
