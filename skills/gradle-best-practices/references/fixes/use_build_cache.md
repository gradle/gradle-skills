# Use the Build Cache
`use_build_cache`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Add `org.gradle.caching=true` to the root `gradle.properties`.
- **Don't:**

  ```properties
  # caching is off by default
  # org.gradle.caching=false
  ```

- **Do:**

  ```properties
  org.gradle.caching=true
  ```
