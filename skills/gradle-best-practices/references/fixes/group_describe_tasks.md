# Group and Describe custom Tasks
`group_describe_tasks`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Set both, either in the registration block or as defaults in the task class constructor:
  `group = "documentation"`, `description = "Generates project documentation from source files."`
- **Don't:**

  ```kotlin
  tasks.register("generateDocs") {
      // Build logic to generate documentation
  }
  ```

- **Do:**

  ```kotlin
  tasks.register("generateDocs") {
      group = "documentation"
      description = "Generates project documentation from source files."
      // Build logic to generate documentation
  }
  ```
