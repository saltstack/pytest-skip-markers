# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.skip_if_binaries_missing`` marker.
"""
import os
import sys

import pytest


@pytest.fixture
def python_binary():
    return os.path.basename(sys.executable)


def test_skipped(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing("python9")
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_skipped_multiple_binaries(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing("python", "python9", check_all=True)
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(skipped=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_not_skipped(pytester, python_binary):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing("{}")
        def test_one():
            assert True
        """.format(
            python_binary
        )
    )
    res = pytester.runpytest_subprocess("-ra", "-vv")
    res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_not_skipped_multiple_binaries(pytester, python_binary):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing("{}", "pip")
        def test_one():
            assert True
        """.format(
            python_binary
        )
    )
    res = pytester.runpytest_subprocess("-ra", "-vv")
    res.assert_outcomes(passed=1)
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_single_non_existing_with_deprecated_message(pytester, python_binary):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing("python9", message="Dam!")
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest_subprocess("-ra", "-vv")
    res.assert_outcomes(skipped=1)
    res.stdout.fnmatch_lines(
        [
            """*: PytestWarning: Please stop passing 'message="Dam!"' and instead pass 'reason="Dam!"'"""
        ]
    )


def test_no_arguments(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=1)
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The 'skip_if_binaries_missing' marker needs at least one binary name to be passed"
        ]
    )


def test_multiple_binaries_as_single_list_arg(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_if_binaries_missing(["python", "python9"])
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    res.assert_outcomes(errors=1)
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The 'skip_if_binaries_missing' marker only accepts strings as arguments. If you are "
            "trying to pass multiple binaries, each binary should be an separate argument."
        ]
    )
