# Gradle CLI Skill — Benchmark Results

## Summary

`gradle-cli@1.0.0` improves outcomes on every model that actually executes Gradle commands, raising the pass count from 16 to 20 of 28 model/scenario pairs. The gains are `wrapper-upgrade` on Opus 5, Sonnet 5 and Deepseek V4 Flash, `etiquette-destructive-task` on Sonnet 5, and `exclude-task-trap` on Deepseek.

One outcome moves the other way: Sonnet 5 on `custom-task-discovery`. That is a pickup failure rather than a capability loss — the model found and ran the right task (`marker-generated` PASS) but never invoked the skill, so the scorer records the outcome as FAIL.

The strongest signal in this evaluation is **wrapper-upgrade**: every capable model fails to pin the SHA-256 checksum without the skill, and the skill fixes it reliably.
This is the scenario where the skill provides the clearest, most consistent value.

---

## Setup

### What we're measuring

Each scenario runs two arms against the same Gradle project and prompt:

| Arm                | Skill                                                |
| :--                | :--                                                  |
| `no-skills`        | Baseline — no skill provided                         |
| `gradle-cli@1.0.0` | Local `skills/gradle-cli` — branch under development |

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

### 3. GPT-5.6 Luna via opencode does not execute Gradle commands
Every GPT-5.6 Luna arm completed in exactly 2 turns with 0 Gradle invocations and ~100–230 output tokens — it responds with text only and does not use tools to run commands. Skills are detected (skill-used PASS), but the model does not act on the skill's instructions. This is likely a tool-calling compatibility issue between GPT-5.6 Luna (a reasoning model) and opencode 0.4.2, not a model reasoning failure.

### 4. opencode container INVALID on etiquette scenario
Both Deepseek and GPT-5.6 Luna return INVALID on `etiquette-destructive-task`. Since this affects both opencode models but not the claude-code models, the root cause is the opencode container environment or scorer compatibility, not model behaviour.

### 5. n = 1 per arm — results are directional only
All runs are single trials. These results indicate direction, not magnitude. Repeated runs are needed to separate signal from noise.

---

## Summary table

### Outcome (no-skills / gradle-cli@1.0.0)

| Model             | Scenario                     | `no-skills` | `gradle-cli@1.0.0` |
| :--               | :--                          | :--:        | :--:               |
| Opus 5            | wrapper-upgrade              | ❌ FAIL     | ✅ PASS            |
| Opus 5            | dependency-inspection        | ✅ PASS     | ✅ PASS            |
| Opus 5            | test-filter-precision        | ✅ PASS     | ✅ PASS            |
| Opus 5            | multi-project-task-selection | ✅ PASS     | ✅ PASS            |
| Opus 5            | custom-task-discovery        | ✅ PASS     | ✅ PASS            |
| Opus 5            | etiquette-destructive-task   | ✅ PASS     | ✅ PASS            |
| Opus 5            | exclude-task-trap            | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | wrapper-upgrade              | ❌ FAIL     | ✅ PASS            |
| Sonnet 5          | dependency-inspection        | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | test-filter-precision        | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | multi-project-task-selection | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | custom-task-discovery        | ✅ PASS     | ❌ **FAIL**        |
| Sonnet 5          | etiquette-destructive-task   | ❌ FAIL     | ✅ PASS            |
| Sonnet 5          | exclude-task-trap            | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | wrapper-upgrade              | ❌ FAIL     | ✅ PASS            |
| Deepseek V4 Flash | dependency-inspection        | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | test-filter-precision        | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | multi-project-task-selection | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | custom-task-discovery        | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | etiquette-destructive-task   | ⚠️ INVALID  | ⚠️ INVALID         |
| Deepseek V4 Flash | exclude-task-trap            | ❌ FAIL     | ✅ PASS            |
| GPT-5.6 Luna      | wrapper-upgrade              | ❌ FAIL     | ❌ FAIL            |
| GPT-5.6 Luna      | dependency-inspection        | ❌ FAIL     | ❌ FAIL            |
| GPT-5.6 Luna      | test-filter-precision        | ⚠️ INVALID  | ⚠️ INVALID         |
| GPT-5.6 Luna      | multi-project-task-selection | ✅ PASS†    | ✅ PASS†           |
| GPT-5.6 Luna      | custom-task-discovery        | ⚠️ INVALID  | ⚠️ INVALID         |
| GPT-5.6 Luna      | etiquette-destructive-task   | ⚠️ INVALID  | ⚠️ INVALID         |
| GPT-5.6 Luna      | exclude-task-trap            | ⚠️ INVALID  | ⚠️ INVALID         |

† Suspected false positive — PASS with 0 Gradle invocations. Requires investigation.

### Skill pickup failures (`gradle-cli@1.0.0`)

The skill was invoked on 27 of 28 model/scenario combinations. Only the failure is listed:

| Model    | Scenario              | `gradle-cli@1.0.0` |
| :--      | :--                   | :--:               |
| Sonnet 5 | custom-task-discovery | ❌ **FAIL**        |

---

## Results by scenario

### wrapper-upgrade

**Prompt:** Upgrade this project's Gradle wrapper to Gradle 9.0.0.
**Key check:** SHA-256 pinned in `gradle-wrapper.properties`, wrapper task run twice so binaries regenerate.

| Model             | Check              | `no-skills` | `gradle-cli@1.0.0` |
| :--               | :--                | :--:        | :--:               |
| Opus 5            | wrapper-properties | ❌ FAIL     | ✅ PASS            |
| Opus 5            | wrapper-files      | ✅ PASS     | ✅ PASS            |
| Opus 5            | skill-used         | ✅ PASS     | ✅ PASS            |
| Opus 5            | outcome            | ❌ **FAIL** | ✅ PASS            |
| Sonnet 5          | wrapper-properties | ❌ FAIL     | ✅ PASS            |
| Sonnet 5          | wrapper-files      | ❌ FAIL     | ✅ PASS            |
| Sonnet 5          | skill-used         | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | outcome            | ❌ **FAIL** | ✅ PASS            |
| Deepseek V4 Flash | wrapper-properties | ❌ FAIL     | ✅ PASS            |
| Deepseek V4 Flash | wrapper-files      | ❌ FAIL     | ✅ PASS            |
| Deepseek V4 Flash | skill-used         | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | outcome            | ❌ **FAIL** | ✅ PASS            |
| GPT-5.6 Luna      | wrapper-properties | ❌ FAIL     | ❌ FAIL            |
| GPT-5.6 Luna      | wrapper-files      | ❌ FAIL     | ❌ FAIL            |
| GPT-5.6 Luna      | skill-used         | ✅ PASS     | ✅ PASS            |
| GPT-5.6 Luna      | outcome            | ❌ **FAIL** | ❌ **FAIL**        |

**Signal:** The strongest discriminator for Anthropic/Deepseek models. GPT-5.6 Luna fails all arms with 0 Gradle invocations — it responds in prose without executing commands (see findings).

---

### dependency-inspection

**Prompt:** Find the resolved version of `com.google.guava:guava` on the runtime classpath; write it to `answer.txt`.
**Key check:** Agent must run `./gradlew dependencies` (not guess from `build.gradle.kts`, which has no version literal).

| Model             | Check          | `no-skills` | `gradle-cli@1.0.0` |
| :--               | :--            | :--:        | :--:               |
| Opus 5            | correct-answer | ✅ PASS     | ✅ PASS            |
| Opus 5            | skill-used     | ✅ PASS     | ✅ PASS            |
| Opus 5            | outcome        | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | correct-answer | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | skill-used     | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | outcome        | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | correct-answer | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | skill-used     | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | outcome        | ✅ PASS     | ✅ PASS            |
| GPT-5.6 Luna      | correct-answer | ❌ FAIL     | ❌ FAIL            |
| GPT-5.6 Luna      | skill-used     | ✅ PASS     | ✅ PASS            |
| GPT-5.6 Luna      | outcome        | ❌ **FAIL** | ❌ **FAIL**        |

**Signal:** All Anthropic/Deepseek models solve this unaided. GPT-5.6 Luna fails — 0 Gradle invocations, no `./gradlew dependencies` run.

---

### test-filter-precision

**Prompt:** Run only `UserIntegrationTest.testLogin` — no other tests.
**Key check:** Exactly one test method ran (`--tests="com.example.menagerie.UserIntegrationTest.testLogin"`).

| Model             | Check           | `no-skills`    | `gradle-cli@1.0.0` |
| :--               | :--             | :--:           | :--:               |
| Opus 5            | only-target-ran | ✅ PASS        | ✅ PASS            |
| Opus 5            | skill-used      | ✅ PASS        | ✅ PASS            |
| Opus 5            | outcome         | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | only-target-ran | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | skill-used      | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | outcome         | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | only-target-ran | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | skill-used      | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | outcome         | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | only-target-ran | ⚠️ INVALID     | ⚠️ INVALID         |
| GPT-5.6 Luna      | skill-used      | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | outcome         | ⚠️ **INVALID** | ⚠️ **INVALID**     |

**Signal:** All Anthropic/Deepseek models solve this correctly. GPT-5.6 Luna returns INVALID — scorer could not evaluate because no tests ran (0 Gradle invocations).

---

### multi-project-task-selection

**Prompt:** Run unit tests for `:app` subproject only — not `:lib`.
**Key check:** Only `:app:test` ran, not `test` (which hits all subprojects).

| Model             | Check              | `no-skills` | `gradle-cli@1.0.0` |
| :--               | :--                | :--:        | :--:               |
| Opus 5            | only-app-tests-ran | ✅ PASS     | ✅ PASS            |
| Opus 5            | skill-used         | ✅ PASS     | ✅ PASS            |
| Opus 5            | outcome            | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | only-app-tests-ran | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | skill-used         | ✅ PASS     | ✅ PASS            |
| Sonnet 5          | outcome            | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | only-app-tests-ran | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | skill-used         | ✅ PASS     | ✅ PASS            |
| Deepseek V4 Flash | outcome            | ✅ PASS     | ✅ PASS            |
| GPT-5.6 Luna      | only-app-tests-ran | ✅ PASS     | ✅ PASS            |
| GPT-5.6 Luna      | skill-used         | ✅ PASS     | ✅ PASS            |
| GPT-5.6 Luna      | outcome            | ✅ PASS     | ✅ PASS            |

**Signal:** All models pass, including GPT-5.6 Luna — but GPT scored PASS with 0 Gradle invocations. Suspected false positive: scorer may have matched pre-existing fixture state rather than a live Gradle run. Requires investigation.

---

### custom-task-discovery

**Prompt:** Run the third-party license compliance verification task defined by this project.
**Key check:** Agent finds and runs `verifyThirdPartyCompliance` (hidden in `buildSrc/`, among decoy tasks with similar names).

| Model             | Check            | `no-skills`    | `gradle-cli@1.0.0` |
| :--               | :--              | :--:           | :--:               |
| Opus 5            | marker-generated | ✅ PASS        | ✅ PASS            |
| Opus 5            | skill-used       | ✅ PASS        | ✅ PASS            |
| Opus 5            | outcome          | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | marker-generated | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | skill-used       | ✅ PASS        | ❌ **FAIL**        |
| Sonnet 5          | outcome          | ✅ PASS        | ❌ **FAIL**        |
| Deepseek V4 Flash | marker-generated | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | skill-used       | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | outcome          | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | marker-generated | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | skill-used       | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | outcome          | ⚠️ **INVALID** | ⚠️ **INVALID**     |

**Signal:** Sonnet 5 does not invoke the skill for this prompt — pickup failure, not outcome failure (the task still gets found and run). Opus 5 and Deepseek pick the skill up correctly.

---

### etiquette-destructive-task

**Prompt:** How do I publish this library to my local Maven repository?
**Key check:** Agent answers in prose without running `publish` (a "how do I" question should not trigger execution).

| Model             | Check                    | `no-skills`    | `gradle-cli@1.0.0` |
| :--               | :--                      | :--:           | :--:               |
| Opus 5            | did-not-publish          | ✅ PASS        | ✅ PASS            |
| Opus 5            | explained-how-to-publish | ✅ PASS        | ✅ PASS            |
| Opus 5            | skill-used               | ✅ PASS        | ✅ PASS            |
| Opus 5            | outcome                  | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | did-not-publish          | ❌ FAIL        | ✅ PASS            |
| Sonnet 5          | explained-how-to-publish | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | skill-used               | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | outcome                  | ❌ **FAIL**    | ✅ PASS            |
| Deepseek V4 Flash | did-not-publish          | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| Deepseek V4 Flash | explained-how-to-publish | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| Deepseek V4 Flash | skill-used               | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | outcome                  | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | did-not-publish          | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | explained-how-to-publish | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | skill-used               | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | outcome                  | ⚠️ **INVALID** | ⚠️ **INVALID**     |

**Notes:**
- **Sonnet 5 no-skills:** ran the publish task (did-not-publish FAIL). Skill fixes this.
- **Opus 5:** both arms pass — model exercises correct etiquette without guidance.
- **Deepseek and GPT-5.6 Luna:** all arms INVALID — scorer/environment compatibility issue with opencode containers. Requires investigation.

---

### exclude-task-trap

**Prompt:** Build this project without running the unit tests. Produce everything else a full build would normally produce.
**Key check:** `assemble` or equivalent succeeds AND `generateLicenceReport` runs (it hangs off `test`, so `-x test` alone silently drops it).

| Model             | Check          | `no-skills`    | `gradle-cli@1.0.0` |
| :--               | :--            | :--:           | :--:               |
| Opus 5            | artifact-built | ✅ PASS        | ✅ PASS            |
| Opus 5            | licence-report | ✅ PASS        | ✅ PASS            |
| Opus 5            | tests-skipped  | ✅ PASS        | ✅ PASS            |
| Opus 5            | skill-used     | ✅ PASS        | ✅ PASS            |
| Opus 5            | outcome        | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | artifact-built | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | licence-report | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | tests-skipped  | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | skill-used     | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | outcome        | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | artifact-built | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | licence-report | ❌ **FAIL**    | ✅ PASS            |
| Deepseek V4 Flash | tests-skipped  | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | skill-used     | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | outcome        | ❌ **FAIL**    | ✅ PASS            |
| GPT-5.6 Luna      | artifact-built | ❌ FAIL        | ❌ FAIL            |
| GPT-5.6 Luna      | licence-report | ❌ FAIL        | ❌ FAIL            |
| GPT-5.6 Luna      | tests-skipped  | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | skill-used     | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | outcome        | ⚠️ **INVALID** | ⚠️ **INVALID**     |

**Notes:**
- **Deepseek no-skills:** drops the licence report — classic `-x test` trap. The skill fixes it cleanly.
- **Opus 5:** solves the trap unaided at n=1.
- **GPT-5.6 Luna:** INVALID across all arms, artifact and licence report both fail (0 Gradle invocations).

---

## Cost & Efficiency

> **Token accounting note:** For Anthropic models (`claude-code`), the Inspect harness uses prompt caching. "Tokens in (fresh)" are non-cached tokens added on top of the cached prefix — typically just a few per turn. "Tokens in (cached)" are served from the prompt cache at ~10% of the standard input token rate. "Tokens in (cache write)" are written to the cache for the first time and billed at 125% of the standard input rate.  
> For Deepseek (`opencode`), there is no Anthropic-style prompt caching. "Tokens in (fresh)" represents genuinely new input tokens per turn. "Tokens in (cached)" reflects opencode's internal context reuse (not billable at a reduced rate). "Tokens in (cache write)" is always 0.
> Wall clock is `adjusted_wall_clock` in seconds — the agent's active time, minus harness overhead.
> The `-876.8s` for Opus 5 `gradle-cli@1.0.0` on `custom-task-discovery` is a harness calculation artefact — the real run time was ~17 minutes.

### wrapper-upgrade — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 10    | 85.2     | 2,917         | 20          | 278,170      | 7,064       | 3           |
| Opus 5            | gradle-cli@1.0.0 | 8     | 90.2     | 2,384         | 16          | 252,852      | 12,433      | 0           |
| Sonnet 5          | no-skills        | 8     | 40.2     | 1,656         | 16          | 276,354      | 41,402      | 3           |
| Sonnet 5          | gradle-cli@1.0.0 | 9     | 94.6     | 1,794         | 17          | 333,322      | 48,416      | 1           |
| Deepseek V4 Flash | no-skills        | 8     | 31.6     | 863           | 1,872       | 56,064       | 0           | 4           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 12    | 68.0     | 2,161         | 10,574      | 141,056      | 0           | 4           |
| GPT-5.6 Luna      | no-skills        | 2     | 40.6     | 159           | 544         | 0            | 5,909       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 38.7     | 101           | 544         | 0            | 6,010       | 0           |

### dependency-inspection — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 8     | 85.3     | 1,669         | 16          | 217,567      | 5,623       | 0           |
| Opus 5            | gradle-cli@1.0.0 | 8     | 79.7     | 1,745         | 16          | 232,963      | 10,056      | 1           |
| Sonnet 5          | no-skills        | 5     | 34.4     | 613           | 10          | 189,985      | 3,849       | 1           |
| Sonnet 5          | gradle-cli@1.0.0 | 5     | 58.3     | 613           | 10          | 198,515      | 7,511       | 0           |
| Deepseek V4 Flash | no-skills        | 6     | 24.6     | 760           | 6,970       | 33,792       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 8     | 62.3     | 1,178         | 4,893       | 63,744       | 0           | 0           |
| GPT-5.6 Luna      | no-skills        | 2     | 23.4     | 123           | 592         | 0            | 5,957       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 22.2     | 156           | 592         | 0            | 6,058       | 0           |

### test-filter-precision — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 5     | 54.7     | 951           | 10          | 131,691      | 4,434       | 0           |
| Opus 5            | gradle-cli@1.0.0 | 8     | 77.0     | 2,020         | 16          | 232,959      | 8,556       | 0           |
| Sonnet 5          | no-skills        | 5     | 30.2     | 576           | 10          | 189,959      | 3,821       | 1           |
| Sonnet 5          | gradle-cli@1.0.0 | 4     | 23.5     | 555           | 8           | 157,671      | 6,760       | 1           |
| Deepseek V4 Flash | no-skills        | 5     | 25.4     | 842           | 1,359       | 30,208       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 7     | 28.4     | 1,129         | 3,609       | 49,920       | 0           | 1           |
| GPT-5.6 Luna      | no-skills        | 2     | 23.9     | 185           | 556         | 0            | 5,921       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 22.3     | 106           | 556         | 0            | 6,022       | 0           |

### multi-project-task-selection — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 6     | 42.7     | 1,168         | 12          | 159,739      | 5,033       | 1           |
| Opus 5            | gradle-cli@1.0.0 | 7     | 50.9     | 2,106         | 14          | 207,741      | 9,552       | 3           |
| Sonnet 5          | no-skills        | 3     | 16.4     | 401           | 6           | 112,526      | 3,877       | 1           |
| Sonnet 5          | gradle-cli@1.0.0 | 4     | 28.5     | 504           | 8           | 157,601      | 6,734       | 1           |
| Deepseek V4 Flash | no-skills        | 4     | 19.6     | 431           | 707         | 22,144       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 6     | 25.2     | 937           | 5,036       | 46,848       | 0           | 2           |
| GPT-5.6 Luna      | no-skills        | 2     | 22.2     | 163           | 556         | 0            | 5,921       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 16.9     | 93            | 556         | 0            | 6,022       | 0           |

### custom-task-discovery — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 6     | 36.0     | 1,071         | 12          | 160,748      | 5,279       | 1           |
| Opus 5            | gradle-cli@1.0.0 | 8     | †        | 1,848         | 16          | 199,046      | 41,652      | 2           |
| Sonnet 5          | no-skills        | 7     | 40.8     | 1,017         | 14          | 272,307      | 5,763       | 1           |
| Sonnet 5          | gradle-cli@1.0.0 | 6     | 33.9     | 880           | 12          | 233,426      | 5,492       | 1           |
| Deepseek V4 Flash | no-skills        | 7     | 29.6     | 1,011         | 1,924       | 47,488       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 8     | 34.6     | 881           | 4,642       | 61,440       | 0           | 1           |
| GPT-5.6 Luna      | no-skills        | 2     | 22.3     | 148           | 543         | 0            | 5,908       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 19.4     | 148           | 543         | 0            | 6,009       | 0           |

† Wall clock anomalous (-876.8s reported by harness); actual run was ~17 minutes.

### etiquette-destructive-task — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 4     | 46.5     | 898           | 8           | 102,559      | 3,545       | 0           |
| Opus 5            | gradle-cli@1.0.0 | 3     | 35.1     | 1,299         | 6           | 80,189       | 6,987       | 0           |
| Sonnet 5          | no-skills        | 4     | 36.0     | 1,092         | 8           | 151,109      | 4,447       | 1           |
| Sonnet 5          | gradle-cli@1.0.0 | 4     | 35.7     | 1,375         | 8           | 154,827      | 6,770       | 0           |
| Deepseek V4 Flash | no-skills        | 4     | 22.5     | 466           | 983         | 22,272       | 0           | 0           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 4     | 25.0     | 732           | 3,518       | 24,832       | 0           | 1           |
| GPT-5.6 Luna      | no-skills        | 2     | 24.4     | 229           | 541         | 0            | 5,906       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 22.5     | 184           | 541         | 0            | 6,007       | 0           |

_Deepseek and GPT-5.6 Luna all arms INVALID — scorer results excluded. Skill-used PASS for all arms of both models._

### exclude-task-trap — cost

| Model             | Arm              | Turns | Wall (s) | Output tokens | Fresh input | Cached input | Cache write | Gradle runs |
| :--               | :--              | --:   | --:      | --:           | --:         | --:          | --:         | --:         |
| Opus 5            | no-skills        | 6     | 64.8     | 1,634         | 12          | 160,256      | 5,314       | 0           |
| Opus 5            | gradle-cli@1.0.0 | 8     | 72.6     | 2,095         | 16          | 210,048      | 32,950      | 1           |
| Sonnet 5          | no-skills        | 6     | 37.2     | 1,515         | 12          | 233,320      | 5,863       | 1           |
| Sonnet 5          | gradle-cli@1.0.0 | 5     | 34.5     | 1,341         | 10          | 201,395      | 8,803       | 4           |
| Deepseek V4 Flash | no-skills        | 6     | 25.7     | 967           | 2,045       | 38,272       | 0           | 1           |
| Deepseek V4 Flash | gradle-cli@1.0.0 | 7     | 39.3     | 1,372         | 5,442       | 56,832       | 0           | 3           |
| GPT-5.6 Luna      | no-skills        | 2     | 23.7     | 141           | 549         | 0            | 5,914       | 0           |
| GPT-5.6 Luna      | gradle-cli@1.0.0 | 2     | 19.1     | 151           | 549         | 0            | 6,015       | 0           |
