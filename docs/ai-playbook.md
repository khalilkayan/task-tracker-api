# My AI Coding Playbook


## 1. When I reach for AI first

- Situation: I reach for AI first when I know what I want to build or investigate but need help turning the idea into a clear technical plan.
- Task type: Planning a feature, understanding unfamiliar code, or getting a structured first pass before I start changing files.
- Desired outcome: I want a useful starting point that I can check against the repository myself, not something I accept blindly.


## 2. When I do not reach for AI

- Situation: I do not use AI when the task involves information I would not be comfortable sharing outside the project.
- Information involved: Credentials, secrets, `.env` contents, real customer or personal data, production data, or code I am not authorized to share.
- Reason: During the governance exercise I realized that even useful technical context can expose sensitive information, so I would rather remove or replace that context than send it to an AI tool.


## 3. My non-negotiables

- Boundary: AI does not get to make repository changes outside the scope I approved.
- Required practice: I review the diff and understand what changed before I accept or commit AI-generated work.
- Prohibited action: I do not approve broad or session-wide permissions when one specific read or change is enough.

## 4. My review rules

- What I verify: I check whether the AI’s claims actually match the repository instead of trusting a confident explanation.
- How I verify it: I inspect the relevant files, review the diff, and run the appropriate tests or checks before accepting the work.
- Condition for acceptance: I only accept AI-generated work when I can explain what changed and the evidence shows it behaves as intended.

## 5. What I am still figuring out

- Open question: How much context I should give an AI before it becomes less useful, more verbose, or too confident.
- Unresolved tradeoff: I am still learning when broad repository context is worth the extra time compared with a smaller targeted set of files.
- Practice to evaluate: I want to keep testing different context strategies and compare whether the extra context actually improves the final result.

## 30-Day Re-read

I will re-read this playbook on September 9, 2026 and update any rules that no longer match how I actually use AI.


## Decision Card

- For a new feature I reach for: GitHub Copilot
- For a code review I reach for: Codex App
- For debugging I reach for: GitHub Copilot
- For infrastructure I reach for: Claude Code
- I will never paste credentials, secrets, `.env` contents, or real customer/personal data into an AI tool.
- My one rule is: I never accept AI-generated work until I have reviewed it and verified that it actually works.

