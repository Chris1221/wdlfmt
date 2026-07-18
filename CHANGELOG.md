# Changelog

## [0.2.0](https://github.com/Chris1221/wdlfmt/compare/v0.1.3...v0.2.0) (2026-07-18)


### Features

* add --check / -c flag for CI format enforcement ([66a3626](https://github.com/Chris1221/wdlfmt/commit/66a362671964cab3d604458854cf0b4238c2c7be))


### Documentation

* link to live check-formatting workflow from usage page ([e4c5925](https://github.com/Chris1221/wdlfmt/commit/e4c5925d41cdb926c27c7924d329d16f611066a6))

## [0.1.3](https://github.com/Chris1221/wdlfmt/compare/v0.1.2...v0.1.3) (2026-07-18)


### Documentation

* remove incorrect pip&gt;=23 requirement for PyPI install ([50a4a9f](https://github.com/Chris1221/wdlfmt/commit/50a4a9f8350df64bfa7df043a94d13aa0f8ab4ee))

## [0.1.2](https://github.com/Chris1221/wdlfmt/compare/v0.1.1...v0.1.2) (2026-07-18)


### Documentation

* add MkDocs site with full documentation ([8badf56](https://github.com/Chris1221/wdlfmt/commit/8badf56c3b8cc9a2ab88ca84164a504888f97c5f))

## [0.1.1](https://github.com/Chris1221/wdlfmt/compare/v0.1.0...v0.1.1) (2026-07-18)


### Bug Fixes

* add Python version classifiers and fix pepy.tech badge URL ([fae8958](https://github.com/Chris1221/wdlfmt/commit/fae8958f8660eedb04e782d4164894be14ae7558))
* resolve shfmt binary relative to sys.executable ([0968e7b](https://github.com/Chris1221/wdlfmt/commit/0968e7bee2eec954473965648a1bde6d2287fe3c))


### Documentation

* update README with PyPI install, badges, and technical overview ([39dcc5e](https://github.com/Chris1221/wdlfmt/commit/39dcc5e67d87b49653c63b97849b5cbee2ddeae9))

## 0.1.0 (2026-07-18)


### Features

* add BioWDL style guide compliance checker ([228ab25](https://github.com/Chris1221/wdlfmt/commit/228ab25cce3568e4a991c62e5891567a7e671f56))
* attempting to debug the multi process memory issue ([2103b35](https://github.com/Chris1221/wdlfmt/commit/2103b3559c3e598b5092170cb5f50ca4e5c094c8))
* comments finally working ([09987e7](https://github.com/Chris1221/wdlfmt/commit/09987e7a4f4af2bb72c06eaf6951a0e4ec7a76e2))
* comments working except in runtime and output ([b1fbda0](https://github.com/Chris1221/wdlfmt/commit/b1fbda06358d0e914b36e96cec756f8f0db2874c))
* comments working now but appending to the end ([b3558b1](https://github.com/Chris1221/wdlfmt/commit/b3558b13598fd00bffa77eaf6b4c95ff013362de))
* if error, just print raw string ([91d7c48](https://github.com/Chris1221/wdlfmt/commit/91d7c48c65018baea7b7436110ec4f975cb2b1bb))
* init ([0c5e206](https://github.com/Chris1221/wdlfmt/commit/0c5e206ae08d3ae0a6a2bcfc0f4c7c4fa5c42547))
* input ([f5d68dd](https://github.com/Chris1221/wdlfmt/commit/f5d68dd1dd23c2fbdb5029a0d1176beaad1056da))
* more concise logic for creating dict ([3ae890c](https://github.com/Chris1221/wdlfmt/commit/3ae890ce0acd3a46fe6265f26bacd0344e4d4b63))
* moved collect formatters, added biowdl tests, still workign through them ([0dbfdf1](https://github.com/Chris1221/wdlfmt/commit/0dbfdf1a4dbe568f4115e039175634ec140c8d0e))
* output and indent ([581adbe](https://github.com/Chris1221/wdlfmt/commit/581adbe19b2ff4f705db7b5e64d1ad5698d9879d))
* ready to start work on workflows ([cfd6916](https://github.com/Chris1221/wdlfmt/commit/cfd6916abfbc5df70bbf944873179a4b4be621ec))
* reuse task formatters for workflow ([317db91](https://github.com/Chris1221/wdlfmt/commit/317db91e2269927dd199d7f03abb04757669650b))
* shell formatting ([e8ee09c](https://github.com/Chris1221/wdlfmt/commit/e8ee09c28d45ad5a1b9cb1f1d797cb9a6482d96f))
* struct formatter and equality assertions, fix [#2](https://github.com/Chris1221/wdlfmt/issues/2) ([401a57f](https://github.com/Chris1221/wdlfmt/commit/401a57f6b1e1931b8529a5a07e1a48846a6e3b0e))
* substitution in shell formatting ([85500a5](https://github.com/Chris1221/wdlfmt/commit/85500a5fba45d4ca343aee6e057d2961a197a9d4))
* threading comments, repeating comments now so not doneyet ([5a40108](https://github.com/Chris1221/wdlfmt/commit/5a40108ff9b65fd6789fbe831c8613ea48f79de5))
* workflow call context ([07dc933](https://github.com/Chris1221/wdlfmt/commit/07dc9333da0b176d6e8cc6566770e91ae7f470c3))


### Bug Fixes

* add whole workflow assertions, fix [#6](https://github.com/Chris1221/wdlfmt/issues/6) ([2249ed6](https://github.com/Chris1221/wdlfmt/commit/2249ed6728588e5b8007b2d9424bbc076e9c6c16))
* cleanup ([1429682](https://github.com/Chris1221/wdlfmt/commit/14296828096a725153cdc77082ccc8f8cb88eea4))
* easier logic for formatter ([432f351](https://github.com/Chris1221/wdlfmt/commit/432f351b15a3e45c753dfb6a2b485c0cce39ee0b))
* fixed tests, must run in subprocess ([85500a5](https://github.com/Chris1221/wdlfmt/commit/85500a5fba45d4ca343aee6e057d2961a197a9d4))
* **grammar:** support sep option with spaces around = in command expressions ([2e460c1](https://github.com/Chris1221/wdlfmt/commit/2e460c15c55ce292d90a00558e003c55cda46867))
* init ([65d05f3](https://github.com/Chris1221/wdlfmt/commit/65d05f358503e9dfecc7e8a65ca03e7144957d10))
* multi file working now ([05b88f8](https://github.com/Chris1221/wdlfmt/commit/05b88f89ca70a1823aa9f759f00739c1d3579d4b))
* prevent comment-dropping when formatting multiple files in one process ([9f58637](https://github.com/Chris1221/wdlfmt/commit/9f586373a980b71a8c2f4c202d9ed30c5af43bfa))
* resolve all flake8 lint violations ([268bb03](https://github.com/Chris1221/wdlfmt/commit/268bb0368887694abcb1424d5f7cc2f98c23633d))
* silence debug logging by default ([63d6db4](https://github.com/Chris1221/wdlfmt/commit/63d6db4bb813dc7b52084db4efa6573ec2c85ba9))
* tweak ([c7cf5d7](https://github.com/Chris1221/wdlfmt/commit/c7cf5d7ff87001a89933803722379f8dcce274a9))


### Documentation

* rewrite README with usage examples and style checker description ([07dd950](https://github.com/Chris1221/wdlfmt/commit/07dd950f0d3274b7987beb74cf08a703673f0c4b))
