# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.skip_on_env`` marker.
"""
import os
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

        @pytest.mark.skip_on_env("FOOBAR")
        def test_one():
            assert True
        """
    )
    with mock.patch.dict(os.environ, FOOBAR="1"):
        res = pytester.runpytest_inprocess()
        res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_not_skipped(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_env("FOOBAR", eq="2")
        def test_one():
            assert True
        """
    )
    with mock.patch.dict(os.environ, FOOBAR="1"):
        res = pytester.runpytest_inprocess()
        res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_error_on_missing_arg(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_env
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The 'skip_on_env' marker needs at least one argument to be passed, "
            "the environment variable name.",
        ]
    )


def test_error_on_multiple_args(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_env("FOOBAR", "BARFOO", eq="2")
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The 'skip_on_env' only accepts one argument, the environment variable name.",
        ]
    )


def test_error_on_bad_kwargs(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_env("FOOBAR", eq="2", bar=True)
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The 'skip_on_env' marker only accepts 'present', 'eq', 'ne' and 'reason' "
            "as keyword arguments.",
        ]
    )
