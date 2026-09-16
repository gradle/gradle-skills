# Avoid `afterEvaluate`
`avoid_after_evaluate`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Use lazy `Property<T>` / `Provider<T>` wiring so values are read at execution time, and `pluginManager.withPlugin("plugin-id") { }` to react to plugin application.
- **Don't:**

  ```kotlin
  plugins {
      id("java-library")
      id("app-info-plugin")
  }

  afterEvaluate {
      the<AppInfoExtension>().appName.set("my-app")
  }
  ```

- **Do:**

  ```kotlin
  plugins {
      id("java-library")
      id("app-info-plugin")
  }

  appInfo {
      appName.set("my-app")
  }
  ```
