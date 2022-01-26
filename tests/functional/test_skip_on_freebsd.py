# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.skip_on_freebsd`` marker.
"""
from unittest import mock


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
