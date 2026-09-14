---
name: gradle-wrapper-upgrade
description: "Upgrade an existing Gradle wrapper to a new version with its SHA-256 pinned and the generated files actually refreshed, on Gradle 7.0–9.x. Use whenever the user asks to upgrade, bump, or update the Gradle wrapper, `gradlew`, `distributionUrl`, or the project's Gradle version."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.0.0"
---

# Gradle Wrapper Upgrade

Upgrading the wrapper means running the built-in `wrapper` task — never hand-editing files. `gradlew`, `gradlew.bat`, and `gradle-wrapper.jar` are generated: the next `wrapper` run overwrites them silently, so any hand-edit is lost without warning.

**Scope:** upgrading a wrapper that already exists. Adding one to a project that has none is a different job (`gradle :wrapper` from a system Gradle install).

## Two modes — match the user's verb

- **"Upgrade the wrapper", "bump Gradle to 8.14.4"** → act. Orient, run the task twice, verify, report the outcome.
- **"How do I upgrade the wrapper?"** → give the copy-pasteable commands, name the run-it-twice gotcha, stop.

If genuinely ambiguous, default to giving the commands.

## Step 1 — Orient

Confirm `gradlew` / `gradlew.bat` are in the project root. Read `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` for the current version (e.g. `gradle-8.14-bin.zip` → 8.14); `./gradlew --version` confirms the version actually running and the JVM.

This skill shows `./gradlew` (Unix/macOS/WSL/Git Bash). Windows cmd → `gradlew.bat`; PowerShell → `.\gradlew`. Options are identical.

## Step 2 — Get the target version's SHA-256

Pinning the checksum is a standard part of every upgrade, not an optional add-on — it is what verifies the download. Get it from:

- https://gradle.org/release-checksums/ (the full list), or
- the `-bin.zip.sha256` file next to the distribution at https://services.gradle.org/distributions/.

Gradle fails the build if the configured sum doesn't match the server's.

Once `distributionSha256Sum` is set in `gradle-wrapper.properties`, any later `wrapper` invocation that *changes* `--gradle-version` must also pass a matching new `--gradle-distribution-sha256-sum` — the build fails rather than silently reuse the old (now wrong) sum. If the version doesn't change, the existing sum is preserved automatically.

## Step 3 — Run the `wrapper` task twice

The leading `:` targets the root project — the only project the task belongs to, which also avoids configuring the others under configure-on-demand / isolated projects.

```
./gradlew :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
./gradlew :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
```

Same command, twice. Both runs are required — see below.

## Step 4 — Verify

```
./gradlew --version
```

It should report the target version. All four wrapper files are part of the upgrade: `gradle/wrapper/gradle-wrapper.properties`, `gradle/wrapper/gradle-wrapper.jar`, `gradlew`, `gradlew.bat`.

## Why run the task TWICE — the #1 real-world gotcha

The `wrapper` task always writes all four files, but `gradlew` / `gradlew.bat` / `gradle-wrapper.jar` come from the **currently running** Gradle's templates — not the target version.

- **First run** (under the old version): the properties point at the new version; the generated files are rewritten from the *old* templates, byte-identical to what was already there.
- **Second run** (auto-downloaded to the new version, because the properties changed): the generated files are rewritten from the *new* templates.

Symptoms of a half-done upgrade, very common in support questions: wrapper or deprecation warnings that won't go away, an odd-looking `gradlew` diff, or a bot (e.g. Dependabot) bumping `distributionUrl` without ever re-running the task. The fix is always the same: run `./gradlew :wrapper` twice.

## Version formats and labels

`--gradle-version` accepts the labels `latest`, `release-candidate`, `release-nightly`, `nightly`, and `release-milestone`. On **Gradle 9+** it also accepts a bare `9` or `9.1`, which resolves to the latest matching release; on 7.x/8.x give a full version.

Since **Gradle 9.0**, `gradle-wrapper.properties` must declare the version as a full `X.Y.Z` — a bare major or major.minor is not accepted *in the file*, even though the CLI's `--gradle-version` still takes them on 9+.

Discover the exact options your project's version supports with `./gradlew help --task=:wrapper`.

Canonical online: https://docs.gradle.org/current/userguide/gradle_wrapper.html.
