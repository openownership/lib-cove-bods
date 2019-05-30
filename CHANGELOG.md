# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Statistic: Count of ownership-or-control statements by year
- Statistic: Count of subjects of ownership-or-control statements by year
- Statistic: Count of different kinds of interested parties by year

## [0.4.0] - 2019-04-02

### Added

- Statistic: Entity Statements with one or more identifiers, by statement type
- Statistic: Entity Statements with one or more identifiers with scheme and id, by statement type
- Statistic: Statements referenced in replacesStatements, but have not appeared in the file yet

### Changed

- Use lib-cove version 0.5.0, which includes schema validation message changes

### Fixed

- scheme is not required in identifier object so if it's not there, that should not trigger an error

## [0.3.0] - 2019-03-22

### Added

- Statistic: % of Persons of each type
- Statistic: % of type of interest statement in ownership-or-control statement
- Statistic: % of ownership-or-control statements with unspecified interestedParty
- Statistic: % of Entities of each type
- Additional Checks: Each statement must have an entirely unique identifier
- Additional Checks: Check Birth Date is in acceptable range

### Changed

- Require jsonschema version before 2.7
- Updated standard Schema to V0.1

## [0.2.0] - 2018-12-04

### Added

- Additional Checks: All relevant statements are present
- Additional Checks: All relevant statements are in correct order
- Additional Checks: Person or entity statements should be used in an ownership-or-control statement
- Additional Checks: scheme should be an org-id code (This requires lib-cove 0.2.0 or higher)
- Statistic: % of Interests of each type

### Changed

- Upgrades lib-cove needed to 0.3.1

## [0.1.0] - 2018-11-22

First Release
