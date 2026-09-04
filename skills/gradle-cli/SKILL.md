---
name: gradle-cli
description: "Produce or run the exact `./gradlew` command for any Gradle CLI invocation on Gradle 7.0–9.x. Use whenever the user asks to build, test, run a task, list tasks, refresh dependencies, or add/upgrade the wrapper."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.3.0"
---

# Gradle CLI

## Two modes — match the user's verb

- **"Run X", "build it", "upgrade the wrapper"** → act. Orient (below), execute, report the outcome.
- **"How do I run X?", "what's the command for X?"** → give the copy-pasteable `./gradlew …` command, name the key flags, stop.

If genuinely ambiguous, default to giving the command — don't launch on a maybe.

## Step 1 — Orient before you type

**1. Wrapper or system Gradle?** Look for `gradlew` / `gradlew.bat` in the project root. If present, **always prefer the wrapper** — it pins the version the project was built against. From a subproject dir, reference it relatively (e.g. `../gradlew`). Only fall back to system `gradle` (check `gradle --version`) when there's no wrapper.

This skill shows `./gradlew` (Unix/macOS/WSL/Git Bash). Windows cmd → `gradlew.bat`; PowerShell → `.\gradlew`. Flags, tasks, and options are identical.

**2. What Gradle version?** Read `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` (e.g. `gradle-8.14-bin.zip` → 8.14). `./gradlew --version` confirms the running version and JVM. For anything version-specific (which flags exist in that version, per-version doc URLs), consult `references/version-matrix.md`.

## Step 2 — Discover what you can actually run

- `./gradlew tasks` — main tasks by category.
- `./gradlew tasks --all` — every task (incl. custom, ungrouped).
- `./gradlew tasks --group="build setup"` — one group.
- `./gradlew help --task=<name>` — one task's type, options, provenance.
- For custom tasks, grep `buildSrc/`, `build-logic/`, and build scripts for `tasks.register(` / `tasks.create(`.

**Use full, exact task and project names — never abbreviations** (e.g. `che` for `check`, `:mA:cT` for `:myApp:compileTest`). They can silently resolve to the wrong task.

## Step 3 — Build the command

**Order: built-in options → task names → each task's own options right after its task.**

```
./gradlew [built-in options]  task1 [task1 options]  task2 [task2 options]
```

```
./gradlew --console=plain test --tests="com.example.MyTest"
#         └ built-in option   └ task └ task option (belongs to test)
```

If a task option collides with a built-in one, put `--` before the task names: `./gradlew -- mytask --profile=value`.

**Selecting tasks across a multi-project build:**

```
./gradlew :task            # task in the root project only
./gradlew :sub:task        # task in subproject :sub
./gradlew :t1 :t2          # several tasks, in the order listed
```

Common built-in options (full catalog: `references/cli-flags.md`):

| Need | Flag | Notes |
|---|---|---|
| Preview what would run | `--dry-run` (`-m`) | Runs nothing; lists the tasks. |
| Keep going after a failure | `--continue` | Reports all failures at the end. |
| Parseable / log-friendly output | `--console=plain` | No progress bar or colors. |
| See what's happening | `--info` (`-i`), `--stacktrace` (`-s`) | Cache info; stack traces on failure. |
| Faster builds | `--build-cache`, `--parallel` | CLI overrides `gradle.properties`. |
| Work offline | `--offline` | Cached dependencies only. |
| Force fresh dependency metadata | `--refresh-dependencies` | Bypasses dependency caches. |

**Running as an agent (non-interactive):**

- Prefer the project root; use `-p=<dir>` or `../gradlew` from a subproject. Add `--console=plain`.
- **Trust the exit code, not the log text:** `0` = success, non-zero = failure. Never grep for `BUILD SUCCESSFUL`/`BUILD FAILED` — `--quiet` suppresses it.
- On Gradle 9.x, add `--non-interactive` to skip prompts (verify with `--help`).
- Leave the daemon on (default); reserve `--no-daemon` for one-shot environments.
- **Avoid** `--rerun-tasks` (slower than `clean` with build cache on).
- **`-x`/`--exclude-task` prunes more than the task you name.** Excluding `T` also drops every task reachable *only* through `T` — its private dependencies. `assemble` has the same hole: it skips everything hanging off `check`, not just the tests. So "build without tests" is a two-step check, never a rule of thumb:
  1. Run both dry runs (each prints one `:task SKIPPED` line per task; they only configure, so this costs seconds):
     ```
     ./gradlew build --dry-run            # the full task list
     ./gradlew build -x test --dry-run    # what -x leaves of it
     ```
  2. Every task in the first list and missing from the second is one of two things. A **test task** is a task whose *name* says so: exactly `test`, `testClasses`, or a `compile…Test…`/`process…Test…` variant. **Everything else is collateral, whatever its name suggests** (`generateSbom`, `generateDocs`, `copyFixtures`): `test` needed it, but it is not a test, and the user asked for everything else. Add each collateral task back by name — `./gradlew build -x test generateSbom` — and say so in your answer. When unsure, add it back: an extra cheap task is harmless, a missing output is not.

  Never answer "build without tests" with a bare `assemble` or a bare `-x test`, and never skip the second dry run.

## Common workflows

```
./gradlew build                          # assemble + run all checks
./gradlew assemble                       # produce outputs, skip verification
./gradlew check                          # all verification tasks (tests + linters)
./gradlew test                           # run the test suite
./gradlew test --tests="com.pkg.MyTest"            # one class
./gradlew test --tests="com.pkg.MyTest.myMethod"   # one method
./gradlew test --tests="*Integration*"             # wildcard pattern
./gradlew :app:test                      # tests for the :app subproject only
./gradlew run                            # run an application (application plugin)
./gradlew clean                          # delete build outputs (destructive)
./gradlew dependencies                   # dependency tree per configuration
./gradlew dependencyInsight --dependency=guava --configuration=compileClasspath
./gradlew projects                       # project/subproject hierarchy
./gradlew properties                     # project properties
./gradlew init                           # scaffold a new build (empty dir; prompts otherwise)
```

`-D` sets a JVM system property (`-Dorg.gradle.jvmargs=-Xmx4g`), `-P` a Gradle project property (`-PapiKey=abc`), `-I` an init script (`-I=init.gradle.kts`), `-g` the Gradle user home (`-g=/tmp/gradle-home`).

## Wrapper operations

The wrapper is generated by the `:wrapper` task (`:` targets the root project — the only place it belongs).

**Upgrade** — pin the version *and* its SHA-256, run twice:

```
./gradlew :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
./gradlew :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
./gradlew --version
```

Get `<sha256>` from https://gradle.org/release-checksums/. Both runs write all four files, but `gradlew`/`gradlew.bat`/`gradle-wrapper.jar` come from the running Gradle's templates — only the second run refreshes them under the new version. Commit all four.

See `references/wrapper.md` for labels, private distributions, JAR verification, and the Gradle 9 version-format change.

## Etiquette and safety

- **Identify destructive/expensive tasks by reading their descriptions** (`./gradlew tasks`, `./gradlew help --task=<name>`). Danger signals in the output: task names like `publish…ToXRepository` or `bootRun`, and descriptions leading with Publishes/Deploys/Releases/Deletes/Runs. For example:
  ```
  publishAllPublicationsToMavenCentralRepository - Publishes all Maven publications ... to mavenCentral.
  clean - Deletes the build directory.
  bootRun - Runs this project as a Spring Boot application.
  ```
  When acting on the user's behalf, do not run these — print the command and stop, whether or not a user is available to confirm.
- **Don't add `--scan` silently.** A Build Scan uploads data; get consent.
- **A long build is a side effect too.** Treat `build`/`check`/`test`/`assemble`/`clean`/`dependencies` as slow — for "how do I" questions, give the command and stop, even if the verb sounded like "run it."
- **Command-line order safety:** `clean build` means clean *then* build; don't reorder.

## References

- `references/cli-flags.md` — complete grouped flag catalog.
- `references/version-matrix.md` — which flags exist in which version (7.0 → 9.x) + per-version doc URLs.
- `references/wrapper.md` — full wrapper reference.

Canonical online: https://docs.gradle.org/current/userguide/command_line_interface.html.
