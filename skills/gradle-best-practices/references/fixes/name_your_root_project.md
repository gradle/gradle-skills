# Name Your Root Project
`name_your_root_project`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Add `rootProject.name = "my-project"` (Kotlin) or `rootProject.name = 'my-project'` (Groovy) to the settings file. Place it *after* any `pluginManagement { }` or `plugins { }` block: Gradle rejects a settings file with any statement before `plugins {}` ("only buildscript {}, pluginManagement {} and other plugins {} script blocks are allowed before plugins {} blocks"), so prepending it to a settings file that applies plugins breaks the build at startup.
- **Don't:**

  ```kotlin
  // Left empty
  ```

- **Do:**

  ```kotlin
  rootProject.name = "my-example-project"
  ```
