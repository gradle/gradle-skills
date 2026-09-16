# Do Not Use Internal APIs
`do_not_use_internal_apis`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Replace with a public API equivalent. If none exists, copy the needed logic into the project rather than depending on an internal type.
- **Don't:**

  ```kotlin
  import org.gradle.api.internal.attributes.AttributeContainerInternal

  configurations.create("bad") {
      attributes {
          attribute(Usage.USAGE_ATTRIBUTE, objects.named<Usage>(Usage.JAVA_RUNTIME))
          attribute(Category.CATEGORY_ATTRIBUTE, objects.named<Category>(Category.LIBRARY))
      }
      val badMap = (attributes as AttributeContainerInternal).asMap()
      logger.warn("Bad map")
      badMap.forEach { (key, value) ->
          logger.warn("$key -> $value")
      }
  }
  ```

- **Do:**

  ```kotlin
  configurations.create("good") {
      attributes {
          attribute(Usage.USAGE_ATTRIBUTE, objects.named<Usage>(Usage.JAVA_RUNTIME))
          attribute(Category.CATEGORY_ATTRIBUTE, objects.named<Category>(Category.LIBRARY))
      }
      val goodMap = attributes.keySet().associate {
          Attribute.of(it.name, it.type) to attributes.getAttribute(it)
      }
      logger.warn("Good map")
      goodMap.forEach { (key, value) ->
          logger.warn("$key -> $value")
      }
  }
  ```
