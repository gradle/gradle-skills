# Build Output Should Be Byte-for-Byte Reproducible
`builds_should_be_reproducible`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Remove overrides of the Gradle 9 defaults (`preserveFileTimestamps = false`, `reproducibleFileOrder = true`), and pin the JDK:

  ```kotlin
  java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }
  ```

  A toolchain that is not installed will be provisioned or will fail the build — check the build still succeeds after adding it, and prefer the version the build already targets.
- **Don't:**

  ```kotlin
  plugins {
      `java-library`
  }

  tasks.named<Jar>("jar") {
      isPreserveFileTimestamps = true
      isReproducibleFileOrder = false
  }
  ```

- **Do:**

  ```kotlin
  plugins {
      `java-library`
  }

  java {
      toolchain {
          // Choose your project's required version
          languageVersion = JavaLanguageVersion.of(21)
      }
  }
  ```
