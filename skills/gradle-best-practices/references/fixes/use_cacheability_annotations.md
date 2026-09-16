# Favor `@CacheableTask` / `@DisableCachingByDefault`
`use_cacheability_annotations`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Annotate the class — `@CacheableTask abstract class MyTask : DefaultTask()` — or `@DisableCachingByDefault(because = "...")` when it should not be cached, and remove the per-instance call.
- **Don't:**

  ```kotlin
  abstract class CalculatorTask : DefaultTask() { /* ... */ }

  tasks.register<CalculatorTask>("add1") {
      outputs.cacheIf { true }
  }
  tasks.register<CalculatorTask>("add2") {
      outputs.cacheIf { true }
  }
  ```

- **Do:**

  ```kotlin
  @CacheableTask
  abstract class CalculatorTask : DefaultTask() { /* ... */ }

  tasks.register<CalculatorTask>("add1")
  tasks.register<CalculatorTask>("add2")
  ```
