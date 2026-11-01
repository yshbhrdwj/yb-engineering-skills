# Comparison with Ponytail

YB adopts a useful simplification procedure: use what is already present, then native facilities or installed dependencies, and add only the code required to satisfy the task. It combines that with focused verification and separate product, architecture, review, QA and operations roles.

The two code reviewers are now one `yb-code-reviewer`, covering behavior and design concerns only where they have concrete cost. This avoids duplicate reads and overlapping reports. State changes retain four explicit cases: concurrent operations, old/new compatibility, interrupted operation with retry, and the first item past a limit.

Ponytail's [core skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md), [review](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md), and [audit](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-audit/SKILL.md) were examined in the earlier research. This is historical scope context; the links are moving branches and do not pin a tested version.

There is **no controlled head-to-head result showing YB is faster or more accurate than Ponytail**. The recovered historical old/new trials had Ponytail instructions present in both arms, one run per case, incomplete harness metadata and several weak assertions. They cannot isolate either plugin's effect. See [validation](VALIDATION.md).

The new [synthetic cases and protocol](evals/README.md) judge actual outcomes: correct behavior, real defects found, false positives, preserved scope and authority, and honest evidence. A future comparison should pin repository, host, model, effort, tools, hooks and plugin versions; repeat matched runs with no-skill and length-matched controls; report time and tokens alongside quality. Shorter text or a smaller diff alone is not a quality score.
