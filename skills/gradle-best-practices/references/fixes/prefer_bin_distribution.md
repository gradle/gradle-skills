# Prefer the `-bin` Gradle Distribution
`prefer_bin_distribution`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Change the URL suffix to `-bin.zip`. If `distributionSha256Sum` is also set, it must be re-fetched for the `-bin` artifact — the checksums differ (see `security.md`).
- **Don't:**

  ```properties
  distributionUrl=https\://services.gradle.org/distributions/gradle-<version>-all.zip
  ```

- **Do:**

  ```properties
  distributionUrl=https\://services.gradle.org/distributions/gradle-<version>-bin.zip
  ```
