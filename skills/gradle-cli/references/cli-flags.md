# Gradle CLI — Complete Flag Reference

Grouped catalog of Gradle command-line options. Reflects the current release (Gradle 9.x); for which flags exist in a specific older version, see `version-matrix.md`. The authoritative page is https://docs.gradle.org/current/userguide/command_line_interface.html.

## Contents
- [Command structure](#command-structure)
- [Executing & selecting tasks](#executing--selecting-tasks)
- [Execution options](#execution-options)
- [Performance options](#performance-options)
- [Daemon options](#daemon-options)
- [Logging options](#logging-options)
- [Warning & problem reporting](#warning--problem-reporting)
- [Dependency verification options](#dependency-verification-options)
- [Environment options](#environment-options)
- [Debugging & help options](#debugging--help-options)
- [Task options](#task-options)
- [Project reporting tasks](#project-reporting-tasks)

## Command structure

```
gradle [taskName...] [--option-name...]
```

- Put built-in (Gradle) options **before** the task names, and each task's own options immediately **after** that task: `gradle [built-in options] task [task options]`.
- Always pass values with `=`: `--opt=value` (e.g. `--console=plain`). Use this form consistently and don't bother with the space-separated variant.
- Boolean options have `--no-` inverses: `--build-cache` / `--no-build-cache`.
- **The exit code is the source of truth for success: `0` = success, any non-zero = build failure.** Don't infer the outcome from log text (and note `--quiet` hides the `BUILD SUCCESSFUL`/`BUILD FAILED` line entirely).
- Common short forms: `-h`/`--help`, `-q`/`--quiet`, `-i`/`--info`, `-s`/`--stacktrace`, `-S`/`--full-stacktrace`, `-m`/`--dry-run`, `-t`/`--continuous`, `-D`/`--system-prop`, `-P`/`--project-prop`, `-I`/`--init-script`, `-g`/`--gradle-user-home`, `-p`/`--project-dir`, `-U`/`--refresh-dependencies`, `-F`/`--dependency-verification`, `-M`/`--write-verification-metadata`, `-v`/`--version`.
- Many built-in flags can instead be set in `gradle.properties` (e.g. `org.gradle.caching=true`); CLI flags override file settings.

### Passing multiple values

Gradle has **no single rule** for multi-value flags — each flag defines its own convention:

**Repeat the flag** (default assumption — most Gradle flags work this way):

```
./gradlew test --tests="com.pkg.Foo" --tests="com.pkg.Bar"
./gradlew -Dfoo=1 -Dbaz=2
./gradlew -I=init1.gradle -I=init2.gradle
```

Applies to `--tests`, `-D`/`--system-prop`, `-P`/`--project-prop`, `-I`/`--init-script`, `--include-build`.

**Comma-separated in one flag** — only where the reference table's placeholder shows `[,…]` (that notation is the tell):

```
./gradlew --update-locks=com.google.guava:guava,org.junit.jupiter:junit-jupiter
./gradlew -M=sha256,pgp   # --write-verification-metadata
```

Applies to `--update-locks`, `--write-verification-metadata`.

**When in doubt, repeat the flag.** It's the more common form, and it never breaks on values that legitimately contain a `,` or `:`. Only reach for the comma form when the flag's own help/docs explicitly show `[,…]`.

## Executing & selecting tasks

| Invocation | Meaning |
|---|---|
| `gradle :task` | Run `task` in the **root** project only. |
| `gradle :sub:task` | Run `task` in subproject `sub`. |
| `gradle t1 t2` | Run multiple tasks, honoring command-line order safety. |

Use the **full, exact** task and project names as `tasks` / `help` report them. Gradle also accepts abbreviated and camel-case names (e.g. `che`, `mAL:cT`) for interactive typing, but an agent should never use them — they can resolve to the wrong task or become ambiguous.

- `--rerun` — built-in **task** option: rerun just that one task even if up-to-date. A *targeted* `--rerun` is the right tool when you genuinely need to force a single task.
- `--rerun-tasks` — **avoid for normal builds.** Forces the requested tasks *and all their dependencies* to re-run; with the build cache enabled this is slower and more wasteful than `clean`. Use only as a last resort when diagnosing a build-logic bug (e.g. a missing task input/output declaration).
- `-x`, `--exclude-task=<name>` — **avoid — it's a trap.** Excluding a task silently drops its transitive dependencies too, so the resulting graph often skips work you didn't intend. Prefer invoking exactly the tasks you want.
- Disambiguation: `gradle [built-in-opts] -- [taskName] [--task-opts]` — the `--` delimiter forces following `--options` to be parsed as task options.

## Execution options

| Flag | Effect |
|---|---|
| `--continue` | Keep executing every runnable task after a failure; report all failures at the end. |
| `-m`, `--dry-run` | Disable all task actions; print the tasks that *would* run. |
| `--task-graph` | Disable task actions and print the task dependency graph. *(Gradle 9.1+)* |
| `-t`, `--continuous` | Re-execute the requested tasks whenever their file inputs change. |
| `--offline` | Build without accessing network resources (cached dependencies only). |
| `-U`, `--refresh-dependencies` | Refresh the state of dependencies (re-check remote metadata). |
| `--include-build=<dir>` | Include another build as a composite build. |
| `--write-locks` | Persist lock state for all lockable resolved configurations. |
| `--update-locks=<group:name>[,…]` | Update locked versions for specific modules (implies `--write-locks`). |
| `-a`, `--no-rebuild` | Don't rebuild project dependencies (e.g. `buildSrc`). Use with caution. |
| `--non-interactive` | Never prompt for input; use defaults. Good for CI / agents. *(recent — verify with `--help`)* |

## Performance options

| Flag | Effect |
|---|---|
| `--build-cache`, `--no-build-cache` | Toggle the build cache (reuse task outputs). Default off. |
| `--configuration-cache`, `--no-configuration-cache` | Toggle the configuration cache (reuse the configured task graph). Default off. |
| `--configuration-cache-problems=(fail\|warn)` | How the configuration cache treats problems. Default `fail`. |
| `--configure-on-demand`, `--no-configure-on-demand` | Configure only relevant projects. (Incubating.) |
| `--isolated-projects`, `--no-isolated-projects` | Configure projects in isolation/parallel; implies `--configuration-cache`. (Incubating.) |
| `--max-workers=<n>` | Cap parallel workers. Default = CPU count. |
| `--parallel`, `--no-parallel` | Build projects in parallel. Default off. |
| `--priority=(normal\|low)` | Scheduling priority for the daemon and its processes. |
| `--profile` | Write an HTML performance report under `build/reports/profile`. `--scan` is richer. |
| `--scan` | Publish a Build Scan with detailed diagnostics. **Uploads build data — get consent.** |
| `--watch-fs`, `--no-watch-fs` | File-system watching between builds. Enabled by default where supported. |

**Cache flag precedence (common confusion):** a CLI `--build-cache` / `--no-build-cache` overrides `org.gradle.caching` in `gradle.properties`. If the cache seems off despite `org.gradle.caching=true`, check for a `--no-build-cache` on the command line or in an init script, and confirm per-task cacheability.

## Daemon options

| Flag | Effect |
|---|---|
| `--daemon`, `--no-daemon` | Use (or don't use) the daemon for this build. Default on. |
| `--foreground` | Start a daemon in a foreground process. |
| `--status` | List running and recently stopped daemons **of the same Gradle version**. |
| `--stop` | Stop all daemons **of the same Gradle version**. |

Notes from the field: `--stop` and `--status` are scoped to the *same* Gradle version — a different version's daemons are unaffected, so on multi-version machines you may need to stop each version. Idle daemons self-expire (default 3h, `-Dorg.gradle.daemon.idletimeout=<ms>`) and also expire under memory pressure ("Expiring Daemon because JVM heap space is exhausted" → raise `org.gradle.jvmargs`).

## Logging options

Least → most verbose: `--quiet` < `--warn` < (default *lifecycle*) < `--info` < `--debug`.

| Flag | Effect |
|---|---|
| `-q`, `--quiet` | Errors only. Also suppresses the `BUILD SUCCESSFUL`/`BUILD FAILED` line — judge the outcome by the exit code, not the log. |
| `-w`, `--warn` | Warnings and above. |
| `-i`, `--info` | Info — shows task/project name expansion, decisions, cache info. |
| `-d`, `--debug` | Debug (very verbose, includes stacktraces). |
| `--console=plain` | **Use this whenever you'll parse the output.** No color or progress bar. (Default `auto` is plain when not attached to a terminal.) |
| `-Dorg.gradle.logging.level=…` | Set log level via property. |

`NO_COLOR` env var (non-empty) suppresses color regardless of console mode.

## Warning & problem reporting

| Flag | Effect |
|---|---|
| `--warning-mode=(all\|fail\|none\|summary)` | How warnings are logged. Default `summary`. `all` shows each (incl. deprecations); `fail` errors out on any warning. |
| `--problems-report`, `--no-problems-report` | Toggle `build/reports/problems-report.html`. On by default. (Incubating.) |

`--warning-mode=all` is the go-to for surfacing deprecation warnings before a major-version upgrade.

## Dependency verification options

| Flag | Effect |
|---|---|
| `-F=(strict\|lenient\|off)`, `--dependency-verification=…` | Verification mode. Default `strict`. |
| `-M`, `--write-verification-metadata=<checksums>` | Generate checksums (e.g. `sha256`) into `verification-metadata.xml`. |
| `--refresh-keys` | Refresh trusted public keys. |
| `--export-keys` | Export trusted public keys. |

## Environment options

| Flag | Effect |
|---|---|
| `-g`, `--gradle-user-home=<dir>` | Gradle user home. Default `~/.gradle`. |
| `-p`, `--project-dir=<dir>` | Start directory for Gradle. Default current dir. |
| `--project-cache-dir=<dir>` | Project-specific cache dir. Default `.gradle` in the root. |
| `-D`, `--system-prop=<k>=<v>` | Set a JVM system property. |
| `-P`, `--project-prop=<k>=<v>` | Set a root-project property. |
| `-I`, `--init-script=<file>` | Run an initialization script. |
| `-Dorg.gradle.jvmargs=…` | JVM args for the build (heap, etc.). |
| `-Dorg.gradle.java.home=…` | JDK used to run Gradle. |

## Debugging & help options

| Flag | Effect |
|---|---|
| `-?`, `-h`, `--help` | Built-in CLI help. Combine with the `help` task for task-specific help. |
| `-v`, `--version` | Print version info and exit. |
| `-s`, `--stacktrace` | Stacktrace for user exceptions (e.g. compile errors). |
| `-S`, `--full-stacktrace` | Full, very verbose stacktrace. |
| `-Dorg.gradle.debug=true` | Wait for a debugger to attach to the daemon (`localhost:5005` by default). |
| `-Dorg.gradle.debug.port=…`, `.host=…`, `.server=…`, `.suspend=…` | Tune remote debugging. |

## Task options

Task options are interpreted by the task, **must come immediately after the task name**, and are listed by `gradle help --task=<name>`. Built-in task options available on every task currently include `--rerun`. Plugins add their own — e.g. `--tests` (Java test filtering), `--continuous` interactions, etc.

## Project reporting tasks

These are built-in *tasks* (not flags) that report on the build:

| Task | Shows |
|---|---|
| `projects` | Subproject hierarchy. |
| `tasks` | Main tasks (grouped). `--all` for everything; `--group="<g>"` to filter; `--provenance` to show what registered each. |
| `help --task=<name>` | A task's path, type, options, and provenance. Add `--types`/`--no-types`. |
| `dependencies` | Dependency tree per configuration. |
| `dependencyInsight --dependency=<d> --configuration=<c>` | Why a particular dependency resolved as it did. |
| `buildEnvironment` | The buildscript (plugin) classpath dependencies. |
| `properties` | Project properties. `--property=<name>` for one. |
| `wrapper` | Generate/upgrade the wrapper (see `wrapper.md`). |
| `init` | Scaffold a new build (`--type=<type>`, e.g. `--type=java-library`, `--type=java-application`). |
