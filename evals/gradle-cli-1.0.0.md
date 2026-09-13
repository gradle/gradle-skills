# Gradle CLI Skill v1.0.0 — Benchmark Results

## Summary

`gradle-cli@1.0.0` was measured against Claude Haiku 4.5, Sonnet 5 and Opus 5 on
seven Gradle CLI scenarios, two arms each. In the 17 of 21 comparisons where the
model actually opened the skill, the treatment arm passed **31 of 31** task checks
against **26 of 31** for the unaided baseline — 5 gains, no regressions.

The gains concentrate almost entirely in one place. **`wrapper-upgrade` is the
only scenario where the skill changes the result for every model**: all three
baselines upgrade `distributionUrl` to 9.0.0 and stop, and all three skilled arms
also pin `distributionSha256Sum`. The only other scenario that moves is
`exclude-task-trap` on Haiku, where the unaided model takes the `-x test` bait and
drops the licence report along with them.

Everything else is at the ceiling. In four of seven scenarios every arm of every
model passed every task check, so those fixtures cannot discriminate at this model
tier and the report can claim nothing from them in either direction.

The other headline is not about the skill at all: **Haiku failed to pick the skill
up in 4 of its 7 treatment arms** — staged, never opened, no `Skill` call and no
read of its files. Those four comparisons are void. They are reported and excluded
from the effect above.

This report is keyed on **checks passed**. The harness also folds each arm's
scorers into a single pass/fail verdict; that verdict is not reported here. With no
skill staged `skill-used` returns `PASS  skill-used: n/a`, so an unaided arm folds
to `PASS` whenever its task checks pass, while a skilled arm that never opened the
skill folds to `FAIL` even when it did the task correctly. On this sweep the fold
tracks Haiku's pickup rate, not the quality of any arm's work.

---

## Setup

### What we're measuring

Each scenario runs two arms against the same Gradle project and prompt:

| Arm               | Skill                                                        |
| :---------------- | :----------------------------------------------------------- |
| `no-skills`       | Baseline — no skill provided                                  |
| `gradle-cli@1.0.0`| `gradle-skills@main#skills/gradle-cli`, resolved to `224a9b6977cc…` |

A third arm pointing at a local working copy of the skill is declared in each
experiment but was **not run**: the local copy was verified byte-identical to the
upstream revision above before the sweep, which would have made it a duplicate of
the treatment arm. It appears as `skipped` in every stored `report.json`.

All 21 treatment arms received the same skill revision — `SKILL.md` plus three
`references/` files, byte-identical across every arm.

### Models tested

| Model                             | CLI                  |
| :-------------------------------- | :------------------- |
| `anthropic/claude-haiku-4-5-20251001` | `claude-code 2.1.233` |
| `anthropic/claude-sonnet-5`           | `claude-code 2.1.233` |
| `anthropic/claude-opus-5`             | `claude-code 2.1.233` |

### Scenarios and fixtures

| Scenario | Fixture | What it asks for |
| :------- | :------ | :--------------- |
| `wrapper-upgrade` | `sample-stale-wrapper` (`sha256:6aa2317ff2b4…`) | Upgrade a Gradle 8.5 wrapper to 9.0.0 |
| `exclude-task-trap` | `sample-ledger` (`sha256:01e5134fddc4…`) | Build without running the unit tests, where `-x test` also drops a licence report |
| `etiquette-destructive-task` | `sample-publishable` (`sha256:15fc5a71d7bd…`) | Answer how to publish locally — without publishing |
| `custom-task-discovery` | `sample-hidden-task` (`sha256:467ca73d6d04…`) | Find and run a licence-verification task the prompt does not name |
| `dependency-inspection` | `sample-guava-user` (`sha256:c87fa83e74de…`) | Report the Guava version, resolvable only through a BOM |
| `multi-project-task-selection` | `sample-two-module` (`sha256:2c0d738a310c…`) | Run the tests of one subproject only |
| `test-filter-precision` | `sample-test-menagerie` (`sha256:db0e2f601b8d…`) | Run a single named test method |

Only three of these produced any movement between arms — `wrapper-upgrade`,
`exclude-task-trap`, and `etiquette-destructive-task` inside a void comparison. On
the other four, every arm of every model passed every task check (finding 5).

### Scorers

Every scenario carries a `skill-used` scorer plus task-specific checks. All task
checks are scripts that read the project tree or the transcript the arm left
behind; the evidence each one reads is archived with the run.

**`skill-used` reads differently here than in the `gradle-best-practices` report.**
With no skill staged it returns `PASS  skill-used: n/a`, so it is not a check an
unaided arm can fail. On a skilled arm it FAILs when the skill was staged and never
consulted, even if the arm did the task correctly — which is what happened on four
of Haiku's seven arms. It is excluded from every checks-passed total below.

### Scorer verdicts

| Verdict        | Meaning |
| :------------- | :------ |
| ✅ **PASS**    | The scorer's criterion was met. |
| ❌ **FAIL**    | The trial ran and the criterion was not met. |
| ⚠️ **INVALID** | The scorer could not render a verdict. No arm in this sweep returned INVALID. |

No arm in this sweep was bounded — none hit a turn, token or wall-clock cap — so
every cost figure in this report is a measurement rather than a floor.

---

## Key findings

### 1. Wrapper upgrade is the only cross-model discriminator, and it turns on one line
Every baseline — Haiku, Sonnet and Opus — edits `distributionUrl` to
`gradle-9.0.0-bin.zip` and stops there. Every skilled arm also writes
`distributionSha256Sum`. That single line is the whole of `wrapper-properties`,
which FAILs in all three baselines and PASSes in all three skilled arms. Verified
directly against the archived `gradle-wrapper.properties` of all six arms.

### 2. Haiku did not reach for the skill in 4 of 7 scenarios
`custom-task-discovery`, `dependency-inspection`, `etiquette-destructive-task` and
`test-filter-precision`: the skill was staged at
`/work/project/.claude/skills/gradle-cli` and never opened. Sonnet and Opus
consulted it in 7 of 7. Those four Haiku comparisons measure nothing about the
skill — they are a second unaided draw — and both of the only regressions in the
whole sweep sit inside one of them (finding 3). Pickup, not capability, is the
binding constraint for the smallest model here.

### 3. The two regressions are in a void arm and are a baseline draw, not a skill effect
Haiku's `etiquette-destructive-task` treatment arm went 2 → 0: it ran
`publishToMavenLocal` on a "how do I publish?" question, and never named the
command in prose. The published jar is in that arm's archived
`final-state/.../build/published-artifacts/`, so the behaviour is real, not a
scorer artifact. But that arm never opened the skill, so what the pair actually
shows is two unaided Haiku draws disagreeing with each other on the same prompt.
It bounds Haiku's etiquette variance; it says nothing about `gradle-cli`.

### 4. Opus and Sonnet need the skill for exactly one thing
Both pass 11 of 12 task checks unaided and 12 of 12 with the skill, the single
difference being `wrapper-properties`. The skill is picked up and used correctly
everywhere; it simply has little left to correct at this tier.

### 5. Four of seven fixtures never discriminated
`custom-task-discovery`, `dependency-inspection`, `multi-project-task-selection`, `test-filter-precision`:
every arm of every model passed every task check. A check that always agrees
cannot support a claim in either direction. This is a limitation of the benchmark,
not evidence that the skill is inert — a fixture that no model fails unaided cannot
show a skill correcting it.

### 6. The `gradle invocations` counter undercounts, provably
Nine of 42 arms record `gradle_calls: 0`, and at least three of those cannot be
true. `dependency-inspection` hides the Guava version behind
`com.google.cloud:libraries-bom:26.44.0` precisely so it cannot be read out of a
build file, yet both Opus arms and Sonnet's treatment arm wrote the correct
`33.2.1-jre` while recording zero invocations; `wrapper-upgrade`/Sonnet/treatment
records zero while regenerating all three wrapper files and pinning the checksum.
The counter recognises a bare `./gradlew` and misses prefixed forms such as
`timeout N ./gradlew`. Treat the `Gradle runs` row as a diagnostic only.

### 7. n = 1 per arm, with no A/A control in this sweep
Single trials throughout. See [Noise floor](#noise-floor) for what that does and
does not permit.

---

## Summary tables

### Checks passed (excluding `skill-used`)

Void comparisons — where the skilled arm never opened the skill — are marked † and
excluded from the totals below them.

| Model | Scenario | `no-skills` | `gradle-cli@1.0.0` | Δ |
| :---- | :------- | :---------: | :----------------: | :-: |
| Haiku 4.5 | `wrapper-upgrade` | 1 / 3 | 3 / 3 | **+2** |
| Haiku 4.5 | `exclude-task-trap` | 2 / 3 | 3 / 3 | **+1** |
| Haiku 4.5 | `etiquette-destructive-task` † | 2 / 2 | 0 / 2 | — |
| Haiku 4.5 | `custom-task-discovery` † | 1 / 1 | 1 / 1 | — |
| Haiku 4.5 | `dependency-inspection` † | 1 / 1 | 1 / 1 | — |
| Haiku 4.5 | `multi-project-task-selection` | 1 / 1 | 1 / 1 | 0 |
| Haiku 4.5 | `test-filter-precision` † | 1 / 1 | 1 / 1 | — |
| Sonnet 5 | `wrapper-upgrade` | 2 / 3 | 3 / 3 | **+1** |
| Sonnet 5 | `exclude-task-trap` | 3 / 3 | 3 / 3 | 0 |
| Sonnet 5 | `etiquette-destructive-task` | 2 / 2 | 2 / 2 | 0 |
| Sonnet 5 | `custom-task-discovery` | 1 / 1 | 1 / 1 | 0 |
| Sonnet 5 | `dependency-inspection` | 1 / 1 | 1 / 1 | 0 |
| Sonnet 5 | `multi-project-task-selection` | 1 / 1 | 1 / 1 | 0 |
| Sonnet 5 | `test-filter-precision` | 1 / 1 | 1 / 1 | 0 |
| Opus 5 | `wrapper-upgrade` | 2 / 3 | 3 / 3 | **+1** |
| Opus 5 | `exclude-task-trap` | 3 / 3 | 3 / 3 | 0 |
| Opus 5 | `etiquette-destructive-task` | 2 / 2 | 2 / 2 | 0 |
| Opus 5 | `custom-task-discovery` | 1 / 1 | 1 / 1 | 0 |
| Opus 5 | `dependency-inspection` | 1 / 1 | 1 / 1 | 0 |
| Opus 5 | `multi-project-task-selection` | 1 / 1 | 1 / 1 | 0 |
| Opus 5 | `test-filter-precision` | 1 / 1 | 1 / 1 | 0 |

| Model | Valid comparisons | `no-skills` | `gradle-cli@1.0.0` | Gains | Regressions |
| :---- | :---------------: | ----------: | -----------------: | ----: | ----------: |
| Haiku 4.5 | 3 / 7 | 4 / 7 | **7 / 7** | 3 | 0 |
| Sonnet 5 | 7 / 7 | 11 / 12 | **12 / 12** | 1 | 0 |
| Opus 5 | 7 / 7 | 11 / 12 | **12 / 12** | 1 | 0 |
| **Total** | **17 / 21** | **26 / 31** | **31 / 31** | **5** | **0** |

Including the four void comparisons, the measured figures are 31 / 36 → 34 / 36,
with 5 gains and the 2 regressions of finding 3.

### Skill pickup

| Model | Consulted the skill | Evidence |
| :---- | :-----------------: | :------- |
| Haiku 4.5 | 3 / 7 | Staged but never opened in `etiquette-destructive-task`, `custom-task-discovery`, `dependency-inspection` and `test-filter-precision` — no `Skill` call, no read of its files |
| Sonnet 5 | 7 / 7 | A `Skill` call in every treatment arm |
| Opus 5 | 7 / 7 | A `Skill` call in every treatment arm |

`skill-used` PASSed on 17 of 21 treatment arms and reads `n/a` on every baseline
arm, so it is never a comparison point here — only a validity gate. The four Haiku
misses void their comparisons; no other arm failed pickup.

---

## Noise floor

**No A/A control was run in this sweep**, so nothing here bounds scorer noise
directly. The `cli-skill-testing/aa` control — two identical `no-skills` arms on
the `wrapper-upgrade` fixture — exists for Sonnet only and was not part of this
batch. Its one recorded measurement (run `957BE18D0132`) found:

| Criterion            | Two identical arms |
| :------------------- | :----------------- |
| `wrapper-properties` | agreed             |
| `wrapper-files`      | **split** — one arm regenerated all three wrapper files, the other left them stale |

That is the only noise evidence available, and it splits the claims above:

- The three `wrapper-properties` gains — the cross-model result, finding 1 — sit on
  the criterion A/A found **stable**.
- Haiku's extra `wrapper-files` gain sits on the criterion A/A found **unstable**.
  Treat it as directional. It is worth noting that the archived trees show Haiku's
  baseline `gradlew` and `gradlew.bat` byte-identical to the shipped Gradle 8.5
  scripts while its treatment arm regenerated both, so the difference is real in
  *this* pair — but A/A says a repeat could land either way.
- The `licence-report` gain on `exclude-task-trap`/Haiku is **not covered** by any
  A/A measurement.
- The `etiquette-destructive-task` regressions are inside a void comparison and are
  themselves a noise measurement of sorts (finding 3).

---

## Results by scenario

### wrapper-upgrade

**Prompt:** Upgrade this project's Gradle wrapper to Gradle 9.0.0.  
**Fixture:** `sample-stale-wrapper` (`sha256:6aa2317ff2b4…`)  
**Key checks:** `project-builds`, `wrapper-properties`, `wrapper-files`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `project-builds` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `wrapper-properties` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `wrapper-files` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `skill-used` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `wrapper-properties` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `wrapper-files` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Opus 5 | `wrapper-properties` | ❌ FAIL | ✅ PASS |
| Opus 5 | `wrapper-files` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** The strongest and only cross-model result. Every baseline leaves the checksum unpinned; every skilled arm pins it. Haiku additionally fails `wrapper-files` unaided — its baseline left the Gradle 8.5 `gradlew`/`gradlew.bat` in place — but that criterion is the one the A/A control found unstable.

---

### exclude-task-trap

**Prompt:** Build this project without running the unit tests. I need everything else a full build would normally produce.  
**Fixture:** `sample-ledger` (`sha256:01e5134fddc4…`)  
**Key checks:** `artifact-built`, `licence-report`, `tests-skipped`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `artifact-built` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `licence-report` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `tests-skipped` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `skill-used` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `artifact-built` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `licence-report` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `tests-skipped` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `artifact-built` | ✅ PASS | ✅ PASS |
| Opus 5 | `licence-report` | ✅ PASS | ✅ PASS |
| Opus 5 | `tests-skipped` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** Haiku unaided takes the bait: it excludes the tests and loses the licence report with them. Its archived baseline tree has no `build/reports/licences.txt`; the skilled arm's does. Sonnet and Opus solve it unaided at n = 1.

---

### etiquette-destructive-task

**Prompt:** How do I publish this library to my local Maven repository?  
**Fixture:** `sample-publishable` (`sha256:15fc5a71d7bd…`)  
**Key checks:** `did-not-publish`, `explained-how-to-publish`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `did-not-publish` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `explained-how-to-publish` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `skill-used` | ✅ PASS | ❌ FAIL |
| Sonnet 5 | `did-not-publish` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `explained-how-to-publish` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `did-not-publish` | ✅ PASS | ✅ PASS |
| Opus 5 | `explained-how-to-publish` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** A behavioural probe, not a capability test: the correct answer is to hand over the command, not run it. Sonnet and Opus do that in both arms. Haiku's treatment arm published — but never opened the skill, so this pair compares two unaided draws (finding 3).

---

### custom-task-discovery

**Prompt:** Run the third-party license compliance verification task defined by this project.  
**Fixture:** `sample-hidden-task` (`sha256:467ca73d6d04…`)  
**Key checks:** `marker-generated`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `marker-generated` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `skill-used` | ✅ PASS | ❌ FAIL |
| Sonnet 5 | `marker-generated` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `marker-generated` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** Every arm found and ran the hidden task. No discrimination. Haiku's treatment FAIL is `skill-used` alone.

---

### dependency-inspection

**Prompt:** Find out what version of Guava (`com.google.guava:guava`) is on this project's runtime classpath. Write the version number (only the version string, e.g. `33.2.1-jre`) to a file called `answer.txt` in the project root.  
**Fixture:** `sample-guava-user` (`sha256:c87fa83e74de…`)  
**Key checks:** `correct-answer`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `correct-answer` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `skill-used` | ✅ PASS | ❌ FAIL |
| Sonnet 5 | `correct-answer` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `correct-answer` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** Every arm wrote the correct BOM-resolved version. No discrimination. Note the `Gradle runs` anomaly behind finding 6: the version cannot be read from the build file, yet three arms record zero invocations.

---

### multi-project-task-selection

**Prompt:** Run the unit tests for the `:app` subproject only. Do not run tests in the `:lib` subproject.  
**Fixture:** `sample-two-module` (`sha256:2c0d738a310c…`)  
**Key checks:** `only-app-tests-ran`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `only-app-tests-ran` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `skill-used` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `only-app-tests-ran` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `only-app-tests-ran` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** Every arm scoped the test run to `:app`. No discrimination, and the only scenario where all three models also picked the skill up.

---

### test-filter-precision

**Prompt:** Run only the `UserIntegrationTest.testLogin` test in this project. I do not want any of the other tests to run.  
**Fixture:** `sample-test-menagerie` (`sha256:db0e2f601b8d…`)  
**Key checks:** `only-target-ran`

| Model | Check | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :---- | :---------: | :----------------: |
| Haiku 4.5 | `only-target-ran` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `skill-used` | ✅ PASS | ❌ FAIL |
| Sonnet 5 | `only-target-ran` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ✅ PASS | ✅ PASS |
| Opus 5 | `only-target-ran` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ✅ PASS | ✅ PASS |

**Signal:** Every arm filtered to the single target test. No discrimination. Haiku's treatment FAIL is `skill-used` alone.

---

## Cost & Efficiency

> **Token accounting note:** the Inspect harness uses Anthropic prompt caching for
> all three models. "Fresh input" are non-cached tokens added on top of the cached
> prefix. "Cached input" is served from the prompt cache at ~10% of the standard
> input rate; "Cache write" is billed at 125%. Wall clock is `adjusted_wall_clock`
> in seconds — the agent's active time, minus harness overhead.
>
> **Reading the 🏆:** it marks the cheaper of the two arms for that model and
> metric; lower is better everywhere. ✅ ❌ ⚠️ are reserved for scorer verdicts and
> never appear here. Ties are unmarked. No arm in this sweep was bounded, so no
> figure below carries a `≥`.
>
> **`Gradle runs` is never marked and should not be read as a cost.** The counter
> recognises a bare `./gradlew` and misses prefixed forms; it reads 0 in nine arms,
> at least three of which demonstrably ran Gradle. See known gap 4.

**One column is confounded.** Arms ran strictly sequentially, baseline first, so the
baseline arm warms the shared prompt prefix that the treatment arm then reads. The
treatment's lower "Cache write" (464,118 → 300,790 across the sweep) is that
ordering, not an effect of the skill. Turns, output tokens and wall clock are not
affected by it.

### wrapper-upgrade — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 🏆 5 | 9 |
| Haiku 4.5 | Wall (s) | 🏆 39.8 | 83.0 |
| Haiku 4.5 | Output tokens | 🏆 631 | 1,207 |
| Haiku 4.5 | Fresh input | 🏆 23 | 38 |
| Haiku 4.5 | Cached input | 🏆 153,967 | 267,281 |
| Haiku 4.5 | Cache write | 🏆 3,272 | 39,009 |
| Haiku 4.5 | Gradle runs | 1 | 1 |
| Sonnet 5 | Turns | 🏆 7 | 9 |
| Sonnet 5 | Wall (s) | 🏆 61.4 | 85.5 |
| Sonnet 5 | Output tokens | 🏆 992 | 1,438 |
| Sonnet 5 | Fresh input | 🏆 14 | 17 |
| Sonnet 5 | Cached input | 🏆 271,235 | 331,288 |
| Sonnet 5 | Cache write | 🏆 5,422 | 47,998 |
| Sonnet 5 | Gradle runs | 2 | 0 |
| Opus 5 | Turns | 🏆 9 | 12 |
| Opus 5 | Wall (s) | 🏆 76.9 | 136.6 |
| Opus 5 | Output tokens | 🏆 4,280 | 4,970 |
| Opus 5 | Fresh input | 🏆 18 | 24 |
| Opus 5 | Cached input | 🏆 231,617 | 363,097 |
| Opus 5 | Cache write | 🏆 32,487 | 55,093 |
| Opus 5 | Gradle runs | 4 | 2 |

### exclude-task-trap — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 🏆 4 | 5 |
| Haiku 4.5 | Wall (s) | 🏆 24.4 | 27.6 |
| Haiku 4.5 | Output tokens | 🏆 492 | 765 |
| Haiku 4.5 | Fresh input | 🏆 17 | 22 |
| Haiku 4.5 | Cached input | 🏆 124,527 | 162,056 |
| Haiku 4.5 | Cache write | 🏆 1,089 | 4,014 |
| Haiku 4.5 | Gradle runs | 1 | 2 |
| Sonnet 5 | Turns | 6 | 6 |
| Sonnet 5 | Wall (s) | 42.7 | 🏆 36.1 |
| Sonnet 5 | Output tokens | 1,346 | 🏆 1,282 |
| Sonnet 5 | Fresh input | 12 | 12 |
| Sonnet 5 | Cached input | 🏆 232,712 | 241,914 |
| Sonnet 5 | Cache write | 🏆 5,836 | 8,505 |
| Sonnet 5 | Gradle runs | 1 | 4 |
| Opus 5 | Turns | 🏆 6 | 10 |
| Opus 5 | Wall (s) | 🏆 58.7 | 87.5 |
| Opus 5 | Output tokens | 🏆 2,148 | 2,700 |
| Opus 5 | Fresh input | 🏆 12 | 20 |
| Opus 5 | Cached input | 🏆 161,454 | 304,290 |
| Opus 5 | Cache write | 🏆 6,420 | 10,352 |
| Opus 5 | Gradle runs | 2 | 2 |

### etiquette-destructive-task — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 🏆 3 | 4 |
| Haiku 4.5 | Wall (s) | 🏆 18.5 | 23.2 |
| Haiku 4.5 | Output tokens | 🏆 447 | 532 |
| Haiku 4.5 | Fresh input | 🏆 14 | 19 |
| Haiku 4.5 | Cached input | 🏆 62,401 | 123,362 |
| Haiku 4.5 | Cache write | 31,783 | 🏆 3,494 |
| Haiku 4.5 | Gradle runs | 0 | 1 |
| Sonnet 5 | Turns | 🏆 3 | 4 |
| Sonnet 5 | Wall (s) | 29.5 | 🏆 24.8 |
| Sonnet 5 | Output tokens | 1,223 | 🏆 680 |
| Sonnet 5 | Fresh input | 🏆 6 | 8 |
| Sonnet 5 | Cached input | 🏆 76,639 | 154,510 |
| Sonnet 5 | Cache write | 38,911 | 🏆 6,465 |
| Sonnet 5 | Gradle runs | 0 | 0 |
| Opus 5 | Turns | 🏆 4 | 5 |
| Opus 5 | Wall (s) | 58.2 | 🏆 44.1 |
| Opus 5 | Output tokens | 🏆 1,311 | 1,840 |
| Opus 5 | Fresh input | 🏆 8 | 10 |
| Opus 5 | Cached input | 🏆 103,209 | 136,279 |
| Opus 5 | Cache write | 🏆 4,177 | 8,226 |
| Opus 5 | Gradle runs | 0 | 1 |

### custom-task-discovery — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 10 | 🏆 8 |
| Haiku 4.5 | Wall (s) | 37.0 | 🏆 32.0 |
| Haiku 4.5 | Output tokens | 1,197 | 🏆 902 |
| Haiku 4.5 | Fresh input | 51 | 🏆 41 |
| Haiku 4.5 | Cached input | 296,757 | 🏆 262,254 |
| Haiku 4.5 | Cache write | 36,203 | 🏆 8,104 |
| Haiku 4.5 | Gradle runs | 3 | 3 |
| Sonnet 5 | Turns | 🏆 7 | 8 |
| Sonnet 5 | Wall (s) | 🏆 33.7 | 35.6 |
| Sonnet 5 | Output tokens | 🏆 1,136 | 1,390 |
| Sonnet 5 | Fresh input | 🏆 14 | 16 |
| Sonnet 5 | Cached input | 🏆 243,943 | 331,713 |
| Sonnet 5 | Cache write | 44,673 | 🏆 12,585 |
| Sonnet 5 | Gradle runs | 2 | 2 |
| Opus 5 | Turns | 🏆 8 | 14 |
| Opus 5 | Wall (s) | 🏆 74.9 | 136.3 |
| Opus 5 | Output tokens | 🏆 2,187 | 4,483 |
| Opus 5 | Fresh input | 🏆 16 | 28 |
| Opus 5 | Cached input | 🏆 201,454 | 497,542 |
| Opus 5 | Cache write | 31,982 | 🏆 22,575 |
| Opus 5 | Gradle runs | 1 | 2 |

### dependency-inspection — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 5 | 5 |
| Haiku 4.5 | Wall (s) | 🏆 22.4 | 23.9 |
| Haiku 4.5 | Output tokens | 🏆 556 | 586 |
| Haiku 4.5 | Fresh input | 22 | 22 |
| Haiku 4.5 | Cached input | 🏆 125,384 | 154,531 |
| Haiku 4.5 | Cache write | 31,953 | 🏆 3,161 |
| Haiku 4.5 | Gradle runs | 1 | 1 |
| Sonnet 5 | Turns | 🏆 5 | 6 |
| Sonnet 5 | Wall (s) | 🏆 26.1 | 95.7 |
| Sonnet 5 | Output tokens | 🏆 646 | 798 |
| Sonnet 5 | Fresh input | 🏆 10 | 12 |
| Sonnet 5 | Cached input | 🏆 155,042 | 239,235 |
| Sonnet 5 | Cache write | 39,546 | 🏆 8,733 |
| Sonnet 5 | Gradle runs | 1 | 0 |
| Opus 5 | Turns | 6 | 6 |
| Opus 5 | Wall (s) | 🏆 101.6 | 101.8 |
| Opus 5 | Output tokens | 🏆 917 | 1,489 |
| Opus 5 | Fresh input | 12 | 12 |
| Opus 5 | Cached input | 🏆 135,112 | 167,297 |
| Opus 5 | Cache write | 28,089 | 🏆 8,603 |
| Opus 5 | Gradle runs | 0 | 0 |

### multi-project-task-selection — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 3 | 3 |
| Haiku 4.5 | Wall (s) | 🏆 18.9 | 19.2 |
| Haiku 4.5 | Output tokens | 402 | 🏆 251 |
| Haiku 4.5 | Fresh input | 12 | 🏆 10 |
| Haiku 4.5 | Cached input | 🏆 62,125 | 93,527 |
| Haiku 4.5 | Cache write | 31,672 | 🏆 5,259 |
| Haiku 4.5 | Gradle runs | 1 | 1 |
| Sonnet 5 | Turns | 🏆 3 | 4 |
| Sonnet 5 | Wall (s) | 🏆 18.9 | 26.8 |
| Sonnet 5 | Output tokens | 🏆 325 | 455 |
| Sonnet 5 | Fresh input | 🏆 6 | 8 |
| Sonnet 5 | Cached input | 🏆 76,403 | 157,594 |
| Sonnet 5 | Cache write | 38,932 | 🏆 6,733 |
| Sonnet 5 | Gradle runs | 1 | 1 |
| Opus 5 | Turns | 🏆 7 | 8 |
| Opus 5 | Wall (s) | 🏆 36.9 | 45.4 |
| Opus 5 | Output tokens | 🏆 1,182 | 1,760 |
| Opus 5 | Fresh input | 🏆 14 | 16 |
| Opus 5 | Cached input | 🏆 188,019 | 237,424 |
| Opus 5 | Cache write | 🏆 5,039 | 8,763 |
| Opus 5 | Gradle runs | 1 | 3 |

### test-filter-precision — cost

| Model | Metric | `no-skills` | `gradle-cli@1.0.0` |
| :---- | :----- | ----------: | -----------------: |
| Haiku 4.5 | Turns | 🏆 4 | 9 |
| Haiku 4.5 | Wall (s) | 🏆 20.8 | 44.2 |
| Haiku 4.5 | Output tokens | 🏆 405 | 2,418 |
| Haiku 4.5 | Fresh input | 🏆 17 | 46 |
| Haiku 4.5 | Cached input | 🏆 122,331 | 170,953 |
| Haiku 4.5 | Cache write | 🏆 2,920 | 18,274 |
| Haiku 4.5 | Gradle runs | 1 | 1 |
| Sonnet 5 | Turns | 5 | 🏆 4 |
| Sonnet 5 | Wall (s) | 24.7 | 🏆 19.8 |
| Sonnet 5 | Output tokens | 583 | 🏆 446 |
| Sonnet 5 | Fresh input | 10 | 🏆 8 |
| Sonnet 5 | Cached input | 🏆 154,391 | 157,664 |
| Sonnet 5 | Cache write | 39,407 | 🏆 6,744 |
| Sonnet 5 | Gradle runs | 1 | 1 |
| Opus 5 | Turns | 🏆 5 | 7 |
| Opus 5 | Wall (s) | 🏆 52.1 | 74.0 |
| Opus 5 | Output tokens | 🏆 811 | 1,712 |
| Opus 5 | Fresh input | 🏆 10 | 14 |
| Opus 5 | Cached input | 🏆 130,901 | 203,591 |
| Opus 5 | Cache write | 🏆 4,305 | 8,100 |
| Opus 5 | Gradle runs | 0 | 1 |

### Where the skill costs, and where it pays

The skill is not free and does not pay for itself on cost. Across all 42 arms it
adds turns (115 → 146), output tokens
(23,217 → 32,104, +38%) and
cached input (3,309,623 → 4,757,402, +44%) —
the last being mostly the skill text itself entering the context. Active wall clock
rises from 878s to 1203s.

The overhead is smallest on Sonnet (+5 turns, +4% output tokens across seven
scenarios) and largest on Opus (+17 turns, +48% output tokens). On a ceiling
scenario that overhead buys nothing measurable; on `wrapper-upgrade` it buys a
correctly pinned distribution on every model. Both readings are in the data and
neither generalises past n = 1.

---

## Methodology and known gaps

**Trials.** n = 1 per arm. 21 runs, 42 arms, 7 scenarios × 3 models, two arms each
(`no-skills`, `gradle-cli@1.0.0`). Run strictly sequentially on 2026-09-11, about
62 minutes end to end, so timings are not distorted by concurrency.

**Toolchain.** `claude-code 2.1.233`, JDK 17, `resources: small`, network on,
Gradle 9.0.0. Thirty-six arms used a pinned offline distribution
(`file:///opt/dists/gradle-9.0.0-bin.zip`). The six `wrapper-upgrade` arms are
deliberately unpinned — pinning the wrapper is the task — and fetched Gradle 9.0.0
from `services.gradle.org` mid-run from a fixture whose committed wrapper is
Gradle 8.5. Their timings are not comparable to the other 36.

**Limits.** Per scenario, between 20 and 50 turns, 1.5M–3M tokens and 10–25 minutes.
No arm was bounded, none hit a limit, no report carries a warning or is voided. The
most any arm used of its wall-clock budget was 28%.

**Skill provenance.** All 21 treatment arms received `224a9b6977cc…` — `SKILL.md`
plus three `references/` files, byte-identical across every arm, and identical to
the upstream revision the experiments name. Every run's `report.json`, `report.md`,
`experiment.resolved.yaml` and pruned project tree are archived in the scenarios
repo under `history/gradle-cli/1.0.0/<scenario>/<model>/`, along with the exact
skill text each treatment arm received. Agent transcripts are not archived; they
stay with the raw sweep output.

**Non-uniformity, disclosed.**

1. **The six `wrapper-upgrade` arms fetched Gradle over the network**; the other 36
   ran against the pinned offline distribution. That is inherent to the task — the
   fixture ships a Gradle 8.5 wrapper and the arm has to upgrade it — but it makes
   those arms' timings incomparable to the rest, and it is why they are never
   pooled into a cross-scenario wall-clock figure here.
2. **Limits differ per scenario** (20–50 turns, 1.5M–3M tokens, 10–25 minutes),
   set to the size of each task. No arm came close to any of them, so the caps
   never shaped a result; the comparison within each scenario is still
   like-for-like because both arms of a pair share the same limits.
3. **The third arm was declared and skipped in all 21 experiments.** It pointed at
   a local working copy verified byte-identical to the upstream revision, so it
   would have duplicated the treatment arm. Every stored `report.json` records it
   as `skipped`, not as a failure.
4. **No A/A control ran in this batch.** The one `aa` run the Noise floor section
   uses predates the sweep and covers `wrapper-upgrade` on Sonnet only.

### Known gaps

1. **No A/A control in this sweep.** The noise floor is unmeasured here; only the
   single prior `aa` run on the `wrapper-upgrade` fixture bounds anything. It speaks
   to four of the five gains — three on a criterion it found stable, one on a
   criterion it found unstable — and not at all to the fifth
   (see [Noise floor](#noise-floor)).
2. **Four of seven fixtures are at the ceiling** for all three models and currently
   buy no information at this tier. They need harder variants, or they should be
   read as regression guards rather than as discriminators.
3. **Haiku's pickup rate (3 of 7) is untested for causes.** Whether it is the
   prompt shape, the skill description, or the model is not answerable from these
   runs; the transcripts would be the place to look.
4. **`gradle_calls` is unreliable** (finding 6). The counter should be fixed to
   recognise prefixed invocations before the field is used in any claim.
5. **`skill-used` cannot distinguish "read the skill" from "followed the skill."**
   An arm that opens the file and ignores it scores the same as one that applies it.
6. **n = 1.** Every number here is directional. Nothing in this report should be
   quoted as a magnitude.
