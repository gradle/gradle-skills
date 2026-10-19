---
name: gradle-wrapper-upgrade
description: "Use whenever the user asks to upgrade, bump, or update the Gradle wrapper, `gradlew`, `distributionUrl`, `gradle-wrapper.properties`, or the build's Gradle version, on Gradle 7.0–9.x — or asks *how* that is done. Covers both modes: 'upgrade the wrapper' means perform it; a 'how do I upgrade' question is answered with the copy-pasteable commands rather than by running them. Not for adding a wrapper to a build that has none."
license: Apache-2.0
metadata:
  author: gradle
  version: "1.1.0"
---

# Gradle Wrapper Upgrade

## Two modes — match the user's verb

Decide this first; everything below is conditional on it.

- **"Upgrade the wrapper", "bump Gradle to 8.14.4"** → act: work the steps, verify, report.
- **"How do I upgrade the wrapper?"** → give the commands, name the run-it-twice gotcha, stop. A "how" question is answered, not executed — including when you have already opened with "I'll upgrade the wrapper." Say the commands; do not run them.

If genuinely ambiguous, give the commands.

The steps below are the same material either way: in act mode you run them, in answer mode you hand them over — all but the snapshot. Leave out Step 3's copy and Step 5's `diff` and delete when answering: they exist so an agent can undo its own work, and a person has their own version control. Drop the `cd "<build-root>" &&` prefix too: a person runs them from the build root.

Upgrading means running the built-in `wrapper` task, never hand-editing files: `gradlew`, `gradlew.bat`, and `gradle-wrapper.jar` are generated, and the next `wrapper` run reverts any edit without warning. **Scope:** a wrapper that already exists — adding one to a build with none is a different job (`gradle :wrapper` from a system Gradle install).

Two references ship beside this file: **`references/snapshot.md`** (Step 3 — securing the wrapper before every upgrade) and **`references/rollback.md`** (Step 6 — undoing an upgrade the build cannot take, a branch most upgrades never hit). **Open either only when the step says to.**

## Step 1 — Orient

Find the build root — the directory holding `gradle/wrapper/gradle-wrapper.properties`, normally beside `gradlew` — and read `distributionUrl` from that file. It carries both things you need: the **current version** (`gradle-8.14-bin.zip` → 8.14) and the **distribution type** (`-bin` or `-all`).

**Note the build root's absolute path** (`pwd` there). It is `"<build-root>"` in every command below — every `./gradlew` run, and every snapshot, verify, restore and delete — so each acts on this build from whatever directory your shell is in. A repository can hold more than one build, each with a wrapper of its own.

**Act mode needs a POSIX shell** — macOS, Linux, or WSL or Git Bash on Windows. The snapshot, verification and rollback are POSIX commands. In native cmd or PowerShell, do not upgrade and do not translate them into `Copy-Item` or `Remove-Item`: give the commands as in answer mode and say they need WSL or Git Bash.

Commands below are `./gradlew`; a user running them by hand in Windows cmd uses `gradlew.bat`, in PowerShell `.\gradlew`. Options are identical.

## Step 2 — Pin the target version and its checksum

Use the version the user named. **If they named none, upgrade to the latest release**, resolved to a concrete version:

```
curl -s https://services.gradle.org/versions/current     # → version + checksumUrl
```

**Target equals the current version → still run the steps.** A bot or a hand edit may have bumped `distributionUrl` without the task, leaving stale scripts and jar (see the end of this page); two runs regenerate them. Resolve before you pin — no checksum can be looked up for `--gradle-version=latest`. Pinning the sum is standard on every upgrade, not an add-on; it is what verifies the download.

**The sum is the distribution URL with `.sha256` appended**, and that one line is the whole lookup:

```
curl -sL https://services.gradle.org/distributions/gradle-9.0.0-bin.zip.sha256
```

`.sha256`, **not `.sha256sum`** — that one 404s on every version and reads like the release doesn't exist. `-L` is required: the URL `301`s to `downloads.gradle.org`, and `-f` won't catch that because it only fails on 4xx and 5xx, so HTML back means you didn't follow the redirect. The body is the bare hex sum. A genuine 404 → the `checksumUrl` in the JSON above, or https://gradle.org/release-checksums/ — not another guessed URL.

**Match the sum to the zip named in `distributionUrl`.** Each release publishes separate sums for the `-bin` zip, the `-all` zip, and the wrapper JAR. The wrong one fails with `Verification of Gradle distribution failed!`, which reads like a tampered download rather than the copy-paste error it usually is.

Once `distributionSha256Sum` is set, any later `wrapper` run that *changes* `--gradle-version` must pass a new matching sum — the build fails rather than reuse the stale one. If the version doesn't change, the sum is preserved automatically.

## Step 3 — Baseline the build, then secure the wrapper

First, establish that the build works *before* you touch it:

```
cd "<build-root>" && ./gradlew --console=plain tasks
```

Keep the exit code. This is the canary, and Steps 5 and 6 re-run it: **a red canary after an upgrade means nothing if it was red beforehand.**

**`tasks`, not `build`.** `tasks` applies every plugin and registers every task — the exact surface a new major breaks — while compiling and running nothing, so it is fast and fails only for reasons the upgrade caused. `build` goes red on a flaky test or an unreachable repository, and rolling back on that would revert upgrades that were fine.

If the build sets `org.gradle.configuration-on-demand=true`, use `tasks --all` instead — plain `tasks` configures the build's root and little else, so it would pass while another part of the build is broken. **Whichever form you pick, use that identical command every later time**; `tasks` before against `tasks --all` after is not a comparison.

**If the canary fails here, stop and do not upgrade.** `:wrapper` configures the build too, so Step 4 will fail for the same reason — there is no supported way to upgrade a build that will not configure. Report what broke; getting it green on its current version comes first.

Then **read `references/snapshot.md` and copy the wrapper files out of the build** — every upgrade, in git or not. Do not skip it. Without a snapshot there is no rollback, and Step 6 assumes one exists.

## Step 4 — Run the `wrapper` task twice

```
cd "<build-root>" && ./gradlew --console=plain :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
cd "<build-root>" && ./gradlew --console=plain :wrapper --gradle-version=8.14.4 --gradle-distribution-sha256-sum=<sha256>
```

Same command, twice: the first regenerates the scripts and jar from the *old* Gradle's templates, the second from the new version's. Both are required — see below. The leading `:` runs the task at the build root, the only place it exists.

**An upgrade never changes the distribution type.** `-all.zip` in Step 1 → add `--distribution-type=all` to both runs; the task defaults to `bin` and will otherwise switch the build silently. Changing type is the user's decision, not a side effect of an upgrade.

Running as an agent:

- **Trust the exit code; never grep for `BUILD SUCCESSFUL`.** A failed checksum must not read as a successful upgrade. A nonzero exit from either run sends you to Step 6, not to a third attempt.
- **Expect a long download.** The second run fetches the full distribution (100 MB+) and can take minutes. Give it a timeout of 10 minutes or more, or run it in the background and wait for it to exit. A long silence is normal, not a hang — abandoning it leaves the half-done state described below, with no error message to quote.
- **`--console=plain`** keeps the output parseable: no progress bar, no colors.

## Step 5 — Verify the files, then run the canary

With the literal snapshot and build-root paths, in double quotes — never `$SNAP`:

```
diff -q "<snapshot>/gradle/wrapper/gradle-wrapper.properties" "<build-root>/gradle/wrapper/gradle-wrapper.properties"
```

It must print `differ`. **Silent is expected only when the target was already the current version** — the two runs then regenerated the scripts and jar, which is the repair a half-done upgrade needs; carry on to the canary. Silent otherwise means the `wrapper` runs changed some other build — they ran outside the build root. Stop and tell the user which directory they ran in; do not roll back, because this build is unchanged. `No such file` means a path is wrong, not that the file differs. Then `cd "<build-root>" && ./gradlew --version` should report the target version.

Only the properties are certain to change. The scripts and jar change only when Gradle changes their templates — the jar is byte-identical across many releases — so an unchanged one is not a missed run. Neither check above proves them current, and neither has to: both `wrapper` runs exiting 0 is that proof.

Those check that the upgrade *landed*. They say nothing about whether the build still works, so re-run the canary — **the same command as Step 3**:

```
cd "<build-root>" && ./gradlew --console=plain tasks
```

**Nonzero exit → Step 6.** Green here, against the green baseline from Step 3, is the upgrade verified: delete the snapshot, and report.

```
rm -f "<snapshot>/gradlew" "<snapshot>/gradlew.bat" "<snapshot>/gradle/wrapper/gradle-wrapper.properties" "<snapshot>/gradle/wrapper/gradle-wrapper.jar" \
  && rmdir "<snapshot>/gradle/wrapper" "<snapshot>/gradle" "<snapshot>"
```

Files by name, then empty directories — never `rm -rf`. `rmdir` refusing a non-empty directory means the path is not your snapshot: stop and tell the user.

## Step 6 — If the build no longer configures, roll back and stop

Three ways to get here, and the second is the one that matters:

- **The `wrapper` task itself failed.** Run 2 *is* the new version, so a build it cannot configure takes the second invocation down with it. Obvious, and it leaves the properties pointing at a version the build cannot run.
- **The `wrapper` task succeeded and the canary failed.** The upgrade landed cleanly, the wrapper files are correct, and the build is now unusable. This is the dangerous one, because every file-level check in Step 5 passes and the agent that stops there reports a successful upgrade over a broken build.
- **Run 2 did not finish** — abandoned mid-download. There is no error to quote, and nothing was learned about whether the build can run the target.

For the first two the cause is the same: a new major removes APIs, raises the minimum JVM, and ships a new Groovy, and a build script, a plugin, or a `buildSrc` that relies on what went away no longer configures. That is a blocked upgrade, not a partial one.

**Read `references/rollback.md` now and follow it** — restoring the wrapper files from the snapshot, verifying the restore, and the four things the closing report must say. Do not improvise it from this page.

Nothing else here applies once you are on this branch. Do not retry the upgrade, and do not edit build scripts to force it through.

## Why run the task TWICE — the #1 real-world gotcha

The task always writes all four files, but the scripts and jar come from the **currently running** Gradle's templates, not the target version's. Run 1 (still the old Gradle) points the properties at the new version and rewrites the generated files from the *old* templates — usually reproducing what was already there, which is also where a hand-edited `gradlew` quietly disappears. Run 2 auto-downloads the new version, because the properties changed, and rewrites them from the *new* templates.

Symptoms of a half-done upgrade, very common in support questions: wrapper or deprecation warnings that won't go away, an odd-looking `gradlew` diff, or a bot (e.g. Dependabot) bumping `distributionUrl` without ever running the task. The fix is always the same — run it twice.

## Version formats

`--gradle-version` also accepts `latest`, `release-candidate`, `release-nightly`, `nightly`, and `release-milestone`, plus a bare `9` or `9.1` on **Gradle 9+**; prefer a concrete version whenever you are pinning a checksum. Since **Gradle 9.0**, `gradle-wrapper.properties` must state a full `X.Y.Z` — a bare major or major.minor is rejected *in the file*, though the CLI still accepts it. Confirm your version's options with `./gradlew help --task=:wrapper`.

## Out of scope

**Fixing the build is out of scope in both directions** — neither to force a blocked upgrade through, nor to repair what the new version broke. A mechanically correct upgrade that leaves the build unusable is still a failed job, and the answer is Step 6, not a patch.

**The dividing line is the build phase, not the command.** No longer *configures* — the `wrapper` task dies, or the canary does — the upgrade is blocked: roll back. Configures and then fails during *execution* — a compile error, a failing test — the upgrade landed and the build has a separate problem: leave the new wrapper in place and report it. Rolling back on a red test is as wrong as leaving behind a build that cannot configure. The line sits there because configuration failure is unambiguous and cheap to check and execution failure is neither; `tasks` passing does not promise the build compiles.

Canonical: https://docs.gradle.org/current/userguide/gradle_wrapper.html.
