# Rolling back a blocked upgrade

Step 6 of `SKILL.md` sends you here: the `wrapper` task failed, it succeeded and the canary failed, or run 2 did not finish. Put the build back exactly as you found it and tell the user what you learned — no retrying the upgrade, no editing build scripts to force it through.

## 1. Restore the wrapper from the snapshot

Use the literal paths from Step 3 — `"<build-root>"` and `"<snapshot>"`, as you told the user — in double quotes. **Never `$SNAP`**; it is empty by now. **Lost a path? Stop and tell the user.** Do not search for the snapshot, guess its path, or rebuild it: restoring from the wrong directory writes its contents into the build.

**The snapshot is the only source.** Never restore with `git checkout`, `git restore` or `git stash`: git cannot see an ignored jar, and it discards the user's uncommitted edits.

First confirm the snapshot is the one you took — every file not reported `missing:`, at its path in the build, and nothing else:

```
find "<snapshot>" -type f
```

Lost the `missing:` lines? Any of the four wrapper files this does not list was missing.

Then copy each file back — one line per file, skipping any reported `missing:`:

```
cp -p "<snapshot>/gradle/wrapper/gradle-wrapper.properties" "<build-root>/gradle/wrapper/gradle-wrapper.properties"
cp -p "<snapshot>/gradle/wrapper/gradle-wrapper.jar" "<build-root>/gradle/wrapper/gradle-wrapper.jar"
cp -p "<snapshot>/gradlew" "<build-root>/gradlew"
cp -p "<snapshot>/gradlew.bat" "<build-root>/gradlew.bat"
```

**One source, one destination, both absolute, per line.** That keeps each file in its own place and confines the restore to the four wrapper paths of this build, whatever directory you run it from. Do not merge the lines into one `cp` with several sources — `cp` puts every source in the one target directory — and do not replace them with a copy of the whole snapshot directory, which writes whatever that directory holds into the build and resets the build root's permissions to the snapshot's.

**Then delete every file the snapshot reported `missing:`.** The `wrapper` task created it, and the snapshot has nothing to put back over it:

```
rm -f "<build-root>/<path from a missing: line>"
```

Nothing reported missing → skip this. `-f` because a run that failed early may not have created it.

## 2. Confirm the restore, then re-run the canary

Every file in the snapshot must match:

```
diff -q "<snapshot>/gradlew" "<build-root>/gradlew"
diff -q "<snapshot>/gradlew.bat" "<build-root>/gradlew.bat"
diff -q "<snapshot>/gradle/wrapper/gradle-wrapper.properties" "<build-root>/gradle/wrapper/gradle-wrapper.properties"
diff -q "<snapshot>/gradle/wrapper/gradle-wrapper.jar" "<build-root>/gradle/wrapper/gradle-wrapper.jar"
```

All silent, apart from the lines for files reported `missing:`; those files must be gone from the build. `distributionUrl` names the original version. A line that prints `differ` → redo that file's `cp` and check again.

Then run the Step 3 canary command again — the same form, `tasks` or `tasks --all`. It passed then and must pass now, which is what proves you restored a working build rather than plausible-looking files. A rollback you did not verify is the same as none.

**Every `diff` silent and the canary still red → stop.** There is nothing left to restore; something outside the wrapper changed, or the canary is flaky. Keep the snapshot, and tell the user both canary results — green at Step 3, red now — with its error, and the snapshot path. Do not reach for git, edit the build, or look for another snapshot. That message replaces the report in §3 — no verdict, no next rung.

**Canary green → delete the snapshot,** and only then write the report:

```
rm -f "<snapshot>/gradlew" "<snapshot>/gradlew.bat" "<snapshot>/gradle/wrapper/gradle-wrapper.properties" "<snapshot>/gradle/wrapper/gradle-wrapper.jar" \
  && rmdir "<snapshot>/gradle/wrapper" "<snapshot>/gradle" "<snapshot>"
```

Files by name, then empty directories — never `rm -rf`. If `rmdir` refuses a non-empty directory, the path is not your snapshot: leave it and tell the user.

## 3. Report — four things, all of them, in the closing message

Put all four in the message that ends your turn, not scattered through earlier ones: the last message is the one the user reads. **A report missing any of the four is a failed report**, however well the rollback itself went.

**Once you have restored, the upgrade did not happen.** No wording of this report may say it succeeded — not "upgraded to 9.0.0", not "regenerated the wrapper files", not a changelog of what the `wrapper` task wrote before you undid it. Those describe a state you deliberately threw away, and the user will read them as the outcome.

**Re-read every fact from the build as it stands now.** Do not quote a `--version` or canary result captured earlier in the turn: a failed run 2 and a bad first restore both produce readings that were true when taken and false by the time you write. Run `cd "<build-root>" && ./gradlew --version` and re-read `distributionUrl` *after* the last restore; where they disagree with what you were about to write, they are right.

**Run 2 did not finish? Then three of the four change,** because nothing was learned about whether the build can run the target. The verdict is *The upgrade to Gradle 9.0.0 did not complete — run 2 was interrupted while downloading*, then the version the build is on now. In place of an error, say it was interrupted. The next step is the same version again, with a timeout of 10 minutes or more or in the background — not a smaller release, and the ladder below does not apply. The links stay.

1. **The verdict.** *This build does not appear to be upgradeable to Gradle 9.0.0* — stated plainly and first, followed by the version the build is on now, taken from that re-read. Do not open with the diagnosis or the file list; open with whether the thing they asked for happened.
2. **The error.** Quote it. "`Could not find method exec()`" tells the user which removal bit them; "the upgrade failed" tells them nothing.
3. **The next rung — a sentence either way.** Name the next release after the one the build is on (from 8.5, that is 8.6), and say where it leads: one release at a time up to the version they asked for.

   **Write it as a single path, not two recommendations.** These are adjacent sentences from a real report:

   > The smallest next hop is Gradle 8.6. Upgrade to the latest Gradle 8.x release and resolve the deprecations before retrying.

   The first sentence is right and the second is wrong *here*, and together they name two different versions, so the user cannot tell which to follow. "Upgrade to the latest 8.x" is Gradle's standard route toward a major and is the correct opening move — but **it is not the advice at this point**, because a hop of that size is precisely what just failed. Say instead: *"Go to 8.6 next. From there 8.7, then 8.8, and so on — one release at a time, running `./gradlew --warning-mode=all build` at each step to clear what the next one removes — until you reach 9.0.0."* One route, one rung at a time.

   When there is no next release — the request was already the next one or smaller, or the build is on the newest release — **say that instead**. Silence is never the right content here, and this is the item that goes missing, because it is the only one that can be dropped without leaving a visible hole.
4. **The links.** Release notes for the version they asked for, `https://docs.gradle.org/<version>/release-notes.html` — for 9.0.0, https://docs.gradle.org/9.0.0/release-notes.html — the per-version record of what changed, and where the cause is most likely written down. For a major, add the upgrade guide (https://docs.gradle.org/current/userguide/upgrading_major_version_9.html for 9.x), which lists the removals against their replacements and is the only way to size the work.

**Recommend the hop; do not take it.** Quietly landing the user on a version they did not ask for, right after telling them the one they did ask for failed, is a second unrequested change on top of a failed first. Offer it and wait — which makes item 3 a sentence you write rather than a command you run, and is exactly why it is the easiest to skip.

## The ladder — one release at a time

**The ladder is recovery, not the default route.** Gradle's own guidance — go to the latest minor of the current major, clear deprecations, then cross — is the correct advice *before* an attempt, and nothing here contradicts it. You are reading this page because that has already been tried and failed, and a hop that has failed once is not worth repeating at the same size. That is what buys the smaller steps their cost.

Resolve the next rung rather than guessing it:

```
curl -sL https://services.gradle.org/versions/all    # every release, newest first
```

**Count only final releases** — the feed carries release candidates, milestones and nightlies too. An entry is final when `snapshot`, `nightly` and `broken` are false and `rcFor` and `milestoneFor` are empty. Offering `8.6-rc-1` as the safe next step is worse than offering nothing.

**The rung is always the next release after the version the build is on — never a fixed waypoint.** From 8.5 it is 8.6. If the user takes 8.6 and the jump from *there* to 9.0.0 fails the same way, the next recommendation is **8.7** — not 8.6 again, and not a leap to the end of the line. Every failure moves the ladder up exactly one rung, and the target the user originally asked for never changes.

One release at a time is the smallest step that makes progress, and a failure on one rung is a far smaller thing to diagnose than a failure across several.

**Do not restart with another oversized jump.** "Get to the latest 8.x, then try 9.0" is Gradle's documented route to a new major, and it is the right place to *start* — but the user has already been there, because the hop that just failed was one of that size. Restarting it from a different rung asks for the same failure: 8.5 → 8.14 crosses nine releases' worth of removals in one step, and when it breaks they are no better off than now. Once a jump that big has failed, each step has to be small enough that a failure names its own cause.

**Clear deprecations on every rung, not at the end.** Each release warns about what the next ones remove, which is how the ladder stays cheap:

```
./gradlew --warning-mode=all build
```

Climb until the build is on the version they originally asked for.
