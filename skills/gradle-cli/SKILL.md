---
name: gradle-cli
description: "Run Gradle builds and tasks from the command line with `gradle` or the `./gradlew` wrapper, and produce the exact, copy-pasteable command for any Gradle invocation. Use this skill whenever the user is in a Gradle project and wants to RUN something with Gradle: build the project, run tests (e.g. 'run the JUnit tests', including `--tests` filters), run a built-in or project-custom task, list tasks, refresh dependencies, toggle the build/configuration cache, or add/upgrade the Gradle wrapper (`./gradlew wrapper --gradle-version`). Trigger on phrases like 'run the tests', 'build this project', 'run the X task', 'upgrade the gradle wrapper', 'how do I run …', 'what's the gradle command for …', 'invoke gradlew with …', or 'list the gradle tasks'. If the user says 'run X', run it; if they ask 'how do I run X', give them the copy-pasteable command with the right flags for their Gradle version. Also use it to choose the correct flags for a specific Gradle version (7.0 through 9.x) and to discover and invoke tasks custom to the current project. Do NOT use this skill to upgrade a system-installed Gradle distribution itself (SDKMAN/Homebrew/`brew upgrade gradle`), to diagnose WHY a build or test failed, or to author build scripts and plugins — it is about invoking the CLI, not installing Gradle, debugging failures, or writing build logic."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.0.0"
---

# Gradle CLI

Be an expert at the Gradle command line. This skill helps you run Gradle builds and tasks, and hand the user the precise command for whatever they want to do — using the flags that actually exist for *their* Gradle version, and the tasks that actually exist in *their* project.

## Two modes — match the user's verb

The user's phrasing tells you what they want:

- **"Run X", "build it", "run the tests", "upgrade the wrapper"** → an instruction to act. Orient yourself (below), then execute the command for them and report the outcome.
- **"How do I run X?", "what's the command for X?"** → a request for knowledge. Give a copy-pasteable command (prefer `./gradlew …`), explain the key flags in a sentence, and stop. Don't run it unless they ask.

When it's genuinely ambiguous, lean toward giving the command and offering to run it — that's cheap and reversible, whereas an unwanted `clean`, `publish`, or 20-minute build is not.

## Step 1 — Orient before you type

A correct Gradle command depends on three things you must establish first. Spend a moment here; it prevents wrong flags and "task not found" errors.

**1. Wrapper or system Gradle?** Look for `gradlew` / `gradlew.bat` in the project root. If present, **always prefer `./gradlew`** (`gradlew.bat` on Windows) over a system `gradle` — it pins the version the project was built against, so the build is reproducible. From a subproject directory, reference it relatively: `../gradlew`. Only fall back to `gradle` when there is no wrapper.

**2. What Gradle version does the project use?** Read `gradle/wrapper/gradle-wrapper.properties` and look at `distributionUrl` — e.g. `gradle-8.14-bin.zip` means the project is on 8.14. This determines which flags are valid. Run `./gradlew --version` to confirm the running version (and the JVM it uses).

**3. What Gradle is installed on the machine?** `gradle --version` (if on PATH) shows the system install. This matters when there's no wrapper yet, or when adding one. They can differ from the project version — that's normal and fine.

If a flag's availability depends on the version, consult `references/version-matrix.md` — it maps notable flags to the release that introduced them and gives the per-version documentation URL so you can verify against the exact `X.Y.Z`.

## Step 2 — Discover what you can actually run

Don't guess task names. Find out what the project offers, especially for custom tasks:

- `./gradlew tasks` — main tasks grouped by category, with descriptions.
- `./gradlew tasks --all` — every task, including dependencies and ungrouped/custom ones.
- `./gradlew tasks --group="build setup"` — just one group.
- `./gradlew help --task <name>` — full detail for one task: its type, **its task-specific options**, and where it was registered. Use this whenever you need a task's own `--options`.
- For custom tasks defined in the build, grep the build scripts (`build.gradle`, `build.gradle.kts`, files under `buildSrc/` and `build-logic/`) for `tasks.register(`, `tasks.create(`, or `task ` to see what exists and what options/inputs they expose.

Task and project **name abbreviation** works and is worth using: `gradle che` matches `check`; camel-case patterns expand too, so `./gradlew mAL:cT` runs `compileTest` in the `my-awesome-library` subproject. When abbreviating in scripts, prefer full names for clarity.

## Step 3 — Build the command

**Selecting tasks across a multi-project build:**

```
./gradlew :task            # task in the root project only
./gradlew task             # task in any project that defines it (ambiguous if several do)
./gradlew :sub:task        # task in subproject :sub
./gradlew test deploy      # several tasks, run in the order listed (with their deps)
./gradlew build -x test    # run build but EXCLUDE the test task (-x / --exclude-task)
```

**Task options go immediately after the task; built-in options can go anywhere:**

```
./gradlew test --tests "com.example.MyTest"        # --tests belongs to the test task
./gradlew --console=plain test --tests "*.MyTest"  # --console is a built-in (Gradle) option
```

If a task defines an option whose name collides with a built-in one (e.g. a task's own `--profile`), separate them with `--`: `./gradlew -- mytask --profile=value` passes `--profile` to the task.

The most common flags are summarized below; the full, grouped catalog of every CLI flag is in `references/cli-flags.md`. Read it when you need anything beyond the basics.

| Need | Flag | Notes |
|---|---|---|
| Preview what would run | `-m`, `--dry-run` | Runs nothing; lists the tasks. Great for checking a command before committing to it. |
| Ignore up-to-date checks | `--rerun-tasks` | Forces re-execution without deleting outputs (lighter than `clean`). |
| Keep going after a failure | `--continue` | Runs every still-runnable task, reports all failures at the end. |
| Parseable / log-friendly output | `--console=plain` | No progress bar or ANSI colors. **Prefer this when you (an agent) will parse the output.** |
| Quieter output | `-q` / `--quiet` | Errors only. Handy for `properties`/`dependencies` queries. |
| More detail when something's off | `-i`/`--info`, `-s`/`--stacktrace` | `--info` shows name-expansion and decisions; `--stacktrace` for exceptions. |
| Faster builds | `--build-cache`, `--parallel` | CLI flags override `gradle.properties`. See the cache note below. |
| Work without the network | `--offline` | Use cached dependencies only. |
| Force fresh dependency metadata | `--refresh-dependencies` | Re-checks remote versions; bypasses dependency caches. |

**Running as an agent (non-interactive):** when you execute Gradle yourself, add `--console=plain` so the output is clean to read. On recent Gradle (9.x) you can add `--non-interactive` to guarantee Gradle never blocks on a prompt (it uses defaults instead) — verify availability with `--help` if unsure. Leave the daemon at its default (on); it makes repeated runs faster. Reserve `--no-daemon` for genuinely one-shot/ephemeral environments.

## Common workflows

```
./gradlew build                          # assemble + run all checks (the usual "build everything")
./gradlew assemble                       # produce outputs, skip verification
./gradlew check                          # all verification tasks (tests + linters)
./gradlew test                           # run the test suite
./gradlew test --tests "com.pkg.MyTest"  # one class
./gradlew test --tests "com.pkg.MyTest.myMethod"   # one method
./gradlew test --tests "*Integration*"   # wildcard pattern
./gradlew :app:test                      # tests for the :app subproject only
./gradlew run                            # run an application (application plugin)
./gradlew clean                          # delete build outputs (destructive — see etiquette)
./gradlew dependencies                   # dependency tree, per configuration
./gradlew dependencyInsight --dependency guava --configuration compileClasspath
./gradlew projects                       # list the project/subproject hierarchy
./gradlew properties                     # project properties
./gradlew init                           # scaffold a new Gradle build
```

`-D` sets a JVM system property, `-P` a Gradle project property, `-I` an init script, `-g` the Gradle user home. Full environment/performance/logging/dependency-verification flags are in `references/cli-flags.md`.

## Wrapper operations

The wrapper is generated by the `wrapper` task, not downloaded. Use `:wrapper` (the `:` targets the root project, which is the only place the task belongs — this also avoids configuring other projects under configure-on-demand / isolated projects).

**Upgrade the wrapper** (the common request):

```
./gradlew wrapper --gradle-version latest      # newest stable
./gradlew wrapper --gradle-version 8.14.4      # a specific version
```

**Critical, and a frequent real-world trip-up:** the first run only updates `gradle-wrapper.properties`. To also refresh the `gradlew`/`gradlew.bat` scripts and `gradle-wrapper.jar` to that version's tuned versions, **run the same `wrapper` command a second time.** If you only edit `distributionUrl` by hand (or let a bot bump it), the scripts and jar go stale and Gradle prints persistent warnings — re-running the `wrapper` task is what clears them. Afterward, confirm with `./gradlew --version` and commit all wrapper files (including the `.jar`) to version control.

Wrapper specifics — `--gradle-distribution-sha256-sum` (checksums live at https://gradle.org/release-checksums/), `--distribution-type=all|bin`, private/authenticated distributions, JAR verification, and the Gradle 9 version-format change — are in `references/wrapper.md`. Read it for any wrapper task beyond a plain upgrade.

## Etiquette and safety

- **Some tasks are expensive or destructive.** `clean` discards cached outputs (slow next build); `publish`, `release`, `bootRun`, deploy tasks, and anything that pushes artifacts or runs servers have real side effects. For a "how do I" question just give the command. Before *running* one of these on the user's behalf, confirm — especially publish/release/deploy.
- **Don't add `--scan` silently.** A Build Scan uploads build data to a Develocity/`scans.gradle.com` server. Mention it as an option; only add it when the user agrees.
- **A long build is a side effect too.** If a command will clearly be slow (full `build`, `clean build`, large test suite) and the user only asked a question, prefer giving the command over launching it.
- **Honor command-line order safety:** `clean build` means clean *then* build; don't reorder for speed.

## When precision matters

For anything beyond the common cases, read the bundled references rather than guessing:

- `references/cli-flags.md` — the complete, grouped catalog of CLI flags (execution, performance, logging, daemon, environment, dependency verification, debugging, task options).
- `references/version-matrix.md` — which flags exist in which Gradle version (7.0 → 9.x), plus the per-version documentation URL so you can confirm against an exact release.
- `references/wrapper.md` — full wrapper reference: adding, using, upgrading, checksums, authenticated distributions, and JAR verification.

The canonical online reference for the current release is https://docs.gradle.org/current/userguide/command_line_interface.html.
