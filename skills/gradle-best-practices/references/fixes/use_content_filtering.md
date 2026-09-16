# Use Content Filtering with multiple Repositories
`use_content_filtering`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:**

  ```kotlin
  repositories {
      google { content { includeGroupByRegex("androidx.*"); includeGroup("com.google.gms") } }
      mavenCentral()
  }
  ```

  or `exclusiveContent { forRepository { google() }; filter { includeGroupByRegex("androidx.*") } }`.
- **Don't:**

  ```kotlin
  dependencyResolutionManagement {
      repositories {
          mavenCentral()
          google()
      }
  }
  ```

- **Do:**

  ```kotlin
  dependencyResolutionManagement {
      repositories {
          google {
              content {
                  // Use this repository for androidx and GMS dependencies
                  includeGroupByRegex("androidx.*")
                  includeGroup("com.google.gms")
              }
          }
          // Specify the fallback repository last
          mavenCentral()
      }
  }
  ```
