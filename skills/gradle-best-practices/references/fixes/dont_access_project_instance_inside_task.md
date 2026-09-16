# Don't access a `Project` instance during Task Execution
`dont_access_project_instance_inside_task`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Declare `@Input abstract val version: Property<String>`, set it during configuration (`version.set(project.version.toString())`), and read `version.get()` in the action. This is also a configuration-cache prerequisite.
- **Don't:**

  ```kotlin
  abstract class VersionTask : DefaultTask() {

      @get:OutputDirectory
      abstract val outputDirectory: DirectoryProperty

      @TaskAction
      fun run() {
          val outputFile = outputDirectory.file("build_version.txt")
          outputFile.get().asFile.writeText(project.version.toString())
      }
  }

  tasks.register<VersionTask>("generateVersionFile") {
      outputDirectory.set(project.layout.buildDirectory)
  }
  ```

- **Do:**

  ```kotlin
  abstract class VersionTask : DefaultTask() {
      @get:Input
      abstract val version: Property<String>

      @get:OutputDirectory
      abstract val outputDirectory: DirectoryProperty

      @TaskAction
      fun run() {
          outputDirectory.file("build_version.txt").get().asFile.writeText(version.get())
      }
  }

  tasks.register<VersionTask>("generateVersionFile") {
      version.set(project.version.toString())
      // ...
  ```
