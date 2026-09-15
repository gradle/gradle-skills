---
name: gradle-wrapper-upgrade
description: "Use whenever the user asks to upgrade, bump, or update the Gradle wrapper, `gradlew`, `distributionUrl`, `gradle-wrapper.properties`, or the project's Gradle version, on Gradle 7.0–9.x. Not for adding a wrapper to a project that has none."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.0.0"
---

# Gradle Wrapper Upgrade

Upgrading means running the built-in `wrapper` task, never hand-editing files: `gradlew`, `gradlew.bat`, and `gradle-wrapper.jar` are generated, and the next `wrapper` run reverts any edit without warning. **Scope:** a wrapper that already exists — adding one to a project with none is a different job (`gradle :wrapper` from a system Gradle install).

## Two modes — match the user's verb

- **"Upgrade the wrapper", "bump Gradle to 8.14.4"** → act: work the steps, verify, report.
- **"How do I upgrade the wrapper?"** → give the commands, name the run-it-twice gotcha, stop.

If genuinely ambiguous, give the commands.

## Step 1 — Orient

Confirm `gradlew` is in the project root and read `distributionUrl` from `gradle/wrapper/gradle-wrapper.properties`. It carries both things you need: the **current version** (`gradle-8.14-bin.zip` → 8.14) and the **distribution type** (`-bin` or `-all`).

Commands below are `./gradlew` (Unix/macOS/WSL/Git Bash); Windows cmd → `gradlew.bat`, PowerShell → `.\gradlew`. Options are identical.

## Step 2 — Pin the target version and its checksum

Use the version the user named. **If they named none, upgrade to the latest release**, resolved to a concrete version:

```
curl -s https://services.gradle.org/versions/current     # → version + checksumUrl
```

Resolve before you pin — no checksum can be looked up for `--gradle-version=latest`. Pinning the sum is standard on every upgrade, not an add-on; it is what verifies the download. Take it from that `checksumUrl`, or from https://gradle.org/release-checksums/.

**Match the sum to the zip named in `distributionUrl`.** Each release publishes separate sums for the `-bin` zip, the `-all` zip, and the wrapper JAR. The wrong one fails with `Verification of Gradle distribution failed!`, which reads like a tampered download rather than the copy-paste error it usually is.

Once `distributionSha256Sum` is set, any later `wrapper` run that *changes* `--gradle-version` must pass a new matching sum — the build fails rather than reuse the stale one. If the version doesn't change, the sum is preserved automatically.

## Step 3 — Run the `wrapper` task twice

```
./gradlew --console=plain :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
./gradlew --console=plain :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
```

Same command, twice: the first regenerates the scripts and jar from the *old* Gradle's templates, the second from the new version's. Both are required — see below. The leading `:` targets the root project, the only one the task belongs to.

**An upgrade never changes the distribution type.** `-all.zip` in Step 1 → add `--distribution-type=all` to both runs; the task defaults to `bin` and will otherwise switch the project silently. Changing type is the user's decision, not a side effect of an upgrade.

Running as an agent:

- **Trust the exit code; never grep for `BUILD SUCCESSFUL`.** A failed checksum must not read as a successful upgrade.
- **The second run downloads the full distribution (100 MB+).** A long silence is normal, not a hang — abandoning it leaves exactly the half-done state described below.
- **`--console=plain`** keeps the output parseable: no progress bar, no colors.

## Step 4 — Verify

```
git status --short gradle/wrapper gradlew gradlew.bat
```

On a real version change, all four files show as modified: `gradle-wrapper.properties`, `gradle-wrapper.jar`, `gradlew`, `gradlew.bat`. **Only the properties moved → the second run didn't happen.** Then `./gradlew --version` should report the target version. That check can't stand alone: the version it prints comes from `distributionUrl`, so it looks correct even while the scripts and jar are stale.

## Why run the task TWICE — the #1 real-world gotcha

The task always writes all four files, but the scripts and jar come from the **currently running** Gradle's templates, not the target version's. Run 1 (still the old Gradle) points the properties at the new version and rewrites the generated files from the *old* templates — usually reproducing what was already there, which is also where a hand-edited `gradlew` quietly disappears. Run 2 auto-downloads the new version, because the properties changed, and rewrites them from the *new* templates.

Symptoms of a half-done upgrade, very common in support questions: wrapper or deprecation warnings that won't go away, an odd-looking `gradlew` diff, or a bot (e.g. Dependabot) bumping `distributionUrl` without ever running the task. The fix is always the same — run it twice.

## Version formats

`--gradle-version` also accepts `latest`, `release-candidate`, `release-nightly`, `nightly`, and `release-milestone`, plus a bare `9` or `9.1` on **Gradle 9+**; prefer a concrete version whenever you are pinning a checksum. Since **Gradle 9.0**, `gradle-wrapper.properties` must state a full `X.Y.Z` — a bare major or major.minor is rejected *in the file*, though the CLI still accepts it. Confirm your version's options with `./gradlew help --task=:wrapper`.

## Out of scope

A mechanically correct upgrade can still leave a build that doesn't run: new versions remove deprecated APIs, raise the minimum JVM, and break plugins that haven't caught up. That is an expected outcome, not a failed upgrade. Finish and verify the wrapper upgrade, then report any build failure as the separate problem it is.

Canonical: https://docs.gradle.org/current/userguide/gradle_wrapper.html.
