# gradle-best-practices v1.0.1 — Benchmark Data

Each scenario gave a model the same task twice: once without the skill and once with it, as two independent runs on the same fixture. 5 scenarios × 6 models, one run each. The summary is generated from the tables below.

Skill tested: `git+https://github.com/gradle/gradle-skills@tt/skills-1.0.1#skills/gradle-best-practices`, revision `401b1fe3ee3c70cd1d73b0bc81eda27b2ca235c2`.

Runs made 2026-10-19 to 2026-10-20.

---

## Findings

**Helps a lot.** Claude Opus 5.5, DeepSeek V4 Pro and GPT-5.6 Luna: the skill closes most of the gap, at roughly one and a half to two and a half times the cost. GPT-5.6 Luna also lost a check with it.

**Large, but within run-to-run variation.** Claude Haiku 5.5: the skill closes most of the gap, but the change is within run-to-run variation. Runs take longer and use more output tokens; no price is configured.

**Helps somewhat.** Qwen3.6 35B-A3B Coding (NVFP4): the skill closes about half the gap, and runs take more than twice as long; it is served locally, so there is no cost. It also lost a check and hit a limit only with the skill.

**Little difference.** Claude Sonnet 5.5: the skill changes little, and the change is within run-to-run variation. Runs take about half again as long; no price is configured. It also lost checks with the skill.

---

## At a glance

| Model | Harness | Without skill | With skill | Gap closed | Level | Run-to-run differences | Beyond run-to-run variation | Cost (with ÷ without) |
| :--- | :--- | ---: | ---: | ---: | :--- | ---: | :--- | ---: |
| Claude Haiku 5.5 | Claude Code | 80% | 96% | +80% | High | 3 of 12 checks | No | n/a |
| Claude Opus 5.5 | Claude Code | 86% | 96% | +71% | High | 1 of 12 checks | Yes | 2.36× |
| Claude Sonnet 5.5 | Claude Code | 90% | 92% | +20% | Low | 1 of 12 checks | No | n/a |
| DeepSeek V4 Pro | OpenCode | 57% | 98% | +95% | High | 2 of 12 checks | Yes | 1.41× |
| GPT-5.6 Luna | OpenCode | 51% | 90% | +80% | High | 1 of 12 checks | Yes | 1.88× |
| Qwen3.6 35B-A3B Coding (NVFP4) | Claude Code | 16% | 61% | +53% | Medium | 1 of 12 checks | Yes | local |

*Without skill*: checks passed without the skill, of all checks in the compared scenarios.

*With skill*: checks passed with the skill, of all checks in the compared scenarios.

*Gap closed*: when the skill gains checks overall, the share of the checks failed without it that pass with it, net of losses; when it loses checks overall, the share of the checks passed without it that fail with it, as a negative figure. It is not the difference between *With skill* and *Without skill*.

*Level* follows mechanically from *Gap closed*: High at +67% or more, Medium from +33%, Low below that, None when the totals are equal, Counterproductive when fewer checks pass with the skill, and Nothing to fix when every check passed without it. With one run per side, a change of a check or two can come from run-to-run variation alone.

*Run-to-run differences*: how many checks differed between two identical runs.

*Beyond run-to-run variation*: Yes when the difference between *With skill* and *Without skill*, in checks, is larger than the number of checks expected to differ between two identical runs: the share of checks that differed in *Run-to-run differences*, applied to all checks in the compared scenarios. No otherwise, and n/a when the model has no identical runs.

*Cost*: the cost of the runs with the skill divided by the cost of the runs without it. It is local for a model served locally, which has no price, and n/a where no price is configured; `≥` marks a lower bound from a run that stopped at a limit.

---

## Summary

5 scenarios, 6 models, one run without and one run with the skill for each pair. Generated from the tables below.

### Per model

- `claude-haiku-5-5` on `claude-code 2.1.281`: 41 / 49 of 51 checks passed without / with the skill, 8 gains and 0 losses; 3 of 12 checks differed between two identical runs. Skill loaded in 2 of 5 runs. With ÷ without: cost n/a, wall clock 1.64×, output tokens 1.79×.
- `claude-opus-5-5` on `claude-code 2.1.281`: 44 / 49 of 51 checks passed without / with the skill, 5 gains and 0 losses; 1 of 12 checks differed between two identical runs. Skill loaded in 5 of 5 runs. With ÷ without: cost 2.36×, wall clock 1.78×, output tokens 1.81×.
- `claude-sonnet-5-5` on `claude-code 2.1.281`: 46 / 47 of 51 checks passed without / with the skill, 3 gains and 2 losses; 1 of 12 checks differed between two identical runs. Skill loaded in 5 of 5 runs. With ÷ without: cost n/a, wall clock 1.55×, output tokens 1.69×.
- `deepseek-v4-pro` on `opencode 1.18.30`: 29 / 50 of 51 checks passed without / with the skill, 21 gains and 0 losses; 2 of 12 checks differed between two identical runs. Skill loaded in 5 of 5 runs. With ÷ without: cost 1.41×, wall clock 1.29×, output tokens 1.45×.
- `gpt-5-6-luna` on `opencode 1.18.30`: 26 / 46 of 51 checks passed without / with the skill, 21 gains and 1 loss; 1 of 12 checks differed between two identical runs. Skill loaded in 5 of 5 runs. With ÷ without: cost 1.88×, wall clock 1.40×, output tokens 1.65×.
- `qwen3-6-35b-a3b-coding-nvfp4` on `claude-code 2.1.233`: 8 / 31 of 51 checks passed without / with the skill, 24 gains and 1 loss; 1 of 12 checks differed between two identical runs. Skill loaded in 3 of 5 runs. With ÷ without: cost local, wall clock ≥ 2.20×, output tokens ≥ 1.74×.

### Checks with the same result for every model

- `project-builds` in `structure`: passed with and without the skill, for all 6 models.
- `no-intraproject-dependson` in `structure`: failed without the skill and passed with it, for all 6 models.
- `project-builds` in `tasks`: passed with and without the skill, for all 6 models.
- `no-absolute-sensitivity` in `tasks`: passed with and without the skill, for all 6 models.
- `no-cacheif` in `tasks`: passed with and without the skill, for all 6 models.
- `no-cc-optout` in `tasks`: passed with and without the skill, for all 6 models.
- `project-builds` in `idioms`: passed with and without the skill, for all 6 models.
- `utf8-in-jvmargs` in `idioms`: failed without the skill and passed with it, for all 6 models.
- `project-builds` in `false-positives`: passed with and without the skill, for all 6 models.

### Lower bounds

- `qwen3-6-35b-a3b-coding-nvfp4` stopped at a limit in `structure` with the skill. Its figures for those runs are lower bounds.

Notes at the end of the report record 4 verified statements about the data and the scorers.

---

## What was tested

### Models and harnesses

| Model | Name | Provider model ID | Harness |
| :--- | :--- | :--- | :--- |
| `claude-haiku-5-5` | Claude Haiku 5.5 | `anthropic/claude-haiku-5-5` | `claude-code 2.1.281` |
| `claude-opus-5-5` | Claude Opus 5.5 | `anthropic/claude-opus-5-5` | `claude-code 2.1.281` |
| `claude-sonnet-5-5` | Claude Sonnet 5.5 | `anthropic/claude-sonnet-5-5` | `claude-code 2.1.281` |
| `deepseek-v4-pro` | DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` | `opencode 1.18.30` |
| `gpt-5-6-luna` | GPT-5.6 Luna | `openai/gpt-5.6-luna` | `opencode 1.18.30` |
| `qwen3-6-35b-a3b-coding-nvfp4` | Qwen3.6 35B-A3B Coding (NVFP4) | `ollama/qwen3.6:35b-a3b-coding-nvfp4` | `claude-code 2.1.233` |

Every run used JDK 21, with network access on.

**Two of these models are not the ones the v1.0.0 sweep ran.** That sweep used `claude-haiku-4-5-20251001` and `claude-sonnet-5`; this one uses `claude-haiku-5-5` and `claude-sonnet-5-5`. A newer model moves the without-skill baseline as well as the with-skill result, so for those two rows a difference between the two sweeps cannot be attributed to the skill version. `claude-opus-5-5`, `deepseek-v4-pro`, `gpt-5-6-luna` and `qwen3-6-35b-a3b-coding-nvfp4` are the same model in both, and this report's scenarios, fixtures and 51 checks are unchanged from v1.0.0, so those four rows can be read across versions.

Every figure in this report compares the two arms of one sweep — with the skill against without it, on the same model. None of them is a comparison against v1.0.0.

### Scenarios

- **`structure`** — 12 checks, prompt P1. A two-project Groovy build (root and `:reporting`) around a car-maintenance library. It plants structure and laziness violations: no `rootProject.name`, source in the root project, repositories in each build script, no version catalog, configuration duplicated across scripts, a redundant dependency, `Provider.get()` at configuration time, `dependsOn` between tasks with actions, a task looked up by name, and no wrapper checksum. The prompt asks the agent to list the violations in VIOLATIONS.md, fix them, and keep `./gradlew build` passing.
- **`tasks`** — 15 checks, prompt P1. A Kotlin DSL build (`:lib`) around a star-charting library. It plants task and dependency violations: undocumented tasks, `PathSensitivity.ABSOLUTE`, `outputs.cacheIf { true }` instead of `@CacheableTask`, two tasks sharing an output directory, `project` access in a task action behind `notCompatibleWithConfigurationCache`, a configuration resolved in the script body, unfiltered `google()` in settings, blanket `configurations.all` exclusions, a consumable configuration without attributes, vaguely named catalog entries, no wrapper checksum, and the configuration cache off. The prompt asks the agent to list, fix, and keep the build passing.
- **`idioms`** — 14 checks, prompt P1. A Groovy multi-project build (`:core`, `:services:exporter`) around a recipe library. It plants legacy idioms: `apply plugin:` in a `subprojects {}` block, `afterEvaluate`, an `org.gradle.internal` import, no root `gradle.properties` (so no build cache, configuration cache or UTF-8 flag), a `gradle.properties` in a subproject, a map-notation dependency, an empty intermediate `:services` project, hashing at configuration time, an eager `fileTree(...).files`, and no wrapper checksum. The prompt asks the agent to list, fix, and keep the build passing.
- **`plugin-authoring`** — 8 checks, prompt P1. A Kotlin DSL multi-project build (`:telemetry`, `:dispatch`, `:docs`) with two convention plugins in an included `build-logic` build. Each plugin silently does nothing unless another plugin was applied first. It also plants a helper in `buildSrc`, `isPreserveFileTimestamps = true` on an archive, and `.map { ... .get() }` where `flatMap` is needed. `:docs` is not a Java library. The prompt asks the agent to list, fix, and keep the build passing.
- **`false-positives`** — 2 checks, prompt P2. Unmodified `gradle init` output for a Kotlin DSL Java library, plus a UTF-8 `org.gradle.jvmargs` line. The prompt asks for an audit only: list issues in VIOLATIONS.md without changing any existing file.

### Prompts

The full text given to the agent, the same with and without the skill.

**P1**, used by `structure`, `tasks`, `idioms`, `plugin-authoring`

> This Gradle build succeeds, but it probably has issues with things not done in the proper way. Investigate the
> build configuration and fix what you find, making sure `./gradlew build` still succeeds.
> The library's code and behavior must be preserved; restructuring which project builds it and how is allowed.
> This is NOT just an audit, your task is to apply fixes to the build.
> Before fixing anything, write a file named VIOLATIONS.md at the root of the project containing ONLY one line per
> issue discovered, starting with the file name containing it, then a colon and a space and the line number where it
> begins, then another colon and a space then a brief one sentence description of the issue.
> Each line must describe exactly ONE issue: a line of code that violates two practices gets two lines; never combine issues on one line.
> Add no headers, blank lines, or any text besides the issue lines.
> Then apply your fixes.
> You are running unattended; no one can answer questions, so make all decisions yourself.
> Before finishing, re-read your VIOLATIONS.md and either fix each item or record why not in a REMAINING-UNFIXED.md file.

**P2**, used by `false-positives`

> This Gradle build succeeds, but it probably has issues with things not done in the proper way. Investigate the
> build configuration and report what you find, NOT changing any existing file.
> This is ONLY an audit, your task is NOT to apply fixes to the build.
> Write a file named VIOLATIONS.md at the root of the project containing ONLY one line per issue discovered, starting
> with the file name containing it, then a colon and a space and the line number where it begins, then another colon
> and a space then a brief one sentence description of the issue.
> Each line must describe exactly ONE issue: a line of code that violates two practices gets two lines; never combine issues on one line.
> Add no headers, blank lines, or any text besides the issue lines.
> If you discover no issues, write an empty VIOLATIONS.md.
> You are running unattended; no one can answer questions, so make all decisions yourself.

---

## Results by model

Checks passed, without the skill / with it, of the total.

| Model (without / with skill) | `structure` | `tasks` | `idioms` | `plugin-authoring` | `false-positives` | Total | Gains | Losses |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | ---: | ---: |
| `claude-haiku-5-5` | 10 / 11 of 12 | 12 / 15 of 15 | 12 / 14 of 14 | 6 / 8 of 8 | 1 / 1 of 2 | 41 / 49 of 51 | 8 | 0 |
| `claude-opus-5-5` | 10 / 12 of 12 | 13 / 14 of 15 | 12 / 14 of 14 | 8 / 8 of 8 | 1 / 1 of 2 | 44 / 49 of 51 | 5 | 0 |
| `claude-sonnet-5-5` | 11 / 12 of 12 | 13 / 12 of 15 | 13 / 14 of 14 | 8 / 8 of 8 | 1 / 1 of 2 | 46 / 47 of 51 | 3 | 2 |
| `deepseek-v4-pro` | 5 / 12 of 12 | 7 / 15 of 15 | 10 / 14 of 14 | 6 / 8 of 8 | 1 / 1 of 2 | 29 / 50 of 51 | 21 | 0 |
| `gpt-5-6-luna` | 3 / 10 of 12 | 8 / 14 of 15 | 8 / 13 of 14 | 6 / 7 of 8 | 1 / 2 of 2 | 26 / 46 of 51 | 21 | 1 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 2 / 7 of 12 | 4 / 9 of 15 | 1 / 8 of 14 | 0 / 6 of 8 | 1 / 1 of 2 | 8 / 31 of 51 | 24 | 1 |

A gain is a check that failed without the skill and passed with it; a loss is the reverse.

### Skill loading and run-to-run variation

| Model | Skill loaded | Differences between two identical runs |
| :--- | ---: | ---: |
| `claude-haiku-5-5` | 2 of 5 runs | 3 of 12 checks |
| `claude-opus-5-5` | 5 of 5 runs | 1 of 12 checks |
| `claude-sonnet-5-5` | 5 of 5 runs | 1 of 12 checks |
| `deepseek-v4-pro` | 5 of 5 runs | 2 of 12 checks |
| `gpt-5-6-luna` | 5 of 5 runs | 1 of 12 checks |
| `qwen3-6-35b-a3b-coding-nvfp4` | 3 of 5 runs | 1 of 12 checks |

*Skill loaded*: runs with the skill available in which the model invoked it. *Differences between two identical runs*: see Run-to-run variation.

---

## Results by scenario

✅ passed, ❌ failed, ⚠️ could not be graded; — where a model has no run.

### structure

A two-project Groovy build (root and `:reporting`) around a car-maintenance library. It plants structure and laziness violations: no `rootProject.name`, source in the root project, repositories in each build script, no version catalog, configuration duplicated across scripts, a redundant dependency, `Provider.get()` at configuration time, `dependsOn` between tasks with actions, a task looked up by name, and no wrapper checksum. The prompt asks the agent to list the violations in VIOLATIONS.md, fix them, and keep `./gradlew build` passing.

- `project-builds` — Runs `./gradlew build` on the final tree. PASS when it succeeds.
- `root-project-named` — PASS when a settings script sets `rootProject.name`, ignoring comments.
- `version-catalog` — PASS when `gradle/libs.versions.toml` exists.
- `repos-not-in-build-scripts` — PASS when no main-build script outside `buildSrc` or an included build declares `mavenCentral()`, ignoring comments.
- `no-eager-getbyname` — PASS when no `.gradle` or `.gradle.kts` script contains `getByName`, ignoring comments.
- `no-intraproject-dependson` — PASS when no build script declares `dependsOn` between tasks in the same project; edges to included builds are not flagged.
- `lazy-extension-wiring` — An init script changes the `carLog` extension's `logFileName` after every script has evaluated, then runs `recordDemoMaintenance`. PASS when the task writes the file under the changed name.
- `no-source-in-root` — PASS when no `src/main/` or `src/test/` directory exists in the root project.
- `convention-plugins` — PASS when `buildSrc` or an included build contains a precompiled script plugin under `src/main/` and a main-build script applies it.
- `wrapper-checksum-engaged` — Reads VIOLATIONS.md and `gradle/wrapper/gradle-wrapper.properties`. PASS when VIOLATIONS.md has a line citing the wrapper properties file and the checksum, or when the properties file pins a 64-digit hex `distributionSha256Sum`.
- `no-duplicate-dependencies` — An init script walks each project's `compileClasspath`. PASS when no external module a project declares directly also arrives through one of its project dependencies.
- `violations-count` — Counts the non-blank lines in VIOLATIONS.md. PASS when there are at least as many as the practices planted in the fixture.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `root-project-named` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `version-catalog` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `repos-not-in-build-scripts` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `no-eager-getbyname` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `no-intraproject-dependson` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `lazy-extension-wiring` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `no-source-in-root` | ❌ / ❌ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `convention-plugins` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ | ❌ / ❌ |
| `wrapper-checksum-engaged` | ✅ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `no-duplicate-dependencies` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ❌ |
| `violations-count` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ | ❌ / ✅ |

### tasks

A Kotlin DSL build (`:lib`) around a star-charting library. It plants task and dependency violations: undocumented tasks, `PathSensitivity.ABSOLUTE`, `outputs.cacheIf { true }` instead of `@CacheableTask`, two tasks sharing an output directory, `project` access in a task action behind `notCompatibleWithConfigurationCache`, a configuration resolved in the script body, unfiltered `google()` in settings, blanket `configurations.all` exclusions, a consumable configuration without attributes, vaguely named catalog entries, no wrapper checksum, and the configuration cache off. The prompt asks the agent to list, fix, and keep the build passing.

- `project-builds` — Runs `./gradlew build` on the final tree. PASS when it succeeds.
- `tasks-documented` — Collects the task names registered in the build's sources, then runs `./gradlew tasks --all`. PASS when every collected task Gradle lists has a description.
- `no-absolute-sensitivity` — PASS when no `.gradle`, `.kts` or `.kt` file contains `PathSensitivity.ABSOLUTE`, ignoring comments.
- `cacheable-annotation` — An init script finds the `renderStarChart` task and walks its class hierarchy, stopping at the first `org.gradle` class. PASS when a class in it carries `@CacheableTask`.
- `no-cacheif` — PASS when no `.gradle`, `.kts` or `.kt` file contains `.cacheIf`, ignoring comments.
- `no-cc-optout` — PASS when no `.gradle`, `.kts` or `.kt` file contains `notCompatibleWithConfigurationCache`, ignoring comments.
- `google-repo-removed` — PASS when no settings script contains `google()`, ignoring comments.
- `no-configurations-all` — PASS when no `.gradle`, `.kts` or `.kt` file contains `configurations.all` or `configurations.configureEach`, ignoring comments.
- `configuration-attributes` — Runs `outgoingVariants --all` for every project. PASS when every consumable variant other than `archives` and `default` lists attributes.
- `catalog-entries-named` — Parses `gradle/libs.versions.toml`. PASS when no entry key contains `stuff` or `utils` and none is exactly `gv` or `theJson`.
- `wrapper-checksum-engaged` — Reads VIOLATIONS.md and `gradle/wrapper/gradle-wrapper.properties`. PASS when VIOLATIONS.md has a line citing the wrapper properties file and the checksum, or when the properties file pins a 64-digit hex `distributionSha256Sum`.
- `unique-task-outputs` — An init script collects every task's declared output files. PASS when no path is claimed by more than one task.
- `no-config-time-resolution` — An init script records any configuration resolved before the task graph is ready. PASS when none is.
- `config-cache-enabled` — PASS when the root `gradle.properties` sets `org.gradle.configuration-cache=true`.
- `violations-count` — Counts the non-blank lines in VIOLATIONS.md. PASS when there are at least as many as the practices planted in the fixture.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `tasks-documented` | ❌ / ✅ | ✅ / ✅ | ✅ / ❌ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `no-absolute-sensitivity` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `cacheable-annotation` | ✅ / ✅ | ❌ / ❌ | ❌ / ❌ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `no-cacheif` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `no-cc-optout` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `google-repo-removed` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ❌ | ❌ / ❌ |
| `no-configurations-all` | ✅ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ❌ |
| `configuration-attributes` | ❌ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `catalog-entries-named` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `wrapper-checksum-engaged` | ❌ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `unique-task-outputs` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `no-config-time-resolution` | ✅ / ✅ | ✅ / ✅ | ✅ / ❌ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `config-cache-enabled` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `violations-count` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |

### idioms

A Groovy multi-project build (`:core`, `:services:exporter`) around a recipe library. It plants legacy idioms: `apply plugin:` in a `subprojects {}` block, `afterEvaluate`, an `org.gradle.internal` import, no root `gradle.properties` (so no build cache, configuration cache or UTF-8 flag), a `gradle.properties` in a subproject, a map-notation dependency, an empty intermediate `:services` project, hashing at configuration time, an eager `fileTree(...).files`, and no wrapper checksum. The prompt asks the agent to list, fix, and keep the build passing.

- `project-builds` — Runs `./gradlew build` on the final tree. PASS when it succeeds.
- `plugins-block-only` — PASS when no `.gradle` or `.gradle.kts` script contains `apply plugin`, ignoring comments.
- `no-after-evaluate` — PASS when no `.gradle` or `.gradle.kts` script contains `afterEvaluate`, ignoring comments.
- `no-internal-apis` — PASS when no `.gradle` or `.gradle.kts` script contains `org.gradle.internal`, ignoring comments.
- `build-cache-enabled` — PASS when the root `gradle.properties` sets `org.gradle.caching=true`.
- `utf8-in-jvmargs` — PASS when the root `gradle.properties` contains `file.encoding=UTF-8`.
- `no-subproject-properties` — PASS when no subproject directory contains a `gradle.properties`; an included build's root file is not counted.
- `single-gav-strings` — PASS when no `.gradle` or `.gradle.kts` script declares a dependency with `group:`, `name:` or `version:` map notation, ignoring comments.
- `no-empty-project` — PASS when no settings script contains `services:exporter`, ignoring comments.
- `no-config-time-hashing` — Runs `build --dry-run` without the configuration cache. PASS when the schema-fingerprint marker the fixture logs does not appear.
- `wrapper-checksum-engaged` — Reads VIOLATIONS.md and `gradle/wrapper/gradle-wrapper.properties`. PASS when VIOLATIONS.md has a line citing the wrapper properties file and the checksum, or when the properties file pins a 64-digit hex `distributionSha256Sum`.
- `config-cache-enabled` — PASS when the root `gradle.properties` sets `org.gradle.configuration-cache=true`.
- `no-eager-filetree` — PASS when no `.gradle`, `.kts` or `.kt` file calls an eager accessor such as `.files` on a `fileTree(...)`, ignoring comments.
- `violations-count` — Counts the non-blank lines in VIOLATIONS.md. PASS when there are at least as many as the practices planted in the fixture.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `plugins-block-only` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ❌ |
| `no-after-evaluate` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `no-internal-apis` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ❌ |
| `build-cache-enabled` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `utf8-in-jvmargs` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `no-subproject-properties` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `single-gav-strings` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `no-empty-project` | ❌ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ | ❌ / ❌ |
| `no-config-time-hashing` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `wrapper-checksum-engaged` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `config-cache-enabled` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `no-eager-filetree` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `violations-count` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |

### plugin-authoring

A Kotlin DSL multi-project build (`:telemetry`, `:dispatch`, `:docs`) with two convention plugins in an included `build-logic` build. Each plugin silently does nothing unless another plugin was applied first. It also plants a helper in `buildSrc`, `isPreserveFileTimestamps = true` on an archive, and `.map { ... .get() }` where `flatMap` is needed. `:docs` is not a Java library. The prompt asks the agent to list, fix, and keep the build passing.

- `project-builds` — Runs `./gradlew build` on the final tree. PASS when it succeeds.
- `plugin-order-agnostic` — Builds a probe that applies the reporting plugin before `java-library` and runs `fleetReport`. PASS when the task exists and stamps the module.
- `convention-order-agnostic` — Builds a probe that applies the compliance plugin before the reporting plugin and runs `verifyFleetStamp`. PASS when the task exists and checks the module.
- `no-forced-java-plugin` — Lists the `:docs` tasks. PASS when `:docs` has no Java compile task. It passes on the untouched fixture.
- `no-buildsrc` — PASS when `buildSrc` has no sources and no build or settings script.
- `reproducible-archives` — PASS when no `.gradle`, `.kts` or `.kt` file sets `preserveFileTimestamps = true`, ignoring comments.
- `flatmap-for-nested-providers` — PASS when no `.gradle`, `.kts` or `.kt` file contains a `.map { ... }` block calling `.get()`, ignoring comments.
- `violations-count` — Counts the non-blank lines in VIOLATIONS.md. PASS when there are at least as many as the practices planted in the fixture.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `plugin-order-agnostic` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ❌ |
| `convention-order-agnostic` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ❌ |
| `no-forced-java-plugin` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `no-buildsrc` | ❌ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `reproducible-archives` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `flatmap-for-nested-providers` | ❌ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ❌ | ❌ / ✅ |
| `violations-count` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |

### false-positives

Unmodified `gradle init` output for a Kotlin DSL Java library, plus a UTF-8 `org.gradle.jvmargs` line. The prompt asks for an audit only: list issues in VIOLATIONS.md without changing any existing file.

- `project-builds` — Runs `./gradlew build` on the final tree. PASS when it succeeds.
- `only-defensible-findings` — Reads VIOLATIONS.md. PASS when the file exists, every line has the required format, and every line reports one of the findings that hold on the staged tree: repositories in the build script, incubating API use, no wrapper checksum, or a distribution URL outside services.gradle.org. An empty file passes.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `only-defensible-findings` | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ | ❌ / ✅ | ❌ / ❌ |

---

## Cost and time

Wall clock is the agent's active time in seconds. Cost is the harness's price for the tokens used; local for a model served locally, which has no price; n/a where no price is configured for the model. `≥ x` marks a figure from a run that stopped at a limit, which is a lower bound.

### Totals over all scenarios

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 778.8 / 1,274.9 (1.64×) | 122,793 / 219,379 (1.79×) | n/a / n/a |
| `claude-opus-5-5` | 532.7 / 950.4 (1.78×) | 35,322 / 64,044 (1.81×) | 1.297 / 3.068 (2.36×) |
| `claude-sonnet-5-5` | 514.3 / 796.0 (1.55×) | 42,350 / 71,657 (1.69×) | n/a / n/a |
| `deepseek-v4-pro` | 1,979.7 / 2,562.3 (1.29×) | 136,121 / 197,183 (1.45×) | 0.517 / 0.727 (1.41×) |
| `gpt-5-6-luna` | 607.9 / 852.4 (1.40×) | 25,300 / 41,722 (1.65×) | 0.087 / 0.164 (1.88×) |
| `qwen3-6-35b-a3b-coding-nvfp4` | 3,609.9 / ≥ 7,959.2 (≥ 2.20×) | 156,272 / ≥ 271,311 (≥ 1.74×) | local / local |

The figure in parentheses is with ÷ without.

### Cost and time: structure

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 234.1 / 360.0 | 40,819 / 67,331 | n/a / n/a |
| `claude-opus-5-5` | 138.4 / 250.1 | 10,495 / 18,636 | 0.408 / 0.855 |
| `claude-sonnet-5-5` | 135.8 / 214.5 | 12,909 / 22,722 | n/a / n/a |
| `deepseek-v4-pro` | 580.6 / 653.4 | 38,973 / 47,479 | 0.164 / 0.182 |
| `gpt-5-6-luna` | 146.5 / 221.4 | 5,540 / 12,453 | 0.021 / 0.052 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 860.5 / ≥ 2,296.1 | 34,467 / ≥ 77,584 | local / local |

### Cost and time: tasks

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 198.9 / 281.9 | 32,364 / 48,838 | n/a / n/a |
| `claude-opus-5-5` | 126.3 / 249.8 | 8,598 / 17,538 | 0.292 / 0.720 |
| `claude-sonnet-5-5` | 115.5 / 176.1 | 9,986 / 15,784 | n/a / n/a |
| `deepseek-v4-pro` | 543.1 / 620.6 | 36,282 / 46,606 | 0.130 / 0.164 |
| `gpt-5-6-luna` | 146.2 / 155.1 | 6,416 / 7,208 | 0.022 / 0.023 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 1,065.2 / 1,825.4 | 45,498 / 69,117 | local / local |

### Cost and time: idioms

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 129.6 / 191.8 | 19,123 / 33,156 | n/a / n/a |
| `claude-opus-5-5` | 100.4 / 163.8 | 7,380 / 11,389 | 0.253 / 0.557 |
| `claude-sonnet-5-5` | 101.9 / 139.8 | 9,720 / 12,627 | n/a / n/a |
| `deepseek-v4-pro` | 303.0 / 512.4 | 24,681 / 45,177 | 0.078 / 0.160 |
| `gpt-5-6-luna` | 116.2 / 165.0 | 5,247 / 7,769 | 0.017 / 0.035 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 49.1 / 933.9 | 658 / 36,401 | local / local |

### Cost and time: plugin-authoring

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 153.6 / 365.3 | 25,502 / 63,699 | n/a / n/a |
| `claude-opus-5-5` | 105.2 / 211.4 | 7,011 / 13,954 | 0.255 / 0.709 |
| `claude-sonnet-5-5` | 103.6 / 194.7 | 8,071 / 17,479 | n/a / n/a |
| `deepseek-v4-pro` | 427.5 / 585.3 | 29,089 / 43,041 | 0.106 / 0.168 |
| `gpt-5-6-luna` | 124.2 / 210.0 | 5,027 / 11,047 | 0.016 / 0.041 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 890.1 / 2,657.4 | 39,480 / 79,683 | local / local |

### Cost and time: false-positives

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 62.7 / 75.8 | 4,985 / 6,355 | n/a / n/a |
| `claude-opus-5-5` | 62.5 / 75.3 | 1,838 / 2,527 | 0.089 / 0.227 |
| `claude-sonnet-5-5` | 57.5 / 70.9 | 1,664 / 3,045 | n/a / n/a |
| `deepseek-v4-pro` | 125.5 / 190.6 | 7,096 / 14,880 | 0.039 / 0.053 |
| `gpt-5-6-luna` | 74.8 / 100.9 | 3,070 / 3,245 | 0.012 / 0.013 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 745.1 / 246.3 | 36,169 / 8,526 | local / local |

---

## Run-to-run variation

Each model ran the same task as the `structure` scenario twice, without the skill and with identical settings. The two runs show how much results vary when nothing changes. Values are first run / second run; `≥ x` marks a lower bound from a run that stopped at a limit.

| Model (first / second run) | Checks passed | Checks that differed | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | :---: | :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 7 / 8 of 12 | `repos-not-in-build-scripts`, `lazy-extension-wiring`, `wrapper-checksum-engaged` | 199.8 / 216.3 | 32,824 / 33,981 | n/a / n/a |
| `claude-opus-5-5` | 11 / 10 of 12 | `no-intraproject-dependson` | 165.9 / 140.0 | 13,248 / 11,366 | 0.590 / 0.392 |
| `claude-sonnet-5-5` | 10 / 11 of 12 | `no-source-in-root` | 131.5 / 152.1 | 11,956 / 14,982 | n/a / n/a |
| `deepseek-v4-pro` | 8 / 8 of 12 | `version-catalog`, `lazy-extension-wiring` | 495.4 / 320.9 | 41,089 / 28,585 | 0.181 / 0.086 |
| `gpt-5-6-luna` | 2 / 3 of 12 | `repos-not-in-build-scripts` | 83.8 / 128.4 | 2,374 / 5,668 | 0.010 / 0.020 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 2 / 1 of 12 | `no-duplicate-dependencies` | 1,291.6 / 1,387.2 | 47,470 / 57,065 | local / local |

---

## Notes

- `qwen3-6-35b-a3b-coding-nvfp4` stopped at a limit in: `structure` with the skill (tokens limit, 10,000,000). Its figures for those runs are lower bounds.
- `claude-haiku-5-5`: no price is configured, so no cost is recorded.
- `claude-sonnet-5-5`: no price is configured, so no cost is recorded.
- `qwen3-6-35b-a3b-coding-nvfp4`: served locally, so no cost is recorded.
- Not every model ran on the same `claude-code` version: `2.1.233` for `qwen3-6-35b-a3b-coding-nvfp4`; `2.1.281` for `claude-haiku-5-5`, `claude-opus-5-5`, `claude-sonnet-5-5`.
- Turn, token and time limits were set per model, so they differ between models. Both runs of a comparison always had the same limits.
- In each run with the skill available where the skill-used check recorded no invocation (Claude Haiku 5.5 in `false-positives`, `plugin-authoring` and `structure`; Qwen3.6 35B-A3B Coding (NVFP4) in `false-positives` and `structure`), the transcript shows the model reading the installed skill's files under `.claude/skills/gradle-best-practices/` with Bash or Read instead of invoking the Skill tool.
- Qwen3.6 35B-A3B Coding (NVFP4) in `structure` with the skill stopped at the token limit while under its turn and wall-clock limits, after it had written VIOLATIONS.md and REMAINING-UNFIXED.md.
- The untouched fixtures contain what `no-absolute-sensitivity`, `no-cacheif`, `no-cc-optout` (`lib/build.gradle.kts` in `tasks`) and `no-intraproject-dependson` (`build.gradle` in `structure`) look for, and the `idioms` fixture has no root `gradle.properties`, so each of those checks and `utf8-in-jvmargs` fails on the untouched fixture.
- Network access was on. Qwen3.6 35B-A3B Coding (NVFP4) used web search or fetch tools in `false-positives` and `structure` without the skill and in `tasks` with it; DeepSeek V4 Pro used a fetch tool in one run-to-run run.
