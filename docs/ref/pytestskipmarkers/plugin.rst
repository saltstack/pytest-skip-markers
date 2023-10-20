=======
Markers
=======

.. _markers.destructive_test:

``destructive_test``
====================

.. py:decorator:: pytest.mark.destructive_test

    Skip the test if ``--run-destructive`` is not passed to pytest on the CLI.

    Use this mark when the test does something destructive to the system where the tests are running, for example,
    adding or removing a user, changing a user password.

    .. admonition:: Note

        Do not use this marker if all the test does is add/remove/change files in the test suite temporary directory

    .. code-block:: python

        @pytest.mark.destructive_test
        def test_func():
            assert True



.. _markers.expensive_test:

``expensive_test``
==================

.. py:decorator:: pytest.mark.expensive_test

    Skip the test if ``--run-expensive`` is not passed to pytest on the CLI.

    Use this test when the test does something expensive(as in monetary expensive), like creating a virtual
    machine on a cloud provider, etc.

    .. code-block:: python

        @pytest.mark.expensive_test
        def test_func():
            assert True



.. _markers.skip_if_not_root:

``skip_if_not_root``
====================

.. py:decorator:: pytest.mark.skip_if_not_root

    Skip the test if the user running the test suite is not ``root`` or ``Administrator`` on Windows.

    .. code-block:: python

        @pytest.mark.skip_if_not_root
        def test_func():
            assert True

    Look :py:func:`here <pytestskipmarkers.utils.markers.skip_if_not_root>` for the full function signature.



.. _markers.skip_if_binaries_missing:

``skip_if_binaries_missing``
============================

.. py:decorator:: pytest.mark.skip_if_binaries_missing(\*binaries, check_all=True, reason=None)

    :param str binaries:
        Any argument passed must be a :py:class:`str` which is the name of the binary
        check for presence in the path. Multiple arguments can be passed.
    :keyword bool check_all:
        If ``check_all`` is :py:const:`True`, the default, all binaries must exist.
        If ``check_all`` is :py:class:`False`, then only one the passed binaries needs to be found.
        Useful when, for example, passing a list of python interpreter names(python3.5,
        python3, python), where only one needs to exist.
    :keyword str reason:
        The skip reason.

    Skip tests if binaries are not found in path.

    .. code-block:: python

        @pytest.mark.skip_if_binaries_missing("sshd")
        def test_func():
            assert True


        @pytest.mark.skip_if_binaries_missing("python3.7", "python3", "python", check_all=False)
        def test_func():
            assert True

    Look :py:func:`here <pytestskipmarkers.utils.markers.skip_if_binaries_missing>` for the full function signature.



.. _markers.requires_network:

``requires_network``
====================



.. _markers.skip_on_windows:

``skip_on_windows``
===================

.. py:decorator:: pytest.mark.skip_on_windows(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on windows.

    .. code-block:: python

        @pytest.mark.skip_on_windows
        def test_func():
            assert True



.. _markers.skip_unless_on_windows:

``skip_unless_on_windows``
==========================

.. py:decorator:: pytest.mark.skip_unless_on_windows(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on windows.

    .. code-block:: python

        @pytest.mark.skip_unless_on_windows
        def test_func():
            assert True



.. _markers.skip_on_linux:

``skip_on_linux``
=================

.. py:decorator:: pytest.mark.skip_on_linux(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on linux.

    .. code-block:: python

        @pytest.mark.skip_on_linux
        def test_func():
            assert True



.. _markers.skip_unless_on_linux:

``skip_unless_on_linux``
========================

.. py:decorator:: pytest.mark.skip_unless_on_linux(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on linux.

    .. code-block:: python

        @pytest.mark.skip_unless_on_linux
        def test_func():
            assert True



.. _markers.skip_on_darwin:

``skip_on_darwin``
==================

.. py:decorator:: pytest.mark.skip_on_darwin(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on darwin.

    .. code-block:: python

        @pytest.mark.skip_on_darwin
        def test_func():
            assert True



.. _markers.skip_unless_on_darwin:

``skip_unless_on_darwin``
=========================

.. py:decorator:: pytest.mark.skip_unless_on_darwin(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on darwin.

    .. code-block:: python

        @pytest.mark.skip_unless_on_darwin
        def test_func():
            assert True



.. _markers.skip_on_sunos:

``skip_on_sunos``
=================

.. py:decorator:: pytest.mark.skip_on_sunos(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on sunos.

    .. code-block:: python

        @pytest.mark.skip_on_sunos
        def test_func():
            assert True



.. _markers.skip_unless_on_sunos:

``skip_unless_on_sunos``
========================

.. py:decorator:: pytest.mark.skip_unless_on_sunos(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on sunos.

    .. code-block:: python

        @pytest.mark.skip_unless_on_sunos
        def test_func():
            assert True



.. _markers.skip_on_smartos:

``skip_on_smartos``
===================

.. py:decorator:: pytest.mark.skip_on_smartos(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on smartos.

    .. code-block:: python

        @pytest.mark.skip_on_smartos
        def test_func():
            assert True



.. _markers.skip_unless_on_smartos:

``skip_unless_on_smartos``
==========================

.. py:decorator:: pytest.mark.skip_unless_on_smartos(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on smartos.

    .. code-block:: python

        @pytest.mark.skip_unless_on_smartos
        def test_func():
            assert True



.. _markers.skip_on_freebsd:

``skip_on_freebsd``
===================

.. py:decorator:: pytest.mark.skip_on_freebsd(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on freebsd.

    .. code-block:: python

        @pytest.mark.skip_on_freebsd
        def test_func():
            assert True



.. _markers.skip_unless_on_freebsd:

``skip_unless_on_freebsd``
==========================

.. py:decorator:: pytest.mark.skip_unless_on_freebsd(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on freebsd.

    .. code-block:: python

        @pytest.mark.skip_unless_on_freebsd
        def test_func():
            assert True



.. _markers.skip_on_netbsd:

``skip_on_netbsd``
==================

.. py:decorator:: pytest.mark.skip_on_netbsd(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on netbsd.

    .. code-block:: python

        @pytest.mark.skip_on_netbsd
        def test_func():
            assert True



.. _markers.skip_unless_on_netbsd:

``skip_unless_on_netbsd``
=========================

.. py:decorator:: pytest.mark.skip_unless_on_netbsd(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on netbsd.

    .. code-block:: python

        @pytest.mark.skip_unless_on_netbsd
        def test_func():
            assert True



.. _markers.skip_on_openbsd:

``skip_on_openbsd``
===================

.. py:decorator:: pytest.mark.skip_on_openbsd(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on openbsd.

    .. code-block:: python

        @pytest.mark.skip_on_openbsd
        def test_func():
            assert True



.. _markers.skip_unless_on_openbsd:

``skip_unless_on_openbsd``
==========================

.. py:decorator:: pytest.mark.skip_unless_on_openbsd(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on openbsd.

    .. code-block:: python

        @pytest.mark.skip_unless_on_openbsd
        def test_func():
            assert True



.. _markers.skip_on_aix:

``skip_on_aix``
===============

.. py:decorator:: pytest.mark.skip_on_aix(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on aix.

    .. code-block:: python

        @pytest.mark.skip_on_aix
        def test_func():
            assert True



.. _markers.skip_unless_on_aix:

``skip_unless_on_aix``
======================

.. py:decorator:: pytest.mark.skip_unless_on_aix(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on aix.

    .. code-block:: python

        @pytest.mark.skip_unless_on_aix
        def test_func():
            assert True



.. _markers.skip_on_aarch64:

``skip_on_aarch64``
===================

.. py:decorator:: pytest.mark.skip_on_aarch64(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on aarch64.

    .. code-block:: python

        @pytest.mark.skip_on_aarch64
        def test_func():
            assert True



.. _markers.skip_unless_on_aarch64:

``skip_unless_on_aarch64``
==========================

.. py:decorator:: pytest.mark.skip_unless_on_aarch64(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on aarch64.

    .. code-block:: python

        @pytest.mark.skip_unless_on_aarch64
        def test_func():
            assert True



.. _markers.skip_on_photonos:

``skip_on_photonos``
====================

.. py:decorator:: pytest.mark.skip_on_photonos(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on PhotonOS.

    .. code-block:: python

        @pytest.mark.skip_on_photonos
        def test_func():
            assert True



.. _markers.skip_unless_on_photonos:

``skip_unless_on_photonos``
===========================

.. py:decorator:: pytest.mark.skip_unless_on_photonos(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is running on PhotonOS.

    .. code-block:: python

        @pytest.mark.skip_unless_on_photonos
        def test_func():
            assert True



.. _markers.skip_on_spawning_platform:

``skip_on_spawning_platform``
=============================

.. py:decorator:: pytest.mark.skip_on_spawning_platform(reason=None)

    :keyword str reason: The skip reason

    Skip test if test suite is running on a platfor which defaults
    multiprocessing to ``spawn``.

    .. code-block:: python

        @pytest.mark.skip_on_spawning_platform
        def test_func():
            assert True



.. _markers.skip_unless_on_spawning_platform:

``skip_unless_on_spawning_platform``
====================================

.. py:decorator:: pytest.mark.skip_unless_on_spawning_platform(reason=None)

    :keyword str reason: The skip reason

    Skip test unless the test suite is not running on a platform which
    defaults multiprocessing to ``spawn``.

    .. code-block:: python

        @pytest.mark.skip_unless_on_spawning_platform
        def test_func():
            assert True



.. _markers.skip_on_env:

``skip_on_env``
===============

.. py:decorator:: pytest.mark.skip_on_env(envvar, present=True, eq=None, ne=None)

    :keyword str varname: The environment variable to check
    :keyword bool present:
        When ``True``, skip if variable is present in the environment.
        When ``False``, skip if variable is not present in the environment.
    :keyword str eq: Skips when the variable is present in the environment and matches this value.
    :keyword str ne: Skips when the variable is present in the environment and does not match this value.
    :keyword str reason: The skip reason

    Skip test based on the presence/absence of `envvar` in the environment and it's value.

    .. code-block:: python

        @pytest.mark.skip_on_env("FLAKY_TEST")
        def test_func():
            assert True


        @pytest.mark.skip_on_env("FLAKY_TEST", eq="1")
        def test_func():
            assert True


        @pytest.mark.skip_on_env("FLAKY_TEST", present=False)
        def test_func():
            assert True



.. _markers.skip_on_fips_enabled_platform:

``skip_on_fips_enabled_platform``
=================================

.. py:decorator:: pytest.mark.skip_on_fips_enabled_platform(reason=None)

    :keyword str reason: The skip reason

    Skip tests if the underlying OS has FIPS enabled.

    .. code-block:: python

        @pytest.mark.skip_on_fips_enabled_platform
        def test_func():
            assert True



.. _markers.skip_on_platforms:

``skip_on_platforms``
=====================

.. py:decorator:: pytest.mark.skip_on_platforms(**platforms, reason=None)

    :keyword bool windows: Skip on windows if :py:const:`True`
    :keyword bool linux: Skip on linux if :py:const:`True`
    :keyword bool darwin: Skip on darwin if :py:const:`True`
    :keyword bool sunos: Skip on sunos if :py:const:`True`
    :keyword bool smartos: Skip on smartos if :py:const:`True`
    :keyword bool freebsd: Skip on freebsd if :py:const:`True`
    :keyword bool netbsd: Skip on netbsd if :py:const:`True`
    :keyword bool openbsd: Skip on openbsd if :py:const:`True`
    :keyword bool aix: Skip on aix if :py:const:`True`
    :keyword bool aarch64: Skip on aarch64 if :py:const:`True`
    :keyword bool photonos: Skip on photonos if :py:const:`True`
    :keyword bool spawning:
        Skip on platforms for which multiprocessing defaults to ``spawn``
        if :py:const:`True`
    :keyword str reason: The skip reason

    Pass :py:const:`True` to any of the platforms defined as keyword arguments to skip the test when running on that
    platform

    .. code-block:: python

        @pytest.mark.skip_on_platforms(windows=True, darwin=True)
        def test_func():
            assert True



.. _markers.skip_unless_on_platforms:

``skip_unless_on_platforms``
============================

.. py:decorator:: pytest.mark.skip_unless_on_platforms(**platforms, reason=None)

    :keyword bool windows: Skip unless on windows if :py:const:`True`
    :keyword bool linux: Skip unless on linux if :py:const:`True`
    :keyword bool darwin: Skip unless on darwin if :py:const:`True`
    :keyword bool sunos: Skip unless on sunos if :py:const:`True`
    :keyword bool smartos: Skip unless on smartos if :py:const:`True`
    :keyword bool freebsd: Skip unless on freebsd if :py:const:`True`
    :keyword bool netbsd: Skip unless on netbsd if :py:const:`True`
    :keyword bool openbsd: Skip unless on openbsd if :py:const:`True`
    :keyword bool aix: Skip unless on aix if :py:const:`True`
    :keyword bool aarch64: Skip on aarch64 if :py:const:`True`
    :keyword bool photonos: Skip on photonos if :py:const:`True`
    :keyword bool spawning:
        Skip on platforms for which multiprocessing does not default to
        ``spawn`` if :py:const:`True`
    :keyword str reason: The skip reason

    Pass :py:const:`True` to any of the platforms defined as keyword arguments to skip the test when not running on
    that platform

    .. code-block:: python

        @pytest.mark.skip_unless_on_platforms(windows=True, darwin=True)
        def test_func():
            assert True
