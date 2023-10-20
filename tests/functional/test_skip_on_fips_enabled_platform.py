# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.skip_on_fips_enabled_platform`` marker.
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


def test_skip_on_fips_enabled_platform_skipped(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_fips_enabled_platform
        def test_one():
            assert True
        """
    )
    with mock.patch("pytestskipmarkers.utils.platform.is_fips_enabled", return_value=True):
        res = pytester.runpytest()
        res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_skip_on_fips_enabled_platform_not_skipped(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_fips_enabled_platform
        def test_one():
            assert True
        """
    )
    with mock.patch("pytestskipmarkers.utils.platform.is_fips_enabled", return_value=False):
        res = pytester.runpytest_inprocess("-ra", "-vv")
        res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_error_on_args_or_kwargs(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_fips_enabled_platform("arg")
        def test_one():
            assert True

        @pytest.mark.skip_on_fips_enabled_platform(kwarg="arg")
        def test_two():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=2)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The skip_on_fips_enabled_platform marker does not accept any arguments",
            "*UsageError: The skip_on_fips_enabled_platform marker only accepts 'reason' as a keyword argument.",
        ]
    )
