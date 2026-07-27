# Changelog

## [0.4.0](https://github.com/alekseibq/ai-for-developers-project-387/compare/calcom-v0.3.0...calcom-v0.4.0) (2026-07-27)


### Features

* **ci:** auto-explain new issues with opencode ([ffb7c86](https://github.com/alekseibq/ai-for-developers-project-387/commit/ffb7c869b0054bc4cd31108579aec3dc89788e84))
* **ci:** auto-explain new issues with opencode ([8d5eea9](https://github.com/alekseibq/ai-for-developers-project-387/commit/8d5eea91c2367d5125731c188c502fa69209ab7f))


### Bug Fixes

* **backend:** remove allow_credentials from CORS config ([a9e76cb](https://github.com/alekseibq/ai-for-developers-project-387/commit/a9e76cbed33fc6302b2082e2226316e30981e341))
* **backend:** remove allow_credentials from CORS config ([2567b7b](https://github.com/alekseibq/ai-for-developers-project-387/commit/2567b7b1cedd8014eea67fe11d41afdc38ce5900)), closes [#22](https://github.com/alekseibq/ai-for-developers-project-387/issues/22)
* **ci:** add model and env config for opencode action in lighthouse workflow ([e1d9fe3](https://github.com/alekseibq/ai-for-developers-project-387/commit/e1d9fe33f37155720abaf7f8e71fc8067b2fb604))
* **ci:** add model and env config for opencode action in lighthouse workflow ([a22a29b](https://github.com/alekseibq/ai-for-developers-project-387/commit/a22a29b22315fa60ad8cf482d3cf5c4709231be8))

## [0.3.0](https://github.com/alekseibq/ai-for-developers-project-387/compare/calcom-v0.2.0...calcom-v0.3.0) (2026-07-27)


### Features

* **infra:** add Lighthouse CI audit workflow ([67e72c3](https://github.com/alekseibq/ai-for-developers-project-387/commit/67e72c3880d34217e68ef7d9a83801b421f7fab1))
* **infra:** add Lighthouse CI audit workflow ([8b4baf1](https://github.com/alekseibq/ai-for-developers-project-387/commit/8b4baf165896aaf10170a213233ba738100f64d1))

## [0.2.0](https://github.com/alekseibq/ai-for-developers-project-387/compare/calcom-v0.1.0...calcom-v0.2.0) (2026-07-27)


### Features

* add breaks and holidays management to meeting types ([dd359ff](https://github.com/alekseibq/ai-for-developers-project-387/commit/dd359ffe18ed4712bd2ee828c872a0416dddf240)), closes [#2](https://github.com/alekseibq/ai-for-developers-project-387/issues/2)
* **ci:** add scheduled schedule-mark job ([147b4d8](https://github.com/alekseibq/ai-for-developers-project-387/commit/147b4d821f68b93c485b03ffee940e6ed7c312c3))
* **ci:** add scheduled schedule-mark job with /api/v1/schedule-mark endpoint ([e23bca7](https://github.com/alekseibq/ai-for-developers-project-387/commit/e23bca72482f64e94d3a790ab129bd7c839688da))
* **infra:** add release-please automated release workflow ([abfad59](https://github.com/alekseibq/ai-for-developers-project-387/commit/abfad59a820e02731a43ba818541abdef959aedc))
* **infra:** add release-please automated release workflow ([e2425ff](https://github.com/alekseibq/ai-for-developers-project-387/commit/e2425ff989a3b2b5082ac5c536c3fb46ac08da19))


### Bug Fixes

* **backend:** add mypy ignore for no-any-return in _parse_time ([128ed49](https://github.com/alekseibq/ai-for-developers-project-387/commit/128ed4933ba409ab8ec6d628b44715668bcc6715))
* **backend:** enable ruff and mypy linting on backend ([dad35aa](https://github.com/alekseibq/ai-for-developers-project-387/commit/dad35aa024cfb1f71c93a09010828118b328004a))
* **backend:** enable ruff and mypy linting on backend ([67a0027](https://github.com/alekseibq/ai-for-developers-project-387/commit/67a002799630c17fe80654a86e47d46db32beb16))
* **backend:** remove unused datetime import ([28bae58](https://github.com/alekseibq/ai-for-developers-project-387/commit/28bae58cd0f7ca99602e27711b68939bf1b7e971))
* **backend:** remove unused noqa PLR0917 directive ([c55b9d0](https://github.com/alekseibq/ai-for-developers-project-387/commit/c55b9d00b07de7daa70aa2644866dd9014ba49a8))
* **ci:** add fallback cron at minute 43 for schedule-mark ([b6620f9](https://github.com/alekseibq/ai-for-developers-project-387/commit/b6620f949913a3d5124df5f4a54fb84fdc7cd65b))
* **ci:** add fallback cron at minute 43 for schedule-mark ([4733166](https://github.com/alekseibq/ai-for-developers-project-387/commit/4733166cefaa88d50fad7755f27a62da973916a3)), closes [#13](https://github.com/alekseibq/ai-for-developers-project-387/issues/13)
* **ci:** add git auth with GITHUB_TOKEN for push ([6d1b1e3](https://github.com/alekseibq/ai-for-developers-project-387/commit/6d1b1e3fdfd4d39cb18508571213e2eb49ea36fe))
* **ci:** add use_github_token to opencode workflow ([fb6af93](https://github.com/alekseibq/ai-for-developers-project-387/commit/fb6af9375977ad593f489204fcc44f70c0295491))
* **ci:** add write permissions and GITHUB_TOKEN to opencode workflow ([3c90796](https://github.com/alekseibq/ai-for-developers-project-387/commit/3c907965e2cf7dcb95f6333b351f85653fbd463b))
* **ci:** checkout PR branch when comment is on a pull request ([e75d68f](https://github.com/alekseibq/ai-for-developers-project-387/commit/e75d68fd35d24c7cb51a4428a83b964c1a111c1d))
* **ci:** configure git identity in opencode workflow ([a419e73](https://github.com/alekseibq/ai-for-developers-project-387/commit/a419e730946d42d998442e388f0c119598971d9d))
* **ci:** enable git push from opencode action by removing persist-credentials: false ([95c23ca](https://github.com/alekseibq/ai-for-developers-project-387/commit/95c23ca32c1717e42d2160d0277d5909b30b967c))
* **ci:** enforce Conventional Commits format for opencode commits ([a0c4b6e](https://github.com/alekseibq/ai-for-developers-project-387/commit/a0c4b6e3f6e02ac4642f9b856a3d9b8ab724a84e))
* **ci:** force-reset PR branch to main before opencode runs ([4e308bc](https://github.com/alekseibq/ai-for-developers-project-387/commit/4e308bc8f81001737d24db55443793682809ac3f))
* **ci:** scope release-please to entire repo, not just frontend ([377221e](https://github.com/alekseibq/ai-for-developers-project-387/commit/377221efebe8a2b80abbddf6e98e5ac9d7e0992a))
* **ci:** scope release-please to entire repo, not just frontend ([14c21af](https://github.com/alekseibq/ai-for-developers-project-387/commit/14c21af5c7a1806467ed2efb0ab7cd4f33e4a032))
