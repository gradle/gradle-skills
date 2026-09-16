# Set Build Flags in `gradle.properties`
`use_the_gradle_properties_file`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Move the flags into the root `gradle.properties`, one `key=value` per line, and commit it.
- **Don't:**

  ```text
  ./gradlew build --continue --parallel
  ```

  Supplied per invocation: easily forgotten, and applied inconsistently across
  machines and CI.
- **Do:**

  ```properties
  # gradle.properties, in the root project, committed to source control
  org.gradle.continue=true
  org.gradle.parallel=true
  ```
