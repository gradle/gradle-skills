---
name: gradle-cli
description: "Run any Gradle build from the command line"
license: Apache-2.0
metadata:
  author: gradle
  version: "1.2.0"
---

# Gradle CLI

## Two modes — match the user's verb

- **"Run X", "build it", "upgrade the wrapper"** → act. Orient (below), execute, report the outcome.
- **"How do I run X?", "what's the command for X?"** → give the copy-pasteable `./gradlew …` command, name the key flags, stop.

If genuinely ambiguous, give the command *and* offer to run it.

## Step 1 — Orient before you type

**1. Wrapper or system Gradle?** Look for `gradlew` / `gradlew.bat` in the project root. If present, **always prefer the wrapper** — it pins the version the project was built against. From a subproject dir, reference it relatively (e.g. `../gradlew`). Only fall back to system `gradle` (check `gradle --version`) when there's no wrapper.

This skill shows `./gradlew` throughout (Unix/macOS/WSL/Git Bash). Translate for the user's shell: **Windows cmd** → `gradlew.bat`; **PowerShell** → `.\gradlew`. Flags, tasks, and task options are identical.

**2. What Gradle version?** Read `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` (e.g. `gradle-8.14-bin.zip` → 8.14). `./gradlew --version` confirms the running version and JVM.

## Step 2 — Discover what you can actually run

- `./gradlew tasks` — main tasks by category.
- `./gradlew tasks --all` — every task (incl. custom, ungrouped).
- `./gradlew tasks --group="build setup"` — one group.
- `./gradlew help --task=<name>` — one task's type, options, provenance.
- For custom tasks, grep `buildSrc/`, `build-logic/`, and build scripts for `tasks.register(` / `tasks.create(`.

**Use full, exact task and project names — never abbreviations** (e.g. `che`, `mAL:cT`). They can silently resolve to the wrong task.

## Step 3 — Build the command

**Order: built-in options first, then task names, then each task's own options right after its task.**

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

- Run from the project root with `--console=plain`.
- **Trust the exit code, not the log text:** `0` = success, non-zero = failure. Never grep for `BUILD SUCCESSFUL`/`BUILD FAILED` — `--quiet` suppresses it.
- On Gradle 9.x, add `--non-interactive` to skip prompts (verify with `--help`).
- Leave the daemon on (default); reserve `--no-daemon` for one-shot environments.
- When some tasks are excluded via the `-x`/`--exclude-task`, you need to check if their transitive dependencies produce build outputs. A transitive dependency is another task which is wired to run whenever the task to be excluded is run, hence it won't run either when you add the exclusion. The transitive dependencies that produce build outputs/artifacts will need to be run explicitly. Let's say you need to exclude the task `test`. You would do that with `-x test`. But before you do run `test --console plain --dry-run` to obtain the list of its transitively dependant tasks and check them.
- **Avoid** `--rerun-tasks` (slower than `clean` with build cache on).

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
./gradlew init                           # scaffold a new build
```

`-D` sets a JVM system property, `-P` a Gradle project property, `-I` an init script, `-g` the Gradle user home.

## Wrapper operations

The wrapper is generated by the `:wrapper` task (`:` targets the root project — the only place it belongs).

**Upgrade** — pin the version *and* its SHA-256, run twice:

```
./gradlew :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
./gradlew :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
./gradlew --version
```

Get `<sha256>` from https://gradle.org/release-checksums/. The first run updates `gradle-wrapper.properties` only; the second (running under the new version) refreshes `gradlew`/`gradlew.bat` and `gradle-wrapper.jar`. Commit all four files.

See `references/wrapper.md` for labels, private distributions, JAR verification, and the Gradle 9 version-format change.

## Etiquette and safety

- **Identify destructive/expensive tasks by reading their descriptions** (`./gradlew tasks`, `./gradlew help --task=<name>`). Verbs like "publishes", "deploys", "releases", "deletes", "starts" signal remote-state changes, deleted outputs, or long-running processes. For "how do I" questions, hand over the command; confirm before running one on the user's behalf.
- **Don't add `--scan` silently.** A Build Scan uploads data; get consent.
- **A long build is a side effect too.** If a command will be slow and the user only asked a question, give the command instead of launching it.
- **Command-line order safety:** `clean build` means clean *then* build; don't reorder.

## References

- `references/cli-flags.md` — complete grouped flag catalog.
- `references/version-matrix.md` — which flags exist in which version (7.0 → 9.x) + per-version doc URLs.
- `references/wrapper.md` — full wrapper reference.

Canonical online: https://docs.gradle.org/current/userguide/command_line_interface.html.
