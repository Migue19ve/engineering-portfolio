# Public portfolio checkpoint

## Source and purpose

New original project: `Migue19ve/engineering-portfolio`. Current task branch: `codex/experience-profile`; default branch: `main`. Original demo implementation was merged in PR #1. All business fixtures are invented; no source history or files were copied from another project.

## Current verification

- 25 Python tests and 3 JavaScript regression tests pass locally, including HTTP integration checks and asynchronous stale-response behavior.
- JavaScript syntax and tracked-file public-content checks pass. All screenshots and tracked source were reviewed for private material.
- Browser verification covered event replay, mixed CSV validation, clean JSON export (USD 266.20), export invalidation after editing, assistant evidence, blocked actions, and answer invalidation after editing.
- Desktop (1280 px), medium (752 px), and mobile (390 px) layouts were checked; mobile panels do not overflow horizontally. Four direct browser screenshots are included.
- Independent review identified malformed CSV header handling, physical line-number reporting, stale assistant answers, and a credential-pattern gap. All were corrected and regression-tested. A follow-up review requested one additional CSV stale-response test; it was added and passes. The second correctness review passed; independent HTTP checks are limited by the review sandbox's socket restrictions. Full HTTP checks passed in the local workspace.

## Publication

Destination ownership and repository name verified as `Migue19ve/engineering-portfolio`. PR #1 was merged after passing CI. The current branch expands the personal profile with eight high-level experience summaries. All 28 automated checks pass; desktop and 390 px mobile layouts were inspected, with no horizontal overflow. Publication of this expansion is pending. The app runs locally; no public server deployment is planned.

## Future applications

Use this repository's exact URL, following `docs/APPLICATIONS.md`. Do not expose client source or use the broad GitHub profile as the default work-sample link.
