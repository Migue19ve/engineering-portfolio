# Public portfolio checkpoint

## Source and purpose

Original project: `Migue19ve/engineering-portfolio`; default branch: `main`. The demo implementation was merged in PR #1, and the expanded profile was merged in PR #2 at `a28d0ec64354042c539975abe12f9243cfe453fe`. All business fixtures are invented; no source history or files were copied from another project.

## Current verification

- 25 Python tests and 3 JavaScript regression tests pass locally, including HTTP integration checks and asynchronous stale-response behavior.
- JavaScript syntax and tracked-file public-content checks pass. All screenshots and tracked source were reviewed for private material.
- Browser verification covered event replay, mixed CSV validation, clean JSON export (USD 266.20), export invalidation after editing, assistant evidence, blocked actions, and answer invalidation after editing.
- Desktop (1280 px), medium (752 px), and mobile (390 px) layouts were checked; mobile panels do not overflow horizontally. Five direct browser screenshots are included, covering the demos and expanded profile.
- Independent review identified malformed CSV header handling, physical line-number reporting, stale assistant answers, and a credential-pattern gap. All were corrected and regression-tested. A follow-up review requested one additional CSV stale-response test; it was added and passes. The second correctness review passed; independent HTTP checks are limited by the review sandbox's socket restrictions. Full HTTP checks passed in the local workspace.

## Publication

Destination ownership and repository name verified as `Migue19ve/engineering-portfolio`. PRs #1 and #2 were merged after passing CI. The published profile includes eight high-level experience summaries. All 28 automated checks passed for the expanded implementation; desktop and 390 px mobile layouts were inspected, with no horizontal overflow. The app runs locally; there is no public server deployment.

## Future applications

Use this repository's exact URL, following `docs/APPLICATIONS.md`. Do not expose client source or use the broad GitHub profile as the default work-sample link.

The October 13 application review added a reusable submission checklist to that guide. Application records, contact details, immigration answers, and employer correspondence remain outside this public repository. No functional demo changes are included in that documentation update.
