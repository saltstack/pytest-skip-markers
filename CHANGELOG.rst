.. _changelog:

=========
Changelog
=========

Versions follow `Semantic Versioning <https://semver.org>`_ (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions with advance notice in the
**Deprecations** section of releases.

.. towncrier-draft-entries::

.. towncrier release notes start

1.5.0 (2023-10-20)
==================

Features
--------

- Add a ``skip_on_fips_enabled_platform`` marker (`#30 <https://github.com/saltstack/pytest-skip-markers/issues/30>`_)


1.4.1 (2023-07-31)
==================

Improvements
------------

- Stop using deprecated `@pytest.mark.trylast` (`#24 <https://github.com/saltstack/pytest-skip-markers/issues/24>`_)


Trivial/Internal Changes
------------------------

- Several minor fixes & improvements:

  * Update pre-commit hooks versions
  * Update copyright headers
  * Update workflows
  * Add dependabot config to update GH Actions workflow versions (`#25 <https://github.com/saltstack/pytest-skip-markers/issues/25>`_)


1.4.0 (2022-12-20)
==================

Breaking Changes
----------------

- Drop support for python versions older than 3.7 (`#22 <https://github.com/saltstack/pytest-skip-markers/issues/22>`_)


Improvements
------------

- Don't cache the functions in `pytestskipmarkers.utils.platform` (`#21 <https://github.com/saltstack/pytest-skip-markers/issues/21>`_)


Trivial/Internal Changes
------------------------

- Updated pre-commit hook versions and added missing `long_description_content_type` to `setup.cfg` (`#23 <https://github.com/saltstack/pytest-skip-markers/issues/23>`_)


1.3.0 (2022-05-09)
==================

Features
--------

- Support skipping all test cases that access the Internet by setting the
  environment variable `NO_INTERNET`. This is useful to make the test run
  reproducible and robust for future runs (to avoid breaking in case some random
  service on the Internet changes). (`#16 <https://github.com/saltstack/pytest-skip-markers/issues/16>`_)


1.2.0 (2022-02-22)
==================

Features
--------

- Added ``pytest.mark.skip_on_photonos`` and ``pytest.mark.skip_unless_on_photonos`` markers (`#13 <https://github.com/saltstack/pytest-skip-markers/issues/13>`_)
- Added the ``pytest.mark.skip_on_env`` marker. (`#14 <https://github.com/saltstack/pytest-skip-markers/issues/14>`_)


1.1.3 (2022-02-16)
==================

Bug Fixes
---------

- Fixed issue with ``sdist`` recompression for reproducible packages not iterating though subdirectories contents. (`#12 <https://github.com/saltstack/pytest-skip-markers/issues/12>`_)


1.1.2 (2022-02-05)
==================

Bug Fixes
---------

- Set lower required python to `3.5.2` and avoid issues with `flake8-typing-imports`. (`#10 <https://github.com/saltstack/pytest-skip-markers/issues/10>`_)


1.1.1 (2022-02-05)
==================

Bug Fixes
---------

- Allow installing on older minior versions of Py3.5. Looking at you Debian. (`#10 <https://github.com/saltstack/pytest-skip-markers/issues/10>`_)


1.1.0 (2022-01-26)
==================

Improvements
------------

- Maintain the skip location under Pytest >= 7.0.x (`#7 <https://github.com/saltstack/pytest-skip-markers/issues/7>`_)
- The plugin is now fully typed (`#8 <https://github.com/saltstack/pytest-skip-markers/issues/8>`_)


Trivial/Internal Changes
------------------------

- Reproducible builds

  * Fix copyright headers hook
  * ``towncrier`` now uses ``issue_format`` (`#7 <https://github.com/saltstack/pytest-skip-markers/issues/7>`_)


skip-markers 1.0.0 (2021-10-04)
===============================

Features
--------

- First public release of the Pytest Skip Markers Plugin
