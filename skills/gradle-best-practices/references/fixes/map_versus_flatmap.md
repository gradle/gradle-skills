# Wiring Task Outputs with `map` and `flatMap`
`map_versus_flatmap`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** `generatorTask.flatMap { it.outputFile }.map { it.asFile.readText() }`, with the producer's output declared as an annotated abstract getter (`@OutputFile abstract val outputFile: RegularFileProperty`).
- **Don't:**

  ```kotlin
  val generatorTask = tasks.register<GeneratorTask>("generator") {
      outputFile.set(layout.buildDirectory.file("eager-output.txt"))
  }

  tasks.register<ConsumerTask>("consumeEager") {
      inputFile.set(generatorTask.flatMap { it.outputFile })
      inputContent.set(generatorTask.map {
          it.outputFile.get().asFile.readText()
      })
  }
  ```

- **Do:**

  ```kotlin
  val generatorTask = tasks.register<GeneratorTask>("generator") {
      outputFile.set(layout.buildDirectory.file("output.txt"))
  }

  tasks.register<ConsumerTask>("consumeLazy") {
      inputFile.set(generatorTask.flatMap { it.outputFile })
      inputContent.set(
          generatorTask.flatMap { it.outputFile }
              .map { it.asFile.readText() }
      )
  }
  ```
