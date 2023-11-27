# Change Log

All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
 <!---
## [Unreleased] - yyyy-mm-dd

### ✨ Feature – for new features
### 🛠 Improvements – for general improvements
### 🚨 Changed – for changes in existing functionality
### ⚠️ Deprecated – for soon-to-be removed features
### 📚 Documentation – for documentation update
### 🗑 Removed – for removed features
### 🐛 Bug Fixes – for any bug fixes
### 🔒 Security – in case of vulnerabilities
### 🏗 Chore – for tidying code

See for sample https://raw.githubusercontent.com/favoloso/conventional-changelog-emoji/master/CHANGELOG.md
-->

## [1.5.0] - 2023-11-DD
### 🔒 Security
- Migrate to Django 4.2+ (#71)

## [1.4.0] - 2023-06-19
### 🛠 Improvements
- Add boolean to **store if private key has been saved** and verified (#91)

## [1.3.1] - 2023-05-10
### 🔒 Security
- **Bump django** from *4.1.8* to *4.1.9* (#85)
### 🐛 Bug Fixes
- **Fix crash** settings if debug false (#86)

## [1.3.0] - 2023-05-09
### 🛠 Improvements
- Apply **auto_sync settings for all accounts** instead of individual one (#81)
- **Log config** for easier deployment (#83)
### 🐛 Bug Fixes
- Settings **autosync** fails (#80)
- **Registration**  returing 204 instead of 201 (#82)

## [1.2.0] - 2023-04-24
### ✨ Feature
- Publish **docker** image ([#69](https://github.com/sebastienbarbier/seven23_server/issues/69))
- Improve **self-hosted experience** ([#66](https://github.com/sebastienbarbier/seven23_server/issues/66))
### 📚 Documentation
- Fix broken links to **swagger** and **redoc** ([#68](https://github.com/sebastienbarbier/seven23_server/issues/68))
### 🔒 Security
- Security updates ([#67](https://github.com/sebastienbarbier/seven23_server/issues/67))

## [1.1.0] - 2022-12-13
### ✨ Feature
- Allow **SQLite** for data storage ([#49](https://github.com/sebastienbarbier/seven23_server/issues/49))
### 🔒 Security
- Update dependencies ([#52](https://github.com/sebastienbarbier/seven23_server/issues/52))
### 🐛 Bug Fixes
- Fix broken password/reset/confirm API ([#60](https://github.com/sebastienbarbier/seven23_server/issues/60))
### 🏗 Chore
- Migrate **Continous Integration** from travis-ci to **Github actions** ([#40](https://github.com/sebastienbarbier/seven23_server/issues/40))
- Run within **Docker** ([#48](https://github.com/sebastienbarbier/seven23_server/issues/48))

## [1.0.1] - 2022-04-07
### 🔒 Security
- **Django** Security update ([#46](https://github.com/sebastienbarbier/seven23_server/issues/46))

## [1.0.0] - 2022-06-08
### ✨ Feature
- Initial **data model**
- **REST API** to fetch data models
- **Admin interface** for data handling.
- **Home page** with logo and redirection to [app.seven23.io](https://app.seven23.io)
### 📚 Documentation
- Implement **Swagger** and **redoc**.
- Export `docs` folder on **readthedocs**.