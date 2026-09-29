# Gradle Wrapper Upgrade Skill v1.0.0 — Benchmark Results

## Summary

`gradle-wrapper-upgrade@1.0.0` (revision `d8dcf73`) was measured on seven models from
five vendors across three agent CLIs, on five wrapper-upgrade scenarios. Each scenario
ran twice per model — once with the skill, once without. With the skill, agents passed
**187 of 203** checks against **91 of 203** unaided — **99 gains, 3 regressions**. A
sixth scenario ran the unaided arm twice on every model, to measure how far two identical
runs drift on their own.

Every model improves. Six of the seven land 26 or better out of 29, and **four reach a
perfect 29 of 29** — Opus 5.5, GPT-5.6-luna, Gemini 3.8 Flash and DeepSeek-v4-pro. Sonnet 5
reaches 28, and its one miss is a scorer false negative rather than a model error, so five
of seven are perfect on the merits. Excluding Qwen3.6-35B, the one local model, **the six
hosted models go 79 of 174 → 170 of 174 with zero regressions.** **29 of 35 skilled arms
clear their fixture outright, against 7 of 35 unaided.**

Three results deserve to be read before the tables:

**The skill is cheaper than not having it.** Across the 35 delta arms, treatment spent
**0.68× the output tokens**, **0.71× the wall clock**, **0.90× the turns** and
**0.86× the input-equivalent tokens** of baseline; billed cost on the six priced models
fell **$2.59 → $2.33**. This is the opposite of the `gradle-best-practices` result and it
is not an artifact: the unaided arms thrash — reading the wrapper jar, grepping for
versions, hand-editing properties, retrying — while the skilled arms run a fixed
six-step procedure and stop. **A skill that supplies a procedure converges; a skill that
supplies a catalog explores.**

**Four checks fail in all seven baselines and pass in all seven treatments.**
`wrapper-properties` on `upgrade`, `wrapper-task-pinned` on both blocked scenarios, and
`reported-blocked` on `upgrade-blocked`. No model pins the distribution checksum
unprompted, and no model rolls a failed upgrade back unprompted. Both habits arrive intact
with the skill on every model tested, on every CLI.

**The noise floor is narrow.** The repeat-run control ran two identical unaided arms on
all seven models: **1 of 35 scorer pairs disagreed**, and six of seven models reproduced
themselves exactly. Every aggregate delta in this report is an order of magnitude outside
that band.

This report is keyed on **checks passed**. The harness also folds each arm's scorers into a
single pass/fail verdict; that verdict is reported here too, because these fixtures are
small enough that an outright PASS is achievable and informative. Harness-side caveats —
scorer defects, coverage holes, measurement limits — are collected at the end of this
report rather than interleaved with the results.

---

## Setup

### What we're measuring

Each scenario runs two arms against the same Gradle project and the same prompt:

| Arm | Skill |
| :--- | :--- |
| `no-skills` | Baseline — no skill provided |
| `with-skills` | `git+https://github.com/gradle/gradle-skills@main#skills/gradle-wrapper-upgrade`, revision `d8dcf73` |

All 35 treatment arms received the same skill revision.

Terms used throughout this report:

| Term | Meaning |
| :--- | :--- |
| **arm** | One agent run: one model, one scenario, one skill setting |
| **baseline arm** | The `no-skills` half of a pair |
| **treatment arm** | The `with-skills` half of the same pair |
| **repeat-run control** (`aa`) | A pair of `no-skills` arms run against the same fixture and prompt, to show how much two identical runs differ on their own |

Four of the five scenarios — `upgrade`, `sha-already-pinned`, `upgrade-blocked` and
`upgrade-blocked-git` — share a one-line prompt with the repeat-run control:
*"Upgrade this project's Gradle wrapper to Gradle 9.0.0."* `advice-only` changes one
word: *"How do I upgrade this project's Gradle wrapper to Gradle 9.0.0?"* — and the
correct behaviour inverts with it.

Nothing in any prompt asks for a checksum, for the `wrapper` task to be run twice, or for
a rollback. Every check that moves is measuring an unprompted habit.

### Models tested

| Model | Vendor | CLI | Short name |
| :--- | :--- | :--- | :--- |
| `anthropic/claude-haiku-4-5-20251001` | Anthropic | `claude-code 2.1.281` | Haiku 4.5 |
| `anthropic/claude-sonnet-5` | Anthropic | `claude-code 2.1.281` | Sonnet 5 |
| `anthropic/claude-opus-5-5` | Anthropic | `claude-code 2.1.281` | Opus 5.5 |
| `openai/gpt-5.6-luna` | OpenAI | `opencode 1.18.30` | GPT-5.6-luna |
| `google/gemini-3.8-flash` | Google | `gemini-cli 0.59.0` | Gemini 3.8 Flash |
| `deepseek/deepseek-v4-pro` | DeepSeek | `opencode 1.18.30` | DeepSeek-v4-pro |
| `ollama/qwen3.6:35b-a3b-coding-nvfp4` | Alibaba (local) | `claude-code 2.1.233` | Qwen3.6-35B |

Three CLIs with three different skill-invocation tools (`Skill`, `skill`,
`activate_skill`). Nothing here rests on a single vendor's prompt conventions or a single
harness's skill-loading mechanism.

### Scenarios and fixtures

| Scenario | Fixture | Checks | What it probes |
| :--- | :--- | ---: | :--- |
| `upgrade` | `sample-stale-wrapper` | 5 | Does a complete upgrade happen? Checksum pinned, all three generated files regenerated, nothing else touched |
| `sha-already-pinned` | `sample-pinned-wrapper` | 5 | Can it upgrade a wrapper that already pins a checksum — where the obvious command fails loudly? |
| `upgrade-blocked` | `sample-kiln-registry` | 8 | When the upgrade *cannot* succeed: snapshot, roll back, report, advise |
| `upgrade-blocked-git` | `sample-kiln-registry` | 9 | The same with the project in git — does it roll back *with git*? |
| `advice-only` | `sample-stale-wrapper` | 2 | Asked *how*, does it answer instead of acting? |
| `aa` | `sample-stale-wrapper` | 5 | Repeat-run control: two identical unaided arms, same fixture and prompt as `upgrade` |

Check counts exclude `skill-used`, which is scored only on the treatment arm and therefore
cannot contribute a delta. `aa` runs no treatment arm and contributes no checks to the
totals.

**`sample-stale-wrapper`** — a two-file `java-library` shipping a Gradle 8.5 wrapper with
no `distributionSha256Sum`. The plausible wrong answer it is rigged to catch is the
half-done upgrade: `distributionUrl` bumped, checksum absent, `gradlew`/`gradlew.bat`/
`gradle-wrapper.jar` left at 8.5 — which is exactly what a hand-edit or a single `wrapper`
run leaves behind.

**`sample-pinned-wrapper`** — the same fixture plus exactly one line, 8.5's correct
`distributionSha256Sum`. That line changes the task: once a sum is set, a `wrapper`
invocation that changes `--gradle-version` must also pass a matching new
`--gradle-distribution-sha256-sum` or the build fails. The documented wrong turn is
deleting the old sum line to get past the error, which leaves the distribution unverified.

**`sample-kiln-registry`** — a Gradle 8.5 build whose `buildSrc` convention plugins use
`Project.getConvention()`, `JavaPluginConvention` and `Project.exec`, all removed in 9.0.0.
Run 1 of the `wrapper` task succeeds under 8.5 and repoints `distributionUrl` at 9.0.0;
run 2 downloads 9.0.0 and dies in `:buildSrc:compileJava`, before the root project
configures at all. The project is left pinned to a version it cannot run. That is the
state the skill has to undo, and the temptation the fixture sets is editing `buildSrc`
until 9.0.0 accepts it.

Fixture revisions: `sample-stale-wrapper` `sha256:6aa2317ff2b4…`, `sample-pinned-wrapper`
`sha256:39279825652e…`, `sample-kiln-registry` `sha256:bdeaade0ed1f…`. Scorer revision
`sha256:f2bf77687103…`.

### Scorers

Filesystem scorers source one `common.sh` that pins the 9.0.0 target checksum, the 8.5
origin checksum, and the fixtures' shipped-versus-regenerated wrapper file hashes.

- **`wrapper-properties`** — `distributionUrl` names `gradle-9.0.0-bin.zip` **and**
  `distributionSha256Sum` is 9.0.0's actual sum. Both, as a conjunction.
- **`wrapper-files`** — all three of `gradlew`, `gradlew.bat`, `gradle-wrapper.jar` hash
  to Gradle 9.0.0's bytes. It distinguishes "untouched at the shipped 8.5 version"
  (the `wrapper` task was run once, or not at all) from "matches neither — hand-edited?".
  This is the check that only passes if the `wrapper` task ran **twice**.
- **`no-collateral-damage`** — every non-wrapper file byte-identical to the fixture, and
  nothing new created. Reports modified / deleted / added separately. On `upgrade` it is a
  precision check; on the blocked scenarios it is what catches the agent that repairs
  `buildSrc`, and what enforces "snapshot outside the project tree".
- **`non-version-properties-preserved`** — the six version-independent entries in
  `gradle-wrapper.properties` survived. **Read one-sidedly:** a FAIL is strong evidence
  the file was rewritten by hand; a PASS proves little, because an in-place edit preserves
  them too.
- **`rolled-back`** — `did-not-upgrade` with the reason changed: `distributionUrl` still
  names 8.5, no `distributionSha256Sum` added, all three generated files at their shipped
  hashes. "Never acted" and "acted and undid it" are the same bytes on disk, which is the
  point — read it paired with `reported-blocked`.
- **`restored-to-head`** (`upgrade-blocked-git`) — the working tree is byte-identical to
  the single staged commit **and there is still only one commit**. Strictly stronger than
  `rolled-back` in the direction `rolled-back` cannot see: unbounded. A stray `.bak`, an
  edited `buildSrc` plugin, a snapshot left inside the tree — all of it is `git status`
  output without any of it being enumerated. An agent that commits the failed upgrade
  leaves a clean tree that is clean against the *wrong* commit; the commit count catches it.
- **`did-not-upgrade`** (`advice-only`) — filesystem-only: still on 8.5, no checksum
  added, all three generated files untouched.
- **`explained-how`** (`advice-only`) — `agent-said`: did the agent write a copy-pasteable
  `gradlew`/`gradle` invocation naming the `wrapper` task and carrying `--gradle-version`
  with a value. Deliberately binary, and deliberately unable to be satisfied by *running*
  the command — `agent-said` reads assistant text blocks only, never tool-call arguments.
- **`wrapper-task-pinned`** — `agent-ran`: a shell command naming `gradlew`, the `wrapper`
  task, `--gradle-version` at 9.0.0 **and** `--gradle-distribution-sha256-sum`.
- **`snapshot-verified`** (`upgrade-blocked`) — `agent-ran`: a `find` over a snapshot
  directory outside the tree (`SNAP` or `/tmp/`) with `-type f`. Proof the snapshot was
  listed back, not just taken.
- **`reported-blocked`** — `agent-said`: an adjacency-based phrase pattern for "rolled
  back" / "upgrade blocked" / "still on 8.5". It deliberately rejects "the `wrapper` task
  failed" on its own, because that sentence is equally true of an agent that left 9.0.0
  pinned — it reports what the build did, not what state the project is in.
- **`quoted-error`** — `agent-said`: named the actual removed API
  (`JavaPluginConvention`, `getConvention(`, `Project.exec`, `cannot find symbol`, …).
- **`advised-next-step`** — `agent-said`: requires the upgrade guide or release notes
  **and** names 8.6 as the next rung, **and** rejects "latest 8.x" / 8.14 phrasing. The
  skill's position is that 8.5 → 8.14 crosses nine releases' worth of removals in one step
  and is the same oversized jump that just failed.
- **`git-used`** (`upgrade-blocked-git`) — `agent-ran`: `git checkout -- …` naming
  `gradlew` or `gradle/wrapper`. It exists because **nothing on disk can answer the
  question**: `git checkout --` and `cp -a <snap>/. .` both end at a clean tree.
- **`project-builds`** — `./gradlew build` on `upgrade`, `sha-already-pinned` and `aa`;
  `./gradlew tasks` on the blocked scenarios, where configuring is the whole question.
  Absent from `advice-only`, where nothing is supposed to change.
- **`skill-used`** — scored on the treatment arm only; verifies the agent actually invoked
  the skill.

### Pairs, not singletons

Three scorers are unreadable alone and the report treats them as pairs throughout.

| `did-not-upgrade` | `explained-how` | Reading |
| :--- | :--- | :--- |
| PASS | PASS | gave the commands, ran nothing — correct |
| PASS | FAIL | said nothing useful — right by accident |
| FAIL | PASS | upgraded *and* explained — overstepped |
| FAIL | FAIL | upgraded silently — overstepped and unhelpful |

| `rolled-back` | `reported-blocked` | Reading |
| :--- | :--- | :--- |
| PASS | PASS | restored and said so — correct |
| PASS | FAIL | restored and claimed success — silently wrong |
| FAIL | PASS | said it rolled back, didn't — worse |
| FAIL | FAIL | left the project broken |

`restored-to-head` says the restore was *complete*; only `git-used` says it was done the
way the git branch prescribes.

### Scorer verdicts

| Verdict | Meaning |
| :--- | :--- |
| ✅ **PASS** | The scorer's criterion was met. |
| ❌ **FAIL** | The trial ran and the criterion was not met. |
| ⚠️ **INVALID** | The scorer could not render a verdict. No arm in this sweep returned INVALID. |

**No arm in this sweep was bounded.** The heaviest arm reached 54% of its turn limit
(DeepSeek-v4-pro, `upgrade-blocked`, baseline); no arm came within a third of any token or
wall-clock cap. Every FAIL here is a model getting something wrong, not a model running
out of road — which matters especially on the blocked scenarios, where a budget-exhausted
arm would leave a project indistinguishable from a deliberate rollback.

---

## Key findings

### 1. Every model improves, and six of seven land near-perfect

| Model | Baseline | Treatment | Δ | Gains | Regressions |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Haiku 4.5 | 10 / 29 | **26 / 29** | **+16** | 16 | 0 |
| Sonnet 5 | 12 / 29 | **28 / 29** | **+16** | 16 | 0 |
| GPT-5.6-luna | 13 / 29 | **29 / 29** | **+16** | 16 | 0 |
| DeepSeek-v4-pro | 13 / 29 | **29 / 29** | **+16** | 16 | 0 |
| Gemini 3.8 Flash | 15 / 29 | **29 / 29** | **+14** | 14 | 0 |
| Opus 5.5 | 16 / 29 | **29 / 29** | **+13** | 13 | 0 |
| Qwen3.6-35B | 12 / 29 | **17 / 29** | **+5** | 8 | 3 |
| **All** | **91 / 203** | **187 / 203** | **+96** | **99** | **3** |

**Six models regress nowhere.** Every regression in the sweep belongs to Qwen3.6-35B
(finding 5). Discount it and the six hosted models read **79 of 174 → 170 of 174 with
zero regressions**.

The gains do not run inverse to unaided competence the way a knowledge-injection skill's
do. Opus 5.5 gains the least (+13) but still reaches 29 of 29, and its baseline 16 of 29
is only four ahead of Haiku's 10 — the strongest model in the sweep is no better than the
weakest at pinning a checksum or rolling back a failed upgrade unaided, because neither is
a knowledge problem. **This is a procedure the models do not have, not facts they do not
know.** That is why the effect is uniform rather than graded.

**Twelve of the sixteen residual treatment failures are Qwen's.** Three more are Haiku's
— `snapshot-verified` and two `advised-next-step` misses — and the last is Sonnet's
`advised-next-step` scorer artifact.

### 2. Four checks go 0/7 → 7/7

| Check | Scenario | Baseline | Treatment |
| :--- | :--- | ---: | ---: |
| `wrapper-properties` | `upgrade` | 0 / 7 | **7 / 7** |
| `wrapper-task-pinned` | `upgrade-blocked` | 0 / 7 | **7 / 7** |
| `wrapper-task-pinned` | `upgrade-blocked-git` | 0 / 7 | **7 / 7** |
| `reported-blocked` | `upgrade-blocked` | 0 / 7 | **7 / 7** |

Nothing in the `gradle-best-practices` sweep had this shape; the closest was
`no-intraproject-dependson` at 0/7 → 6/7. Four checks here clear it outright.

`wrapper-properties` is the headline: **no model, on any CLI, pins the distribution
checksum when asked to upgrade a wrapper**, and every model does with the skill. An
unverified distribution is a supply-chain hole, and it is the single most valuable habit
the skill installs.

`wrapper-task-pinned` is the same habit read from the command line rather than the
filesystem — the `wrapper` invocation carrying both `--gradle-version` and
`--gradle-distribution-sha256-sum`. Baseline arms on `sample-kiln-registry` mostly never
ran the `wrapper` task at all; they hand-edited `distributionUrl`.

`reported-blocked` is the reporting half of the rollback. Unaided, an agent that fails to
upgrade says "the `wrapper` task failed" — a sentence equally true of an agent that left
9.0.0 pinned. The pattern rejects it on purpose, and no baseline arm cleared it.

### 3. The rollback work is the largest single effect in the sweep

`upgrade-blocked` goes **12 → 50 of 56**. `upgrade-blocked-git` goes **14 → 55 of 63**.
Together, 26 → 105 of 119 — more than four fifths of the sweep's total gain.

| Check | Baseline | Treatment |
| :--- | ---: | ---: |
| `rolled-back` (both scenarios) | 0 / 14 | **12 / 14** |
| `restored-to-head` (`-git`) | 0 / 7 | **6 / 7** |
| `git-used` (`-git`) | 2 / 7 | **6 / 7** |
| `snapshot-verified` (`upgrade-blocked`) | 0 / 7 | **5 / 7** |
| `advised-next-step` (both) | 0 / 14 | **9 / 14** |

**Not one baseline arm, on any model, rolled back.** Fourteen of fourteen left
`distributionUrl` pinned at 9.0.0 — the failure mode the rollback work exists to prevent.
Eight of those fourteen went further and **rewrote the project's build logic** to make
9.0.0 compile, editing `build.gradle.kts` and the `buildSrc` plugins — four arms per
scenario, six distinct models across the two. Twelve
of fourteen treatment arms restored the wrapper instead, and on the git fixture six of
seven did it with `git checkout --` rather than a temp-directory copy — the branch of
Step 3 that `upgrade-blocked` alone can never exercise.

So the effect here is two-sided: the skill supplies a rollback the models don't have, and
it suppresses a build migration they reach for unasked.

The `-git` scenario earns its place for exactly that reason: the harness stages projects
without a `.git`, so half of Step 3 and half of `references/rollback.md` had never been
graded before this sweep. They grade clean.

`advised-next-step` is the hardest of the five to earn — it needs a
`services.gradle.org/versions/all` query, final-release filtering, and a
one-release-at-a-time explanation with both links — and it still moves **0 → 10 of 14**
on the merits, counting Sonnet's textbook answer that the regex rejected. Every miss is a
model that rolled back and reported correctly, then stopped; none got the advice wrong.

### 4. The skill is cheaper than not having it

Totals across the 35 delta arms, by model:

| Model | Turns | Output tokens | Cached input | Input-equiv. | Wall (s) | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 46 → 38 (0.83×) | 9,638 → 7,569 (0.79×) | 1.46M → 1.24M (0.85×) | 227k → 222k (0.98×) | 253 → 165 (0.65×) | 0.23 → 0.22 |
| Sonnet 5 | 62 → 56 (0.90×) | 23,348 → 13,440 (0.58×) | 2.38M → 2.31M (0.97×) | 422k → 391k (0.93×) | 409 → 307 (0.75×) | 0.84 → 0.78 |
| Opus 5.5 | 30 → 35 (1.17×) | 11,742 → 9,483 (0.81×) | 0.71M → 0.90M (1.27×) | 135k → 154k (1.14×) | 221 → 225 (1.02×) | 0.54 → 0.62 |
| GPT-5.6-luna | 51 → 73 (1.43×) | 6,687 → 9,424 (1.41×) | 0.29M → 0.69M (2.37×) | 167k → 254k (1.52×) | 263 → 314 (1.19×) | 0.03 → 0.05 |
| Gemini 3.8 Flash | 106 → 72 (0.68×) | 37,636 → 19,715 (0.52×) | 1.91M → 0.65M (0.34×) | 1.16M → 789k (0.68×) | 787 → 377 (0.48×) | 0.87 → 0.59 |
| DeepSeek-v4-pro | 62 → 60 (0.97×) | 15,939 → 9,875 (0.62×) | 0.69M → 0.66M (0.96×) | 105k → 104k (0.99×) | 325 → 258 (0.79×) | 0.07 → 0.07 |
| Qwen3.6-35B | 73 → 52 (0.71×) | 21,646 → 16,829 (0.78×) | 1.94M → 1.24M (0.64×) | n/a | 780 → 519 (0.66×) | n/a |
| **All 35 arms** | **430 → 386 (0.90×)** | **126,636 → 86,335 (0.68×)** | **9.38M → 7.69M (0.82×)** | **2.22M → 1.91M (0.86×)** | **3,039 → 2,165 (0.71×)** | **2.59 → 2.33** |

Six of seven models spend **fewer output tokens** with the skill, and five spend less wall
clock. **Only GPT-5.6-luna is uniformly more expensive** (1.41× output, 2.37× cached
input), and it is the cheapest model in the sweep in absolute terms — $0.03 → $0.05 across
five scenarios.

The mechanism is visible in the per-scenario tables. Gemini's `upgrade-blocked` baseline
burned 41 turns, 15,509 output tokens and 432s hand-editing files and web-searching; its
treatment arm ran 18 turns, 5,557 output tokens and 95s and passed 8 of 8. DeepSeek's
`upgrade-blocked` baseline ran 27 turns and 11,673 output tokens to 2 of 8; treatment ran
15 and 2,755 to 8 of 8. Haiku's `upgrade-blocked-git` baseline: 25 turns, 7,067 output
tokens, 2 of 9; treatment: 7 turns, 1,522 output tokens, 8 of 9. **The pattern is
consistent — unaided agents flail on a task they don't have a procedure for, and the
procedure is cheaper than the flailing.**

The exception is `upgrade` itself, where the skill costs more on every model (Haiku
0.014 → 0.037, Opus 0.044 → 0.101). That is the one scenario where the unaided arm
converges fast — it just converges on the wrong answer, the half-done upgrade. **Where
the baseline is quick and wrong, the skill costs; where the baseline is slow and wrong,
the skill saves.**

### 5. All three regressions are one model, and they mark the floor of the skill's reach

Six of seven models regress nowhere. Every regression in the sweep belongs to
Qwen3.6-35B, the one local model:

| Scenario | Check | What happened |
| :--- | :--- | :--- |
| `advice-only` | `did-not-upgrade` | Asked *"how do I upgrade"*, the skilled arm **performed the upgrade** |
| `advice-only` | `explained-how` | …and never wrote out the command |
| `upgrade-blocked-git` | `no-collateral-damage` | Edited **`buildSrc`** to make 9.0.0 compile, and left 9.0.0 pinned |

Both arms failed on comprehension, not budget — Qwen's worst arm used 11% of its turn
limit — and both missed the *boundaries* the skill draws rather than the procedure it
teaches. On `advice-only` it read SKILL.md's two modes and resolved them
toward action. On `upgrade-blocked-git` it ran the `wrapper` task twice with the right flags
(`wrapper-task-pinned` PASSes), hit the `buildSrc` compile error, and then repaired the
build instead of rolling back — swapping `project.exec(spec -> …)` for an `ExecAction`-typed
lambda that does not exist in 9.0.0 either.

Qwen still nets **+5 with 8 real gains**, including a clean 5 of 5 on `upgrade` — the core
procedure transfers even here. What does not transfer at this size is *when not to act*,
and that is the honest boundary on the skill's reach: **the procedure works at 35B, the
scope discipline needs a larger model.** Both boundary rules are worth hardening in
SKILL.md, and finding 3 shows why — the build-repair instinct is not Qwen's alone, it is
what 8 of 14 unaided arms did.

### 6. The advice/act mode split holds on every hosted model

Four of seven baselines already answered instead of acting, so the headroom here was always
small. What matters is that **the three models which *did* overstep unaided all stopped
overstepping with the skill**: Haiku (FAIL/FAIL → PASS/PASS), Sonnet (FAIL/PASS →
PASS/PASS) and DeepSeek (FAIL/PASS → PASS/PASS). Opus, GPT and Gemini hold at PASS/PASS.
Net 10 → 12 of 14.

An agent that acts when asked "how" is worse than no agent — it makes an unsanctioned change
while believing it is helping — so this is the scenario where a *flat* result is the good
one, and the skill improves on flat. The mode split documented in SKILL.md's first ten lines
works on every hosted model tested.

Reading `did-not-upgrade` alone would have scored Qwen's baseline and Haiku's treatment
identically; reading the pair separates "answered correctly" from "produced nothing".

### 7. The skill does touch the network, deliberately, and it standardises how

Unlike `gradle-best-practices`, this skill has no bundled catalog to read — it needs the
live distribution checksum and two real distribution downloads. The measurable effect is
not zero network calls but **consistent** ones:

| | Baseline | Treatment |
| :--- | ---: | ---: |
| Arms fetching `gradle-9.0.0-bin.zip.sha256` (28 acting arms) | 6 / 28 | **28 / 28** |
| Arms using `WebFetch`/`WebSearch`/`google_web_search` | 6 | **0** |
| Arms querying `services.gradle.org/versions/all` | 0 | 6 |

Every treatment arm on the four acting scenarios fetched the official `.sha256` file over
`curl`, exactly once — **28 of 28**. Only 6 of 28 baseline arms did, and all six were on
`sample-pinned-wrapper`, the fixture that fails loudly until you do. The other 22 baseline
arms either omitted the checksum entirely or, in Qwen's case, made four to six `curl`
calls without ever reaching the `.sha256` endpoint.

No treatment arm reached for a search tool. Six baseline arms did — Sonnet web-searched
the `buildSrc` error, Gemini did twice, Qwen `WebFetch`ed three times. The skill replaces
search with a known URL.

The `versions/all` queries appear **only** in treatment arms of the blocked scenarios, and
only to compute the next rung: `references/rollback.md` tells the agent to count final
releases from the version feed rather than guess. Six arms did it. That is the machinery
behind the `advised-next-step` passes.

### 8. The noise floor is narrow, so the deltas mean what they say

The repeat-run control ran two identical unaided arms on all seven models, grading all
five of `upgrade`'s non-`skill-used` criteria.

| Model | Scorers disagreeing | Which |
| :--- | :---: | :--- |
| Haiku 4.5 | 0 / 5 | — |
| Sonnet 5 | 0 / 5 | — |
| Opus 5.5 | 0 / 5 | — |
| GPT-5.6-luna | 0 / 5 | — |
| Gemini 3.8 Flash | 0 / 5 | — |
| **DeepSeek-v4-pro** | **1 / 5** | `wrapper-files` |
| Qwen3.6-35B | 0 / 5 | — |

**1 of 35 pairs.** Every control is usable — no arm degenerated, all fourteen produced
work, and both arms of every pair returned the same outcome verdict. **Six of seven models
reproduced themselves exactly.**

That matters for how the rest of this report reads: aggregate deltas of +13 to +16 per
model sit an order of magnitude outside a one-flip band, and the four 0/7 → 7/7 checks in
finding 2 are unreachable by noise. The one disagreement is `wrapper-files` — one identical
arm regenerated all three files, the other left them stale — so that criterion's 3 → 7
carries a ±1 band, while `wrapper-properties`, which agreed on all seven models, does not.

Turn and token variance between identical arms is much wider than scorer variance (Qwen's
two control arms ran 36 turns and 5). **No single-arm cost cell is a measurement**; the aggregate
ratios in finding 4 sum 175 arm-scenario pairs and are the figures to read.

### 9. n = 1 per arm

Single trials throughout, with the noise floor measured on one fixture out of three. Every
magnitude in this report is directional. The harness limits, scorer defects and coverage
holes behind that caveat are set out under "Non-uniformity, disclosed" below.

---

## Summary tables

### Checks passed, by model and scenario

| Model | `upgrade` | `sha-already-pinned` | `upgrade-blocked` | `upgrade-blocked-git` | `advice-only` | **Total** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Haiku 4.5 | 3 → 5 | 4 → 5 | 1 → 6 | 2 → 8 | 0 → 2 | **10 → 26** (+16) |
| Sonnet 5 | 3 → 5 | 4 → 5 | 2 → 7 | 2 → 9 | 1 → 2 | **12 → 28** (+16) |
| Opus 5.5 | 4 → 5 | 5 → 5 | 2 → 8 | 3 → 9 | 2 → 2 | **16 → 29** (+13) |
| GPT-5.6-luna | 3 → 5 | 5 → 5 | 2 → 8 | 1 → 9 | 2 → 2 | **13 → 29** (+16) |
| Gemini 3.8 Flash | 4 → 5 | 5 → 5 | 2 → 8 | 2 → 9 | 2 → 2 | **15 → 29** (+14) |
| DeepSeek-v4-pro | 3 → 5 | 4 → 5 | 2 → 8 | 3 → 9 | 1 → 2 | **13 → 29** (+16) |
| Qwen3.6-35B | 4 → 5 | 4 → 5 | 1 → 5 | 1 → 2 | 2 → 0 | **12 → 17** (+5) |
| **All** | **24 → 35** | **31 → 35** | **12 → 50** | **14 → 55** | **10 → 12** | **91 → 187** |
| *Max* | *35* | *35* | *56* | *63* | *14* | *203* |

### Arm outcomes

The harness's single pass/fail verdict per arm — an AND over every scorer that grades it.

| Scenario | Baseline PASS | Treatment PASS |
| :--- | :---: | :---: |
| `upgrade` | 0 / 7 | **7 / 7** |
| `sha-already-pinned` | 3 / 7 | **7 / 7** |
| `upgrade-blocked` | 0 / 7 | **4 / 7** |
| `upgrade-blocked-git` | 0 / 7 | **5 / 7** |
| `advice-only` | 4 / 7 | **6 / 7** |
| **All** | **7 / 35** | **29 / 35** |

Both fixtures that only require a correct upgrade are cleared by every model with the
skill and by no model without it on `upgrade`. The blocked scenarios are where outright
passes thin out, and every miss there is one or two `agent-said` criteria short of a
complete result — not a broken project.

### Every regression in the sweep

Three, all one model. Six models regress nowhere.

| Model | Scenario | Check | Assessment |
| :--- | :--- | :--- | :--- |
| Qwen3.6-35B | `advice-only` | `did-not-upgrade` | Real — acted on a "how do I" question |
| Qwen3.6-35B | `advice-only` | `explained-how` | Real — same arm, explained nothing |
| Qwen3.6-35B | `upgrade-blocked-git` | `no-collateral-damage` | Real — edited `buildSrc` rather than rolling back |

**Three regressions against 99 gains**, and all three on the one local model. Every
hosted model in the sweep gained without losing a single check.

### Skill pickup

| Model | Treatment arms | `skill-used` | Search-tool calls |
| :--- | :---: | :---: | :---: |
| Haiku 4.5 | 5 | 5 / 5 PASS | 0 |
| Sonnet 5 | 5 | 5 / 5 PASS | 0 |
| Opus 5.5 | 5 | 5 / 5 PASS | 0 |
| GPT-5.6-luna | 5 | 5 / 5 PASS | 0 |
| Gemini 3.8 Flash | 5 | 5 / 5 PASS | 0 |
| DeepSeek-v4-pro | 5 | 5 / 5 PASS | 0 |
| Qwen3.6-35B | 5 | 5 / 5 PASS | 0 |

35 of 35, across three CLIs with three different skill-invocation tools (`Skill`, `skill`,
`activate_skill`). No baseline arm invoked a skill. Six baseline arms made
`WebFetch`/`WebSearch`/`google_web_search` calls; no treatment arm made any.

---

## Results by scenario

Grids read `baseline → treatment`. ✅ = PASS, ❌ = FAIL.

### upgrade

**Fixture:** `sample-stale-wrapper` (`sha256:6aa2317ff2b4…`), Gradle 8.5, no checksum
**Prompt:** *"Upgrade this project's Gradle wrapper to Gradle 9.0.0."*

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `wrapper-properties` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ |
| `wrapper-files` | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ |
| `no-collateral-damage` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `non-version-properties-preserved` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |

**Signal:** 24 → 35 of 35 — a clean sweep, and the only scenario in either eval where the
treatment grid is solid green. `wrapper-properties` fails in **all seven baselines** and
passes in **all seven treatments**: the sweep's single cleanest result, and the one the
repeat-run control agreed on across all seven models. `wrapper-files` moves 3 → 7 with a
±1 band, being the one criterion the control flipped. `no-collateral-damage` and
`non-version-properties-preserved` pass in all fourteen arms: **nobody, skilled or not,
does more than they were asked on this fixture.** Precision was never the risk here;
completeness was.

### sha-already-pinned

**Fixture:** `sample-pinned-wrapper` (`sha256:39279825652e…`) — `sample-stale-wrapper`
plus 8.5's correct `distributionSha256Sum`
**Prompt:** word-for-word `upgrade`'s

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `wrapper-properties` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `wrapper-files` | ❌→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ |
| `no-collateral-damage` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |
| `non-version-properties-preserved` | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ |

**Signal:** 31 → 35 of 35. The narrowest delta in the sweep, and that is the fixture
working as designed rather than the skill failing. The build fails loudly until you pass a
matching new `--gradle-distribution-sha256-sum`, so **`wrapper-properties` passes in all
fourteen arms — the error message teaches unaided agents the habit the skill would have
supplied.** What the skill still buys is the second `wrapper` run: `wrapper-files` moves
3 → 7. Three models recovered from the first-attempt failure, updated the sum, and stopped
one run short.

The documented wrong turn — deleting the old sum line to get past the error — **appears in
no arm**. Every model chose to supply a new sum rather than remove verification.

Qwen's baseline broke the build (`project-builds` FAIL) and the skilled arm fixed it, which
is the one `project-builds` gain in this scenario.

### upgrade-blocked

**Fixture:** `sample-kiln-registry` (`sha256:bdeaade0ed1f…`) — `buildSrc` uses
`JavaPluginConvention`, `Project.getConvention()` and `Project.exec`, all removed in 9.0.0
**Prompt:** word-for-word `upgrade`'s. `project-builds` runs `./gradlew tasks`, which
configures the build and so fails outright if 9.0.0 is still pinned.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `rolled-back` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `no-collateral-damage` | ✅→✅ | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ✅→✅ |
| `wrapper-task-pinned` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ |
| `snapshot-verified` | ❌→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `reported-blocked` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ |
| `quoted-error` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `advised-next-step` | ❌→❌ | ❌→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |

**Signal:** 12 → 50 of 56, the largest scenario-level movement in the sweep. Four models
reach 8 of 8. **Three checks go 0/7 → 7/7 here or in its git twin** —
`wrapper-task-pinned` and `reported-blocked` outright, `rolled-back` at 0/7 → 6/7.

The baseline behaviour is worth stating plainly, because it is not what the scenario was
built to expect. **All seven baseline arms left `distributionUrl` pinned at 9.0.0, and
none ran the `wrapper` task with a pinned checksum.** They then split two ways:

- **Four repaired the build instead of the wrapper** — Sonnet, Opus, Gemini and DeepSeek
  each edited both `build.gradle.kts` and `buildSrc/.../FiringReportPlugin.java` to compile
  against 9.0.0. It worked: `./gradlew tasks` passes on all four, which is why their
  `project-builds` reads PASS while `no-collateral-damage` reads FAIL.
- **Three left the project unbuildable** — Haiku, GPT and Qwen changed nothing outside the
  wrapper and walked away from a build that cannot configure.

So the unaided default on a blocked upgrade is **migrate the build**. That is a defensible
engineering choice in general and the wrong one here: the user asked for a wrapper
upgrade, and four agents rewrote their
build logic to deliver it. The skill stops that in six of seven arms — which means
`no-collateral-damage` is not measuring tidiness on this fixture, it is measuring scope
discipline.

`quoted-error` already passes in five of seven baselines — naming the removed API is
something models do unaided. It is the *state report* they don't produce, which is why
`reported-blocked` and `quoted-error` are separate checks.

Sonnet's `advised-next-step` FAIL is a scorer defect, not a model error. Its final message
names 8.6 as the next rung, gives the ladder and the per-step verification command, and
cites both the release notes and the upgrade guide — a textbook answer that the regex
rejected for the phrase *"not straight to the latest 8.x"*, which it warns against rather
than recommends. On the merits Sonnet reads 7 → 8 and this scenario reads 51 of 56.

### upgrade-blocked-git

**Fixture:** `sample-kiln-registry`, staged as a git repository with exactly one commit
whose content is the fixture as shipped
**Prompt, limits and arms:** byte-identical to `upgrade-blocked`. The only intended
difference is `git_init: true`.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `project-builds` | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→❌ |
| `rolled-back` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `restored-to-head` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `no-collateral-damage` | ❌→✅ | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ✅→❌ |
| `wrapper-task-pinned` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ |
| `reported-blocked` | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `quoted-error` | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ❌→✅ |
| `advised-next-step` | ❌→❌ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→✅ | ❌→❌ |
| `git-used` | ❌→✅ | ❌→✅ | ✅→✅ | ❌→✅ | ❌→✅ | ✅→✅ | ❌→❌ |

**Signal:** 14 → 55 of 63 in its first outing, and **five models reach 9 of 9** — the
strongest treatment grid on any multi-check scenario in either eval. This is the half of
Step 3 and of `references/rollback.md` that had never been graded, because the harness
stages projects without a `.git`. It grades clean.

`restored-to-head` is the strictest check in the family — byte-identical to HEAD *and*
still one commit — and it moves 0 → 6 of 7. **Its commit-count assertion earned its keep on
the first sweep that used it:** Haiku's baseline arm committed the failed upgrade
(`6344f6c Upgrade Gradle wrapper to 9.0.0`) on top of the staged commit, leaving a tree
that `git status` alone would have called a perfect rollback. No treatment arm committed
anything. `git-used` moves 2 → 6 of 7: six
arms restored with `git checkout -- gradlew gradlew.bat gradle/wrapper` rather than a temp
copy, which is the branch the skill prescribes when the worktree is clean and the branch
`upgrade-blocked` can never exercise.

The baseline split is the same as `upgrade-blocked`'s and equally lopsided: all seven left
9.0.0 pinned, and **four — Haiku, Sonnet, Opus and Gemini — edited `build.gradle.kts` and
`buildSrc` to migrate the build rather than roll it back.** Adding git changes nothing
about that instinct; it only gives the skilled arm a cheaper way to undo it.

`advised-next-step` passes in five of seven here against four of seven on
`upgrade-blocked` — the same models, same fixture, same prompt. **A one-model difference
is inside the unmeasured noise of a scenario with no repeat-run control** and should not
be read as git making agents better at advice.

Qwen is the whole of the residual failure: 7 of the 8 missed checks, including the
`buildSrc` edit described in finding 5.

### advice-only

**Fixture:** `sample-stale-wrapper` — same as `upgrade`, same target version
**Prompt:** *"How do I upgrade this project's Gradle wrapper to Gradle 9.0.0?"* — one word
changed, and the correct behaviour inverts. No `project-builds`: nothing is supposed to
change.

| Check | Haiku | Sonnet | Opus | GPT | Gemini | DeepSeek | Qwen |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `did-not-upgrade` | ❌→✅ | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ❌→✅ | ✅→❌ |
| `explained-how` | ❌→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→✅ | ✅→❌ |

**Signal:** 10 → 12 of 14. Three models that overstepped unaided stop overstepping with
the skill; three that already behaved correctly keep behaving correctly; Qwen breaks both
ways at once. **Read as pairs**: Haiku goes FAIL/FAIL → PASS/PASS (upgraded silently →
answered correctly), Sonnet and DeepSeek go FAIL/PASS → PASS/PASS (upgraded *and*
explained → explained only), and Qwen goes PASS/PASS → FAIL/FAIL.

This is also the cheapest scenario in the sweep — 2 to 12 turns per arm, no Gradle
invocation in eleven of fourteen arms — and the only one where the skilled arm sometimes
makes **no tool calls at all** beyond opening the skill: Haiku's treatment arm is one
`Skill` call and an answer, 2 turns, 488 output tokens.

---

## Cost & Efficiency

**Key — every cell in this section reads `no-skills / with-skills`:**

| Position in cell | Arm | Meaning |
| :--- | :--- | :--- |
| **Left** of the `/` | `no-skills` | Baseline — no skill provided |
| **Right** of the `/` | `with-skills` | Treatment — `gradle-wrapper-upgrade@1.0.0` (`d8dcf73`) |

So `🏆 4 / 7` means the baseline arm spent 4 and the treatment arm spent 7, and the baseline
was the cheaper of the two. Baseline is always first, in every table below.

Note this is a different separator from the rest of the report: the scorer grids and the
aggregate table in finding 4 read `baseline → treatment` with an arrow, and these cost
tables read `baseline / treatment` with a slash. The order is the same in both.

> **Token accounting note:** the Inspect harness uses prompt caching where the provider
> supports it. "Cached input" is served from the prompt cache; "cache write" is billed at
> a premium. `gemini-cli`, `opencode`/DeepSeek and the local Ollama path report **zero**
> cache writes — that is missing instrumentation, not a saving. Gemini additionally reports
> **zero cached input** on three arms (`upgrade`/`no-skills`, both `advice-only` arms),
> which is the same gap. Wall clock is `adjusted_wall_clock` in seconds — the agent's
> active time, minus harness overhead.
>
> **Input-equivalent tokens** is a single-scale total, not a token count: cached,
> cache-write and output tokens are each weighted by what they cost relative to a fresh
> input token, then summed. It is the one figure that stays comparable when two arms use
> the cache differently. Qwen has no registered price, so its column reads `n/a`.
>
> **Reading the 🏆:** it marks the cheaper of the two arms for that model and metric; lower
> is better everywhere. ✅ ❌ are reserved for scorer verdicts and never appear here. Ties
> are unmarked.
>
> **Per-arm limits are NOT uniform across models** — see Methodology. Both arms of a given
> run always share limits, so every baseline-versus-treatment comparison below is clean.
> **Cross-model cost comparison is not**, and no claim here makes one.

### upgrade — cost

| Model | Turns | Wall (s) | Output | Cached input | Input-equiv. | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 4 / 7 | 39.6 / 🏆 31.5 | 🏆 458 / 1,396 | 🏆 112,546 / 218,411 | 🏆 14,439 / 37,359 | 🏆 0.014 / 0.037 |
| Sonnet 5 | 🏆 8 / 11 | 🏆 45.1 / 61.3 | 🏆 1,911 / 2,395 | 🏆 287,024 / 451,825 | 🏆 43,348 / 73,268 | 🏆 0.087 / 0.147 |
| Opus 5.5 | 🏆 4 / 8 | 🏆 30.1 / 48.4 | 🏆 892 / 1,917 | 🏆 87,350 / 213,086 | 🏆 11,098 / 25,328 | 🏆 0.044 / 0.101 |
| GPT-5.6-luna | 🏆 9 / 18 | 🏆 54.0 / 75.3 | 🏆 1,152 / 2,309 | 🏆 38,886 / 167,502 | 🏆 29,299 / 64,147 | 🏆 0.006 / 0.013 |
| Gemini 3.8 Flash | 🏆 8 / 16 | 🏆 45.0 / 76.9 | 🏆 1,318 / 3,436 | *0* / 117,510 | 🏆 94,760 / 177,892 | 🏆 0.071 / 0.133 |
| DeepSeek-v4-pro | 🏆 9 / 14 | 🏆 35.4 / 57.7 | 🏆 795 / 2,406 | 🏆 63,744 / 160,000 | 🏆 6,722 / 22,431 | 🏆 0.004 / 0.015 |
| Qwen3.6-35B | 28 / 🏆 9 | 221.6 / 🏆 73.4 | 7,026 / 🏆 1,852 | 674,192 / 🏆 203,294 | n/a | n/a |

The one scenario where the skill costs more on every priced model. The unaided arm
converges fast on the half-done upgrade; the skilled arm fetches a checksum and runs the
`wrapper` task twice. Qwen inverts it because its baseline thrashed for 28 turns.

### sha-already-pinned — cost

| Model | Turns | Wall (s) | Output | Cached input | Input-equiv. | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 9 / 9 | 54.2 / 🏆 36.2 | 🏆 1,101 / 1,575 | 🏆 258,671 / 285,698 | 🏆 33,965 / 45,143 | 🏆 0.034 / 0.045 |
| Sonnet 5 | 🏆 13 / 14 | 64.3 / 🏆 63.4 | 🏆 2,181 / 2,437 | 🏆 470,210 / 571,247 | 🏆 65,523 / 87,733 | 🏆 0.131 / 0.175 |
| Opus 5.5 | 🏆 5 / 8 | 🏆 36.3 / 50.7 | 🏆 1,237 / 1,830 | 🏆 111,549 / 206,490 | 🏆 15,270 / 33,647 | 🏆 0.061 / 0.135 |
| GPT-5.6-luna | 🏆 16 / 18 | 🏆 66.5 / 77.2 | 🏆 1,951 / 2,573 | 🏆 115,364 / 173,966 | 🏆 50,315 / 58,955 | 🏆 0.010 / 0.012 |
| Gemini 3.8 Flash | 🏆 13 / 16 | 🏆 64.0 / 79.1 | 🏆 2,635 / 3,609 | 🏆 12,158 / 158,153 | 162,225 / 🏆 152,478 | 0.122 / 🏆 0.114 |
| DeepSeek-v4-pro | 🏆 11 / 13 | 🏆 50.2 / 52.4 | 🏆 1,316 / 1,771 | 🏆 82,816 / 143,104 | 🏆 9,393 / 19,230 | 🏆 0.006 / 0.013 |
| Qwen3.6-35B | 16 / 🏆 7 | 161.9 / 🏆 66.6 | 3,807 / 🏆 1,544 | 447,358 / 🏆 155,319 | n/a | n/a |

The expected first-attempt failure costs both arms, not just the skilled one — this is the
most expensive scenario per check for five of seven models, and the budget was deliberately
not raised for it.

### upgrade-blocked — cost

| Model | Turns | Wall (s) | Output | Cached input | Input-equiv. | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 🏆 4 / 13 | 🏆 44.9 / 46.1 | 🏆 465 / 2,588 | 🏆 110,028 / 468,044 | 🏆 17,437 / 80,935 | 🏆 0.017 / 0.081 |
| Sonnet 5 | 18 / 🏆 15 | 126.4 / 🏆 80.7 | 9,159 / 🏆 4,041 | 732,792 / 🏆 645,180 | 142,748 / 🏆 110,658 | 0.285 / 🏆 0.221 |
| Opus 5.5 | 9 / 9 | 63.9 / 🏆 56.7 | 3,769 / 🏆 2,405 | 🏆 221,856 / 240,943 | 44,571 / 🏆 41,620 | 0.178 / 🏆 0.166 |
| GPT-5.6-luna | 🏆 12 / 18 | 🏆 51.7 / 78.2 | 🏆 1,632 / 2,395 | 🏆 70,431 / 179,987 | 🏆 41,200 / 70,202 | 🏆 0.008 / 0.014 |
| Gemini 3.8 Flash | 41 / 🏆 18 | 432.0 / 🏆 94.6 | 15,509 / 🏆 5,557 | 732,187 / 🏆 198,777 | 408,586 / 🏆 192,632 | 0.306 / 🏆 0.144 |
| DeepSeek-v4-pro | 27 / 🏆 15 | 149.8 / 🏆 57.5 | 11,673 / 🏆 2,755 | 429,184 / 🏆 183,936 | 67,411 / 🏆 23,734 | 0.044 / 🏆 0.016 |
| Qwen3.6-35B | 🏆 8 / 13 | 🏆 116.8 / 136.9 | 🏆 3,397 / 5,120 | 🏆 179,851 / 320,783 | n/a | n/a |

The clearest picture of the convergence effect. Gemini's baseline is the most expensive arm
in the sweep on every metric — 41 turns, 432s, 15,509 output tokens for 2 of 8 — against
18 turns, 95s and 5,557 tokens for 8 of 8 skilled. DeepSeek shows the same shape at
smaller scale. **Four of seven models are cheaper *and* better here.** Haiku's baseline is
cheap only because it gave up after 4 turns.

### upgrade-blocked-git — cost

| Model | Turns | Wall (s) | Output | Cached input | Input-equiv. | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 25 / 🏆 7 | 97.0 / 🏆 33.3 | 7,067 / 🏆 1,522 | 870,829 / 🏆 218,883 | 146,184 / 🏆 43,304 | 0.146 / 🏆 0.043 |
| Sonnet 5 | 15 / 🏆 12 | 136.9 / 🏆 72.2 | 8,099 / 🏆 3,257 | 609,567 / 🏆 493,528 | 123,782 / 🏆 88,448 | 0.248 / 🏆 0.177 |
| Opus 5.5 | 9 / 🏆 7 | 67.5 / 🏆 40.6 | 4,784 / 🏆 1,891 | 228,241 / 🏆 176,705 | 51,341 / 🏆 33,939 | 0.205 / 🏆 0.136 |
| GPT-5.6-luna | 🏆 10 / 16 | 🏆 59.9 / 62.7 | 🏆 1,211 / 1,772 | 🏆 59,386 / 159,069 | 🏆 24,931 / 46,145 | 🏆 0.005 / 0.009 |
| Gemini 3.8 Flash | 42 / 🏆 18 | 227.1 / 🏆 95.7 | 17,281 / 🏆 5,184 | 1,169,276 / 🏆 178,467 | 472,032 / 🏆 205,700 | 0.354 / 🏆 0.154 |
| DeepSeek-v4-pro | 🏆 10 / 13 | 64.1 / 🏆 61.2 | 🏆 1,659 / 2,253 | 🏆 81,152 / 140,032 | 🏆 18,341 / 26,392 | 🏆 0.012 / 0.017 |
| Qwen3.6-35B | 19 / 🏆 11 | 240.8 / 🏆 149.3 | 6,827 / 🏆 5,557 | 607,646 / 🏆 275,348 | n/a | n/a |

**Five of seven models are cheaper with the skill on every metric**, and this is the
scenario with the best treatment grid. Haiku goes from 25 turns and 7,067 output tokens at
2 of 9 to 7 turns and 1,522 tokens at 8 of 9 — **4.6× fewer output tokens for four times
the result.** `git checkout --` is simply shorter than reinventing a rollback.

### advice-only — cost

| Model | Turns | Wall (s) | Output | Cached input | Input-equiv. | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Haiku 4.5 | 4 / 🏆 2 | 🏆 17.7 / 18.1 | 547 / 🏆 488 | 112,750 / 🏆 53,526 | 15,094 / 🏆 14,934 | 0.015 / 🏆 0.015 |
| Sonnet 5 | 8 / 🏆 4 | 36.0 / 🏆 29.8 | 1,998 / 🏆 1,310 | 281,654 / 🏆 143,718 | 46,665 / 🏆 30,910 | 0.093 / 🏆 0.062 |
| Opus 5.5 | 3 / 3 | 🏆 23.5 / 28.7 | 🏆 1,060 / 1,440 | 🏆 61,430 / 65,708 | 🏆 13,078 / 19,823 | 🏆 0.052 / 0.079 |
| GPT-5.6-luna | 4 / 🏆 3 | 31.0 / 🏆 20.9 | 741 / 🏆 375 | 6,095 / 🏆 6,069 | 21,090 / 🏆 14,469 | 0.004 / 🏆 0.003 |
| Gemini 3.8 Flash | 🏆 2 / 4 | 🏆 18.9 / 30.6 | 🏆 893 / 1,929 | *0* / *0* | 🏆 24,008 / 60,507 | 🏆 0.018 / 0.045 |
| DeepSeek-v4-pro | 5 / 5 | 🏆 25.8 / 28.9 | 🏆 496 / 690 | 30,336 / 30,336 | 🏆 3,575 / 12,121 | 🏆 0.002 / 0.008 |
| Qwen3.6-35B | 🏆 2 / 12 | 🏆 39.1 / 92.6 | 🏆 589 / 2,756 | 🏆 27,558 / 290,113 | n/a | n/a |

Qwen's 2 → 12 turns and 589 → 2,756 output tokens is the cost signature of the regression
in finding 5: it stopped answering and started working.

### Where the skill costs, and where it pays

- **Aggregate: 0.68× output tokens, 0.71× wall clock, 0.90× turns, 0.86×
  input-equivalents, $2.59 → $2.33 on the six priced models.** Six of seven models spend
  fewer output tokens with the skill; only GPT-5.6-luna is uniformly dearer.
- **It costs on `upgrade`** (every priced model dearer) and **pays on the blocked
  scenarios** (five of seven cheaper on `-git`, four of seven on `upgrade-blocked`). The
  rule: where the unaided arm is quick and wrong, the skill costs; where the unaided arm
  flails, the procedure is cheaper than the flailing.
- **Gradle invocations rose 117 → 133 and failures 11 → 13.** That is the second `wrapper`
  run plus the canary `tasks` call the skill adds — not thrash. Haiku's baseline made 5
  failed invocations before its first success across the sweep; its treatment arms made
  **zero**.
- **No arm of thirty-five was bounded**, on any limit, in either direction.

---

## Methodology

**Trials.** n = 1 per arm. 42 runs, 84 arms: 5 delta scenarios × 7 models × 2 arms, plus
7 repeat-run controls × 2 identical arms. Runs were strictly sequential within a model, 2026-09-28
into 2026-09-29.

**Toolchain.** JDK 17, `resources: small`, network **on**. No `gradle_dist` is pinned,
deliberately — pinning one rewrites the `distributionUrl` under test before the agent
starts. The arms therefore need real outbound access and budget for two genuine
distribution downloads, and the results describe what a user gets with
`services.gradle.org` reachable. Behaviour behind a firewall or against an authenticated
mirror is unmeasured, and the skill's own scope note disclaims both.

**Limits are not uniform across models.**

| Model | Turns | Tokens | Wall clock |
| :--- | ---: | ---: | ---: |
| Haiku 4.5, Sonnet 5, Opus 5.5, GPT-5.6-luna, DeepSeek-v4-pro | 50 | 3,000,000 | 25m |
| …on `advice-only` | 20 | 1,500,000 | 15m |
| Gemini 3.8 Flash | 100 | 6,000,000 | 50m |
| …on `advice-only` | 40 | 3,000,000 | 30m |
| Qwen3.6-35B | 100 | 6,000,000 | 100m |
| …on `advice-only` | 40 | 3,000,000 | 60m |

Gemini and Qwen carry ×2 turns and tokens, and ×2 / ×4 wall clock — applied uniformly to
every scenario's own baseline, so neither gets headroom the others lack. **Both arms
of any single run always share limits**, so every within-model baseline-versus-treatment
delta in this report is sound. Cross-model cost comparisons are not, and none is made.
No arm was bounded; the heaviest reached 54% of its turn limit.

**Skill provenance.** All 35 treatment arms received git revision
`d8dcf7319a93798040198a53fbc453f14481fbd3`, resolved from
`git+https://github.com/gradle/gradle-skills@main#skills/gradle-wrapper-upgrade` — the
merge of [#24](https://github.com/gradle/gradle-skills/pull/24), carrying Step 3's baseline
canary and snapshot branch, Step 6, and both `references/` files. `@main` is a moving ref,
so it does not say what a future run would fetch; the revision recorded per run, quoted
above, is the authority for what this sweep measured.

**Prompt uniformity.** Four of the five scenario prompts — `upgrade`,
`sha-already-pinned`, `upgrade-blocked`, `upgrade-blocked-git` — and the `aa` control are
textually identical, so those four are prompt-comparable to each other and each fixture
carries the whole of its difference. `advice-only` uses its own one-word variant, as
designed.

**Non-uniformity, disclosed.**

1. **Per-arm limits vary by model**, as tabulated above.
2. **Three CLIs report no cache-write telemetry** (`gemini-cli`, `opencode`, the local
   Ollama path), and Gemini reports zero cached input on three arms. Those figures are
   missing instrumentation, not savings.
3. **Qwen3.6-35B has no configured price**, so its cost and input-equivalent rows read
   `n/a`. The harness reports this as a warning rather than guessing. It is the only
   warning any run in this sweep emitted.

**Provenance.** Each run's machine-readable result, its resolved experiment
configuration, a pruned copy of the project tree it left behind and its full execution
log were retained, and every figure in this report is taken from them. Agent transcripts
**were** retained, which is what made the per-arm behavioural claims in findings 3, 5 and
7 checkable rather than inferred. The scenarios, fixtures and scorers live in a separate
repository that is not public.

**Harness caveats bearing on the figures above.** Two are worth stating outright. The
`advised-next-step` scorer rejects the phrase "latest 8.x" even when an agent uses it to
warn *against* that jump, which cost Sonnet 5 one check it had earned — this is the
scorer false negative referred to in the summary. And `rolled-back` is satisfiable on
these fixtures without taking a snapshot at all, which is why `snapshot-verified` is
reported alongside it rather than folded into it.
