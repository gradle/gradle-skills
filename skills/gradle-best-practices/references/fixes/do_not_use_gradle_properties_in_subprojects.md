# Do not use `gradle.properties` in subprojects
`do_not_use_gradle_properties_in_subprojects`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Move the values to the root `gradle.properties`. For genuinely per-subproject configuration, use a convention plugin with an extension type.
- **Don't:**

  ```kotlin
  // build.gradle.kts
  // This file is located in /app
  tasks.register("printProperties") {
      val propA = project.findProperty("propertyA")
      val propB = project.findProperty("propertyB")

      doLast {
          println("propertyA in app: $propA")
          println("propertyB in app: $propB")
      }
  }
  ```

  ```kotlin
  // build.gradle.kts
  // This file is located in /util
  tasks.register("printProperties") {
      val propA = project.findProperty("propertyA")
      val propB = project.findProperty("propertyB")

      doLast {
          println("propertyA in util: $propA")
          println("propertyB in util: $propB")
      }
  }
  ```

- **Do:**

  ```kotlin
  // build.gradle.kts
  // This file is located in /app
  plugins {
      id("project-properties")
  }

  myProperties {
      propertyA = providers.gradleProperty("propertyA")
      propertyB = providers.gradleProperty("propertyB")
  }
  ```

  ```kotlin
  // build.gradle.kts
  // This file is located in /util
  plugins {
      id("project-properties")
  }

  myProperties {
      propertyA = providers.gradleProperty("propertyA")
      propertyB = "otherValue"
  }
  ```
