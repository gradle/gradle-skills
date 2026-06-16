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

- Options may appear before or after task names.
- Value options accept `--opt value` or `--opt=value`; **`=` is recommended**.
- Boolean options have `--no-` inverses: `--build-cache` / `--no-build-cache`.
- Many long options have short forms: `-h`/`--help`, `-q`/`--quiet`, `-i`/`--info`, `-S`/`--full-stacktrace`, `-s`/`--stacktrace`, `-m`/`--dry-run`, `-t`/`--continuous`, `-x`/`--exclude-task`, `-D`/`--system-prop`, `-P`/`--project-prop`, `-I`/`--init-script`, `-g`/`--gradle-user-home`, `-p`/`--project-dir`, `-U`/`--refresh-dependencies`, `-a`/`--no-rebuild`, `-F`/`--dependency-verification`, `-M`/`--write-verification-metadata`, `-v`/`--version`, `-V`/`--show-version`.
- Many built-in flags can instead be set in `gradle.properties` (e.g. `org.gradle.caching=true`); CLI flags override file settings.

## Executing & selecting tasks

| Invocation | Meaning |
|---|---|
| `gradle :task` | Run `task` in the **root** project only. |
| `gradle task` | Run `task` in any project that defines it (ambiguous if multiple do). |
| `gradle :sub:task` / `gradle sub:task` | Run `task` in subproject `sub`. |
| `gradle t1 t2` | Run multiple tasks, honoring command-line order safety. |
| `gradle lib:che` | Name abbreviation — enough characters to be unique. |
| `gradle mAL:cT` | Camel-case abbreviation → `my-awesome-library:compileTest`. |

- `-x`, `--exclude-task <name>` — exclude a task (and only-its dependencies) from the run. Works with abbreviations.
- `--rerun-tasks` — ignore up-to-date checks; rerun the requested tasks and all dependencies.
- `--rerun` — built-in **task** option: rerun just that one task even if up-to-date.
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
| `--include-build <dir>` | Include another build as a composite build. |
| `--write-locks` | Persist lock state for all lockable resolved configurations. |
| `--update-locks <group:name>[,…]` | Update locked versions for specific modules (implies `--write-locks`). |
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
| `--max-workers <n>` | Cap parallel workers. Default = CPU count. |
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
| `-q`, `--quiet` | Errors only. |
| `-w`, `--warn` | Warnings and above. |
| `-i`, `--info` | Info — shows task/project name expansion, decisions, cache info. |
| `-d`, `--debug` | Debug (very verbose, includes stacktraces). |
| `--console=(auto\|plain\|colored\|rich\|verbose)` | Console output style. **`plain` = no color/progress bar, best for parsing.** `auto` (default) is plain when not attached to a terminal. |
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
| `-M`, `--write-verification-metadata <checksums>` | Generate checksums (e.g. `sha256`) into `verification-metadata.xml`. |
| `--refresh-keys` | Refresh trusted public keys. |
| `--export-keys` | Export trusted public keys. |

## Environment options

| Flag | Effect |
|---|---|
| `-g`, `--gradle-user-home <dir>` | Gradle user home. Default `~/.gradle`. |
| `-p`, `--project-dir <dir>` | Start directory for Gradle. Default current dir. |
| `--project-cache-dir <dir>` | Project-specific cache dir. Default `.gradle` in the root. |
| `-D`, `--system-prop <k>=<v>` | Set a JVM system property. |
| `-P`, `--project-prop <k>=<v>` | Set a root-project property. |
| `-I`, `--init-script <file>` | Run an initialization script. |
| `-Dorg.gradle.jvmargs=…` | JVM args for the build (heap, etc.). |
| `-Dorg.gradle.java.home=…` | JDK used to run Gradle. |

## Debugging & help options

| Flag | Effect |
|---|---|
| `-?`, `-h`, `--help` | Built-in CLI help. Combine with the `help` task for task-specific help. |
| `-v`, `--version` | Print version info and exit. |
| `-V`, `--show-version` | Print version info and continue executing. |
| `-s`, `--stacktrace` | Stacktrace for user exceptions (e.g. compile errors). |
| `-S`, `--full-stacktrace` | Full, very verbose stacktrace. |
| `-Dorg.gradle.debug=true` | Wait for a debugger to attach to the daemon (`localhost:5005` by default). |
| `-Dorg.gradle.debug.port=…`, `.host=…`, `.server=…`, `.suspend=…` | Tune remote debugging. |

## Task options

Task options are interpreted by the task, **must come immediately after the task name**, and are listed by `gradle help --task <name>`. Built-in task options available on every task currently include `--rerun`. Plugins add their own — e.g. `--tests` (Java test filtering), `--continuous` interactions, etc.

## Project reporting tasks

These are built-in *tasks* (not flags) that report on the build:

| Task | Shows |
|---|---|
| `projects` | Subproject hierarchy. |
| `tasks` | Main tasks (grouped). `--all` for everything; `--group="<g>"` to filter; `--provenance` to show what registered each. |
| `help --task <name>` | A task's path, type, options, and provenance. Add `--types`/`--no-types`. |
| `dependencies` | Dependency tree per configuration. |
| `dependencyInsight --dependency <d> --configuration <c>` | Why a particular dependency resolved as it did. |
| `buildEnvironment` | The buildscript (plugin) classpath dependencies. |
| `properties` | Project properties. `--property <name>` for one. |
| `wrapper` | Generate/upgrade the wrapper (see `wrapper.md`). |
| `init` | Scaffold a new build (`--type`, e.g. `java-library`, `java-application`). |
