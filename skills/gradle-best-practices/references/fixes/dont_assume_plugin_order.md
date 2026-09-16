# Don't Assume your Plugin is Applied after Another
`dont_assume_plugin_order`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Wrap in `project.pluginManager.withPlugin("plugin-id") { ... }`, or apply the prerequisite explicitly with `project.pluginManager.apply("plugin-id")`.
- **Don't:**

  ```kotlin
  // build.gradle.kts
  subprojects {
      // Apply the Java plugin to every subproject
      afterEvaluate {
          // This runs after the app subproject’s build script is evaluated and results in an error
          pluginManager.apply("java")
      }
  }
  ```

  ```kotlin
  // app/build.gradle.kts
  plugins {
      id("myplugin")
  }
  // Assumes 'java' plugin is present
  extensions.getByType<org.gradle.api.plugins.JavaPluginExtension>().apply {
      toolchain.languageVersion.set(JavaLanguageVersion.of(21))
  }
  ```

- **Do:**

  ```kotlin
  // app/build.gradle.kts
  pluginManager.withPlugin("java") {
      extensions.configure<org.gradle.api.plugins.JavaPluginExtension> {
          toolchain.languageVersion.set(JavaLanguageVersion.of(21))
      }
  }
  ```

  ```kotlin
  // buildSrc/src/main/kotlin/MyPlugin.kt
  class MyPlugin : Plugin<Project> {
      override fun apply(project: Project) {
          // If your plugin requires 'java', apply it so order doesn’t matter
          project.pluginManager.apply("java")
          // Now it's safe to configure Java things immediately
          project.extensions.configure(JavaPluginExtension::class.java) {
              toolchain.languageVersion.set(JavaLanguageVersion.of(21))
          }
      }
  }
  ```
