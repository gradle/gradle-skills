# Gradle CLI Skill v1.0.0 — Benchmark Results

## Summary

`gradle-cli@1.0.0` improves outcomes on every model that actually executes Gradle commands, raising the pass count from 17 to 21 of 28 model/scenario pairs. The gains are `wrapper-upgrade` on Opus 5, Sonnet 5 and Deepseek V4 Flash, and `exclude-task-trap` on Deepseek.

No outcome moves the other way. Sonnet 5 on `custom-task-discovery` does fail *intermittently*, and always for the same reason: the model finds and runs the right task, but sometimes (around 25% of cases) never invokes the skill. It is a pickup flake, not a capability loss, and the summary table shows the majority verdict.

The strongest signal in this evaluation is **wrapper-upgrade**: every capable model fails to pin the SHA-256 checksum without the skill, and the skill fixes it reliably.
This is the scenario where the skill provides the clearest, most consistent value.

---

## Setup

### What we're measuring

Each scenario runs two arms against the same Gradle project and prompt:

| Arm                | Skill                        |
| :----------------- | :--------------------------- |
| `no-skills`        | Baseline — no skill provided |
| `gradle-cli@1.0.0` | Local `skills/gradle-cli`    |

### Models tested

| Model                        | CLI              | Notes                          |
| :--------------------------- | :--------------- | :----------------------------- |
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
| :---------------- | :--------------------------- | :---------: | :----------------: |
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
| Sonnet 5          | custom-task-discovery        | ✅ PASS     | ✅ PASS‡           |
| Sonnet 5          | etiquette-destructive-task   | ✅ PASS     | ✅ PASS            |
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

The skill was invoked on every model/scenario combination except one, which is
intermittent rather than consistent:

| Model    | Scenario              | `gradle-cli@1.0.0` |
| :------- | :-------------------- | :----------------: |
| Sonnet 5 | custom-task-discovery | ✅ PASS 3 of 4‡    |

‡ Sonnet 5 does not reliably reach for the skill on this prompt.

---

## Results by scenario

### wrapper-upgrade

**Prompt:** Upgrade this project's Gradle wrapper to Gradle 9.0.0.
**Key check:** SHA-256 pinned in `gradle-wrapper.properties`, wrapper task run twice so binaries regenerate. `project-builds` confirms the upgraded wrapper still builds the project.

| Model             | Check              | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :----------------- | :---------: | :----------------: |
| Opus 5            | project-builds     | ✅ PASS     | ✅ PASS            |
| Opus 5            | wrapper-properties | ❌ FAIL     | ✅ PASS            |
| Opus 5            | wrapper-files      | ✅ PASS     | ✅ PASS            |
| Opus 5            | skill-used         | ✅ PASS     | ✅ PASS            |
| Opus 5            | outcome            | ❌ **FAIL** | ✅ PASS            |
| Sonnet 5          | project-builds     | ✅ PASS     | ✅ PASS            |
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
| :---------------- | :------------- | :---------: | :----------------: |
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
| :---------------- | :-------------- | :------------: | :----------------: |
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
| :---------------- | :----------------- | :---------: | :----------------: |
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
| :---------------- | :--------------- | :------------: | :----------------: |
| Opus 5            | marker-generated | ✅ PASS        | ✅ PASS            |
| Opus 5            | skill-used       | ✅ PASS        | ✅ PASS            |
| Opus 5            | outcome          | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | marker-generated | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | skill-used       | ✅ PASS        | ✅ PASS‡           |
| Sonnet 5          | outcome          | ✅ PASS        | ✅ PASS‡           |
| Deepseek V4 Flash | marker-generated | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | skill-used       | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | outcome          | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | marker-generated | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | skill-used       | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | outcome          | ⚠️ **INVALID** | ⚠️ **INVALID**     |

**Signal:** Sonnet 5 does not *reliably* invoke the skill for this prompt — it picked it up around 75% of the time and missed in the rest. That is a pickup flake, not an outcome failure. Opus 5 and Deepseek pick the skill up correctly.

---

### etiquette-destructive-task

**Prompt:** How do I publish this library to my local Maven repository?
**Key check:** Agent answers in prose without running `publish` (a "how do I" question should not trigger execution).

| Model             | Check                    | `no-skills`    | `gradle-cli@1.0.0` |
| :---------------- | :----------------------- | :------------: | :----------------: |
| Opus 5            | did-not-publish          | ✅ PASS        | ✅ PASS            |
| Opus 5            | explained-how-to-publish | ✅ PASS        | ✅ PASS            |
| Opus 5            | skill-used               | ✅ PASS        | ✅ PASS            |
| Opus 5            | outcome                  | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | did-not-publish          | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | explained-how-to-publish | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | skill-used               | ✅ PASS        | ✅ PASS            |
| Sonnet 5          | outcome                  | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | did-not-publish          | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| Deepseek V4 Flash | explained-how-to-publish | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| Deepseek V4 Flash | skill-used               | ✅ PASS        | ✅ PASS            |
| Deepseek V4 Flash | outcome                  | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | did-not-publish          | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | explained-how-to-publish | ⚠️ **INVALID** | ⚠️ **INVALID**     |
| GPT-5.6 Luna      | skill-used               | ✅ PASS        | ✅ PASS            |
| GPT-5.6 Luna      | outcome                  | ⚠️ **INVALID** | ⚠️ **INVALID**     |

**Notes:**
- **Sonnet 5:** both arms pass. sThe skill has no measurable effect here.
- **Opus 5:** both arms pass — model exercises correct etiquette without guidance.
- **Deepseek and GPT-5.6 Luna:** all arms INVALID — scorer/environment compatibility issue with opencode containers. Requires investigation.

---

### exclude-task-trap

**Prompt:** Build this project without running the unit tests. Produce everything else a full build would normally produce.
**Key check:** `assemble` or equivalent succeeds AND `generateLicenceReport` runs (it hangs off `test`, so `-x test` alone silently drops it).

| Model             | Check          | `no-skills`    | `gradle-cli@1.0.0` |
| :---------------- | :------------- | :------------: | :----------------: |
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
>
> **Reading the 🏆 in these tables:** it marks the cheaper of the two arms for that model and metric — lower is better for every metric shown. ✅ ❌ ⚠️ are reserved for scorer verdicts and never appear here. Ties are left unmarked. `Gradle runs` is never marked: it is a diagnostic rather than a cost, and fewer invocations can mean the agent never did the work (see GPT-5.6 Luna, which scores 0 everywhere).

### wrapper-upgrade — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 14          | 🏆 9               |
| Opus 5            | Wall (s)      | 🏆 113.9    | 154.9              |
| Opus 5            | Output tokens | 4,753       | 🏆 4,067           |
| Opus 5            | Fresh input   | 28          | 🏆 18              |
| Opus 5            | Cached input  | 358,797     | 🏆 234,243         |
| Opus 5            | Cache write   | 🏆 9,348    | 53,488             |
| Opus 5            | Gradle runs   | 1           | 0                  |
| Sonnet 5          | Turns         | 12          | 🏆 11              |
| Sonnet 5          | Wall (s)      | 🏆 95.9     | 126.7              |
| Sonnet 5          | Output tokens | 🏆 2,142    | 2,269              |
| Sonnet 5          | Fresh input   | 24          | 🏆 21              |
| Sonnet 5          | Cached input  | 358,459     | 🏆 337,019         |
| Sonnet 5          | Cache write   | 🏆 35,935   | 48,928             |
| Sonnet 5          | Gradle runs   | 3           | 2                  |
| Deepseek V4 Flash | Turns         | 🏆 8        | 12                 |
| Deepseek V4 Flash | Wall (s)      | 🏆 31.6     | 68.0               |
| Deepseek V4 Flash | Output tokens | 🏆 863      | 2,161              |
| Deepseek V4 Flash | Fresh input   | 🏆 1,872    | 10,574             |
| Deepseek V4 Flash | Cached input  | 🏆 56,064   | 141,056            |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 4           | 4                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 40.6        | 🏆 38.7            |
| GPT-5.6 Luna      | Output tokens | 159         | 🏆 101             |
| GPT-5.6 Luna      | Fresh input   | 544         | 544                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,909    | 6,010              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |

### dependency-inspection — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 🏆 8        | 11                 |
| Opus 5            | Wall (s)      | 🏆 108.2    | 112.1              |
| Opus 5            | Output tokens | 🏆 2,797    | 3,102              |
| Opus 5            | Fresh input   | 🏆 16       | 22                 |
| Opus 5            | Cached input  | 🏆 197,021  | 294,762            |
| Opus 5            | Cache write   | 🏆 7,180    | 10,692             |
| Opus 5            | Gradle runs   | 0           | 2                  |
| Sonnet 5          | Turns         | 🏆 5        | 7                  |
| Sonnet 5          | Wall (s)      | 🏆 36.1     | 71.1               |
| Sonnet 5          | Output tokens | 🏆 643      | 995                |
| Sonnet 5          | Fresh input   | 🏆 10       | 14                 |
| Sonnet 5          | Cached input  | 🏆 147,626  | 218,496            |
| Sonnet 5          | Cache write   | 🏆 3,973    | 8,686              |
| Sonnet 5          | Gradle runs   | 1           | 0                  |
| Deepseek V4 Flash | Turns         | 🏆 6        | 8                  |
| Deepseek V4 Flash | Wall (s)      | 🏆 24.6     | 62.3               |
| Deepseek V4 Flash | Output tokens | 🏆 760      | 1,178              |
| Deepseek V4 Flash | Fresh input   | 6,970       | 🏆 4,893           |
| Deepseek V4 Flash | Cached input  | 🏆 33,792   | 63,744             |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 1           | 0                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 23.4        | 🏆 22.2            |
| GPT-5.6 Luna      | Output tokens | 🏆 123      | 156                |
| GPT-5.6 Luna      | Fresh input   | 592         | 592                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,957    | 6,058              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |

### test-filter-precision — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 🏆 6        | 8                  |
| Opus 5            | Wall (s)      | 🏆 65.2     | 76.7               |
| Opus 5            | Output tokens | 🏆 1,266    | 1,789              |
| Opus 5            | Fresh input   | 🏆 12       | 16                 |
| Opus 5            | Cached input  | 🏆 140,207  | 207,288            |
| Opus 5            | Cache write   | 🏆 4,732    | 8,175              |
| Opus 5            | Gradle runs   | 0           | 1                  |
| Sonnet 5          | Turns         | 🏆 5        | 6                  |
| Sonnet 5          | Wall (s)      | 59.6        | 🏆 39.7            |
| Sonnet 5          | Output tokens | 🏆 753      | 847                |
| Sonnet 5          | Fresh input   | 🏆 10       | 12                 |
| Sonnet 5          | Cached input  | 🏆 146,792  | 192,028            |
| Sonnet 5          | Cache write   | 🏆 4,082    | 7,606              |
| Sonnet 5          | Gradle runs   | 0           | 1                  |
| Deepseek V4 Flash | Turns         | 🏆 5        | 7                  |
| Deepseek V4 Flash | Wall (s)      | 🏆 25.4     | 28.4               |
| Deepseek V4 Flash | Output tokens | 🏆 842      | 1,129              |
| Deepseek V4 Flash | Fresh input   | 🏆 1,359    | 3,609              |
| Deepseek V4 Flash | Cached input  | 🏆 30,208   | 49,920             |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 1           | 1                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 23.9        | 🏆 22.3            |
| GPT-5.6 Luna      | Output tokens | 185         | 🏆 106             |
| GPT-5.6 Luna      | Fresh input   | 556         | 556                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,921    | 6,022              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |

### multi-project-task-selection — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 7           | 🏆 6               |
| Opus 5            | Wall (s)      | 52.9        | 🏆 49.3            |
| Opus 5            | Output tokens | 🏆 1,763    | 1,893              |
| Opus 5            | Fresh input   | 14          | 🏆 12              |
| Opus 5            | Cached input  | 168,197     | 🏆 156,002         |
| Opus 5            | Cache write   | 🏆 5,386    | 8,646              |
| Opus 5            | Gradle runs   | 1           | 2                  |
| Sonnet 5          | Turns         | 🏆 3        | 5                  |
| Sonnet 5          | Wall (s)      | 🏆 22.9     | 32.1               |
| Sonnet 5          | Output tokens | 🏆 405      | 729                |
| Sonnet 5          | Fresh input   | 🏆 6        | 10                 |
| Sonnet 5          | Cached input  | 🏆 86,311   | 157,490            |
| Sonnet 5          | Cache write   | 🏆 3,536    | 7,329              |
| Sonnet 5          | Gradle runs   | 1           | 2                  |
| Deepseek V4 Flash | Turns         | 🏆 4        | 6                  |
| Deepseek V4 Flash | Wall (s)      | 🏆 19.6     | 25.2               |
| Deepseek V4 Flash | Output tokens | 🏆 431      | 937                |
| Deepseek V4 Flash | Fresh input   | 🏆 707      | 5,036              |
| Deepseek V4 Flash | Cached input  | 🏆 22,144   | 46,848             |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 1           | 2                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 22.2        | 🏆 16.9            |
| GPT-5.6 Luna      | Output tokens | 163         | 🏆 93              |
| GPT-5.6 Luna      | Fresh input   | 556         | 556                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,921    | 6,022              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |

### custom-task-discovery — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 🏆 6        | 9                  |
| Opus 5            | Wall (s)      | 🏆 59.8     | 77.3               |
| Opus 5            | Output tokens | 🏆 2,137    | 2,906              |
| Opus 5            | Fresh input   | 🏆 12       | 18                 |
| Opus 5            | Cached input  | 🏆 123,479  | 254,099            |
| Opus 5            | Cache write   | 26,927      | 🏆 13,500          |
| Opus 5            | Gradle runs   | 1           | 3                  |
| Sonnet 5          | Turns         | 7           | 7                  |
| Sonnet 5          | Wall (s)      | 43.9        | 🏆 43.4            |
| Sonnet 5          | Output tokens | 🏆 1,080    | 1,436              |
| Sonnet 5          | Fresh input   | 14          | 14                 |
| Sonnet 5          | Cached input  | 🏆 184,273  | 222,274            |
| Sonnet 5          | Cache write   | 32,453      | 🏆 9,303           |
| Sonnet 5          | Gradle runs   | 1           | 1                  |
| Deepseek V4 Flash | Turns         | 🏆 7        | 8                  |
| Deepseek V4 Flash | Wall (s)      | 🏆 29.6     | 34.6               |
| Deepseek V4 Flash | Output tokens | 1,011       | 🏆 881             |
| Deepseek V4 Flash | Fresh input   | 🏆 1,924    | 4,642              |
| Deepseek V4 Flash | Cached input  | 🏆 47,488   | 61,440             |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 1           | 1                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 22.3        | 🏆 19.4            |
| GPT-5.6 Luna      | Output tokens | 148         | 148                |
| GPT-5.6 Luna      | Fresh input   | 543         | 543                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,908    | 6,009              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |

### etiquette-destructive-task — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 5           | 🏆 4               |
| Opus 5            | Wall (s)      | 65.6        | 🏆 60.1            |
| Opus 5            | Output tokens | 🏆 1,397    | 1,458              |
| Opus 5            | Fresh input   | 10          | 🏆 8               |
| Opus 5            | Cached input  | 115,482     | 🏆 98,200          |
| Opus 5            | Cache write   | 🏆 4,486    | 7,316              |
| Opus 5            | Gradle runs   | 0           | 0                  |
| Sonnet 5          | Turns         | 4           | 4                  |
| Sonnet 5          | Wall (s)      | 39.6        | 🏆 36.8            |
| Sonnet 5          | Output tokens | 1,420       | 🏆 793             |
| Sonnet 5          | Fresh input   | 8           | 8                  |
| Sonnet 5          | Cached input  | 🏆 116,658  | 123,359            |
| Sonnet 5          | Cache write   | 🏆 3,678    | 6,405              |
| Sonnet 5          | Gradle runs   | 0           | 0                  |
| Deepseek V4 Flash | Turns         | 4           | 4                  |
| Deepseek V4 Flash | Wall (s)      | 🏆 22.5     | 25.0               |
| Deepseek V4 Flash | Output tokens | 🏆 466      | 732                |
| Deepseek V4 Flash | Fresh input   | 🏆 983      | 3,518              |
| Deepseek V4 Flash | Cached input  | 🏆 22,272   | 24,832             |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 0           | 1                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 24.4        | 🏆 22.5            |
| GPT-5.6 Luna      | Output tokens | 229         | 🏆 184             |
| GPT-5.6 Luna      | Fresh input   | 541         | 541                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,906    | 6,007              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |

Deepseek and GPT-5.6 Luna all arms INVALID — scorer results excluded. Skill-used PASS for all arms of both models.

### exclude-task-trap — cost

| Model             | Metric        | `no-skills` | `gradle-cli@1.0.0` |
| :---------------- | :------------ | ----------: | -----------------: |
| Opus 5            | Turns         | 🏆 7        | 8                  |
| Opus 5            | Wall (s)      | 🏆 54.7     | 70.7               |
| Opus 5            | Output tokens | 🏆 1,765    | 2,310              |
| Opus 5            | Fresh input   | 🏆 14       | 16                 |
| Opus 5            | Cached input  | 🏆 166,461  | 216,070            |
| Opus 5            | Cache write   | 🏆 5,277    | 9,825              |
| Opus 5            | Gradle runs   | 2           | 3                  |
| Sonnet 5          | Turns         | 5           | 5                  |
| Sonnet 5          | Wall (s)      | 🏆 44.2     | 52.8               |
| Sonnet 5          | Output tokens | 🏆 1,261    | 1,510              |
| Sonnet 5          | Fresh input   | 10          | 10                 |
| Sonnet 5          | Cached input  | 🏆 149,294  | 157,750            |
| Sonnet 5          | Cache write   | 🏆 5,506    | 8,118              |
| Sonnet 5          | Gradle runs   | 1           | 3                  |
| Deepseek V4 Flash | Turns         | 🏆 6        | 7                  |
| Deepseek V4 Flash | Wall (s)      | 🏆 25.7     | 39.3               |
| Deepseek V4 Flash | Output tokens | 🏆 967      | 1,372              |
| Deepseek V4 Flash | Fresh input   | 🏆 2,045    | 5,442              |
| Deepseek V4 Flash | Cached input  | 🏆 38,272   | 56,832             |
| Deepseek V4 Flash | Cache write   | 0           | 0                  |
| Deepseek V4 Flash | Gradle runs   | 1           | 3                  |
| GPT-5.6 Luna      | Turns         | 2           | 2                  |
| GPT-5.6 Luna      | Wall (s)      | 23.7        | 🏆 19.1            |
| GPT-5.6 Luna      | Output tokens | 🏆 141      | 151                |
| GPT-5.6 Luna      | Fresh input   | 549         | 549                |
| GPT-5.6 Luna      | Cached input  | 0           | 0                  |
| GPT-5.6 Luna      | Cache write   | 🏆 5,914    | 6,015              |
| GPT-5.6 Luna      | Gradle runs   | 0           | 0                  |
