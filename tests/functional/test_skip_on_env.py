# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the ``@pytest.mark.skip_on_env`` marker.
"""
import os
from unittest import mock


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
