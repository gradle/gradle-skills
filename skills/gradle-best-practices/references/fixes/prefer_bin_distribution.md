# Prefer the `-bin` Gradle Distribution
`prefer_bin_distribution`

**Rule:** Prefer the smaller `-bin` distribution over `-all`, which additionally carries sources and documentation.

---

- **Fix:** Re-run the `wrapper` task at the project's **current** version, asking for the `bin` type:

  ```
  ./gradlew wrapper --gradle-version <the version already in distributionUrl> --distribution-type=bin --gradle-distribution-sha256-sum <sha256 of the -bin zip>
  ```

  **Do not hand-edit the URL.** `gradle-wrapper.properties` is written by that task, alongside `gradlew`, `gradlew.bat` and `gradle-wrapper.jar`; an edit made by hand is overwritten by the next run without warning.

  One run is enough here, unlike a version change: the scripts and jar are regenerated from the Gradle the project is already on, which is the version staying put. Keep it that way — changing the type and the version together turns this into an upgrade, which is the `gradle-wrapper-upgrade` skill's job, not this entry's.

  Re-pin the checksum. Each release publishes separate sums for `-bin` and `-all`, so carrying the old one over fails the next build with `Verification of Gradle distribution failed!` (see `validate_gradle_checksum` in `security.md`).
- **Don't** — the state that triggers this finding:

  ```properties
  distributionUrl=https\://services.gradle.org/distributions/gradle-<version>-all.zip
  ```

- **Do** — the state the task leaves behind, with a matching `-bin` checksum:

  ```properties
  distributionUrl=https\://services.gradle.org/distributions/gradle-<version>-bin.zip
  ```
