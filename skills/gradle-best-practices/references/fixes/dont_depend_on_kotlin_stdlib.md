# Don't Explicitly Depend on the Kotlin Standard Library
`dont_depend_on_kotlin_stdlib`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Delete the declaration.
- **Don't:**

  ```kotlin
  plugins {
      kotlin("jvm").version("2.4.0")
  }

  dependencies {
      api(kotlin("stdlib"))
  }
  ```

- **Do:**

  ```kotlin
  plugins {
      kotlin("jvm").version("2.4.0")
  }
  ```
