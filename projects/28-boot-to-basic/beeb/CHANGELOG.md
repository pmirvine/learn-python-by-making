# Changelog

Everything that a user of beeb would notice is written down here, newest first.
The format is that of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the version numbers follow [semantic versioning](https://semver.org).

## [Unreleased]

## [1.1.0] - 2026-09-27

### Added

- `beeb.canvas()`, which returns the surface that's being drawn on, for programs
  that would sooner put it on the screen themselves than call `vsync`.

## [1.0.0] - 2026-09-20

The interface is now a promise: everything in `beeb.__all__` will go on working
until 2.0.

### Added

- `beeb --version`, and `beeb.__version__`.
- Type hints are published: the package has a `py.typed`, and passes pyright's strict mode.
- A README, a licence (MIT) and this changelog.

### Changed

- The name to install is now `beeb-lpbm`. The name to import is still `beeb`.
- The test card beeps.

### Fixed

- `beeb.synth.samples` said that it returned an `array`, and didn't say of what.

## [0.2.0] - 2026-09-12

### Added

- `sound` and `envelope`: three channels of square waves, and one of noise.
- `beeb.synth`, for making samples without playing them.

## [0.1.0] - 2026-09-08

### Added

- `mode`, `gcol`, `clg`, `move`, `draw`, `plot`, `point`, `inkey`, `mouse`, `vsync`
  and `screenshot`.
- The `beeb` command, which shows a test card.

[Unreleased]: https://github.com/yourname/beeb/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/yourname/beeb/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yourname/beeb/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/yourname/beeb/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourname/beeb/releases/tag/v0.1.0
