# Avoid Unintentionally Creating Empty Projects
`avoid_empty_projects`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:**

  ```kotlin
  include(":my-web-module")
  project(":my-web-module").projectDir = file("subs/web/my-web-module")
  ```

  Invocation then becomes `gradle :my-web-module:build`.
- **Don't:**

  ```kotlin
  include(":app")
  include(":subs:web:my-web-module")
  ```

- **Do:**

  ```kotlin
  include(":app")

  include(":my-web-module")
  project(":my-web-module").projectDir = file("subs/web/my-web-module")
  ```
