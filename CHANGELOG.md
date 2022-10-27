# Changelog
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`<major>`.`<minor>`.`<patch>`)

## [0.5.1]
### Fixed
* Fix incorrect output type for `<split_on>`; the main loop contained a `str2num` call but the function should only return a `LoxArray` of strings.

### Added
* Add `<map>` to pure-lox stdlib headers.

## [0.5.0]
### Added
* #4 Add a basic import mechanism
  * Supports "stdlib" imports (`<header_name>`) and path imports (`"path/to/file"`)
  * Recursive `include` not supported
  * Imported source assumed to be valid code
* Add initial pure-lox stdlib headers:
  * `<array_sum>`
  * `<hello_world>`
  * `<split_on>`
* #18 Add additional builtins:
  * `re_findall`
  * `re_match`
  * `re_search`
  * `re_sub`

### Fixed
* #20 Fixed string representation of nested `LoxArray`s

## [v0.4.0]
### Added
* Add a `LoxArray` `join` method to join an array of strings together
* Add a `LoxArray` `slice` method to slice the array into a new instance

## [v0.3.2]
### Fixed
* Pass the actual arguments for `str2num` instead of a `list` generic.

## [v0.3.1]
### Fixed
* #19 Fix incorrect generation of string literals during scanning.

## [v0.3.0]
### Added
* Add additional builtins:
  * `str2num`

## [v0.2.0]
### Added
* Add support for block comments (`/* ... */`)
* Add an array object (`LoxArray`)
* Add additional builtins:
  * `array`
  * `divmod`
  * `input`
  * `len`
  * `mean`
  * `median`
  * `mode`
  * `ord`
  * `read_text`
  * `std`
  * `string_array`

### Changed
  * Tokens now store end line/column locations, allowing for better support of multiline code constructs (e.g. strings)

### Fixed
  * Fixed incorrect token metadata for multiline strings

## [v0.1.0]
Initial Release!!! 🥯🎉🥳
