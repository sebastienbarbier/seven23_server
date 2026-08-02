# API contract tests

Kept under ``seven23.tests`` (not under ``seven23.api``) so this package can be
removed without touching API implementation modules.

- `shapes.py` — shared JSON shape matcher
- `v1/` — frozen contracts for `API_VERSION = [1, 1, 0]`

When response JSON must change incompatibly: bump `API_VERSION`, add `v2/`, keep `v1/` until clients migrate.

```shell
uv run python manage.py test seven23.tests.contracts --settings seven23.settings_tests --parallel auto
```
