# Use the Latest Minor Version of Gradle
`use_latest_minor_versions`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** `./gradlew wrapper --gradle-version <version>`, then update plugins and test compatibility. Upgrade Gradle before plugins.
