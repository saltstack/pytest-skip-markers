# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the "skip_on_env" marker helper.
"""
import logging
import os
from unittest import mock

import pytest

import pytestskipmarkers.utils.markers as markers

log = logging.getLogger(__name__)


def test_not_present_and_eq():
    with pytest.raises(pytest.UsageError):
        markers.skip_on_env("FOOBAR", present=False, eq="1")


def test_not_present_and_ne():
    with pytest.raises(pytest.UsageError):
        markers.skip_on_env("FOOBAR", present=False, ne="1")


def test_present_and_eq_and_ne():
    with pytest.raises(pytest.UsageError):
        markers.skip_on_env("FOOBAR", eq="1", ne="1")


def test_present_true():
    with mock.patch.dict(os.environ, FOO="1"):
        assert markers.skip_on_env("FOO") is not None


def test_present_false():
    assert markers.skip_on_env(__name__.upper(), present=False) is not None


def test_present_true_and_eq():
    with mock.patch.dict(os.environ, FOO="1"):
        assert markers.skip_on_env("FOO", eq="1") is not None
        assert markers.skip_on_env("FOO", eq="2") is None


def test_present_true_and_ne():
    with mock.patch.dict(os.environ, FOO="1"):
        assert markers.skip_on_env("FOO", ne="2") is not None
        assert markers.skip_on_env("FOO", ne="1") is None
