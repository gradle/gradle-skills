# Gradle CLI Skill — Benchmark Results

## Summary

`gradle-cli@1.3.0` produces the same outcomes as `1.2.0` across Opus 5 and Deepseek V4 Flash. On Sonnet 5, `1.3.0` picks up the skill automatically in 2 scenarios where `1.2.0` did not.

The strongest signal in this evaluation is **wrapper-upgrade**: every capable model fails to pin the SHA-256 checksum without the skill, and both skill versions fix it reliably.
This is the scenario where the skill provides the clearest, most consistent value.

---

## Setup

### What we're measuring

Each scenario runs three arms against the same Gradle project and prompt:

| Arm                | Skill                                                       |
| :--                | :--                                                         |
| `no-skills`        | Baseline — no skill provided                                |
| `gradle-cli@1.2.0` | `gradle-skills@main` — canonical skill from the public repo |
| `gradle-cli@1.3.0` | Local `skills/gradle-cli` — branch under development        |

### Models tested

| Model                        | CLI              | Notes                          |
| :--                          | :--              | :--                            |
| `anthropic/claude-sonnet-5`  | `claude-code`    |                                |
| `anthropic/claude-opus-5`    | `claude-code`    |                                |
| `deepseek/deepseek-v4-flash` | `opencode 0.4.2` | Referred to as "V4 Flash 0731" |
| `openai/gpt-5.6-luna`        | `opencode 0.4.2` | Reasoning model; see findings  |

### Scorers

Every scenario includes a `skill-used` scorer that verifies the skill was actually invoked (Skill tool call or file read in transcript). Task-specific scorers measure correctness of the outcome.

### Outcome definitions

| Outcome        | Meaning                                                                                                                                                                                   |
| :--            | :--                                                                                                                                                                                       |
| ✅ **PASS**    | The scorer's criterion was met — the agent produced the correct result.                                                                                                                   |
| ❌ **FAIL**    | The trial ran but the criterion was not met — wrong output, missing file, wrong behaviour.                                                                                                |
| ⚠️ **INVALID** | The scorer could not render a verdict. The trial ran, but a prerequisite for evaluation was absent (e.g. no test results directory because Gradle never ran, no build output to inspect). |

---

## Key findings

### 1. Wrapper upgrade is the clearest discriminator for capable models
The only scenario where Sonnet 5, Opus 5, and Deepseek all fail without the skill. The SHA-256 checksum pinning and double `./gradlew wrapper` invocation are habits the skill supplies that no model produces unprompted.

### 2. Opus 5 mostly needs no help
Passes 6 of 7 scenarios unaided (wrapper-upgrade being the exception). The skill is picked up and used correctly on all scenarios, but doesn't change outcomes except on wrapper-upgrade.

### 3. Sonnet 5 has upstream skill pickup gaps
The upstream skill (`gradle-cli@1.2.0`) fails to be invoked by Sonnet 5 on 3 scenarios: `custom-task-discovery`, `etiquette-destructive-task`, and `exclude-task-trap`. The local skill (`gradle-cli@1.3.0`) is picked up on 2 of those 3. This suggests the upstream skill's description is less effective at triggering automatic invocation on Sonnet 5 than on stronger models.

### 4. Deepseek V4 Flash picks up both skills reliably
skill-used PASS on every non-INVALID scenario for both upstream and local. The skill makes a material difference on `wrapper-upgrade` (SHA-256) and `exclude-task-trap` (licence report). Strong pickup behaviour comparable to Opus 5.

### 5. GPT-5.6 Luna via opencode does not execute Gradle commands
Every GPT-5.6 Luna arm completed in exactly 2 turns with 0 Gradle invocations and ~100–230 output tokens — it responds with text only and does not use tools to run commands. Skills are detected (skill-used PASS), but the model does not act on the skill's instructions. This is likely a tool-calling compatibility issue between GPT-5.6 Luna (a reasoning model) and opencode 0.4.2, not a model reasoning failure.

### 6. opencode container INVALID on etiquette scenario
Both Deepseek and GPT-5.6 Luna return INVALID on `etiquette-destructive-task`. Since this affects both opencode models but not the claude-code models, the root cause is the opencode container environment or scorer compatibility, not model behaviour.

### 7. n = 1 per arm — results are directional only
All runs are single trials. These results indicate direction, not magnitude. Repeated runs are needed to separate signal from noise.

---

## Summary table

### Outcome (no-skills / gradle-cli@1.2.0 / gradle-cli@1.3.0)

| Scenario                     | Model             | `no-skills` | `gradle-cli@1.2.0` | `gradle-cli@1.3.0` |
| :--                          | :--               | :--:        | :--:               | :--:               |
| wrapper-upgrade              | Sonnet 5          | ❌ FAIL     | ✅ PASS            | ✅ PASS            |
| wrapper-upgrade              | Opus 5            | ❌ FAIL     | ✅ PASS            | ✅ PASS            |
| wrapper-upgrade              | Deepseek V4 Flash | ❌ FAIL     | ✅ PASS            | ✅ PASS            |
| wrapper-upgrade              | GPT-5.6 Luna      | ❌ FAIL     | ❌ FAIL            | ❌ FAIL            |
| dependency-inspection        | Sonnet 5          | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | Opus 5            | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | Deepseek V4 Flash | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | GPT-5.6 Luna      | ❌ FAIL     | ❌ FAIL            | ❌ FAIL            |
| test-filter-precision        | Sonnet 5          | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| test-filter-precision        | Opus 5            | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| test-filter-precision        | GPT-5.6 Luna      | ⚠️ INVALID  | ⚠️ INVALID         | ⚠️ INVALID         |
| test-filter-precision        | Deepseek V4 Flash | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | Sonnet 5          | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | Opus 5            | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | Deepseek V4 Flash | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | GPT-5.6 Luna      | ✅ PASS†    | ✅ PASS†           | ✅ PASS†           |
| custom-task-discovery        | Sonnet 5          | ✅ PASS     | ❌ **FAIL**        | ❌ **FAIL**        |
| custom-task-discovery        | Opus 5            | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| custom-task-discovery        | Deepseek V4 Flash | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| custom-task-discovery        | GPT-5.6 Luna      | ⚠️ INVALID  | ⚠️ INVALID         | ⚠️ INVALID         |
| etiquette-destructive-task   | Sonnet 5          | ❌ FAIL     | ❌ **FAIL**        | ✅ PASS            |
| etiquette-destructive-task   | Opus 5            | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| etiquette-destructive-task   | Deepseek V4 Flash | ⚠️ INVALID  | ⚠️ INVALID         | ⚠️ INVALID         |
| etiquette-destructive-task   | GPT-5.6 Luna      | ⚠️ INVALID  | ⚠️ INVALID         | ⚠️ INVALID         |
| exclude-task-trap            | Sonnet 5          | ✅ PASS     | ❌ **FAIL**        | ✅ PASS            |
| exclude-task-trap            | Opus 5            | ✅ PASS     | ✅ PASS            | ✅ PASS            |
| exclude-task-trap            | Deepseek V4 Flash | ❌ FAIL     | ✅ PASS            | ✅ PASS            |
| exclude-task-trap            | GPT-5.6 Luna      | ⚠️ INVALID  | ⚠️ INVALID         | ⚠️ INVALID         |

† Suspected false positive — PASS with 0 Gradle invocations. Requires investigation.

### skill-used (gradle-cli@1.2.0 / gradle-cli@1.3.0)

| Scenario                     | Model             | `gradle-cli@1.2.0` | `gradle-cli@1.3.0` |
| :--                          | :--               | :--:               | :--:               |
| wrapper-upgrade              | Sonnet 5          | ✅ PASS            | ✅ PASS            |
| wrapper-upgrade              | Opus 5            | ✅ PASS            | ✅ PASS            |
| wrapper-upgrade              | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | Sonnet 5          | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | Opus 5            | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| test-filter-precision        | Sonnet 5          | ✅ PASS            | ✅ PASS            |
| test-filter-precision        | Opus 5            | ✅ PASS            | ✅ PASS            |
| test-filter-precision        | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | Sonnet 5          | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | Opus 5            | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| custom-task-discovery        | Sonnet 5          | ❌ **FAIL**        | ❌ **FAIL**        |
| custom-task-discovery        | Opus 5            | ✅ PASS            | ✅ PASS            |
| custom-task-discovery        | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| etiquette-destructive-task   | Sonnet 5          | ❌ **FAIL**        | ✅ PASS            |
| etiquette-destructive-task   | Opus 5            | ✅ PASS            | ✅ PASS            |
| etiquette-destructive-task   | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| exclude-task-trap            | Sonnet 5          | ❌ **FAIL**        | ✅ PASS            |
| exclude-task-trap            | Opus 5            | ✅ PASS            | ✅ PASS            |
| exclude-task-trap            | Deepseek V4 Flash | ✅ PASS            | ✅ PASS            |
| wrapper-upgrade              | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |
| dependency-inspection        | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |
| test-filter-precision        | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |
| multi-project-task-selection | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |
| custom-task-discovery        | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |
| etiquette-destructive-task   | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |
| exclude-task-trap            | GPT-5.6 Luna      | ✅ PASS            | ✅ PASS            |

---

---

## Results by scenario

### wrapper-upgrade

**Prompt:** Upgrade this project's Gradle wrapper to Gradle 9.0.0.
**Key check:** SHA-256 pinned in `gradle-wrapper.properties`, wrapper task run twice so binaries regenerate.

| Model             | Arm                | wrapper-properties | wrapper-files | skill-used | outcome     |
| :--               | :--                | :--:               | :--:          | :--:       | :--:        |
| Sonnet 5          | `no-skills`        | ❌ FAIL            | ❌ FAIL       | ✅ PASS    | ❌ **FAIL** |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS       | ✅ PASS    | ✅ PASS     |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS       | ✅ PASS    | ✅ PASS     |
| Opus 5            | `no-skills`        | ❌ FAIL            | ✅ PASS       | ✅ PASS    | ❌ **FAIL** |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS       | ✅ PASS    | ✅ PASS     |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS       | ✅ PASS    | ✅ PASS     |
| Deepseek V4 Flash | `no-skills`        | ❌ FAIL            | ❌ FAIL       | ✅ PASS    | ❌ **FAIL** |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS       | ✅ PASS    | ✅ PASS     |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS       | ✅ PASS    | ✅ PASS     |
| GPT-5.6 Luna      | `no-skills`        | ❌ FAIL            | ❌ FAIL       | ✅ PASS    | ❌ **FAIL** |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ❌ FAIL            | ❌ FAIL       | ✅ PASS    | ❌ **FAIL** |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ❌ FAIL            | ❌ FAIL       | ✅ PASS    | ❌ **FAIL** |

**Signal:** The strongest discriminator for Anthropic/Deepseek models. GPT-5.6 Luna fails all arms with 0 Gradle invocations — it responds in prose without executing commands (see findings).

---

### dependency-inspection

**Prompt:** Find the resolved version of `com.google.guava:guava` on the runtime classpath; write it to `answer.txt`.
**Key check:** Agent must run `./gradlew dependencies` (not guess from `build.gradle.kts`, which has no version literal).

| Model             | Arm                | correct-answer | skill-used | outcome     |
| :--               | :--                | :--:           | :--:       | :--:        |
| Sonnet 5          | `no-skills`        | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Opus 5            | `no-skills`        | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Deepseek V4 Flash | `no-skills`        | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ✅ PASS        | ✅ PASS    | ✅ PASS     |
| GPT-5.6 Luna      | `no-skills`        | ❌ FAIL        | ✅ PASS    | ❌ **FAIL** |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ❌ FAIL        | ✅ PASS    | ❌ **FAIL** |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ❌ FAIL        | ✅ PASS    | ❌ **FAIL** |

**Signal:** All Anthropic/Deepseek models solve this unaided. GPT-5.6 Luna fails — 0 Gradle invocations, no `./gradlew dependencies` run.

---

### test-filter-precision

**Prompt:** Run only `UserIntegrationTest.testLogin` — no other tests.
**Key check:** Exactly one test method ran (`--tests="com.example.menagerie.UserIntegrationTest.testLogin"`).

| Model             | Arm                | only-target-ran | skill-used | outcome        |
| :--               | :--                | :--:            | :--:       | :--:           |
| Sonnet 5          | `no-skills`        | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Opus 5            | `no-skills`        | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Deepseek V4 Flash | `no-skills`        | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ✅ PASS         | ✅ PASS    | ✅ PASS        |
| GPT-5.6 Luna      | `no-skills`        | ⚠️ INVALID      | ✅ PASS    | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ⚠️ INVALID      | ✅ PASS    | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ⚠️ INVALID      | ✅ PASS    | ⚠️ **INVALID** |

**Signal:** All Anthropic/Deepseek models solve this correctly. GPT-5.6 Luna returns INVALID — scorer could not evaluate because no tests ran (0 Gradle invocations).

---

### multi-project-task-selection

**Prompt:** Run unit tests for `:app` subproject only — not `:lib`.
**Key check:** Only `:app:test` ran, not `test` (which hits all subprojects).

| Model             | Arm                | only-app-tests-ran | skill-used | outcome |
| :--               | :--                | :--:               | :--:       | :--:    |
| Sonnet 5          | `no-skills`        | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Opus 5            | `no-skills`        | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Deepseek V4 Flash | `no-skills`        | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| GPT-5.6 Luna      | `no-skills`        | ✅ PASS            | ✅ PASS    | ✅ PASS |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ✅ PASS            | ✅ PASS    | ✅ PASS |

**Signal:** All models pass, including GPT-5.6 Luna — but GPT scored PASS with 0 Gradle invocations. Suspected false positive: scorer may have matched pre-existing fixture state rather than a live Gradle run. Requires investigation.

---

### custom-task-discovery

**Prompt:** Run the third-party license compliance verification task defined by this project.
**Key check:** Agent finds and runs `verifyThirdPartyCompliance` (hidden in `buildSrc/`, among decoy tasks with similar names).

| Model             | Arm                | marker-generated | skill-used  | outcome        |
| :--               | :--                | :--:             | :--:        | :--:           |
| Sonnet 5          | `no-skills`        | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS          | ❌ **FAIL** | ❌ **FAIL**    |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS          | ❌ **FAIL** | ❌ **FAIL**    |
| Opus 5            | `no-skills`        | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| Deepseek V4 Flash | `no-skills`        | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ✅ PASS          | ✅ PASS     | ✅ PASS        |
| GPT-5.6 Luna      | `no-skills`        | ⚠️ **INVALID**   | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ⚠️ **INVALID**   | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ⚠️ **INVALID**   | ✅ PASS     | ⚠️ **INVALID** |

**Signal:** Sonnet 5 does not invoke either skill for this prompt — pickup failure, not outcome failure (the task still gets found and run). Opus 5 and Deepseek pick up both skills correctly.

---

### etiquette-destructive-task

**Prompt:** How do I publish this library to my local Maven repository?
**Key check:** Agent answers in prose without running `publish` (a "how do I" question should not trigger execution).

| Model             | Arm                | did-not-publish | explained-how-to-publish | skill-used  | outcome        |
| :--               | :--                | :--:            | :--:                     | :--:        | :--:           |
| Sonnet 5          | `no-skills`        | ❌ FAIL         | ✅ PASS                  | ✅ PASS     | ❌ **FAIL**    |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS         | ✅ PASS                  | ❌ **FAIL** | ❌ **FAIL**    |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS         | ✅ PASS                  | ✅ PASS     | ✅ PASS        |
| Opus 5            | `no-skills`        | ✅ PASS         | ✅ PASS                  | ✅ PASS     | ✅ PASS        |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS         | ✅ PASS                  | ✅ PASS     | ✅ PASS        |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS         | ✅ PASS                  | ✅ PASS     | ✅ PASS        |
| Deepseek V4 Flash | `no-skills`        | ⚠️ **INVALID**  | ⚠️ **INVALID**           | ✅ PASS     | ⚠️ **INVALID** |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ⚠️ **INVALID**  | ⚠️ **INVALID**           | ✅ PASS     | ⚠️ **INVALID** |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ⚠️ **INVALID**  | ⚠️ **INVALID**           | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `no-skills`        | ⚠️ **INVALID**  | ⚠️ **INVALID**           | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ⚠️ **INVALID**  | ⚠️ **INVALID**           | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ⚠️ **INVALID**  | ⚠️ **INVALID**           | ✅ PASS     | ⚠️ **INVALID** |

**Notes:**
- **Sonnet 5 no-skills:** ran the publish task (did-not-publish FAIL). Skill fixes this.
- **Sonnet 5 upstream:** skill not picked up (skill-used FAIL), but did not publish anyway — outcome FAIL because the constraint was not proven to be skill-driven.
- **Opus 5:** all three arms pass — model exercises correct etiquette without guidance.
- **Deepseek and GPT-5.6 Luna:** all arms INVALID — scorer/environment compatibility issue with opencode containers. Requires investigation.

---

### exclude-task-trap

**Prompt:** Build this project without running the unit tests. Produce everything else a full build would normally produce.
**Key check:** `assemble` or equivalent succeeds AND `generateLicenceReport` runs (it hangs off `test`, so `-x test` alone silently drops it).

| Model             | Arm                | artifact-built | licence-report | tests-skipped  | skill-used  | outcome        |
| :--               | :--                | :--:           | :--:           | :--:           | :--:        | :--:           |
| Sonnet 5          | `no-skills`        | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| Sonnet 5          | `gradle-cli@1.2.0` | ✅ PASS        | ✅ PASS        | ✅ PASS        | ❌ **FAIL** | ❌ **FAIL**    |
| Sonnet 5          | `gradle-cli@1.3.0` | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| Opus 5            | `no-skills`        | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| Opus 5            | `gradle-cli@1.2.0` | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| Opus 5            | `gradle-cli@1.3.0` | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| Deepseek V4 Flash | `no-skills`        | ✅ PASS        | ❌ **FAIL**    | ✅ PASS        | ✅ PASS     | ❌ **FAIL**    |
| Deepseek V4 Flash | `gradle-cli@1.2.0` | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| Deepseek V4 Flash | `gradle-cli@1.3.0` | ✅ PASS        | ✅ PASS        | ✅ PASS        | ✅ PASS     | ✅ PASS        |
| GPT-5.6 Luna      | `no-skills`        | ❌ FAIL        | ❌ FAIL        | ⚠️ **INVALID** | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.2.0` | ❌ FAIL        | ❌ FAIL        | ⚠️ **INVALID** | ✅ PASS     | ⚠️ **INVALID** |
| GPT-5.6 Luna      | `gradle-cli@1.3.0` | ❌ FAIL        | ❌ FAIL        | ⚠️ **INVALID** | ✅ PASS     | ⚠️ **INVALID** |

**Notes:**
- **Sonnet 5 upstream:** skill not invoked, outcome FAIL by scorer logic (skill-used required).
- **Deepseek no-skills:** drops the licence report — classic `-x test` trap. Both skills fix it cleanly.
- **Opus 5:** solves the trap unaided at n=1.
- **GPT-5.6 Luna:** INVALID across all arms, artifact and licence report both fail (0 Gradle invocations).

---

## Cost & Efficiency

> **Token accounting note:** For Anthropic models (`claude-code`), the Inspect harness uses prompt caching. "Tokens in (fresh)" are non-cached tokens added on top of the cached prefix — typically just a few per turn. "Tokens in (cached)" are served from the prompt cache at ~10% of the standard input token rate. "Tokens in (cache write)" are written to the cache for the first time and billed at 125% of the standard input rate.  
> For Deepseek (`opencode`), there is no Anthropic-style prompt caching. "Tokens in (fresh)" represents genuinely new input tokens per turn. "Tokens in (cached)" reflects opencode's internal context reuse (not billable at a reduced rate). "Tokens in (cache write)" is always 0.
> Wall clock is `adjusted_wall_clock` in seconds — the agent's active time, minus harness overhead.
> A wall clock of `663.4s` for Sonnet 5 `gradle-cli@1.2.0` on `exclude-task-trap` is a known anomaly (5 Gradle invocations, likely a retry loop). Treat with caution.
> The `-876.8s` for Opus 5 `gradle-cli@1.3.0` on `custom-task-discovery` is a harness calculation artefact — the real run time was ~17 minutes.

### wrapper-upgrade — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 8     | 40.2     | 1,656         | 16          | 276,354      | 41,402      | 3           |
| Sonnet 5          | gradle-cli@1.2.0 | 7     | 81.3     | 1,314         | 14          | 297,453      | 11,207      | 1           |
| Sonnet 5          | gradle-cli@1.3.0 | 9     | 94.6     | 1,794         | 17          | 333,322      | 48,416      | 1           |
| Opus 5            | no-skills        | 10    | 85.2     | 2,917         | 20          | 278,170      | 7,064       | 3           |
| Opus 5            | gradle-cli@1.2.0 | 11    | 104.1    | 2,754         | 22          | 341,248      | 12,561      | 1           |
| Opus 5            | gradle-cli@1.3.0 | 8     | 90.2     | 2,384         | 16          | 252,852      | 12,433      | 0           |
| Deepseek V4 Flash | no-skills        | 8     | 31.6     | 863           | 1,872       | 56,064       | 0           | 4           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 10    | 60.1     | 1,815         | 19,434      | 143,872      | 0           | 4           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 12    | 68.0     | 2,161         | 10,574      | 141,056      | 0           | 4           |
| GPT-5.6 Luna      | no-skills        | 2     | 40.6     | 159           | 544         | 0            | 5,909       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 39.1     | 159           | 544         | 0            | 5,965       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 38.7     | 101           | 544         | 0            | 6,010       | 0           |

### dependency-inspection — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 5     | 34.4     | 613           | 10          | 189,985      | 3,849       | 1           |
| Sonnet 5          | gradle-cli@1.2.0 | 5     | 47.4     | 565           | 10          | 197,127      | 7,204       | 0           |
| Sonnet 5          | gradle-cli@1.3.0 | 5     | 58.3     | 613           | 10          | 198,515      | 7,511       | 0           |
| Opus 5            | no-skills        | 8     | 85.3     | 1,669         | 16          | 217,567      | 5,623       | 0           |
| Opus 5            | gradle-cli@1.2.0 | 6     | 64.6     | 750           | 12          | 164,278      | 6,957       | 0           |
| Opus 5            | gradle-cli@1.3.0 | 8     | 79.7     | 1,745         | 16          | 232,963      | 10,056      | 1           |
| Deepseek V4 Flash | no-skills        | 6     | 24.6     | 760           | 6,970       | 33,792       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 7     | 26.9     | 1,130         | 4,313       | 52,224       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 8     | 62.3     | 1,178         | 4,893       | 63,744       | 0           | 0           |
| GPT-5.6 Luna      | no-skills        | 2     | 23.4     | 123           | 592         | 0            | 5,957       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 21.8     | 103           | 592         | 0            | 6,013       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 22.2     | 156           | 592         | 0            | 6,058       | 0           |

### test-filter-precision — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 5     | 30.2     | 576           | 10          | 189,959      | 3,821       | 1           |
| Sonnet 5          | gradle-cli@1.2.0 | 4     | 21.8     | 537           | 8           | 156,318      | 6,164       | 1           |
| Sonnet 5          | gradle-cli@1.3.0 | 4     | 23.5     | 555           | 8           | 157,671      | 6,760       | 1           |
| Opus 5            | no-skills        | 5     | 54.7     | 951           | 10          | 131,691      | 4,434       | 0           |
| Opus 5            | gradle-cli@1.2.0 | 7     | 61.4     | 1,257         | 14          | 198,187      | 7,512       | 0           |
| Opus 5            | gradle-cli@1.3.0 | 8     | 77.0     | 2,020         | 16          | 232,959      | 8,556       | 0           |
| Deepseek V4 Flash | no-skills        | 5     | 25.4     | 842           | 1,359       | 30,208       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 7     | 27.8     | 744           | 1,912       | 47,360       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 7     | 28.4     | 1,129         | 3,609       | 49,920       | 0           | 1           |
| GPT-5.6 Luna      | no-skills        | 2     | 23.9     | 185           | 556         | 0            | 5,921       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 22.2     | 150           | 556         | 0            | 5,977       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 22.3     | 106           | 556         | 0            | 6,022       | 0           |

### multi-project-task-selection — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 3     | 16.4     | 401           | 6           | 112,526      | 3,877       | 1           |
| Sonnet 5          | gradle-cli@1.2.0 | 4     | 22.9     | 463           | 8           | 156,256      | 6,092       | 1           |
| Sonnet 5          | gradle-cli@1.3.0 | 4     | 28.5     | 504           | 8           | 157,601      | 6,734       | 1           |
| Opus 5            | no-skills        | 6     | 42.7     | 1,168         | 12          | 159,739      | 5,033       | 1           |
| Opus 5            | gradle-cli@1.2.0 | 6     | 49.0     | 1,320         | 12          | 171,536      | 7,878       | 1           |
| Opus 5            | gradle-cli@1.3.0 | 7     | 50.9     | 2,106         | 14          | 207,741      | 9,552       | 3           |
| Deepseek V4 Flash | no-skills        | 4     | 19.6     | 431           | 707         | 22,144       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 4     | 23.3     | 263           | 2,478       | 24,192       | 0           | 0           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 6     | 25.2     | 937           | 5,036       | 46,848       | 0           | 2           |
| GPT-5.6 Luna      | no-skills        | 2     | 22.2     | 163           | 556         | 0            | 5,921       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 19.2     | 97            | 556         | 0            | 5,977       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 16.9     | 93            | 556         | 0            | 6,022       | 0           |

### custom-task-discovery — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 7     | 40.8     | 1,017         | 14          | 272,307      | 5,763       | 1           |
| Sonnet 5          | gradle-cli@1.2.0 | 6     | 46.2     | 890           | 12          | 232,810      | 5,257       | 1           |
| Sonnet 5          | gradle-cli@1.3.0 | 6     | 33.9     | 880           | 12          | 233,426      | 5,492       | 1           |
| Opus 5            | no-skills        | 6     | 36.0     | 1,071         | 12          | 160,748      | 5,279       | 1           |
| Opus 5            | gradle-cli@1.2.0 | 9     | 59.3     | 1,452         | 18          | 257,550      | 8,435       | 2           |
| Opus 5            | gradle-cli@1.3.0 | 8     | †        | 1,848         | 16          | 199,046      | 41,652      | 2           |
| Deepseek V4 Flash | no-skills        | 7     | 29.6     | 1,011         | 1,924       | 47,488       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 7     | 25.1     | 723           | 2,381       | 48,128       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 8     | 34.6     | 881           | 4,642       | 61,440       | 0           | 1           |
| GPT-5.6 Luna      | no-skills        | 2     | 22.3     | 148           | 543         | 0            | 5,908       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 17.3     | 140           | 543         | 0            | 5,964       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 19.4     | 148           | 543         | 0            | 6,009       | 0           |

† Wall clock anomalous (-876.8s reported by harness); actual run was ~17 minutes.

### etiquette-destructive-task — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 4     | 36.0     | 1,092         | 8           | 151,109      | 4,447       | 1           |
| Sonnet 5          | gradle-cli@1.2.0 | 3     | 29.8     | 1,501         | 6           | 112,514      | 3,207       | 0           |
| Sonnet 5          | gradle-cli@1.3.0 | 4     | 35.7     | 1,375         | 8           | 154,827      | 6,770       | 0           |
| Opus 5            | no-skills        | 4     | 46.5     | 898           | 8           | 102,559      | 3,545       | 0           |
| Opus 5            | gradle-cli@1.2.0 | 5     | 38.1     | 1,200         | 10          | 133,714      | 7,020       | 1           |
| Opus 5            | gradle-cli@1.3.0 | 3     | 35.1     | 1,299         | 6           | 80,189       | 6,987       | 0           |
| Deepseek V4 Flash | no-skills        | 4     | 22.5     | 466           | 983         | 22,272       | 0           | 0           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 5     | 28.9     | 1,111         | 3,184       | 30,592       | 0           | 0           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 4     | 25.0     | 732           | 3,518       | 24,832       | 0           | 1           |
| GPT-5.6 Luna      | no-skills        | 2     | 24.4     | 229           | 541         | 0            | 5,906       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 22.5     | 170           | 541         | 0            | 5,962       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 22.5     | 184           | 541         | 0            | 6,007       | 0           |

_Deepseek and GPT-5.6 Luna all arms INVALID — scorer results excluded. Skill-used PASS for all arms of both models._

### exclude-task-trap — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Sonnet 5          | no-skills        | 6     | 37.2     | 1,515         | 12          | 233,320      | 5,863       | 1           |
| Sonnet 5          | gradle-cli@1.2.0 | 10    | ‡663.4   | 1,862         | 20          | 400,886      | 14,116      | 5           |
| Sonnet 5          | gradle-cli@1.3.0 | 5     | 34.5     | 1,341         | 10          | 201,395      | 8,803       | 4           |
| Opus 5            | no-skills        | 6     | 64.8     | 1,634         | 12          | 160,256      | 5,314       | 0           |
| Opus 5            | gradle-cli@1.2.0 | 7     | 54.8     | 2,054         | 14          | 200,918      | 8,282       | 2           |
| Opus 5            | gradle-cli@1.3.0 | 8     | 72.6     | 2,095         | 16          | 210,048      | 32,950      | 1           |
| Deepseek V4 Flash | no-skills        | 6     | 25.7     | 967           | 2,045       | 38,272       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.2.0 | 10    | 42.6     | 2,209         | 7,342       | 94,976       | 0           | 4           |
| Deepseek V4 Flash | gradle-cli@1.3.0 | 7     | 39.3     | 1,372         | 5,442       | 56,832       | 0           | 3           |
| GPT-5.6 Luna      | no-skills        | 2     | 23.7     | 141           | 549         | 0            | 5,914       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.2.0 | 2     | 18.5     | 154           | 549         | 0            | 5,970       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.3.0 | 2     | 19.1     | 151           | 549         | 0            | 6,015       | 0           |

‡ Known anomaly — likely a retry loop (5 Gradle invocations, skill not picked up). Skill-used FAIL for this arm.
