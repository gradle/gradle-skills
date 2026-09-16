---
name: gradle-best-practices
description: "Audit a Gradle project against the official Gradle best practices, report findings, and propose code changes to bring the build into compliance. Use this skill whenever the user wants to check, audit, lint, review, or validate a Gradle build — and also when they want to apply, adopt, fix, or enforce best practices. Trigger on phrases like 'check my build', 'audit gradle', 'best practices review', 'any issues with my build?', 'gradle health check', 'lint my build files', 'is my gradle setup correct?', 'apply gradle best practices', 'fix my build to follow best practices', 'make my build follow best practices', 'modernize my build', or simply 'check best practices'. Also trigger when the user asks about Gradle build quality concerns such as dependency management, build performance, build structure, or task wiring."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.1.0"
  catalog_captured: "2026-08-27"
  catalog_gradle_version: "9.7.1"
  catalog_verified: "2026-09-16"
  catalog_source: "https://docs.gradle.org/current/userguide/best_practices.html"
---

# Gradle Best Practices

Audit a project against the official Gradle best practices, produce a structured findings report, and propose concrete code changes to fix the issues. Checks and fixes cover build scripts (`*.gradle.kts`, `*.gradle`), settings files, `gradle.properties`, the wrapper config, the version catalog, and Java/Kotlin/Groovy source under `buildSrc/` and `build-logic/`.

**The best-practices catalog ships with this skill, pre-digested, under `references/`.** Read it from disk. Do not fetch anything from the network at run time.

**Which catalog you have:** 45 practices, captured 2026-08-27 and verified complete against the Gradle **9.7.1** documentation on 2026-09-16. That is every practice in the published index, plus `dont_assume_plugin_order`, which the General category page documents but the index omits.

**The trade-off, stated plainly:** a bundled catalog is reproducible but can go stale. Fetching the live docs would always reflect the newest practices; reading a bundled copy means every run checks the same things the same way, costs no network, and cannot be truncated or paraphrased in transit. Gradle adds practices at most once per release, so the exposure is bounded — but it is real. If the project you are auditing targets a Gradle version newer than the one above, say so in the report: there may be practices this catalog does not know about. Do not fetch them mid-run; see "Keeping the catalog current" at the end.

## Sources of truth

Read these from the skill directory:

- **`references/index.md`** — the full catalog: every best practice with its title, category, anchor, and the Gradle version that introduced it, plus an applicability triage table saying which category files a given project needs.
- **`references/<category>.md`** — one file per category, holding the decoded entries: `general.md`, `structuring-builds.md`, `dependencies.md`, `tasks.md`, `performance.md`, `security.md`, `testing.md`.
- **`references/fixes/<anchor>.md`** — one file per practice, holding the fix and, for most entries, the documentation's own `Don't`/`Do` pair in Kotlin DSL. Read one only when you are about to propose that specific fix; they total roughly 105 KB and reading them all would swamp the context for no gain.

The direct link for any given best practice is still `https://docs.gradle.org/current/userguide/best_practices_<category>.html#<anchor>`, where `<anchor>` is the ID recorded in `references/index.md`. Cite those URLs in the report so the reader can follow up — but read the bundled file, never fetch it.

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

## Step 2: Read the best-practices catalog

1. Read `references/index.md`. It gives the full `(title, category, anchor, added-in-version)` list and an applicability triage table.
2. Use that triage table to decide which category files this project can possibly violate. `general.md` and `performance.md` always apply; the rest have preconditions (no custom task source means `tasks.md` and `testing.md` are out, for example). Skipping a category here is a legitimate *not applicable*, and Step 5 reports it as such.
3. Read each applicable `references/<category>.md`. Each entry carries its rule, precondition, detection recipe, and severity band — everything needed to decide.

Do not read `references/fixes/` yet. Those files are fix material, not detection material; Step 6 reads them one at a time.

Say which categories you skipped and why, rather than silently dropping them. If a reference file is missing or unreadable, say so and stop — do not fall back to memorized best practices or to fetching the docs.

## Step 3: Take each entry's detection approach from the catalog

The translation from documentation prose into a concrete check is already done, once, and recorded in the category files. **Do not re-derive it.** The recipes are this skill's fixed contract: two runs against the same project must check the same things the same way, and a re-derived check breaks that. Each entry gives you:

1. **Applies when** — the precondition. If the project does not meet it, the entry is *not applicable*; count it and move on. (No Kotlin plugin applied means the Kotlin-stdlib entry is out. No custom tasks or plugins means the TestKit entry is out.)
2. **Detect** — the check to run against the files discovered in Step 1, marked with its kind:
   - **Deterministic** — a specific string, glob, or property value answers it yes/no. Examples: any `.gradle` file present (Kotlin DSL), `distributionUrl` ends in `-all.zip` (bin distribution), `org.gradle.caching=true` missing (build cache), `apply plugin:` in a build script (plugins block), `afterEvaluate {` anywhere (avoid `afterEvaluate`), `PathSensitivity.ABSOLUTE` in custom task source.
   - **Heuristic** — requires judgment across multiple files (e.g., "duplication across subprojects suggests a convention plugin is missing", "many source files in a single project suggests modularization is needed", "`dependsOn` is fine for lifecycle tasks but not for tasks with actions"). Flag only on the evidence the entry names, and note the uncertainty in the finding.
3. **Severity band** — given per entry. These bands are this skill's editorial classification; the official docs assign none, so do not present them as Gradle ranking one practice above another.
   - **High** — security risks, likely build failures, broken configuration cache, or significant correctness problems.
   - **Medium** — suboptimal builds, maintenance burden, or violations of Gradle conventions.
   - **Recommendation** — modern idioms and nice-to-have improvements.

Run every applicable check. Batch the searching by pattern rather than by entry — one pass per pattern across the discovered files is cheaper than re-reading every file once per entry.

## Step 4: Check the project

Apply each detection approach by searching and reading the files discovered in Step 1. Record each finding with: best practice title, anchor URL, file(s) and line(s) where the violation appears, a one-sentence description, a suggested fix, and the severity band.

Violations are not mutually exclusive: one line can violate several practices at once, and matching a line to one practice does not exhaust it. Example: `dependsOn 'listMaintainedCars'` between two tasks with actions violates both *Don't hardcode task names* (the string) and *Avoid dependsOn* (the coupling) — fixing the string form to `dependsOn someTaskProvider` resolves the first and leaves the second. Record one finding per violated practice, even when findings share a line.

## Step 5: Present the report

If no issues were found, emit a single line: **No issues found.** Then stop.

Otherwise:

```
# Gradle Best Practices Audit

Catalog: bundled references/index.md — captured [catalog_captured], Gradle [catalog_gradle_version]
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
- Before making a given change, read `references/fixes/<anchor>.md` for that practice. It holds the change to make and, for most entries, the documentation's own `Don't`/`Do` pair in Kotlin DSL — the **Don't** block is the shape to match, the **Do** block the shape to write. Long blocks are excerpted around the lines that actually differ, with `// ...` marking the elision; copy the shape, not the surrounding scaffolding. Read these one at a time, as you reach each fix — never up front. Five entries (`modularize_builds`, `no_source_in_root`, `favor_composite_builds`, `use_convention_plugins`, `test_custom_types_with_testkit`) carry no `Don't`/`Do` pair, because the documentation's example is a whole-project layout; their `Fix` prose is the specification.
- Start with the highest-priority issues. Group related fixes (e.g., all `repositories {}` blocks moved at once).
- For **straightforward fixes** (adding `org.gradle.caching=true`, renaming `-all.zip` to `-bin.zip`, adding `rootProject.name`, swapping `apply plugin:` for the `plugins {}` block, adding `group`/`description` to a task, replacing `.get()` with `.map { }`), edit the file in place and show the diff.
- For **source-level fixes** in `buildSrc/` or `build-logic/` (replacing `PathSensitivity.ABSOLUTE`, removing `project.` access inside `@TaskAction`, adding `attributes { }` to consumable configurations), apply the edit and re-read the file to confirm it still compiles.
- For **structural fixes** (migrating `buildSrc/` to `build-logic/`, modularizing a project, converting Groovy DSL to Kotlin DSL, extracting convention plugins from duplication), describe the plan first, get user confirmation — or, unattended, record the plan and proceed without it — then apply incrementally with a checkpoint after each step.
- After each fix, confirm the change resolved the issue. If a fix uncovers a related issue (e.g., moving repositories to settings reveals that `FAIL_ON_PROJECT_REPOS` should be set), surface that as a follow-up.
- After fixing a line, re-check it against the remaining findings and the full catalog: a fix for one facet often leaves a co-located violation intact, or introduces a new one.
- If the user declines a fix, leave it as-is and move on.

## Keeping the catalog current

The bundled catalog is regenerated per Gradle release, not per run. When the docs move, re-capture `references/` from the URLs recorded in `index.md`, review the diff, and update this file's frontmatter: `metadata.version`, `catalog_captured`, `catalog_gradle_version`, and `catalog_verified`.

Keep those honest — a fresh-looking date over an unchecked catalog is worse than an old one, because it hides the staleness instead of showing it. If a check finds the catalog already complete, bump `catalog_verified` alone and leave `catalog_captured` where it is.

Never patch the catalog from inside a run.
