# Do not call `get()` on a Provider outside a Task action
`avoid_provider_get_outside_task_action`

**Rule:** Do not query a provider during configuration; transform it with `map` / `flatMap` so the value is read at execution time.

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
