# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.skip_on_freebsd`` marker.
"""
import sys
from unittest import mock

import pytest

pytestmark = [
    pytest.mark.skipif(
        sys.platform.startswith("win")
        and sys.version_info >= (3, 8)
        and sys.version_info < (3, 10),
        reason="PyTest's capture and pytester.runpytest_inprocess looks broken on Windows and Py(>3.8,<3.10)",
    ),
]


def test_skipped(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_freebsd
        def test_one():
            assert True
        """
    )
    return_value = True
    with mock.patch("pytestskipmarkers.utils.platform.is_freebsd", return_value=return_value):
        res = pytester.runpytest_inprocess()
        res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_not_skipped(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_freebsd
        def test_one():
            assert True
        """
    )
    return_value = False
    with mock.patch("pytestskipmarkers.utils.platform.is_freebsd", return_value=return_value):
        res = pytester.runpytest_inprocess()
        res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_skip_reason(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_freebsd(reason='Because!')
        def test_one():
            assert True
        """
    )
    return_value = True
    with mock.patch("pytestskipmarkers.utils.platform.is_freebsd", return_value=return_value):
        res = pytester.runpytest_inprocess("-ra", "-s", "-vv")
        res.assert_outcomes(skipped=1)
    res.stdout.fnmatch_lines(["SKIPPED * test_skip_reason.py:*: Because!"])


def test_error_on_args_or_kwargs(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_freebsd("arg")
        def test_one():
            assert True

        @pytest.mark.skip_on_freebsd(kwarg="arg")
        def test_two():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=2)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The skip_on_freebsd marker does not accept any arguments",
            "*UsageError: The skip_on_freebsd marker only accepts 'reason' as a keyword argument.",
        ]
    )
