# Gradle CLI — Version Matrix (7.0 → 9.x)

Use this to pick flags that actually exist in the project's Gradle version, and to verify against the exact release when it matters.

## How to verify against an exact version

Every published release has its own CLI and wrapper docs. Substitute the exact `X.Y.Z`:

- CLI: `https://docs.gradle.org/<version>/userguide/command_line_interface.html`
- Wrapper: `https://docs.gradle.org/<version>/userguide/gradle_wrapper.html`
- Release notes (deprecations/removals): `https://docs.gradle.org/<version>/release-notes.html`

Examples: `https://docs.gradle.org/8.0/userguide/command_line_interface.html`, `https://docs.gradle.org/8.14.4/userguide/command_line_interface.html`, `https://docs.gradle.org/9.3.0/userguide/command_line_interface.html`. `current` always points at the latest stable release.

**Determine the project version first:** read `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` (e.g. `gradle-8.14-bin.zip` → 8.14), or run `./gradlew --version`. Then fetch the matching doc above if you need certainty about a specific flag.

The single most reliable check is to ask the running Gradle itself: `./gradlew --help` lists every built-in option that build supports, and `./gradlew help --task=<name>` lists a task's own options. When in doubt, trust that over any table.

## Major.minor releases that have their own docs

```
7.0  7.1  7.2  7.3  7.4  7.5  7.6
8.0  8.1  8.2  8.3  8.4  8.5  8.6  8.7  8.8  8.9  8.10  8.11  8.12  8.13  8.14
9.0  9.1  9.2  9.3  9.4  9.5  9.6
```

Patch releases (e.g. `7.6.6`, `8.14.4`, `9.3.0`) also have docs at the same URL pattern. When a user names a patch version, use it verbatim in the URL.

## Notable flag availability

Most everyday flags — `build`, `test`, `--tests`, `--continue`, `--dry-run`, `--offline`, `--refresh-dependencies`, `--parallel`, `--max-workers`, `--build-cache`, logging (`-q/-i/-d/-s/-S`), `--console`, `--warning-mode`, environment (`-D/-P/-I/-g/-p`), daemon (`--daemon/--no-daemon/--status/--stop`), dependency verification (`-F/-M/--refresh-keys/--export-keys`), and `--write-locks`/`--update-locks` — are present across **all** of Gradle 7.0 → 9.x. Reach for the table below only for the flags that changed.

| Flag / behavior | Status across versions |
|---|---|
| `--configuration-cache`, `--no-configuration-cache` | Present and incubating throughout 7.x; promoted toward stable in the 8.x line. Behavior and problem strictness evolved — confirm against the project version's docs for serious use. |
| `--configuration-cache-problems=(fail\|warn)` | 7.x onward. |
| `--isolated-projects`, `--no-isolated-projects` | Incubating; introduced during the 8.x line and still incubating in 9.x. Implies `--configuration-cache`. Verify with `--help` on older 8.x. |
| `--problems-report`, `--no-problems-report` | Added mid-8.x (incubating); on by default in 9.x. Not present in early 7.x. |
| `--task-graph` | **Gradle 9.1.0+** only. |
| `--non-interactive` | Gradle 9.x line. Verify with `--help`; older versions simply don't prompt the same way. |
| `--watch-fs`, `--no-watch-fs` | Present 7.x→9.x; default-on where the OS supports it. |
| `--configure-on-demand`, `--no-configure-on-demand` | Present throughout (incubating). |
| Wrapper `--gradle-version` accepting a bare major/minor (e.g. `9`, `9.1`) | **Gradle 9+ only** (resolves to the latest matching release). On 7.x/8.x give a full version. |
| `gradle-wrapper.properties` `distributionUrl` version format | Since **Gradle 9.0** the file must use full `X.Y.Z`; bare major/minor is not accepted *in the file* (only on the CLI in 9+). |
| Wrapper `--network-timeout`, `--validate-url`/`--no-validate-url` | Present from 7.6 onward. |
| Wrapper `--retries`, `--retry-back-off-ms` | Recent additions; verify with `./gradlew help --task=:wrapper` on the project version. |

## Runtime / JVM requirements (affects whether a version even runs)

These bite when `./gradlew` fails before any task runs:

- **Gradle 7.x** runs on JDK 8–19 (exact upper bound varies by minor; 7.6 supports up to JDK 19).
- **Gradle 8.x** runs on JDK 8–21+ (later 8.x minors add newer JDKs; e.g. 8.5+ supports JDK 21).
- **Gradle 9.x** raised the **minimum** JDK to run Gradle to **17** (you can still *target*/compile for older Java via toolchains).

If a build fails immediately with an "unsupported class file / JVM version" style error, it's usually a Gradle-vs-JDK mismatch — check `./gradlew --version` (it prints the launcher JVM) against the version's compatibility matrix at `https://docs.gradle.org/<version>/userguide/compatibility.html`.

## When upgrading versions

**Upgrade one minor at a time.** At each step, run with `--warning-mode=all` and fix every deprecation before the next hop. Deprecations become removals at major boundaries (7→8, 8→9), so an unfixed warning today is a broken build later.

The **upgrade guides** are the actionable reference — more useful than the raw release notes:

- `https://docs.gradle.org/current/userguide/upgrading_version_8.html` — 8.x and to 9.x
- `https://docs.gradle.org/current/userguide/upgrading_version_7.html` — 7.x and to 8.x
