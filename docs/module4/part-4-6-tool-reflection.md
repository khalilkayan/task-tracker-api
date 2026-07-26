# Reflection — Copilot, Codex, and Claude Code

Working through this module, I ended up using three different AI coding
tools, and they were genuinely useful for different kinds of tasks — not as
one tool being universally "better" than the others.

**Copilot** is what I reach for when I'm typing out something repetitive and
local: a test function that follows the same shape as the five before it, a
fixture, a small loop. It's fast because it's inline, it doesn't need me to
explain anything, and I can just accept or reject a suggestion line by line
as I go. Its weakness is exactly that narrowness — it doesn't know anything
about the rest of the repository, so it's not the tool I'd use for anything
that needs to stay consistent with a decision made in a different file.

**Codex** is what I'd use for bounded implementation work where I already
have a clear specification and tests to check it against — for example,
"implement this one function so these specific tests pass." It's good at
producing a focused diff for a well-defined problem, but it's operating
mostly blind to the surrounding project unless I explicitly give it that
context, so I still have to be the one who defines the boundary of the task
correctly.

**Claude Code** is what I used for everything in this module that touched
the whole repository at once: reading `app/main.py`, `app/models.py`,
`app/storage.py`, and `app/business_rules.py` together to write accurate
docstrings; reading and explaining Git diffs; writing and explaining the CI
workflow and the Dockerfile; updating `README.md` to match what the code and
containers actually do; and reviewing a commit against the actual diff. That
kind of work needs a tool that can hold a lot of files in context at once,
not just the file I'm currently typing in.

The risk that showed up most clearly across all of this is that a tool can
produce something plausible-sounding that's just wrong. Twice in this
module, Claude stated something confidently that wasn't true. First, it
claimed `app/frontend/index.html` wasn't included in the Docker image — but
the `Dockerfile`'s `COPY --chown=app:app app/ ./app/` copies the whole
`app/` directory, so the file is present; the container's `CMD` just never
serves it over HTTP. Second, when I asked it to add a 404 response and
clarify the 422 response in the OpenAPI metadata, it initially assumed that
supplying only a `description` for a custom `responses[422]` entry would
automatically preserve FastAPI's auto-generated `HTTPValidationError`
schema — which turned out to be an unsafe assumption, since a custom
response for a status code FastAPI already documents can replace what it
would have generated instead of merging with it. In both cases, it was me
actually reading the `Dockerfile` line by line, and later inspecting the
generated OpenAPI schema directly, that caught the mistake before it
shipped. Both were corrected, and the tests and CI still passed afterward.

The other risks I watched for were a tool changing more than I asked for, me
blindly accepting a generated diff without reading it, and — on the opposite
end — spending so much time re-verifying trivial, obviously-correct changes
that the verification loop slowed down work that didn't need it.

My personal rule going forward: use Copilot for small, local, repetitive
code; use Codex when I already have a tight spec and tests to check against;
use Claude Code when the task spans multiple files, needs explanation, or
touches infrastructure like CI and Docker. But regardless of which tool
produced it, I still read every diff before approving it, because this
module proved that a confident-sounding claim from any of these tools is not
the same thing as a correct one.
