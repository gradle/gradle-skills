# Prefer `@PathSensitivity.NONE` for files, `RELATIVE` for directories
`default_path_sensitivities`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** `@InputFile @PathSensitive(PathSensitivity.NONE) abstract val candidatesFile: RegularFileProperty`, and `RELATIVE` for `@InputDirectory`.
- **Don't:**

  ```kotlin
  abstract class AnimalSearchTask : DefaultTask() {
      @get:Input
      abstract val find: Property<String>

      @get:InputFile
      @get:PathSensitive(PathSensitivity.ABSOLUTE)
      abstract val candidatesFile: RegularFileProperty

      @get:OutputFile
      abstract val resultsFile: RegularFileProperty

      @TaskAction
      fun search() {
          if (candidatesFile.get().getAsFile().readLines().contains(find.get())) {
              val msg = "Found a " + find.get() + "!"
              // ...
  ```

- **Do:**

  ```kotlin
  @get:InputFile
  @get:PathSensitive(PathSensitivity.NONE)
  abstract val candidatesFile: RegularFileProperty
  ```
