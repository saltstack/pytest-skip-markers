.. _changelog:

=========
Changelog
=========

Versions follow `Semantic Versioning <https://semver.org>`_ (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions with advance notice in the
**Deprecations** section of releases.

.. towncrier-draft-entries::

.. towncrier release notes start

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
