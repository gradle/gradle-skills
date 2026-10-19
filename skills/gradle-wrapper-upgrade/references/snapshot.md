# Snapshotting the wrapper

Step 3 of `SKILL.md` sends you here on every upgrade, in git or not. One mechanism for every build, and it sees files git does not — an ignored `gradle-wrapper.jar` is invisible to `git status` and beyond the reach of `git checkout`.

`"<build-root>"` is the build root's absolute path from Step 1, and `"<snapshot>"` the directory this command prints. Substitute both, keep the double quotes.

## Take the copy

One command:

```
cd "<build-root>" && d=${TMPDIR:-/tmp} && SNAP=$(mktemp -d "${d%/}/gradle-wrapper-snapshot.XXXXXX") \
  && echo "snapshot: $SNAP" && echo "build root: $(pwd)" && mkdir -p "$SNAP/gradle/wrapper" \
  && cp -p gradle/wrapper/gradle-wrapper.properties "$SNAP/gradle/wrapper/gradle-wrapper.properties" \
  && ok=1 && for f in gradlew gradlew.bat gradle/wrapper/gradle-wrapper.jar; do
       if [ -e "$f" ]; then cp -p "$f" "$SNAP/$f" || ok=0; else echo "missing: $f"; fi
     done && [ "$ok" = 1 ] && find "$SNAP" -type f
```

`gradle-wrapper.properties` must exist — it is where Step 1 read the version — so its copy is unconditional and fails the command without it. The other three are copied when present and reported `missing:` when not. Each file is copied to its own path inside the snapshot, so the tree comes out the same shape as the build's. Do not rewrite the loop as one `cp` with several sources: `cp` puts every source in the one target directory, and the two nested files land flat at the snapshot root.

**Do not suppress stderr here.** No `2>/dev/null`, no `|| true`. A snapshot that half-failed silently is worse than one that failed loudly, because the failure only surfaces later as files written into the user's build.

**Check the shape before going on.** The trailing `find` must list every file not reported `missing:`, each at its path in the build, and nothing else:

```
<snapshot>/gradlew
<snapshot>/gradlew.bat
<snapshot>/gradle/wrapper/gradle-wrapper.properties
<snapshot>/gradle/wrapper/gradle-wrapper.jar
```

**Nonzero exit, or a wrong shape → delete what it made and stop.** Report the error; do not upgrade without a snapshot.

```
rm -f "<snapshot>/gradlew" "<snapshot>/gradlew.bat" "<snapshot>/gradle/wrapper/gradle-wrapper.properties" "<snapshot>/gradle/wrapper/gradle-wrapper.jar" \
  && rmdir "<snapshot>/gradle/wrapper" "<snapshot>/gradle" "<snapshot>"
```

Files by name, then empty directories — never `rm -rf`. If `rmdir` refuses a non-empty directory, leave it and tell the user.

**Tell the user, in a message, before going on:** the build root, the snapshot path, and every `missing:` line. If anything stops the upgrade partway, the user knows where their wrapper files are.

**Never write `$SNAP` again.** Shell variables do not survive into your next command, so `$SNAP` is empty by the time you would restore, and an empty `$SNAP` turns the restore source into the root of the filesystem. Every later command uses the literal paths. **If you lose them, stop and tell the user.** Do not search for the snapshot, guess its path, or rebuild it — a wrong directory restored into the build is the hazard the snapshot exists to avoid.

**`missing:` matters at rollback.** The `wrapper` task creates the files the build lacked, and a rollback has to delete them; the snapshot cannot hold a file that never existed.

**All four files, not just the properties.** Run 1 of the `wrapper` task rewrites the scripts and jar from the old templates and run 2 from the new, so a failure between them leaves a mixture. Reverting `gradle-wrapper.properties` alone moves the version back while leaving the new `gradlew` and jar in place.

**Outside the build.** The snapshot lives under `$TMPDIR` (`/var/folders/…/T/` on macOS) or `/tmp`, readable only by you. A `.bak` beside the original is not outside, and is a file you have added to the user's tree.
