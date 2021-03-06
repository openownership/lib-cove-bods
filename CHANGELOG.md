# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.10.0] - 2021-04-08

### Changed

- Update to latest lib-cove and lib-cove-web, and make some changes to the tests for compatibility with these

## [0.9.0] - 2021-01-27

### Changed

- Update to latest lib-cove and lib-cove-web, and make some changes for compatibility with these

## [0.8.1] - 2021-01-06

### Fixed

- Catch error when `statementDate` is `null`

## [0.8.0] - 2020-08-28

### Changed

- Rename schema object attributes to remove word "release", as in latest lib-cove

## [0.7.0] - 2020-06-26

### Changed

- requirements: Update Django to 2.2 LTS and lib-cove to latest

## [0.6.0] - 2020-02-18

Changes to packaging only; 

- Removed all requirements files and moved to setup.py
- Require latest version of lib-cove, so that optional flatten-tool dependencies are pulled in [#54](https://github.com/openownership/lib-cove-bods/pull/54#issuecomment-585303356)
- Moved data underneath main folder where it can be included in package

## [0.5.0] - 2019-07-19

### Added

- Support for schema version 0.2.
  If no meta information is in the data, 0.1 is assumed and work happens as before.
  - Add new schema_version key for reporting https://github.com/openownership/lib-cove-bods/issues/28
  - The options in count_ownership_or_control_statement_interest_statement_types are different in schema 0.1 and 0.2
- Statistic: Count of current ownership/control statements
- Statistic: Count of ownership-or-control statements by year
- Statistic: Count of subjects of ownership-or-control statements by year
- Statistic: Count of different kinds of interested parties by year
- Improve validation error messages (including oneOf)
  - https://github.com/openownership/cove-bods/issues/16
  - https://github.com/openownership/lib-cove-bods/pull/5
  - This adds translation issues, human messages and a requirement for Django; it was not intended that these should be in this library but as discussed in the pull request we added it hopefully temporarily.
- Statistic: hasPepStatus (0.2 only) https://github.com/openownership/lib-cove-bods/issues/29
- Statistic: pepStatusDetails.missingInfoReason (0.2 only) https://github.com/openownership/lib-cove-bods/issues/30
- Additional Check: inconsistent bodsVersion https://github.com/openownership/lib-cove-bods/issues/27
- Additional Check: address types (0.2 only) https://github.com/openownership/lib-cove-bods/issues/22
- Additional Check: ownership_or_control_statement has is_compontent and component_statement_ids (0.2 only) https://github.com/openownership/lib-cove-bods/issues/26
- Additional Check: component_statement_id not in package (0.2 only) https://github.com/openownership/lib-cove-bods/issues/25
- Additional Check: statement_is_component_but_not_used_in_component_statement_ids and statement_is_component_but_is_after_use_in_component_statement_id (0.2 only) 
  - https://github.com/openownership/lib-cove-bods/issues/24
  - https://github.com/openownership/lib-cove-bods/issues/23
- Statistic: Addresses, with country, with postcode, with postcode in address https://github.com/openownership/lib-cove-bods/issues/16

### Changed

- get_statistics() function becomes GetStatistics class, like the RunAdditionalChecks class

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
