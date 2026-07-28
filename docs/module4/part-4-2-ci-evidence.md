# Part 4.2 — CI Pipeline Evidence

Date: 2026-07-26  
Branch: `module-4`  
Repository: `task-tracker-api`

## 1. CI workflow creation

Claude Code read `CLAUDE.md` and `requirements.txt`, then proposed a GitHub Actions workflow at `.github/workflows/ci.yml`.

The proposal was inspected before approval.

The final workflow:

- Triggers on pushes to every branch
- Triggers on pull requests targeting `main`
- Contains exactly one job named `test`
- Runs on `ubuntu-latest`
- Uses Python `3.11`
- Installs dependencies from `requirements.txt`
- Runs `python -m pytest -v --tb=short`

Workflow steps:

1. `actions/checkout@v4`
2. `actions/setup-python@v5`
3. `actions/cache@v4`
4. Upgrade pip
5. Install dependencies
6. Run pytest

The workflow contains no:

- `continue-on-error`
- `|| true`
- `--exit-zero`
- Deployment steps
- Secrets
- Environment variables
- Matrix builds
- Working-directory overrides
- Extra jobs

Workflow commit:

- `f729ad2` — Add GitHub Actions CI workflow

## 2. Local verification

The exact CI command was run locally:

`python -m pytest -v --tb=short`

Result:

- `28 passed`
- `2 warnings`

The warnings were visible and did not prevent the tests from passing.

`git diff --check` produced no formatting errors.

## 3. First green CI run

The `module-4` branch was pushed to GitHub.

The push automatically triggered GitHub Actions.

The first workflow run completed successfully:

- Branch: `module-4`
- Workflow: `CI`
- Job: `test`
- Status: success
- Test result: `28 passed`

Checkout, Python setup, caching, dependency installation, and pytest all succeeded.

## 4. Deliberate red CI run

One test assertion was deliberately changed from:

`assert r.status_code == 200`

to:

`assert r.status_code == 201`

The targeted test failed locally as expected:

- Actual status: `200`
- Expected status: `201`
- Result: `1 failed`

Deliberate failure commit:

- `df95573` — Break test intentionally to verify CI failure

After pushing, GitHub Actions turned red.

The GitHub Actions log showed:

- Python `3.11.15`
- `27 passed`
- `1 failed`
- Failure: `assert 200 == 201`
- Process completed with exit code `1`

All setup and installation steps succeeded. The workflow failed specifically at the `Run tests` step.

This proved that pytest failures were not swallowed.

## 5. Restored green CI run

The test was restored to:

`assert r.status_code == 200`

The full suite was run locally again:

- `28 passed`
- `2 warnings`

Restoration commit:

- `80d4853` — Restore test after CI failure verification

After pushing, the final GitHub Actions run returned to green.

Final GitHub test result:

- `28 passed`
- `2 warnings`

The required sequence was successfully demonstrated:

**Green → Red → Green**

## 6. Claude workflow explanation

Claude later explained the workflow without editing files or running commands.

Claude correctly identified:

- Push and pull-request triggers
- The single Ubuntu test job
- Python setup
- Pip caching
- Dependency installation
- Pytest execution
- Why a test failure turns the workflow red
- The absence of failure-swallowing or unrelated CI settings

One wording issue was manually corrected:

- `requirements.txt` contains six package names, but they are not pinned to exact package versions.
- `python-version: "3.11"` selects the Python 3.11 minor series.
- The GitHub runner used Python `3.11.15`.

## 7. Human verification

The workflow was manually inspected line by line.

Manual checks confirmed:

- Exactly one job named `test`
- No forbidden patterns
- Correct triggers
- Correct Python version
- Correct requirements path
- Correct pytest command
- Clean Git status following read-only verification

Claude proposed and explained the workflow, but the human remained responsible for inspecting, testing, approving, pushing, reviewing the logs, deliberately causing failure, and restoring the project.
