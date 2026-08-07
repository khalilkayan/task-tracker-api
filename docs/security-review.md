# Security Review

## Scope and Method

This review reconciles an AI-generated security audit with a subsequent manual security scan.

The reconciliation uses these classifications:

- **Agreement:** Both the AI audit and manual scan identified the same or a closely related issue.
- **AI-only:** The AI identified the issue, but the manual scan did not independently identify it.
- **You-only:** The manual scan identified the issue, but the AI audit missed it.

No additional security findings were sought as part of this reconciliation.

## AI Findings with My Grades and Reasons

### 1. Explicit-null PATCH can violate required stored-field invariants

- **Grade:** Valid
- **Severity:** Medium
- **Reason:** The PATCH path can accept an explicit null in a way that violates invariants expected of required stored fields. The manual review independently traced this behavior through `app/models.py`, `app/main.py`, and `app/storage.py`.

### 2. No authentication or authorization on task CRUD

- **Grade:** Valid — intentional course-scope limitation
- **Severity:** Informational in the current course scope; important if publicly deployed
- **Reason:** Task CRUD is not protected by authentication or authorization. This is a real security boundary absence, but the manual review confirmed that it is an intentional project-scope decision using `docs/midcourse/mini-adr.md`, `AGENTS.md`, and `app/main.py`. It should be reconsidered if the application is exposed publicly.

### 3. Unbounded task creation, unconstrained description/assignee strings, and unpaginated list responses

- **Grade:** Valid
- **Severity:** Medium
- **Reason:** The combination can permit uncontrolled growth in stored data and response size. This is particularly relevant to an in-memory service because resource consumption can grow without an application-level bound. The manual scan did not independently identify this issue.

### 4. CORS permits the `"null"` origin and wildcard methods/headers

- **Grade:** Valid
- **Severity:** Low
- **Reason:** The CORS policy is broader than necessary because it permits the `"null"` origin and uses wildcard methods and headers. The manual review independently confirmed the configuration in `app/main.py`.

### 5. Python dependencies are unpinned, `python:3.11-slim` is not digest-pinned, and the runtime environment contains the full requirements set

- **Grade:** Valid
- **Severity:** Medium
- **Reason:** Mutable dependency and base-image inputs reduce build reproducibility and make upstream changes less predictable. Including the full requirements set in the runtime environment also increases the installed runtime package set. The manual review independently confirmed the unpinned dependencies and mutable Docker inputs in `requirements.txt` and `Dockerfile`.

### 6. GitHub Actions uses major-version action tags and no explicit permissions block

- **Grade:** Noise
- **Severity:** Not applicable
- **Reason:** This was not accepted as an actionable finding for the current review. The manual scan did not independently identify it.

### 7. Runtime app user owns application source files

- **Grade:** Noise
- **Severity:** Not applicable
- **Reason:** This was not accepted as an actionable finding for the current review. The manual scan did not independently identify it.

## My Manual Findings

### 1. Explicit-null PATCH invariant issue

Manual evidence was traced through:

- `app/models.py`
- `app/main.py`
- `app/storage.py`

This agrees with AI finding 1.

### 2. Broad/null CORS configuration

Manual evidence:

- `app/main.py`

This agrees with AI finding 4.

### 3. Unpinned dependencies and mutable Docker inputs

Manual evidence:

- `requirements.txt`
- `Dockerfile`

This agrees with AI finding 5.

### 4. Absence of authentication/authorization is intentional project scope

Manual evidence:

- `docs/midcourse/mini-adr.md`
- `AGENTS.md`
- `app/main.py`

This agrees with AI finding 2 while supplying the project-scope context needed to grade its current severity as Informational.

### Areas Manually Checked with No Finding

- All five `innerHTML` uses were inspected; dynamic values were escaped or the content was static.
- No `eval()` usage was found.
- No `localStorage` usage was found.
- No password references were found.
- Searching for `secret` returned documentation references only.
- `.gitignore` excludes `.env`.
- `.dockerignore` excludes `.env` and `.env.*`.

## Reconciliation

| Agreement | AI-only | You-only |
|---|---|---|
| Explicit-null PATCH invariant issue<br><br>Broad/null CORS configuration<br><br>Unpinned dependencies and mutable Docker inputs<br><br>Absence of authentication/authorization | Unbounded task creation, unconstrained description/assignee strings, and unpaginated list responses<br><br>GitHub Actions major-version tags and missing permissions block — graded Noise<br><br>Runtime app user owns source files — graded Noise | None |

The AI covered the principal application, configuration, resource-control, and supply-chain risks well.

Human judgment was essential to distinguish actionable risks from course-scope limitations and noisy hardening observations.

## Top-3 Unfixed Backlog

| Rank | Finding | Why it matters | Suggested owner | Next action |
|---:|---|---|---|---|
| 1 | Explicit-null PATCH can violate required stored-field invariants | A partial update can leave stored task data inconsistent with fields intended to remain required. | Backend owner | Define the intended explicit-null behavior, then add validation and regression tests while preserving the existing PATCH contract. |
| 2 | Unbounded task creation, unconstrained strings, and unpaginated list responses | Uncontrolled input and collection growth can increase memory use and response size, degrading an in-memory service. | Backend/API owner | Propose conservative field limits, task-cap behavior, and pagination semantics for approval before implementation. |
| 3 | Unpinned dependencies and mutable Docker inputs | Mutable inputs weaken build reproducibility and make dependency or base-image changes less predictable. | Build/container owner | Establish an approved pinning strategy for Python dependencies and the Docker base image, and review whether runtime dependencies can be separated without adding new tooling. |
