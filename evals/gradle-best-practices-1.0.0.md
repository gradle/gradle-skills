# Gradle Best Practices Skill v1.0.0 — Benchmark Results

## Summary

`gradle-best-practices@1.0.0` was measured against Claude Haiku 4.5, Sonnet 5 and
Opus 5 on four Gradle build-quality scenarios, two arms each, plus a three-model
A/A control. The treatment arm passed **77 of 105** best-practice checks against
**65 of 105** for the unaided baseline — 20 gains, 8 regressions. On a corrected
reading that discounts three verified scorer artifacts (finding 3), it is
**80 of 105**: 20 gains, 5 regressions.

The effect is concentrated almost entirely in **Sonnet 5**, which goes from 22/35
to **33/35** with **11 gains and zero regressions**, and produces the only folded
`PASS` in the matrix (`tasks`, 12 of 12). **Haiku 4.5 nets +1** (14 → 15) with six
gains against five regressions. **Opus 5 nets zero as measured** (29 → 29) and
**+3 corrected** (29 → 32, three gains and no regressions once the artifacts are
discounted) — it is the strongest model unaided and the skill moves it least.

There is a second, cleaner result that the pass/fail grids understate. The
scenarios also ask each arm to write a `VIOLATIONS.md` inventory before fixing
anything, and **the skill sharply increased what Sonnet and Opus found** — by 1.4× to 2.3× on
every fixture. Sonnet went 8 → 18, 12 → 27 and 13 → 18 issue lines on the three
fixing fixtures; Opus went 19 → 30, 25 → 37 and 30 → 41. The A/A control bounds run-to-run variation on that
count at ±2 lines, so these are far outside noise. Haiku is the exception and
moves the wrong way on one fixture (15 → 7).

**The folded per-scenario outcome carries no signal here and is not the headline.**
These scenarios fold to `PASS` only when every scorer passes, and each fixture
carries nine or more seeded violations, so 3 of 15 comparisons show any outcome
change at all and 23 of 24 delta arms read `FAIL` regardless of the skill. A
`no-skills` arm additionally can never fold to `PASS`, because `skill-used` FAILs
by construction when there is no skill to use. This report is keyed on **checks
passed**; the outcome table is reported for completeness.

---

## Setup

### What we're measuring

Each scenario runs two arms against the same Gradle project and the same prompt:

| Arm                           | Skill                                                      |
| :---------------------------- | :--------------------------------------------------------- |
| `no-skills`                   | Baseline — no skill provided                                |
| `gradle-best-practices@1.0.0` | Local `skills/gradle-best-practices`, `sha256:2e4a645f33fc…` |

All 12 treatment arms received the same skill revision, and the 12 archived copies
of `SKILL.md` are byte-identical to each other. The skill under test is the
**live-fetch** variant: it ships no embedded best-practices catalog and fetches
`docs.gradle.org` on every run. That is directly visible in the tool profiles —
every treatment arm made 4–17 `WebFetch` calls and exactly one `Skill` call; no
baseline arm made any.

The prompts ask the agent to investigate the build, write a `VIOLATIONS.md` with
one issue per line before changing anything, then apply the fixes while keeping
`./gradlew build` green, and record anything left over in `REMAINING-UNFIXED.md`.
`false-positives` is audit-only and forbids edits.

### Models tested

| Model                                 | CLI                   | Short name |
| :------------------------------------ | :-------------------- | :--------- |
| `anthropic/claude-haiku-4-5-20251001` | `claude-code 2.1.233` | Haiku 4.5  |
| `anthropic/claude-sonnet-5`           | `claude-code 2.1.233` | Sonnet 5   |
| `anthropic/claude-opus-5`             | `claude-code 2.1.233` | Opus 5     |

All three are Anthropic models on `claude-code`. This benchmark carries **no
cross-vendor or cross-CLI signal** (finding 8).

### Scenarios and fixtures

| Scenario          | Fixture               | Checks | Seeded-violation floor | What it probes |
| :---------------- | :-------------------- | -----: | ---------------------: | :------------- |
| `structure`       | `sample-carlog`       | 10     | 10 | Build layout: settings, version catalog, repository placement, convention plugins, lazy wiring |
| `tasks`           | `sample-star-charter` | 12     | 10 | Custom task types: caching, path sensitivity, configuration cache, catalog naming |
| `idioms`          | `sample-recipe-vault` | 11     |  9 | Script idioms: `apply plugin`, `afterEvaluate`, internal APIs, properties placement, config-time work |
| `false-positives` | `sample-init-library` |  2     |  — | Restraint on untouched `gradle init` output — audit only, no edits |
| `aa`              | `sample-carlog`       | 10     | 10 | A/A control: two identical `no-skills` arms, same fixture and prompt as `structure` |

Check counts exclude `skill-used`. `aa` runs no treatment arm and contributes no
checks to the totals.

### Scorers

Every scenario carries a `skill-used` scorer plus task-specific checks. Most are
`file-exists` greps over comment-stripped copies of the build sources. Four are
behavioural or structural probes worth calling out, because they are where the
interesting failures live:

- **`lazy-extension-wiring`** (`structure`) — not a regex. An init script
  reconfigures the `carLog` extension in `gradle.afterProject`, after every build
  script has evaluated, then runs `recordDemoMaintenance`. Lazy wiring picks the
  new value up and writes the probe file; eager `.get()` at configuration time
  does not. Fix-shape agnostic: `map`/`flatMap`, provider pass-through and
  action-time `.get()` all pass.
- **`convention-plugins`** (`structure`) — requires the whole chain: an included
  build, a *precompiled script plugin* inside it (a `*.gradle[.kts]` under
  `src/main/` whose filename is the plugin id), and a main-build script that
  applies that id. **It does not recognise binary convention plugins** declared
  through `gradlePlugin { … implementationClass … }` (finding 3).
- **`tasks-documented`** (`tasks`) — harvests script-defined task names, then runs
  `./gradlew tasks --all` and demands every harvested name Gradle lists carry a
  description. **Its harvest regex matches `tasks.register(` but not Java's
  `project.getTasks().register(`** (finding 3).
- **`violations-count`** (all three fixing scenarios) — a one-sided recall floor:
  the `VIOLATIONS.md` the prompt mandates must hold at least as many non-blank
  lines as the fixture plants. Over-reporting passes; under-reporting fails.

### Outcome definitions

| Outcome        | Meaning |
| :------------- | :------ |
| ✅ **PASS**    | The scorer's criterion was met. |
| ❌ **FAIL**    | The trial ran and the criterion was not met. |
| 🚧 **LIMIT**   | The arm was cut off by a resource cap. Scorer verdicts stand; cost figures are lower bounds. |
| ⚠️ **INVALID** | The scorer could not render a verdict. No arm in this sweep returned INVALID. |

---
## Key findings

### 1. Sonnet 5 is where the skill pays off — 11 gains, zero regressions
Sonnet goes 22 → 33 of 35, improving on all three fixing scenarios (+3 `structure`,
+4 `tasks`, +4 `idioms`) and regressing nowhere. Its `tasks` treatment arm is the
only arm in the whole matrix to fold to `PASS`: 12 of 12. The archived tree shows
why — it added `@CacheableTask`, gave every registered task a `group` and
`description`, replaced `.cacheIf` and `configurations.all`, and wired
`inputs.files(configurations.runtimeClasspath)` lazily, all inside
`lib/build.gradle.kts`. Unaided, the same model manages 8 of 12.

### 2. The strongest and most consistent effect is on detection, not on fixes
Every fixing prompt mandates a `VIOLATIONS.md` inventory. The skill raises it by
1.4× to 2.3× for the two larger models, on every fixture:

| Scenario | Floor | Haiku base → treat | Sonnet base → treat | Opus base → treat |
| :------- | ----: | -----------------: | ------------------: | ----------------: |
| `structure` | 10 | 15 → **7** | 13 → **18** | 30 → **41** |
| `tasks`     | 10 |  8 → **7** | 12 → **27** | 25 → **37** |
| `idioms`    |  9 |  7 → **9** |  8 → **18** | 19 → **30** |

The A/A control bounds this: two identical unaided arms on `sample-carlog`
produced 9 vs 9 lines (Haiku), 13 vs 11 (Sonnet) and 23 vs 25 (Opus) — a ±2 band.
Sonnet's +5/+15/+10 and Opus's +11/+12/+11 are an order of magnitude outside it.
This is the clearest positive result in the evaluation, and the `violations-count`
scorer only registers part of it because it is a one-sided floor: Opus clears the
floor in both arms, so tripling its recall scores nothing.

### 3. All three of Opus's regressions are scorer artifacts, not defects
Every Opus regression was opened and checked against the archived tree. All three
are cases where Opus did the **more** idiomatic thing and the scorer could not see
it. Opus's measured net of zero is a scorer limitation as much as a null result.

- **`structure` / `convention-plugins`.** Opus replaced `buildSrc`'s Groovy
  precompiled script plugins with a `build-logic` composite build exposing two
  **binary** plugins — `gradlePlugin { register("javaLibraryConventions") { id =
  "carlog.java-library-conventions"; implementationClass =
  "…JavaLibraryConventionsPlugin" } }` — and `carlog/build.gradle.kts` applies both
  ids. `convention-plugins.sh` only recognises precompiled *script* plugins
  (a `*.gradle[.kts]` under `src/main/`), so it reports "no precompiled script
  plugin found". The chain is complete and the build compiles and applies it —
  `project-builds` passes. On a corrected reading this is **PASS**.
- **`tasks` / `tasks-documented`.** Opus extracted its three custom tasks into a
  Java convention plugin and set `setGroup(…)` and `setDescription(…)` on every
  one of them. The harvest regex anchors on `tasks.register(` and does not match
  `project.getTasks().register(`, so it harvested zero names and failed by the
  zero-names rule — while the tasks were, in fact, documented. On a corrected
  reading this is **PASS**. Note the contrast with finding 1: Sonnet scored 12/12
  partly because it left the tasks in a Kotlin build script, where the regex works.
- **`idioms` / `no-subproject-properties`.** Opus moved shared logic into
  `includeBuild("build-logic")` and gave that build its own `gradle.properties`,
  with a comment explaining that Gradle properties are not inherited across build
  boundaries — which is correct. The scorer forbids any file matching
  `.+/gradle\.properties`, which matches an included build's *root* as readily as
  a subproject's. On a corrected reading this is **PASS**.

Corrected, Opus reads 29 → 32: three gains, no regressions.

### 4. The one regression that reproduced across models does not survive inspection
`idioms` / `no-subproject-properties` failed in both Haiku's and Opus's treatment
arms, which is the aggregator's strongest negative flag. The two have nothing in
common. Opus's is the artifact above. **Haiku's is real, and worse than the single
scorer suggests**: its treatment arm deleted the root `gradle.properties`
altogether and left a single `core/gradle.properties` behind. That one move flipped
`no-subproject-properties` *and* `build-cache-enabled` (which reads
`org.gradle.caching=true` from the root file), and is two of Haiku's five
regressions. There is no cross-model signal that the skill encourages
per-subproject properties files.

### 5. Haiku 4.5 gains and loses in roughly equal measure, and cuts corners
Six gains against five regressions, net +1 of 35. Two regressions are the
`gradle.properties` deletion above. Two more are **failures to act**: on `tasks`,
the baseline removed the seeded `google()` repository from `settings.gradle.kts`
and renamed the deliberately opaque catalog entries (`stuff`, `utils`, `theJson`,
`gv`), and the treatment arm left both exactly as the fixture ships them. The
fifth is `structure`/`violations-count`: Haiku's report went from 15 lines to 7,
below the fixture's floor of 10, while it also spent 33 turns to the
baseline's 85 and under a third of the cached input. The skill broadens what Haiku looks at and appears to
crowd out defects it catches unaided.

### 6. `false-positives` cannot be won as configured, and produced no signal
`only-defensible-findings` FAILs in all six arms. The scorer allows exactly two
findings on untouched `gradle init` output — repositories declared outside
settings, and `@Incubating` API use — and every arm reported more. But the single
most-reported "false positive", present in **all six** arms, is the wrapper's
`distributionUrl`, and that line is **harness scaffolding**: the fixture ships
`https://services.gradle.org/distributions/gradle-9.5.0-bin.zip` and the container
rewrites it to `file:///opt/dists/gradle-9.5.0-bin.zip` so the build runs offline.
The agents are correctly flagging a genuinely anomalous line that the fixture's
author never wrote.

| Model | Arm | Lines reported | Harness wrapper lines | Allowlisted | Residual |
| :---- | :-- | -------------: | --------------------: | ----------: | -------: |
| Haiku 4.5 | baseline | 3 | 1 | 0 | 2 |
| Haiku 4.5 | treatment | 3 | 1 | 1 | 1 |
| Sonnet 5 | baseline | 7 | 3 | 1 | 3 |
| Sonnet 5 | treatment | 5 | 2 | 1 | 2 |
| Opus 5 | baseline | 2 | 1 | 0 | 1 |
| Opus 5 | treatment | 6 | 3 | 1 | 2 |

Even discounting the wrapper lines entirely, no arm passes, so the corrected
reading is the same null: the skill neither reduced nor caused false positives
here. Two smaller observations: all three treatment arms reported the
repositories finding and only one baseline did, and **no arm in either condition
reported the `@Incubating` finding** the generated headers announce.

### 7. The skill is not free
Across the 24 delta arms it adds output tokens (269,038 → 523,855, +95%), cached
input (20.9M → 28.3M, +35%) and cache writes (640,873 → 2,572,928, 4.0×), driven
by the skill text plus 4–17 fetched documentation pages entering the context.
**Two arms blew the 5M token cap outright** — `idioms`/Sonnet and
`structure`/Opus, both treatment — and a third, `idioms`/Opus, reached 70% of both
the token and wall-clock budgets. Haiku is the exception: its treatment arms were
*cheaper* on turns (189 → 159) and cached input (7.3M → 4.7M), which finding 5
suggests is a symptom rather than an efficiency.

### 8. No cross-vendor coverage
All three models are Anthropic on `claude-code`. Nothing here speaks to how the
skill behaves on another vendor or CLI.

### 9. n = 1 per arm, but the noise floor is measured
Single trials throughout. Unlike the `gradle-cli` benchmark, what that implies is
quantified rather than assumed — see [Noise floor](#noise-floor), including which
specific claims it does *not* cover.

---
## Summary tables

### Checks passed (excluding `skill-used`)

Artifact-corrected columns apply finding 3 and are marked ‡. `false-positives`
contributes 1/2 in every arm and never moves.

| Model | Scenario | `no-skills` | `gradle-best-practices@1.0.0` | Δ | Corrected ‡ |
| :---- | :------- | ----------: | ----------------------------: | --: | ----------: |
| Haiku 4.5 | `structure`       | 3 / 10 | 4 / 10 | +1 | — |
| Haiku 4.5 | `tasks`           | 5 / 12 | 5 / 12 |  0 | — |
| Haiku 4.5 | `idioms`          | 5 / 11 | 5 / 11 |  0 | — |
| Haiku 4.5 | `false-positives` | 1 / 2  | 1 / 2  |  0 | — |
| **Haiku 4.5** | **total**    | **14 / 35** | **15 / 35** | **+1** | **15 / 35** |
| Sonnet 5 | `structure`       | 6 / 10 | 9 / 10 | +3 | — |
| Sonnet 5 | `tasks`           | 8 / 12 | 12 / 12 | +4 | — |
| Sonnet 5 | `idioms`          | 7 / 11 | 11 / 11 | +4 | — |
| Sonnet 5 | `false-positives` | 1 / 2  | 1 / 2  |  0 | — |
| **Sonnet 5** | **total**     | **22 / 35** | **33 / 35** | **+11** | **33 / 35** |
| Opus 5 | `structure`       | 8 / 10 | 8 / 10 |  0 | 9 / 10 ‡ |
| Opus 5 | `tasks`           | 11 / 12 | 10 / 12 | −1 | 11 / 12 ‡ |
| Opus 5 | `idioms`          | 9 / 11 | 10 / 11 | +1 | 11 / 11 ‡ |
| Opus 5 | `false-positives` | 1 / 2  | 1 / 2  |  0 | — |
| **Opus 5** | **total**       | **29 / 35** | **29 / 35** | **0** | **32 / 35 ‡** |
| **All** | **total**        | **65 / 105** | **77 / 105** | **+12** | **80 / 105 ‡** |

| Model | Baseline | Treatment | Gains | Regressions | Corrected treatment ‡ |
| :---- | -------: | --------: | ----: | ----------: | --------------------: |
| Haiku 4.5 | 14 | **15** | 6 | 5 | 15 (6 gains, 5 regressions) |
| Sonnet 5  | 22 | **33** | 11 | 0 | 33 (11 gains, 0 regressions) |
| Opus 5    | 29 | **29** | 3 | 3 | **32** (3 gains, 0 regressions) |
| **Total** | **65** | **77** | **20** | **8** | **80** (20 gains, 5 regressions) |

### Folded outcome (reported for completeness)

Only 3 of 15 comparisons move, and no baseline arm can fold to `PASS` because
`skill-used` FAILs by construction without a skill. Read the per-check grids.

| Model | Scenario | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :------- | :---------: | :---------------------------: |
| Haiku 4.5 | `structure`       | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `tasks`           | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `idioms`          | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `false-positives` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `aa`              | ❌ FAIL | ❌ FAIL (second unaided arm) |
| Sonnet 5 | `structure`       | ❌ FAIL | ❌ FAIL |
| Sonnet 5 | `tasks`           | ❌ FAIL | ✅ **PASS** |
| Sonnet 5 | `idioms`          | ❌ FAIL | 🚧 **LIMIT (tokens)** |
| Sonnet 5 | `false-positives` | ❌ FAIL | ❌ FAIL |
| Sonnet 5 | `aa`              | ❌ FAIL | ❌ FAIL (second unaided arm) |
| Opus 5 | `structure`       | ❌ FAIL | 🚧 **LIMIT (tokens)** |
| Opus 5 | `tasks`           | ❌ FAIL | ❌ FAIL |
| Opus 5 | `idioms`          | ❌ FAIL | ❌ FAIL |
| Opus 5 | `false-positives` | ❌ FAIL | ❌ FAIL |
| Opus 5 | `aa`              | ❌ FAIL | ❌ FAIL (second unaided arm) |

### Skill pickup

| Model | Consulted the skill | Evidence |
| :---- | :-----------------: | :------- |
| Haiku 4.5 | 4 / 4 | 1 `Skill` call and 5–17 `WebFetch` calls per treatment arm |
| Sonnet 5  | 4 / 4 | 1 `Skill` call and 4–9 `WebFetch` calls per treatment arm |
| Opus 5    | 4 / 4 | 1 `Skill` call and 6–8 `WebFetch` calls per treatment arm |

`skill-used` PASSed on all 12 treatment arms and FAILed on all 12 baseline arms.
No comparison in this sweep is void for non-pickup. No baseline arm made a single
`WebFetch` call, so the fetched-catalog behaviour is attributable to the skill.

---

## Noise floor

The `aa` control runs two identical `no-skills` arms on `sample-carlog` with the
`structure` prompt — the same fixture, the same prompt (modulo YAML whitespace
round-tripping) and the same ten scorers. It measures **run-to-run variation of
the agent on the same task**, which is exactly what a single-trial delta must
clear.

| Model | Scorers disagreeing between two identical arms | Which |
| :---- | :--------------------------------------------: | :---- |
| Haiku 4.5 | 1 / 10 | `lazy-extension-wiring` |
| Sonnet 5  | 2 / 10 | `repos-not-in-build-scripts`, `no-eager-getbyname` |
| Opus 5    | 0 / 10 | — |

Detection count over the same pairs: 9 vs 9 (Haiku), 13 vs 11 (Sonnet), 23 vs 25
(Opus) — a ±2 band.

**What this covers, and what it does not.**

- Sonnet's +11 and Haiku's six gains / five regressions are aggregate movements
  far outside a 0–2 scorer band. The aggregate readings are safe.
- **Two of the six `structure` gains sit on scorers the control found unstable.**
  `lazy-extension-wiring` (gained by Opus and Sonnet) is the scorer Haiku's A/A
  flipped; `repos-not-in-build-scripts` (gained by Haiku) is one Sonnet's A/A
  flipped. Treat those three individual flips as directional.
- The `structure` control does **not** transfer to `tasks`, `idioms` or
  `false-positives`: different fixtures, different scorers, no A/A was run on any
  of them. Sonnet's +4 on `tasks` and +4 on `idioms`, and every claim about the
  `sample-star-charter` and `sample-recipe-vault` scorers, are uncontrolled.
- The control says nothing about the three artifacts in finding 3. Those are
  deterministic scorer blind spots, not noise; they reproduce on any run that
  writes a binary convention plugin, a Java task registration, or an included
  build with its own properties file.

---
## Results by scenario

### structure

**Prompt:** This Gradle build succeeds, but it probably has issues with things not done in the proper way. Investigate the build configuration and fix what you find, making sure `./gradlew build` still succeeds. … This is NOT just an audit, your task is to apply fixes to the build. Before fixing anything, write a file named `VIOLATIONS.md` … one line per issue … Then apply your fixes. … Before finishing, re-read your `VIOLATIONS.md` and either fix each item or record why not in a `REMAINING-UNFIXED.md` file.
**Fixture:** `sample-carlog` (`sha256:624f1d41fe05…`), 10 seeded violations
**Key checks:** root project named in settings; version catalog present; repositories declared in settings rather than build scripts; no eager `getByName`; no `dependsOn`; lazy extension wiring (behavioural probe); no sources in the root project; convention plugins wired end to end; detection floor of 10.

| Model | Check | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :---- | :---------: | :---------------------------: |
| Haiku 4.5 | `project-builds` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `root-project-named` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `version-catalog` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `repos-not-in-build-scripts` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `no-eager-getbyname` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `no-dependson` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `lazy-extension-wiring` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-source-in-root` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `convention-plugins` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `violations-count` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |
| Sonnet 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `root-project-named` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `version-catalog` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `repos-not-in-build-scripts` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `no-eager-getbyname` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `no-dependson` | ❌ FAIL | ❌ FAIL |
| Sonnet 5 | `lazy-extension-wiring` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-source-in-root` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `convention-plugins` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `violations-count` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |
| Opus 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Opus 5 | `root-project-named` | ✅ PASS | ✅ PASS |
| Opus 5 | `version-catalog` | ✅ PASS | ✅ PASS |
| Opus 5 | `repos-not-in-build-scripts` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-eager-getbyname` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-dependson` | ❌ FAIL | ❌ FAIL |
| Opus 5 | `lazy-extension-wiring` | ❌ FAIL | ✅ PASS |
| Opus 5 | `no-source-in-root` | ✅ PASS | ✅ PASS |
| Opus 5 | `convention-plugins` | ✅ PASS | ❌ FAIL |
| Opus 5 | `violations-count` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Opus 5 | **outcome** | ❌ **FAIL** | 🚧 **LIMIT (tokens)** |

**Signal:** Sonnet is the clear winner at +3, taking both structural probes — it moved the root project's sources into subprojects and created `build-logic/src/main/groovy/carlog.java-conventions.gradle` and `carlog.maintenance-log.gradle`, where its baseline had neither. Opus reads flat at 8/10, but that is the artifact in finding 3: its treatment arm built two *binary* convention plugins that `convention-plugins.sh` cannot see, so a correct and arguably better refactor scores as a break. Corrected, Opus is +1. Haiku picks up the two cheap textual checks and regresses on `violations-count` — 15 issue lines down to 7, under the floor of 10 — after spending under 40% of the turns its baseline did. `no-dependson` fails in all six arms: no model removes task `dependsOn` wiring with or without the skill. Opus's treatment arm hit the 5M token cap; its scorer verdicts stand and its cost figures are lower bounds.

---

### tasks

**Prompt:** As `structure`, against a project whose custom task types carry caching and input-normalisation defects. This scenario's prompt omits the "This is NOT just an audit" line the other two fixing prompts carry — uniformly across all three models, so the comparison is unaffected (see Methodology).
**Fixture:** `sample-star-charter` (`sha256:88676a5a66f6…`), 10 seeded violations
**Key checks:** every script-defined task documented (`gradle tasks --all` probe); no `PathSensitivity.ABSOLUTE`; `@CacheableTask` present; no `.cacheIf`; no configuration-cache opt-out; no `runtimeClasspath.get()`; `google()` removed from settings; no `configurations.all`; configuration attributes set; catalog entries meaningfully named; detection floor of 10.

| Model | Check | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :---- | :---------: | :---------------------------: |
| Haiku 4.5 | `project-builds` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `tasks-documented` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-absolute-sensitivity` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `cacheable-annotation` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-cacheif` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-cc-optout` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `lazy-classpath` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `google-repo-removed` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `no-configurations-all` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `configuration-attributes` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `catalog-entries-named` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `violations-count` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |
| Sonnet 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `tasks-documented` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-absolute-sensitivity` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `cacheable-annotation` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-cacheif` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-cc-optout` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `lazy-classpath` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `google-repo-removed` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `no-configurations-all` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `configuration-attributes` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `catalog-entries-named` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `violations-count` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | **outcome** | ❌ **FAIL** | ✅ **PASS** |
| Opus 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Opus 5 | `tasks-documented` | ✅ PASS | ❌ FAIL |
| Opus 5 | `no-absolute-sensitivity` | ✅ PASS | ✅ PASS |
| Opus 5 | `cacheable-annotation` | ❌ FAIL | ❌ FAIL |
| Opus 5 | `no-cacheif` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-cc-optout` | ✅ PASS | ✅ PASS |
| Opus 5 | `lazy-classpath` | ✅ PASS | ✅ PASS |
| Opus 5 | `google-repo-removed` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-configurations-all` | ✅ PASS | ✅ PASS |
| Opus 5 | `configuration-attributes` | ✅ PASS | ✅ PASS |
| Opus 5 | `catalog-entries-named` | ✅ PASS | ✅ PASS |
| Opus 5 | `violations-count` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Opus 5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |

**Signal:** The strongest single result in the sweep and the only folded `PASS`. Sonnet goes 8 → 12 of 12, adding `@CacheableTask`, descriptions on every registered task, and lazy classpath wiring. Opus's −1 is the `tasks-documented` harvest artifact (finding 3): it documented all three tasks, in Java, in a convention plugin the regex cannot read — corrected, 11 → 11. Haiku is flat at 5/12 but the composition changed: it gained `no-absolute-sensitivity` and `configuration-attributes` while *losing* two seeded defects its baseline had fixed — `google()` stayed in `settings.gradle.kts` and the opaque catalog entries `stuff`, `utils`, `theJson` and `gv` were left exactly as the fixture ships them. `cacheable-annotation` fails in both Haiku arms and both Opus arms.

---

### idioms

**Prompt:** As `structure`.
**Fixture:** `sample-recipe-vault` (`sha256:edc64794f43e…`), 9 seeded violations
**Key checks:** `plugins {}` rather than `apply plugin`; no `afterEvaluate`; no `org.gradle.internal` APIs; build cache enabled in the root `gradle.properties`; UTF-8 pinned in `org.gradle.jvmargs`; no `gradle.properties` outside the build root; no `group:name:version` map-form GAVs; no empty container project; no configuration-time file hashing (behavioural probe); detection floor of 9.

| Model | Check | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :---- | :---------: | :---------------------------: |
| Haiku 4.5 | `project-builds` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `plugins-block-only` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-after-evaluate` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `no-internal-apis` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `build-cache-enabled` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `utf8-in-jvmargs` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-subproject-properties` | ✅ PASS | ❌ FAIL |
| Haiku 4.5 | `single-gav-strings` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `no-empty-project` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `no-config-time-hashing` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `violations-count` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |
| Sonnet 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `plugins-block-only` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-after-evaluate` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `no-internal-apis` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `build-cache-enabled` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `utf8-in-jvmargs` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-subproject-properties` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `single-gav-strings` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `no-empty-project` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `no-config-time-hashing` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `violations-count` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | **outcome** | ❌ **FAIL** | 🚧 **LIMIT (tokens)** |
| Opus 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Opus 5 | `plugins-block-only` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-after-evaluate` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-internal-apis` | ✅ PASS | ✅ PASS |
| Opus 5 | `build-cache-enabled` | ✅ PASS | ✅ PASS |
| Opus 5 | `utf8-in-jvmargs` | ❌ FAIL | ✅ PASS |
| Opus 5 | `no-subproject-properties` | ✅ PASS | ❌ FAIL |
| Opus 5 | `single-gav-strings` | ✅ PASS | ✅ PASS |
| Opus 5 | `no-empty-project` | ❌ FAIL | ✅ PASS |
| Opus 5 | `no-config-time-hashing` | ✅ PASS | ✅ PASS |
| Opus 5 | `violations-count` | ✅ PASS | ✅ PASS |
| Opus 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Opus 5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |

**Signal:** Sonnet takes every check, 7 → 11 of 11, and is the only arm in the sweep to clear a fixture completely on the non-`skill-used` checks — though it hit the 5M token cap doing so, which caps its outcome at `LIMIT` and makes its cost a lower bound. Opus is +1 as measured and +2 corrected: `no-subproject-properties` fails only because it gave its `build-logic` composite the properties file that composite genuinely needs (finding 3). Haiku is flat at 5/11 with two gains and two regressions, and both regressions trace to one action — deleting the root `gradle.properties` and leaving `core/gradle.properties` in its place, which took out `build-cache-enabled` with it. `plugins-block-only`, `utf8-in-jvmargs`, `no-empty-project` and `no-config-time-hashing` all still fail in both Haiku arms.

---

### false-positives

**Prompt:** … Investigate the build configuration and report what you find, **NOT changing any existing file**. This is ONLY an audit … If you discover no issues, write an empty `VIOLATIONS.md`.
**Fixture:** `sample-init-library` (`sha256:e5667ae0b78a…`) — untouched `gradle init` output, no seeded violations
**Key checks:** the build still builds; every reported finding is one of the two defensible on `gradle init` output (repositories outside settings, `@Incubating` API use).

| Model | Check | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :---- | :---------: | :---------------------------: |
| Haiku 4.5 | `project-builds` | ✅ PASS | ✅ PASS |
| Haiku 4.5 | `only-defensible-findings` | ❌ FAIL | ❌ FAIL |
| Haiku 4.5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Haiku 4.5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |
| Sonnet 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Sonnet 5 | `only-defensible-findings` | ❌ FAIL | ❌ FAIL |
| Sonnet 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Sonnet 5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |
| Opus 5 | `project-builds` | ✅ PASS | ✅ PASS |
| Opus 5 | `only-defensible-findings` | ❌ FAIL | ❌ FAIL |
| Opus 5 | `skill-used` | ❌ FAIL | ✅ PASS |
| Opus 5 | **outcome** | ❌ **FAIL** | ❌ **FAIL** |

**Signal:** No signal, and the scenario cannot currently produce one — see finding 6. Every arm fails `only-defensible-findings`, and the most-reported "false positive" in all six is the wrapper `distributionUrl` the harness itself rewrote to a `file://` path. `project-builds` passes everywhere, which is the audit-only prompt being obeyed. The one thing the grid does show is pickup: `skill-used` is the sole scorer that moves, in all three models.

---
## Cost & Efficiency

> **Token accounting note:** the Inspect harness uses Anthropic prompt caching for
> all three models. "Fresh input" are non-cached tokens added on top of the cached
> prefix. "Cached input" is served from the prompt cache at ~10% of the standard
> input rate; "Cache write" is billed at 125%. Wall clock is `adjusted_wall_clock`
> in seconds — the agent's active time, minus harness overhead.
>
> **Reading the 🏆:** it marks the cheaper of the two arms for that model and
> metric; lower is better everywhere. ✅ ❌ 🚧 are reserved for scorer verdicts and
> never appear here. Ties are unmarked. **A bounded arm is never marked and its
> figures carry `≥`** — it was cut off, so its cost is a floor, not a measurement.
>
> **`Gradle runs` is never marked and should not be read as a cost.** The counter
> recognises a bare `./gradlew` and misses prefixed forms; it reads 0 in six arms,
> four of them Opus treatment arms that demonstrably restructured a build and left
> it green. See known gap 4.
>
> **One confound is unquantifiable from this data.** Arms ran strictly
> sequentially, so one arm warms the shared prompt prefix the next one reads, but
> the archived reports do not record arm order. The dominant driver of the
> treatment's cache-write increase is visible directly in the tool profiles: the
> skill text plus 4–17 fetched documentation pages entering the context.

### structure — cost

| Model | Metric | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :----- | ----------: | ----------------------------: |
| Haiku 4.5 | Turns | 85 | 🏆 33 |
| Haiku 4.5 | Wall (s) | 338.7 | 🏆 168.2 |
| Haiku 4.5 | Output tokens | 19,964 | 🏆 8,318 |
| Haiku 4.5 | Fresh input | 436 | 🏆 154 |
| Haiku 4.5 | Cached input | 3,438,246 | 🏆 1,009,263 |
| Haiku 4.5 | Cache write | 🏆 74,444 | 111,606 |
| Haiku 4.5 | Gradle runs | 14 | 8 |
| Sonnet 5 | Turns | 🏆 37 | 48 |
| Sonnet 5 | Wall (s) | 🏆 458.6 | 637.2 |
| Sonnet 5 | Output tokens | 🏆 27,895 | 57,349 |
| Sonnet 5 | Fresh input | 🏆 74 | 87 |
| Sonnet 5 | Cached input | 🏆 2,265,796 | 3,474,255 |
| Sonnet 5 | Cache write | 🏆 82,328 | 282,662 |
| Sonnet 5 | Gradle runs | 2 | 3 |
| Opus 5 | Turns | 28 | ≥ 48 |
| Opus 5 | Wall (s) | 524.7 | ≥ 1,480.1 |
| Opus 5 | Output tokens | 33,868 | ≥ 89,684 |
| Opus 5 | Fresh input | 56 | ≥ 98 |
| Opus 5 | Cached input | 1,594,905 | ≥ 4,635,215 |
| Opus 5 | Cache write | 79,642 | ≥ 321,437 |
| Opus 5 | Gradle runs | 3 | 0 |

### tasks — cost

| Model | Metric | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :----- | ----------: | ----------------------------: |
| Haiku 4.5 | Turns | 🏆 38 | 48 |
| Haiku 4.5 | Wall (s) | 🏆 212.7 | 269.3 |
| Haiku 4.5 | Output tokens | 🏆 9,329 | 13,850 |
| Haiku 4.5 | Fresh input | 🏆 195 | 204 |
| Haiku 4.5 | Cached input | 1,330,120 | 🏆 1,043,579 |
| Haiku 4.5 | Cache write | 🏆 22,581 | 217,306 |
| Haiku 4.5 | Gradle runs | 9 | 6 |
| Sonnet 5 | Turns | 46 | 🏆 42 |
| Sonnet 5 | Wall (s) | 🏆 483.3 | 640.4 |
| Sonnet 5 | Output tokens | 🏆 32,671 | 66,298 |
| Sonnet 5 | Fresh input | 92 | 🏆 77 |
| Sonnet 5 | Cached input | 🏆 2,551,107 | 3,031,763 |
| Sonnet 5 | Cache write | 🏆 50,991 | 258,894 |
| Sonnet 5 | Gradle runs | 6 | 7 |
| Opus 5 | Turns | 🏆 44 | 52 |
| Opus 5 | Wall (s) | 🏆 1,037.6 | 1,182.4 |
| Opus 5 | Output tokens | 🏆 44,564 | 80,814 |
| Opus 5 | Fresh input | 🏆 88 | 104 |
| Opus 5 | Cached input | 🏆 2,823,907 | 4,008,942 |
| Opus 5 | Cache write | 🏆 93,454 | 285,732 |
| Opus 5 | Gradle runs | 4 | 0 |

### idioms — cost

| Model | Metric | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :----- | ----------: | ----------------------------: |
| Haiku 4.5 | Turns | 🏆 52 | 60 |
| Haiku 4.5 | Wall (s) | 🏆 250.6 | 285.8 |
| Haiku 4.5 | Output tokens | 🏆 9,323 | 16,709 |
| Haiku 4.5 | Fresh input | 🏆 255 | 288 |
| Haiku 4.5 | Cached input | 🏆 2,162,459 | 2,220,448 |
| Haiku 4.5 | Cache write | 🏆 47,701 | 142,896 |
| Haiku 4.5 | Gradle runs | 9 | 8 |
| Sonnet 5 | Turns | 37 | ≥ 58 |
| Sonnet 5 | Wall (s) | 405.4 | ≥ 885.9 |
| Sonnet 5 | Output tokens | 27,025 | ≥ 71,300 |
| Sonnet 5 | Fresh input | 74 | ≥ 110 |
| Sonnet 5 | Cached input | 1,872,325 | ≥ 4,674,341 |
| Sonnet 5 | Cache write | 44,360 | ≥ 310,494 |
| Sonnet 5 | Gradle runs | 6 | 0 |
| Opus 5 | Turns | 🏆 31 | 46 |
| Opus 5 | Wall (s) | 🏆 487.8 | 1,253.9 |
| Opus 5 | Output tokens | 🏆 28,260 | 65,901 |
| Opus 5 | Fresh input | 🏆 62 | 92 |
| Opus 5 | Cached input | 🏆 1,387,384 | 3,136,756 |
| Opus 5 | Cache write | 🏆 43,124 | 307,335 |
| Opus 5 | Gradle runs | 4 | 0 |

### false-positives — cost

| Model | Metric | `no-skills` | `gradle-best-practices@1.0.0` |
| :---- | :----- | ----------: | ----------------------------: |
| Haiku 4.5 | Turns | 🏆 14 | 18 |
| Haiku 4.5 | Wall (s) | 🏆 75.5 | 124.2 |
| Haiku 4.5 | Output tokens | 🏆 2,956 | 4,836 |
| Haiku 4.5 | Fresh input | 77 | 🏆 73 |
| Haiku 4.5 | Cached input | 🏆 335,723 | 389,291 |
| Haiku 4.5 | Cache write | 🏆 23,303 | 84,045 |
| Haiku 4.5 | Gradle runs | 1 | 1 |
| Sonnet 5 | Turns | 🏆 8 | 14 |
| Sonnet 5 | Wall (s) | 🏆 142.5 | 230.0 |
| Sonnet 5 | Output tokens | 🏆 7,139 | 17,245 |
| Sonnet 5 | Fresh input | 🏆 16 | 24 |
| Sonnet 5 | Cached input | 🏆 262,080 | 387,462 |
| Sonnet 5 | Cache write | 🏆 12,223 | 95,747 |
| Sonnet 5 | Gradle runs | 0 | 0 |
| Opus 5 | Turns | 32 | 🏆 13 |
| Opus 5 | Wall (s) | 440.9 | 🏆 306.9 |
| Opus 5 | Output tokens | 🏆 26,044 | 31,551 |
| Opus 5 | Fresh input | 64 | 🏆 26 |
| Opus 5 | Cached input | 921,033 | 🏆 267,492 |
| Opus 5 | Cache write | 🏆 66,722 | 154,774 |
| Opus 5 | Gradle runs | 1 | 0 |

### Where the skill costs, and where it pays

Totals across the 24 delta arms (the two bounded treatment arms are included, so
every treatment figure is a floor):

| Model | Metric | `no-skills` | `gradle-best-practices@1.0.0` | Ratio |
| :---- | :----- | ----------: | ----------------------------: | ----: |
| Haiku 4.5 | Turns | 189 | 159 | 0.84× |
| Haiku 4.5 | Output tokens | 41,572 | 43,713 | 1.05× |
| Haiku 4.5 | Cached input | 7,266,548 | 4,662,581 | 0.64× |
| Haiku 4.5 | Cache write | 168,029 | 555,853 | 3.31× |
| Sonnet 5 | Turns | 128 | 162 | 1.27× |
| Sonnet 5 | Output tokens | 94,730 | 212,192 | 2.24× |
| Sonnet 5 | Cached input | 6,951,308 | 11,567,821 | 1.66× |
| Sonnet 5 | Cache write | 189,902 | 947,797 | 4.99× |
| Opus 5 | Turns | 135 | 159 | 1.18× |
| Opus 5 | Output tokens | 132,736 | 267,950 | 2.02× |
| Opus 5 | Cached input | 6,727,229 | 12,048,405 | 1.79× |
| Opus 5 | Cache write | 282,942 | 1,069,278 | 3.78× |

The skill roughly **doubles output tokens on the two larger models** and multiplies
cache writes three- to fivefold, and two arms exceeded the 5M token cap outright.
Some of that buys measurable work: Sonnet's +11 checks and its 2–2.3× larger
violation inventories come with a 2.24× output-token bill, which on a build-quality
audit is a reasonable trade. Opus pays a comparable multiple for three
corrected gains and inventories 1.4–1.6× longer.

Haiku is the one place where the skill is *cheaper* — 0.84× turns, 0.64× cached
input — and finding 5 argues this is not efficiency. Its `structure` treatment arm
spent 33 turns to the baseline's 85 and 1.0M cached-input tokens to the baseline's
3.4M, and reported 7 violations to the baseline's 15.
Read the cost saving there together with the scorer row, not on its own.

---

## Methodology and known gaps

**Trials.** n = 1 per arm. 15 runs, 30 arms: 4 delta scenarios × 3 models × 2 arms,
plus 3 A/A runs × 2 identical arms. About 4.4 hours of arm time in total. Runs were
strictly sequential, so wall-clock and token figures are not distorted by
concurrency.

**Toolchain.** `claude-code 2.1.233`, JDK 21, Gradle 9.5.0, `resources: small`,
network on. Every arm ran against a pinned offline distribution — the container
rewrites the fixture's `distributionUrl` to `file:///opt/dists/gradle-9.5.0-bin.zip`.
That rewrite is itself a confound on `false-positives` (finding 6).

**Limits.** `turns: 100`, `tokens: 5,000,000`, `wall_clock: 30m` per arm,
identical across all 30 arms. **Two arms were bounded**, both treatment, both on
tokens: `idioms`/Sonnet 5 (101% of the token budget) and `structure`/Opus 5 (101%,
and 82% of wall clock). Their scorer verdicts stand; their cost figures are lower
bounds and they are never awarded a 🏆. No arm was nudged, no report carries a
warning, and no report is voided.

**Skill provenance.** All 12 treatment arms received `sha256:2e4a645f33fc…`. The 12
archived `SKILL.md` copies are byte-identical to one another, and their body is
byte-identical to `skills/gradle-best-practices/SKILL.md` in the scenarios repo;
they differ only in YAML frontmatter the harness round-trips through a parser.

**Non-uniformity, disclosed.**

1. **`tasks`/Opus 5 came from a re-run on a later evaluator build.** The first
   attempt aborted when the sandbox killed `./gradlew -p build-logic check` at a
   120s exec cap; the evaluator was changed to pass `BASH_DEFAULT_TIMEOUT_MS=300000`
   and both arms were re-run. The re-run's baseline reproduced the original on all
   12 scorers. The other 14 runs predate that change; the aborted attempt is not
   archived.
2. **The `tasks` prompt omits one line** the `structure` and `idioms` prompts carry
   ("This is NOT just an audit, your task is to apply fixes to the build"). It is
   omitted uniformly across all three models, so the within-scenario comparison is
   unaffected, but `tasks` deltas are not strictly prompt-comparable to the other
   two.
3. **The `aa` and `structure` prompts are textually identical** apart from
   whitespace normalisation in the YAML round-trip, and use the same fixture
   revision — which is what makes the A/A control transferable to `structure` and
   only to `structure`.
4. **One archived tree is incomplete.** `structure`/Opus 5/treatment is missing its
   convention-plugin sources: the plugins live in the Java package
   `com.example.carlog.build`, and the archiver's `build/` exclusion pruned that
   package directory along with real Gradle output. The empty
   `build-logic/src/main/java/com/example/carlog/` remains. Scorers ran against the
   live container, not the archive, so the verdicts are unaffected — but that arm's
   plugin *implementation* cannot be audited from stored data. The registration and
   application sites survive in `build-logic/build.gradle.kts` and
   `carlog/build.gradle.kts`, which is what finding 3 rests on.

**Provenance.** Every run's `report.json`, `report.md`, `experiment.resolved.yaml`
and pruned project tree are archived in the scenarios repo under
`history/gradle-best-practices/1.0.0/<scenario>/<model>/`, together with the exact
skill text each treatment arm received. Agent transcripts are not archived; they
stay with the raw sweep output, which is why several questions below cannot be
answered from this data.

### Known gaps

1. **`convention-plugins.sh` does not recognise binary convention plugins.** It
   requires a precompiled script plugin (`*.gradle[.kts]` under `src/main/`) and
   fails a `java-gradle-plugin` build that registers plugins with
   `implementationClass` and has them applied by id. This produced one false
   negative (`structure`/Opus 5/treatment) and will reproduce for any model that
   prefers binary plugins. Fix: also accept an id declared in a
   `gradlePlugin { plugins { … } }` block of an included build.
2. **`tasks-documented.sh` cannot see Java-style task registration.** Its harvest
   regex matches `tasks.register(` but not `project.getTasks().register(`, so a
   Java convention plugin harvests zero names and fails by the zero-names rule
   despite documenting every task. One false negative here
   (`tasks`/Opus 5/treatment).
3. **`no-subproject-properties` does not distinguish a subproject from an included
   build root.** Its pattern `.+/gradle\.properties` flags `build-logic/gradle.properties`,
   which a composite build legitimately needs because properties are not inherited
   across build boundaries. One false negative (`idioms`/Opus 5/treatment), and it
   penalises exactly the composite-build layout the skill recommends.
4. **`gradle_calls` is unreliable.** It reads 0 in six arms; four of those are Opus
   treatment arms that restructured a build and left `./gradlew build` green, which
   the counter cannot be right about. The counter recognises a bare `./gradlew` and
   misses prefixed forms. Without archived transcripts the true counts cannot be
   recovered for these runs. The field is excluded from every claim in this report.
5. **`false-positives` is unwinnable as configured.** The harness rewrites the
   wrapper's `distributionUrl` to a `file://` path and the scorer then counts
   reporting it as a false positive. All six arms failed, and all six flagged that
   line. Either allowlist harness-injected scaffolding or stop rewriting the
   wrapper for this fixture; until then the scenario measures only skill pickup.
6. **The A/A control covers one fixture out of four.** `tasks`, `idioms` and
   `false-positives` have no noise measurement at all, and two of the `structure`
   gains sit on scorers the control found unstable. An A/A per fixture would settle
   which single-check flips are real.
7. **`violations-count` is a one-sided floor and loses the detection signal**
   (finding 2). Opus clears the floor in both arms on every fixture, so tripling
   its recall registers as no change. A graded or delta-based recall measure would
   capture the largest reproducible effect in this sweep.
8. **`skill-used` cannot distinguish "read the skill" from "followed the skill."**
   An arm that opens the file and ignores it scores the same as one that applies it.
9. **No cross-vendor or cross-CLI coverage** (finding 8).
10. **n = 1.** Every number here is directional. Nothing in this report should be
    quoted as a magnitude.
