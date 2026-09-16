# Use unique output files and directories
`use_unique_output_files_and_directories`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Give each a distinct path, or switch to `@OutputFile` with distinct file names: `layout.buildDirectory.dir("greetings").map { it.file("a.txt") }`.
- **Don't:**

  ```kotlin
  tasks.register<GreetingTask>("greeterA") {
      type = "a"
      outputDirectory = layout.buildDirectory.dir("greetings")
  }
  tasks.register<GreetingTask>("greeterB") {
      type = "b"
      outputDirectory = layout.buildDirectory.dir("greetings")  // same directory
  }
  ```

- **Do:**

  ```kotlin
  tasks.register<GreetingTask>("greeterA") {
      type = "a"
      outputDirectory = layout.buildDirectory.dir("greetings")
  }
  tasks.register<GreetingTask>("greeterB") {
      type = "b"
      outputDirectory = layout.buildDirectory.dir("greetings-2")
  }
  ```
