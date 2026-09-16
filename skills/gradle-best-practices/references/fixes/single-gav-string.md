# Declare Dependencies using a single GAV String
`single-gav-string`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Collapse to one string: `implementation("com.example:lib:1.0")`. Keep any `exclude`/`because` configuration in a trailing block.
- **Don't:**

  ```kotlin
  dependencies {
      implementation(group = "com.fasterxml.jackson.core", name = "jackson-databind", version = "32.17.0")
      api(group = "com.google.guava", name = "guava", version = "32.1.2-jre") {
          exclude(group = "com.google.code.findbugs", module = "jsr305")
      }
  }
  ```

- **Do:**

  ```kotlin
  dependencies {
      implementation("com.fasterxml.jackson.core:jackson-databind:2.17.0")
      api("com.google.guava:guava:32.1.2-jre") {
          exclude(group = "com.google.code.findbugs", module = "jsr305")
      }
  }
  ```
