# Validate the Gradle Wrapper on every Upgrade
`validate_wrapper_checksum`

**Rule:** Treat the committed `gradle-wrapper.jar` as security-sensitive: verify it is a genuine Gradle release artifact whenever the wrapper changes. It is an executable binary no reviewer reads, and it runs on every `./gradlew` invocation.

---

- **Fix:** Regenerate the wrapper with a trusted Gradle install and diff the result against what is committed — a genuine jar is byte-identical to the one that install ships, so a clean diff is the verification:

  ```
  gradle wrapper --gradle-version <the version in distributionUrl>
  git diff --stat gradle/wrapper/gradle-wrapper.jar
  ```

  Silent output means the committed jar matches what that Gradle release produces. Any difference is the finding, and it is not one to fix by overwriting the file quietly — say what differed.

  Match the version to the one already in `distributionUrl`: regenerating at a different version changes the jar for a legitimate reason and tells you nothing about the old one.

  This check is about the jar. Pinning `distributionSha256Sum` for the distribution the jar downloads is the separate `validate_gradle_checksum` fix; a project usually wants both.
