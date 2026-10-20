# gradle-wrapper-upgrade v1.1.0 — Benchmark Data

Each scenario gave a model the same task twice: once without the skill and once with it, as two independent runs on the same fixture. 4 scenarios × 6 models, one run each. The summary is generated from the tables below.

Skill tested: `git+https://github.com/gradle/gradle-skills@tt/skills-1.0.1#skills/gradle-wrapper-upgrade`, revision `401b1fe3ee3c70cd1d73b0bc81eda27b2ca235c2`.

Runs made 2026-10-19.

---

## Findings

**Helps a lot, at higher cost.** Claude Opus 5.5 and GPT-5.6 Luna pass every check with the skill, closing the whole gap, at roughly twice the cost or more and somewhat longer run times.

**Helps a lot, cost not priced.** Claude Haiku 5.5 and Claude Sonnet 5.5 pass every check with the skill, closing the whole gap; no price is configured for them, and they take somewhat longer with it.

**Helps a lot, for a little less.** DeepSeek V4 Pro passes every check with the skill, closing the whole gap, and costs and takes a little less with it.

**Helps a lot, short of the whole gap.** Qwen3.6 35B-A3B Coding (NVFP4) closes most of the gap, served locally with no price, and finishes faster with the skill; it also lost a check with it.

---

## At a glance

| Model | Harness | Without skill | With skill | Gap closed | Level | Run-to-run differences | Beyond run-to-run variation | Cost (with ÷ without) |
| :--- | :--- | ---: | ---: | ---: | :--- | ---: | :--- | ---: |
| Claude Haiku 5.5 | Claude Code | 55% | 100% | +100% | High | 0 of 5 checks | Yes | n/a |
| Claude Opus 5.5 | Claude Code | 65% | 100% | +100% | High | 0 of 5 checks | Yes | 2.07× |
| Claude Sonnet 5.5 | Claude Code | 65% | 100% | +100% | High | 0 of 5 checks | Yes | n/a |
| DeepSeek V4 Pro | OpenCode | 50% | 100% | +100% | High | 0 of 5 checks | Yes | 0.90× |
| GPT-5.6 Luna | OpenCode | 50% | 100% | +100% | High | 0 of 5 checks | Yes | 2.38× |
| Qwen3.6 35B-A3B Coding (NVFP4) | Claude Code | 35% | 80% | +69% | High | 0 of 5 checks | Yes | local |

*Without skill*: checks passed without the skill, of all checks in the compared scenarios.

*With skill*: checks passed with the skill, of all checks in the compared scenarios.

*Gap closed*: when the skill gains checks overall, the share of the checks failed without it that pass with it, net of losses; when it loses checks overall, the share of the checks passed without it that fail with it, as a negative figure. It is not the difference between *With skill* and *Without skill*.

*Level* follows mechanically from *Gap closed*: High at +67% or more, Medium from +33%, Low below that, None when the totals are equal, Counterproductive when fewer checks pass with the skill, and Nothing to fix when every check passed without it. With one run per side, a change of a check or two can come from run-to-run variation alone.

*Run-to-run differences*: how many checks differed between two identical runs.

*Beyond run-to-run variation*: Yes when the difference between *With skill* and *Without skill*, in checks, is larger than the number of checks expected to differ between two identical runs: the share of checks that differed in *Run-to-run differences*, applied to all checks in the compared scenarios. No otherwise, and n/a when the model has no identical runs.

*Cost*: the cost of the runs with the skill divided by the cost of the runs without it. It is local for a model served locally, which has no price, and n/a where no price is configured; `≥` marks a lower bound from a run that stopped at a limit.

---

## Summary

4 scenarios, 6 models, one run without and one run with the skill for each pair. Generated from the tables below.

### Per model

- `claude-haiku-5-5` on `claude-code 2.1.281`: 11 / 20 of 20 checks passed without / with the skill, 9 gains and 0 losses; 0 of 5 checks differed between two identical runs. Skill loaded in 4 of 4 runs. With ÷ without: cost n/a, wall clock 1.14×, output tokens 1.13×.
- `claude-opus-5-5` on `claude-code 2.1.281`: 13 / 20 of 20 checks passed without / with the skill, 7 gains and 0 losses; 0 of 5 checks differed between two identical runs. Skill loaded in 4 of 4 runs. With ÷ without: cost 2.07×, wall clock 1.30×, output tokens 1.46×.
- `claude-sonnet-5-5` on `claude-code 2.1.281`: 13 / 20 of 20 checks passed without / with the skill, 7 gains and 0 losses; 0 of 5 checks differed between two identical runs. Skill loaded in 4 of 4 runs. With ÷ without: cost n/a, wall clock 1.30×, output tokens 1.51×.
- `deepseek-v4-pro` on `opencode 1.18.30`: 10 / 20 of 20 checks passed without / with the skill, 10 gains and 0 losses; 0 of 5 checks differed between two identical runs. Skill loaded in 4 of 4 runs. With ÷ without: cost 0.90×, wall clock 0.80×, output tokens 0.56×.
- `gpt-5-6-luna` on `opencode 1.18.30`: 10 / 20 of 20 checks passed without / with the skill, 10 gains and 0 losses; 0 of 5 checks differed between two identical runs. Skill loaded in 4 of 4 runs. With ÷ without: cost 2.38×, wall clock 1.44×, output tokens 1.86×.
- `qwen3-6-35b-a3b-coding-nvfp4` on `claude-code 2.1.233`: 7 / 16 of 20 checks passed without / with the skill, 10 gains and 1 loss; 0 of 5 checks differed between two identical runs. Skill loaded in 4 of 4 runs. With ÷ without: cost local, wall clock 0.63×, output tokens 0.61×.

### Checks with the same result for every model

- `project-builds` in `upgrade`: passed with and without the skill, for all 6 models.
- `wrapper-properties` in `upgrade`: failed without the skill and passed with it, for all 6 models.
- `no-collateral-damage` in `upgrade`: passed with and without the skill, for all 6 models.
- `non-version-properties-preserved` in `upgrade`: passed with and without the skill, for all 6 models.
- `non-version-properties-preserved` in `sha-already-pinned`: passed with and without the skill, for all 6 models.
- `explained-how` in `advice-only`: passed with and without the skill, for all 6 models.
- `rolled-back` in `upgrade-blocked`: failed without the skill and passed with it, for all 6 models.
- `wrapper-task-pinned` in `upgrade-blocked`: failed without the skill and passed with it, for all 6 models.
- `reported-blocked` in `upgrade-blocked`: failed without the skill and passed with it, for all 6 models.
- `advised-next-step` in `upgrade-blocked`: failed without the skill and passed with it, for all 6 models.

Notes at the end of the report record 6 verified statements about the data and the scorers.

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

Every run used JDK 17, with network access on.

### Scenarios

- **`upgrade`** — 5 checks, prompt P1. `sample-stale-wrapper`, a one-module `java-library` build on a Gradle 8.5 wrapper with no `distributionSha256Sum`. The prompt asks for the wrapper to be upgraded to Gradle 9.0.0.
- **`sha-already-pinned`** — 5 checks, prompt P1. `sample-pinned-wrapper`, the `upgrade` fixture plus one line: Gradle 8.5's `distributionSha256Sum`. With a checksum set, a `wrapper` task run that changes `--gradle-version` without a matching `--gradle-distribution-sha256-sum` fails. The prompt is the same as `upgrade`'s.
- **`advice-only`** — 2 checks, prompt P2. The `upgrade` fixture, with the prompt asking how to upgrade the wrapper to Gradle 9.0.0 rather than asking for the upgrade.
- **`upgrade-blocked`** — 8 checks, prompt P1. `sample-kiln-registry`, a Gradle 8.5 build whose root build script and `buildSrc` convention plugins call `Project.getConvention()`, `JavaPluginConvention` and `Project.exec`, which Gradle 9.0.0 removed. The first `wrapper` run repoints `distributionUrl` at 9.0.0; the build then fails to configure under 9.0.0. The prompt is the same as `upgrade`'s. The project is staged without a git repository.

### Prompts

The full text given to the agent, the same with and without the skill.

**P1**, used by `upgrade`, `sha-already-pinned`, `upgrade-blocked`

> Upgrade this project's Gradle wrapper to Gradle 9.0.0.

**P2**, used by `advice-only`

> How do I upgrade this project's Gradle wrapper to Gradle 9.0.0?

---

## Results by model

Checks passed, without the skill / with it, of the total.

| Model (without / with skill) | `upgrade` | `sha-already-pinned` | `advice-only` | `upgrade-blocked` | Total | Gains | Losses |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: | ---: |
| `claude-haiku-5-5` | 3 / 5 of 5 | 4 / 5 of 5 | 2 / 2 of 2 | 2 / 8 of 8 | 11 / 20 of 20 | 9 | 0 |
| `claude-opus-5-5` | 4 / 5 of 5 | 5 / 5 of 5 | 2 / 2 of 2 | 2 / 8 of 8 | 13 / 20 of 20 | 7 | 0 |
| `claude-sonnet-5-5` | 4 / 5 of 5 | 5 / 5 of 5 | 2 / 2 of 2 | 2 / 8 of 8 | 13 / 20 of 20 | 7 | 0 |
| `deepseek-v4-pro` | 3 / 5 of 5 | 4 / 5 of 5 | 1 / 2 of 2 | 2 / 8 of 8 | 10 / 20 of 20 | 10 | 0 |
| `gpt-5-6-luna` | 3 / 5 of 5 | 4 / 5 of 5 | 1 / 2 of 2 | 2 / 8 of 8 | 10 / 20 of 20 | 10 | 0 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 3 / 5 of 5 | 2 / 2 of 5 | 2 / 2 of 2 | 0 / 7 of 8 | 7 / 16 of 20 | 10 | 1 |

A gain is a check that failed without the skill and passed with it; a loss is the reverse.

### Skill loading and run-to-run variation

| Model | Skill loaded | Differences between two identical runs |
| :--- | ---: | ---: |
| `claude-haiku-5-5` | 4 of 4 runs | 0 of 5 checks |
| `claude-opus-5-5` | 4 of 4 runs | 0 of 5 checks |
| `claude-sonnet-5-5` | 4 of 4 runs | 0 of 5 checks |
| `deepseek-v4-pro` | 4 of 4 runs | 0 of 5 checks |
| `gpt-5-6-luna` | 4 of 4 runs | 0 of 5 checks |
| `qwen3-6-35b-a3b-coding-nvfp4` | 4 of 4 runs | 0 of 5 checks |

*Skill loaded*: runs with the skill available in which the model invoked it. *Differences between two identical runs*: see Run-to-run variation.

---

## Results by scenario

✅ passed, ❌ failed, ⚠️ could not be graded; — where a model has no run.

### upgrade

`sample-stale-wrapper`, a one-module `java-library` build on a Gradle 8.5 wrapper with no `distributionSha256Sum`. The prompt asks for the wrapper to be upgraded to Gradle 9.0.0.

- `project-builds` — Runs `./gradlew build` in the final project. PASS when it exits 0.
- `wrapper-properties` — Reads `gradle/wrapper/gradle-wrapper.properties`. PASS when `distributionUrl` names `gradle-9.0.0-bin.zip` and `distributionSha256Sum` equals Gradle 9.0.0's published SHA-256.
- `wrapper-files` — Hashes `gradlew`, `gradlew.bat` and `gradle/wrapper/gradle-wrapper.jar`. PASS when all three match the files the Gradle 9.0.0 `wrapper` task generates.
- `no-collateral-damage` — Compares every non-wrapper fixture file with its shipped SHA-256 and scans for new files, skipping `build` directories and dot-entries. PASS when nothing was modified, deleted or added outside the four wrapper files.
- `non-version-properties-preserved` — Reads the six version-independent entries of `gradle-wrapper.properties` (`distributionBase`, `distributionPath`, `networkTimeout`, `validateDistributionUrl`, `zipStoreBase`, `zipStorePath`). PASS when all six are present with their shipped values.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `wrapper-properties` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `wrapper-files` | ❌ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `no-collateral-damage` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |
| `non-version-properties-preserved` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |

### sha-already-pinned

`sample-pinned-wrapper`, the `upgrade` fixture plus one line: Gradle 8.5's `distributionSha256Sum`. With a checksum set, a `wrapper` task run that changes `--gradle-version` without a matching `--gradle-distribution-sha256-sum` fails. The prompt is the same as `upgrade`'s.

- `project-builds` — Runs `./gradlew build` in the final project. PASS when it exits 0.
- `wrapper-properties` — Reads `gradle/wrapper/gradle-wrapper.properties`. PASS when `distributionUrl` names `gradle-9.0.0-bin.zip` and `distributionSha256Sum` equals Gradle 9.0.0's published SHA-256.
- `wrapper-files` — Hashes `gradlew`, `gradlew.bat` and `gradle/wrapper/gradle-wrapper.jar`. PASS when all three match the files the Gradle 9.0.0 `wrapper` task generates.
- `no-collateral-damage` — Compares every non-wrapper fixture file with its shipped SHA-256 and scans for new files, skipping `build` directories and dot-entries. PASS when nothing was modified, deleted or added outside the four wrapper files.
- `non-version-properties-preserved` — Reads the six version-independent entries of `gradle-wrapper.properties` (`distributionBase`, `distributionPath`, `networkTimeout`, `validateDistributionUrl`, `zipStoreBase`, `zipStorePath`). PASS when all six are present with their shipped values.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `wrapper-properties` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ❌ |
| `wrapper-files` | ❌ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `no-collateral-damage` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ❌ |
| `non-version-properties-preserved` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |

### advice-only

The `upgrade` fixture, with the prompt asking how to upgrade the wrapper to Gradle 9.0.0 rather than asking for the upgrade.

- `did-not-upgrade` — Reads the wrapper files. PASS when `distributionUrl` still names Gradle 8.5, no `distributionSha256Sum` was added, and `gradlew`, `gradlew.bat` and `gradle-wrapper.jar` are byte-identical to the shipped files.
- `explained-how` — Matches the agent's assistant messages, not its tool calls, against a pattern for a `gradlew` or `gradle` invocation of the `wrapper` task carrying `--gradle-version` with a value. PASS when any message matches.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `did-not-upgrade` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ | ✅ / ✅ |
| `explained-how` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ |

### upgrade-blocked

`sample-kiln-registry`, a Gradle 8.5 build whose root build script and `buildSrc` convention plugins call `Project.getConvention()`, `JavaPluginConvention` and `Project.exec`, which Gradle 9.0.0 removed. The first `wrapper` run repoints `distributionUrl` at 9.0.0; the build then fails to configure under 9.0.0. The prompt is the same as `upgrade`'s. The project is staged without a git repository.

- `project-builds` — Runs `./gradlew tasks` in the final project, which configures the build. PASS when it exits 0.
- `rolled-back` — Reads the wrapper files. PASS when `distributionUrl` names Gradle 8.5, no `distributionSha256Sum` is present, and `gradlew`, `gradlew.bat` and `gradle-wrapper.jar` are byte-identical to the shipped files. The same bytes result from an arm that never ran the `wrapper` task.
- `no-collateral-damage` — Compares every non-wrapper fixture file with its shipped SHA-256 and scans for new files, skipping `build` directories and dot-entries. PASS when nothing was modified, deleted or added outside the four wrapper files.
- `wrapper-task-pinned` — Matches the agent's shell commands. PASS when one command contains `gradlew`, `wrapper`, `--gradle-version` with `9.0.0`, and `--gradle-distribution-sha256-sum`.
- `snapshot-verified` — Matches the agent's shell commands. PASS when one runs `find` with `-type f` on a path containing `SNAP` or `/tmp/`.
- `reported-blocked` — Matches the agent's assistant messages against phrases stating the wrapper was rolled back, reverted or restored, the upgrade was blocked or could not be done, or the project remains on Gradle 8.5. PASS when any message matches.
- `quoted-error` — Matches the agent's assistant messages against the removed-API names and compile errors the fixture produces under 9.0.0, such as `JavaPluginConvention`, `getConvention(`, `Project.exec`, `compileJava` or `cannot find symbol`. PASS when any message matches.
- `advised-next-step` — Matches the agent's assistant messages. PASS when they reference the Gradle upgrade guide and name Gradle 8.6 as an intermediate version, and do not name 8.14 or the latest 8.x release.

| Check (without / with skill) | `claude-haiku-5-5` | `claude-opus-5-5` | `claude-sonnet-5-5` | `deepseek-v4-pro` | `gpt-5-6-luna` | `qwen3-6-35b-a3b-coding-nvfp4` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `rolled-back` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `no-collateral-damage` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `wrapper-task-pinned` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `snapshot-verified` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ❌ |
| `reported-blocked` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |
| `quoted-error` | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ✅ / ✅ | ❌ / ✅ |
| `advised-next-step` | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ | ❌ / ✅ |

---

## Cost and time

Wall clock is the agent's active time in seconds. Cost is the harness's price for the tokens used; local for a model served locally, which has no price; n/a where no price is configured for the model. `≥ x` marks a figure from a run that stopped at a limit, which is a lower bound.

### Totals over all scenarios

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 122.9 / 140.5 (1.14×) | 10,827 / 12,207 (1.13×) | n/a / n/a |
| `claude-opus-5-5` | 139.3 / 181.6 (1.30×) | 6,786 / 9,885 (1.46×) | 0.299 / 0.619 (2.07×) |
| `claude-sonnet-5-5` | 130.2 / 169.1 (1.30×) | 6,272 / 9,442 (1.51×) | n/a / n/a |
| `deepseek-v4-pro` | 261.1 / 208.8 (0.80×) | 14,596 / 8,190 (0.56×) | 0.062 / 0.056 (0.90×) |
| `gpt-5-6-luna` | 208.7 / 300.2 (1.44×) | 5,718 / 10,611 (1.86×) | 0.028 / 0.066 (2.38×) |
| `qwen3-6-35b-a3b-coding-nvfp4` | 662.7 / 417.8 (0.63×) | 21,446 / 13,063 (0.61×) | local / local |

The figure in parentheses is with ÷ without.

### Cost and time: upgrade

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 21.5 / 39.4 | 1,002 / 3,025 | n/a / n/a |
| `claude-opus-5-5` | 29.2 / 45.6 | 987 / 2,403 | 0.046 / 0.150 |
| `claude-sonnet-5-5` | 25.6 / 47.4 | 983 / 2,293 | n/a / n/a |
| `deepseek-v4-pro` | 39.8 / 52.7 | 722 / 1,841 | 0.003 / 0.011 |
| `gpt-5-6-luna` | 62.5 / 63.8 | 1,279 / 2,231 | 0.007 / 0.009 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 177.5 / 101.7 | 6,285 / 2,697 | local / local |

### Cost and time: sha-already-pinned

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 27.0 / 34.3 | 1,547 / 3,075 | n/a / n/a |
| `claude-opus-5-5` | 36.2 / 51.1 | 1,263 / 2,564 | 0.063 / 0.171 |
| `claude-sonnet-5-5` | 30.1 / 44.8 | 1,197 / 2,378 | n/a / n/a |
| `deepseek-v4-pro` | 52.9 / 55.4 | 1,181 / 2,433 | 0.006 / 0.015 |
| `gpt-5-6-luna` | 51.0 / 71.7 | 977 / 2,173 | 0.005 / 0.013 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 208.9 / 148.4 | 7,832 / 5,191 | local / local |

### Cost and time: advice-only

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 17.4 / 17.7 | 910 / 1,259 | n/a / n/a |
| `claude-opus-5-5` | 22.6 / 28.2 | 1,195 / 1,462 | 0.055 / 0.084 |
| `claude-sonnet-5-5` | 22.2 / 22.9 | 919 / 1,252 | n/a / n/a |
| `deepseek-v4-pro` | 23.8 / 31.9 | 944 / 786 | 0.008 / 0.010 |
| `gpt-5-6-luna` | 34.1 / 22.7 | 1,093 / 431 | 0.006 / 0.003 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 126.2 / 50.5 | 1,691 / 1,414 | local / local |

### Cost and time: upgrade-blocked

| Model (without / with skill) | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 57.0 / 49.1 | 7,368 / 4,848 | n/a / n/a |
| `claude-opus-5-5` | 51.3 / 56.6 | 3,341 / 3,456 | 0.135 / 0.215 |
| `claude-sonnet-5-5` | 52.2 / 54.0 | 3,173 / 3,519 | n/a / n/a |
| `deepseek-v4-pro` | 144.6 / 68.9 | 11,749 / 3,130 | 0.044 / 0.021 |
| `gpt-5-6-luna` | 61.1 / 142.1 | 2,369 / 5,776 | 0.010 / 0.041 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 150.1 / 117.3 | 5,638 / 3,761 | local / local |

---

## Run-to-run variation

Each model ran the same task as the `upgrade` scenario twice, without the skill and with identical settings. The two runs show how much results vary when nothing changes. Values are first run / second run; `≥ x` marks a lower bound from a run that stopped at a limit.

| Model (first / second run) | Checks passed | Checks that differed | Wall clock (s) | Output tokens | Cost (USD) |
| :--- | :---: | :--- | ---: | ---: | ---: |
| `claude-haiku-5-5` | 3 / 3 of 5 | none | 23.8 / 24.4 | 1,141 / 1,000 | n/a / n/a |
| `claude-opus-5-5` | 4 / 4 of 5 | none | 29.8 / 27.9 | 1,101 / 1,025 | 0.155 / 0.048 |
| `claude-sonnet-5-5` | 4 / 4 of 5 | none | 25.6 / 31.1 | 913 / 1,083 | n/a / n/a |
| `deepseek-v4-pro` | 3 / 3 of 5 | none | 53.5 / 33.3 | 1,009 / 760 | 0.010 / 0.004 |
| `gpt-5-6-luna` | 3 / 3 of 5 | none | 56.7 / 56.8 | 1,006 / 1,034 | 0.006 / 0.006 |
| `qwen3-6-35b-a3b-coding-nvfp4` | 3 / 3 of 5 | none | 127.3 / 218.0 | 2,766 / 4,348 | local / local |

---

## Notes

- `claude-haiku-5-5`: no price is configured, so no cost is recorded.
- `claude-sonnet-5-5`: no price is configured, so no cost is recorded.
- `qwen3-6-35b-a3b-coding-nvfp4`: served locally, so no cost is recorded.
- Not every model ran on the same `claude-code` version: `2.1.233` for `qwen3-6-35b-a3b-coding-nvfp4`; `2.1.281` for `claude-haiku-5-5`, `claude-opus-5-5`, `claude-sonnet-5-5`.
- Turn, token and time limits were set per model, so they differ between models. Both runs of a comparison always had the same limits.
- Every arm with the skill fetched `gradle-wrapper-upgrade` from `tt/skills-1.0.1` at revision `401b1fe3ee3c70cd1d73b0bc81eda27b2ca235c2`.
- In `upgrade`, every arm left `distributionUrl` naming Gradle 9.0.0, and no arm without the skill left a `distributionSha256Sum` line.
- In `upgrade-blocked`, the arms without the skill for `claude-haiku-5-5`, `claude-opus-5-5`, `claude-sonnet-5-5` and `deepseek-v4-pro` modified `build.gradle.kts` and both `buildSrc` plugin sources; the arm without the skill for `qwen3-6-35b-a3b-coding-nvfp4` added `META-INF/MANIFEST.MF` and `gradle/wrapper/gradle-wrapper.jar.test`.
- In `sha-already-pinned`, the arm with the skill for `qwen3-6-35b-a3b-coding-nvfp4` added `gradle/wrapper/gradle-wrapper.jar.bak` and left `distributionUrl` naming Gradle 8.5.
- Run-to-run variation is measured on the `upgrade` fixture and prompt only; `sha-already-pinned`, `advice-only` and `upgrade-blocked` have no identical-run control of their own.
- The recorded `final-state/` directories omit `.jar` files, so `gradle-wrapper.jar` cannot be re-checked from them.
