# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| The `TaskUpdate` title validator correctly separates an omitted PATCH title from an explicit `null`. | Useful | This matches the intended PATCH behavior: omission remains valid while an explicit `null` is rejected. | Verified against `app/models.py` and the existing status-only PATCH coverage. No change needed. |
| `Optional[str]` may make the generated OpenAPI schema advertise `null` even though runtime validation rejects it. | Useful | This identifies a real schema/runtime contract mismatch risk that generated clients could encounter. | Recorded as a review concern. No final-project code change was made because the current fix already protects the required runtime behavior. |
| The null-title regression test does not assert the specific validation error detail. | Useful | A detail assertion would make the test more specific, although the current test already reproduces the reported bug and verifies that the stored title remains unchanged. | Kept the current test because it already protects the actual failure that was reported. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| The API has no authentication and CORS allows the `"null"` origin with broad methods and headers. | `app/main.py` defines CRUD routes without authentication and configures CORS with `"null"`, wildcard methods, and wildcard headers. | Valid | The CORS configuration creates a real browser-access risk if the service is exposed. Lack of authentication is an intentional course-scope limitation, so I would not add authentication as part of this final project. | Keep the course app restricted to its intended local/trusted use. Record the CORS limitation rather than adding an out-of-scope authentication feature. |
| Task creation and in-memory storage are effectively unbounded. | `app/models.py` does not set maximum lengths for some user-controlled strings, and `app/storage.py` keeps tasks in a process-global dictionary and scans the collection for listing/search. | Valid | Repeated creation of large or numerous tasks could consume memory and make list/search operations increasingly expensive. | Record as a known limitation. Do not expand the final project into pagination, rate limiting, or storage redesign. |
| CI and Docker builds depend on mutable remote inputs such as action tags, `python:3.11-slim`, and network-installed packages. | `.github/workflows/ci.yml` uses major action tags and `ubuntu-latest`; `Dockerfile` uses `python:3.11-slim` and upgrades pip from the network. | Valid | Mutable tags and package inputs reduce reproducibility and introduce some supply-chain risk. For this course project, the existing configuration is functional and verified, so a pinning overhaul is not necessary. | Keep the current verified configuration and treat stronger dependency/image pinning as a future hardening improvement. |

## Manual security check

I manually checked the running Docker container for baked environment files with:

```bash
docker exec task-tracker-final sh -c 'find /app -type f \( -name ".env" -o -name "*.env" \) -print'

```

The command returned no output, so no `.env` or `*.env` files were present under `/app` in the running container.

I also verified that the container runs as the non-root `app` user:

```bash
docker exec task-tracker-final id
```

Result:

```text
uid=1000(app) gid=1000(app) groups=1000(app)
```

## One AI output I rejected or corrected

During an earlier Docker review, an AI assistant claimed that the frontend was not included in the Docker image.

I checked the actual `Dockerfile` and rejected that claim because `COPY app/ ./app/` copies the entire `app/` directory, including `app/frontend/`.

The more accurate conclusion is that the frontend files are present in the image, but the runtime command serves only the FastAPI backend. I corrected the AI conclusion instead of accepting it blindly.

## Three AI usage rules

1. Never paste credentials, secrets, `.env` files, real customer data, sensitive personal data, production data, or code I am not authorized to share.
2. Always review AI-generated changes, understand what they do, and verify them with the repository, tests, or actual runtime behavior before accepting them.
3. Record important AI contributions and what I personally checked, corrected, rejected, or verified.

## Ownership statement

I used AI throughout this project as a tool for planning, review, debugging, and documentation, but I did not treat its output as automatically correct. I checked important claims against the repository and verified the application with tests, local runtime checks, Docker checks, and manual inspection. When an AI claim was wrong or too broad, I corrected or rejected it rather than changing the project blindly. I understand the commands, configuration, code changes, and evidence included in this submission and take responsibility for the final result.