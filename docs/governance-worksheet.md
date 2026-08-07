# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|---|---|---|---|
| Task Tracker code | 2-5 | Low | This is toy project code and no sensitive data is indicated. |
| Test output and stack traces | 2-4 | Medium | Stack traces can expose internal implementation details, paths, and error context. |
| Frontend code | 3 | Low | Frontend code for this toy project is low risk because it contains no indicated secrets or private data. |
| Dockerfile and CI YAML | 4 | Medium | CI and Docker configuration can reveal internal architecture, build steps, and deployment assumptions. |
| Any real external data I used by mistake | TODO | Ambiguous | The risk depends on what the data contained; it could be High if it included credentials, PII, financial data, health data, production exports, or unauthorized code. |

## What I Received From AI

| Generated Thing | Module | Do I Understand It Line by Line? | Action |
|---|---|---|---|
| Backend models and validators | 2 | No | Review before modifying or reusing. |
| Frontend board and drag-and-drop logic | 3 | No | Review before modifying or reusing. |
| CI workflow | 4 | Yes | Keep; I traced this block line by line. |
| Dockerfile | 4 | No | Review before modifying or reusing. |
| Security findings and plans | 5 | Yes | Keep only after checking the evidence and grading the findings myself. |
