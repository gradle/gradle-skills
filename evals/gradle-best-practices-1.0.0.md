# Gradle Best Practices Skill v1.0.0 — Benchmark Results

## Summary

`gradle-best-practices@1.0.0` (revision `0b1f547`) was measured against seven models
from five vendors across three agent CLIs, on five Gradle build-quality scenarios,
two arms each, plus a seven-model A/A control. The treatment arm passed **292 of 357**
best-practice checks against **191 of 357** for the unaided baseline — **113 gains,
12 regressions**.

The effect is broad rather than concentrated. All seven models improve, four of them
by 18 checks or more: **DeepSeek-v4-pro +22** (0 regressions), **Sonnet 5 +20**
(0 regressions), **GPT-5.6-luna +20**, **Haiku 4.5 +18**. Eighteen of the 35 treatment
arms clear their fixture outright, and **DeepSeek-v4-pro takes every check in all five
scenarios, 51 of 51**. **Opus 5.5 reaches 48 of 51** — but it starts at 45, so the
skill moves the strongest model least.

Two results deserve to be read before the tables:

**The skill does not touch the network.** It ships the catalog on disk under
`references/` — one detection layer, seven category files covering 48 practices,
and 48 per-practice fix files. **Every treatment arm in this sweep made zero
`WebFetch` calls.** Runs are reproducible offline and cannot drift when the
documentation does.

**Pickup is universal and directly measured.** A `skill-used` scorer verifies the
agent actually invoked the skill. It returns PASS in **35 of 35** treatment arms,
across `claude-code`, `opencode` and `gemini-cli`. No comparison in this sweep is void
for non-pickup.

This report is keyed on **checks passed**. The harness also folds each arm's scorers
into a single pass/fail verdict; that verdict is not reported here. It is an AND over
every check, so a fixture carrying a dozen seeded violations reads `FAIL` almost
everywhere regardless of the skill.

---

## Setup

### What we're measuring

Each scenario runs two arms against the same Gradle project and the same prompt:

| Arm | Skill |
| :--- | :--- |
| `no-skills` | Baseline — no skill provided |
| `with-skills` | `git+https://github.com/gradle/gradle-skills@main#skills/gradle-best-practices`, revision `0b1f547` |

All 35 treatment arms received the same skill revision.

The four fixing prompts ask the agent to investigate the build, write a
`VIOLATIONS.md` with one `<file>: <line>: <description>` line per issue before
changing anything, then apply the fixes while keeping `./gradlew build` green, and
record anything left over in `REMAINING-UNFIXED.md`. `false-positives` is audit-only
and forbids edits. **All five fixing prompts are textually identical**, and the `aa`
prompt matches them exactly.

### Models tested

| Model | Vendor | CLI | Short name |
| :--- | :--- | :--- | :--- |
| `anthropic/claude-haiku-4-5-20251001` | Anthropic | `claude-code 2.1.233` | Haiku 4.5 |
| `anthropic/claude-sonnet-5` | Anthropic | `claude-code 2.1.233` | Sonnet 5 |
| `anthropic/claude-opus-5-5` | Anthropic | `claude-code 2.1.281` | Opus 5.5 |
| `openai/gpt-5.6-luna` | OpenAI | `opencode 1.18.30` | GPT-5.6-luna |
| `google/gemini-3.8-flash` | Google | `gemini-cli 0.59.0` | Gemini 3.8 Flash |
| `deepseek/deepseek-v4-pro` | DeepSeek | `opencode 1.18.30` | DeepSeek-v4-pro |
| `ollama/qwen3.6:35b-a3b-coding-nvfp4` | Alibaba (local) | `claude-code 2.1.233` | Qwen3.6-35B |

Cross-vendor and cross-CLI coverage is the most useful property of this benchmark:
nothing here rests on a single vendor's prompt conventions or a single harness's
skill-loading mechanism.

### Scenarios and fixtures

| Scenario | Fixture | Checks | Detection floor | What it probes |
| :--- | :--- | ---: | ---: | :--- |
| `structure` | `sample-carlog` | 12 | 14 | Build layout: settings, version catalog, repository placement, convention plugins, lazy wiring, wrapper checksum, duplicate dependencies |
| `tasks` | `sample-star-charter` | 15 | 16 | Custom task types: caching, path sensitivity, configuration cache, output collisions, config-time resolution, catalog naming |
| `idioms` | `sample-recipe-vault` | 14 | 13 | Script idioms: `apply plugin`, `afterEvaluate`, internal APIs, properties placement, config-time work, eager file trees |
| `plugin-authoring` | `sample-fleet-tracker` | 8 | 6 | Plugin hygiene: order-independence, no `buildSrc`, reproducible archives, `flatMap` for nested providers |
| `false-positives` | `sample-init-library` | 2 | — | Restraint on untouched `gradle init` output — audit only, no edits |
| `aa` | `sample-carlog` | 12 | 14 | A/A control: two identical `no-skills` arms, same fixture and prompt as `structure` |

Check counts exclude `skill-used`, which is scored only on the treatment arm and
therefore cannot contribute a delta. `aa` runs no treatment arm and contributes no
checks to the totals.

Fixture revisions: `sample-carlog` `sha256:624f1d41fe05…`, `sample-star-charter`
`sha256:88676a5a66f6…`, `sample-recipe-vault` `sha256:edc64794f43e…`,
`sample-fleet-tracker` `sha256:833ff574c5f9…`, `sample-init-library`
`sha256:9e2a7c7b0f14…`.

### Scorers

Most checks are `file-exists` greps over comment-stripped copies of the build
sources. The ones worth calling out are the behavioural and structural probes, and
the two meta-scorers:

- **`lazy-extension-wiring`** (`structure`) — not a regex. An init script reconfigures
  the `carLog` extension in `gradle.afterProject`, after every build script has
  evaluated, then runs `recordDemoMaintenance`. Lazy wiring picks the new value up
  and writes the probe file; eager `.get()` at configuration time does not.
  Fix-shape agnostic.
- **`convention-plugins`** (`structure`) — requires the whole chain: an included build,
  a plugin inside it, and a main-build script applying it by id. Accepts binary
  plugins declared through `gradlePlugin { plugins { … id = … } }` as well as
  precompiled script plugins.
- **`tasks-documented`** (`tasks`) — harvests script-defined task names, then runs
  `./gradlew tasks --all` and demands every harvested name Gradle lists carry a
  description. **Cannot see Java-style registration** — see known gap 1.
- **`plugin-order-agnostic`** / **`convention-order-agnostic`** (`plugin-authoring`) —
  behavioural probes that apply the plugin before and after the `java` plugin and
  demand the same result.
- **`only-defensible-findings`** (`false-positives`) — every reported finding must be
  one the tree actually supports. The allowlist covers the two `gradle init` findings
  *and* three wrapper findings the harness's own `distributionUrl` rewrite creates,
  matched on file **and** description as a conjunction. Allowlisting the wrapper
  findings is what makes the scenario winnable; see finding 5.
- **`violations-count`** (all four fixing scenarios) — a one-sided recall floor over
  non-blank lines in `VIOLATIONS.md`. Over-reporting passes; under-reporting fails.
  The floors sit close to each fixture's full seeded inventory, so mid-sized reports
  fail it.
- **`skill-used`** — scored on the treatment arm only; verifies the agent actually
  invoked the skill.

### Scorer verdicts

| Verdict | Meaning |
| :--- | :--- |
| ✅ **PASS** | The scorer's criterion was met. |
| ❌ **FAIL** | The trial ran and the criterion was not met. |
| ⚠️ **INVALID** | The scorer could not render a verdict. No arm in this sweep returned INVALID. |

One arm was bounded by its token cap: `plugin-authoring`/Qwen3.6-35B, treatment. Its
scorer verdicts stand; its cost figures are lower bounds and are marked `≥`.

---

## Key findings

### 1. Every model improves, but the weakest model's gain is the least trustworthy

| Model | Baseline | Treatment | Δ | Gains | Regressions |
| :--- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek-v4-pro | 29 / 51 | **51 / 51** | **+22** | 22 | 0 |
| Sonnet 5 | 30 / 51 | **50 / 51** | **+20** | 20 | 0 |
| GPT-5.6-luna | 27 / 51 | **47 / 51** | **+20** | 21 | 1 |
| Haiku 4.5 | 11 / 51 | **29 / 51** | **+18** | 20 | 2 |
| Qwen3.6-35B | 11 / 51 | **21 / 51** | **+10** | 17 | 7 |
| Gemini 3.8 Flash | 38 / 51 | **46 / 51** | **+8** | 9 | 1 |
| Opus 5.5 | 45 / 51 | **48 / 51** | **+3** | 4 | 1 |
| **All** | **191 / 357** | **292 / 357** | **+101** | **113** | **12** |

Gains run broadly inverse to unaided competence, which is what a knowledge-injection
skill should do. Opus 5.5 already knows most of this catalog; the skill buys it three
checks. Haiku 4.5, which does not, gains 18 against two regressions — the cleanest
demonstration in the sweep that the catalog supplies knowledge the model lacks.

**Qwen3.6-35B is the exception and should not be read as part of that pattern.** Its
+10 is the second-largest raw gain count in the sweep (17 gains), but it comes with
**seven regressions — more than the other six models combined** — and two of those are
`project-builds` flipping PASS → FAIL. It still nets an improvement, and every one of
its 17 gains is a real check it did not pass unaided; but a net that is built from 17
gains and 7 regressions is a different thing from Haiku's 20 and 2, and finding 4
argues the trade is not worth taking at that model size.

**DeepSeek-v4-pro is the standout**: 51 of 51 with zero regressions, including
perfect grids on `structure` (12/12), `tasks` (15/15), `idioms` (14/14) and
`plugin-authoring` (8/8). Sonnet 5 misses only `cacheable-annotation` on `tasks`.

### 2. The detection signal is large, consistent, and only partly captured

Every fixing prompt mandates a `VIOLATIONS.md` inventory. Non-blank line counts,
baseline → treatment, with the fixture's floor:

| Scenario | Floor | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `structure` | 14 | 3 → **9** | 8 → **26** | 25 → **30** | 8 → **17** | 12 → **22** | 6 → **28** | 4 → **13** |
| `tasks` | 16 | 3 → **8** | 17 → **27** | 24 → **34** | 13 → **24** | 24 → **27** | 12 → **31** | 6 → **14** |
| `idioms` | 13 | 1 → **8** | 7 → **18** | 18 → **25** | 9 → **14** | 10 → **11** | 8 → **17** | 4 → **10** |
| `plugin-authoring` | 6 | 2 → **3** | 4 → **11** | 12 → **10** | 6 → **13** | 6 → **6** | 7 → **10** | 3 → **4** |

The skill raises detection in **25 of 28 fixture-model pairs**, flat in two, down in
one (Opus on `plugin-authoring`, 12 → 10, where both arms clear the floor of 6 and
score 8/8 regardless). Typical multiples are 1.5× to 4×; DeepSeek on `structure` is
6 → 28.

The grid captures part of this. `violations-count` moves for Sonnet (3 of 4 fixtures),
GPT (3), DeepSeek (3) and Gemini (1). It is one-sided, so Opus's 25 → 30 on
`structure` scores nothing — both arms clear the floor of 14.

**But see finding 8 before quoting any of these numbers as an effect size.** The A/A
control puts the run-to-run band on this metric at up to ±7 lines.

### 3. `plugin-authoring` is the cleanest scenario, and it works

The `sample-fleet-tracker` fixture probes plugin hygiene with two behavioural
order-independence checks. Results: **five of seven models gain, none lose except
Qwen**, and five arms reach 8/8. Sonnet goes 3 → 8 with five gains.

The two most-gained checks are `flatmap-for-nested-providers` (+5 models) and
`reproducible-archives` (+3) — both textbook catalog entries that models do not reach
for unaided. `no-forced-java-plugin` passes in 13 of 14 arms and `project-builds` in
13 of 14, so the fixture is not simply hard; it is targeted.

### 4. Qwen3.6-35B is where the skill does damage

17 gains against **7 regressions** — by far the worst ratio in the sweep — and two of
those regressions are **`project-builds` flipping PASS → FAIL**. The treatment arm
broke the build on `idioms` and on `plugin-authoring`, having left it green unaided.
Its `idioms` grid goes 7/14 → 3/14, losing `plugins-block-only`, `no-after-evaluate`,
`build-cache-enabled` and `config-cache-enabled` alongside the build itself.

The cost profile says why: turns 93 → 289 (3.11×), cached input 4.6M → 21.7M (4.76×),
and the `plugin-authoring` treatment arm hit 100% of its token cap and was bounded.
A 35B local model given a 48-practice catalog attempts far more than it can land.

**This is a real limitation, not a scoring artifact.** The skill should carry guidance
on scoping work when the model cannot hold the whole catalog, or the catalog needs a
smaller default slice.

### 5. `false-positives` produces real signal, and the skill reduces invented findings

This scenario only works because `only-defensible-findings.sh` allowlists three
wrapper findings (`validate_gradle_checksum`, `validate_wrapper_checksum`,
`use_latest_minor_versions`) alongside the two `gradle init` findings, each matched on
file **and** description. The harness rewrites the wrapper's `distributionUrl` to a
`file://` path before the agent sees it; an agent that reports that line is right
about the tree as staged, and scoring it as a false positive would make the scenario
unwinnable by construction.

Result: **five of seven models gain**, and the treatment arm passes in six of seven.

| Model | Baseline | Treatment |
| :--- | :--- | :--- |
| Haiku 4.5 | ❌ FAIL | ✅ PASS |
| Sonnet 5 | ❌ FAIL | ✅ PASS |
| Opus 5.5 | ❌ FAIL | ❌ FAIL |
| GPT-5.6-luna | ❌ FAIL | ✅ PASS |
| Gemini 3.8 Flash | ✅ PASS | ❌ FAIL |
| DeepSeek-v4-pro | ❌ FAIL | ✅ PASS |
| Qwen3.6-35B | ❌ FAIL | ✅ PASS |

The skill makes agents report *fewer invented* findings on clean `gradle init`
output, which is the opposite of the intuition that a checklist encourages
nitpicking. The two exceptions are instructive:

- **Opus 5.5 fails in both arms.** Its treatment report is four defensible lines plus
  one that is not: the JUnit version being hardcoded in `lib/build.gradle.kts` rather
  than in a catalog. `gradle init` writes that line; there is no catalog to move it
  to.
- **Gemini's regression is the scenario working as designed.** Its baseline wrote an
  empty `VIOLATIONS.md` — a trivial PASS, silence on a clean build. Its treatment arm
  reported two findings, one of them the same hardcoded-version claim. The skill
  turned a vacuous pass into a real, slightly-wrong audit.

### 6. The skill is not free

Totals across the 35 delta arms, by model:

| Model | Turns | Output tokens | Cached input | Wall (s) | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 147 → 209 (1.42×) | 27,671 → 46,174 (1.67×) | 5.78M → 11.15M (1.93×) | 556 → 900 (1.62×) | 0.81 → 1.57 |
| Sonnet 5 | 117 → 154 (1.32×) | 116,163 → 229,102 (1.97×) | 6.94M → 14.92M (2.15×) | 1,597 → 2,858 (1.79×) | 3.05 → 6.31 |
| Opus 5.5 | 43 → 67 (1.56×) | 40,441 → 68,101 (1.68×) | 1.30M → 3.32M (2.55×) | 639 → 1,061 (1.66×) | 1.52 → 3.16 |
| GPT-5.6-luna | 96 → 100 (1.04×) | 27,819 → 36,441 (1.31×) | 1.15M → 2.17M (1.88×) | 601 → 834 (1.39×) | 0.10 → 0.16 |
| Gemini 3.8 Flash | 294 → 287 (0.98×) | 492,621 → 345,219 (0.70×) | 15.83M → 18.57M (1.17×) | 2,867 → 2,557 (0.89×) | 4.30 → 3.86 |
| DeepSeek-v4-pro | 178 → 148 (0.83×) | 191,258 → 251,428 (1.31×) | 6.15M → 8.88M (1.44×) | 1,884 → 2,238 (1.19×) | 0.63 → 0.87 |
| Qwen3.6-35B | 93 → 289 (3.11×) | 188,886 → 297,934 (1.58×) | 4.57M → 21.75M (4.76×) | ≥10,167 → ≥12,902 (1.27×) | n/a |

Gemini's apparent saving is one outlier: its `plugin-authoring` **baseline** burned
263,866 output tokens and 1,060s, more than four times its own treatment arm. Strip
that scenario and Gemini's output-token ratio is 1.20×, not 0.70×. Do not read
Gemini as evidence the skill is free.

A more useful figure than the raw multiple is **extra output tokens spent per check
gained**: ~430 for GPT-5.6-luna, ~1,050 for Haiku 4.5, ~2,700 for DeepSeek-v4-pro,
~5,600 for Sonnet 5, ~9,200 for Opus 5.5. The models that gain most cost least per
gain, which is the right shape — the skill is cheapest exactly where it does the most
work, and Opus pays the most per check because it had the least left to learn. Gemini
is omitted because its output-token delta is negative on the outlier above; Qwen is
omitted because its gain count is not comparable (finding 1).

**One arm of thirty-five was bounded**, `plugin-authoring`/Qwen3.6-35B on tokens. No
Anthropic, OpenAI, Google or DeepSeek arm came within a third of any cap.

### 7. The bundled catalog trades fetch cost for read cost, and buys determinism

Zero `WebFetch` calls in any treatment arm. The catalog does not arrive free — it
moves into `Read` calls on `references/`, and treatment arms consistently show
elevated `Read` counts (Haiku `structure` 7 → 16, Qwen `structure` 11 → 44, DeepSeek
`plugin-authoring` 24 → 44).

What this buys is **determinism**: every run reads the same catalog, captured from the
Gradle 9.9.0-nightly documentation on 2026-09-23, and no run can be perturbed by a
documentation edit, a rate limit, or a failed fetch. For a skill whose entire purpose
is injecting a specific body of knowledge, reproducibility is worth more than the
token delta — and it means these results describe what a user will get offline, not
what the docs happened to say on 2026-09-24.

### 8. The noise floor is wide

The `aa` control runs on all seven models. Scorer disagreement between two
**identical** `no-skills` arms:

| Model | Scorers disagreeing | Which | Detection lines |
| :--- | :---: | :--- | :--- |
| GPT-5.6-luna | 0 / 12 | — | 4 vs 11 |
| Haiku 4.5 | 1 / 12 | `no-duplicate-dependencies` | 8 vs 1 |
| Opus 5.5 | 1 / 12 | `wrapper-checksum-engaged` | 24 vs 25 |
| Qwen3.6-35B | 2 / 12 | `root-project-named`, `lazy-extension-wiring` | 5 vs 3 |
| Sonnet 5 | 3 / 12 | `repos-not-in-build-scripts`, `convention-plugins`, `wrapper-checksum-engaged` | 17 vs 14 |
| DeepSeek-v4-pro | 3 / 12 | `version-catalog`, `convention-plugins`, `violations-count` | 14 vs 11 |
| Gemini 3.8 Flash | 4 / 12 | `root-project-named`, `no-eager-getbyname`, `lazy-extension-wiring`, `no-duplicate-dependencies` | 9 vs — ⚠️ |

⚠️ **Gemini's A/A is void.** Its `no-skills-b` arm ran two turns, produced 554 output
tokens, wrote no `VIOLATIONS.md` and consumed zero cached input. That is a degenerate
arm, not a measurement, and its 4/12 should be discarded.

**The detection-count band is much wider than the scorer band.** Haiku's A/A produced
**8 versus 1** lines and GPT's **4 versus 11** — swings of 7 lines on the same fixture,
same prompt, same conditions. Finding 2's detection multiples remain directionally
solid because most of them are far larger than 7, but **the smaller ones (Gemini
`idioms` 10 → 11, Haiku `plugin-authoring` 2 → 3, Qwen `plugin-authoring` 3 → 4) are
inside the noise and should not be counted.**

On the scorer grid, up to 3 of 12 checks flip between identical arms. Aggregate
deltas of +18 and above are far outside that; **Opus's +3 is not.** Opus's A/A was
clean (1/12), which helps, but a single-check-per-scenario movement on one model is
directional at best.

### 9. n = 1 per arm

Single trials throughout, with the noise floor measured on one fixture per model.
Every magnitude in this report is directional.

---

## Summary tables

### Checks passed, by model and scenario

| Model | `structure` | `tasks` | `idioms` | `plugin-authoring` | `false-positives` | **Total** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Haiku 4.5 | 2 → 6 | 3 → 9 | 2 → 7 | 3 → 5 | 1 → 2 | **11 → 29** (+18) |
| Sonnet 5 | 6 → 12 | 10 → 14 | 10 → 14 | 3 → 8 | 1 → 2 | **30 → 50** (+20) |
| Opus 5.5 | 11 → 12 | 13 → 13 | 12 → 14 | 8 → 8 | 1 → 1 | **45 → 48** (+3) |
| GPT-5.6-luna | 3 → 11 | 8 → 13 | 9 → 13 | 6 → 8 | 1 → 2 | **27 → 47** (+20) |
| Gemini 3.8 Flash | 5 → 10 | 13 → 15 | 10 → 12 | 8 → 8 | 2 → 1 | **38 → 46** (+8) |
| DeepSeek-v4-pro | 4 → 12 | 9 → 15 | 9 → 14 | 6 → 8 | 1 → 2 | **29 → 51** (+22) |
| Qwen3.6-35B | 1 → 5 | 0 → 7 | 7 → 3 | 2 → 4 | 1 → 2 | **11 → 21** (+10) |
| **All** | **32 → 68** | **56 → 86** | **59 → 77** | **36 → 49** | **8 → 12** | **191 → 292** |
| *Max* | *84* | *105* | *98* | *56* | *14* | *357* |

### Every regression in the sweep

Twelve, across five models. Two models regress nowhere.

| Model | Scenario | Check | Assessment |
| :--- | :--- | :--- | :--- |
| Opus 5.5 | `tasks` | `tasks-documented` | **Scorer artifact** — see known gap 1 |
| Qwen3.6-35B | `idioms` | `project-builds` | Real — treatment broke the build |
| Qwen3.6-35B | `idioms` | `plugins-block-only` | Real |
| Qwen3.6-35B | `idioms` | `no-after-evaluate` | Real |
| Qwen3.6-35B | `idioms` | `build-cache-enabled` | Real |
| Qwen3.6-35B | `idioms` | `config-cache-enabled` | Real |
| Qwen3.6-35B | `plugin-authoring` | `project-builds` | Real — treatment broke the build |
| Qwen3.6-35B | `plugin-authoring` | `no-forced-java-plugin` | Real |
| Haiku 4.5 | `structure` | `no-duplicate-dependencies` | **Inside the A/A band** — Haiku's own control flipped this exact scorer |
| Haiku 4.5 | `tasks` | `no-cc-optout` | Real — added a configuration-cache opt-out |
| GPT-5.6-luna | `tasks` | `no-cc-optout` | Real — same failure mode |
| Gemini 3.8 Flash | `false-positives` | `only-defensible-findings` | Real, but replaces a vacuous pass — see finding 5 |

Discounting the one scorer artifact and the one A/A-band flip, **10 real
regressions, 7 of them one model.**

`no-cc-optout` failing in two independent treatment arms and no baseline arm is the
only cross-model negative signal in the sweep. Both agents added
`notCompatibleWithConfigurationCache` to a task rather than fixing the incompatibility.
**The skill should say not to do that.**

### Skill pickup

| Model | Treatment arms | `skill-used` | `WebFetch` calls |
| :--- | :---: | :---: | :---: |
| Haiku 4.5 | 5 | 5 / 5 PASS | 0 |
| Sonnet 5 | 5 | 5 / 5 PASS | 0 |
| Opus 5.5 | 5 | 5 / 5 PASS | 0 |
| GPT-5.6-luna | 5 | 5 / 5 PASS | 0 |
| Gemini 3.8 Flash | 5 | 5 / 5 PASS | 0 |
| DeepSeek-v4-pro | 5 | 5 / 5 PASS | 0 |
| Qwen3.6-35B | 5 | 5 / 5 PASS | 0 |

35 of 35, across three CLIs with three different skill-invocation tools (`Skill`,
`skill`, `activate_skill`). No baseline arm invoked a skill. Two baseline arms made
incidental `WebFetch`/`WebSearch` calls; no treatment arm fetched the catalog.

---

## Results by scenario

Grids read `baseline → treatment`. ✅ = PASS, ❌ = FAIL.

### structure

**Fixture:** `sample-carlog` (`sha256:624f1d41fe05…`), detection floor 14
**Key checks:** root project named in settings; version catalog present; repositories
declared in settings; no eager `getByName`; no intra-project `dependsOn`; lazy
extension wiring (behavioural); no sources in the root project; convention plugins
wired end to end; wrapper checksum engaged; no duplicate dependencies.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `root-project-named` | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ |
| `version-catalog` | ❌→❌ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `repos-not-in-build-scripts` | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `no-eager-getbyname` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `no-intraproject-dependson` | ❌→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ |
| `lazy-extension-wiring` | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `no-source-in-root` | ❌→❌ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→❌ | ❌→✅ | ❌→✅ |
| `convention-plugins` | ❌→❌ | ❌→✅ | ✅→✅ | ❌→❌ | ❌→❌ | ❌→✅ | ❌→❌ |
| `wrapper-checksum-engaged` | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `no-duplicate-dependencies` | ✅→❌ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `violations-count` | ❌→❌ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |

**Signal:** The biggest scenario-level movement in the sweep, 32 → 68 of 84. GPT and
DeepSeek both gain eight checks; Sonnet and DeepSeek reach 12/12, joining Opus.
`no-intraproject-dependson` is the clearest single result — it fails in **all seven
baselines and passes in six of seven treatments**, the only check in the sweep with
that shape. No model removes intra-project `dependsOn` wiring unaided; six of seven
do with the catalog. `convention-plugins` is the hardest check here: four models
still cannot build the full included-build-plus-plugin-id chain.

### tasks

**Fixture:** `sample-star-charter` (`sha256:88676a5a66f6…`), detection floor 16
**Key checks:** every script-defined task documented (`gradle tasks --all` probe); no
`PathSensitivity.ABSOLUTE`; `@CacheableTask` present; no `.cacheIf`; no
configuration-cache opt-out; `google()` removed from settings; no `configurations.all`;
configuration attributes set; catalog entries meaningfully named; wrapper checksum;
unique task outputs; no config-time resolution; configuration cache enabled.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `tasks-documented` | ❌→✅ | ❌→✅ | ✅→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ |
| `no-absolute-sensitivity` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `cacheable-annotation` | ❌→✅ | ❌→❌ | ❌→❌ | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `no-cacheif` | ✅→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `no-cc-optout` | ✅→❌ | ✅→✅ | ✅→✅ | ✅→❌ | ✅→✅ | ✅→✅ | ❌→❌ |
| `google-repo-removed` | ❌→❌ | ✅→✅ | ✅→✅ | ❌→❌ | ✅→✅ | ✅→✅ | ❌→❌ |
| `no-configurations-all` | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `configuration-attributes` | ❌→❌ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→❌ |
| `catalog-entries-named` | ❌→❌ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ❌→✅ |
| `wrapper-checksum-engaged` | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `unique-task-outputs` | ❌→❌ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `no-config-time-resolution` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `config-cache-enabled` | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ |
| `violations-count` | ❌→❌ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→❌ |

**Signal:** 56 → 86 of 105. Gemini and DeepSeek reach 15/15. `tasks-documented` gains
in six of seven models and is the single most-gained check in the sweep — and Opus's
lone regression on it is the scorer artifact in known gap 1, not a defect: Opus
documented all three tasks in a Java convention plugin the harvester cannot read.
Corrected, Opus reads 13 → 14. `cacheable-annotation` fails in both Sonnet and both
Opus arms, the only check that resists the two strongest Anthropic models.
`no-cc-optout` is the sweep's one cross-model regression — see
[Every regression in the sweep](#every-regression-in-the-sweep).

### idioms

**Fixture:** `sample-recipe-vault` (`sha256:edc64794f43e…`), detection floor 13
**Key checks:** `plugins {}` rather than `apply plugin`; no `afterEvaluate`; no
`org.gradle.internal` APIs; build cache enabled; UTF-8 pinned in `org.gradle.jvmargs`;
no `gradle.properties` outside the build root; no map-form GAVs; no empty container
project; no configuration-time file hashing (behavioural); wrapper checksum;
configuration cache enabled; no eager `fileTree`.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |
| `plugins-block-only` | ❌→❌ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |
| `no-after-evaluate` | ❌→❌ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅���❌ |
| `no-internal-apis` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `build-cache-enabled` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |
| `utf8-in-jvmargs` | ❌→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `no-subproject-properties` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `single-gav-strings` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `no-empty-project` | ❌→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `no-config-time-hashing` | ❌→❌ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `wrapper-checksum-engaged` | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ❌→❌ | ❌→✅ | ❌→❌ |
| `config-cache-enabled` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |
| `no-eager-filetree` | ❌→❌ | ✅→✅ | ✅→✅ | ❌→❌ | ✅→✅ | ❌→✅ | ❌→✅ |
| `violations-count` | ❌→❌ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→❌ | ❌→✅ | ❌→❌ |

**Signal:** 59 → 77 of 98. Sonnet, Opus and DeepSeek all reach 14/14. `utf8-in-jvmargs`
and `no-empty-project` are the story: both fail in **all seven baselines** and both
gain in five treatments — two checks no model reaches for unaided and the catalog
reliably surfaces. `no-subproject-properties` passes in 13 of 14 arms: the scorer
distinguishes an included build's own root from a subproject, so the composite layout
the skill recommends is not penalised. Qwen supplies five of the sweep's twelve
regressions here, all downstream of breaking the build.

### plugin-authoring

**Fixture:** `sample-fleet-tracker` (`sha256:833ff574c5f9…`), detection floor 6
**Key checks:** plugin applies correctly regardless of ordering (behavioural);
convention plugin likewise; no forced `java` plugin application; no `buildSrc`;
reproducible archives configured; `flatMap` rather than `map` for nested providers.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |
| `plugin-order-agnostic` | ❌→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `convention-order-agnostic` | ❌→❌ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |
| `no-forced-java-plugin` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |
| `no-buildsrc` | ✅→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `reproducible-archives` | ❌→❌ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ |
| `flatmap-for-nested-providers` | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ |
| `violations-count` | ❌→❌ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→❌ |

**Signal:** 36 → 49 of 56 in its first outing. Five arms reach 8/8. Opus and Gemini
already score 8/8 unaided, so only five models could improve at all, and all five
did. `flatmap-for-nested-providers` gains in five
models — the largest single-check gain in the sweep — and `reproducible-archives` in
three. The scenario is the cleanest evidence that the bundled catalog transfers
specific, non-obvious practices rather than general tidiness.

### false-positives

**Fixture:** `sample-init-library` (`sha256:9e2a7c7b0f14…`) — untouched `gradle init`
output, no seeded violations
**Key checks:** the build still builds; every reported finding is defensible against
the tree as staged.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `only-defensible-findings` | ❌→✅ | ❌→✅ | ❌→❌ | ❌→✅ | ✅→❌ | ❌→✅ | ❌→✅ |

**Signal:** Five gains, one regression, one flat — see finding 5. `project-builds`
passes in all fourteen arms, which is the audit-only prompt being obeyed everywhere.
The two remaining failures cluster on one claim: that `gradle init`'s hardcoded JUnit
version belongs in a version catalog the generated project does not have. Both Opus's
treatment failure and Gemini's regression are that line.

---

## Cost & Efficiency

> **Token accounting note:** the Inspect harness uses prompt caching where the
> provider supports it. "Cached input" is served from the prompt cache; "cache write"
> is billed at a premium. `gemini-cli`, `opencode`/DeepSeek and the local Ollama path
> report **zero** cache writes — that is missing instrumentation, not a saving, and
> those cells are omitted. Wall clock is `adjusted_wall_clock` in seconds — the
> agent's active time, minus harness overhead.
>
> **Reading the 🏆:** it marks the cheaper of the two arms for that model and metric;
> lower is better everywhere. ✅ ❌ are reserved for scorer verdicts and never appear
> here. Ties are unmarked. **A bounded arm is never marked and its figures carry `≥`.**
>
> **Per-arm limits are NOT uniform across models** — see Methodology. Both arms of a
> given run always share limits, so every baseline-versus-treatment comparison below
> is clean. **Cross-model cost comparison is not**, and no claim here makes one.

### structure — cost

| Model | Turns | Wall (s) | Output | Cached input | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 23 / 36 | 🏆 99.7 / 171.4 | 🏆 4,329 / 9,109 | 🏆 908,573 / 1,969,285 | 🏆 0.133 / 0.290 |
| Sonnet 5 | 🏆 13 / 34 | 🏆 235.7 / 827.0 | 🏆 17,559 / 70,579 | 🏆 739,399 / 3,896,073 | 🏆 0.425 / 1.783 |
| Opus 5.5 | 🏆 12 / 18 | 🏆 195.4 / 356.0 | 🏆 14,953 / 23,604 | 🏆 467,833 / 1,109,695 | 🏆 0.556 / 1.032 |
| GPT-5.6-luna | 24 / 🏆 22 | 🏆 155.9 / 190.4 | 🏆 7,131 / 9,688 | 🏆 384,083 / 589,307 | 🏆 0.025 / 0.043 |
| Gemini 3.8 Flash | 72 / 🏆 52 | 549.1 / 🏆 524.1 | 85,058 / 🏆 80,706 | 5,963,023 / 🏆 3,465,753 | 1.060 / 🏆 0.779 |
| DeepSeek-v4-pro | 51 / 🏆 32 | 🏆 415.9 / 508.4 | 🏆 37,433 / 59,099 | 🏆 1,766,144 / 2,092,544 | 🏆 0.147 / 0.202 |
| Qwen3.6-35B | 🏆 10 / 66 | 🏆 332.1 / 1,598.6 | 🏆 13,158 / 52,772 | 🏆 315,385 / 5,034,109 | n/a |

### tasks — cost

| Model | Turns | Wall (s) | Output | Cached input | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 39 / 42 | 🏆 154.7 / 189.4 | 🏆 8,504 / 9,632 | 🏆 1,613,600 / 2,262,058 | 🏆 0.231 / 0.323 |
| Sonnet 5 | 🏆 42 / 43 | 🏆 436.0 / 659.4 | 🏆 31,597 / 53,176 | 🏆 2,687,974 / 4,203,828 | 🏆 0.988 / 1.603 |
| Opus 5.5 | 🏆 9 / 19 | 🏆 135.0 / 255.5 | 🏆 8,169 / 18,070 | 🏆 243,677 / 887,600 | 🏆 0.292 / 0.779 |
| GPT-5.6-luna | 🏆 23 / 25 | 🏆 135.1 / 199.1 | 🏆 6,020 / 8,619 | 🏆 288,129 / 530,142 | 🏆 0.023 / 0.036 |
| Gemini 3.8 Flash | 🏆 50 / 64 | 542.5 / 🏆 481.9 | 66,370 / 🏆 57,957 | 🏆 2,460,184 / 4,844,521 | 🏆 0.677 / 0.850 |
| DeepSeek-v4-pro | 56 / 🏆 38 | 542.4 / 🏆 483.2 | 57,077 / 🏆 54,160 | 2,492,928 / 🏆 2,153,728 | 0.202 / 🏆 0.199 |
| Qwen3.6-35B | 🏆 12 / 49 | 🏆 332.7 / 1,441.8 | 🏆 12,181 / 50,217 | 🏆 301,267 / 3,405,159 | n/a |

### idioms — cost

| Model | Turns | Wall (s) | Output | Cached input | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 45 / 46 | 🏆 132.8 / 167.0 | 🏆 7,599 / 9,524 | 🏆 1,785,112 / 2,373,754 | 🏆 0.238 / 0.324 |
| Sonnet 5 | 26 / 🏆 25 | 🏆 292.8 / 559.9 | 🏆 21,473 / 46,518 | 🏆 1,455,452 / 1,990,509 | 🏆 0.592 / 1.054 |
| Opus 5.5 | 🏆 9 / 12 | 🏆 117.9 / 177.8 | 🏆 8,224 / 12,635 | 🏆 242,293 / 536,577 | 🏆 0.289 / 0.568 |
| GPT-5.6-luna | 🏆 21 / 23 | 🏆 120.3 / 173.5 | 🏆 5,731 / 7,504 | 🏆 208,779 / 513,645 | 🏆 0.018 / 0.035 |
| Gemini 3.8 Flash | 🏆 51 / 55 | 🏆 417.0 / 511.2 | 🏆 55,129 / 69,742 | 🏆 2,333,572 / 3,836,368 | 🏆 0.622 / 0.758 |
| DeepSeek-v4-pro | 24 / 🏆 23 | 🏆 261.5 / 462.8 | 🏆 25,173 / 55,515 | 🏆 583,296 / 1,107,456 | 🏆 0.077 / 0.166 |
| Qwen3.6-35B | 🏆 28 / 55 | 🏆 515.7 / 1,880.6 | 🏆 20,349 / 54,644 | 🏆 1,138,400 / 3,830,761 | n/a |

### plugin-authoring — cost

| Model | Turns | Wall (s) | Output | Cached input | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 27 / 64 | 🏆 110.2 / 245.8 | 🏆 5,035 / 13,025 | 🏆 1,034,623 / 3,592,217 | 🏆 0.148 / 0.479 |
| Sonnet 5 | 🏆 26 / 44 | 🏆 476.5 / 675.8 | 🏆 36,569 / 50,904 | 🏆 1,638,690 / 4,450,288 | 🏆 0.828 / 1.640 |
| Opus 5.5 | 🏆 8 / 13 | 🏆 119.4 / 192.6 | 🏆 6,423 / 11,773 | 🏆 234,940 / 639,424 | 🏆 0.266 / 0.593 |
| GPT-5.6-luna | 🏆 17 / 19 | 🏆 122.2 / 169.2 | 🏆 5,927 / 7,585 | 🏆 199,931 / 380,417 | 🏆 0.019 / 0.031 |
| Gemini 3.8 Flash | 75 / 🏆 63 | 1,060.1 / 🏆 535.8 | 263,866 / 🏆 67,951 | 3,780,164 / 🏆 3,360,416 | 1.551 / 🏆 0.763 |
| DeepSeek-v4-pro | 🏆 20 / 48 | 🏆 329.7 / 644.8 | 🏆 36,416 / 71,584 | 🏆 612,224 / 3,444,224 | 🏆 0.100 / 0.261 |
| Qwen3.6-35B | 32 / ≥ 107 | 8,756.0 / ≥ 7,630.6 | 136,078 / ≥ 128,221 | 🏆 2,649,556 / ≥ 9,259,438 | n/a |

Gemini's baseline here is the sweep's single most expensive arm and the sole reason
its aggregate reads as a saving. Treat it as an outlier, not a result.

### false-positives — cost

| Model | Turns | Wall (s) | Output | Cached input | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 13 / 21 | 🏆 58.3 / 126.3 | 🏆 2,204 / 4,884 | 🏆 440,718 / 953,409 | 🏆 0.062 / 0.151 |
| Sonnet 5 | 10 / 🏆 8 | 155.5 / 🏆 135.8 | 8,965 / 🏆 7,925 | 423,133 / 🏆 381,369 | 🏆 0.214 / 0.228 |
| Opus 5.5 | 5 / 5 | 🏆 71.0 / 78.9 | 2,672 / 🏆 2,019 | 🏆 111,371 / 144,614 | 🏆 0.116 / 0.190 |
| GPT-5.6-luna | 11 / 11 | 🏆 67.3 / 101.9 | 🏆 3,010 / 3,045 | 🏆 73,555 / 152,270 | 🏆 0.011 / 0.013 |
| Gemini 3.8 Flash | 🏆 46 / 53 | 🏆 298.4 / 504.3 | 🏆 22,198 / 68,863 | 🏆 1,291,041 / 3,063,779 | 🏆 0.387 / 0.715 |
| DeepSeek-v4-pro | 27 / 🏆 7 | 334.1 / 🏆 138.9 | 35,159 / 🏆 11,070 | 697,472 / 🏆 79,360 | 0.108 / 🏆 0.044 |
| Qwen3.6-35B | 🏆 11 / 12 | 🏆 230.8 / 350.5 | 🏆 7,120 / 12,080 | 🏆 165,519 / 218,795 | n/a |

### Where the skill costs, and where it pays

Totals across the 35 delta arms appear in finding 6. The short version:

- The skill costs **1.3× to 2.0× output tokens** and **1.4× to 2.6× cached input** on
  six of seven models; Qwen is the outlier at 4.8× cached input.
- **Extra output tokens per check gained** range from ~430 (GPT-5.6-luna) to ~9,200
  (Opus 5.5), and track inversely with how much the model gained.
- **One arm of thirty-five was bounded**, on tokens, and it is Qwen.
- **Failed `./gradlew` invocations rose 18 → 43** across all arms. Treatment arms
  attempt more and thrash more mid-flight. `project-builds` still passes in 33 of 35
  treatment arms against 34 of 35 baselines, so they recover — but that churn is real
  and appears in the wall-clock figures.

---

## Methodology and known gaps

**Trials.** n = 1 per arm. 42 runs, 84 arms: 5 delta scenarios × 7 models × 2 arms,
plus 7 A/A runs × 2 identical arms. Runs were strictly sequential within a model.

**Toolchain.** JDK 21, Gradle 9.5.0, `resources: small`, network on. CLIs and versions
per model are in [Models tested](#models-tested). Every arm ran against a pinned
offline distribution — the container rewrites the fixture's `distributionUrl` to
`file:///opt/dists/gradle-9.5.0-bin.zip`. That rewrite is now explicitly accounted
for by the `false-positives` allowlist rather than penalising agents who notice it.

**Limits are not uniform across models.**

| Model | Turns | Tokens | Wall clock |
| :--- | ---: | ---: | ---: |
| Haiku 4.5, Opus 5.5 | 100 | 5,500,000 | 30m |
| Sonnet 5 | 125 | 6,875,000 | 2,250s |
| Opus 5.5, Sonnet 5 (`plugin-authoring` only) | 100 | 6,875,000 | 30m |
| GPT-5.6-luna, DeepSeek-v4-pro | 100 | 5,000,000 | 30m |
| DeepSeek-v4-pro (`plugin-authoring` only) | 100 | 6,250,000 | 30m |
| Gemini 3.8 Flash | 200 | 10,000,000 | 60m |
| Qwen3.6-35B | 200 | 10,000,000 | 120m (180m on `plugin-authoring`) |

**Both arms of any single run always share limits**, so every within-model
baseline-versus-treatment delta in this report is sound. Cross-model cost comparisons
are not, and none is made. One arm was bounded: `plugin-authoring`/Qwen3.6-35B,
treatment, at 100% of tokens.

**Skill provenance.** All 35 treatment arms received git revision
`0b1f5470c1999ba3d351ce2ba4d7010188c325b0`, resolved from
`git+https://github.com/gradle/gradle-skills@main#skills/gradle-best-practices`. The
bundled catalog was captured from the Gradle 9.9.0-nightly documentation on
2026-09-23 and covers 48 practices.

**Prompt uniformity.** All five fixing prompts — including `aa` — are textually
identical, so every fixing scenario is prompt-comparable to every other.
`false-positives` uses its own audit-only prompt, as designed.

**Non-uniformity, disclosed.**

1. **Per-arm limits vary by model**, as tabulated above.
2. **Gemini's A/A control is void.** Its `no-skills-b` arm ran two turns and produced
   no report. Gemini has no usable noise measurement in this sweep.
3. **Three CLIs report no cache-write telemetry** (`gemini-cli`, `opencode`, the local
   Ollama path). Those cells are omitted rather than recorded as zero.
4. **Qwen3.6-35B has no configured price**, so its cost rows read `n/a`. The harness
   reports this as a warning rather than guessing.

**Provenance.** Every run's `report.json`, `report.md`, `experiment.resolved.yaml` and
pruned project tree are archived under
`test-runs/bp-skill-testing-complete-2026-09-24/<model>/runs/<run-id>/`. Agent
transcripts are not archived.

### Known gaps

1. **`tasks-documented.sh` still cannot see Java-style task registration.** Two
   independent causes, both live: its `find` filter covers only `*.gradle`,
   `*.gradle.kts` and `*.kt` — never `*.java` — and its harvest regex anchors on
   `tasks.register(`, which `project.getTasks().register(` does not match. A Java
   convention plugin therefore harvests zero names and fails by the zero-names rule
   despite documenting every task. This produced the one false negative in
   `tasks`/Opus 5.5/treatment, where the arm documented all three tasks with
   `setGroup` and `setDescription` in
   `build-logic/src/main/java/…/StarObservationsPlugin.java`. **The scorer currently
   rewards leaving tasks in a build script and punishes extracting them into a
   convention plugin** — the opposite of what the skill under test recommends.
   Tracked on `tt/fix-tasks-documented-scorer`.
2. **The zero-harvest branch of `tasks-documented.sh` asserts a conclusion it cannot
   support.** It reports "the fixture's custom tasks were removed rather than
   documented", but a harvester that cannot parse the build's language produces
   byte-identical output to an agent that deleted the tasks. Correct and destructive
   refactors score the same.
3. **`violations-count` is a one-sided floor.** Opus clears every floor in both arms,
   so its 1.2× to 1.4× detection gains register as nothing. A graded or delta-based
   recall measure would capture the effect in finding 2 directly.
4. **`gradle_calls` is unreliable.** The counter recognises a bare `./gradlew` and
   misses prefixed forms. The field is excluded from every claim in this report except
   the failed-invocation count in the cost summary, which is a ratio between arms
   measured the same way.
5. **The A/A control covers one fixture out of five**, and one of the seven controls is
   void. `tasks`, `idioms`, `plugin-authoring` and `false-positives` have no noise
   measurement at all, and Gemini has none anywhere.
6. **The detection-count noise band is wide.** Haiku's A/A produced 8 versus 1 lines
   and GPT's 4 versus 11. Small detection gains are not interpretable; see finding 8.
7. **`skill-used` proves invocation, not compliance.** An arm that opens the skill and
   ignores it passes the scorer. It is not a compliance measure.
8. **n = 1.** Every number here is directional. Nothing in this report should be quoted
   as a magnitude.

Three further findings point at catalog edits rather than harness work — the
`notCompatibleWithConfigurationCache` regression, the invented `gradle init`
version-catalog finding, and the small-model scoping problem. They are written up in
`bt-agentic-gradle-evaluator/docs/notes/bp-skill-catalog-gaps-2026-09-24.md`.
