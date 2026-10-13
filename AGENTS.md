# Portfolio boundaries

This repository contains original, fictional demonstrations for Miguel Moreno's public portfolio.

- Never import client code, source history, records, screenshots, credentials, infrastructure IDs, private URLs, or internal documents.
- Invent fixtures from scratch. Use reserved `.example` domains if an address is needed.
- Label simulated behavior. The assistant uses deterministic tools, not a live model. No production performance claims.
- No runtime third-party connections, analytics, cloud credentials, or package dependencies.
- Bind the demo server to localhost. This is a local review tool, not a hosted production service.
- Test with `python3 -m unittest discover -s tests -v` `node --check static/app.js`, and `node --test tests/frontend.test.cjs`.
- Before publishing: review the full tracked tree, run tests and the public-content check, and verify screenshots contain only this demo.
- Future applications must link to this portfolio, not private project repositories or the broad GitHub profile.
