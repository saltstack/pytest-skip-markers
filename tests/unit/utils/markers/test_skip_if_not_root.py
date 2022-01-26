# Copyright 2021-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Test the "skip_if_not_root" marker helper.
"""
import sys
from unittest import mock

import pytestskipmarkers.utils.markers


def test_when_root():
    if sys.platform.startswith("win"):
        with mock.patch("pytestskipmarkers.utils.win_functions.is_admin", return_value=True):
            assert pytestskipmarkers.utils.markers.skip_if_not_root() is None
    else:
        with mock.patch("os.getuid", return_value=0):
            assert pytestskipmarkers.utils.markers.skip_if_not_root() is None


def test_when_not_root():
    if sys.platform.startswith("win"):
        with mock.patch("pytestskipmarkers.utils.win_functions.is_admin", return_value=False):
            assert pytestskipmarkers.utils.markers.skip_if_not_root() is not None
    else:
        with mock.patch("os.getuid", return_value=1):
            assert pytestskipmarkers.utils.markers.skip_if_not_root() is not None
