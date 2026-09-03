---
name: gradle-best-practices
description: "Audit a Gradle project against the official Gradle best practices, report findings, and propose code changes to bring the build into compliance. Use this skill whenever the user wants to check, audit, lint, review, or validate a Gradle build — and also when they want to apply, adopt, fix, or enforce best practices. Trigger on phrases like 'check my build', 'audit gradle', 'best practices review', 'any issues with my build?', 'gradle health check', 'lint my build files', 'is my gradle setup correct?', 'apply gradle best practices', 'fix my build to follow best practices', 'make my build follow best practices', 'modernize my build', or simply 'check best practices'. Also trigger when the user asks about Gradle build quality concerns such as dependency management, build performance, build structure, or task wiring."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.0.0"
---

# Gradle Best Practices

Audit a project against the official Gradle best practices, produce a structured findings report, and propose concrete code changes to fix the issues. Checks and fixes cover build scripts (`*.gradle.kts`, `*.gradle`), settings files, `gradle.properties`, the wrapper config, the version catalog, and Java/Kotlin/Groovy source under `buildSrc/` and `build-logic/`.

**The best-practices catalog is fetched live from `docs.gradle.org` every run.** This skill ships no embedded list. The source of truth is always the latest published documentation.

## Sources of truth

Fetch these at runtime — do not cache them across sessions:

- **Overview:** `https://docs.gradle.org/current/userguide/best_practices.html`
- **Index (every best practice with anchor and Gradle version):** `https://docs.gradle.org/current/userguide/best_practices_index.html`
- **Category pages** (each best practice has its own anchor on one of these):
  - `https://docs.gradle.org/current/userguide/best_practices_general.html`
  - `https://docs.gradle.org/current/userguide/best_practices_structuring_builds.html`
  - `https://docs.gradle.org/current/userguide/best_practices_dependencies.html`
  - `https://docs.gradle.org/current/userguide/best_practices_tasks.html`
  - `https://docs.gradle.org/current/userguide/best_practices_performance.html`
  - `https://docs.gradle.org/current/userguide/best_practices_security.html`
  - `https://docs.gradle.org/current/userguide/best_practices_testing.html`

The direct link for any given best practice is `https://docs.gradle.org/current/userguide/best_practices_<category>.html#<anchor>`, where `<anchor>` is the ID listed in the index.

## Modes

- **Audit mode** (default — "check my build", "audit gradle", "are there issues?"): run Steps 1–5 and stop after presenting the report. Then offer to apply fixes in Step 6.
- **Apply mode** ("apply best practices", "fix my build", "modernize my build"): run Steps 1–5 to gather findings, briefly summarize them, and proceed directly into Step 6 — proposing fixes for the highest-priority items first.

## Never block on a question

If you are running unattended — a scripted, CI, or single-turn session where no reply will come — treat every "ask the user" or "get confirmation" step in this skill as: choose the recommended option, record the decision and its rationale in the report, and continue. Never end the session waiting for input. For structural fixes, write the plan into the report instead of asking, then execute it.

## Step 1: Discover the project's Gradle files

Find Gradle-related files in the project by glob pattern:

| Pattern | Purpose |
|---------|---------|
| `**/settings.gradle.kts`, `**/settings.gradle` | Settings files |
| `**/build.gradle.kts`, `**/build.gradle` | Build scripts (root + subprojects) |
| `**/gradle.properties` | Properties files (root + subprojects) |
| `**/gradle/wrapper/gradle-wrapper.properties` | Wrapper config |
| `**/gradle/libs.versions.toml` | Version catalog |
| `**/buildSrc/**/*.{kt,kts,groovy,java}` | buildSrc sources (including `src/main/`) |
| `**/build-logic/**/*.{kt,kts,groovy,java}` | build-logic sources (including `src/main/`) |
| `**/*.gradle.kts`, `**/*.gradle` | Convention plugins and other Gradle scripts |

Read each discovered file — the checks depend on contents, not just existence.

If no Gradle files are found at all, tell the user this doesn't appear to be a Gradle project and stop.

## Step 2: Fetch the best-practices catalog

1. Fetch the index page: `https://docs.gradle.org/current/userguide/best_practices_index.html`.
2. Parse the index into a list of `(title, category, anchor, added-in-version)` entries. The category determines which page hosts the anchor (e.g., `General` → `best_practices_general.html`).
3. For **each** entry, fetch its category page if not already loaded, and extract the section under that anchor — title, explanation, and any "References" / "Tags" subsections.

If a fetch fails, tell the user network access is required and stop. Do not fall back to memorized best practices — the point of this skill is to reflect the live docs.

## Step 3: Derive a detection approach for each best practice

The Gradle docs describe each best practice in prose. The skill's job is to translate that prose into a concrete check against the project's files. For each best practice, decide:

1. **Applicability** — does the project use the feature this best practice talks about? (Skip a Kotlin-stdlib best practice if no Kotlin plugin is applied. Skip a TestKit best practice if there are no custom tasks or plugins.)
2. **Locus** — which file(s) discovered in Step 1 would contain a violation? Build scripts, the settings file, `gradle.properties`, the wrapper config, the version catalog, or `buildSrc/` / `build-logic/` source?
3. **Detection kind:**
   - **Deterministic** — a specific string, glob, or property value answers it yes/no. Examples: any `.gradle` file present (Kotlin DSL), `distributionUrl` ends in `-all.zip` (bin distribution), `org.gradle.caching=true` missing (build cache), `apply plugin:` in a build script (plugins block), `afterEvaluate {` anywhere (avoid `afterEvaluate`), `PathSensitivity.ABSOLUTE` in custom task source.
   - **Heuristic** — requires judgment across multiple files (e.g., "duplication across subprojects suggests a convention plugin is missing", "many source files in a single project suggests modularization is needed", "`dependsOn` is fine for lifecycle tasks but not for tasks with actions"). Flag only with clear evidence; note the uncertainty.
4. **Severity band** (this skill's editorial classification; the official docs don't assign severity):
   - **High** — security risks, likely build failures, broken configuration cache, or significant correctness problems.
   - **Medium** — suboptimal builds, maintenance burden, or violations of Gradle conventions.
   - **Recommendation** — modern idioms and nice-to-have improvements.

Run every applicable check.

## Step 4: Check the project

Apply each detection approach by searching and reading the files discovered in Step 1. Record each finding with: best practice title, anchor URL, file(s) and line(s) where the violation appears, a one-sentence description, a suggested fix, and the severity band.

Violations are not mutually exclusive: one line can violate several practices at once, and matching a line to one practice does not exhaust it. Example: `dependsOn 'listMaintainedCars'` between two tasks with actions violates both *Don't hardcode task names* (the string) and *Avoid dependsOn* (the coupling) — fixing the string form to `dependsOn someTaskProvider` resolves the first and leaves the second. Record one finding per violated practice, even when findings share a line.

## Step 5: Present the report

If no issues were found, emit a single line: **No issues found.** Then stop.

Otherwise:

```
# Gradle Best Practices Audit

Source: https://docs.gradle.org/current/userguide/best_practices.html (fetched [timestamp])
Best practices evaluated: N
Best practices not applicable: N

## Summary
| Priority | Count |
|---|---|
| High | N |
| Medium | N |
| Recommendation | N |

## Issues

### [Category]

**[Best Practice Title]** — [High / Medium / Recommendation]
- **Where:** file.gradle.kts:12, other-file.gradle.kts:5
- **Issue:** What's wrong, concretely.
- **Fix:** What to change.
- **Reference:** https://docs.gradle.org/current/userguide/best_practices_<category>.html#<anchor>
```

### Optional: HTML report

If the user asks for an HTML report (sortable by priority/location with clickable links), offer to write one to `build/reports/best-practices-audit.html` instead of (or in addition to) the markdown report.

## Step 6: Apply fixes

In Audit mode, ask: "Would you like me to apply any of these fixes? I can propose code changes to your build scripts, settings, properties, version catalog, and source under `buildSrc/` / `build-logic/`." If no reply can come (see "Never block on a question"), apply the fixes without asking.

In Apply mode, skip the question and proceed directly.

When applying fixes:
- Start with the highest-priority issues. Group related fixes (e.g., all `repositories {}` blocks moved at once).
- For **straightforward fixes** (adding `org.gradle.caching=true`, renaming `-all.zip` to `-bin.zip`, adding `rootProject.name`, swapping `apply plugin:` for the `plugins {}` block, adding `group`/`description` to a task, replacing `.get()` with `.map { }`), edit the file in place and show the diff.
- For **source-level fixes** in `buildSrc/` or `build-logic/` (replacing `PathSensitivity.ABSOLUTE`, removing `project.` access inside `@TaskAction`, adding `attributes { }` to consumable configurations), apply the edit and re-read the file to confirm it still compiles.
- For **structural fixes** (migrating `buildSrc/` to `build-logic/`, modularizing a project, converting Groovy DSL to Kotlin DSL, extracting convention plugins from duplication), describe the plan first, get user confirmation — or, unattended, record the plan and proceed without it — then apply incrementally with a checkpoint after each step.
- After each fix, confirm the change resolved the issue. If a fix uncovers a related issue (e.g., moving repositories to settings reveals that `FAIL_ON_PROJECT_REPOS` should be set), surface that as a follow-up.
- After fixing a line, re-check it against the remaining findings and the full catalog: a fix for one facet often leaves a co-located violation intact, or introduces a new one.
- If the user declines a fix, leave it as-is and move on.
