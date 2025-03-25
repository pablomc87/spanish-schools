# CHANGELOG



## v0.1.0 (2025-03-25)

### Feature

* feat: add linting and testing workflow with mypy support, and add tests (#1)

* ci: add linting and testing workflow with mypy support, and add tests ([`26da9e2`](https://github.com/pablomc87/spanish-schools/commit/26da9e20fe7c638d782ccaad8e5203d61cd4fbe3))

### Unknown

* fix ([`4a3c95b`](https://github.com/pablomc87/spanish-schools/commit/4a3c95b6e101656c5c7b8cc4657e6d188d98b08b))

* allowing releases to overwrite main ([`722452f`](https://github.com/pablomc87/spanish-schools/commit/722452f44e00f7ef5130709997b35c336125c2d7))


## v0.0.3 (2025-03-24)

### Fix

* fix(scraper): improve HTML parsing in ListScraper for robust school ID extraction

- Refactor table detection to handle escaped HTML attributes

- Update HTML parsing to use CSS selectors instead of direct attribute search

- Replace payload with body in tests to prevent double-encoding issues

- Add additional test cases for edge conditions (no tables, malformed HTML)

- Improve logging for better debugging ([`0dcce0f`](https://github.com/pablomc87/spanish-schools/commit/0dcce0f472891f135f0be0a36feaf228e1f66aea))


## v0.0.2 (2025-03-24)

### Fix

* fix(readme): correct repository path ([`101579c`](https://github.com/pablomc87/spanish-schools/commit/101579c62265c3a93af81b860eca21743742b60b))


## v0.0.1 (2025-03-24)

### Fix

* fix: add required permissions for semantic release ([`b9a1ac1`](https://github.com/pablomc87/spanish-schools/commit/b9a1ac10c71b0abc6e5d8f8295d5b9ba529f012d))

* fix: properly install semantic-release in workflow ([`5a1f4b1`](https://github.com/pablomc87/spanish-schools/commit/5a1f4b12c273cf4d5e2caf97cfcd81ef43b9c6a7))

* fix: use Python-specific semantic release action ([`79a4a53`](https://github.com/pablomc87/spanish-schools/commit/79a4a53ced3e208597654ab27e9b8587bd22c9ad))

### Refactor

* refactor: switch to semantic-release-action for faster releases ([`ea960a6`](https://github.com/pablomc87/spanish-schools/commit/ea960a658d9627eeb4c28f0f17adc7c3f698d27a))

### Unknown

* revert: restore original semantic release workflow ([`73c8122`](https://github.com/pablomc87/spanish-schools/commit/73c81220314a91eafd1858c3857bfee651661ffd))

* Add automated release workflow with semantic versioning ([`9c37df0`](https://github.com/pablomc87/spanish-schools/commit/9c37df0f749140c865146f899cbadf85b4117853))

* Initial commit: Spanish schools scraper with database support ([`9e1fe08`](https://github.com/pablomc87/spanish-schools/commit/9e1fe08f2d5f05feaf38140276a0817e6a0bf8b7))
