# Set up your Dependency Repositories in the Settings file
`set_up_repositories_in_settings`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Move them into settings:

  ```kotlin
  pluginManagement { repositories { gradlePluginPortal(); mavenCentral() } }
  dependencyResolutionManagement {
      repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
      repositories { mavenCentral() }
  }
  ```

  Setting `FAIL_ON_PROJECT_REPOS` is what stops the situation recurring; add it once the project-level blocks are gone.
- **Don't:**

  ```kotlin
  buildscript {
      repositories {
          mavenCentral()
          gradlePluginPortal()
      }
  }

  plugins {
      id("java")
  }

  repositories {
      mavenCentral()
  }
  ```

- **Do:**

  ```kotlin
  pluginManagement {
      repositories {
          mavenCentral()
          gradlePluginPortal()
      }
  }
  dependencyResolutionManagement {
      repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
      repositories {
          mavenCentral()
      }
  }
  ```
