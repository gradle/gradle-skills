# Rolling back a blocked upgrade

Step 6 of `SKILL.md` sends you here: the `wrapper` task failed, or it succeeded and the canary failed. The target version cannot run this build. Put the project back exactly as you found it and tell the user what you learned — no retrying the upgrade, no editing build scripts to force it through.

## 1. Restore all four files

```
git checkout -- gradlew gradlew.bat gradle/wrapper
```

That is the whole step, and it cannot be got wrong. If Step 3 had you take a copy instead — a dirty tree, or no git — restore from it as `references/snapshot.md` describes, and heed the warning there about naming the four files individually: doing so scatters two of them into the project root and leaves the failed upgrade in place.

## 2. Confirm the restore, then re-run the canary

`git status --short gradlew gradlew.bat gradle/wrapper` prints nothing — or, from a snapshot, `diff -r` is silent and `distributionUrl` names the original version.

Then run the Step 3 canary command again — the same form, `tasks` or `tasks --all`. It passed then and must pass now, which is what proves you restored a working build rather than four plausible-looking files. A rollback you did not verify is the same as none.

**If this canary fails, you are not done — you have a bad restore, not a second finding.** Fix the restore and re-run until it is green. Only then delete the snapshot, and do not write the report before that point.

## 3. Report — four things, all of them, in the closing message

Put all four in the message that ends your turn, not scattered through earlier ones: the last message is the one the user reads. **A report missing any of the four is a failed report**, however well the rollback itself went.

**Once you have restored, the upgrade did not happen.** No wording of this report may say it succeeded — not "upgraded to 9.0.0", not "regenerated the wrapper files", not a changelog of what the `wrapper` task wrote before you undid it. Those describe a state you deliberately threw away, and the user will read them as the outcome.

**Re-read every fact from the project as it stands now.** Do not quote a `--version` or canary result captured earlier in the turn: a failed run 2 and a bad first restore both produce readings that were true when taken and false by the time you write. Run `./gradlew --version` and re-read `distributionUrl` *after* the last restore; where they disagree with what you were about to write, they are right.

1. **The verdict.** *This build does not appear to be upgradeable to Gradle 9.0.0* — stated plainly and first, followed by the version the project is on now, taken from that re-read. Do not open with the diagnosis or the file list; open with whether the thing they asked for happened.
2. **The error.** Quote it. "`Could not find method exec()`" tells the user which removal bit them; "the upgrade failed" tells them nothing.
3. **The smaller hop — a sentence either way.** Name the next minor release when there is one and they asked for more than that: from 8.5 that is 8.6. When there is not — the request was already the next minor or smaller, or the current version is the newest release — **say that instead**. Silence is never the right content here, and this is the item that goes missing, because it is the only one that can be dropped without leaving a visible hole.
4. **The links.** Release notes for the version they asked for, `https://docs.gradle.org/<version>/release-notes.html` — for 9.0.0, https://docs.gradle.org/9.0.0/release-notes.html — the per-version record of what changed, and where the cause is most likely written down. For a major, add the upgrade guide (https://docs.gradle.org/current/userguide/upgrading_major_version_9.html for 9.x), which lists the removals against their replacements and is the only way to size the work.

**Recommend the hop; do not take it.** Quietly landing the user on a version they did not ask for, right after telling them the one they did ask for failed, is a second unrequested change on top of a failed first. Offer it and wait — which makes item 3 a sentence you write rather than a command you run, and is exactly why it is the easiest to skip.

## Resolving the next minor

```
curl -sL https://services.gradle.org/versions/all    # every release, newest first
```

**Count only final releases** — the feed carries release candidates, milestones and nightlies too. An entry is final when `snapshot`, `nightly` and `broken` are false and `rcFor` and `milestoneFor` are empty. Offering `8.6-rc-1` as the safe next step is worse than offering nothing.

One minor at a time is the smallest step that makes progress, and a failure there is a far smaller thing to diagnose than a failure across a major. It is not the destination: before retrying the major they need the **last release of the current major**, which is where everything the new major removed shows up as a deprecation warning rather than an error:

```
./gradlew --warning-mode=all build
```
