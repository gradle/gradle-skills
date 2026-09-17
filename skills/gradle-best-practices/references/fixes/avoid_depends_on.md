# Avoid DependsOn
`avoid_depends_on`

**Rule:** Use `dependsOn` only for lifecycle tasks that have no actions. Between tasks that do work, declare inputs and outputs and let Gradle infer the ordering.

---

- **Fix:** Wire the producer's output into the consumer's input: `inputs.file(tasks.named<Producer>("produce").map { it.outputFile })`, or `from(tasks.named(...))` for a copy-like task. Delete the `dependsOn`.
- **Don't:**

  ```kotlin
  // ...
  tasks.register<SimpleTranslationTask>("translateBad") {
      dependsOn(tasks.named("helloWorld"))
  }
  ```

- **Do:**

  ```kotlin
  // ...
  tasks.register<SimpleTranslationTask>("translateGood") {
      inputs.file(tasks.named<SimplePrintingTask>("helloWorld").map { messageFile })
  }
  ```
