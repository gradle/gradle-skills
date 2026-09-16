# Avoid using eager APIs on File Collections
`avoid_eager_file_collection_apis`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Pass the collection through unresolved — `myTask.from(configurations.runtimeClasspath)` — and do any counting or inspection inside the task action.
- **Don't:**

  ```kotlin
  // ...
  tasks.register<FileCounterTask>("badCountingTask") {
      if (!configurations.runtimeClasspath.get().isEmpty()) {
          logger.lifecycle("Resolved: " + (configurations.runtimeClasspath.get().state == RESOLVED))
          countMe.from(configurations.runtimeClasspath)
      }
  }

  tasks.register<FileCounterTask>("badCountingTask2") {
      val files = configurations.runtimeClasspath.get().files
      countMe.from(files)
      logger.lifecycle("Resolved: " + (configurations.runtimeClasspath.get().state == RESOLVED))
  }
  // ...
  ```

- **Do:**

  ```kotlin
  abstract class FileCounterTask: DefaultTask() {
      @get:InputFiles
      abstract val countMe: ConfigurableFileCollection

      @TaskAction
      fun countFiles() {
          logger.lifecycle("Count: " + countMe.files.size)
      }
  }

  tasks.register<FileCounterTask>("goodCountingTask") {
      countMe.from(configurations.runtimeClasspath)
      countMe.from(layout.projectDirectory.file("extra.txt"))
      logger.lifecycle("Resolved: " + (configurations.runtimeClasspath.get().state == RESOLVED))
  }
  ```
