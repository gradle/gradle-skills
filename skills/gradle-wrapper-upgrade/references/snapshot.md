# Snapshotting a wrapper outside git

Step 3 of `SKILL.md` sends you here when `git status --short gradlew gradlew.bat gradle/wrapper` printed something, or the project is not in git at all. Either way git cannot give the four files back, so you need a copy before the upgrade touches them.

## Take the copy

One command, from the project root:

```
SNAP=$(mktemp -d) && mkdir -p "$SNAP/gradle/wrapper" \
  && cp gradlew gradlew.bat "$SNAP/" \
  && cp gradle/wrapper/gradle-wrapper.{properties,jar} "$SNAP/gradle/wrapper/" \
  && echo "snapshot: $SNAP"
```

**Write down the path it prints.** Shell variables do not survive into your next command, so `$SNAP` is empty by the time you would restore — and unset, `cp -a "$SNAP"/. .` becomes `cp -a /. .`, which copies the root of the filesystem into the project. Use the literal path from here on.

**All four files, not just the properties.** Run 1 of the `wrapper` task rewrites the scripts and jar from the old templates and run 2 from the new, so a failure between them leaves a mixture. Reverting `gradle-wrapper.properties` alone moves the version back while leaving the new `gradlew` and jar in place — which is the half-done state Step 5 exists to detect, reached while trying to undo one.

**Outside the project.** `mktemp -d` is outside it; a `.bak` beside the original is not, and is a file you have added to the user's tree. Delete the snapshot once Step 5 passes.

## Verify against it

Anywhere `SKILL.md` or `references/rollback.md` checks state with `git status --short`, use the snapshot instead: `diff -r <snapshot> .` over the four paths. After a successful upgrade all four must differ; after a rollback none may.

## Restore from it

```
cp -a /tmp/tmp.XXXX/. .
```

**Do not expand that into a list of the four files.** `cp` with several sources and a directory target puts *every* source in that directory, so naming them individually drops `gradle-wrapper.properties` and `gradle-wrapper.jar` into the project root while `gradle/wrapper/` keeps the failed upgrade — two stray files, a wrapper never actually restored, and a canary that now fails for an unrelated reason. The trailing `/.` copies the tree instead, putting each file back where it came from.
