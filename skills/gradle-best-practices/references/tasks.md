# Tasks

Base URL for every anchor below: `https://docs.gradle.org/current/userguide/best_practices_tasks.html`

Read this file only if the build registers or configures a task, or has task/plugin source under `buildSrc/` or `build-logic/`.

---

## Avoid DependsOn
`avoid_depends_on` · 8.14 · **Medium**

- **Rule:** Use `dependsOn` only for lifecycle tasks that have no actions. Between tasks that do work, declare inputs and outputs and let Gradle infer the ordering.
- **Applies when:** Any `dependsOn` appears.
- **Detect** (deterministic): `dependsOn` in a build script or task definition where the depended-on task has a `@TaskAction` or `doLast`/`doFirst` (i.e. is not a pure lifecycle task such as `build`, `check`, `assemble`).
- **Fix:** see `references/fixes/avoid_depends_on.md` — read it only when you are about to apply this entry.

---

## Favor `@CacheableTask` / `@DisableCachingByDefault`
`use_cacheability_annotations` · 8.14 · **Medium**

- **Rule:** Declare cacheability on the task class with `@CacheableTask` or `@DisableCachingByDefault`, not per instance with `cacheIf` / `doNotCacheIf`.
- **Applies when:** The build defines a custom task type.
- **Detect** (deterministic): `outputs.cacheIf` or `outputs.doNotCacheIf` anywhere.
- **Fix:** see `references/fixes/use_cacheability_annotations.md` — read it only when you are about to apply this entry.

---

## Group and Describe custom Tasks
`group_describe_tasks` · 9.0.0 · **Recommendation**

- **Rule:** Give every custom task a `group` and a `description` so it is discoverable in the task report.
- **Applies when:** The build registers a task.
- **Detect** (deterministic): a `tasks.register(` / `tasks.create(` block, or a custom task class, with no `group =` / `group` and no `description =` / `description` assignment.
- **Fix:** see `references/fixes/group_describe_tasks.md` — read it only when you are about to apply this entry.

---

## Do not call `get()` on a Provider outside a Task action
`avoid_provider_get_outside_task_action` · 9.1.0 · **High**

- **Rule:** Do not query a provider during configuration; transform it with `map` / `flatMap` so the value is read at execution time.
- **Applies when:** The build uses providers or lazy properties.
- **Detect** (deterministic): `.get()`, `.getOrElse(`, `.getOrNull()`, `.isPresent` on a `Provider`/`Property`, or `layout.buildDirectory.get()`, at the top level of a script or inside a task *configuration* block — as opposed to inside `@TaskAction` / `doLast`.
- **Fix:** see `references/fixes/avoid_provider_get_outside_task_action.md` — read it only when you are about to apply this entry.

---

## Don't resolve Configurations before Task Execution
`dont_resolve_configurations_before_task_execution` · 9.1.0 · **High**

- **Rule:** Do not resolve a configuration during the configuration phase; pass the configuration itself to the task input so dependency information survives.
- **Applies when:** The build passes a configuration to a task.
- **Detect** (deterministic): `.resolve()` on a configuration, or assignment of `configurations.<name>.files` / `.asFileTree` / `.singleFile` to a task property during configuration.
- **Fix:** see `references/fixes/dont_resolve_configurations_before_task_execution.md` — read it only when you are about to apply this entry.

---

## Avoid using eager APIs on File Collections
`avoid_eager_file_collection_apis` · 9.1.0 · **High**

- **Rule:** Do not call methods that force a `FileCollection` or `Configuration` to resolve during configuration.
- **Applies when:** The build touches file collections or configurations.
- **Detect** (deterministic): `.size`, `.isEmpty()`, `.files`, `.asPath`, `.toList()`, or arithmetic (`+`) on a `Configuration` / `FileCollection` outside a task action.
- **Fix:** see `references/fixes/avoid_eager_file_collection_apis.md` — read it only when you are about to apply this entry.

---

## Prefer `@PathSensitivity.NONE` for files, `RELATIVE` for directories
`default_path_sensitivities` · 9.2.0 · **Medium**

- **Rule:** Annotate file inputs `@PathSensitive(PathSensitivity.NONE)` and directory inputs `@PathSensitive(PathSensitivity.RELATIVE)`, so absolute paths do not defeat up-to-date checks and caching.
- **Applies when:** The build defines a custom task type with file or directory inputs.
- **Detect** (deterministic): `PathSensitivity.ABSOLUTE`; `PathSensitivity.NAME_ONLY` on an input; or an `@InputFile` / `@InputFiles` / `@InputDirectory` with no `@PathSensitive` at all (the default is `ABSOLUTE`).
- **Fix:** see `references/fixes/default_path_sensitivities.md` — read it only when you are about to apply this entry.

---

## Use unique output files and directories
`use_unique_output_files_and_directories` · 9.3.0 · **Medium**

- **Rule:** Give each task its own output location, so a sibling task writing to a shared directory does not invalidate it.
- **Applies when:** Two or more tasks declare outputs.
- **Detect** (deterministic): two task registrations whose `@OutputDirectory` / `outputs.dir` resolve to the same path, e.g. both using `layout.buildDirectory.dir("greetings")`.
- **Fix:** see `references/fixes/use_unique_output_files_and_directories.md` — read it only when you are about to apply this entry.

---

## Don't hardcode Task names unless they are documented as Public API
`dont_hardcode_task_names` · 9.7.0 · **Recommendation**

- **Rule:** Prefer, in this order: (1) the plugin's own DSL extension, (2) the task *type*, (3) a task name — and only when that name is explicitly documented as public API. Most task names in Gradle and in third-party plugins are internal details that may be renamed or removed.
- **Applies when:** The build looks tasks up by name.
- **Detect** (heuristic): `tasks.named("...")` / `tasks.getByName("...")` with a **string literal** task name, e.g. `"generatePomFileForMavenPublication"`. Two things are *not* violations and must not be flagged:
  - `tasks.withType<JavaCompile>()` and other by-**type** lookups — the documentation ranks configuring by type *above* configuring by name, so flagging it inverts the practice.
  - A name supplied as a documented public constant, e.g. `tasks.named(JavaPlugin.COMPILE_JAVA_TASK_NAME)`.

  This is heuristic because deciding whether a given literal is documented public API needs judgment; report the literal and say why it looks internal.
- **Fix:** see `references/fixes/dont_hardcode_task_names.md` — read it only when you are about to apply this entry.

---

## Don't access a `Project` instance during Task Execution
`dont_access_project_instance_inside_task` · 9.7.0 · **High**

- **Rule:** Do not touch `Project` inside a task action; capture what you need as inputs at configuration time.
- **Applies when:** The build defines a custom task type or uses `doLast`/`doFirst`.
- **Detect** (deterministic): `project.` inside a `@TaskAction` method, or inside a `doLast {` / `doFirst {` block — e.g. `project.version`, `project.layout`, `project.file(...)`.
- **Fix:** see `references/fixes/dont_access_project_instance_inside_task.md` — read it only when you are about to apply this entry.

---

## Wiring Task Outputs with `map` and `flatMap`
`map_versus_flatmap` · 9.7.0 · **Medium**

- **Rule:** Use `flatMap` to reach a `Provider`-typed output of a task and `map` to transform a value, keeping the dependency chain intact.
- **Applies when:** One task consumes another's output.
- **Detect** (deterministic): `.get()` inside a `map {` / `flatMap {` closure; a bare `provider { someTask.get().output.get() }`; or `map { it.property.get() }`.
- **Fix:** see `references/fixes/map_versus_flatmap.md` — read it only when you are about to apply this entry.
