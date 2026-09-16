# Validate the Gradle Wrapper on every Upgrade
`validate_wrapper_checksum`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Use `gradle/actions/setup-gradle` (v4+), which validates the wrapper JAR, or regenerate the wrapper with a trusted Gradle install and diff the result against what is committed.
