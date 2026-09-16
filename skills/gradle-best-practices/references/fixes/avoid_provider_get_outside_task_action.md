# Do not call `get()` on a Provider outside a Task action
`avoid_provider_get_outside_task_action`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** `currentEnvironment.map { "currentEnvironment=$it" }`; `layout.buildDirectory.file("out/report.txt")` instead of `layout.buildDirectory.get().asFile`.
- **Don't:**

  ```kotlin
  tasks.register<MyTask>("avoidThis") {
      myInput = "currentEnvironment=${currentEnvironment.get()}"
      myOutput = layout.buildDirectory.get().asFile.resolve("output-avoid.txt")
  }
  ```

- **Do:**

  ```kotlin
  tasks.register<MyTask>("doThis") {
      myInput = currentEnvironment.map { "currentEnvironment=$it" }
      myOutput = layout.buildDirectory.file("output-do.txt")
  }
  ```
