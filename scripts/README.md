# scripts

Thin wrappers, so a bare checkout works without an install, and generators for
everything derived.

| Script | Does |
|---|---|
| `atlas` | Run the CLI from a checkout: `scripts/atlas check` |
| `build_reference.py` | Regenerate `docs/reference/cli.md` from the argument parser |
| `build_library.py` | Regenerate `library/prompts/index.yaml` from the prompt files |
| `build_design.py` | Derive `assets/design/tokens.yaml` and the design index from `library/design/DESIGN.md` |
| `build_assets.py` | Regenerate the badges from `project.yaml` and the design tokens |
| `build_screenshots.py` | Re-record the README's terminal demos by running the commands |

Everything here derives something from something else in the repository. If a
generated file and its source disagree, the source wins and the script is
re-run. The `generated-current` gate makes that a failure rather than a habit.
