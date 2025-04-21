# Contributor Onboarding Guide: Distributed Validation & Chaos Engineering

Welcome to the Windsurf Agent Platform! This guide will help new contributors quickly understand and participate in our advanced validation, merge, and observability workflows.

## 1. Project Structure
- **Legacy tests:** `tests/legacy/`
- **Property-based & chaos tests:** `tests/property_based/`
- **Merge drivers:** `scripts/merge_schema`, configured in `.gitattributes`
- **Feature flags:** `config/feature_flags.yml`
- **ML pipeline:** `ml_conflict_prediction.py` (sample data: `ml_conflict_sample.csv`)
- **Chaos workflows:** `.github/workflows/chaos_validation.yml`, `.github/workflows/chaos_byzantine.yml`

## 2. Step-by-Step Onboarding Workflow
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd agent-team
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run all tests locally:**
   ```bash
   pytest tests/legacy/
   pytest tests/property_based/
   ```
4. **Review feature flags:**
   - Edit `config/feature_flags.yml` to enable/disable observability features as needed.
5. **Check ML merge conflict prediction:**
   - Run: `python ml_conflict_prediction.py ml_conflict_sample.csv`
   - Use your real merge/test history for advanced predictions.
6. **Review chaos test results:**
   - Artifacts and logs are available in GitHub Actions after each chaos workflow run.

## 3. Running Chaos Tests Locally
1. **Install Docker** (for Redis/Postgres containers) and required Python dependencies.
2. **Start services:**
   ```bash
   docker-compose up -d
   ```
3. **Inject chaos (example for Linux):**
   ```bash
   sudo tc qdisc add dev lo root netem delay 500ms
   pytest tests/property_based/
   sudo tc qdisc del dev lo root netem
   ```
4. **Analyze results:**
   - Check logs and Prometheus metrics for alert triggers and test outcomes.

## 4. Merge Conflict Resolution
- Schema files use semantic merge drivers.
- ML pipeline predicts likely conflicts before PR merges:
   ```bash
   python ml_conflict_prediction.py ml_conflict_sample.csv
   ```

## 5. Observability & Chaos Engineering
- Feature flags control alerting and metrics rollout.
- Chaos workflows inject faults and validate trace/circuit breaker resilience.

## 6. Documentation
- All major architectural and workflow changes are documented in `project_architecture.md` and `session_log.md`.

## 7. Support
- For questions, check `project_architecture.md` or ask in the project Slack channel.
