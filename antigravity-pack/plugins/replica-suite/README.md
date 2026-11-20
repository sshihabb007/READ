# Replica App-Cloning & Parity Suite (`replica-suite`)

Bundles all 11 clean-room app-cloning skills and 6 zero-dependency Python verification tools from [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) (MIT License):

- `replica-recon` -> `replica-architect` -> `replica-design` -> `replica-build` -> `replica-backend` -> `replica-test` -> `replica-diff` -> `replica-entrepreneur` -> `replica-brand` -> `replica-launch` -> `replica-deploy`

Verification tools included under `skills/<skill>/`:
- `skills/replica-design/contrast.py` - WCAG 2.2 AA/AAA contrast checker
- `skills/replica-diff/imgdiff.py` - Layout-only PNG edge diff (ignores palette changes)
- `skills/replica-diff/parity.py` - Weighted Must/Should/Could feature & layout parity scorer
- `skills/replica-entrepreneur/reviews.py` - Linked verbatim user-review complaint ranker
- `skills/replica-brand/sweep.py` - Codebase & filename leftover sweep for rebranding
- `skills/replica-launch/listing.py` - App Store & Google Play character/claim/copycat linter

Run tool unit tests:

```bash
python3 -m unittest discover -s tests -v
```
