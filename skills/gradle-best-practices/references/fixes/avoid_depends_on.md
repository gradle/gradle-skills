# Avoid DependsOn
`avoid_depends_on`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

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
